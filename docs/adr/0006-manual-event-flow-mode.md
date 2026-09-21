# ADR 0006: Make the Web UI Event Flow Manually Stepped by Default

## Status

Accepted

## Decision

The web UI queues one lifecycle event per button click in manual mode. It renders `Queued for Kafka` as soon as the API accepts the command, then replaces it with the broker-confirmed record. This keeps the interview-demo controls responsive while preserving a visible distinction between command acceptance and Kafka delivery. Automatic payment and fulfillment consumers are enabled only with the Compose `automatic` profile.
