# Local Kafka Lab Runbook

## Prerequisites

- Docker Desktop with Docker Compose v2.
- Ports `9092` and `8080` must be available on the host.
- PowerShell 7+ is recommended on Windows.

## Start the lab

From the repository root, run:

```powershell
.\scripts\lab.ps1 -Action Start
```

Wait for the command to finish. Open `http://localhost:8080`, select the `learning-lab` cluster, and inspect the topics.

The command also starts the Order API. Open its Swagger interface at `http://localhost:8000/docs` and call `POST /orders` with:

```json
{
  "order_id": "order-1002",
  "item": "coffee",
  "amount": 42.5,
  "simulate_payment_failure": "none"
}
```

For the visual flow, open `http://localhost:8000`. The UI creates an order and polls a Kafka observer consumer group for the records that actually passed through the topics.
Click `Create order` and keep the page open; the timeline updates automatically. `lab.ps1 -Action Start` starts or rebuilds containers and is not required after creating an order.

Observe the same `order_id` in `order.created`, `payment.requested`, `payment.completed`, and `order.fulfilled` in Kafka UI. The `payment-processor-v1` and `fulfillment-processor-v1` consumer groups and their committed offsets are also visible there.

Use `"transient"` to produce an `order.retry` event, or `"terminal"` to produce an `order.dlq` event. The next phase will add scheduled retry processing and metrics.

The host bootstrap address is `localhost:9092`. Docker services use `kafka:19092`. These are intentionally different: Kafka clients receive the advertised address appropriate to the network they use.

## Troubleshooting startup

If the script reports `permission denied while trying to connect to the docker API`, start Docker Desktop, wait until its engine is running, then verify access with:

```powershell
docker version
```

If `Start` fails, its final error now includes the exact Compose command. Run that command again without the script to see the full Docker output. The stack's `kafka-data-init` service sets the required ownership on the local KRaft volume automatically; do not manually modify the volume.

## Verify the initial topics

```powershell
.\scripts\lab.ps1 -Action Verify
```

Expected topics:

```text
order.created
order.dlq
order.fulfilled
order.retry
payment.completed
payment.requested
```

Kafka's internal topics may appear after the first consumer group is created.

## First exercise: a record, key, partition, and offset

Open a shell in the Kafka container:

```powershell
docker compose --file platform/compose/docker-compose.yml exec kafka bash
```

In that shell, publish two records with the same key:

```bash
/opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:19092 --topic order.created --property parse.key=true --property key.separator=:
order-1001:{"order_id":"order-1001","amount":42.50}
order-1001:{"order_id":"order-1001","amount":43.00}
```

Read the records and print their metadata:

```bash
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:19092 --topic order.created --from-beginning --property print.key=true --property print.partition=true --property print.offset=true
```

Records with the same key are assigned to the same partition, so their order is preserved within that partition. Inspect the same records in Kafka UI.

## Stop or reset

```powershell
.\scripts\lab.ps1 -Action Stop
```

Stopping preserves messages in the named Docker volume. To delete the local lab data and start over:

```powershell
.\scripts\lab.ps1 -Action Reset
```

`Reset` is destructive only to the named local Docker volume `kafka-learning-lab-data`.
