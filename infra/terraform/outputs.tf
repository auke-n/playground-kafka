output "instance_id" {
  value = aws_instance.lab.id
}

output "public_ip" {
  value = aws_instance.lab.public_ip
}

output "event_timeline_url" {
  value = "http://${aws_instance.lab.public_ip}:8000"
}

output "kafka_ui_url" {
  value = "http://${aws_instance.lab.public_ip}:8080"
}
