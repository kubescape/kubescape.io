# Scanning with Kubescape

## Introduction

A common use case for Kubescape is to validate the configuration of a Kubernetes cluster, or some resources you could deploy to one.

## Scanning using the command line interface

### The overview scan

Running `kubescape scan` with no other parameters will perform the cluster overview/baseline security scan.  This performs some key security checks and then shows you the number of resources which have certain permissions. You are then able to set up [risk acceptance rules](accepting-risk.md) to allow for things which are deliberately installed or configured about your cluster.

For example, malware in a cluster will often attempt to create a cluster admin role, or a role with permissions that approximates that.  With the Kubescape baseline scan, you can identify which roles you have installed that should have these permissions, and then easily see, or be notified, when the configuration changes from your secure baseline.

### Framework scans

A common use case for Kubescape is to validate a cluster against a [security framework](frameworks-and-controls/index.md). To run a framework scan:

```sh
kubescape scan framework <framework>
```

[Learn what frameworks are available, or how to create your own](frameworks-and-controls/index.md).

!!! note "Note"
    Before Kubescape 3.0, the default behaviour of `kubescape scan` was to scan the NSA and MITRE frameworks.

### The host scanner

Most of Kubescape's controls validate data from a Kubernetes API server, such as configuration of a cluster or a workload deployed to it.  Some controls require validating a configuration which has to run on the nodes of a Kubernetes cluster; for example, [to check if the Kubelet enforces client TLS authentication](controls/c-0070.md).

To enable the host scanner, install the [Kubescape Operator](install-operator.md) in your cluster.

### Verbose mode

In verbose mode (when the `--verbose` flag is provided) Kubescape will perform a scan of your specified cluster as usual. The output will then include per-resource information for each resource that triggered a control failure, including a link to the documentation for that control, and *assisted remediation*, Kubescape's suggestion of what parameters can be changed to mitigate or remove the failure.

For example:

```
################################################################################
ApiVersion: v1
Kind: ServiceAccount
Name: vpnkit-controller
Namespace: kube-system

Controls: 1 (Failed: 1, action required: 0)

┌──────────┬────────────────────────────────┬────────────────────────────────┬────────────────────────────────────┐
│ SEVERITY │          CONTROL NAME          │              DOCS              │        ASSISTED REMEDIATION        │
├──────────┼────────────────────────────────┼────────────────────────────────┼────────────────────────────────────┤
│ Medium   │ Automatic mapping of service   │ https://ks.dev/controls/c-0034 │ automountServiceAccountToken=false │
│          │ account                        │                                │                                    │
└──────────┴────────────────────────────────┴────────────────────────────────┴────────────────────────────────────┘
```

### Scanning files

Kubescape can be used to scan local YAML/JSON files before they are deployed to Kubernetes. This is a common use case for integrations into CI/CD systems; see [Integrations](integrations/index.md) for how this can be used.

* Scan local YAML/JSON files before deploying:
    ```sh
    kubescape scan *.yaml
    ```

* Scan Kubernetes manifest files from a Git repository:

    ```sh
    kubescape scan https://github.com/kubescape/kubescape
    ```

* Scan Helm charts:

    ```sh
    kubescape scan </path/to/directory>
    ```

    !!! note "Note"
        Kubescape will load the default VALUES file.

* Scan a Kustomize directory:

    ```sh
    kubescape scan </path/to/directory>
    ```

    !!! note "Note"
        Kubescape will generate Kubernetes YAML objects using a `kustomize` file and scan them.

## Examples

* Scan a specific control, using the control name or control ID. [See the control library](controls/index.md).

    ```sh
    kubescape scan control "Privileged container"
    ```

* Use an alternative `kubeconfig`` file:

    ```sh
    kubescape scan --kubeconfig cluster.conf
    ```

* Scan specific namespaces:

    ```sh
    kubescape scan --include-namespaces development,staging,production
    ```

* Exclude certain namespaces:

    ```sh
    kubescape scan --exclude-namespaces kube-system,kube-public
    ```

* Scan with exceptions

    ```sh
    kubescape scan --exceptions examples/exceptions/exclude-kube-namespaces.json
    ```

    Objects with exceptions will be presented as `exclude` and not `fail`.

    [Learn more about accepting risk with exceptions](accepting-risk.md)

### Output formats

The default output format for a Kubescape scan is a "pretty-printed" table view.  Other formats are also available:

* JSON:

    ```sh
    kubescape scan --format json --format-version v2 --output results.json
    ```

    !!! note "Note"
        Add the `--format-version v2` flag for maximum compatibility.

* junit XML: 

    ```sh
    kubescape scan --format junit --output results.xml
    ```

* PDF:

    ```sh
    kubescape scan --format pdf --output results.pdf
    ```

* Prometheus metrics:

    ```sh
    kubescape scan --format prometheus
    ```

* HTML

    ```sh
    kubescape scan --format html --output results.html
    ```

* Display all scanned resources (including the resources which passed):

    ```sh
    kubescape scan --verbose
    ```

## Scanning with the Kubescape Operator

Besides the CLI, the Kubescape operator can also be installed via a Helm chart. Installing the Helm chart is an excellent way to begin using Kubescape, as it provides extensive features such as continuous scanning, image vulnerability scanning, runtime analysis, network policy generation, and more. You can find the Helm chart in the [Kubescape-operator documentation](../docs/install-operator.md).
