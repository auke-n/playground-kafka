# ADR 0005: Store Terraform State in the Existing S3 Backend

## Status

Accepted

## Decision

Store this lab's Terraform state in the existing S3 bucket `personal-project-tfstate-156275709793-eu-central-1-an` under `playground-kafka/terraform.tfstate`. Enable encryption and S3 lockfiles.

## Consequences

- Terraform state is not stored in the repository or local working directory.
- The operator needs S3 permissions for the state object and its `.tflock` lock file.
- The existing bucket and its policies remain outside this project's Terraform scope.
