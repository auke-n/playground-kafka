"""Consumes order events and emits payment lifecycle events."""

import logging

from services.common import configure_logging, consumer, decode, new_event, producer, publish

configure_logging()
logger = logging.getLogger("payment-processor")


def process() -> None:
    input_consumer = consumer("payment-processor-v1")
    output_producer = producer()
    input_consumer.subscribe(["order.created"])
    logger.info("subscribed topic=order.created group=payment-processor-v1")
    try:
        while True:
            message = input_consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logger.error("consumer error=%s", message.error())
                continue
            try:
                event = decode(message)
                order_id = event["correlation_id"]
            except (KeyError, UnicodeDecodeError, ValueError) as error:
                raw_value = message.value().decode("utf-8", errors="replace")
                raw_key = message.key().decode("utf-8", errors="replace") if message.key() else "unknown"
                publish(output_producer, "order.dlq", new_event("order.invalid_event", raw_key, {"raw_value": raw_value, "reason": str(error)}))
                input_consumer.commit(message=message, asynchronous=False)
                logger.warning("invalid_event_sent_to_dlq partition=%s offset=%s", message.partition(), message.offset())
                continue
            failure = event["data"].get("simulate_payment_failure", "none")
            if failure == "terminal":
                publish(output_producer, "order.dlq", new_event("order.payment_failed", order_id, {"source_event": event, "reason": "terminal demo failure"}))
                logger.warning("sent_to_dlq order_id=%s partition=%s offset=%s", order_id, message.partition(), message.offset())
            elif failure == "transient":
                publish(output_producer, "order.retry", new_event("order.payment_retry", order_id, {"source_event": event, "reason": "transient demo failure"}))
                logger.warning("sent_to_retry order_id=%s partition=%s offset=%s", order_id, message.partition(), message.offset())
            else:
                publish(output_producer, "payment.requested", new_event("payment.requested", order_id, {"order_id": order_id, "amount": event["data"]["amount"]}))
                publish(output_producer, "payment.completed", new_event("payment.completed", order_id, {"order_id": order_id, "amount": event["data"]["amount"], "status": "paid"}))
                logger.info("payment_completed order_id=%s partition=%s offset=%s", order_id, message.partition(), message.offset())
            input_consumer.commit(message=message, asynchronous=False)
    finally:
        input_consumer.close()
        output_producer.flush(10)


if __name__ == "__main__":
    process()
