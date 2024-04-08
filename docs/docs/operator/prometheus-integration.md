# Kubescape-Prometheus Integration

Most of the end-users either use [`prometheus-community/kube-prometheus-stack`](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) or [`prometheus-community/prometheus`](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus) to install Prometheus for monitoring. Based on your choice of Prometheus, you can follow either of the below methods to enable kubescape monitoring with Prometheus.

---

## Prometheus operator (kube-prometheus-stack) helm chart

1. Install the `kube-prometheus-stack` Helm Chart
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace prometheus
helm install -n prometheus kube-prometheus-stack prometheus-community/kube-prometheus-stack --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false,prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

2. Install the `kubescape-operator` Helm Chart with `capabilities.prometheusExporter` enabled

```
helm repo add kubescape https://kubescape.github.io/helm-charts/
helm repo update
helm upgrade --install <...> --set capabilities.prometheusExporter=enable
``` 

---

## Prometheus community helm chart

1. Install the `prometheus-community` Helm Chart
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace prometheus
helm install -n prometheus prometheus prometheus-community/prometheus
```

2. Install the `kubescape-operator` Helm Chart with `capabilities.prometheusExporter` and `configurations.prometheusAnnotations` enabled

```
helm repo add kubescape https://kubescape.github.io/helm-charts/
helm repo update
helm upgrade --install <...> --set capabilities.prometheusExporter=enable --set configurations.prometheusAnnotations=enable
```

---

## Component Diagram

```mermaid
graph TB

subgraph Cluster
    pr(Prometheus)
    ks(Kubescape)
    k8sApi(Kubernetes API)
end

pr -->|Start Scan| ks
ks -->|Collect Cluster Info|k8sApi
ks -->|Scan results| pr

classDef k8s fill:#326ce5,stroke:#fff,stroke-width:1px,color:#fff;
classDef plain fill:#ddd,stroke:#fff,stroke-width:1px,color:#000

class k8sApi k8s
class pr plain
```