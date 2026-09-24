# ADR 0007: Use MSK Serverless through CloudFormation

## Status

Accepted

## Decision

This branch uses `AWS::MSK::Serverless` instead of a self-managed EC2 Kafka broker. CloudFormation provisions networking, MSK, IAM, and an EC2 demo host. The host runs Docker only for the Python demo services and Kafbat UI; Kafka brokers are AWS managed.

## Consequences

- Clients use private MSK endpoints, TLS, and IAM authentication.
- The demo host needs an IAM role; no Kafka passwords are stored.
- The EC2 IMDSv2 hop limit is set to `2` so Docker containers can retrieve instance-profile credentials for MSK IAM authentication.
- MSK Serverless has managed-service cost and provisioning time.
