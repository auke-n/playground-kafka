#!/usr/bin/env bash
set -euo pipefail

bootstrap_server="kafka:19092"

create_topic() {
  local topic_name="$1"
  local partition_count="$2"

  /opt/kafka/bin/kafka-topics.sh \
    --bootstrap-server "${bootstrap_server}" \
    --create \
    --if-not-exists \
    --topic "${topic_name}" \
    --partitions "${partition_count}" \
    --replication-factor 1 \
    --config retention.ms=604800000
}

create_topic "order.created" 3
create_topic "payment.requested" 3
create_topic "payment.completed" 3
create_topic "order.fulfilled" 3
create_topic "order.retry" 3
create_topic "order.dlq" 3

echo "Kafka learning topics are ready."
