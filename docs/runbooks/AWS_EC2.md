# AWS EC2 Deployment Runbook

## Scope

This is a disposable learning deployment in `eu-central-1`. It creates an ARM64 `t4g.large` Amazon Linux 2023 instance, installs Docker, clones the public repository, and starts the Compose stack.

The Event Timeline and Kafka UI are intentionally public on ports 8000 and 8080. Kafka port 9092 and SSH port 22 are not public. Administration uses AWS Systems Manager Session Manager.

## Prerequisites

- Terraform 1.10 or newer.
- AWS CLI v2.
- AWS shared configuration profile `borys`, permitted to create VPC, EC2, IAM, and SSM resources in `eu-central-1`.
- S3 permissions for `personal-project-tfstate-156275709793-eu-central-1-an/playground-kafka/terraform.tfstate` and its `.tflock` lock file.

## Provision

```powershell
cd infra/terraform
aws sts get-caller-identity --profile borys
terraform init
terraform plan
terraform apply
```

The backend is an existing S3 bucket. Run `terraform init -reconfigure` if you previously initialized this directory with a different backend.

Record the `instance_id`, `event_timeline_url`, and `kafka_ui_url` outputs. Cloud-init needs several minutes to install packages, clone the repository, pull images, and build Python services.

## Insufficient EC2 capacity

`InsufficientInstanceCapacity` means AWS has no available `t4g.large` capacity in the selected Availability Zone; it is not an IAM or Terraform configuration failure. Try another Frankfurt zone:

```powershell
terraform apply -var 'availability_zone=eu-central-1c'
```

Try `eu-central-1a`, `eu-central-1b`, and `eu-central-1c` one at a time. If none has capacity, use the smaller ARM64 alternative:

```powershell
terraform apply -var 'instance_type=t4g.medium'
```

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
sudo COMPOSE_BAKE=false docker compose --file platform/compose/docker-compose.yml up --detach --build
```

## Install Docker plugins on an existing instance

Cloud-init installs ARM64 Compose and Buildx plugins for new instances. If an existing instance reports `compose build requires buildx 0.17.0 or later`, install or replace both plugins through an SSM shell:

```bash
curl --version
sudo install -d -m 0755 /usr/local/lib/docker/cli-plugins
sudo curl -fsSL "https://github.com/docker/compose/releases/download/v5.5.0/docker-compose-linux-aarch64" -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod 0755 /usr/local/lib/docker/cli-plugins/docker-compose
sudo curl -fsSL "https://github.com/docker/buildx/releases/download/v0.37.1/buildx-v0.37.1.linux-arm64" -o /usr/local/lib/docker/cli-plugins/docker-buildx
echo "e5cc9fe3bbff5cbc91230981f7860e06076110730a2db997082652199042a1f2  /usr/local/lib/docker/cli-plugins/docker-buildx" | sudo sha256sum --check
sudo chmod 0755 /usr/local/lib/docker/cli-plugins/docker-buildx
docker compose version
docker buildx version
```

Then build and start the stack normally:

```bash
cd /opt/kafka-learning-lab
sudo docker compose --file platform/compose/docker-compose.yml up --detach --build
```

## Destroy

Run this from `infra/terraform` when the lab is no longer needed:

```powershell
terraform destroy
```

This permanently removes the EC2 instance, its root EBS volume, networking resources, and all Kafka records stored on that instance.
