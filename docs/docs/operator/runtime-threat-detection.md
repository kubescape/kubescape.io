# Runtime Threat Detection

Kubescape's  runtime threat detection feature enables users to gain visibility into the runtime environment and detects security threats in real time within Kubernetes Pods and API server.

It is designed to be a simple, low-footprint, easy-to-use, and effective tool for detecting threats in your Kubernetes cluster at runtime.

It is uses eBPF-based event monitoring on Kubernetes nodes and an advanced rule engine that allows you to write rules that can detect and respond to threats in your cluster and more specifically in your workload itself🛡️.

## Architecture

Runtime threat detection is part of the Kubescape Operator, and most of the functionality is implemented as part of the node-agent.

![Node agent design](/assets/node-agent-design.svg)

node-agent uses [Inspektor Gadget](https://www.inspektor-gadget.io/) for eBPF event acquisition for most events and implements some of its own eBPF gadgets. It uses the [Kubescape Storage](https://github.com/kubescape/storage) to store and monitor detection related objects.

Alerts can be sent to multiple sink components, from logs to Prometheus AlertManager.

Detection capabilities are organized into "Rules" and each of them is designed to detect a single threat.

## How it works

Kubescape node-agent leverages advanced eBPF (extended Berkeley Packet Filter) technology for comprehensive runtime security detection in Kubernetes environments. Its detection capabilities encompass a wide array of events including new process initiations, file activities, network operations, system call activities, and usage of Linux capabilities.

The runtime threat detection feature is divided into three main detection strategies:

* [Anomaly detection engine](#anomaly-detection-engine) 🔎
* [Behavioral analysis engine](#behavior-analysis-engine) 🧠
* [Malware scanner](#malware-scanning) 🐛


### Anomaly detection engine
The anomaly detection engine is responsible for detecting any abnormal behavior in the runtime environment. It does this by recording the baseline behavior of the application and comparing it to the current state. If any deviation is detected, the engine will raise an alert.

Kubescape observes containers during a customizable learning phase to understand the application's typical behavior. It then stores this information persistently in objects called `ApplicationProfiles` (see [here](https://github.com/kubescape/storage/blob/968527e99defc5be451813e1008453869cf82c0a/pkg/apis/softwarecomposition/v1beta1/types.go#L238)) , capturing details such as file access, network connections, system calls, and other relevant data. This profile, stored as a Kubernetes Custom Resource (CR), serves as a benchmark for normal behavior. Once the learning phase concludes and the profile is established, Kubescape validates application events coming from eBPF for deviations from this norm, triggering alerts upon detecting anomalies.

### Behavioral analysis engine
Additionally, Kubescape is equipped with rules designed to identify well-known attack signatures. These rules are adept at uncovering various threats, such as unauthorized software executions that deviate from the original container image, detection of unpackers in memory, reverse shell activities, and more. Users have the flexibility to create 'Rule Bindings'—specific instructions that direct Kubescape on which rules should be applied to which Pods. This level of customization ensures that security measures are tailored to the unique needs of each Kubernetes deployment, enhancing the overall security posture and responsiveness of the system.

### Malware scanning
Kubescape can scan the nodes for malware using ClamAV as an engine, a popular open-source antivirus engine. ClamAV supports scanning of files, directories, and volumes, and can be configured to scan the entire node or only specific directories. You can read more about ClamAV here.

Kubescape uses its own virus database which is a subset of the latest ClamAV virus database release but adapted to Kubernetes environment to save resources.

### Rule bindings
The CRD `runtimerulealertbindings.kubescape.io` is used to define the rules that should be enforced by the runtime threat detection engine.
By default, all the rules are enforced on all workloads.
You can customize the bindings of the rules to the workloads by editing the CRD.
The CRD supports Kubernetes selectors to bind the rules to specific workloads.
You can find the CRD definition [here](https://github.com/kubescape/helm-charts/blob/main/charts/dependency_chart/clustered-crds/crds/runtime-rule-binding.crd.yaml).

Example of a `RuntimeRuleAlertBinding` CRD:
<details>
<summary>Click to expand</summary>

```yaml
apiVersion: kubescape.io/v1
kind: RuntimeRuleAlertBinding
metadata:
  name: all-rules-all-pods
spec:
  namespaceSelector:
    matchExpressions:
      - key: "kubernetes.io/metadata.name"
        operator: "NotIn"
        values:
        - "kube-system"
        - "kube-public"
        - "kube-node-lease"
        - "kubeconfig"
        - "gmp-system"
        - "gmp-public"
  rules:
    - ruleName: "Unexpected process launched"
    - ruleName: "Unexpected file access"
      parameters:
        ignoreMounts: true
        ignorePrefixes: ["/proc", "/run/secrets/kubernetes.io/serviceaccount", "/var/run/secrets/kubernetes.io/serviceaccount", "/tmp"]
    - ruleName: "Unexpected system call"
    - ruleName: "Unexpected capability used"
    - ruleName: "Unexpected domain request"
    - ruleName: "Unexpected Service Account Token Access"
    - ruleName: "Kubernetes Client Executed"
    - ruleName: "Exec from malicious source"
    - ruleName: "Kernel Module Load"
    - ruleName: "Exec Binary Not In Base Image"
    - ruleName: "Malicious SSH Connection"
    - ruleName: "Fileless Execution"
    - ruleName: "XMR Crypto Mining Detection"
    - ruleName: "Exec from mount"
    - ruleName: "Crypto Mining Related Port Communication"
    - ruleName: "Crypto Mining Domain Communication"
    - ruleName: "Read Environment Variables from procfs"
    - ruleName: "eBPF Program Load"
    - ruleName: "Symlink Created Over Sensitive File"
    - ruleName: "Unexpected Sensitive File Access"
    - ruleName: "LD_PRELOAD Hook"
    - ruleName: "Hardlink Created Over Sensitive File"
```
</details>

The rules are defined in the [node-agent repository](https://github.com/kubescape/node-agent/tree/main/pkg/ruleengine/v1).
Currently, the following rules are supported:

| **Rule**                                      | **Description**                                                                                       |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **Unexpected process launched**               | Detects the launch of an unexpected or unauthorized process.                                           |
| **Unexpected file access**                    | Identifies unexpected access to files. `ignoreMounts` parameter can be used to ignore mounts, `ignorePrefixes` parameter can be used to ignore specific prefixes. |
| **Unexpected system call**                    | Detects unexpected or unauthorized system calls.                                                      |
| **Unexpected capability used**                | Flags the use of unexpected capabilities.                                                             |
| **Unexpected domain request**                 | Identifies requests to unexpected or unauthorized domains.                                            |
| **Unexpected Service Account Token Access**   | Detects unauthorized access to service account tokens.                                                |
| **Kubernetes Client Executed**                | Detects the execution of a Kubernetes client.                                                         |
| **Exec from malicious source**                | Identifies execution of commands from a known malicious source.                                       |
| **Kernel Module Load**                        | Detects the loading of unauthorized or unexpected kernel modules.                                     |
| **Exec Binary Not In Base Image**             | Flags execution of binaries not included in the base image.                                           |
| **Malicious SSH Connection**                  | Detects malicious or unauthorized SSH connections.                                                    |
| **Fileless Execution**                        | Identifies execution of commands or scripts without a file.                                           |
| **XMR Crypto Mining Detection**               | Detects cryptocurrency mining activity related to Monero (XMR).                                       |
| **Exec from mount**                           | Flags execution of commands from a mounted directory.                                                 |
| **Crypto Mining Related Port Communication**  | Identifies port communication related to cryptocurrency mining.                                       |
| **Crypto Mining Domain Communication**        | Detects communication with domains associated with cryptocurrency mining.                             |
| **Read Environment Variables from procfs**    | Flags unauthorized reading of environment variables from procfs.                                       |
| **eBPF Program Load**                         | Detects loading of eBPF programs.                                                                     |
| **Symlink Created Over Sensitive File**       | Flags the creation of symlinks over sensitive files. `additionalPaths` parameter can be used to specify additional paths to be checked. |
| **Unexpected Sensitive File Access**          | Identifies access to sensitive files. `additionalPaths` parameter can be used to specify additional paths to be checked. |
| **LD_PRELOAD Hook**                           | Detects the use of LD_PRELOAD to hook shared libraries.                                               |
| **Hardlink Created Over Sensitive File**      | Flags the creation of hardlinks over sensitive files. `additionalPaths` parameter can be used to specify additional paths to be checked. |


The rules are written in golang and are compiled into the node-agent binary.
In the future we plan to add additional rules, as well as support custom rules.
Some of the rules support parameters that can be set in the Rule Binding CRD.

## Application profiles
Application profiles are used to store the normal behavior of the application, as recorded during the learning phase.
The profiles are stored in the `ApplicationProfile` CRD.

An example of an `ApplicationProfile` CRD:
<details>
<summary>Click to expand</summary>

```json
{
  "kind": "ApplicationProfile",
  "apiVersion": "spdx.softwarecomposition.kubescape.io/v1beta1",
  "metadata": {
    "name": "replicaset-nginx-77b4fdf86c",
    "creationTimestamp": "2024-03-19T09:27:05Z",
    "labels": {
      "kubescape.io/instance-template-hash": "77b4fdf86c",
      "kubescape.io/workload-api-group": "apps",
      "kubescape.io/workload-api-version": "v1",
      "kubescape.io/workload-kind": "Deployment",
      "kubescape.io/workload-name": "nginx"
    },
    "annotations": {
      "kubescape.io/completion": "complete",
      "kubescape.io/resource-size": "85",
      "kubescape.io/status": "completed"
    }
  },
  "spec": {
    "architectures": [
      "amd64",
      "arm64"
    ],
    "containers": [
      {
        "capabilities": [
          "NET_BIND_SERVICE",
          "DAC_OVERRIDE",
          "CHOWN",
          "SETGID",
          "SETUID"
        ],
        "execs": [
          {
            "path": "/usr/bin/dpkg-query",
            "args": [
              "--show",
              "--showformat=${Conffiles}\\n",
              "/usr/bin/dpkg-query",
              "nginx"
            ]
          },
          {
            "path": "/docker-entrypoint.sh",
            "args": [
              "-g",
              "/docker-entrypoint.sh",
              "daemon off;",
              "nginx"
            ]
          },
          {
            "path": "/usr/bin/cut",
            "args": [
              "-d ",
              "-f",
              "/usr/bin/cut",
              "3"
            ]
          },
          {
            "path": "/docker-entrypoint.d/30-tune-worker-processes.sh",
            "args": [
              "/docker-entrypoint.d/30-tune-worker-processes.sh"
            ]
          },
          {
            "path": "/docker-entrypoint.d/10-listen-on-ipv6-by-default.sh",
            "args": [
              "/docker-entrypoint.d/10-listen-on-ipv6-by-default.sh"
            ]
          },
          {
            "path": "/usr/bin/touch",
            "args": [
              "/etc/nginx/conf.d/default.conf",
              "/usr/bin/touch"
            ]
          },
          {
            "path": "/usr/sbin/nginx",
            "args": [
              "-g",
              "/usr/sbin/nginx",
              "daemon off;"
            ]
          },
          {
            "path": "/usr/bin/md5sum",
            "args": [
              "-",
              "-c",
              "/usr/bin/md5sum"
            ]
          },
          {
            "path": "/usr/bin/sed",
            "args": [
              "-E",
              "-i",
              "/etc/nginx/conf.d/default.conf",
              "/usr/bin/sed",
              "s,listen       80;,listen       80;\\n    listen  [::]:80;,"
            ]
          },
          {
            "path": "/usr/bin/grep",
            "args": [
              "-q",
              "/etc/nginx/conf.d/default.conf",
              "/usr/bin/grep",
              "etc/nginx/conf.d/default.conf",
              "listen  \\[::]\\:80;"
            ]
          },
          {
            "path": "/etc/nginx/conf.d/sedzJNyeW"
          }
        ],
        "opens": null,
        "syscalls": null,
        "seccompProfile": {
          "path": "default/replicaset-nginx-bf5d5cf98-nginx.json",
          "spec": {
            "defaultAction": "SCMP_ACT_ERRNO",
            "architectures": [
              "SCMP_ARCH_X86_64",
              "SCMP_ARCH_X86",
              "SCMP_ARCH_X32"
            ],
            "syscalls": [
              {
                "names": [
                  "accept4",
                  "epoll_wait",
                  "pselect6",
                  "futex",
                  "madvise",
                  "epoll_ctl",
                  "getsockname",
                  "setsockopt",
                  "vfork",
                  "mmap",
                  "arch_prctl",
                  "sysinfo",
                  "symlinkat",
                  "connect",
                  "dup3",
                  "getcwd",
                  "getpid",
                  "brk",
                  "fchdir",
                  "pread64",
                  "wait4",
                  "clone3",
                  "setuid",
                  "write",
                  "prctl",
                  "munmap",
                  "rt_sigprocmask",
                  "rt_sigreturn",
                  "fsetxattr",
                  "getrandom",
                  "ioctl",
                  "mount",
                  "getpeername",
                  "gettid",
                  "fcntl",
                  "mkdirat",
                  "prlimit64",
                  "setgid",
                  "fgetxattr",
                  "pwrite64",
                  "sched_yield",
                  "uname",
                  "openat2",
                  "vfork",
                  "openat",
                  "umask",
                  "nanosleep",
                  "eventfd2",
                  "getgid",
                  "listen",
                  "mprotect",
                  "epoll_ctl",
                  "fchmodat",
                  "getegid",
                  "epoll_pwait",
                  "keyctl",
                  "mkdir",
                  "set_robust_list",
                  "tgkill",
                  "read",
                  "rseq",
                  "statfs",
                  "unlinkat",
                  "capset",
                  "epoll_create",
                  "fstatfs",
                  "sched_getaffinity",
                  "fchownat",
                  "newfstatat",
                  "sendmsg",
                  "chown",
                  "clone",
                  "execve",
                  "faccessat2",
                  "rename",
                  "umount2",
                  "access",
                  "futex",
                  "getsockopt",
                  "readlinkat",
                  "dup2",
                  "geteuid",
                  "bind",
                  "pipe2",
                  "rt_sigsuspend",
                  "fstat",
                  "socketpair",
                  "mmap",
                  "set_tid_address",
                  "setgroups",
                  "setsid",
                  "exit",
                  "getuid",
                  "io_setup",
                  "mknodat",
                  "unshare",
                  "getppid",
                  "madvise",
                  "setsockopt",
                  "getdents64",
                  "lseek",
                  "mount_setattr",
                  "rt_sigaction",
                  "sigaltstack",
                  "capget",
                  "chdir",
                  "epoll_wait",
                  "linkat",
                  "exit_group",
                  "getrlimit",
                  "recvmsg",
                  "socket",
                  "fadvise64",
                  "pivot_root",
                  "sethostname",
                  "utimensat",
                  "close",
                  "epoll_create1",
                  "fchown",
                  "getsockname"
                ],
                "action": "SCMP_ACT_ALLOW"
              }
            ]
          }
        }
      }
    ]
  },
  "status": {}
}
```
</details>

You can modify the `ApplicationProfile` CRD to add or remove execs, syscalls, capabilities, and opens.
Once the learning phase is over, the profile is used to detect anomalies in the runtime environment.
If you want to know when a profile is completed, you can check the `kubescape.io/status` annotation, `completed` means that the profile is ready to be used for detection.
`kubescape.io/completion` annotation can be used to track the completion of the profile. This is useful in cases where we started the recording of the profile on an already running workload. It is initially marked as`partial` until the workload is restarted. Note: we do enforce the rules on the workload even if the profile is incomplete (i.e. lacks the completion annotation).
We recommend that you restart the workloads after installing the Kubescape Operator to ensure that the profiles are completed.

## Getting started

### Basic installation

To install Kubescape with runtime detection enabled, run the following installation steps:

```bash
helm repo add kubescape https://kubescape.github.io/helm-charts/
helm repo update
helm upgrade --install kubescape kubescape/kubescape-operator -n kubescape --create-namespace --set capabilities.runtimeDetection=enable --set alertCRD.installDefault=true
```

This installs the node-agent with detection enabled and with default alert rule bindings.
Note, that we have not defined an exporter, therefore the alerts are sent to the node-agent logs.

Wait for the learning period to end (the default is 24h!) and you can try out the detection capabilities.

For example, in this case we ran the system on a Kind cluster and here is what you see in logs if you open a process on a container:
```bash
$ kubectl apply -f https://k8s.io/examples/application/deployment.yaml
$ sleep $LEARNING_PERIOD
$ kubectl exec nginx-deployment-86dcfdf4c6-lh6cb -- echo "I am alerting"
I am alerting
```

We can see the alerts that were produced due to the fact that the `echo` process is not expected to run in this container:
```bash
$ kubectl -n kubescape logs node-agent-dj74j | grep "Unexpected process"
{"BaseRuntimeMetadata":{"alertName":"Unexpected process launched","arguments":{"retval":0},"infectedPID":912230,"fixSuggestions":"If this is a valid behavior, please add the exec call \"/bin/echo\" to the whitelist in the application profile for the Pod \"nginx-deployment-86dcfdf4c6-lh6cb\". You can use the following command: kubectl patch applicationprofile replicaset-nginx-deployment-86dcfdf4c6 --namespace default --type merge -p '{\"spec\": {\"containers\": [{\"name\": \"nginx\", \"execs\": [{\"path\": \"/bin/echo\", \"args\": [\"/bin/echo\",\"I am alerting\"]}]}]}}'","md5Hash":"29f4bf55fe826e5b167340f91aeb0f49","sha1Hash":"ebaa9671f9af592e581fef02d8a44481637da137","sha256Hash":"615183f74a4f135160e2323720678396454266d17647874816f2843714bad102","severity":5,"size":"32 kB","timestamp":"2024-07-15T12:00:32.039539572Z"},"RuleID":"R0001","RuntimeK8sDetails":{"clusterName":"cluster","containerName":"nginx","hostNetwork":false,"image":"docker.io/library/nginx:1.14.2","namespace":"default","containerID":"750aad8591525bcc8afb666ad88fc943afa3ffca3d4b2ff4d101e3eae660e498","podName":"nginx-deployment-86dcfdf4c6-lh6cb","podNamespace":"default","workloadName":"nginx-deployment","workloadNamespace":"default","workloadKind":"Deployment"},"RuntimeProcessDetails":{"processTree":{"pid":912230,"cmdline":"/bin/echo I am alerting","comm":"echo","ppid":912221,"pcomm":"containerd-shim","hardlink":"/bin/echo","uid":0,"gid":0,"upperLayer":false,"cwd":"/","path":"/bin/echo"},"uniqueID":0,"containerID":"750aad8591525bcc8afb666ad88fc943afa3ffca3d4b2ff4d101e3eae660e498"},"event":{"runtime":{"runtimeName":"containerd","containerId":"750aad8591525bcc8afb666ad88fc943afa3ffca3d4b2ff4d101e3eae660e498","containerImageName":"docker.io/library/nginx:1.14.2"},"k8s":{"namespace":"default","podName":"nginx-deployment-86dcfdf4c6-lh6cb","podLabels":{"app":"nginx","pod-template-hash":"86dcfdf4c6"},"containerName":"nginx"},"timestamp":1721044832039539572,"type":"normal"},"level":"error","message":"Unexpected process launched: /bin/echo in: nginx","msg":"Unexpected process launched","time":"2024-07-15T12:00:32Z"}
```
### Adjusting learning period

The default learning period is 24 hours, you can adjust it with this value:

```bash
--set nodeAgent.config.maxLearningPeriod=10m
```

### Viewing alerts
The alerts raised by the sensor can be viewed in the stdout of the node agent pod.
If you want to view the alerts in a more structured way, we support several exporters:

#### Prometheus (Alertmanager)
```bash
--set nodeAgent.config.alertManagerExporterUrls=localhost:9093 or localhost:9093,localhost:9094
```
#### Syslog
```bash
--set nodeAgent.config.syslogExporterURL=localhost:514
```
#### HTTP
```bash
--set nodeAgent.config.httpExporterConfig.url=http://localhost:8080
# Optional
--set nodeAgent.config.httpExporterConfig.maxAlertsPerMinute=1000
```
#### STDOUT
```bash
--set nodeAgent.config.stdoutExporter=true
```

## Alert aggregation
When running anomaly detection, the system relies on the fact that normal application behavior was recorded and can be compared to the current state. This means that if something was missed (e.g syscall/file access) during the learning phase, the system will generate many alerts during runtime. To avoid this, we recommend using a learning phase that is long enough to capture all the possible behavior of the application. The default is 24h. In addition, we recommend you to consider disabling the "Unexpected file access" rule or any other anomaly rule (i.e. those that start eith the word 'Unexpected') as long you are not doing any alert aggregation.

## Limitations

### Linux kernel

The runtime threat detection functionality is based on eBPF, which is currently only implemented on Linux. This feature will not work on Windows. The kernel version on the node must be >= 4.14.
