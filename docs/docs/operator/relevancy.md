# Vulnerability relevancy

The relevancy feature of the Kubescape operator enables users to understand which vulnerabilities detected by [the vulnerability scanner](vulnerabilities.md) are likely to be relevant, based on evaluation at runtime.

Kubescape's relevancy filtering is implemented by an [eBPF](https://ebpf.io/) program on each node, deployed using the [node agent](index.md#node-agent). It scans the running environment and maps out artifacts and libraries that are loaded into memory and therefore are in use in the environment.

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
% kubectl get -n kubescape sbomsyfts
NAME                                                                                                                                              CREATED AT
docker.io-library-alpine-sha256-e1c082e3d3c45cccac829840a25941e679c25d438cc8412c2fa221cf1a824e6a-824e6a                                           2024-02-13T09:14:25Z
docker.io-library-busybox-sha256-e8e5cca392e3cf056fcdb3093e7ac2bf83fcf28b3bcf5818fe8ae71cf360c231-60c231                                          2024-02-13T09:15:02Z
docker.io-library-redis-sha256-92f3e116c1e719acf78004dd62992c3ad56f68f810c93a8db3fe2351bb9722c2-9722c2                                            2024-02-13T09:14:30Z
docker.io-library-wordpress-sha256-5f1873a461105cb1dc1a75731671125f1fb406b18e3fcf63210e8f7f84ce560b-ce560b                                        2024-02-13T09:14:55Z
docker.io-otel-opentelemetry-collector-0.92.0-aaa6c0                                                                                              2024-02-13T09:11:47Z
gke.gcr.io-addon-resizer-1.8.19-gke.0-sha256-a462e2d1edde8ef5bc42f09ab08b15b6fa70fc61941a45da01babdc71d07abcf-07abcf                              2024-02-13T09:11:03Z
gke.gcr.io-cluster-proportional-autoscaler-1.8.4-gke.1-a146bc                                                                                     2024-02-13T09:13:02Z
gke.gcr.io-cluster-proportional-autoscaler-1.8.4-gke.1-sha256-0f232ba18b63363e33f205d0242ef98324fb388434f8598c2fc8e967dca146bc-a146bc             2024-02-13T09:12:40Z
gke.gcr.io-csi-node-driver-registrar-v2.9.2-gke.0-sha256-c3fffb646042a56c2f2e0da9017922f47c520bd25ffe52dd470125868899c8be-99c8be                  2024-02-13T09:11:11Z
gke.gcr.io-event-exporter-sha256-2607d2e19305547b3fe63b10752ae725d98c6e80940a48385974ba84007d8cc5-7d8cc5                                          2024-02-13T09:12:35Z
gke.gcr.io-fluent-bit-gke-exporter-v0.26.0-gke.5-sha256-1de68ae89a169af1013424adc95a29fd1ed8b35694c1323f245c39d647fe0876-fe0876                   2024-02-13T09:12:01Z
```

To view the filtered information:

```
% kubectl get -n kubescape sbomsyftfiltereds
NAME                                                             CREATED AT
job-kubescape-scheduler-28465179-kubescape-scheduler-ebc9-3511   2024-02-14T11:39:13Z
job-kubevuln-scheduler-28464136-kubevuln-scheduler-c7f6-7f3d     2024-02-13T18:16:10Z
replicaset-collection-94c495554-alpine-container-a3d8-540c       2024-02-13T09:16:22Z
replicaset-collection-94c495554-redis-6eab-b388                  2024-02-13T09:16:22Z
replicaset-collection-94c495554-wordpress-94fd-4e76              2024-02-13T09:16:23Z
replicaset-storage-745bb58996-apiserver-a381-b389                2024-02-13T09:12:37Z
```

## Limitations

### Linux kernel

The relevancy functionality is based on eBPF, which is currently only implemented on Linux. This feature will not work on Windows. The kernel version on the node must be >= 4.14.

!!! info Info
    The node agent uses the [Inspektor Gadget](https://www.inspektor-gadget.io/) library.

### Symlinks

The eBPF probes used by Kubescape do not report on the actual file when a symlink is opened, meaning relevant files opened by symlink may cause CVEs to appear as not relevant.  This may result in false positives.