---
date: 2024-08-04
categories:
  - Project
authors:
  - oshratn
slug: 'cel-and-kubescape'
---
# CEL and Kubescape: Transforming Kubernetes Admission Control

## Introduction
Admission control is a crucial part of the Kubernetes security, enabling the approval or modification of API objects as they are submitted to the server. It allows administrators to enforce business logic or policies on what objects can be admitted into a cluster. Kubernetes RBAC is a scalable authorization mechanism, but lacks the fine grained control over different Kubernetes objects. This creates the need for another layer of control which is Admission Policies. To enhance this capability, Kubernetes introduced dynamic admission control webhooks in version 1.7. Despite its benefits, adoption of admission controllers for policy enforcement faces challenges, namely scalability challenges. Maintaining webhook infrastructure as a production service is complex, and handling webhook failures can either reduce cluster availability or undermine policy enforcement. Additionally, the network hop and evaluation time involved in admission control can introduce significant latency, particularly in "serverless” environments where pods are rapidly spun up in response to network requests.
Kubernetes 1.30 has brought a significant development to the table with the introduction of the Common Expression Language (CEL) for admission control. This new feature offers an alternative to validating admission webhooks for enforcing custom policies, with a focus on policy enforcement capabilities and CRD validation rules that were previously in beta.
The introduction of CEL for admission control enables administrators to define complex and tailored policies, improving the overall security of Kubernetes clusters. This is significant for organizations with complex security requirements, as it allows them to create finely tuned policies that precisely match the security needs of different applications and environments.
In this blog post, we'll explore the benefits of Validating Admission Policies, its goals, and how Kubescape maintainers have leveraged it to create a robust and precise cel-admission-library.

