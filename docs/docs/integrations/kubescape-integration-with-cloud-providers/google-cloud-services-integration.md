# Google Cloud Services integration

This uses the Kubescape CLI to scan the clusters and run commands.

The Google Kubernetes Engine (GKE) integration is based on the official [GCP SDK](https://cloud.google.com/go/docs/reference).

To install Kubescape in Google Cloud Services, you must:

1. Set up your credentials.
2. Set up a service account.
3. Create an IAM role for the service account.
4. Bind the IAM role to the service account.
5. Install and upgrade the Kubescape Helm chart.

## Set up credentials

Authentication is based on the local execution context of the CLI and must be defined in the execution context of Kubescape.

Set one of the following:

- GOOGLE_APPLICATION_CREDENTIALS\` environment variable
- `~/.config/gcloud/application_default_credentials.json` file

If you're missing the `application_default_credentials.json` file, but you do have GCP access from the shell, run the following command to create it:

```Text Create login
gcloud auth application-default login
```

## Verify your GCP connection

Run the following to ensure you can access your cluster:

```Text Verify connection
gcloud container clusters describe <cluster name> --zone <cluster zone> --project <GCP project>
```

## Integrate with the Kubescape in-cluster components

Kubescape in-cluster components can be authorized to access Google Container Registry (GCR) for container vulnerability scanning and GKE for Kubernetes risk assessment. Both authorizations are supported using [GKE workload identities](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity).

### Workload identity support

The workload identity is not enabled by default in GKE. Ensure you aren't interfering with existing applications in the cluster by enabling it.

Ensure that your cluster has workload identity enabled by running this command:

```Text Verify workload identity
gcloud container clusters describe <CLUSTER_NAME> | grep workloadPool
```

Use [this recipe](https://hub.armosec.io/recipes/setup-gcp-iam-authorization-for-in-cluster-installation-of-kubescape-in-gke-1) to finish setting up the GCP IAM authorization and Kubescape integration.

After you’ve installed Kubescape and successfully authorized the components, you can use Kubescape CLI commands to scan clusters hosted in GCP and send the scan results to ARMO Platform to visualize your data.

```Text Scan
kubescape scan . --submit --account=<accountID>
```
