# Host Sensor

Host scanning is enabled by default so Kubescape Operator can receive information about the worker nodes in your cluster.

Host scanning provides information about:

- the control plane, if applicable
- the container network interface (CNI) configuration
- the kernel and OS version
- the kubelet and kube-proxy configuration
- whether the node is running on a cloud provider, and if it has access to the cloud metadata server
- any open ports

The _host scanner_, or _host sensor_, is a microservice that exposes values from a Linux host. When a scan is being performed, the host scanner is deployed as a DaemonSet in a custom namespace. The host filesystem is mapped as a volume mount into the pod. After the data is collected, the DaemonSet and the namespace are deleted.

More information on the host scanner, and its source code, is [available on GitHub](https://github.com/kubescape/host-scanner/).