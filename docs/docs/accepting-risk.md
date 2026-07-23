# Accepting risk with exceptions

!!! info "Risk acceptance support"
    Risk acceptance is available for Kubescape CLI only at this point.


Control failures cannot account for all situations.  What is acceptable in one environment may not be in another, and vice versa. Kubescape offers sensible defaults but should be configured to reflect each environment in which it runs.

**Exceptions** are the method for excluding failed resources from affecting the risk score. For example, a control may count the number of resources that have `cluster-admin` role assigned. Any number above 0 will be considered a failure. Using exceptions, you note that you have considered each resource and deemed it OK. Then, you know that if you ever see this control failure, it is something that warrants investigation.

Exceptions can be supplied in two ways: an exceptions file passed to the CLI (described below), or `SecurityException` / `ClusterSecurityException` resources stored in the cluster (described in [Accepting risk with in-cluster resources](#accepting-risk-with-in-cluster-resources)).

## Accepting risk with in-cluster resources

Exceptions can also be stored in the cluster as custom resources, instead of or alongside an exceptions file. This suits GitOps workflows, where the exceptions live in Git with the rest of your manifests. The exceptions file described in the following sections continues to work unchanged.

There are two kinds, both served at `kubescape.io/v1beta1`:

- `SecurityException` (namespaced, short name `se`) — applies within its own namespace.
- `ClusterSecurityException` (cluster-scoped, short name `cse`) — can apply across namespaces and adds a `namespaceSelector`.

When you scan a cluster, Kubescape reads these resources automatically; there is no extra flag. A single resource can hold posture exceptions, vulnerability exceptions, or both. The posture part is what affects framework and control scans, and is what this section covers.

### Example

This `SecurityException` stops `Deployment/nginx` in the `production` namespace from failing control `C-0034`:

```yaml
apiVersion: kubescape.io/v1beta1
kind: SecurityException
metadata:
  name: except-c0034-nginx
  namespace: production
spec:
  reason: "Service account mapping reviewed and accepted for nginx"
  author: "platform-team"
  posture:
    - controlID: C-0034
      action: ignore
  match:
    resources:
      - kind: Deployment
        name: nginx
```

Apply it, then scan the cluster as usual:

```sh
kubectl apply -f except-c0034-nginx.yaml
kubescape scan framework nsa --include-namespaces production
```

With the exception in place, `C-0034` on `Deployment/nginx` is reported as passed with exceptions instead of failed. Kubescape also records a Kubernetes Event on the `SecurityException` resource, which you can view with:

```sh
kubectl describe securityexception except-c0034-nginx -n production
```

### Fields

Under `spec`:

- `reason` — free-text explanation, shown in `kubectl get se`.
- `author` — free-text owner of the exception.
- `expiresAt` — optional RFC 3339 timestamp. It is checked at scan time: once it has passed, the exception is ignored and the finding is reported again. It is not enforced by the resource itself, only during a scan.
- `match` — which resources the exception applies to (see [Matching resources](#matching-resources)).
- `posture` — a list of `{ controlID, action, frameworkName }` entries. `controlID` and `action` are required; `frameworkName` optionally limits the exception to a single framework.
- `vulnerabilities` — vulnerability exceptions, handled by the in-cluster vulnerability scanner (kubevuln). They do not affect posture scans.

At least one of `posture` or `vulnerabilities` must be set.

`action` can be `ignore` or `alert_only`. In a CLI posture scan, a matched resource is reported as passed with exceptions for either value, and it is excluded from the control's failed-resource count and compliance score. The value you choose is preserved in the scan results, which is where the two currently differ.

### Matching resources

`match` supports:

- `resources` — a list of `{ kind, name, apiGroup }` entries. `kind` is required; `name` and `apiGroup` are optional.
- `objectSelector` — a standard Kubernetes label selector matched against the workload's labels.
- `namespaceSelector` — (`ClusterSecurityException` only) a label selector matched against namespace labels.

Multiple `resources` entries are combined with a logical OR — any one match is enough. If you also set an `objectSelector`, it is combined with the resource match using AND, so a workload has to satisfy both. If `match` is empty, a `SecurityException` applies to its whole namespace and a `ClusterSecurityException` applies cluster-wide.

### Precedence over the exceptions file and cloud exceptions

If the same control and resource is covered by both a file or cloud exception and an in-cluster resource, the file or cloud exception takes precedence and the overlapping in-cluster entry is skipped. Any non-overlapping parts of the in-cluster exception still apply.

### Enabling the in-cluster components

The Kubescape CLI reads these resources using whatever access your kubeconfig has. The in-cluster components (operator and kubevuln) read them only when the Helm value `capabilities.riskAcceptance` is set to `enable`; it defaults to `disable`. Enabling it also grants the access needed to resolve `objectSelector` and `namespaceSelector` labels, and lets the operator trigger a re-scan when an exception is added, changed, or removed.

For the full design, see the [SecurityException design document](https://github.com/kubescape/kubevuln/blob/main/docs/security-exception-design.md).

## Scanning with an exceptions file

Use the `--exceptions` flag when performing a scan:

```sh
kubescape scan --exceptions /path/to/exceptions.json
```

## Definitions

- `name`- Exception name - a unique name representing the exception
- `policyType`- Do not change
- `actions`- List of available actions. Currently, alertOnly is supported
- `resources`- List of resources to apply this exception on
    - `designatorType: Attributes`- An attribute-based declaration {key: value}  
    Supported keys:
    - `name`: k8s resource name (case-sensitive, regex supported)
    - `kind`: k8s resource kind (case-sensitive, regex supported)
    - `namespace`: k8s resource namespace (case-sensitive, regex supported)
    - `cluster`: k8s cluster name (usually it is the `current-context`) (case-sensitive, regex supported)
    - resource labels as key value (case-sensitive, regex NOT supported)
- `posturePolicies`- An attribute-based declaration {key: value}
    - `frameworkName` - [Framework name](https://github.com/kubescape/regolibrary/tree/master/frameworks) (regex supported)
    - `controlID` - [Control ID](https://github.com/kubescape/regolibrary/tree/master/controls) (regex supported)
    - `ruleName` - [Rule name](https://github.com/kubescape/regolibrary/tree/master/rules) (regex supported)

[The Kubescape GitHub repository contains examples of exception files](https://github.com/kubescape/kubescape/tree/master/examples/exceptions).

## Usage

The `resources` list and `posturePolicies` list are designed to be a combination of the resources and policies to exclude.

!!! note
    You must declare at least one resource and one policy.

For example, if you wish to exclude all namespaces with the label `environment: dev`, the resource list should contain:
```
"resources": [
    {
        "designatorType": "Attributes",
        "attributes": {
            "namespace": ".*",
            "environment": "dev"
        }
    }
]
```

Policies are combined with a logical *OR*. To exclude all namespaces *OR* any resource with the label `environment: dev`, the resource list should be configured:

```
"resources": [
    {
        "designatorType": "Attributes",
        "attributes": {
            "namespace": ".*"
        }
    },
    {
        "designatorType": "Attributes",
        "attributes": {
            "environment": "dev"
        }
    }
]
```

The `posturePolicies` list works in a similar fashion.  For example, if you wish to exclude the resources declared in the `resources` list that failed when scanning the `NSA` framework *AND* failed the `C-0030` control, both can be defined in the `posturePolicies` list:

```
"posturePolicies": [
    {
        "frameworkName": "NSA",
        "controlID": "C-0030" 
    }
]
```

But, if you wish to exclude the resources declared in the `resources` list that failed when scanning the `NSA` framework *OR* failed the `C-0030` control, the `posturePolicies` list should look as follows:

```
"posturePolicies": [
    {
        "frameworkName": "NSA" 
    },
    {
        "controlID": "C-0030" 
    }
]
```

## Examples

Here are some examples demonstrating the different ways the exceptions file can be configured

### Exclude control

Exclude the C-0060 control by declaring the control ID in the `posturePolicies` section.

The resources

```
[
    {
        "name": "exclude-allowed-hostPath-control",
        "policyType": "postureExceptionPolicy",
        "actions": [
            "alertOnly"
        ],
        "resources": [
            {
                "designatorType": "Attributes",
                "attributes": {
                    "kind": ".*"
                }
            }
        ],
        "posturePolicies": [
            {
                "controlID": "C-0060" 
            }
        ]
    }
]
```

### Exclude deployments in the default namespace that failed the "C-0030" control

```
[
    {
        "name": "exclude-deployments-in-ns-default",
        "policyType": "postureExceptionPolicy",
        "actions": [
            "alertOnly"
        ],
        "resources": [
            {
                "designatorType": "Attributes",
                "attributes": {
                    "namespace": "default",
                    "kind": "Deployment"
                }
            }
        ],
        "posturePolicies": [
            {
                "controlID": "C-0030" 
            }
        ]
    }
]
```

### Exclude resources with the label "app=nginx" running in a minikube cluster that failed the "NSA" or "MITRE" framework

```
[
    {
        "name": "exclude-nginx-minikube",
        "policyType": "postureExceptionPolicy",
        "actions": [
            "alertOnly"
        ],
        "resources": [
            {
                "designatorType": "Attributes",
                "attributes": {
                    "cluster": "minikube",
                    "app": "nginx"
                }
            }
        ],
        "posturePolicies": [
            {
                "frameworkName": "NSA" 
            },
            {
                "frameworkName": "MITRE" 
            }
        ]
    }
]
```

!!! info "Deprecated exceptions by control name"

    Creating exceptions by control name (`controlName` field) has been deprecated in Kubescape version `v3.0.29`<sup>[1](https://github.com/kubescape/kubescape/releases/tag/v3.0.29)</sup>
