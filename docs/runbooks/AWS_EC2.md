# AWS EC2 Deployment Runbook

## Scope

This is a disposable learning deployment in `eu-central-1`. It creates an ARM64 `t4g.large` Amazon Linux 2023 instance, installs Docker, clones the public repository, and starts the Compose stack.

The Event Timeline and Kafka UI are intentionally public on ports 8000 and 8080. Kafka port 9092 and SSH port 22 are not public. Administration uses AWS Systems Manager Session Manager.

## Prerequisites

- Terraform 1.8 or newer.
- AWS CLI v2.
- AWS credentials configured for an identity permitted to create VPC, EC2, IAM, and SSM resources in `eu-central-1`.

## Provision

```powershell
cd infra/terraform
terraform init
terraform plan
terraform apply
```

Record the `instance_id`, `event_timeline_url`, and `kafka_ui_url` outputs. Cloud-init needs several minutes to install packages, clone the repository, pull images, and build Python services.

## Access and verify

Start a shell through SSM:

```powershell
aws ssm start-session --target <instance_id> --region eu-central-1
```

On the instance:

```bash
sudo docker compose --file /opt/kafka-learning-lab/platform/compose/docker-compose.yml ps
sudo docker compose --file /opt/kafka-learning-lab/platform/compose/docker-compose.yml logs --tail 100
```

Open the Terraform output URLs in a browser. Do not use the public IP with port 9092.

## Update a deployment

From an SSM shell after pushing a new commit to `main`:

```bash
cd /opt/kafka-learning-lab
sudo git pull --ff-only
sudo docker compose --file platform/compose/docker-compose.yml up --detach --build
```

## Destroy

Run this from `infra/terraform` when the lab is no longer needed:

```powershell
terraform destroy
```

This permanently removes the EC2 instance, its root EBS volume, networking resources, and all Kafka records stored on that instance.
