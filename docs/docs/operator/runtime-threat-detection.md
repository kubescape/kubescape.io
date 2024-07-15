# Runtime Threat Detection

The runtime threat detection feature of Kubescape enables users to have visibility into the runtime environment and detects security threats in real time within the Kubernetes Pods and API server.

It is designed to be a simple, low-footprint, easy-to-use, and effective tool for detecting threats in your Kubernetes cluster at runtime.

It is based on eBPF-based event monitoring on Kubernetes nodes and an advanced rule engine that allows you to write rules that can detect and respond to threats in your cluster and more specifically in your workload itself🛡️.

## Architecture

Runtime threat detection is part of the Kubescape Operator, and most of the functionality is implemented as part of the Node-agent.

![Node agent design](/assets/node-agent-design.svg)

Node-agent uses [Inspektor Gadget](https://www.inspektor-gadget.io/) for eBPF event aquistion. It uses the [Kubescape Storage](https://github.com/kubescape/storage) to store and monitor detection related objects.

Alerts can be sent to multiple sink components, from logs to Prometheus AlertManager.

Detection capabilities are organized into "Rules" and each of them is designed to detect a single threat.

## How it works

Kubescape Node-agent leverages advanced eBPF (extended Berkeley Packet Filter) technology for comprehensive runtime security detection in Kubernetes environments. Its detection capabilities encompass a wide array of events including new process initiations, file activities, network operations, system call activities, and usage of Linux capabilities.

The runtime threat detection feature is divided into three main detection strategies:

* [Anomaly detection engine](#anomaly-detection-engine) 🔎
* [Behavior analysis engine](#behavior-analysis-engine) 🧠
* [Malware scanner](#malware-scanning) 🐛


### Anomaly detection engine
The anomaly detection engine is responsible for detecting any abnormal behavior in the runtime environment. It does this by recording the baseline behavior of the application and comparing it to the current state. If any deviation is detected, the engine will raise an alert.

Kubescape observes containers during a customizable learning phase to understand the application's typical behavior. It then stores this information persistently in objects called `ApplicationProfiles` (see [here](https://github.com/kubescape/storage/blob/968527e99defc5be451813e1008453869cf82c0a/pkg/apis/softwarecomposition/v1beta1/types.go#L238)) , capturing details such as file access, network connections, system calls, and other relevant data. This profile, stored as a Kubernetes Custom Resource (CR), serves as a benchmark for normal behavior. Once the learning phase concludes and the profile is established, Kubescape validates application events coming from eBPF for deviations from this norm, triggering alerts upon detecting anomalies.

### Behavior analysis engine
Additionally, Kubescape is equipped with rules designed to identify well-known attack signatures. These rules are adept at uncovering various threats, such as unauthorized software executions that deviate from the original container image, detection of unpackers in memory, reverse shell activities, and more. Users have the flexibility to create 'Rule Bindings'—specific instructions that direct Kubescape on which rules should be applied to which Pods. This level of customization ensures that security measures are tailored to the unique needs of each Kubernetes deployment, enhancing the overall security posture and responsiveness of the system.

### Malware scanning
Kubescape can scan the nodes for malware using ClamAV as an engine, a popular open-source antivirus engine. ClamAV supports scanning of files, directories, and volumes, and can be configured to scan the entire node or only specific directories. You can read more about ClamAV here.

Kubescape uses its own virus database which is a subset of the latest ClamAV virus database release but adopted to Kubernetes environment to save resources.

### Rule bindings
The CRD `runtimerulealertbindings.kubescape.io` is used to define the rules that should be enforced by the runtime threat detection engine.
By default, all the rules are enforced on all workloads.
You can customize the bindings of the rules to the workloads by editing the CRD.
The CRD supports Kubernetes selectors to bind the rules to specific workloads.

## Getting started

### Basic installation

To install Kubescape with runtime detection enabled, run the following installation steps:

```bash
helm repo add kubescape https://kubescape.github.io/helm-charts/
helm repo update
helm upgrade --install kubescape kubescape/kubescape-operator -n kubescape --create-namespace --set capabilities.runtimeDetection=enable --set alertCRD.installDefault=true
```

This installs the Node-agent with detection enabled and with default alert rule bindings.
Note, that we have not defined an exporter, therefore the alerts are sent to the Node-agent logs.

Wait for the learning period to end (the default is 24h!) and you can try out the detection capabilities.

For example, in this case we run the system on a Kind cluster and here is what you see in logs if you open a process on a container:
```bash
$ kubectl apply -f https://k8s.io/examples/application/deployment.yaml
$ sleep $LEARNING_PERIOD
$ kubectl exec nginx-deployment-86dcfdf4c6-lh6cb -- echo "I am alerting"
I am alerting
```

We can see the alerts that were produced due to the fact that the `echo` process is not expect to run in this container:
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





## Limitations

### Linux kernel

The runtime threat detection functionality is based on eBPF, which is currently only implemented on Linux. This feature will not work on Windows. The kernel version on the node must be >= 4.14.
