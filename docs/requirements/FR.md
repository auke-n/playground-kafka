# Functional Requirements

| ID | Requirement | Priority | Acceptance evidence |
| --- | --- | --- | --- |
| FR-001 | The user can start a local Kafka lab. | Must | Documented startup succeeds and Kafka UI connects. |
| FR-002 | The user can create and inspect topics and records. | Must | Kafka UI or documented CLI exercise; the MSK topic list shows a changing message total after a demo event is produced. |
| FR-003 | A Python producer publishes keyed order events. | Must | Records appear in `order.created`. |
| FR-004 | Consumer services process order events as a consumer group. | Must | Group state and offsets are visible. |
| FR-005 | The lab visualizes broker and consumer health. | Must | Grafana shows throughput and consumer lag. |
| FR-006 | The lab demonstrates retry and dead-letter handling. | Should | A forced failure produces observable retry/DLQ records. |
| FR-007 | CloudFormation provisions a managed MSK learning environment. | Must | Deploy and delete runbook are available. |
| FR-008 | The learner can follow practical Kafka and incident exercises. | Must | Exercises and runbooks exist. |
| FR-009 | A web event-timeline UI is available. | Could | Optional phase accepted only if it adds learning value. |
