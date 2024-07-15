# Control configuration parameters

While most of the [controls](../controls/index.md) look for specific parameters and their values, which are predefined and determined by Kubernetes, some of the controls look for certain values which change from cluster to cluster or from one environment to another. We recommend that you adjust these controls to your specific use case, as the default settings can lead to false positive results.

If a control supports configuration, the parameters will be listed on its page in the [control library](../controls/index.md).

## Changing the default values

### Downloading your control configuration

If you are connected to a [provider](../providers.md), you can download the control configuration file associated with your account ID. All other users will receive the [default control configuration from GitHub](https://github.com/kubescape/regolibrary/blob/master/default-config-inputs.json).

```sh
kubescape download controls-inputs
```

The file will be saved as `~/.kubescape/controls-inputs.json`. You can configure a different download location with the `-o` flag.

Edit this file to define configuration parameters for Kubescape scans.

### Overriding the custom control file

Kubescape's `scan` command supports a `--controls-config` flag, which allows you to use your custom control configuration.

## Configuration parameter reference

### cpu_limit_max

Used for controls that test that [CPU resource `limit` values](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) are set and under a defined maximum value.

* Default value: none

### cpu_limit_min

Used for controls that test that [CPU resource `limit` values](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) are set and above a defined minimum value.

* Default value: 0

### cpu_request_max

Used for controls that test that [CPU resource `request` values](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) are set and under a defined maximum value.

* Default value: none

### cpu_request_min

Used for controls that test that [CPU resource `request` values](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) are set and above a defined minimum value.

* Default value: 0

### imageRepositoryAllowList

Kubescape checks that containers are using images from the allowed container registries configured in this list.

* Default values: none

### insecureCapabilities

Kubescape looks for the following [capabilities](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#set-capabilities-for-a-container) in containers, which might lead to attackers getting elevated privileges in your cluster.

Default values:

* `SETPCAP`
* `NET_ADMIN`
* `NET_RAW`
* `SYS_MODULE`
* `SYS_RAWIO`
* `SYS_PTRACE`
* `SYS_ADMIN`
* `SYS_BOOT`
* `MAC_OVERRIDE`
* `MAC_ADMIN`
* `PERFMON`
* `ALL`
* `BPF`

You can see the full list of capabilities in [the capabilities(7) manual page](https://man7.org/linux/man-pages/man7/capabilities.7.html).

### k8sRecommendedLabels

Kubescape checks that workloads have at least one of the following [Kubernetes recommended labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/).

Default values:

* `app.kubernetes.io/name`
* `app.kubernetes.io/instance`
* `app.kubernetes.io/version`
* `app.kubernetes.io/component`
* `app.kubernetes.io/part-of`
* `app.kubernetes.io/managed-by`
* `app.kubernetes.io/created-by`

### listOfDangerousArtifacts

Kubescape checks if container images contain any of a list of files.  The default values are shell executables.

Default values:

* `bin/bash`
* `sbin/sh`
* `bin/ksh`
* `bin/tcsh`
* `bin/zsh`
* `usr/bin/scsh`
* `bin/csh`
* `bin/busybox`
* `usr/bin/busybox`

### max_critical_vulnerabilities

The maximum number of `Critical` severity vulnerabilities to allow.

* Default value: 5

### max_high_vulnerabilities

The maximum number of `High` severity vulnerabilities to allow.

* Default value: 10

### memory_limit_max

Used for controls that test that [memory resource `limit` values](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) are set and under a defined maximum value.

* Default value: none

### memory_limit_min

Used for controls that test that [memory resource `limit` values](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) are set and above a defined minimum value.

* Default value: 0

### memory_request_max

Used for controls that test that [memory resource `request` values](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) are set and under a defined maximum value.

* Default value: none

### memory_request_min

Used for controls that test that [memory resource `request` values](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) are set and above a defined minimum value.

* Default value: 0

### publicRegistries

Kubescape checks that none of these public container registries are in use.

* Default values: none

### recommendedLabels

Kubescape checks that workloads have at least one label that identifies semantic attributes.

Default values:

* `app`
* `tier`
* `phase`
* `version`
* `owner`
* `env`

### sensitiveInterfaces

Some popular cluster management services were not intended to be exposed to the internet, and therefore don’t require authentication by default. Kubescape checks if any of the items on this list are externally exposed.

Default values:

* `nifi`
* `argo-server`
* `weave-scope-app`
* `kubeflow`
* `kubernetes-dashboard`
* `jenkins`
* `prometheus-deployment`

### sensitiveKeyNames

Certain key names identify a potential value that should be stored in a `Secret`, and not in a `ConfigMap` or an environment variable.

Default values:

* `aws_access_key_id'`
* `aws_secret_access_key'`
* `azure_batchai_storage_account'`
* `azure_batchai_storage_key'`
* `azure_batch_account'`
* `azure_batch_key'`
* `secret'`
* `key'`
* `password'`
* `pwd'`
* `token'`
* `jwt'`
* `bearer'`
* `credential'`

### sensitiveValues

Certain strings identify a value that should be stored in a `Secret`, and not in a `ConfigMap` or an environment variable.

If you want to override these values, you can add them explicitly in the `sensitiveValuesAllowed` parameter.

Default values:

* `BEGIN \w+ PRIVATE KEY`
* `PRIVATE KEY`
* `eyJhbGciO`
* `JWT`
* `Bearer`
* `_key_`
* `_secret_`

### sensitiveValuesAllowed

Allowed values, which will override `sensitiveValues`.

* Default values: `AllowedValue`

### servicesNames

Some popular cluster management services were not intended to be exposed to the internet, and therefore don’t require authentication by default. Kubescape checks for services that match the common service names used by these applications.

Default values:

* `nifi-service`
* `argo-server`
* `minio`
* `postgres`
* `workflow-controller-metrics`
* `weave-scope-app`
* `kubernetes-dashboard`

### trustedCosignPublicKeys

Trusted [cosign](https://github.com/sigstore/cosign) public keys that are used for validating container image signatures.

* Default values: none

### untrustedRegistries

You can define container registries that should be considered untrusted, and Kubescape will report if any are in use.

* Default values: none
