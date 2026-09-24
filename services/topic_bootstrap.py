"""Create the learning topics on a managed Kafka cluster."""
from confluent_kafka.admin import AdminClient, NewTopic
from services.common import client_config, configure_logging
configure_logging()
topics = ["order.created", "payment.requested", "payment.completed", "order.fulfilled", "order.retry", "order.dlq"]
admin = AdminClient(client_config())
for name, future in admin.create_topics([NewTopic(topic, num_partitions=3, replication_factor=1) for topic in topics]).items():
    try: future.result()
    except Exception as error:
        if "TOPIC_ALREADY_EXISTS" not in str(error): raise
