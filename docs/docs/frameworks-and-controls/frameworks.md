A security framework is a set of guidelines, best practices, or standards, usually codified as a number of [controls](../controls/).

Security frameworks are often published by government agencies or non-profit research centers. Many  groups have published guidance on how to improve the security posture of a Kubernetes environment.

ARMO Platform includes collections of controls that are arranged into frameworks. These are drawn from [RegoLibrary](https://github.com/kubescape/regolibrary/tree/master/frameworks), an open source library maintained by ARMO. You can use ARMO Platform to validate running clusters and manifest files against frameworks included in RegoLibrary. By default, ARMO Platform validates against all available frameworks to verify how compliant your Kubernetes environment is with those frameworks.

## Published frameworks

The most commonly referenced security frameworks are:

- [NSA-CISA Kubernetes Hardening Guide](https://www.armosec.io/blog/nsa-cisa-kubernetes-hardening-guide/) , published by the United States [National Security Agency](https://nsa.gov) and [Cybersecurity and Infrastructure Security Agency](https://cisa.gov/)

- [CIS Benchmarks](https://www.armosec.io/blog/cis-kubernetes-benchmark-framework-scanning-tools-comparison/,), published by the [Center for Internet Security](https://www.cisecurity.org/):
  - CIS Kubernetes Benchmark
  - CIS Amazon Elastic Kubernetes Service (EKS) Benchmark
  - CIS Azure Kubernetes Service (AKS) Benchmark

- [MITRE ATT&CK Threat Matrix for Kubernetes](https://microsoft.github.io/Threat-Matrix-for-Kubernetes/), published by [MITRE](https://mitre.org/) and [Microsoft](https://www.microsoft.com)

## View controls included in a framework

- In the sidebar, click **Settings**.
- Navigate to Workspace, and click **Frameworks**.

![ARMO Platform Frameworks](https://files.readme.io/51637c4-ARMO-Platform_3.png)

- Click the arrow next to a framework to view or add controls.

You cannot edit controls in this view. You must use the [Controls](https://cloud.armosec.io/settings/workspace/controls) page.

You can view more information about the control by clicking the Control ID.
