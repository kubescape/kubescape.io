# Amazon Elastic Kubernetes Service integration
Scan clusters running in Amazon Elastic Kubernetes Service (EKS). This uses the Kubescape CLI to scan the clusters and run commands.

The Amazon Web Services (AWS) integration is based on the official [AWS SDK for Go](https://github.com/aws/aws-sdk-go).

## Set up authentication

Authentication must be defined in the local execution context of Kubescape.

If you use an Amazon Elastic Compute Cloud (EC2) instance, you can authenticate using an IAM role through the EC2 metadata service.

From the AWS Command Line Interface (AWS CLI), run the following commands:

1. Configure AWS keys.
   ```Text Configure AWS keys
   config AWS Access Key ID [****************XXXX]:
   config AWS Secret Access Key [****************XXXX]:
   ```
2. Press **Enter** for approval.
3. Ensure that the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are configured properly.
   ```AWS Verify credentials
   cat ~/.aws/credentials
   ```

The Kubescape EKS integration works automatically from any shell where you access your cluster.

## Set the cloud region

The `KS_CLOUD_REGION` environment variable is required to get your cluster region. If this variable is not set, Kubescape tries to get the cluster region from the cluster's name.

We recommend setting the `KS_CLOUD_PROVIDER` environment variable to `eks`.

1. Configure the region name.
   ```Text Configure region
   config Default region name \[]: (cluster default region)
   ```
2. Ensure that the region is configured.
   ```Text Verify region
   \`cat ~/.aws/config
   ```

## Verify your connection and IAM roles

Run the following to ensure that you have cluster access:

```Text Verify access
kubectl get nodes
```

Run the following command in the AWS CLI to verify your IAM permissions to your AWS cluster:

```Text Verify IAM
aws eks describe-cluster --name <cluster-name> --region <cluster region>
```

## Integrate with the ARMO in-cluster microservice

Authorize ARMO in-cluster component to access Amazon Elastic Container Registry (ECR) for container vulnerability scanning and Amazon EKS for Kubernetes risk assessment. [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) support both authorizations.

The script to set up AWS IAM authorization is provided in [this recipe](https://hub.armo.cloud/recipes/setup-aws-iam-authorization-of-in-cluster-installation-of-kubescape-in-eks).
