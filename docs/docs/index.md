# Documentation

Welcome to the Kubescape documentation.  Please explore the platform using the list of pages in the navigation panel.

## Choose a scan: manifests or live cluster

Kubescape can check Kubernetes configuration before deployment and in a running cluster. Choose the starting point that matches what you have:

| | Local manifests | Live cluster |
| --- | --- | --- |
| **When to use it** | Check configuration during development or in CI before deploying. | Check the current configuration of deployed resources. |
| **What it scans** | Kubernetes resources defined in local YAML or JSON files. | Resources retrieved from the Kubernetes API server. |
| **What you need** | The [Kubescape CLI](install-cli.md) and a manifest file. No running cluster is required. | The [Kubescape CLI](install-cli.md), a running cluster, and a kubeconfig with access to its resources. |
| **Try it** | `kubescape scan deployment.yaml` | `kubescape scan` |
| **Learn more** | [Scanning files](scanning.md#scanning-files) | [Cluster overview scan](scanning.md#the-overview-scan) or the [CLI cluster tutorial](guides/kubescape-cli/index.md) |

Replace `deployment.yaml` with the path to your manifest. For a cluster scan, Kubescape uses your current kubeconfig context; you can also [specify a kubeconfig file](scanning.md#examples). A manifest scan cannot inspect live cluster or node configuration; some node checks require the [host scanner](scanning.md#the-host-scanner).
