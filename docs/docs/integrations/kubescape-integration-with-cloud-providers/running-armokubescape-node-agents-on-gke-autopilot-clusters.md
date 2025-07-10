# Running ARMO/Kubescape Node Agents on GKE Autopilot Clusters

GKE Autopilot has historically restricted workloads that require privileged permissions, such as node agents used for security observability. This made it difficult for tools like ARMO’s Kubescape to deploy their node-level agents on Autopilot clusters.

## Why It Works Now

Starting with recent updates, GKE Autopilot supports a new mechanism for customers to run approved privileged workloads through a feature called **Workload Allowlisting**. This allows cluster operators to enable specific vendor workloads by referencing a vendor-provided allowlist.
Learn more in the official GKE documentation:
👉 [Running Autopilot Partner Workloads](https://cloud.google.com/kubernetes-engine/docs/how-to/run-autopilot-partner-workloads)

***

## Prerequisites

- **GKE version:** `1.32.2-gke.1652000` or later
- **Kubescape Helm chart:** `1.27.5` or later

***

## Step-by-Step Guide

### Step 1: Create an AllowlistSynchronizer Resource

First, define an `AllowlistSynchronizer` resource to pull ARMO’s allowlist for node agent workloads.

Create a file named `kubescape-allowlist.yaml` with the following content:

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

<br />

### Step 2: Apply the Allowlist Resource

Apply the YAML using `kubectl`:

```bash
kubectl apply -f kubescape-allowlist.yaml
```

### Step 3: Validate the Allowlist Sync

Confirm that the allowlist has been successfully synced by running:

```bash
kubectl get WorkloadAllowlist
```

You should see a list of synced resources matching the allowlist paths.

```
$ kubectl get WorkloadAllowlist
NAME                             AGE
armo-kubescape-node-agent-1.27   37s
armo-private-node-agent-1.27     37s
```

***

### Step 4: Install Kubescape with Helm

Install or upgrade Kubescape using Helm and set the required allowlist parameters:

```bash
helm upgrade --install kubescape kubescape/kubescape-operator \
... <all the other settings> ...
  --set nodeAgent.gke.allowlist.enabled=true \
  --set nodeAgent.gke.allowlist.name=armo-kubescape-node-agent-1.27
```

Make sure your Helm chart version is `>= 1.27.5`..

:exclamation:Note that the `allowlist.name` must include the major version of the Helm chart, like in the example, we are installing the Helm chart version `1.27.5`, therefore, the name is `armo-kubescape-node-agent-1.27`. In case of Helm chart version `1.28.1` the name will be `armo-kubescape-node-agent-1.28` and so on. Also for **ARMO** users, in case you are installing ARMO Private Node-agent, use the name `armo-private-node-agent-1.27`.

***

### Step 5: Verify Node Agent Pod is Running

Check that the node agent pod is successfully running:

```bash
kubectl get pods -n kubescape
```

Look for a pod with a name similar to `node-agent-*` and ensure it has `STATUS: Running`.

***

## 🎉 You're Done!

Your GKE Autopilot cluster is now running ARMO/Kubescape's node agents securely and in compliance with GKE's partner workload policies.
