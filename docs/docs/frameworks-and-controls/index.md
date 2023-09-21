# Frameworks and controls

Security researchers and professionals codify best practices in *controls*: preventative, detective or corrective measures that can be taken to avoid, or contain, a security breach.

A security *framework* is a set of guidelines, best practices, or standards, usually codified as a number of controls. Security frameworks are often published by government agencies or non-profit research centers. 

Kubescape comes with hundreds of controls that can be used in either [provided or custom](frameworks.md) frameworks. The controls are tests that look at a certain aspect of your security posture. Kubescape can examine:

- **Kubernetes object configuration**: any YAML file, any Helm chart, or any resource that the API server exposes.
- **API server settings**: configuration of the Kubernetes API server.
- **Worker nodes**: the configuration of the Kubernetes worker nodes, including `kubelet` configuration and host settings.
- **Container image**: the results from image scanning, to give you high-level visibility into items that need your attention.

Kubescape's controls are written in the [Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) language, and evaluated using the [Open Policy Agent](https://www.openpolicyagent.org/).

The controls, and their grouping into frameworks, are maintained in the Kubescape [regolibrary](https://github.com/kubescape/regolibrary) repository.

## Next steps

* [Read about the supported frameworks](frameworks.md)
* [Create your own framework](frameworks.md#custom-frameworks)
* [Learn about downloading artifacts for offline usage](../install-cli.md#offlineair-gapped-environment-support)