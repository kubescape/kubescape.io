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

Enable the GKE Autopilot allowlist when you install or upgrade. Recent chart versions set
`nodeAgent.gke.allowlist.name` to the correct allowlist for that chart version **by default**, so you
normally only need to enable the feature:

```bash
helm upgrade --install kubescape kubescape/kubescape-operator \
  ... <all the other settings> ... \
  --set nodeAgent.gke.allowlist.enabled=true
```

> Enabling the feature adds the `cloud.google.com/matching-allowlist` label to the node-agent pod, which
> is how GKE matches the workload to the allowlist.

**Overriding the allowlist name** (older charts, or to pin a specific version): set
`nodeAgent.gke.allowlist.name` to the exact name shown in Step 3 that matches your chart — for example
`armo-kubescape-node-agent-1.40-v2` (public Kubescape node-agent). **ARMO** users running the private
node-agent (`quay.io/armosec/node-agent`) should use `armo-private-node-agent-…` instead. The name must
match an allowlist installed in the cluster (Step 3).

### Step 5: Verify the Node Agent Pod is Running

```bash
kubectl get pods -n kubescape
```

Look for a pod named `node-agent-*` with `STATUS: Running`.

***

## Using private (mirrored) images

If you mirror the node-agent image into a private registry, reference it by SHA-256 **digest** that matches the public image. The allowlist publishes the accepted digests (`containerImageDigests`); see [Run Autopilot partner workloads — private image mirrors](https://cloud.google.com/kubernetes-engine/docs/how-to/run-autopilot-partner-workloads).

## Troubleshooting

**Node-agent pod/DaemonSet rejected with a GKE Warden error** (`Workload Mismatches Found` or
`does not contain all required exemptions`): the workload doesn't match the allowlist it was pointed at.
Common causes:

- **Wrong or missing version.** The allowlist named on the pod isn't installed in the cluster. Re-check
  Step 3 (`kubectl get WorkloadAllowlist`) and make sure the name matches an installed allowlist for
  your chart version. If it isn't there yet, the approved allowlist may still be rolling out to your
  region (Google rolls out gradually, up to ~7 business days after approval).
- **`AllowlistSynchronizer` not `Ready`.** Run `kubectl get allowlistsynchronizer` — a `SyncError`
  usually means one listed path isn't published yet. Keep only paths you use.
- **The node-agent genuinely changed.** If you run a chart version newer than the latest approved
  allowlist, its node-agent may require settings the allowlist doesn't cover yet. Use a chart version
  whose matching allowlist is approved.

The node-agent runs one DaemonSet per node group (the autoscaler sizes them per instance type), so you
may see several `node-agent-*` pods — this is expected.

## 🎉 You're Done!

Your GKE Autopilot cluster is now running Kubescape's node agents in compliance with GKE's partner workload policies.
