[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Start", "Stop", "Status", "Verify", "Reset")]
    [string]$Action
)

$ErrorActionPreference = "Stop"
$composeFile = Join-Path $PSScriptRoot "..\platform\compose\docker-compose.yml"

function Invoke-Compose {
    param([string[]]$Arguments)

    & docker compose --file $composeFile @Arguments
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        $commandText = "docker compose --file `"$composeFile`" $($Arguments -join ' ')"
        throw "Docker Compose command failed with exit code $exitCode. Command: $commandText"
    }
}

switch ($Action) {
    "Start" {
        Invoke-Compose @("up", "--detach", "--wait", "kafka")
        Invoke-Compose @("run", "--rm", "--no-deps", "topic-bootstrap")
        Invoke-Compose @("up", "--detach", "--no-deps", "kafka-ui")
        Invoke-Compose @("up", "--detach", "--build", "--no-deps", "order-api")
        Write-Host "Kafka UI: http://localhost:8080"
        Write-Host "Order API: http://localhost:8000/docs"
        Write-Host "Kafka bootstrap server: localhost:9092"
    }
    "Stop" {
        Invoke-Compose @("down")
    }
    "Status" {
        Invoke-Compose @("ps")
    }
    "Verify" {
        Invoke-Compose @("exec", "-T", "kafka", "/opt/kafka/bin/kafka-topics.sh", "--bootstrap-server", "localhost:19092", "--list")
        Invoke-Compose @("exec", "-T", "kafka", "/opt/kafka/bin/kafka-topics.sh", "--bootstrap-server", "localhost:19092", "--describe", "--topic", "order.created")
    }
    "Reset" {
        Invoke-Compose @("down", "--volumes")
        Write-Host "The local Kafka volume was removed. Run '.\scripts\lab.ps1 -Action Start' to create a fresh lab."
    }
}
