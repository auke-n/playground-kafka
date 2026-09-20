# ADR 0003: Add a Minimal Kafka-backed Timeline UI

## Status

Accepted

## Context

The learner needs a simple interface to generate an order and see its actual Kafka lifecycle.

## Decision

Serve a dependency-free HTML interface from the Order API. A dedicated observer consumer group reads the lifecycle topics and keeps an in-memory timeline for the UI.

## Consequences

- The UI reflects records consumed from Kafka, rather than simulated state.
- Timeline state is intentionally ephemeral and resets when the Order API restarts.
- React remains unnecessary for this learning-focused interface.
