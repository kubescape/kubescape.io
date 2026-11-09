# Scanning with Kubescape

## Introduction

A common use case for Kubescape is to validate the configuration of a Kubernetes cluster, or some resources you could deploy to one.

## Scanning using the command line interface

### The overview scan

Running `kubescape scan` with no other parameters will perform the cluster overview/baseline security scan.  This performs some key security checks and then shows you the number of resources which have certain permissions. You are then able to set up [risk acceptance rules](accepting-risk.md) to allow for things which are deliberately installed or configured about your cluster.

For example, malware in a cluster will often attempt to create a cluster admin role, or a role with permissions that approximates that.  With the Kubescape baseline scan, you can identify which roles you have installed that should have these permissions, and then easily see, or be notified, when the configuration changes from your secure baseline.

<div style="width: 100%; margin: 1.5em 0;">
  <video controls autoplay muted loop playsinline width="100%" poster="../../assets/scanning/scan-overview-poster.png" style="width: 100%; aspect-ratio: 1916 / 970; display: block; border-radius: 8px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
    <source src="../../assets/scanning/scan-overview.mp4" type="video/mp4">
    <source src="/assets/scanning/scan-overview.mp4" type="video/mp4">
    <source src="../assets/scanning/scan-overview.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <p style="text-align: center; font-size: 0.85em; color: var(--md-default-fg-color--light); margin-top: 0.5em;"><em>Running a baseline cluster overview scan with Kubescape</em></p>
</div>

!!! info "Key Results from this Overview Scan"
    * **Target Context:** Scans the active Kubernetes cluster context automatically (e.g., `docker-desktop`).
    * **Multi-Domain Baseline:** Evaluates 48 baseline controls categorized by:
        * **Control Plane & Networking:** Validates Kubelet authentication, insecure ports, and network policies.
        * **Workload Security:** Checks for non-root containers, privileged flags, and known CVEs.
        * **Resource & Storage:** Identifies missing CPU/memory limits and writable `hostPath` mounts.
    * **Highest-Stake Workloads:** Automatically identifies workloads with the greatest blast radius if compromised (e.g., `kube-apiserver`, `etcd`, `kube-proxy`).
    * **Preliminary Compliance:** Provides quick compliance estimations against established frameworks (MITRE ATT&CK and NSA-CISA).
    * **Drill-Down Recommendation:** The table suggests exact commands to investigate specific failing controls (e.g., `kubescape scan control C-0057 -v`).

### Framework scans

A common use case for Kubescape is to validate a cluster against a [security framework](frameworks-and-controls/index.md). To run a framework scan:

```sh
kubescape scan framework <framework>
```

[Learn what frameworks are available, or how to create your own](frameworks-and-controls/index.md).

