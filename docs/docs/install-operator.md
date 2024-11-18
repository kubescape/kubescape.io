# Kubescape Operator

Kubescape can run as a set of microservices inside a Kubernetes cluster. This allows you to continually monitor the status of a cluster, including for compliance and vulnerability management, and to export this data to [an external provider](providers.md).

The Kubescape Operator is installed using [Helm](https://helm.sh/).

## Prerequisites

First, [configure kubectl to refer to the Kubernetes cluster you wish to install the Kubescape Operator into](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/).

If you have not already, you should [install Helm](https://helm.sh/docs/intro/install/).

## Install

> **Warning:** We only support installing this chart using Helm or ArgoCD.
Using alternative installation methods, such as Kustomize, Helmfile or using custom scripts, may lead to unexpected behavior and issues.
We cannot guarantee compatibility or provide support for deployments that are installed using methods other than Helm or ArgoCD.

Run the installation command:
```
helm repo add kubescape https://kubescape.github.io/helm-charts/ ; helm repo update ; helm upgrade --install kubescape kubescape/kubescape-operator -n kubescape --create-namespace --set clusterName=`kubectl config current-context` --set capabilities.continuousScan=enable
```

Verify that the installation was successful:
```shell
$ kubectl get pods -n kubescape
kubescape     kubescape-548d6b4577-qshb5                          1/1     Running   0               60m
kubescape     kubevuln-6779c9d74b-wfgqf                           1/1     Running   0               60m
kubescape     operator-5d745b5b84-ts7zq                           1/1     Running   0               60m
kubescape     storage-59567854fd-hg8n8                            1/1     Running   0               60m
```

## View results

The scanning results will be available gradually as the scans are completed.

There are multiple options to visualize the results (GUI):
* [Headlamp integration](operator/ui-with-headlamp.md)
* [Lens integration](integrations/lens.md)
* [ARMO Platform](https://armosec.io) (commertial)

### Compliance scanning

View Compliance summary report per namespace:
```
kubectl get workloadconfigurationscansummaries
```

View Compliance **summary** report for each workload:
```
kubectl get workloadconfigurationscansummaries -A
```

View Compliance **detailed** report for each workload:
```
kubectl get workloadconfigurationscans -A
```

### Image Vulnerabilities scanning

View Vulnerabilities summary report per namespace:
```
kubectl get vulnerabilitysummaries
```

View vulnerabilities **summary** report for each workload/image:
```
kubectl get vulnerabilitymanifestsummaries -A
```

View vulnerabilities **detailed** report for each workload/image:
```
kubectl get vulnerabilitymanifests -A
```

### Network Policy Generation

View generated network policies:
```
kubectl get generatednetworkpolicies -A
```

## Upgrading to a new release

To upgrade to the most recent version of the Kubescape Operator:

```bash
helm repo update; helm upgrade kubescape kubescape/kubescape-operator -n kubescape
```

You can find the current version of the Helm chart installed in your cluster by running `helm list -n kubescape`.

To manually check if a newer version is available, visit the GitHub page for the Helm chart, or run

```bash
helm repo update; helm search repo kubescape/kubescape-operator
```

## Uninstall

You can uninstall this helm chart by running the following command:
```shell
helm uninstall kubescape -n kubescape
```
Then, delete the kubescape namespace:
```shell
kubectl delete ns kubescape
```

## Configuring your installation

The Helm charts for the Kubescape Operator offer both broad and detailed configuration options.

### Enabling capabilities

High-level capabilities of the Kubescape Operator can be configured using the `values.yaml` file:

```yaml
capabilities:
  # ====== configuration scanning related capabilities ======
  #
  # Default configuration scanning setup
  configurationScan: enable
  # Continuous Scanning continuously evaluates the security posture of your cluster.
  continuousScan: disable
  nodeScan: enable

  # ====== Image vulnerabilities scanning related capabilities ======
  #
  vulnerabilityScan: enable
  relevancy: enable
  # Generate VEX documents alongside the image vulnerabilities report (experimental)
  vexGeneration: disable

  # ====== Runtime related capabilities ======
  #
  runtimeObservability: enable
  networkPolicyService: enable
  runtimeDetection: disable
  malwareDetection: disable
  nodeProfileService: disable
  seccompProfileService: enable

  # ====== Other capabilities ======
  #
  # This is an experimental capability with an elevated security risk. Read the
  # matching docs before enabling.
  autoUpgrading: disable
  prometheusExporter: disable
  # seccompGenerator: disable

#extra capability - service discovery option
serviceScanConfig:
  enabled : false
  interval: 1h
```

You can configure these by using `--set` when installing the chart, or by specifying your own values file with the `-f` flag. [Read the Helm documentation to learn more](https://helm.sh/docs/chart_template_guide/values_files/).

### Configuring parameters

See [the GitHub repository for the Kubescape operator](https://github.com/kubescape/helm-charts/blob/main/charts/kubescape-operator/README.md#chart-support) to learn the full set of configuration parameters.

### Sizing resources

By default, Kubescape supports small- to medium-sized clusters. If you have a larger cluster and you experience slowdowns, or see Kubernetes evicting components, revise the number of resources allocated for the troubled component.

The defaults of 500 MiB of memory and 500m CPU work well for clusters up to 1250 total resources when running Kubescape.

If you have more total resources or experience resource pressure, verify how many resources are in your cluster by running the following command:

```
kubectl get all -A --no-headers | wc -l
```

The command prints an approximate count of resources in your cluster.
Then based on the number you see, allocate 100 MiB of memory for every 200 resources in your cluster over the count of 1250, but no less than 128 MiB total.

The formula for memory is as follows:

```
MemoryLimit := max(128, 0.4 * YOUR_AMOUNT_OF_RESOURCES)
```

For example, if your cluster has 500 resources, a sensible memory limit would be:

```
kubescape:
  resources:
    limits:
      memory: 200Mi  # max(128, 0.4 * 500) == 200
```

If your cluster has 50 resources, we recommend allocating at least 128 MiB of memory.

For the CPU, the more you allocate, the faster your clusters are scanned. This is especially true for clusters that have a large number of resources.

However, we recommend that you give Kubescape no less than 500m CPU no matter the size of your cluster so it can scan a relatively large amount of resources fast.

## Verifying images

Kubescape container images are signed with [Cosign](https://docs.sigstore.dev/signing/quickstart/).

### Keyless verification

For keyless verification use GitHub as the trust anchor, see this example:
```bash
cosign verify quay.io/kubescape/kubescape:v2.9.2-prerelease --certificate-identity-regexp "github.com" --certificate-oidc-issuer-regexp "githubusercontent.com" && echo Signature OK
```

### Validation with Public key

Put the following key to a file called `cosign.pub`.

Kubescape Cosign public key (version 1):
```
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEbgIMZrMTTlEFDLEeZXz+4R/908BG
EeO70x6oMN7E4JQgzgbCB5rinqhK5t7dB61saVKQTb4P2NGtjPjXVbSTwQ==
-----END PUBLIC KEY-----
```

Use the following command to verify the image integrity with it:
```bash
cosign verify --key cosign.pub quay.io/kubescape/kubescape:v2.9.2-prerelease  && echo Signature OK
```
