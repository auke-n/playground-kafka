# Project Context

## Purpose

Build a practical Kafka learning lab for a DevOps engineer preparing for a project interview. The lab must make Kafka concepts and message processing observable with real, repeatable examples.

## Audience and language

- Primary user: a DevOps engineer new to Kafka.
- Conversation language: Ukrainian.
- Repository artifacts: English, including code comments.

## Scope

- A local, Docker-based development lab.
- An AWS MSK Serverless deployment provisioned with CloudFormation.
- A single-node local KRaft deployment and AWS managed MSK Serverless for demonstration.
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
- The MSK CloudFormation deployment targets `eu-central-1`; a Graviton EC2 host administered through SSM runs only the demo services and Kafka UI. MSK brokers remain private and use IAM authentication.
- The demo host defaults to `t4g.small`; it hosts no Kafka broker. Use `t4g.medium` only if the Java-based Kafka UI needs more memory during a demonstration.
- EC2 startup installs explicit ARM64 Docker Compose and Buildx plugins because the Amazon Linux Docker package can provide an older Buildx plugin that is incompatible with Compose builds.
- Amazon Linux 2023 ships `curl-minimal`; cloud-init uses its existing `curl` command and does not install the conflicting full `curl` package.
- The web UI defaults to manually stepped event processing; automatic consumers use the Compose `automatic` profile.
- The demo UI renders a stage as `Queued for Kafka` synchronously on the user's click, then replaces that optimistic state with the broker-confirmed record returned by the same API request. A manual stage fails within one second if Kafka cannot confirm delivery. The observer consumer independently verifies the record without duplicate timeline entries.
- Timeline polling does not replace unchanged UI elements, so a user interaction cannot be lost to a background refresh.
- The MSK Compose deployment pins Kafbat UI to `v1.3.0`: later releases display `N/A` instead of topic message totals in the topic-list view, even when records are present. The pinned version makes the demonstration counter observable.

## Context maintenance

This file is the durable project memory. Update it when scope, assumptions, constraints, or the chosen architecture materially change. See `AGENTS.md` for the full maintenance rule.
