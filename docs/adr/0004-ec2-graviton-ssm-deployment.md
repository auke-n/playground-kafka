# ADR 0004: Deploy the Learning Lab to Graviton EC2 with SSM Administration

## Status

Accepted

## Decision

Deploy to a `t4g.large` Amazon Linux 2023 ARM64 instance in `eu-central-1`. Use an EC2 IAM role with SSM instead of inbound SSH. Expose only the demo HTTP interfaces on ports 8000 and 8080; keep Kafka port 9092 bound to loopback.

## Consequences

- The stack uses ARM64-compatible images and avoids SSH key management.
- The public UI endpoints have no authentication and are suitable only for a temporary demo.
- The public Git repository is cloned by cloud-init during instance creation.
