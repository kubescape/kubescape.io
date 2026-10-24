# Network Policy generation

Creating Network Policies for workloads running in a cluster is a very important step in securing your cluster. But doing so manually can be a very tedious and error-prone task.   
Kubescape provides a way to automatically generate Network Policies for your cluster. Once the Network Policy generation feature is enabled, Kubescape will listen to the network communication on your workloads, and you can then use `kubectl` to generate Network Policies automatically based on the captured traffic. Please note that the policies won't be applied to the cluster automatically. You will have to apply them manually.

## Installation 
Kubescape Network Policy generation is built into the Kubescape Operator Helm chart and is enabled by default. 
To `enable`/`disable` this capability, you need to `enable`/`disable` it when installing the chart:
```bash
--set capabilities.networkPolicyService=enable
```

Once you apply the chart with the capability enabled, Kubescape will continuously listen to the workloads traffic and you could then generate network policies for them.

In case a [provider](https://kubescape.io/docs/providers) is configured, Network Policy generation capability will be disabled by default.
To enable this capability, you need to enable it when installing the chart:
```bash
--set storage.forceVirtualCrds=true
```

## Network Policy generation

To generate a Network Policy for a workload, all you need to do is run the following command:
```
kubectl -n <namespace> get generatednetworkpolicies <workload-kind>-<workload-name> -o yaml
```
For example, if you want to generate a Network Policy for a `Deployment` named `nginx` in the `default` namespace, you would run the following command:
```
kubectl -n default get generatednetworkpolicies deployment-nginx -o yaml
```
This will return you a CRD of Kind `GeneratedNetworkPolicy`. This CRD will contain on its `spec` the generated Network Policy. You can then apply this Network Policy to your cluster.

This is an example of a generated CRD:
```yaml
apiVersion: spdx.softwarecomposition.kubescape.io/v1beta1
kind: GeneratedNetworkPolicy
metadata:
  creationTimestamp: "2023-12-12T08:46:30Z"
  labels:
    kubescape.io/workload-api-group: apps
    kubescape.io/workload-api-version: v1
    kubescape.io/workload-kind: deployment
    kubescape.io/workload-name: operator
    kubescape.io/workload-namespace: kubescape
    kubescape.io/workload-resource-version: "76459062"
  name: deployment-operator
  namespace: kubescape
policyRef:
- dns: report.armo.cloud.
  ipBlock: 16.171.184.118/32
  name: ""
  originalIP: 16.171.184.118
  server: ""
spec:
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    annotations:
      generated-by: kubescape
    creationTimestamp: null
    labels:
      kubescape.io/workload-api-group: apps
      kubescape.io/workload-api-version: v1
      kubescape.io/workload-kind: deployment
      kubescape.io/workload-name: operator
      kubescape.io/workload-namespace: kubescape
      kubescape.io/workload-resource-version: "76459062"
    name: deployment-operator
    namespace: kubescape
  spec:
    egress:
    - ports:
      - port: 4317
        protocol: TCP
      to:
      - podSelector:
          matchLabels:
            app: otel-collector
    - ports:
      - port: 8001
        protocol: TCP
      to:
      - podSelector:
          matchLabels:
            app: gateway
    - ports:
      - port: 8080
        protocol: TCP
      to:
      - podSelector:
          matchLabels:
            app: kubescape
    - ports:
      - port: 443
        protocol: TCP
      to:
      - ipBlock:
          cidr: 16.171.184.118/32
    - ports:
      - port: 53
        protocol: UDP
      to:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: kube-system
        podSelector:
          matchLabels:
            k8s-app: kube-dns
    - ports:
      - port: 8080
        protocol: TCP
      to:
      - podSelector:
          matchLabels:
            app: kubevuln
    - ports:
      - port: 443
        protocol: TCP
      to:
      - ipBlock:
          cidr: 10.128.0.90/32
    podSelector:
      matchLabels:
        app.kubernetes.io/instance: kubescape
        app.kubernetes.io/name: operator
        tier: ks-control-plane
    policyTypes:
    - Egress
```

`spec` - contains the Kubernetes native Network Policy to be applied on the cluster.  
`policyRef` - contains enrichment information about the generated Network Policy. Each entry refers to a single `cidr` on the Network Policy.  
`policyRef.originalIP` - the original IP that was captured on the traffic.  
`policyRef.ipBlock` - the IP Block that was generated based on the original IP.  
`policyRef.dns` - the DNS resolution of the original IP. This enrichment is done by the node-agent component.  
`policyRef.server` - the server to which the IP belongs to. This enrichment is done by the storage component, based on the `KnownServer` CRDs (see "Advanced Usage").  
`policyRef.name` - this is a user identifier for the IP. This is used to identify the IP in a user-friendly manner. This enrichment is done by the storage component, based on the `KnownServer` CRDs (see "Advanced Usage").  

Since the Network Policy generation is based on the traffic that is captured, it is recommended to generate the Network Policy after the workload has been running for a while. This will ensure that the Network Policy will contain all the required rules.
We also recommend going over the generated Network Policy and making sure that it contains all the required rules. You can then apply the Network Policy to your cluster.

## How it works
With Network Policy feature enabled, Kubescape will use the `node-agent` component to listen for the network traffic in all your Pods. The traffic of each container is saved in the `ingress` and `egress` fields of its `ContainerProfile`, which represents the incoming and outgoing communication of that container across all Pods of the same workload. When the client asks for a `GeneratedNetworkPolicy`, Kubescape combines the `ContainerProfile` objects of all the workload's containers with the `KnownServer` objects (see "Advanced Usage") to generate the Network Policy, converting all traffic into Network Policy rules.  

```mermaid
sequenceDiagram
    actor u as User
    participant k8a as K8sAPI
    participant kss as Storage
    participant ksn as Node-Agent

    u ->> k8a: Install Kubescape Helm Chart
    par Install Storage
        k8a ->> kss: Start
        kss -->> k8a: Confirm Storage Started
    and Install Node-Agent
        k8a ->> ksn: Start
        ksn -->> k8a: Confirm Node-Agent Started
    end
    k8a ->> u: Installation Complete

    %% Initial creation of ContainerProfile resources by Node-Agent
    ksn ->> ksn: Listen for Initial Network Traffic
    ksn ->> k8a: Create ContainerProfile Resource (one per container)
    k8a ->> kss: Store ContainerProfile Resource

    %% Node-Agent continuously monitors network traffic and updates the ContainerProfiles
    loop Continuously Monitor Network Traffic
        ksn ->> ksn: Listen for Network Traffic
        ksn ->> k8a: Update ContainerProfile Resource
        k8a ->> kss: Store Updated ContainerProfile
    end

    %% Optional scenario: User creates a 'KnownServer' CRD
    opt User creates KnownServer CRD
        u ->> k8a: Create KnownServer CRD
        k8a ->> kss: Store KnownServer CRD
    end

    %% User requests GeneratedNetworkPolicy CRD
    u ->> k8a: GET GeneratedNetworkPolicy
    k8a ->> kss: Request GeneratedNetworkPolicy
    kss ->> kss: Generate Policy from the workload's ContainerProfiles and KnownServers
    kss -->> k8a: Return GeneratedNetworkPolicy
    k8a -->> u: Provide GeneratedNetworkPolicy

```

## Advanced Usage  
  
### Known Servers

When generating Network Policies based on captured traffic, we will often encounter IPs which, by themselves, don't have any meaning. They may be part of a bigger network on which every IP actually belongs to the same service, and thus, the entire network should be represented on the policy. Or it may be unclear for someone looking at the policy what this IP actually means, and what service it represents.    
The `KnownServer` CRD comes to take care of both situations. You can define for an IP the network which is equivalent to it, and also the server to which it belongs to. You can also name it in a user-friendly manner, so it will be easier to understand what this IP actually means.

Example of a `KnownServer` CRD:
```yaml
apiVersion: spdx.softwarecomposition.kubescape.io/v1beta1
kind: KnownServer
metadata:
  name: github
spec:
- ipBlock: 142.250.1.100/24
  name: github-workflows
  server: github.com
```

This KnownServer is saying that the IP network of `142.250.1.100/24` is equivalent to the server `github.com`, and on this example we name it `github-workflows`, to give more details about what this service is used for.  
When generating a Network Policy, Kubescape will use this information to enrich the generated Network Policy.    


So if, for example, we encounter the IP `142.250.1.104` in the captured traffic, the generated network policy will have `142.250.1.100/24` as the `ipBlock` for the rule which was generated based on this IP. And the `policyRef` section will include an entry as follows:
```yaml
policyRef:
- server: github.com
  ipBlock: 142.250.1.100/24
  name: github-workflows
  originalIP: 142.250.1.104
  dns: ""
```
The `dns` field will be populated depending on the data retrieved from the node-agent and stored in the `ContainerProfile`.
  
You can generate as many `KnownServer` CRDs as you want. Kubescape will use all of them when generating the Network Policy.

### Container Profiles
The captured traffic is stored by the node-agent in the `ingress` and `egress` fields of a `ContainerProfile`. There is one `ContainerProfile` per container of the workload's Pod template, not one per Pod (for example, a Deployment with 3 replicas of a Pod with 2 containers has 2 container profiles). A `ContainerProfile` also holds the container's runtime behavior (executed processes, opened files, system calls), which is used for [runtime threat detection](runtime-threat-detection.md).  
The storage combines the profiles of all containers of a workload to generate its Network Policy on-the-fly upon a request from the user, so a Deployment `web` with an `nginx` and a `log-shipper` container gets one policy, `deployment-web`, with the traffic of both.

The network part of a `ContainerProfile` (other fields left out):
```yaml
apiVersion: spdx.softwarecomposition.kubescape.io/v1beta1
kind: ContainerProfile
metadata:
  annotations:
    kubescape.io/completion: complete
    kubescape.io/status: completed
  labels:
    kubescape.io/instance-template-hash: 5d8f7c9b4
    kubescape.io/workload-api-group: apps
    kubescape.io/workload-api-version: v1
    kubescape.io/workload-container-name: nginx
    kubescape.io/workload-kind: Deployment
    kubescape.io/workload-name: web
    kubescape.io/workload-namespace: default
  name: replicaset-web-5d8f7c9b4-nginx-1f16-ff4e
  namespace: default
spec:
  matchLabels:
    app: web
  ingress:
  - dns: ""
    identifier: 3f1c
    ipAddress: ""
    namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: shop
    podSelector:
      matchLabels:
        app: frontend
    ports:
    - name: TCP-80
      port: 80
      protocol: TCP
    type: internal
  egress:
  - dns: ""
    identifier: 9a2e
    ipAddress: ""
    namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: kube-system
    podSelector:
      matchLabels:
        k8s-app: kube-dns
    ports:
    - name: UDP-53
      port: 53
      protocol: UDP
    type: internal
```
`spec.matchLabels` - the labels that select the workload's Pods; they become the `podSelector` of the generated Network Policy.  
`egress.identifier` - a unique identifier for an egress traffic entry.  
`egress.ipAddress` - the IP address of the entry's traffic.  
`egress.dns` - the DNS resolution of the entry's traffic, in case its IP address was resolved to a DNS name.  
`egress.namespaceSelector` - the namespace selector for the entry's traffic, in case the traffic is going to a Pod in a different namespace.  
`egress.podSelector` - the pod selector for the entry's traffic, in case the traffic is going to a Pod in the cluster.  
`egress.ports` - the ports for the entry's traffic.  
`egress.ports.port` - the port number for the entry's traffic.  
`egress.ports.protocol` - the protocol for the entry's traffic.
`egress.ports.name` - the identifier for the port entry.  
`egress.type` - the type of the entry's traffic. Can be `internal` or `external`, where internal means that the traffic is going to a Pod in the cluster, and external means that the traffic is going outside the cluster.  
`ingress` - same as `egress`, but for ingress traffic.

To list the container profiles of a workload, you can run the following command:
```bash
kubectl -n <namespace> get containerprofiles -l kubescape.io/workload-name=<workload-name>
```

!!! info "Removed NetworkNeighborhood and NetworkNeighbors CRDs"

    The `NetworkNeighborhood` CRD was removed in storage v0.0.303<sup>[1](https://github.com/kubescape/storage/pull/351)</sup>; its traffic data is now part of the `ContainerProfile`. The older `NetworkNeighbors` CRD had been replaced by `NetworkNeighborhood` before that<sup>[2](https://github.com/kubescape/storage/pull/107)</sup>.
