variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "project_name" {
  type    = string
  default = "kafka-learning-lab"
}

variable "repository_url" {
  type        = string
  description = "Public Git repository cloned by the EC2 instance."
  default     = "https://github.com/auke-n/playground-kafka.git"
}

variable "repository_ref" {
  type    = string
  default = "main"
}

variable "instance_type" {
  type    = string
  default = "t4g.large"
}

variable "vpc_cidr" {
  type    = string
  default = "172.31.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "172.31.0.0/20"
}

variable "availability_zone" {
  type        = string
  description = "Availability Zone for the single-instance learning lab. Change it when an instance type has no capacity."
  default     = "eu-central-1b"
}
