---
hide:
  - navigation
  - toc
---

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cncf/artwork/master/projects/kubescape/stacked/white/kubescape-stacked-white.svg" width="300">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/cncf/artwork/master/projects/kubescape/stacked/color/kubescape-stacked-color.svg" width="300">
  <img alt="Kubescape logo" src="https://raw.githubusercontent.com/cncf/artwork/master/projects/kubescape/stacked/color/kubescape-stacked-color.svg" width="300">
</picture>

_Comprehensive Kubernetes Security from Development to Runtime_

Kubescape is an open-source Kubernetes security platform that provides comprehensive security coverage, from left to right across the entire development and deployment lifecycle. It offers hardening, posture management, and runtime security capabilities to ensure robust protection for Kubernetes environments.

_Key features of Kubescape include_

* **Shift-left security**: Kubescape enables developers to scan for misconfigurations as early as the manifest file submission stage, promoting a proactive approach to security.
* **Runtime security**: Kubescape extends its protection to the runtime environment, providing continuous monitoring and threat detection for deployed applications and runtime context to posture management.
* **IDE and CI/CD integration**: The tool integrates seamlessly with popular IDEs like VSCode and Lens, as well as CI/CD platforms such as GitHub and GitLab, allowing for security checks throughout the development process.
* **Cluster scanning**: Kubescape can scan active Kubernetes clusters for vulnerabilities, misconfigurations, and security issues.
* **Multi-framework compliance support**: Kubescape can test against many security frameworks, including NSA-CISA Kubernetes Hardening Guidance, MITRE ATT&CK , SOC 2, CIS Benchmarks and more. Thus, simplifying compliance efforts and protetcing from configuration drift. 
* **YAML and Helm chart validation**: The tool checks YAML files and Helm charts for correct configuration according to the frameworks above, without requiring an active cluster.
* **Kubernetes hardening**: Kubescape ensures proactive identification and rapid remediation of misconfigurations and vulnerabilities through manual, recurring, or event-triggered scans.
* **Multi-cloud support**: Kubescape offers frictionless security across various cloud providers and Kubernetes distributions.

By providing this comprehensive security coverage from development to runtime, Kubescape enables organizations to ensure a robust security posture throughout their Kubernetes deployment, addressing potential vulnerabilities and threats at every stage of the application lifecycle.

Kubescape was created by [ARMO](https://www.armosec.io/?utm_source=github&utm_medium=repository) and is a [Cloud Native Computing Foundation (CNCF) sandbox project](https://www.cncf.io/sandbox-projects/).

## Demo
<img src="https://github.com/kubescape/kubescape/raw/master/docs/img/demo.gif" alt="demo">

_Please [star ⭐](https://github.com/kubescape/kubescape/stargazers) the repo if you want us to continue developing and improving Kubescape! 😀_

## Getting started

Experimenting with Kubescape is as easy as:

``` sh
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
```

Learn more about:

* [Installing Kubescape](https://github.com/kubescape/kubescape/blob/master/docs/getting-started.md#install-kubescape)
* [Running your first scan](https://github.com/kubescape/kubescape/blob/master/docs/getting-started.md#run-your-first-scan)
* [Usage](https://github.com/kubescape/kubescape/blob/master/docs/getting-started.md#examples)
* [Architecture](https://github.com/kubescape/kubescape/blob/master/docs/architecture.md)
* [Building Kubescape from source](https://github.com/kubescape/kubescape/blob/master/docs/building.md)

_Did you know you can use Kubescape in all these places?_

<div>
    <img src="https://github.com/kubescape/kubescape/raw/master/docs/img/ksfromcodetodeploy.png" alt="Places you can use Kubescape: in your IDE, CI, CD, or against a running cluster.">
</div>

## Under the hood

Kubescape uses [Open Policy Agent](https://github.com/open-policy-agent/opa) to verify Kubernetes objects against [a library of posture controls](https://github.com/kubescape/regolibrary).  
For image scanning, it uses [Grype](https://github.com/anchore/grype).  
For image patching, it uses [Copacetic](https://github.com/project-copacetic/copacetic).
For eBPF, it uses [Inspektor Gadet](https://github.com/inspektor-gadget)

By default, the results are printed in a console-friendly manner, but they can be:

* exported to JSON or junit XML
* rendered to HTML or PDF
* submitted to a [cloud service](https://github.com/kubescape/kubescape/blob/master/docs/providers.md)

It retrieves Kubernetes objects from the API server and runs a set of [Rego snippets](https://www.openpolicyagent.org/docs/latest/policy-language/) developed by [ARMO](https://www.armosec.io/?utm_source=kubescape.io&utm_medium=website).

## Community

Kubescape is an open source project. We welcome your feedback and ideas for improvement. We are part of the CNCF community and are evolving Kubescape in sync with the security needs of Kubernetes users. To learn more about where Kubescape is heading, please check out our [ROADMAP](https://github.com/kubescape/project-governance/blob/main/ROADMAP.md).

If you feel inspired to contribute to Kubescape, check out our [CONTRIBUTING](https://github.com/kubescape/project-governance/blob/main/CONTRIBUTING.md) file to learn how. You can find the issues we are working on (triage to development) on the [Kubescaping board](https://github.com/orgs/kubescape/projects/4/views/1)

* Feel free to pick a task from the [board](https://github.com/orgs/kubescape/projects/4) or suggest a feature of your own.
* Open an issueon the board. We aim to respond to all issues within 48 hours.
* [Join the CNCF Slack](https://slack.cncf.io/) and then our [users](https://cloud-native.slack.com/archives/C04EY3ZF9GE) or [developers](https://cloud-native.slack.com/archives/C04GY6H082K) channel.

The Kubescape project follows the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md).

For more information about the Kubescape community, please visit [COMMUNITY](https://github.com/kubescape/project-governance/blob/main/COMMUNITY.md).

We would like to take this opportunity to thank all our contibutors to date.

<br>

<div style="text-align: center">
<a href = "https://github.com/kubescape/kubescape/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=kubescape/kubescape" alt="kubescape contributors"/>
</a>
</div>

## License

Copyright 2021-2024, the Kubescape Authors. All rights reserved. Kubescape is released under the Apache 2.0 license. See the [LICENSE](https://github.com/kubescape/project-governance/blob/main/LICENSE) file for details.

Kubescape is a [Cloud Native Computing Foundation (CNCF) sandbox project](https://www.cncf.io/sandbox-projects/) and was contributed by [ARMO](https://www.armosec.io/?utm_source=kubescape.io&utm_medium=website).

Kubescape is a [trademark](https://www.linuxfoundation.org/legal/trademark-usage) owned by the [Linux Foundation](https://www.linuxfoundation.org/)

<div>
    <img src="https://raw.githubusercontent.com/cncf/artwork/master/other/cncf-sandbox/horizontal/color/cncf-sandbox-horizontal-color.svg" width="300" alt="CNCF Sandbox Project">
</div>
