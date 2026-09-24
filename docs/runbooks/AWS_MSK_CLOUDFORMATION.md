# AWS MSK Serverless Deployment

## Deploy

CloudFormation creates a managed MSK Serverless cluster plus a disposable EC2 demo host. Docker is required only on that host for the Python services and Kafka UI.

```powershell
aws cloudformation deploy `
  --profile borys `
  --region eu-central-1 `
  --stack-name kafka-learning-lab-msk `
  --template-file infra/cloudformation/msk-learning-lab.yml `
  --capabilities CAPABILITY_IAM
```

Wait for `CREATE_COMPLETE`, then retrieve the public UI URLs:

```powershell
aws cloudformation describe-stacks --profile borys --region eu-central-1 --stack-name kafka-learning-lab-msk --query "Stacks[0].Outputs"
```

CloudFormation must first create MSK; this takes minutes. Once active, the EC2 user data fetches the private IAM bootstrap brokers and starts the demo services.

## Manual and automatic modes

Manual UI steps work unchanged. Do not run automatic consumers when demonstrating manual processing. The MSK client port 9098 is private and accepts traffic only from the demo EC2 security group.

## Delete

```powershell
aws cloudformation delete-stack --profile borys --region eu-central-1 --stack-name kafka-learning-lab-msk
```
