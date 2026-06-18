# Running ARMO/Kubescape Node Agents on GKE Autopilot Clusters

GKE Autopilot has historically restricted workloads that require privileged permissions, such as node agents used for security observability. This made it difficult for tools like Kubescape to deploy their node-level agents on Autopilot clusters.

## Why It Works Now

GKE Autopilot supports a mechanism for customers to run approved privileged workloads through a feature called **Workload Allowlisting**. A vendor (here, ARMO, which maintains the Kubescape node-agent allowlist) publishes a Google-approved `WorkloadAllowlist`, and cluster operators enable it by installing an `AllowlistSynchronizer` that references the vendor's allowlist path.

Learn more in the official GKE documentation:
👉 [Running Autopilot Partner Workloads](https://cloud.google.com/kubernetes-engine/docs/how-to/run-autopilot-partner-workloads)

***

## Prerequisites

- **GKE version:** `1.32.2-gke.1652000` or later (required for the `AllowlistSynchronizer` resource).
- **Kubescape Helm chart:** a version that exposes the `nodeAgent.gke.allowlist` values (`1.27.5` or later). Use a recent chart version.

***

## How allowlist versioning works

Each allowlist is published per **Helm chart minor version**, and its name encodes that minor version:

```
armo-kubescape-node-agent-<CHART_MINOR>
```

For example, Helm chart `1.40.x` uses the allowlist `armo-kubescape-node-agent-1.40`; chart `1.41.x` uses `armo-kubescape-node-agent-1.41`, and so on. The `AllowlistSynchronizer` path below uses a wildcard, so it installs **all approved versions** for the workload — you then select the one that matches your chart with the Helm flag in Step 4.

> The allowlist matching your chart minor must already be approved and published by Google. After you install the synchronizer, confirm the expected version appears in `kubectl get WorkloadAllowlist` (Step 3) before deploying.

***

## Step-by-Step Guide

### Step 1: Create an AllowlistSynchronizer Resource

Define an `AllowlistSynchronizer` to pull ARMO's allowlist(s) for the node-agent workload. Use the path for the image you run:

- `ARMO/armo-kubescape-node-agent/*` — the public Kubescape node-agent (`quay.io/kubescape/node-agent`).
- `ARMO/armo-private-node-agent/*` — the ARMO private node-agent (`quay.io/armosec/node-agent`).

Create a file named `kubescape-allowlist.yaml`:

```yaml
apiVersion: auto.gke.io/v1
kind: AllowlistSynchronizer
metadata:
  name: kubescape-allow-list
spec:
  allowlistPaths:
  - ARMO/armo-kubescape-node-agent/*
  - ARMO/armo-private-node-agent/*
```

### Step 2: Apply the Allowlist Resource

```bash
kubectl apply -f kubescape-allowlist.yaml
```

Optionally wait for the synchronizer to finish installing the allowlists:

```bash
kubectl wait --for=condition=Ready allowlistsynchronizer/kubescape-allow-list --timeout=60s
```

### Step 3: Validate the Allowlist Sync

```bash
kubectl get WorkloadAllowlist
```

You should see the installed allowlists, including the version that matches your Helm chart minor:

```
$ kubectl get WorkloadAllowlist
NAME                             AGE
armo-kubescape-node-agent-1.40   37s
armo-private-node-agent-1.40     37s
```

### Step 4: Install Kubescape with Helm

Install or upgrade Kubescape and point the node-agent at the matching allowlist:

```bash
helm upgrade --install kubescape kubescape/kubescape-operator \
  ... <all the other settings> ... \
  --set nodeAgent.gke.allowlist.enabled=true \
  --set nodeAgent.gke.allowlist.name=armo-kubescape-node-agent-<CHART_MINOR>
```

Set `nodeAgent.gke.allowlist.name` to the allowlist whose minor version matches the Helm chart you are installing — e.g. for chart `1.40.x`, use `armo-kubescape-node-agent-1.40`. **ARMO** users running the private node-agent should instead use `armo-private-node-agent-<CHART_MINOR>`.

> Enabling `nodeAgent.gke.allowlist.enabled` adds the `cloud.google.com/matching-allowlist` label to the node-agent pod, which is how GKE matches the workload to the named allowlist.

### Step 5: Verify the Node Agent Pod is Running

```bash
kubectl get pods -n kubescape
```

Look for a pod named `node-agent-*` with `STATUS: Running`.

***

## Using private (mirrored) images

If you mirror the node-agent image into a private registry, reference it by SHA-256 **digest** that matches the public image. The allowlist publishes the accepted digests (`containerImageDigests`); see [Run Autopilot partner workloads — private image mirrors](https://cloud.google.com/kubernetes-engine/docs/how-to/run-autopilot-partner-workloads).

## 🎉 You're Done!

Your GKE Autopilot cluster is now running Kubescape's node agents in compliance with GKE's partner workload policies.
