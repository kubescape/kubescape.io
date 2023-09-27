# Vulnerability relevancy

The relevancy feature of the Kubescape operator enables users to understand which vulnerabilities detected by [the vulnerability scanner](vulnerabilities.md) are likely to be relevant, based on evaluation at runtime.

ARMO's relevancy is implemented by an eBPF program on each node, deployed using the [node agent](index.md#node-agent). It scans the running environment and maps out artifacts and libraries that are loaded into memory and therefore are in use in the environment.

Using eBPF probes, it looks at the file activity of a running container. When a pod starts on a node, the node agent will watch its containers for a configurable learning period and store an activity log.

During the process of scanning a container, an SBOM is generated. This contains the vulnerability scanner’s understanding of which components are installed in the container. When vulnerabilities are checked, the engine is provided with a filtered SBOM, including the packages that relate to files that were accessed during the learning period.


## Enabling relevancy

Relevancy is installed by default when installing the Kubescape operator through Helm.  You must have a node that supports eBPF.

!!! note Note
    Relevancy does not work on Minikube or Docker Desktop.

The durations for how long the node agent will observe a running container are configured with the `nodeAgent.config` values in the Helm installation:

```
nodeAgent:
  config:
    maxLearningPeriod: 3h 
    learningPeriod: 2m
    updatePeriod: 10m
```

## Using the Relevancy feature

After installation, the node agent will start listening for every **new** or **restarted** container for the time configured in the learning period. Once the learning period concludes, the relevancy information will be available in the [in-cluster storage](index.md#in-cluster-storage) and sent to a configured [provider](../providers.md). The node agent will keep listening for the container until the maxLearningPeriod is reached.

### View relevancy information

Counts of relevant vulnerabilties are available in the [vulnerability summary objects](vulnerabilities.md#vulnerabilty-summaries). The [vulnerability manifest](vulnerabilities.md#vulnerabilty-manifests) will show whether a given CVE was found relevant or not.

The full and filtered SBOM objects are stored in the `kubescape` namespace. View the labels to get the information as to which image and parent object the SBOM relates to.

```
% kubectl get -n kubescape --show-labels SBOMSPDXv2p3
NAME                                                               CREATED AT             LABELS
0349106521d476e8a833088c33f6db5ac4c898f00d1b6b6f15d9902ff5fdd0f4   2023-04-23T09:07:47Z   kubescape.io/image-name=gcr-io-vmwarecloudadvocacy-acmeshop-order
0f232ba18b63363e33f205d0242ef98324fb388434f8598c2fc8e967dca146bc   2023-04-23T09:04:23Z   kubescape.io/image-name=gke-gcr-io-cluster-proportional-autoscaler
1198b3b3f1e324799012d0634e96ef99e43831cdb240749f7ceaaab551b09622   2023-04-23T09:15:28Z   kubescape.io/image-name=quay-io-kubescape-kubevuln
13964b29d63efcd1490d1a500c4332c642655fe4ca613683fa4dde9a205dd0f7   2023-04-23T09:14:05Z   kubescape.io/image-name=ghcr-io-dexidp-dex
1d20492ca374191e5b6ff4b7712b62b41ab75ce226424974356dc266e6e99e83   2023-04-23T09:04:06Z   kubescape.io/image-name=gke-gcr-io-metrics-server
20b172e673454b675cade099b95125fb1ce01b53fbf99c5b6260e048174060b1   2023-04-23T09:08:29Z   kubescape.io/image-name=gcr-io-google-samples-microservices-demo-frontend
```

To view the filtered information:

```
% kubectl get -n kubescape --show-labels SBOMSPDXv2p3Filtered
NAME                                                               CREATED AT             LABELS
0207f7055a0a13a655efe073c320de83219ca19e396e37e1bdcc83de976ca99a   2023-04-23T10:05:48Z   kubescape.io/workload-api-group=apps,kubescape.io/workload-api-version=v1,kubescape.io/workload-container-name=redis,kubescape.io/workload-kind=Deployment,kubescape.io/workload-name=argocd-redis,kubescape.io/workload-namespace=argocd
0d69953f27f65b0546fbd29b12849368cbc5a0cf358b828ee31fbe2865279dea   2023-04-23T10:06:07Z   kubescape.io/workload-api-group=apps,kubescape.io/workload-api-version=v1,kubescape.io/workload-container-name=main,kubescape.io/workload-kind=Deployment,kubescape.io/workload-name=loadgenerator,kubescape.io/workload-namespace=onlineboutique
28372aa3a8dfdebb9cd2561f85beabbe58fbeb67060c3bde74a061c62923183f   2023-04-23T10:05:49Z   kubescape.io/workload-api-group=apps,kubescape.io/workload-api-version=v1,kubescape.io/workload-container-name=argocd-notifications-controller,kubescape.io/workload-kind=Deployment,kubescape.io/workload-name=argocd-notifications-controller,kubescape.io/workload-namespace=argocd
30c70b40821cd009b417167b2280cd9d2df4e4eef8dff79f3c7f9a8ee7d75672   2023-04-23T10:05:42Z   kubescape.io/workload-api-group=apps,kubescape.io/workload-api-version=v1,kubescape.io/workload-container-name=payment,kubescape.io/workload-kind=Deployment,kubescape.io/workload-name=payment,kubescape.io/workload-namespace=acme-fitness
```

## Limitations

### Linux kernel

The relevancy functionality is based on eBPF technology, which is implemented only on Linux kernels. This feature will not work on Windows. The kernel version on the node must be >= 4.14.

### Relevancy engine

The relevancy functionality is based on the Falco library. Falco downloads the kernel object per the kernel version in the node. Not all kernel versions have a matching object.

### Symlinks

The Falco library does not report on the actual file when a symlink is opened, meaning relevant files opened by symlink may cause CVEs to appear as not relevant.  This may result in false positives.