# ADR 0006: Make the Web UI Event Flow Manually Stepped by Default

## Status

Accepted

## Decision

The web UI publishes one lifecycle event per button click in manual mode. It renders `Queued for Kafka` synchronously on the click, then replaces it with the broker-confirmed record returned by the same API request. Kafka delivery confirmation has a one-second limit, so a broken broker is reported quickly rather than appearing as a slow demo. This keeps the interview-demo controls responsive while preserving a visible distinction between user intent and Kafka delivery. Automatic payment and fulfillment consumers are enabled only with the Compose `automatic` profile.
