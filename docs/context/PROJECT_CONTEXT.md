# Project Context

## Purpose

Build a practical Kafka learning lab for a DevOps engineer preparing for a project interview. The lab must make Kafka concepts and message processing observable with real, repeatable examples.

## Audience and language

- Primary user: a DevOps engineer new to Kafka.
- Conversation language: Ukrainian.
- Repository artifacts: English, including code comments.

## Scope

- A local, Docker-based development lab.
- An AWS EC2 deployment provisioned with Terraform.
- A single-node Kafka deployment in KRaft mode for learning and demonstration.
- A FastAPI order producer and Python payment and fulfillment consumers that model an order-processing workflow.
- Operational visibility through Kafka UI, Prometheus-compatible metrics, and Grafana dashboards.
- Guided exercises and operational runbooks.

## Non-goals for the first release

- Production-grade high availability, multi-AZ Kafka, or managed Kafka migration.
- Processing personally identifiable or business data.
- A full business application or a feature-rich React product UI.

## Current assumptions

- AWS credentials, region, and SSH access method will be supplied only during the infrastructure phase.
- The EC2 environment is disposable and cost-conscious.
- Docker Compose will run the application and observability stack on the EC2 instance.
- Kafka UI and Grafana will not be publicly exposed without authentication or network restriction.
- Docker Desktop is required to run the local lab on the current Windows development machine; it was not available during the initial implementation check.
- The persistent local Kafka volume is initialized by a one-shot root container so the broker's non-root runtime user can write KRaft metadata on Docker Desktop.
- AWS deployment targets `eu-central-1` on a Graviton `t4g.large` instance administered through SSM. Only ports 8000 and 8080 are public; Kafka remains loopback-bound.
- Terraform state is stored in the existing S3 bucket `personal-project-tfstate-156275709793-eu-central-1-an` at `playground-kafka/terraform.tfstate` with encryption and S3 lockfiles.
- Terraform uses the local AWS shared configuration profile `borys` for provider and backend access.
- EC2 startup installs explicit ARM64 Docker Compose and Buildx plugins because the Amazon Linux Docker package can provide an older Buildx plugin that is incompatible with Compose builds.
- The web UI defaults to manually stepped event processing; automatic consumers use the Compose `automatic` profile.

## Context maintenance

This file is the durable project memory. Update it when scope, assumptions, constraints, or the chosen architecture materially change. See `AGENTS.md` for the full maintenance rule.
