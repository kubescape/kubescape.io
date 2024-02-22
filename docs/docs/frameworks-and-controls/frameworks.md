# Supported frameworks

Kubescape comes with support for the following frameworks:

## NSA  

The `nsa` framework is built on the [Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF) released by the published by the United States [National Security Agency](https://nsa.gov) and [Cybersecurity and Infrastructure Security Agency](https://cisa.gov/). Controls in this framework will validate adherence to these best practices.

## MITRE

The `mitre` framework is based on the MITRE ATT&CK® framework, a knowledge base of known tactics, techniques and procedures (TTP) that are involved in cyberattacks. The [Threat Matrix for Kubernetes](https://microsoft.github.io/Threat-Matrix-for-Kubernetes/) was inspired from MITRE ATT&CK, and contains mitigations specific to Kubernetes environments and attack techniques. Controls in this framework map to the various TTP in the threat matrix.

## CIS

The CIS family of frameworks are derived from the [CIS Kubernetes Benchmarks](https://www.cisecurity.org/benchmark/kubernetes), a set of secure configuration guidelines developed for Kubernetes.

The frameworks are:

* `cis-v1.23-t1.0.1`, for default Kubernetes clusters
* `cis-aks-t1.2.0`, for Azure Kubernetes Service
* `cis-eks-t1.2.0`, for Amazon Elastic Kubernetes Service

## Scanning using a framework

To scan a cluster using a particular framework, use the command `kubescape scan framework <framework>`.  You can specify more than one framework by providing a comma-separated list, such as `kubescape scan framework nsa,mitre`.

To get a full list of frameworks that kubescape supports run the command `kubescape list frameworks`.

!!! note "Note"
    Before Kubescape 3.0, the default behaviour of `kubescape scan` was to scan the NSA and MITRE frameworks.

[Learn more about scanning](../scanning.md).

## Using frameworks for compliance

Kubescape uses two metrics to help you use frameworks for validating the compliance of an environment.

The **control compliance score** measures the compliance of individual controls within a framework. It is calculated by evaluating the ratio of resources that passed to the total number of resources evaluated against that control.

The **framework compliance score** provides an overall assessment of your cluster's compliance with a specific framework. It is calculated by averaging the Control Compliance Scores of all controls within the framework.

In scan results, you may see the control compliance score listed as **Action Required**.  Some controls require configuration before they can be evaluated; for example, the list of allowed container registries. See [Customizing control configuration](configuring-controls.md).

## Downloading frameworks

To learn how to download the framework data, [see the documentation for installing in an air-gapped environment](../install-cli.md#offlineair-gapped-environment-support).

## Custom frameworks

To learn how to create and use your own custom framework, see the [Contributing section of the regolibrary README.md](https://github.com/kubescape/regolibrary/blob/master/README.md#contributing).

You can use a locally defined framework