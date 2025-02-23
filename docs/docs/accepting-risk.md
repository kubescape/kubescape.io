# Accepting risk with exceptions

!!! info "Risk acceptance support"
    Risk acceptance is available for Kubescape CLI only at this point.


Control failures cannot account for all situations.  What is acceptable in one environment may not be in another, and vice versa. Kubescape offers sensible defaults but should be configured to reflect each environment in which it runs.

**Exceptions** are the method for excluding failed resources from affecting the risk score. For example, a control may count the number of resources that have `cluster-admin` role assigned. Any number above 0 will be considered a failure. Using exceptions, you note that you have considered each resource and deemed it OK. Then, you know that if you ever see this control failure, it is something that warrants investigation.

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
