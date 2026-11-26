# Hardening Kubernetes workloads with the Kubescape command-line tool

## Intro

Using tools such as Kubescape to help remediate security issues in your cluster is crucial to any security plan. With Kubescape, you can scan your manifests, Helm charts, or active clusters for compliance with [security frameworks](../../frameworks-and-controls/index.md) such as NSA, MITRE, SOC 2, and more.
There are several ways to run Kubescape, including a command-line tool, an in-cluster Operator, a Visual Studio Code integration, and a GitHub action. In this guide, you will use the Kubescape command-line tool (CLI) to illustrate hardening a running Kubernetes cluster with a simple deployment. Since the Kubescape CLI is agentless, it doesn't have as much insight into the cluster as the operator does. However, it’s still a potent tool.

## Deploy a Cluster
In this example, you will use a Kubernetes cluster deployed with K3s. Any cluster will do as long as it supports a local container image registry and basic Kubectl commands. If you don’t have a cluster meeting those criteria, you can set one up using the following instructions.

### Install K3s

First, install K3s. Use the `--write-kubeconfig-mode 644` flag to allow Kubescape and non-root users to access the Kubeconfig file without `sudo`. By default, the Kubeconfig file is owned by root with privileges of `600`. The complete list of K3s configuration options can be found [here](https://docs.k3s.io/cli/server).
```shell
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
```

Now, configure the KUBECONFIG environment variable to point to the default location of the K3s configuration:
```shell
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```

Verify the cluster is up:

![image](01-cluster-up.png)

## Deploy a Pod
For this deployment, we will use a very simple NGINX container. 

### Create the Manifest

```shell
touch nginx-app.yml
```

#### nginx-app.yml

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: app
  labels:
    name: app
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-app
  namespace: app
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    imagePullPolicy: Always
    securityContext:
        privileged: true
```

### Deploy the Pod
#### Deploy
```shell
kubectl apply -f nginx-app.yml
```
#### Verify
```shell
kubectl get pods -n app
```
![image](02-get-pods.png)

Great! Now that your cluster is set up and your pod is deployed, use Kubescape to harden it.

## Use the Kubescape CLI to Detect Cluster Security Issues

### Kubescape Scan
First, install Kubescape. Do so by running the script below:
```shell
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
```

A plain `kubescape scan` runs the [cluster overview](../../scanning.md#the-overview-scan) with ClusterScan checks, highest-stake workloads, and preliminary NSA and MITRE compliance scores. Run an explicit framework scan for the detailed NSA-CISA and MITRE ATT&CK control results.

```shell
kubescape scan framework nsa,mitre
```

Record the compliance scores from the `Frameworks scanned` line and review the failed controls in the results table. The screenshot shows how scores appeared in an earlier version of the cluster overview.

![Earlier Kubescape cluster overview showing MITRE and NSA compliance scores](04-first-scan-summary.png)

### Remediate a Network Control Failure

Check for missing network policies in the `app` namespace. The verbose report lists affected resources and links to the [C-0260 control documentation](../../controls/c-0260.md).

```shell
kubescape scan control C-0260 --include-namespaces app -v
```

The example policy selects all pods in `app` and uses the automatic `kubernetes.io/metadata.name` label to allow ingress from pods in that namespace. See the [K3s Hardening Guide](https://docs.k3s.io/security/hardening-guide#networkpolicies).

#### netpol.yml

```yaml
---
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: intra-namespace
  namespace: app
spec:
  podSelector: {}
  ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: app
```

Apply the network policy.

```shell
kubectl apply -f netpol.yml
```

Rerun the control scan for `app`.

```shell
kubescape scan control C-0260 --include-namespaces app -v
```

Check that **Missing network policy** reports zero failed resources. C-0260 checks for missing policy configuration. Test pod connectivity separately to verify that the ingress restrictions are enforced.

### Workload Scanning

Scan the `nginx-app` pod to review its control results.

```shell
kubescape scan workload Pod/nginx-app --namespace app
```
![image](08-workload-scan-1.png)

You can remediate several issues. Remediate the "Privileged container" first. If you access the [C-0057 docs](https://kubescape.io/docs/controls/c-0057/), you’ll see a nice remediation example. In the `nginx-app.yml`, you can see that our `privileged` attribute is set to `true`. Sure, this is a relatively contrived and simple example, but it’s a pretty easy fix. In your `nginx-app.yml`, change the `privileged` attribute to `false`:

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: app
  labels:
    name: app
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-app
  namespace: app
spec:
  containers:
  - name: nginx-app
    image: nginx:1.21
    ports:
    - containerPort: 80
    imagePullPolicy: Always
    securityContext:
        privileged: false
```
Re-create the pod in the existing namespace to preserve the network policy.

```shell
kubectl delete pod nginx-app -n app && kubectl apply -f nginx-app.yml
```

Rerun the workload scan to check that the `C-0057` finding is cleared.

```shell
kubescape scan workload Pod/nginx-app --namespace app
```

![image](09-privilege-remediation.png)

Rerun the framework scan and compare the compliance scores with your first scan.

```shell
kubescape scan framework nsa,mitre
```

### Image Scanning
Use the `image` subcommand with the image reference from `nginx-app.yml` to scan for vulnerabilities.

```shell
kubescape scan image nginx:1.21
```

![Example vulnerability report for nginx:1.21](10-image-scan-1.png)

Set `image: nginx:latest` in `nginx-app.yml`, then re-create the pod.

```shell
kubectl delete pod nginx-app -n app && kubectl apply -f nginx-app.yml
```

Scan the updated image and compare vulnerability counts by severity with the first scan.

```shell
kubescape scan image nginx:latest
```

![Example vulnerability report for nginx:latest](11-image-scan-2.png)

Your results depend on the image contents and the vulnerability database at the time of the scan.

### Image Patching
To remediate the remaining vulnerabilities, you can also try to patch the image. Kubescape integrates with [Copacetic](https://github.com/project-copacetic/copacetic) to patch container images. To do so, run the following command:
```shell
kubescape patch -i nginx:latest
```
This command will create a patched image, by updating the packages to their applicable fixed-in versions. The patched image will be tagged with the suffix `-patched`. You can then deploy the patched image to your cluster.
```shell
docker images
REPOSITORY              TAG               IMAGE ID       CREATED         SIZE
nginx                   latest            fffffc90d343   3 weeks ago     188MB
nginx                   latest-patched    c9b68957ce42   3 weeks ago     190MB
```

By default, `kubescape patch` loads the patched image into your local Docker image store and does not push it to the source registry. The patched tarball is streamed from BuildKit into `docker load`, so the `docker` CLI must be available on your `PATH`.

To push the patched image to the source registry, pass the `--push` flag:

```shell
kubescape patch -i myregistry.example.com/team/app:1.2.3 --push
```

For private registries, run `docker login <registry>` before running the command. The BuildKit pull and push path reads registry credentials from your Docker credential store. The `--username` and `--password` flags authenticate the scan and re-scan steps, not the patch export.

With `--push`, BuildKit uploads the patched image to the registry and does not add it to your local Docker image store.


## Conclusion

In this guide, you have used Kubescape to scan a basic Kubernetes cluster for vulnerabilities, researched those vulnerabilities, and remediated them with a very straightforward process. Kubescape can also scan Helm manifests, Kustomize directories, and more. While this guide only scratches the surface, you can leverage Kubescape's CLI to harden your clusters to meet your own security requirements.
