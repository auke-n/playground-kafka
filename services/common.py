"""Shared Kafka helpers for the learning services."""

import json
import logging
import os
import time
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from confluent_kafka import Consumer, Producer

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:19092")


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def new_event(event_type: str, order_id: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": str(uuid4()),
        "event_type": event_type,
        "occurred_at": datetime.now(UTC).isoformat(),
        "correlation_id": order_id,
        "data": data,
    }


def producer() -> Producer:
    return Producer(
        {
            "bootstrap.servers": BOOTSTRAP_SERVERS,
            "client.id": os.getenv("SERVICE_NAME", "learning-lab"),
            "acks": "1",
            "linger.ms": 0,
            "queue.buffering.max.ms": 0,
        }
    )


def publish(client: Producer, topic: str, event: dict[str, Any]) -> dict[str, Any]:
    delivery_error: list[str] = []
    delivery_metadata: dict[str, Any] = {}

    def delivered(error: Any, message: Any) -> None:
        if error is not None:
            delivery_error.append(str(error))
            return
        delivery_metadata.update({"topic": message.topic(), "partition": message.partition(), "offset": message.offset()})
        logging.getLogger("kafka.producer").info(
            "published topic=%s partition=%s offset=%s event_id=%s",
            message.topic(), message.partition(), message.offset(), event["event_id"],
        )

    client.produce(topic, key=event["correlation_id"], value=json.dumps(event), callback=delivered)
    deadline = time.monotonic() + 1
    while not delivery_error and not delivery_metadata and time.monotonic() < deadline:
        client.poll(0.01)
    if delivery_error:
        raise RuntimeError(f"Kafka delivery failed: {delivery_error[0]}")
    if not delivery_metadata:
        raise RuntimeError("Kafka delivery was not confirmed within one second")
    return delivery_metadata


def consumer(group_id: str) -> Consumer:
    return Consumer(
        {
            "bootstrap.servers": BOOTSTRAP_SERVERS,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "fetch.min.bytes": 1,
            "fetch.wait.max.ms": 50,
        }
    )


def decode(message: Any) -> dict[str, Any]:
    return json.loads(message.value().decode("utf-8"))
