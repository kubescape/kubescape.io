# Node Agent Rule Library

Kubescape runtime threat detection can load CEL-based rules from the `Rules` custom resource (`apiVersion: kubescape.io/v1`, resource name `rules.kubescape.io`). When you install the operator with `--set alertCRD.installDefault=true`, the Helm chart creates a `default-rules` object from [`charts/kubescape-operator/templates/node-agent/default-rules.yaml`](https://github.com/kubescape/helm-charts/blob/main/charts/kubescape-operator/templates/node-agent/default-rules.yaml).

The authoring source for these rules lives in [`kubescape/rulelibrary`](https://github.com/kubescape/rulelibrary). Each rule lives under `pkg/rules/r####-descriptive-name/`, and `./gen.sh` generates the combined [`rules-crd.yaml`](https://github.com/kubescape/rulelibrary/blob/main/rules-crd.yaml) artifact.

!!! note
    Treat the Helm chart template as the release snapshot and `kubescape/rulelibrary` as the authoring source. For cluster-specific changes, create your own `Rules` object instead of editing the chart template in place.

## Rule families

Kubescape currently ships two broad rule families:

- `R0xxx`: profile-driven anomaly rules that compare runtime activity to learned behavior.
- `R1xxx`: signature and behavioral rules that look for explicit suspicious activity.

The `profileDependency` field controls how much profile data a rule needs:

| Value | Meaning |
| --- | --- |
| `0` | A profile is required. |
| `1` | A profile is optional. |
| `2` | A profile is not required. |

If you need a refresher on the learning phase and application profiles, see [Runtime Threat Detection](runtime-threat-detection.md).

## Default rules

In the current Helm chart template, the default rule library contains 26 rules: 22 enabled by default and 4 disabled by default (`R0002`, `R0011`, `R1003`, and `R1011`).

### Profile-driven anomaly rules

| ID | Default | Event type | Rule | What it detects |
| --- | --- | --- | --- | --- |
| `R0001` | On | `exec` | Unexpected process launched | Detects unexpected process launches that are not in the baseline. |
| `R0002` | Off | `open` | Files Access Anomalies in container | Detects unexpected file access that is not in the baseline. |
| `R0003` | On | `syscall` | Syscalls Anomalies in container | Detects unexpected system calls that are not whitelisted by the application profile. |
| `R0004` | On | `capabilities` | Linux Capabilities Anomalies in container | Detects unexpected capabilities that are not whitelisted by the application profile. |
| `R0005` | On | `dns` | DNS Anomalies in container | Detects unexpected domain requests that are not whitelisted by the learned profile. |
| `R0006` | On | `open` | Unexpected service account token access | Detects unexpected access to service account tokens. |
| `R0007` | On | `exec`, `network` | Workload uses Kubernetes API unexpectedly | Detects unplanned `kubectl` execution or traffic to the Kubernetes API server. |
| `R0008` | On | `open` | Read Environment Variables from procfs | Detects reading environment variables from procfs. |
| `R0009` | On | `bpf` | eBPF Program Load | Detects eBPF program load operations. |
| `R0010` | On | `open` | Unexpected Sensitive File Access | Detects unexpected access to sensitive files. |
| `R0011` | Off | `network` | Unexpected Egress Network Traffic | Detects unexpected outbound traffic that is not whitelisted by the learned profile. |

### Signature and behavioral rules

| ID | Default | Event type | Rule | What it detects |
| --- | --- | --- | --- | --- |
| `R1000` | On | `exec` | Process executed from malicious source | Detects execution from suspicious locations such as shared memory mounts. |
| `R1001` | On | `exec` | Drifted process executed | Detects execution of binaries that are not part of the base image. |
| `R1002` | On | `kmod` | Process tries to load a kernel module | Detects kernel module load attempts. |
| `R1003` | Off | `ssh` | Disallowed ssh connection | Detects SSH connections to disallowed ports. |
| `R1004` | On | `exec` | Process executed from mount | Detects execution from mounted paths. |
| `R1005` | On | `exec` | Fileless execution detected | Detects fileless execution techniques. |
| `R1006` | On | `unshare` | Process tries to escape container | Detects `unshare` usage that can be used for container escape. |
| `R1007` | On | `randomx` | Crypto miner launched | Detects XMRig-style cryptomining activity. |
| `R1008` | On | `dns` | Crypto Mining Domain Communication | Detects DNS communication with known cryptomining domains. |
| `R1009` | On | `network` | Crypto Mining Related Port Communication | Detects network traffic on suspicious cryptomining ports. |
| `R1010` | On | `symlink` | Soft link created over sensitive file | Detects symlink creation over sensitive files. |
| `R1011` | Off | `exec`, `open` | ld_preload hooks technique detected | Detects `LD_PRELOAD`-based hook techniques. |
| `R1012` | On | `hardlink` | Hard link created over sensitive file | Detects hardlink creation over sensitive files. |
| `R1015` | On | `ptrace` | Malicious Ptrace Usage | Detects potentially malicious `ptrace` usage. |
| `R1030` | On | `iouring` | Unexpected io_uring Operation Detected | Detects `io_uring` activity that was not observed during the learning period. |

For the full rule definitions, including severities, MITRE mappings, tags, and trigger settings, see:

- [`default-rules.yaml`](https://github.com/kubescape/helm-charts/blob/main/charts/kubescape-operator/templates/node-agent/default-rules.yaml)
- [`rules-crd.yaml`](https://github.com/kubescape/rulelibrary/blob/main/rules-crd.yaml)

## CEL helpers and built-in functions

Kubescape rule expressions use standard CEL syntax plus several helper namespaces that the node-agent registers at runtime. For the base CEL operators, macros, and standard definitions, see the [CEL language definition](https://github.com/google/cel-spec/blob/master/doc/langdef.md#list-of-standard-definitions).

Kubescape also injects:

- `event`: the current runtime event object
- `eventType`: the current event type string, such as `exec` or `network`
- `http`: an alias to `event` for HTTP events

The implementation for the helper namespaces lives in the [`node-agent` CEL libraries directory](https://github.com/kubescape/node-agent/tree/main/pkg/rulemanager/cel/libraries). The current `ap.*` and `nn.*` helpers are:

### Application profile helpers (`ap.*`)

These helpers query learned workload behavior from the runtime profile cache. If the profile is not available yet, the helper resolves to `false` so rule evaluation can continue.

| Function | What it checks |
| --- | --- |
| `ap.was_executed(containerId, path)` | Whether the executable path was previously observed or declared in the Pod spec command/hooks. |
| `ap.was_executed_with_args(containerId, path, args)` | Whether the executable path and full argument list were previously observed. |
| `ap.was_path_opened(containerId, path)` | Whether the path was previously opened by the container. |
| `ap.was_path_opened_with_flags(containerId, path, flags)` | Whether the path was previously opened with the same open flags. |
| `ap.was_path_opened_with_suffix(containerId, suffix)` | Whether a previously opened path ends with the given suffix. |
| `ap.was_path_opened_with_prefix(containerId, prefix)` | Whether a previously opened path starts with the given prefix. |
| `ap.was_syscall_used(containerId, syscallName)` | Whether the syscall was recorded in the learned profile. |
| `ap.was_capability_used(containerId, capabilityName)` | Whether the Linux capability was previously observed. |
| `ap.was_endpoint_accessed(containerId, endpoint)` | Whether the HTTP endpoint path was previously observed. |
| `ap.was_endpoint_accessed_with_method(containerId, endpoint, method)` | Whether the HTTP endpoint was previously accessed with the given method. |
| `ap.was_endpoint_accessed_with_methods(containerId, endpoint, methods)` | Whether the HTTP endpoint was previously accessed with any method in the provided list. |
| `ap.was_endpoint_accessed_with_prefix(containerId, prefix)` | Whether any learned endpoint starts with the given prefix. |
| `ap.was_endpoint_accessed_with_suffix(containerId, suffix)` | Whether any learned endpoint ends with the given suffix. |
| `ap.was_host_accessed(containerId, host)` | Whether the host was previously observed in learned HTTP endpoint data. |

### Network neighborhood helpers (`nn.*`)

These helpers query the learned ingress and egress addresses, domains, and port/protocol tuples associated with the workload profile.

| Function | What it checks |
| --- | --- |
| `nn.was_address_in_egress(containerId, address)` | Whether the IP address was seen in learned egress traffic. |
| `nn.was_address_in_ingress(containerId, address)` | Whether the IP address was seen in learned ingress traffic. |
| `nn.is_domain_in_egress(containerId, domain)` | Whether the domain was seen in learned egress DNS data. |
| `nn.is_domain_in_ingress(containerId, domain)` | Whether the domain was seen in learned ingress DNS data. |
| `nn.was_address_port_protocol_in_egress(containerId, address, port, protocol)` | Whether the address, port, and protocol tuple was seen in learned egress traffic. |
| `nn.was_address_port_protocol_in_ingress(containerId, address, port, protocol)` | Whether the address, port, and protocol tuple was seen in learned ingress traffic. |

### Other helper namespaces

| Namespace | Functions | Purpose |
| --- | --- | --- |
| `k8s.*` | `get_container_mount_paths`, `is_api_server_address`, `get_container_by_name` | Query Pod-spec data and cluster API-server address information. |
| `parse.*` | `get_exec_path` | Normalize exec arguments into an executable path. |
| `net.*` | `is_private_ip` | Test whether an IP falls into private, loopback, or local-use ranges. |
| `process.*` | `get_process_env`, `get_ld_hook_var` | Inspect process environment variables from `/proc`. |

## Event field reference

The rule engine exposes the current event through `event.*`, and HTTP rules can also use the `http.*` alias. The authoritative field list is implemented in [`pkg/utils/cel.go`](https://github.com/kubescape/node-agent/blob/main/pkg/utils/cel.go).

!!! note
    Only fields defined in `utils.CelFields` and `utils.HttpRequestFields` are available in CEL expressions. If a field exists in the underlying Go struct but is not in those maps, it is not available in rule expressions.

### Common metadata fields

Most event types populate these top-level fields:

- `event.containerId`
- `event.containerName`
- `event.namespace`
- `event.podName`
- `event.comm`
- `event.pid`
- `event.ppid`
- `event.uid`

Fields that are not populated by a given tracer evaluate to their empty or zero value, so it is best to guard rules with `eventType` and use the field subset that matches that event type.

### Event-type-specific fields

| Event type | Commonly populated CEL fields |
| --- | --- |
| `exec` | `event.args`, `event.cwd`, `event.exepath`, `event.pcomm`, `event.pupperlayer`, `event.upperlayer` |
| `open` | `event.path`, `event.flags`, `event.flagsRaw` |
| `procfs` | `event.path` |
| `syscall` | `event.syscallName` |
| `capabilities` | `event.capName`, `event.syscallName` |
| `dns` | `event.name`, `event.dstIp`, `event.dstPort`, `event.srcPort`, `event.proto`, `event.cwd`, `event.exepath` |
| `network` | `event.dstAddr`, `event.dstPort`, `event.pktType`, `event.proto` |
| `ssh` | `event.dstIp`, `event.dstPort`, `event.srcPort` |
| `bpf` | `event.cmd`, `event.attrSize`, `event.exepath`, `event.upperlayer` |
| `kmod` | `event.module`, `event.exepath`, `event.syscallName`, `event.upperlayer` |
| `symlink` / `hardlink` | `event.newPath`, `event.oldPath`, `event.exepath`, `event.upperlayer` |
| `ptrace` | `event.exepath` |
| `unshare` | `event.exepath`, `event.upperlayer` |
| `iouring` | `event.opcode`, `event.flags` |
| `http` | `event.direction`, `event.dstIp`, `event.dstPort`, `event.srcPort`, `event.request.headers`, `event.request.host`, `event.request.method`, `event.request.url`, `event.request.path`, `event.request.body` |
| `randomx`, `fork`, `exit` | These event types currently rely on the common metadata set and do not add dedicated `utils.CelFields` entries beyond it. |

For the full event-type interfaces that back these fields, see [`pkg/utils/events.go`](https://github.com/kubescape/node-agent/blob/main/pkg/utils/events.go).

## Create your own rule

There are two common workflows:

1. Create a cluster-local `Rules` object for your own environment.
2. Contribute a reusable rule to [`kubescape/rulelibrary`](https://github.com/kubescape/rulelibrary).

### 1. Start from an existing rule

The fastest path is to copy a rule that already uses the event type you need and adjust the CEL expressions:

- Anomaly example: [`r0001-unexpected-process-launched`](https://github.com/kubescape/rulelibrary/blob/main/pkg/rules/r0001-unexpected-process-launched/unexpected-process-launched.yaml)
- Signature example: [`r1000-exec-from-malicious-source`](https://github.com/kubescape/rulelibrary/blob/main/pkg/rules/r1000-exec-from-malicious-source/exec-from-malicious-source.yaml)

### 2. Create a `Rules` manifest

Create a namespaced `Rules` object with one or more rules under `spec.rules`. The CRD requires `enabled`, `id`, `name`, `description`, `expressions`, `profileDependency`, `severity`, `supportPolicy`, `isTriggerAlert`, `mitreTactic`, and `mitreTechnique`.

```yaml
apiVersion: kubescape.io/v1
kind: Rules
metadata:
  name: custom-runtime-rules
  namespace: kubescape
spec:
  rules:
    - name: "Unexpected curl execution"
      enabled: true
      id: "R2000"
      description: "Detects curl executions that were not part of the learned application profile."
      expressions:
        message: "'Unexpected curl execution: ' + event.comm"
        uniqueId: "event.containerId + '_unexpected_curl'"
        ruleExpression:
          - eventType: "exec"
            expression: "event.comm == 'curl' && !ap.was_executed(event.containerId, parse.get_exec_path(event.args, event.comm))"
      profileDependency: 0
      severity: 5
      supportPolicy: false
      isTriggerAlert: true
      mitreTactic: "TA0002"
      mitreTechnique: "T1059"
      tags:
        - "context:kubernetes"
        - "custom"
        - "exec"
        - "applicationprofile"
```

Guidelines:

- Use an unused `R####` identifier.
- Keep the `message` and `uniqueId` expressions stable and deterministic.
- If the rule depends on learned behavior, use `profileDependency: 0` or `1`.
- Reuse tags consistently so you can bind groups of rules with `ruleTags`.

### 3. Bind the rule to workloads

`RuntimeRuleAlertBinding` controls where a rule is evaluated. You can target rules by `ruleID`, `ruleName`, or `ruleTags`.

```yaml
apiVersion: kubescape.io/v1
kind: RuntimeRuleAlertBinding
metadata:
  name: team-a-custom-rules
spec:
  namespaceSelector:
    matchLabels:
      kubernetes.io/metadata.name: team-a
  rules:
    - ruleID: "R2000"
```

Apply both manifests:

```bash
kubectl apply -f custom-runtime-rules.yaml
kubectl apply -f team-a-custom-rule-binding.yaml
```

If your rule depends on learned behavior, give the workload time to finish the learning period first. You can shorten that period with `nodeAgent.config.maxLearningPeriod`; see [Runtime Threat Detection](runtime-threat-detection.md#adjusting-learning-period).

### 4. Contribute upstream

If the rule should be part of the shared default library:

1. Create a directory under `pkg/rules/` using the `r####-descriptive-name/` convention.
2. Add the rule YAML file and a matching `rule_test.go`.
3. Run `go test -v ./pkg/rules/...`.
4. Run `./gen.sh` to regenerate `rules-crd.yaml`.
5. Open a pull request against `kubescape/rulelibrary`.

This keeps the rule authoring workflow in one place and lets Helm pick up generated rule sets cleanly in later releases.
