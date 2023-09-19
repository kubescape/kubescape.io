---
date: 2023-09-19
categories:
  - Announcements
  - Project
authors:
  - craigbox
slug: "introducing-kubescape-3"
---

# Introducing Kubescape 3.0

We are excited to announce the preview release of Kubescape 3.0, the next generation of the CNCF [Kubernetes security posture management](https://www.armosec.io/glossary/kubernetes-security-posture-management/) tool.

Kubescape 3.0 will add:

* Compliance and container scan results stored as Kubernetes resources inside the cluster
* Scanning container images for vulnerabilities from the CLI
* Reporting on the vulnerabilities of all the images in a cluster 
* A new overview security scan, which helps you set a baseline for cluster security
* Highlighting of high-risk workloads: those that could do the most damage if they are compromised
* Improved display output
* A new capability-based Helm chart
* Per workload, per namespace and per cluster Prometheus metrics
* Alerting through Prometheus Alertmanager
* Sending data outside of the cluster to hosted services

Most of these features have landed already, with some being finished over the next few weeks.

!!! note "_[Are you running Kubescape? Want to help us get to incubation in the CNCF? Please help us by filling in our three-question survey!](https://kubescape.io/project/survey/)_"

<!-- more -->

## How we got here

[Kubescape](http://kubescape.io/) launched in September 2021 as a tool for validating a cluster against the NSA hardening guidance that had been issued under a month before. As Kubescape’s original creators [ARMO](https://armosec.io/) built out their hosted offering, the maintainers added features to Kubescape to support that product, including vulnerability scanning and analysis of access control rules. That data was only available through ARMO’s commercial product.

The Kubescape project was donated to the Cloud Native Computing Foundation in 2022. Now, as a CNCF project, we’ve brought key functionality in-cluster, exposing security data in a Kubernetes-native format and enabling more DevOps-focused use cases. 

## New features

### Configuration scan results stored in-cluster

Kubescape can scan running clusters in two ways: with an in-cluster agent installed via a Helm chart, or “agent-free” using the command line tool.  In previous versions, the result data from in-cluster scans was only available to be sent to the ARMO service.

In Kubescape 3.0 we have added in-cluster storage for scan results.  With the Kubescape in-cluster components installed, you will be able to see your scan results in `ConfigurationScanSummary` and `WorkloadConfigurationScanSummary` objects . Watch for enhancements in this area, including continuous scanning, where results are updated as resources change.

### Vulnerability scanning, in-cluster and in the CLI

In previous versions, Kubescape supported vulnerability scanning inside a cluster. We’ve brought this feature to the Kubescape command line in 3.0.

<figure markdown>
  ![Scanning a single image in Kubescape 3.0](/blog/introducing-kubescape-3/scan-image.png){ width="600" }
  <figcaption>The UX for scanning a single image in Kubescape.  Output can be in tabular or `VulnerabilityManifest` JSON format</figcaption>
</figure>

Bringing our image scanning to the command line unlocks many great use cases.  You can scan a manifest file in a CI pipeline, and flag or reject it based on the number and class of vulnerabilities in the containers that will be installed. You can also use the CLI to scan an individual image and get output in the same JSON format as the in-cluster objects.

Our in-cluster agent previously had support for scanning the images in a Kubernetes cluster. We have extended that support to include exposing these results in-cluster with `VulnerabilityManifestSummary` objects, with full SBOM and vulnerability information in related `VulnerabilityManifest` objects. including software bills of materials (SBOMs) for each container, and filtered output using the Kubescape relevancy engine.

```yaml
{
    "apiVersion": "spdx.softwarecomposition.kubescape.io/v1beta1",
    "kind": "VulnerabilityManifestSummary",
    "metadata": {
        "annotations": {
            "kubescape.io/image-id": "nginx@sha256:6926dd802f40e5e7257fded83e0d8030039642e4e10c4a98a6478e9c6fe06153",
            "kubescape.io/status": "",
            "kubescape.io/wlid": "wlid://cluster-docker-desktop/namespace-default/deployment-nginx-deployment",
            "kubescape.io/workload-container-name": "nginx"
        },
        "creationTimestamp": "2023-09-18T08:37:38Z",
        "labels": {
            "kubescape.io/context": "non-filtered",
            "kubescape.io/image-id": "nginx-sha256-6926dd802f40e5e7257fded83e0d8030039642e4e10c4a98a6",
            "kubescape.io/image-name": "nginx",
            "kubescape.io/workload-api-group": "apps",
            "kubescape.io/workload-api-version": "v1",
            "kubescape.io/workload-container-name": "nginx",
            "kubescape.io/workload-kind": "Deployment",
            "kubescape.io/workload-name": "nginx-deployment",
            "kubescape.io/workload-namespace": "default"
        },
        "name": "Deployment-nginx-deployment-nginx",
        "namespace": "default",
        "resourceVersion": "1",
        "uid": "3aea854d-8eea-4b8b-8a99-6472d3bc0521"
    },
    "spec": {
        "severities": {
            "critical": {
                "all": 0,
                "relevant": 0
            },
            "high": {
                "all": 4,
                "relevant": 0
            },
            "low": {
                "all": 4,
                "relevant": 0
            },
            "medium": {
                "all": 23,
                "relevant": 0
            },
            "negligible": {
                "all": 72,
                "relevant": 0
            },
            "unknown": {
                "all": 10,
                "relevant": 0
            }
        },
        "vulnerabilitiesRef": {
            "all": {
                "kind": "vulnerabilitymanifests",
                "name": "nginx-e06153",
                "namespace": "default"
            },
            "relevant": {
                "kind": "",
                "name": "",
                "namespace": ""
            }
        }
    },
    "status": {}
}
```

### New scan modes

We have introduced a new cluster overview/baseline security scan, which performs some key security checks and then shows you the number of resources which have certain permissions. You are then able to set up risk acceptance rules to allow for things which are deliberately installed or configured about your cluster.

For example, malware in a cluster will often attempt to create a cluster admin role, or a role with permissions that approximates that.  With the Kubescape baseline scan, you can identify which roles you have installed that should have these permissions, and then easily see, or be notified, when the configuration changes from your secure baseline.

If you would like to preview the new security scan mode, update Kubescape to the latest version (2.9.x) and try `kubescape scan --view=security`.

This scan will become the default behavior of `kubescape scan` in the coming weeks. You can access the previous default by running `kubescape scan framework allcontrols,nsa,mitre`.

<figure markdown>
  ![The new overview security scan](/blog/introducing-kubescape-3/security-scan.png){ width="600" }
  <figcaption>The new overview security scan. Use Kubescape's risk acceptance feature to get all the scores down to 0, and then anything above this represents an issue worth investigating.</figcaption>
</figure>


### Enhancements to monitoring and alerting

Now we have data in the cluster regarding the configuration and vulnerability status of your environment, we can make this available through Prometheus.  Our wonderful LFX mentorship students [Tejas Jamdade](https://github.com/0xt3j4s) and [Yash Raj Singh](https://github.com/yrs147) have been building a Prometheus exporter and dashboards. These will allow you to look at control failures and vulnerabilities at a workload, namespace or cluster level, as well as setting up [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) to inform you when security problems exceed a configurable threshold.

### Third-party cluster data services

Good security practice is to store security information regarding a cluster outside of that cluster, so that it cannot be altered in the event of an attack.

As part of our commitment to vendor neutrality as a CNCF project, we have updated support for submitting data outside the cluster it is collected from. Previously, this feature was tightly coupled to the service operated by Kubescape’s creators. With Kubescape 3.0, we are fully documenting the APIs required for operating a Kubescape-compatible service, and allowing submission to any URL that is running a compliant service.

### Capabilities-based in-cluster installation

With all our new in-cluster features, we’ve made it easy to enable and disable them in our Helm chart.  You can now configure configuration scanning, vulnerability scanning, relevancy, and the node scanner in the `values.yaml` file:

``` yaml
capabilities:
  relevancy: enable
  configurationScan: enable
  continuousScan: disable
  vulnerabilityScan: enable
  nodeScan: enable
```

### Other new features

* [distroless](https://github.com/GoogleContainerTools/distroless) base images for added security
* New eBPF engine, for lower resource consumption and improved kernel compatibility
* Experimental support for [patching container images](https://github.com/kubescape/kubescape/pull/1332) (thanks to LFX mentorship student [Anubhav Gupta](https://github.com/anubhav06)) 
* Much nicer color and table output (thanks to contributor [Anant Vijay](https://github.com/XDRAGON2002))
* Improvements for empty scans and scanning deleted resources

## Kubescape 3.1 and beyond

We’re certainly not done here! For the rest of the year we will be finishing off our compliance and vulnerability scanning roadmap, including an in-cluster UI for better visualization of the saved results.

<figure markdown>
  ![Kubescape 3.1 UI preview](/blog/introducing-kubescape-3/ui-preview.png){ width="600" }
  <figcaption>A work-in-progress look at what we’re building for the in-cluster UI. The final UI will probably be much different (and much better!)</figcaption>
</figure>

## Join the Kubescape community

We welcome your feedback and ideas for improvement. We hold [community meetings](https://kubescape.io/project/community/#monthly-meeting) on Zoom, on the first Tuesday of every month, at 14:00 GMT.

Thanks to all our contributors! Check out our [CONTRIBUTING](https://github.com/kubescape/kubescape/blob/master/CONTRIBUTING.md) file to learn how to join them.

* Feel free to pick a task from the [good first issue list](https://github.com/kubescape/kubescape/issues?q=is%3Aissue+is%3Aopen+label%3A%22open+for+contribution%22) and suggest a design
* [Open an issue](https://github.com/kubescape/kubescape/issues/new/choose): we aim to respond to all issues within 48 hours
* [Join the CNCF Slack](https://slack.cncf.io/) and then our [users](https://cloud-native.slack.com/archives/C04EY3ZF9GE) or [developers](https://cloud-native.slack.com/archives/C04GY6H082K) channel
* Don’t forget to leave a star on our [repository](https://github.com/kubescape/kubescape): it means the world to us!

The Kubescape project follows the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md).

## Watch this space

We will be publishing more detailed posts about the new features in Kubescape 3.0 in the coming weeks. Stay tuned!