For example, to scan your cluster against the [NSA-CISA hardening guidance](frameworks-and-controls/frameworks.md#nsa):

```sh
kubescape scan framework nsa
```

<div style="width: 100%; margin: 1.5em 0;">
  <video controls autoplay muted loop playsinline width="100%" poster="../../assets/scanning/scan-framework-nsa-poster.png" style="width: 100%; aspect-ratio: 1468 / 706; display: block; border-radius: 8px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
    <source src="../../assets/scanning/scan-framework-nsa.mp4" type="video/mp4">
    <source src="/assets/scanning/scan-framework-nsa.mp4" type="video/mp4">
    <source src="../assets/scanning/scan-framework-nsa.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <p style="text-align: center; font-size: 0.85em; color: var(--md-default-fg-color--light); margin-top: 0.5em;"><em>Scanning an active cluster against the NSA-CISA security framework</em></p>
</div>

!!! info "Key Results from this Framework Scan"
    * **Framework Compliance:** Evaluates all 26 controls defined by the NSA-CISA Kubernetes Hardening Guidance.
    * **Control Breakdown:** Displays the number of passed, failed, and action-required controls with their individual compliance scores.
    * **Severity Distribution:** Highlights failed resources categorized by risk level (Critical, High, Medium, Low).
    * **Resource Summary:** Provides the aggregate compliance score (e.g., 67.13%) calculated across all evaluated resources.
    * **Scan Coverage:** Confirms the percentage of controls evaluated (91% in this demo) and notes any cloud-specific checks skipped on local clusters.

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

╭──────────┬──────────────────────────────────┬────────────────────────────────────┬────────────────────────────────────╮
│ Severity │ Control name                     │ Docs                               │ Assisted remediation               │
├──────────┼──────────────────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ Medium   │ Automatic mapping of service     │ https://hub.armosec.io/docs/c-0034 │ automountServiceAccountToken=false │
│          │ account                          │                                    │                                    │
╰──────────┴──────────────────────────────────┴────────────────────────────────────┴────────────────────────────────────╯
```

When scanning files rather than a cluster, each block is preceded by a `Source:` line naming
the file the resource came from.

Assisted remediation identifies *where* to look: the JSON path of the field that triggered
the control, with a suggested value appended for the paths Kubescape can fix (`path=value`).
It does not show the value the field currently holds.

<div style="width: 100%; margin: 1.5em 0;">
  <video controls autoplay muted loop playsinline width="100%" poster="../../assets/scanning/scan-verbose-poster.png" style="width: 100%; aspect-ratio: 1462 / 698; display: block; border-radius: 8px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
    <source src="../../assets/scanning/scan-verbose.mp4" type="video/mp4">
    <source src="/assets/scanning/scan-verbose.mp4" type="video/mp4">
    <source src="../assets/scanning/scan-verbose.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <p style="text-align: center; font-size: 0.85em; color: var(--md-default-fg-color--light); margin-top: 0.5em;"><em>Scanning local resources with verbose mode enabled (<code>--verbose</code>)</em></p>
</div>

!!! info "Key Results from Verbose Scanning"
    * **Granular Per-Resource Breakdown:** Surfaces exact failing resources (Deployments, Pods, ServiceAccounts) with their API version, name, and namespace.
    * **Actionable Assisted Remediation:** Shows the precise YAML/JSON path and suggested fix value (`path=value`, e.g., `automountServiceAccountToken=false` or `privileged=false`).
    * **Direct Documentation Links:** Includes immediate URLs to Kubescape control documentation for remediation context and background.
    * **Interactive Drill-Down Commands:** Generates direct copy-paste commands to inspect individual controls (e.g., `kubescape scan control C-0034 pod.yaml -v`).

### Scanning files

Kubescape can be used to scan local YAML/JSON files before they are deployed to Kubernetes. This is a common use case for integrations into CI/CD systems; see [Integrations](integrations/index.md) for how this can be used.

* Scan local YAML/JSON files before deploying:
    ```sh
    kubescape scan *.yaml
    ```

<div style="width: 100%; margin: 1.5em 0;">
  <video controls autoplay muted loop playsinline width="100%" poster="../../assets/scanning/scan-manifest-poster.png" style="width: 100%; aspect-ratio: 1464 / 704; display: block; border-radius: 8px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
    <source src="../../assets/scanning/scan-manifest.mp4" type="video/mp4">
    <source src="/assets/scanning/scan-manifest.mp4" type="video/mp4">
    <source src="../assets/scanning/scan-manifest.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <p style="text-align: center; font-size: 0.85em; color: var(--md-default-fg-color--light); margin-top: 0.5em;"><em>Creating a local Kubernetes manifest and scanning it before deployment</em></p>
</div>

!!! info "Key Results from this Manifest Scan"
    * **No Cluster Required:** Runs entirely on local YAML/JSON files without needing an active Kubernetes cluster or network connection.
    * **Pre-Deployment Shift-Left Security:** Catches misconfigurations during development or in CI before manifests are deployed.
    * **Node Escape Detection:** Instantly flags dangerous container configurations such as `privileged: true`, non-root container violations, and privilege escalation.
    * **Resource & Hygiene Checks:** Identifies missing CPU/memory limits, naked pods, and missing liveness/readiness probes.
    * **Direct Remediation Command:** Suggests the exact CLI command to inspect any failed control (e.g., `kubescape scan control C-0057 pod.yaml -v`).

* Scan Kubernetes manifest files from a Git repository:

    ```sh
    kubescape scan https://github.com/kubescape/kubescape
    ```

* Scan Helm charts:

    ```sh
    kubescape scan </path/to/directory>
    ```

<div style="width: 100%; margin: 1.5em 0;">
  <video controls autoplay muted loop playsinline width="100%" poster="../../assets/scanning/scan-helm-poster.png" style="width: 100%; aspect-ratio: 1474 / 706; display: block; border-radius: 8px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
    <source src="../../assets/scanning/scan-helm.mp4" type="video/mp4">
    <source src="/assets/scanning/scan-helm.mp4" type="video/mp4">
    <source src="../assets/scanning/scan-helm.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <p style="text-align: center; font-size: 0.85em; color: var(--md-default-fg-color--light); margin-top: 0.5em;"><em>Creating and scanning a Helm chart directory with Kubescape</em></p>
</div>

!!! info "Key Results from this Helm Chart Scan"
    * **Automatic Template Rendering:** Kubescape automatically renders your chart templates against default `values.yaml` without needing manual template generation or a running cluster.
    * **Multi-Workload Posture:** Scans all rendered resources (Deployments, Pods, Services) in a single pass.
    * **Highest-Stake Workloads Ranked:** Identifies high-impact rendered resources (like `deployment.yaml` and test pods).
    * **Pre-Deployment Helm Validation:** Validates security controls before publishing charts or running `helm install`.

    !!! note "Note"
        Kubescape will load the default VALUES file and will use it to render the chart.
        Charts that require custom values will not be processed by Kubescape.

* Scan a Kustomize directory:

    ```sh
    kubescape scan </path/to/directory>
    ```

    !!! note "Note"
        Kubescape will generate Kubernetes YAML objects using a `kustomize` file and scan them.

### Scanning Images

Kubescape can scan container images for known vulnerabilities before deployment. You can scan images from public registries, private registries, or use an offline vulnerability database.

* Scan a public image:
    ```sh
    kubescape scan image <image:tag>
    ```

<div style="width: 100%; margin: 1.5em 0;">
  <video controls autoplay muted loop playsinline width="100%" poster="../../assets/scanning/scan-image-poster.png" style="width: 100%; aspect-ratio: 1452 / 698; display: block; border-radius: 8px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
    <source src="../../assets/scanning/scan-image.mp4" type="video/mp4">
    <source src="/assets/scanning/scan-image.mp4" type="video/mp4">
    <source src="../assets/scanning/scan-image.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <p style="text-align: center; font-size: 0.85em; color: var(--md-default-fg-color--light); margin-top: 0.5em;"><em>Scanning a container image for vulnerabilities with Kubescape</em></p>
</div>

!!! info "Key Results from Container Image Vulnerability Scanning"
    * **CVE Identification & Severity Triage:** Scans container layers and packages, categorizing CVEs by severity (Critical, High, Medium, Low).
    * **Exploitability Intelligence (KEV & EPSS):** Flags actively exploited vulnerabilities (**KEV: yes**) and displays **EPSS** probability scores (e.g., 100% / 99th percentile) to prioritize real-world threats.
    * **Clear Remediation Targets:** Identifies vulnerable software components, currently installed versions, and the exact patched version available in `Fixed in`.
    * **Shift-Left Registry & Local Scanning:** Can scan public container registries (`nginx:1.20`), private registries with credentials, or local images prior to cluster deployment.

* Scan with verbose output:
    ```sh
    kubescape scan image <image:tag> -v
    ```

* Scan a private registry image
    ```sh
    kubescape scan image </path/to/image:tag> --username user --password pass
    ```

#### Using an Offline Grype Database

* Start the offline Grype database server
   ```sh
   docker run --rm -p8080:8080 quay.io/kubescape/grype-offline-db:v6-latest
   ```

* Scan an image using the offline database
  ```sh 
  kubescape scan image --grype-db-url http://localhost:8080/databases/ <image:tag>
  ```


### Score-based thresholds

Kubescape exposes two score-based threshold flags:

* `--compliance-threshold <float>` — exit code 1 if the compliance score is below the given percent.
* `--fail-threshold <float>` *(deprecated)* — exit code 1 if the risk score is above the given percent. This gates a different metric (risk score, not compliance score); it is being phased out in favour of `--compliance-threshold`.

These flags apply to the framework/control subcommands and to the resource/control views:

```sh
kubescape scan framework nsa --compliance-threshold 80 ./manifests
kubescape scan control C-0017 --compliance-threshold 80 ./manifests
kubescape scan --view resource --compliance-threshold 80 ./manifests
kubescape scan --view control  --compliance-threshold 80 ./manifests
```

The default `kubescape scan [path]` uses `--view security`, which does not evaluate against a score threshold — pick one of the forms above when you want the exit code to reflect the score. `--severity-threshold` and `--fail-coverage-below` apply in every view.

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

* HTML:

    ```sh
    kubescape scan --format html --output results.html
    ```
- SARIF:

    ```sh
    kubescape scan --format sarif --output results.sarif
    ```

- GitLab SAST:

    ```sh
    kubescape scan --format gitlab-sast --output gl-sast-report.json
    ```

- YAML:

    ```sh
    kubescape scan --format yaml --output results.yaml
    ```

- CSV:

    ```sh
    kubescape scan --format csv --output results.csv
    ```

- Markdown:

    ```sh
    kubescape scan --format markdown --output results.md
    ```

- PolicyReport:

    ```sh
    kubescape scan --format policyreport --output policyreport.yaml
    ```

* Multiple output formats in a single scan:

    ```sh
    kubescape scan --format json,html,prometheus --output result
    ```

* Display all scanned resources (including the resources which passed):

    ```sh
    kubescape scan --verbose
    ```

## Protecting report metadata

Kubescape reports can contain sensitive information such as Pod names, namespaces, resource names, annotations, repository metadata, and source paths. In some environments, this information is classified as confidential and should only be visible to a restricted group of users.

Only labels specified through `--labels-to-copy` are pseudonymized or encrypted. All other resource labels remain unchanged in the generated report.

For example, a report may include a namespace named after an employee or a Pod name containing an unreleased product. While this information is valuable for security analysis, it may not be appropriate to disclose when sharing reports outside your organization.

To help protect sensitive report metadata, Kubescape provides two mechanisms:

* **Hide (`--hide`)** replaces sensitive report metadata with deterministic pseudonyms to reduce incidental exposure.
* **Encrypt (`--encrypt`)** encrypts sensitive report metadata so it can later be restored using `kubescape decrypt`.

### Hiding sensitive metadata

Replace sensitive report metadata with deterministic pseudonyms when exporting JSON reports.

This reduces incidental exposure but is not a confidentiality guarantee. Values drawn from small or predictable sets, such as common namespace names, may be recovered by comparing candidate hashes. Use `--encrypt` when sensitive metadata requires confidentiality.

### Hiding examples

* Scan the current cluster and generate an anonymized report:

    ```sh
    kubescape scan --hide --format json --output report.json
    ```

* Scan local manifests and save an anonymized report:

    ```sh
    kubescape scan /path/to/manifests \
      --hide \
      --format json \
      --output report.json
    ```

    !!! note "Note"
        `--hide` replaces sensitive values with deterministic pseudonyms derived from an unsalted hash of the original value. Values drawn from a small or guessable set, such as common namespace names, can be recovered by hashing candidate values and matching the result, and identical values produce identical pseudonyms across reports.

        Use `--hide` to reduce incidental exposure, not as a confidentiality guarantee. To share a report whose metadata is genuinely protected, use `--encrypt` and withhold the master key.

### Encrypting sensitive metadata

Encrypt sensitive report metadata using the master key supplied through the `KUBESCAPE_MASTER_KEY` environment variable.

The master key is used as raw bytes and must be exactly 32 bytes (32 ASCII characters) long. Use `--format json` to generate a report that can later be decrypted with `kubescape decrypt`.

If both `--encrypt` and `--hide` are specified, `--encrypt` takes precedence.

### Encryption examples

* Generate an encrypted report:

    ```sh
    # The key is used as raw bytes and must be exactly 32 bytes (32 ASCII characters) long.
    # Note: `openssl rand -base64 32` (44 chars) and `openssl rand -hex 32` (64 chars)
    # are NOT valid — they exceed 32 bytes once passed through as raw text.
    export KUBESCAPE_MASTER_KEY="01234567890123456789012345678901"

    kubescape scan \
      --encrypt \
      --format json \
      --output encrypted-report.json
    ```

* Scan local manifests and generate an encrypted report:

    ```sh
    kubescape scan /path/to/manifests \
      --encrypt \
      --format json \
      --output encrypted-report.json
    ```

    !!! warning "Store the master key"
        Store `KUBESCAPE_MASTER_KEY` in a secret manager before generating the report.

        The key is **not** written to the report and cannot be recovered. Without this key, the encrypted metadata is permanently unreadable.

    !!! note "Note"
        `--encrypt` requires the `KUBESCAPE_MASTER_KEY` environment variable. The key must be exactly 32 bytes (32 ASCII characters) long. Reports that you intend to decrypt later must be generated with `--format json`, and the same key must be supplied when running `kubescape decrypt`.

### Decrypting encrypted reports

Decrypt report metadata from a JSON report that was protected with `kubescape scan --encrypt`.

Only metadata encrypted by `kubescape scan --encrypt` is restored. Metadata pseudonymized with `--hide` cannot be recovered by `kubescape decrypt`.

### Decryption examples

* Decrypt an encrypted report:

    ```sh
    # Use the exact 32-byte key that was used with `kubescape scan --encrypt`,
    # retrieved from wherever you stored it.
    export KUBESCAPE_MASTER_KEY="01234567890123456789012345678901"

    kubescape decrypt encrypted-report.json
    ```

* Save the decrypted report to a file:

    ```sh
    kubescape decrypt encrypted-report.json > decrypted-report.json
    ```

    !!! note "Note"
        `kubescape decrypt` restores metadata encrypted by `kubescape scan --encrypt`. It does not reverse deterministic pseudonymization produced by `--hide`.

## Scanning with the Kubescape Operator

Besides the CLI, the Kubescape operator can also be installed via a Helm chart. Installing the Helm chart is an excellent way to begin using Kubescape, as it provides extensive features such as continuous scanning, image vulnerability scanning, runtime analysis, network policy generation, and more. You can find the Helm chart in the [Kubescape-operator documentation](../docs/install-operator.md).
