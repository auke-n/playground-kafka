# Implementation Plan

## Recommended delivery sequence

### Phase 0 — Foundation and design

Create the documentation system, architecture baseline, backlog, ADRs, and local development conventions. This phase is complete when future work has clear scope and traceability.

### Phase 1 — Local Kafka learning lab

Create a Docker Compose stack with a Kafka broker in KRaft mode and Kafka UI. Verify topic creation, producing records, consuming records, consumer groups, offsets, partitions, and retention locally.

**Why first:** it is fast, cheap, reproducible, and separates Kafka learning from AWS troubleshooting.

### Phase 2 — Observable Python event flow

Implement a small Python demo around an order lifecycle:

`order.created` -> `payment.requested` -> `payment.completed` -> `order.fulfilled`

Include a producer API/CLI, consumer services, intentionally configurable processing delay/failure, structured logs, retry and dead-letter topic examples, and metrics.

### Phase 3 — Observability and learning UI

Add Prometheus and Grafana dashboards for broker health, throughput, consumer lag, partition distribution, and application processing outcomes. Kafka UI remains the primary tool for inspecting topics, records, consumer groups, and offsets.

A small web UI is optional after this phase. It should visualize submitted orders and their event timeline; React is justified only if this provides learning value beyond Kafka UI and Grafana.

### Phase 4 — AWS EC2 deployment

Provision a minimal EC2 environment with Terraform, then install/run the versioned Docker Compose stack using cloud-init or a documented deployment command. Restrict inbound traffic and provide teardown instructions.

### Phase 5 — Interview and operations exercises

Add guided scenarios, incident-style runbooks, and a concise interview cheat sheet covering design trade-offs and common failures.

## Repository layout

The documentation folders below are present now. Runtime folders will be created only with the phase that uses them, so an empty directory never masquerades as implemented functionality.

```text
.
├── AGENTS.md                         # Durable working agreement for coding agents
├── README.md                         # Entry point
├── docs/
│   ├── context/                      # Durable scope, assumptions, constraints
│   ├── planning/                     # Delivery plan and milestones
│   ├── requirements/                 # Functional and later non-functional requirements
│   ├── architecture/                 # Diagrams and topology descriptions
│   ├── adr/                          # Architecture decision records
│   ├── backlog/                      # Prioritized, traceable work items
│   ├── guides/                       # Learning material and exercises
│   └── runbooks/                     # Operational procedures
├── infra/
│   └── terraform/                    # EC2 networking and instance definitions
├── platform/
│   └── compose/                      # Kafka and observability Compose stack
├── services/
│   ├── order_api/                    # Python producer/API
│   ├── payment_processor/             # Python consumer
│   └── fulfillment_processor/         # Python consumer
├── dashboards/                       # Grafana dashboard definitions
├── scripts/                          # Safe developer and demo helpers
└── tests/                            # Integration and smoke tests
```

## Definition of done for the first learning release

- The full lab starts locally with one documented command sequence.
- An order event traverses multiple Kafka topics and services.
- A learner can inspect records, offsets, consumer lag, and dashboards.
- A failure path reaches a retry or dead-letter topic and is explainable.
- Terraform can create and destroy the AWS demo infrastructure safely.
- Documentation explains every component and includes exercises.
