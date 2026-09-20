# ADR 0002: Use FastAPI and confluent-kafka for the Demo Event Flow

## Status

Accepted

## Context

The lab needs a minimal but observable producer and consumer implementation that runs consistently in Docker and demonstrates consumer groups and offset commits.

## Decision

Use FastAPI for an HTTP order producer and `confluent-kafka` for producer and consumer clients. The payment and fulfillment processors are separate long-running services. Consumers disable automatic commits and commit an input record only after their output event has been delivered.

## Consequences

- `POST /orders` makes event creation easy to demonstrate through Swagger UI or PowerShell.
- The flow demonstrates at-least-once processing and why consumers must be idempotent.
- The synchronous delivery wait is intentional for a small learning lab and is not a throughput-oriented production pattern.
