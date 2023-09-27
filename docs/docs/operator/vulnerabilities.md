# Vulnerability scanning with the Kubescape operator

The Kubescape operator includes a component which performs vulnerability scanning of all container images that are running in your cluster.  

The **Kubevuln** component scans images which are deployed to the cluster when:

- A new Deployment, StatefulSet, DaemonSet or naked Pod is created
- The container image tag in an existing Deployment, StatefulSet, DaemonSet or Pod is changed

It uses the [Grype](https://github.com/anchore/grype) engine to evaluate against a [database of known vulnerabilities](https://github.com/anchore/grype#grypes-database) from a variety of publicly available vulnerability data sources.  The sources include the security announcement data from all major Linux distributions, the [National Vulnerability Database](https://nvd.nist.gov/vuln/data-feeds), and [GitHub security advisories](https://github.com/advisories).

The results are made available in API objects exposed by the [Kubescape storage engine](index.md#in-cluster-storage).

## Vulnerabilty summaries

For each running container, a `VulnerabilityManifestSummary` object will be created in the namespace.  These are named for the method that the container is deployed.

!!! note "Why do you need more than one object per container?"
    Kubescape's relevancy features consider usage of a container as part of its vulnerability profile.  If code is not run during the inspection period, a component may be filtered from the vulnerabilty list. This means that the SBOM and number of relevant vulnerabilities for a container can vary depending on how it is deployed. [Read more about vulnerability relevancy.](relevancy.md)

Here is an example `VulnerabilityManifestSummary`.  You will see that the relevancy feature is not enabled, and a link to the full vulnerability manifest is provided.

```yaml
apiVersion: spdx.softwarecomposition.kubescape.io/v1beta1
kind: VulnerabilityManifestSummary
metadata:
  annotations:
    kubescape.io/image-id: nginx@sha256:6926dd802f40e5e7257fded83e0d8030039642e4e10c4a98a6478e9c6fe06153
    kubescape.io/status: ""
    kubescape.io/wlid: wlid://cluster-docker-desktop/namespace-default/deployment-nginx-deployment
    kubescape.io/workload-container-name: nginx
  creationTimestamp: "2023-09-25T06:55:06Z"
  labels:
    kubescape.io/context: non-filtered
    kubescape.io/image-id: nginx-sha256-6926dd802f40e5e7257fded83e0d8030039642e4e10c4a98a6
    kubescape.io/image-name: nginx
    kubescape.io/workload-api-group: apps
    kubescape.io/workload-api-version: v1
    kubescape.io/workload-container-name: nginx
    kubescape.io/workload-kind: Deployment
    kubescape.io/workload-name: nginx-deployment
    kubescape.io/workload-namespace: default
  name: Deployment-nginx-deployment-nginx
  namespace: default
  resourceVersion: "1"
  uid: 056f6be1-ebb1-4026-89ef-a4d6d6a8bf54
spec:
  severities:
    critical:
      all: 0
      relevant: 0
    high:
      all: 4
      relevant: 0
    low:
      all: 4
      relevant: 0
    medium:
      all: 27
      relevant: 0
    negligible:
      all: 72
      relevant: 0
    unknown:
      all: 6
      relevant: 0
  vulnerabilitiesRef:
    all:
      kind: vulnerabilitymanifests
      name: nginx-e06153
      namespace: default
    relevant:
      kind: ""
      name: ""
      namespace: ""
status: {}
```

## Vulnerabilty manifests

The `VulnerabilityManifest` contains the full output of the vulnerability scanner, and lets you identify which vulnerabilities were detected in which files.

## Relevancy filtering

Kubescape can examine the use of containers at runtime to suggest which vulnerabilities are most relevant. [Learn about the relevancy feature.](relevancy.md)

## Uploading scan results to a provider

If you have Kubescape configured to use a [provider](../providers.md), then Kubevuln will send 

## Configuration

### Scanning images pulled from private registries

To scan images that are pulled from private registries, you can define a Secret with credentials.

!!! note Note
    The secret must start with the name `kubescape-registry-scan`.

For example:

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: kubescape-registry-scan-my-acr-secret
  namespace: kubescape
type: Opaque
stringData:
  registriesAuth: |
    [     
      {
        "registry": "myrepo.azurecr.io",
        "username": "<username/clientID>",
        "password": "<password/secret>",
        "auth_method": "credentials"
      }
    ]
```

### Air-gapped installation support

It is possible to get image vulnerability results in an air-gapped mode, where you don't have access to download the Grype database. 

When installing the Helm chart, add the following flag: `--set grypeOfflineDB.enabled=true`

### Recurring image vulnerability scanning

The scanner is triggered by a `CronJob` called `kubevuln-scheduler`. By default, the scanner is triggered daily at midnight:

```
kubevulnScheduler.scanSchedule="0 0 * * *"` 
```

To customize the scan frequency, use `--set kubevulnScheduler.scanSchedule` when installing the Helm chart.
