# ADR 0001: Start Local and Use a Single-Node KRaft Kafka Lab

## Status

Accepted

## Context

The project is a time-constrained learning environment for a Kafka beginner. It needs to be reproducible, inexpensive, and easy to observe before AWS deployment is introduced.

## Decision

Use Docker Compose as the primary local runtime. Run one Kafka broker in KRaft mode, without ZooKeeper. Deploy the same logical stack to one EC2 instance in the AWS demo phase.

## Consequences

- The setup is simpler and reflects current Kafka metadata architecture.
- It is suitable for demonstrating core Kafka concepts, not high availability or production failure tolerance.
- Cluster sizing, replication, TLS/SASL, and managed Kafka are deferred topics and may become later ADRs.
