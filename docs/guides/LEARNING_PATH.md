# Kafka Learning Path

## First concepts to master

1. Publish an event to a topic and inspect its key, value, partition, and offset.
2. Use the same key repeatedly and observe partition affinity and ordering within one partition.
3. Run two consumers in one group and observe partition assignment and rebalancing.
4. Stop a consumer, produce events, and observe consumer lag; restart it and watch lag recover.
5. Reset a consumer group's offset and replay retained records.
6. Trigger a processing failure and trace a retry and dead-letter event.
7. Change partition count in a safe demo topic and discuss the ordering consequence.

## Topics for the interview

- Kafka versus a traditional queue: retention, replay, and consumer groups.
- Ordering guarantees: per partition, not across a whole topic.
- Delivery semantics and idempotent consumers.
- Consumer lag, rebalances, partition count, and scaling limits.
- Replication, ISR, `acks`, `min.insync.replicas`, and why the lab does not model HA.
- KRaft versus ZooKeeper and managed Kafka trade-offs.
