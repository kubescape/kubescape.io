# Runtime Threat Detection & Response
The runtime threat detection & response feature of the Kubescape operator enables users to have visibility into the runtime environment and respond to threats in real-time.
Using eBPF probes toghether with Kubernetes context, kubescape effectively monitors the runtime environment for any suspicious activity.

## How it works
The runtime threat detection & response feature is divided into two main components: <br>
- [Anomaly detection engine](#Anomaly-detection-engine) 🔎 <br>
- [Behavior analysis engine](#Behavior-analysis-engine) 🧠

### Anomaly detection engine
The anomaly detection engine is responsible for detecting any abnormal behavior in the runtime environment. It does this by recording the normal behavior of the application and comparing it to the current state. If any deviation is detected, the engine will raise an alert.

To learn the normal behavior of the application, the node agent will watch the containers for a configurable learning period and store the "Application Profile" in the in-cluster storage. The Application Profile contains the base line behavior of the application, including the files accessed, network connections, system calls and more.

The durations for how long the node agent will observe a running container are configured with the nodeAgent.config values in the Helm installation:
```
nodeAgent:
  config:
    maxLearningPeriod: 12h 
    learningPeriod: 2m
    updatePeriod: 10m
```

### Behavior analysis engine
The behavior analysis engine is responsible for analyzing the behavior of the application and determining if it is malicious. It does this by analyzing the behavior of the application and comparing it to known malicious behavior. If any malicious behavior is detected, the engine will raise an alert.

The behavior analysis engine uses a set of predefined rules to determine if the behavior of the application is malicious. These rules are defined as a Custom Resource Definition (CRD) and can be customized by the user.
By default, all the rules are being enforced.
The rules are defined in the `runtimerulealertbindings.kubescape.io` CRD.
Kubescape covers a wide range of threats, including but not limited to code execution, network attacks, crypto-mining, fileless malware, and more.

## Enabling runtime threat detection & response
Runtime threat detection & response isn't installed by default when installing the Kubescape operator through Helm. 
To enable it, you must have a node that supports eBPF.
To `enable`/`disable` this capability, you need to `enable`/`disable` it when installing the chart:
```bash
--set capabilities.runtimeDetection=enable
```

## Viewing alerts
The alerts raised by the sensor can be viewed in the stdout of the node agent pod.
If you want to view the alerts in a more structured way, we support several exporters:<br>
### Prometheus (Alertmanager)
```bash
--set nodeAgent.config.alertManagerExporterUrls=localhost:9093 or localhost:9093,localhost:9094
```
### Syslog
```bash
--set nodeAgent.config.syslogExporterURL=localhost:514
```
### HTTP
```bash
--set nodeAgent.config.httpExporterConfig.url=http://localhost:8080
# Optional
--set nodeAgent.config.httpExporterConfig.maxAlertsPerMinute=1000
```
### STDOUT
```bash
--set nodeAgent.config.stdoutExporter=true
```

## Rule bindings
The CRD `runtimerulealertbindings.kubescape.io` is used to define the rules that should be enforced by the runtime threat detection & response engine.
By default, all the rules are being enforced on all workloads.
You can customize the bindings of the rules to the workloads by editing the CRD.
The CRD supports Kubernetes selectors to bind the rules to specific workloads.

## BETA features
Some features are still in beta and are not enabled by default. To enable them, you need to set the helm values accordingly.

### Malware detection
We are working on integrating a malware detection engine into the runtime threat detection & response feature. This engine will be able to detect known malware in real-time by scanning the files and processes accessed by the application.
In addition to the anomaly detection and behavior analysis engines, the malware detection engine will be able to scan the files and processes accessed by the application and compare them to known malware signatures and yara rules.
```bash
--set capabilities.malwareDetection=enable
```

## Limitations

### Linux kernel

The runtime threat detection & response functionality is based on eBPF, which is currently only implemented on Linux. This feature will not work on Windows. The kernel version on the node must be >= 4.14.
