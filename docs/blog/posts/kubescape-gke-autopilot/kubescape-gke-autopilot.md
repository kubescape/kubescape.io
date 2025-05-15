---
date: 2025-05-15
categories:
  - Announcements
  - Project
authors:
  - slashben
slug: "kubescape-gke-autopilot"
---

# Kubescape Node Agent Now Works on GKE Autopilot Clusters

The Kubescape community is excited to share that **Kubescape’s node agent now supports GKE Autopilot clusters**, thanks to Google Cloud’s newly introduced **Workload Allowlisting** capability.

This is a significant milestone that opens the door for **full runtime observability and Kubernetes-native security** on fully-managed GKE environments.

---

## A Quick Background: Why It Wasn’t Possible Before

Historically, GKE Autopilot enforced strict constraints on workloads requiring privileged permissions, like those needed by Kubescape’s node agent. This made it impossible to get visibility into system-level activity — something many security-conscious users rely on for runtime protection, vulnerability tracing, and compliance enforcement.

But with the rollout of Google Cloud’s **Autopilot partner workload support**, this has changed. Users can now explicitly allow trusted workloads through a declarative **AllowlistSynchronizer** configuration. Kubescape is among the first open-source tools to make use of this capability.

👉 [Learn more about Google Cloud’s Allowlisting mechanism](https://cloud.google.com/kubernetes-engine/docs/how-to/run-autopilot-partner-workloads)

---

## Why It Matters

By running Kubescape’s node agent on GKE Autopilot, users can finally get **deep runtime visibility and Kubernetes-native security** without needing to manage the underlying nodes themselves.

This means:

* Access to **real-time anomaly detection** from inside your container and host environment
* Support for **seccomp and network policy insights**, including smart suggestions
* Seamless **vulnerability prioritization** with in-use and reachable package analysis
* **Compliance scanning and misconfiguration detection** with behavioral remediation insights

---

## How to Enable It

1. Make sure your cluster is running GKE Autopilot **version `1.32.2-gke.1652000` or newer**
2. Use Kubescape Helm chart **version `1.27.5` or newer**
3. Create an `AllowlistSynchronizer` object to sync the allowlist for Kubescape:

```yaml
apiVersion: auto.gke.io/v1
kind: AllowlistSynchronizer
metadata:
  name: kubescape-allow-list
spec:
  allowlistPaths:
  - ARMO/armo-kubescape-node-agent/1.27/*
```

4. Apply it to your cluster:

```bash
kubectl apply -f kubescape-allowlist.yaml
```

5. Confirm it's synced:

```bash
kubectl get WorkloadAllowlist
```

6. Install Kubescape with Helm:

```bash
helm upgrade --install kubescape kubescape/kubescape-operator \
  --set nodeAgent.gke.allowlist.enabled=true \
  --set nodeAgent.gke.allowlist.name=armo-kubescape-node-agent-1.27
```

7. Verify the node agent is running:

```bash
kubectl get pods -n kubescape
```

---

## What’s Next?

Kubescape continues to evolve with community input and contributions. Supporting GKE Autopilot is part of a broader goal: making **Kubernetes security accessible, powerful, and fully open** — no matter where or how you run your workloads. We're excited to see this feature land and look forward to seeing what the community will build with it.

If you are missing a feature or have feedback, please let us know on [GitHub](https://github.com/kubescape/kubescape/issues) or [Discussions](https://github.com/kubescape/kubescape/discussions).
