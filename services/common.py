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


def is_msk_iam() -> bool:
    return os.getenv("KAFKA_AUTH_MODE") == "msk_iam"


def msk_python_config(group_id: str | None = None) -> dict[str, Any]:
    from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
    from kafka.sasl.oauth import AbstractTokenProvider

    class MskTokenProvider(AbstractTokenProvider):
        def token(self) -> str:
            return MSKAuthTokenProvider.generate_auth_token(os.environ["AWS_REGION"])[0]

    config: dict[str, Any] = {
        "bootstrap_servers": BOOTSTRAP_SERVERS.split(","),
        "security_protocol": "SASL_SSL",
        "sasl_mechanism": "OAUTHBEARER",
        "sasl_oauth_token_provider": MskTokenProvider(),
        "client_id": os.getenv("SERVICE_NAME", "learning-lab"),
    }
    if group_id:
        config.update({"group_id": group_id, "auto_offset_reset": "earliest", "enable_auto_commit": False})
    return config


class MskMessage:
    def __init__(self, record: Any): self.record = record
    def error(self) -> None: return None
    def value(self) -> bytes: return self.record.value
    def key(self) -> bytes | None: return self.record.key
    def topic(self) -> str: return self.record.topic
    def partition(self) -> int: return self.record.partition
    def offset(self) -> int: return self.record.offset


class MskProducer:
    def __init__(self):
        from kafka import KafkaProducer
        self.client = KafkaProducer(**msk_python_config())
    def produce(self, topic: str, key: str, value: str, callback: Any) -> None:
        metadata = self.client.send(topic, key=key.encode(), value=value.encode()).get(timeout=10)
        callback(None, type("Delivery", (), {"topic": lambda _: metadata.topic, "partition": lambda _: metadata.partition, "offset": lambda _: metadata.offset})())
    def poll(self, _: float) -> None: return None
    def flush(self, timeout: float | None = None) -> None: self.client.flush(timeout=timeout)


class MskConsumer:
    def __init__(self, group_id: str):
        from kafka import KafkaConsumer
        self.client = KafkaConsumer(**msk_python_config(group_id))
    def subscribe(self, topics: list[str]) -> None: self.client.subscribe(topics)
    def poll(self, timeout: float) -> MskMessage | None:
        records = self.client.poll(timeout_ms=max(1, int(timeout * 1000)), max_records=1)
        return MskMessage(next(iter(next(iter(records.values()))))) if records else None
    def commit(self, **_: Any) -> None: self.client.commit()
    def close(self) -> None: self.client.close()


def client_config() -> dict[str, Any]:
    config: dict[str, Any] = {"bootstrap.servers": BOOTSTRAP_SERVERS, "client.id": os.getenv("SERVICE_NAME", "learning-lab")}
    if os.getenv("KAFKA_AUTH_MODE") == "msk_iam":
        from aws_msk_iam_sasl_signer import MSKAuthTokenProvider

        def oauth_callback(_: str) -> tuple[str, float]:
            token, expiry_ms = MSKAuthTokenProvider.generate_auth_token(os.environ["AWS_REGION"])
            return token, expiry_ms / 1000

        config.update({"security.protocol": "SASL_SSL", "sasl.mechanisms": "OAUTHBEARER", "oauth_cb": oauth_callback})
    return config


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
    if is_msk_iam():
        return MskProducer()  # type: ignore[return-value]
    return Producer(client_config() | {
            "acks": "1",
            "linger.ms": 0,
            "queue.buffering.max.ms": 0,
        })


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
    if is_msk_iam():
        return MskConsumer(group_id)  # type: ignore[return-value]
    return Consumer(client_config() | {
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "fetch.min.bytes": 1,
            "fetch.wait.max.ms": 50,
        })


def decode(message: Any) -> dict[str, Any]:
    return json.loads(message.value().decode("utf-8"))
