# Generating VEX documents using Kubescape Operator

> Note: this is an experimental feature

## What is VEX?

VEX stands for Vulnerability Exploitability Exchange, which is a standardized format for describing and sharing information about software vulnerabilities. VEX documents typically include details about the vulnerability, affected software versions, and information about a given vulnerability that is exploitable in the given software product. This information can be used by security practitioners and operators to prioritize efforts to fix vulnerabilities.

Read more about it [here](https://openvex.dev/)

## Kubescape and VEX

The Kubescape supports runtime profiling of applications using eBPF enables it to decide which vulnerability is reachable in a given workload and which is not. Read more about it [here](/docs/operator/relevancy/)

Using the information that Kubescape generates, it can also produce meaningful VEX documents for the images running in a Kubernetes cluster. It can mark (logically) vulnerabilities as "affected" based on whether the package that the vulnerability belongs to is loaded into the memory during the runtime of the container and left as "not affected" when not loaded to the memory.

There are multiple formats and implementations of the VEX as an idea. Kubescape uses the [OpenVEX specification](/docs/operator/relevancy/).

## Installing Kubescape Operator

Kubescape operator is installed as usual (see full installation guide [here](/docs/install-operator/)) expect that VEX document generation needs to be explicitly enabled using `capabilities.vexGeneration=enable` HELM flag.

Run the following to install Kubescape Operator with VEX generation.
```bash
helm repo add kubescape https://kubescape.github.io/helm-charts/
helm repo update
helm upgrade --install kubescape kubescape/kubescape-operator -n kubescape --create-namespace --set clusterName=`kubectl config current-context` --set capabilities.vexGeneration=enable
```

Make sure that all the components are running:
```bash
$ kubectl -n kubescape get pods
NAME                         READY   STATUS    RESTARTS   AGE
kubescape-6bd764869d-nmk5k   1/1     Running   0          99s
kubevuln-76bbbdfcd4-8fxcq    1/1     Running   0          99s
node-agent-dnf6l             1/1     Running   0          99s
operator-75c999bfc6-dlfj8    1/1     Running   0          99s
storage-5898d46fd-rmv4x      1/1     Running   0          99s
```

## Getting VEX document

To produce a VEX document, Kubescape needs to see a workload that runs the given image from its start. In other words, it needs to see containers from start.

Let's run a simple NGINX deployment:
```bash
kubectl apply -f https://k8s.io/examples/application/deployment.yaml
```

Wait for the VEX objects using this command:
```bash
kubectl -n kubescape get openvulnerabilityexchangecontainers.spdx.softwarecomposition.kubescape.io -w
```

It takes 2 minutes of monitoring time (by default) to produce the first version of the VEX for the image in the above deployment, it can take more if the processing queue is busy.


To get the VEX document as a JSON file locally you can use `jsonpath` to extract the `.spec` field that contains the VEX itself:
```
kubectl -n kubescape get openvulnerabilityexchangecontainer $(kubectl -n kubescape get openvulnerabilityexchangecontainer -o jsonpath='{.items[0].metadata.name}') -o jsonpath='{.spec}' > nginx.json
```
this stores the JSON format in `nginx.json`

Here is an example to see how many vulnerabilities are affected:

```bash
$ jq "." nginx.json | grep -c "\"affected\""
58
$ jq "." nginx.json | grep -c "\"not_affected\""
338
```

## Using the generated VEX document with Grype

(tested with Grype 0.71.0)

You can use the produced VEX document with Grype. Grype will take into account the VEX information when calculating results for the image `nginx:1.14.2` . Grype shall ignore all vulnerabilities that were marked as "not_affected".

Here is how to run it:
```bash
grype nginx:1.14.2 --vex nginx.json
```

This produces the following output (note the 338 ignored vulnerabilities!):
```
$ grype nginx:1.14.2 --vex nginx.json
 ✔ Vulnerability DB                [no update available]
 ✔ Loaded image                                                                                                      nginx:1.14.2
 ✔ Parsed image                                           sha256:295c7be079025306c4f1d65997fcf7adb411c88f139ad1d34b537164aa060369
 ✔ Cataloged packages              [111 packages]
 ✔ Scanned for vulnerabilities     [58 vulnerability matches]
   ├── by severity: 55 critical, 102 high, 85 medium, 52 low, 102 negligible
   └── by status:   126 fixed, 270 not-fixed, 338 ignored
```

Voila! 😎
