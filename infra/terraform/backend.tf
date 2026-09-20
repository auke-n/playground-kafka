terraform {
  backend "s3" {
    bucket       = "personal-project-tfstate-156275709793-eu-central-1-an"
    key          = "playground-kafka/terraform.tfstate"
    region       = "eu-central-1"
    profile      = "borys"
    encrypt      = true
    use_lockfile = true
  }
}
