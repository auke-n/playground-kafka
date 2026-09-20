"""HTTP producer for order-created events."""

from contextlib import asynccontextmanager
from pathlib import Path
from threading import Event, Lock, Thread
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from services.common import configure_logging, consumer, decode, new_event, producer, publish

configure_logging()
kafka_producer = producer()
timeline: dict[str, list[dict[str, object]]] = {}
timeline_lock = Lock()
observer_stop = Event()


def observe_events() -> None:
    event_consumer = consumer("order-timeline-observer-v1")
    event_consumer.subscribe(["order.created", "payment.requested", "payment.completed", "order.fulfilled", "order.retry", "order.dlq"])
    try:
        while not observer_stop.is_set():
            message = event_consumer.poll(0.5)
            if message is None or message.error():
                continue
            try:
                event = decode(message)
                order_id = event["correlation_id"]
                stage = {"topic": message.topic(), "event_type": event["event_type"], "occurred_at": event["occurred_at"], "partition": message.partition(), "offset": message.offset()}
                with timeline_lock:
                    timeline.setdefault(order_id, []).append(stage)
            except (KeyError, UnicodeDecodeError, ValueError) as error:
                logging.getLogger("timeline-observer").warning(
                    "ignored_invalid_event topic=%s partition=%s offset=%s error=%s",
                    message.topic(), message.partition(), message.offset(), error,
                )
            finally:
                event_consumer.commit(message=message, asynchronous=False)
    finally:
        event_consumer.close()


class OrderRequest(BaseModel):
    order_id: str | None = Field(default=None, min_length=1)
    amount: float = Field(gt=0)
    item: str = Field(min_length=1)
    simulate_payment_failure: Literal["none", "transient", "terminal"] = "none"


@asynccontextmanager
async def lifespan(_: FastAPI):
    observer_stop.clear()
    observer_thread = Thread(target=observe_events, daemon=True)
    observer_thread.start()
    yield
    observer_stop.set()
    observer_thread.join(timeout=2)
    kafka_producer.flush(10)


app = FastAPI(title="Kafka Learning Lab Order API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/orders/{order_id}/timeline")
def order_timeline(order_id: str) -> dict[str, object]:
    with timeline_lock:
        return {"order_id": order_id, "events": sorted(timeline.get(order_id, []), key=lambda event: str(event["occurred_at"]))}


@app.post("/orders", status_code=status.HTTP_202_ACCEPTED)
def create_order(request: OrderRequest) -> dict[str, str]:
    order_id = request.order_id or f"order-{uuid4()}"
    event = new_event("order.created", order_id, {"order_id": order_id, **request.model_dump(exclude={"order_id"})})
    try:
        publish(kafka_producer, "order.created", event)
    except RuntimeError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    return {"status": "accepted", "order_id": order_id, "event_id": event["event_id"]}