## Validating Admission Policies Short Primer
The first part of this blog post explains what ValidatingAdmissionPolicies are and explain why they were added and their benefits. If you have been following the development of KEP-3488, through alpha in Kubernetes 1.26, beta in Kubernetes 1.28 and GA in the aforementioned Kubernetes 1.30 and you just want to get started with them, feel free to skip to [Using the Kubescape CEL library in your cluster](#using-the-kubescape-cel-library-in-your-cluster).
If you are reading this and thinking: “I already have OPA Gatekeeper or Kyverno up and running to solve this”.

<figure markdown>
  ![Admission control meme](/assets/admission-meme.jpg){ width="600" }
</figure>

Please join us to get a better understanding of this Kubernetes native feature, what it seeks to achieve and what the benefits of using it are. Also, take into account that this functionality will become the de-facto standard, similar to what happened with OpenTelemetry and GatewayAPI.

### Introduction to ValidatingAdmissionPolicies
ValidatingAdmissionPolicies are: A declarative, in-process alternative to validating admission webhooks. They use the Common Expression Language (CEL) to define the policies.

They consist of two main resources:

* ValidatingAdmissionPolicy describes the policy logic
* ValidatingAdmissionPolicyBinding links the above policy to the resources it applies to

### The Goals of Validating Admission Policies
The Kubernetes team has established specific goals for Validating Admission Policies to guarantee that it aligns with the community's requirements.:

1. **Alternative to Webhooks**: Validating Admission Policies aims to provide an alternative to webhooks for the majority of validating admission use cases.
2. **In-Tree Extensions**: The feature intends to offer the in-tree extensions required to build policy frameworks for Kubernetes without relying on webhooks.
3. **Efficient Type Checking**: Validating Admission Policies aims to make good use of CEL type checking, even when considering that CRD schemas can be changed at any time, and not all fields of built-in types exist in older Kubernetes versions.
4. **Polyfill Implementati****on**: The Kubernetes organization plans to provide a polyfill implementation that offers enhancement functionality to Kubernetes versions where this feature is not available.
5. **Core Functionality as a Library**: Validating Admission Policies intends to provide core functionality as a library, enabling use cases like GitOps, CI/CD pipelines, and auditing to run the same CEL validation checks as the API server.
Having said that, Polyfill Implementation and Core Functionality as a Library (points 4 and 5 above) have yet to be implemented, and we should keep an eye out for them in the future.

### The Benefits of Validating Admission Policies
The Validating Admission Policies functionality offers several advantages over webhooks, making it a more attractive choice for policy enforcement:

1. **No Infrastructure Requirement**: Validating Admission Policies doesn't require you to build infrastructure to host the admission webhook, simplifying the process.
2. **Reduced Latency**: By eliminating the need for an additional network hop, Validating Admission Policies helps reduce latency, ensuring smoother and faster operations.
3. **Increased Reliability and Scalability**: In-process webhooks used by Validating Admission Policies are less prone to failure than webhooks with extra infrastructure dependencies, enhancing the overall reliability. Beyond this, the in-process admission decision makes the Kubernetes control plane more scaleable since it doesn't depend on an external component.
4. **Lower Operational Burden**: Cluster administrators responsible for the observability, security, and release/rollout/rollback plans for webhooks will experience a lower operational burden with Validating Admission Policies.

## Kubescape's Cel-Admission-Library
When Validating Admission Policies was first introduced in beta in version 1.26, the maintainers of Kubescape were eager to utilize it. They created the [cel-admission-library](https://github.com/kubescape/cel-admission-library) based on Kubescape controls originally written in Rego. The library includes the following 27 admission controls:

| Control ID | Name | Policy name | Configuration parameter |
| --- | --- | --- | --- |
| [C-0001](https://hub.armosec.io/docs/c-0001) | Forbidden Container Registries | [kubescape-c-0001-deny-forbidden-container-registries](/docs/policies-based-on-kubescape-controls/kubescape-c-0001-deny-forbidden-container-registries.md) | [untrustedRegistries](https://hub.armosec.io/docs/configuration_parameter_untrustedregistries) |
| [C-0004](https://hub.armosec.io/docs/c-0004) | Resources memory limit and request | [kubescape-c-0004-deny-resources-with-memory-limit-or-request-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0004-deny-resources-with-memory-limit-or-request-not-set.md) | [memoryRequestMin](https://hub.armosec.io/docs/configuration_parameter_memoryrequestmin) |
| [C-0009](https://hub.armosec.io/docs/c-0009) | Resource limits | [kubescape-c-0009-deny-resources-with-memory-or-cpu-limit-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0009-deny-resources-with-memory-or-cpu-limit-not-set.md) | not configurable |
| [C-0016](https://hub.armosec.io/docs/c-0016) | Allow privilege escalation | [kubescape-c-0016-allow-privilege-escalation](/docs/policies-based-on-kubescape-controls/kubescape-c-0016-allow-privilege-escalation.md) | not configurable |
| [C-0017](https://hub.armosec.io/docs/c-0017) | Immutable container filesystem | [kubescape-c-0017-deny-resources-with-mutable-container-filesystem](/docs/policies-based-on-kubescape-controls/kubescape-c-0017-deny-resources-with-mutable-container-filesystem.md) | not configurable |
| [C-0018](https://hub.armosec.io/docs/c-0018) | Configured readiness probe | [kubescape-c-0018-deny-resources-without-configured-readiness-probes](/docs/policies-based-on-kubescape-controls/kubescape-c-0018-deny-resources-without-configured-readiness-probes.md) | not configurable |
| [C-0020](https://hub.armosec.io/docs/c-0020) | Mount service principal | [kubescape-c-0020-deny-resources-having-volumes-with-potential-access-to-known-cloud-credentials](/docs/policies-based-on-kubescape-controls/kubescape-c-0020-deny-resources-having-volumes-with-potential-access-to-known-cloud-credentials.md) | [cloudProvider](https://hub.armosec.io/docs/configuration_parameter_cloudprovider) |
| [C-0034](https://hub.armosec.io/docs/c-0034) | Automatic mapping of service account | [kubescape-c-0034-deny-resources-with-automount-service-account-token-enabled](/docs/policies-based-on-kubescape-controls/kubescape-c-0034-deny-resources-with-automount-service-account-token-enabled.md) | not configurable |
| [C-0038](https://hub.armosec.io/docs/c-0038) | Host PID/IPC privileges | [kubescape-c-0038-deny-resources-with-host-ipc-or-pid-privileges](/docs/policies-based-on-kubescape-controls/kubescape-c-0038-deny-resources-with-host-ipc-or-pid-privileges.md) | not configurable |
| [C-0041](https://hub.armosec.io/docs/c-0041) | HostNetwork access | [kubescape-c-0041-deny-resources-with-host-network-access](/docs/policies-based-on-kubescape-controls/kubescape-c-0041-deny-resources-with-host-network-access.md) | not configurable |
| [C-0042](https://hub.armosec.io/docs/c-0042) | SSH server running inside container | [kubescape-c-0042-deny-resources-with-ssh-server-running](/docs/policies-based-on-kubescape-controls/kubescape-c-0042-deny-resources-with-ssh-server-running.md) | not configurable |
| [C-0044](https://hub.armosec.io/docs/c-0044) | Container hostPort | [kubescape-c-0044-deny-resources-with-host-port](/docs/policies-based-on-kubescape-controls/kubescape-c-0044-deny-resources-with-host-port.md) | not configurable |
| [C-0045](https://hub.armosec.io/docs/c-0045) | Writable hostPath mount | [kubescape-c-0045-deny-workloads-with-hostpath-volumes-readonly-not-false](/docs/policies-based-on-kubescape-controls/kubescape-c-0045-deny-workloads-with-hostpath-volumes-readonly-not-false.md) | not configurable |
| [C-0046](https://hub.armosec.io/docs/c-0046) | Insecure capabilities | [kubescape-c-0046-deny-resources-with-insecure-capabilities](/docs/policies-based-on-kubescape-controls/kubescape-c-0046-deny-resources-with-insecure-capabilities.md) | [insecureCapabilities](https://hub.armosec.io/docs/configuration_parameter_insecurecapabilities) |
| [C-0048](https://hub.armosec.io/docs/c-0048) | HostPath mount | [kubescape-c-0048-deny-workloads-with-hostpath-mounts](/docs/policies-based-on-kubescape-controls/kubescape-c-0048-deny-workloads-with-hostpath-mounts.md) | not configurable |
| [C-0050](https://hub.armosec.io/docs/c-0050) | Resources CPU limit and request | [kubescape-c-0050-deny-resources-with-cpu-limit-or-request-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0050-deny-resources-with-cpu-limit-or-request-not-set.md) | [cpuLimitMin](https://hub.armosec.io/docs/configuration_parameter_cpulimitmin) |
| [C-0055](https://hub.armosec.io/docs/c-0055) | Linux hardening | [kubescape-c-0055-linux-hardening](/docs/policies-based-on-kubescape-controls/kubescape-c-0055-linux-hardening.md) | not configurable |
| [C-0056](https://hub.armosec.io/docs/c-0056) | Configured liveness probe | [kubescape-c-0056-deny-resources-without-configured-liveliness-probes](/docs/policies-based-on-kubescape-controls/kubescape-c-0056-deny-resources-without-configured-liveliness-probes.md) | not configurable |
| [C-0057](https://hub.armosec.io/docs/c-0057) | Privileged container | [kubescape-c-0057-privileged-container-denied](/docs/policies-based-on-kubescape-controls/kubescape-c-0057-privileged-container-denied.md) | not configurable |
| [C-0061](https://hub.armosec.io/docs/c-0061) | Pods in default namespace | [kubescape-c-0061-deny-workloads-in-default-namespace](/docs/policies-based-on-kubescape-controls/kubescape-c-0061-deny-workloads-in-default-namespace.md) | not configurable |
| [C-0062](https://hub.armosec.io/docs/c-0062) | Sudo in container entrypoint | [kubescape-c-0062-deny-resources-having-containers-with-sudo-in-entrypoint](/docs/policies-based-on-kubescape-controls/kubescape-c-0062-deny-resources-having-containers-with-sudo-in-entrypoint.md) | not configurable |
| [C-0073](https://hub.armosec.io/docs/c-0073) | Naked PODs | [kubescape-c-0073-deny-naked-pods](/docs/policies-based-on-kubescape-controls/kubescape-c-0073-deny-naked-pods.md) | not configurable |
| [C-0074](https://hub.armosec.io/docs/c-0074) | Containers mounting Docker socket | [kubescape-c-0074-resources-mounting-docker-socket-denied](/docs/policies-based-on-kubescape-controls/kubescape-c-0074-resources-mounting-docker-socket-denied.md) | not configurable |
| [C-0075](https://hub.armosec.io/docs/c-0075) | Image pull policy on latest tag | [kubescape-c-0075-deny-resources-with-image-pull-policy-not-set-to-always-for-latest-tag](/docs/policies-based-on-kubescape-controls/kubescape-c-0075-deny-resources-with-image-pull-policy-not-set-to-always-for-latest-tag.md) | not configurable |
| [C-0076](https://hub.armosec.io/docs/c-0076) | Label usage for resources | [kubescape-c-0076-deny-resources-without-configured-list-of-labels-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0076-deny-resources-without-configured-list-of-labels-not-set.md) | [recommendedLabels](https://hub.armosec.io/docs/configuration_parameter_recommendedlabels) |
| [C-0077](https://hub.armosec.io/docs/c-0077) | K8s common labels usage | [kubescape-c-0077-deny-resources-without-configured-list-of-k8s-common-labels-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0077-deny-resources-without-configured-list-of-k8s-common-labels-not-set.md) | [k8sRecommendedLabels](https://hub.armosec.io/docs/configuration_parameter_k8srecommendedlabels) |
| [C-0078](https://hub.armosec.io/docs/c-0078) | Images from allowed registry | [kubescape-c-0078-only-allow-images-from-allowed-registry](/docs/policies-based-on-kubescape-controls/kubescape-c-0078-only-allow-images-from-allowed-registry.md) | [imageRepositoryAllowList](https://hub.armosec.io/docs/configuration_parameter_imagerepositoryallowlist) |
[source](https://github.com/kubescape/cel-admission-library/edit/main/README.md)

## Using the Kubescape CEL library in your cluster
This section originally appeared in [Kubernetes Validating Admission Policies: A Practical Example](https://kubernetes.io/blog/2023/03/30/kubescape-validating-admission-policy-library/#using-the-cel-library-in-your-cluster) on the Kubernetes blog.
Policies are provided as Kubernetes objects, which are then bound to certain resources by a [selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors).
[Minikube](https://minikube.sigs.k8s.io/docs/) is a quick and easy way to install and configure a Kubernetes cluster for testing. To install Kubernetes v1.26 with the ValidatingAdmissionPolicy [feature gate](https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/) enabled:
```bash minikube start --kubernetes-version=1.30.2 --extra-config=apiserver.runtime-config=admissionregistration.k8s.io/v1alpha1  --feature-gates='ValidatingAdmissionPolicy=true'```

To install the policies in your cluster:
```bash
# Install configuration CRD
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/policy-configuration-definition.yaml

# Install basic configuration
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/basic-control-configuration.yaml

# Install policies
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/kubescape-validating-admission-policies.yaml
```

To apply policies to objects, create a ValidatingAdmissionPolicyBinding resource. Let’s apply the above Kubescape C-0017 control to any namespace with the label policy=enforced:
```bash
# Create a binding
kubectl apply -f - <<EOT
apiVersion: admissionregistration.k8s.io/v1alpha1
kind: ValidatingAdmissionPolicyBinding
metadata:
 name: c0017-binding
spec:
 policyName: kubescape-c-0017-deny-mutable-container-filesystem
 matchResources:
   namespaceSelector:
     matchLabels:
       policy: enforced
EOT

# Create a namespace for running the example
kubectl create namespace policy-example
kubectl label namespace policy-example 'policy=enforced'
```

Now, if you attempt to create an object without specifying a readOnlyRootFilesystem, it will not be created.
```bash
# The next line should fail
kubectl -n policy-example run nginx --image=nginx --restart=Never
```

The output shows our error:
```bash The pods "nginx" is invalid: : ValidatingAdmissionPolicy 'kubescape-c-0017-deny-mutable-container-filesystem' with binding 'c0017-binding' denied request: Pods having containers with mutable filesystem not allowed! (see more at https://hub.armosec.io/docs/c-0017)```

## Configuration
Policy objects can include configuration, which is provided in a different object. Many of the Kubescape controls require a configuration: which labels to require, which capabilities to allow or deny, which registries to allow containers to be deployed from, etc. Default values for those controls are defined in [the ControlConfiguration object](https://github.com/kubescape/cel-admission-library/blob/main/configuration/basic-control-configuration.yaml).
To use this configuration object, or your own object in the same format, add a paramRef.name value to your binding object:
```bash
apiVersion: admissionregistration.k8s.io/v1alpha1
kind: ValidatingAdmissionPolicyBinding
metadata:
 name: c0001-binding
spec:
 policyName: kubescape-c-0001-deny-forbidden-container-registries
 paramRef:
   name: basic-control-configuration
 matchResources:
   namespaceSelector:
     matchLabels:
       policy: enforced
```

## Conclusion
The introduction of Validating Admission Policies in Kubernetes 1.30 is a game-changer, offering a more efficient and reliable way to enforce custom policies. With its numerous benefits and well-defined goals, Validating Admission Policies is set to make a significant impact on the Kubernetes landscape. The cel-admission-library created by Kubescape maintainers is a testament to the potential of this new feature, and we encourage you to try it out using Kubescape.
We are happy to contribute this library to the Kubernetes community and will continue to develop it for Kubescape and Kubernetes users alike. We hope it becomes useful, either as something you use yourself, or as examples for you to write your own policies.
As for the validating admission policy feature itself, we are very excited to see this native functionality generally available on Kubernetes.


