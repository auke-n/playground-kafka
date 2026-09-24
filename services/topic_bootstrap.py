"""Create the learning topics on a managed Kafka cluster."""
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from services.common import configure_logging, msk_python_config
configure_logging()
topics = ["order.created", "payment.requested", "payment.completed", "order.fulfilled", "order.retry", "order.dlq"]
admin = KafkaAdminClient(**msk_python_config())
try:
    admin.create_topics([NewTopic(topic, num_partitions=3, replication_factor=1) for topic in topics])
except TopicAlreadyExistsError:
    pass
finally:
    admin.close()
