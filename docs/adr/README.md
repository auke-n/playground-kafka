# Architecture Decision Records

ADRs capture decisions that materially affect implementation or operations. Create a new file as `NNNN-short-title.md` using the structure: Status, Context, Decision, Consequences.

| ADR | Decision | Status |
| --- | --- | --- |
| [0001](0001-local-first-single-node-kraft.md) | Start local and use a single-node KRaft Kafka lab | Accepted |
| [0002](0002-python-event-services.md) | Use FastAPI and confluent-kafka for the demo event flow | Accepted |
| [0003](0003-minimal-kafka-backed-timeline-ui.md) | Add a minimal Kafka-backed timeline UI | Accepted |
| [0004](0004-ec2-graviton-ssm-deployment.md) | Deploy on Graviton EC2 with SSM administration | Accepted |
| [0005](0005-s3-remote-terraform-state.md) | Store Terraform state in the existing S3 backend | Accepted |
| [0006](0006-manual-event-flow-mode.md) | Make the web UI event flow manually stepped by default | Accepted |
