# Target Architecture

## Baseline topology

```text
Order Producer/API
        |
        v
Kafka topic: order.created ---> Payment Consumer ---> payment.requested
        |                           |                     |
        |                           +--> payment.completed +--> Fulfillment Consumer
        |                                                      |
        +--> retry / dead-letter topics                       +--> order.fulfilled

Kafka broker (single node, KRaft mode)
        |
        +--> Kafka UI: topics, records, consumer groups, offsets
        +--> JMX exporter -> Prometheus -> Grafana: broker and application metrics
```

## Deployment layers

| Layer | Local lab | AWS demo |
| --- | --- | --- |
| Runtime | Docker Compose | Docker Compose on one EC2 instance |
| Infrastructure | None | Terraform |
| Kafka metadata mode | KRaft | KRaft |
| Broker count | 1 | 1 |
| Visibility | Kafka UI, Prometheus, Grafana | Kafka UI, Prometheus, Grafana |

The local Compose stack uses a named volume for Kafka data. A one-shot initialization container assigns that volume to Kafka's non-root container user before the broker starts.

## Key learning entities

| Entity | What the lab demonstrates |
| --- | --- |
| Broker | Kafka server that stores and serves records |
| Topic | Named, append-only stream, such as `order.created` |
| Partition | Ordered shard of a topic; unit of parallelism |
| Record | Key, value, timestamp, headers, offset |
| Producer | Writes records; key controls partition affinity |
| Consumer group | Cooperating consumers; each partition is assigned once per group |
| Offset | Consumer position in a partition |
| Retention | How long Kafka keeps records independently of consumption |
| Retry / DLQ | Explicit handling of transient and terminal processing failures |

## Security baseline

- Allow SSH only from an explicitly configured administrator CIDR, or prefer AWS SSM later.
- Do not expose Kafka's broker port to the public internet.
- Restrict Kafka UI and Grafana to a trusted CIDR or access them through an SSH tunnel.
- Store secrets outside Git and never commit Terraform state.
