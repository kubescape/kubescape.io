# Multiple Node-Agent DaemonSets per Node Pool

## Overview

In Kubernetes clusters with heterogeneous node pools (different CPU/memory sizes), it is often necessary to run the `node-agent` with different resource requests/limits and scheduling constraints per node pool. This ensures optimal resource usage and stability, as each node pool can have a `node-agent` DaemonSet tailored to its hardware profile.

The Kubescape Operator Helm chart supports this use case via the `nodeAgent.multipleDaemonSets` feature, allowing you to deploy multiple `node-agent` DaemonSets, each with its own configuration.

***

## Why Use Multiple DaemonSets?

- **Resource Optimization:** Assign appropriate CPU/memory requests and limits for each node pool, preventing over- or under-provisioning.
- **Scheduling Control:** Use `nodeSelector` to target specific node pools, ensuring each DaemonSet runs only where intended.
- **Scalability:** Easily add or modify configurations as your cluster grows or changes.

***

## When to Use

- Your cluster has multiple node pools with different hardware profiles (e.g., standard, high-memory, GPU).
- You need to fine-tune the `node-agent` resource usage per node pool.
- You want to ensure the `node-agent` only runs on specific nodes.

***

## How to Enable and Configure

1. **Enable the Feature**

    In your `values.yaml` (or via `--set`), enable the feature:

    ```yaml
    nodeAgent:
    multipleDaemonSets:
        enabled: true
    ```

2. **Define Configurations**

    Add an entry under `configurations` for each node pool. Each entry can specify:

    - `nodeSelector`: to target the node pool
    - `resources`: requests and limits for CPU/memory

    **Example:**

    ```yaml
    nodeAgent:
    multipleDaemonSets:
        enabled: true
        configurations:
        - nodeSelector:
            kubernetes.io/os: linux
            doks.digitalocean.com/node-pool: pool-1
            resources:
            requests:
                cpu: 300m
                memory: 128Mi
            limits:
                cpu: 400m
                memory: 512Mi
        - nodeSelector:
            kubernetes.io/os: linux
            doks.digitalocean.com/node-pool: pool-2
            resources:
            requests:
                cpu: 100m
                memory: 256Mi
            limits:
                cpu: 200m
                memory: 512Mi
    ```

3. **Apply the Chart**

    Install or upgrade your Helm release as usual:

    ```sh
    helm upgrade --install kubescape-operator ./charts/kubescape-operator -f values.yaml
    ```

***

## How It Works

- When `nodeAgent.multipleDaemonSets.enabled` is `true`, the chart will render a separate DaemonSet for each configuration in the `configurations` array.
- Each DaemonSet will have its own `nodeSelector` and resource settings, and will only schedule pods on the matching nodes.

***

## Notes

- The original single DaemonSet is disabled when this feature is enabled.
- All other Kubescape Operator components are unaffected and will be deployed as usual.
- You can add as many configurations as needed for your node pools.

***

## Troubleshooting

- Ensure your node labels (used in `nodeSelector`) match those assigned to your node pools.
- If a DaemonSet is not scheduling pods, check the `nodeSelector` and resource settings for typos or conflicts.

