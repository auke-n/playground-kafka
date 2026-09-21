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
order_details: dict[str, dict[str, object]] = {}
manual_stages: dict[str, set[str]] = {}
timeline_lock = Lock()
observer_stop = Event()


def observe_events() -> None:
    event_consumer = consumer("order-timeline-observer-v1")
    event_consumer.subscribe(["order.created", "payment.requested", "payment.completed", "order.fulfilled", "order.retry", "order.dlq"])
    try:
        while not observer_stop.is_set():
            message = event_consumer.poll(0.05)
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
    details = {"order_id": order_id, **request.model_dump(exclude={"order_id"})}
    event = new_event("order.created", order_id, details)
    try:
        publish(kafka_producer, "order.created", event)
    except RuntimeError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    with timeline_lock:
        order_details[order_id] = details
        manual_stages[order_id] = {"order.created"}
    return {"status": "accepted", "order_id": order_id, "event_id": event["event_id"]}


def publish_manual_stage(order_id: str, prerequisite: str, topic: str, event_type: str, data: dict[str, object]) -> dict[str, str]:
    with timeline_lock:
        if order_id not in order_details:
            raise HTTPException(status_code=404, detail="Create this order in the current UI session first.")
        if prerequisite not in manual_stages[order_id]:
            raise HTTPException(status_code=409, detail=f"Complete {prerequisite} first.")
        if topic in manual_stages[order_id]:
            return {"status": "already_completed", "order_id": order_id, "topic": topic}
    publish(kafka_producer, topic, new_event(event_type, order_id, data))
    with timeline_lock:
        manual_stages[order_id].add(topic)
    return {"status": "published", "order_id": order_id, "topic": topic}


@app.post("/orders/{order_id}/manual/payment-request")
def request_payment(order_id: str) -> dict[str, str]:
    return publish_manual_stage(order_id, "order.created", "payment.requested", "payment.requested", {"order_id": order_id, "amount": order_details.get(order_id, {}).get("amount")})


@app.post("/orders/{order_id}/manual/payment-complete")
def complete_payment(order_id: str) -> dict[str, str]:
    return publish_manual_stage(order_id, "payment.requested", "payment.completed", "payment.completed", {"order_id": order_id, "amount": order_details.get(order_id, {}).get("amount"), "status": "paid"})


@app.post("/orders/{order_id}/manual/fulfill")
def fulfill_order(order_id: str) -> dict[str, str]:
    return publish_manual_stage(order_id, "payment.completed", "order.fulfilled", "order.fulfilled", {"order_id": order_id, "status": "fulfilled"})
