# Kafka Learning Lab

A hands-on, observable Kafka learning environment for a DevOps interview preparation project.

The project provides a local Docker-based lab and will add a single-node AWS EC2 demo deployment, a Python event-driven application, Kafka UI, and operational dashboards.

Start with [the project plan](docs/planning/IMPLEMENTATION_PLAN.md) and [the learning path](docs/guides/LEARNING_PATH.md).

## Start the local lab

After installing Docker Desktop, run:

```powershell
.\scripts\lab.ps1 -Action Start
```

Open Kafka UI at `http://localhost:8080`. Full instructions and the first exercise are in [the local lab runbook](docs/runbooks/LOCAL_LAB.md).

## Project documentation

- [Project context](docs/context/PROJECT_CONTEXT.md)
- [Requirements](docs/requirements/FR.md)
- [Architecture](docs/architecture/ARCHITECTURE.md)
- [Architecture decisions](docs/adr/README.md)
- [Backlog](docs/backlog/BACKLOG.md)
- [Runbooks](docs/runbooks/README.md)
