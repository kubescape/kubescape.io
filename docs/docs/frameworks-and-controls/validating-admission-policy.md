# Use Kubescape to configure a validating admission policy

## What is Validating Admission Policy?

Validating admission policies offer a declarative, in-process alternative to validating admission webhooks.

Validating admission policies use the Common Expression Language (CEL) to declare the validation rules of a policy.
Validation admission policies are highly configurable, enabling policy authors to define policies that can be
parameterized and scoped to resources as needed by cluster administrators.

## What Resources Make a Policy

A policy is generally made up of three resources:
* The `ValidatingAdmissionPolicy` describes the abstract logic of a policy
(think: "this policy makes sure a particular label is set to a particular value").
* A `ValidatingAdmissionPolicyBinding` links the above resources together and provides scoping.
If you only want to require an `owner` label to be set for `Pods`, the binding is where you would specify this restriction.
* A parameter resource provides information to a ValidatingAdmissionPolicy to make it a concrete statement
(think "the `owner` label must be set to something that ends in `.company.com`").
A native type such as ConfigMap or a CRD defines the schema of a parameter resource.
`ValidatingAdmissionPolicy` objects specify what Kind they are expecting for their parameter resource.

At least a `ValidatingAdmissionPolicy` and a corresponding `ValidatingAdmissionPolicyBinding` must be defined for
a policy to have an effect.

If a `ValidatingAdmissionPolicy` does not need to be configured via parameters, simply leave `spec.paramKind`
in `ValidatingAdmissionPolicy` not specified.

## Before you begin

* Ensure the `ValidatingAdmissionPolicy` [feature gate](https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/) is enabled.
* Ensure that the `admissionregistration.k8s.io/v1beta1` API is enabled.

## Getting Started with Validating Admission Policy

### Deploying the CEL Admission Policy Library

Downloading and deploying the CEL Admission Policy Library is a simple operation with kubescape:
```shell
kubescape vap deploy-library | kubectl apply -f -
```

You can now see all controls available in the library by running:
```shell
kubectl get ValidatingAdmissionPolicy -A
```

### Creating a Validating Admission Policy Binding

Let's now create a policy binding for the [C-0073](https://kubescape.io/docs/controls/c-0073/) control in the default namespace:
```shell
kubescape vap create-policy-binding --name my-policy-binding --policy kubescape-c-0073-deny-naked-pods --namespace default | kubectl apply -f -
```

### Testing the Validating Admission Policy

This command should be denied since the binding on [C-0073](https://kubescape.io/docs/controls/c-0073/) forbids creating naked pods in the default namespace.

```shell
kubectl run nginx --image=nginx --namespace default
The pods "nginx" is invalid: : ValidatingAdmissionPolicy 'kubescape-c-0073-deny-naked-pods' with binding 'replicalimit-binding-nontest' denied request: Pods doesn't have a parent! (see more at https://kubescape.io/docs/controls/c-0073/)
```
