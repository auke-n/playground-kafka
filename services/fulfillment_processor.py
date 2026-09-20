"""Consumes completed payments and emits fulfilled-order events."""

import logging

from services.common import configure_logging, consumer, decode, new_event, producer, publish

configure_logging()
logger = logging.getLogger("fulfillment-processor")


def process() -> None:
    input_consumer = consumer("fulfillment-processor-v1")
    output_producer = producer()
    input_consumer.subscribe(["payment.completed"])
    logger.info("subscribed topic=payment.completed group=fulfillment-processor-v1")
    try:
        while True:
            message = input_consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logger.error("consumer error=%s", message.error())
                continue
            event = decode(message)
            order_id = event["correlation_id"]
            publish(output_producer, "order.fulfilled", new_event("order.fulfilled", order_id, {"order_id": order_id, "status": "fulfilled"}))
            input_consumer.commit(message=message, asynchronous=False)
            logger.info("order_fulfilled order_id=%s partition=%s offset=%s", order_id, message.partition(), message.offset())
    finally:
        input_consumer.close()
        output_producer.flush(10)


if __name__ == "__main__":
    process()
