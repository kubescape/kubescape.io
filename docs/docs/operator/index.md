# The Kubescape operator

When installed in your cluster, Kubescape runs as a set of microservices.  These allow you to continually monitor the security posture of the cluster the operator is installed in.

The Kubescape operator includes:

* scanning for misconfigurations
* scanning all deployed images for vulnerabilties (CVEs)
* exposing in-cluster data as Kubernetes API objects
* exporting data to a configured [provider](../providers.md) 
* allowing secure control by a configured provider

## Install

The Kubescape operator is installed using [Helm](https://helm.sh/).
[Here](../install-operator.md) you can find the installation instructions for the Kubescape operator.

## Misconfiguration scanning

The `kubescape` service uses the same engine as the Kubescape CLI to scan the cluster for misconfigurations.

## Vulnerability scanning

The `kubevuln` microservice scans container images for vulnerabilities. 

* [Learn about vulnerability scanning](vulnerabilities.md)

## In-cluster storage

The `storage` microservice provides an [aggregated API server](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/) to expose Kubescape scan data inside the cluster.

In-cluster scan results are considered ephemeral, as they are regularly updated and can be fully regenerated. If you want a history we recommend you use Kubescape's [provider interface](../providers.md) to send the data out of the cluster when scans are complete.

To see a list of the types that are added to your cluster, use `kubectl api-resources`:

```
$ kubectl api-resources | grep kubescape
applicationactivities                                     spdx.softwarecomposition.kubescape.io/v1beta1   true         ApplicationActivity
applicationprofiles                                       spdx.softwarecomposition.kubescape.io/v1beta1   true         ApplicationProfile
applicationprofilesummaries                               spdx.softwarecomposition.kubescape.io/v1beta1   true         ApplicationProfileSummary
configurationscansummaries                                spdx.softwarecomposition.kubescape.io/v1beta1   false        ConfigurationScanSummary
generatednetworkpolicies                                  spdx.softwarecomposition.kubescape.io/v1beta1   true         GeneratedNetworkPolicy
knownservers                                              spdx.softwarecomposition.kubescape.io/v1beta1   false        KnownServer
networkneighborses                                        spdx.softwarecomposition.kubescape.io/v1beta1   true         NetworkNeighbors
openvulnerabilityexchangecontainers                       spdx.softwarecomposition.kubescape.io/v1beta1   true         OpenVulnerabilityExchangeContainer
sbomspdxv2p3filtereds                                     spdx.softwarecomposition.kubescape.io/v1beta1   true         SBOMSPDXv2p3Filtered
sbomspdxv2p3s                                             spdx.softwarecomposition.kubescape.io/v1beta1   true         SBOMSPDXv2p3
sbomsummaries                                             spdx.softwarecomposition.kubescape.io/v1beta1   true         SBOMSummary
sbomsyftfiltereds                                         spdx.softwarecomposition.kubescape.io/v1beta1   true         SBOMSyftFiltered
sbomsyfts                                                 spdx.softwarecomposition.kubescape.io/v1beta1   true         SBOMSyft
vulnerabilitymanifests                                    spdx.softwarecomposition.kubescape.io/v1beta1   true         VulnerabilityManifest
vulnerabilitymanifestsummaries                            spdx.softwarecomposition.kubescape.io/v1beta1   true         VulnerabilityManifestSummary
vulnerabilitysummaries                                    spdx.softwarecomposition.kubescape.io/v1beta1   false        VulnerabilitySummary
workloadconfigurationscans                                spdx.softwarecomposition.kubescape.io/v1beta1   true         WorkloadConfigurationScan
workloadconfigurationscansummaries                        spdx.softwarecomposition.kubescape.io/v1beta1   true         WorkloadConfigurationScanSummary
```

1. [Custom Resource Definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions), a common approach for adding new types to the Kubernetes API.
2. Software Bill of Materials    
    
## Telemetry

Several of our in-cluster components implement telemetry data using OpenTelemetry (OTel). You can optionally install an OTel collector in your cluster to aggregate these metrics and send them to your own tracing tool.

* [Learn about setting up telemetry](https://github.com/kubescape/helm-charts/blob/main/charts/kubescape-operator/README.md#setting-up-telemetry)

## Automation and control

* The `operator` and `gateway` microservices interact to start or [schedule](scheduled-scans.md) scans. 
* The `kollector` service sends information about the state of the cluster to a configured [provider](../providers.md). 

For information on how these services interact, [check out their documentation on GitHub.](https://github.com/kubescape/helm-charts/blob/main/charts/kubescape-operator/README.md)

## Node agent

Some functions of Kubescape require access to every node.  These include controls which require [host scanning](../scanning.md#the-host-scanner), and [calculating runtime vulnerability relevancy](relevancy.md).  

The optional Kubescape node agent runs as a DaemonSet, deployed to every node in your cluster.