# Signing &amp; tamper detection

A user-defined profile is an **allow-list** — whoever can edit it controls what the runtime treats
as "normal". If an attacker (or a careless CI job) quietly adds `/bin/sh` to a workload's
`ApplicationProfile`, they have *disabled* the detection for that workload, silently. Signing closes
that gap: it binds a profile to the key that authored it, and Kubescape re-checks the signature every
time it loads the profile — so any later modification is caught and raises **R1016 – Signed profile
tampered**.

This is the "signed" in *Signed Bill of Behavior*. It is exercised end to end by the node-agent
component tests `Test_29` (a signed profile is accepted), `Test_30` (tampering invalidates the
signature), and `Test_31` (the R1016 alert fires).

## The idea

```
 author                          cluster                              node-agent
 ──────                          ───────                              ──────────
 write ApplicationProfile
 sign it (cosign)  ──apply──▶  signed profile (CR)  ──load──▶  verify signature
                                     │                              ├─ valid   → use it, no alert
 attacker edits the CR ─────────────┘                              └─ changed → R1016 "tampered"
```

The signature travels **with** the object, as an annotation. Kubescape verifies it on every
cache-load, so tampering is detected wherever it happens — `kubectl edit`, a compromised operator, a
malicious admission mutation.

## 1. Sign a profile

Signing is done with the **`sign-object`** CLI, published as a minimal image
`ghcr.io/k8sstormcenter/sign-object:v0.0.3`. Key-based ECDSA needs no Sigstore/OIDC — run it against
your working directory:

```bash
alias sign-object='docker run --rm -v "$PWD:/work" ghcr.io/k8sstormcenter/sign-object:v0.0.3'

# one-time: generate a keypair
sign-object generate-keypair --output cosign.key   # → cosign.key + cosign.key.pub

# author an ApplicationProfile, then sign it
sign-object sign --file my-profile.yaml --output my-profile.signed.yaml \
  --key cosign.key --type applicationprofile
kubectl apply -f my-profile.signed.yaml
```

!!! warning "Author the profile round-trip-safe"
    Storage normalises empty arrays (`opens: []`, `syscalls: []`, `capabilities: []`, `endpoints: []`)
    to `null` on apply. Sign a profile that carries them and the stored form no longer matches the
    signature — R1016 fires at the first bind, a false tamper. **Omit** the fields you aren't
    constraining; `sign-object` emits `null` for them, which matches what storage stores. (Verified:
    the signed-vs-stored spec diff drops to zero.)

Attach the signed profile to a workload with the usual label:

```yaml
metadata:
  labels:
    kubescape.io/user-defined-profile: my-profile
```

At load, node-agent calls `VerifyObjectAllowUntrusted` — self-signed **is** the trust model here
(you sign with *your* key, not a public CA), so strict CA verification would reject every legitimate
profile. Nothing anomalous → no alert (`Test_29`).

!!! info "What is actually signed"
    The signature covers `metadata.{name, namespace, labels}` **plus** `spec` — and deliberately
    **excludes annotations**. Storage mutates annotations constantly (managed-by, completion, size,
    checksums), so signing over them would report tampering on every housekeeping write. The tamper
    check compares only the signed content.

## 2. Tamper with it

An attacker weakens the allow-list — say, whitelisting a shell so their RCE won't trip R0001. A
*completed* User profile is write-protected in place (an in-place `kubectl patch` is silently a
no-op), so they **replace** it: edit the signed YAML to append `/bin/sh` to the execs — **keeping the
original signature annotation** — and re-apply.

```bash
# add {path: /bin/sh, args: ["/bin/sh"]} to spec.containers[0].execs in my-profile.signed.yaml, then:
kubectl delete applicationprofile my-profile -n sig-demo
kubectl apply  -f my-profile.signed.yaml
```

The `spec` changed but the signature is still the old one, so it no longer verifies (`Test_30`).

!!! note "When R1016 fires"
    node-agent verifies a profile's signature on **cache-load** and caches the result, so the tamper
    is caught on the next re-verification — a profile re-sync or a fresh load — not the instant you
    edit. To see it immediately, force a reload: `kubectl -n kubescape rollout restart ds/node-agent`.

## 3. The detection — R1016

node-agent re-verifies on the next load, logs *"user-defined ApplicationProfile signature mismatch
(tamper detected)"*, and raises R1016. The whole flow — signed profile → tamper → alert:

![R1016 tamper detection](r1016-tamper.gif)

Here is the **actual alert**, captured live on a k3s rig running sbob-rc3:

```json
{"RuleID":"R1016","alertName":"Signed profile tampered","severity":10,
 "namespace":"sig-demo","workloadName":"sigapp",
 "message":"Signed ApplicationProfile 'sigapp' in namespace 'sig-demo' has been tampered with:
  signature verification failed: invalid signature…"}
```

The full alert also carries a `fixSuggestions` field — *"Investigate who modified the
ApplicationProfile 'sigapp'… Re-sign the profile after verifying its contents."* Read it like any
other rule violation:

```bash
kubectl -n kubescape logs -l app=node-agent --tail=200 | grep KubescapeRuleViolated \
  | jq -c 'select(.RuleID=="R1016") | {RuleID, msg: .BaseRuntimeMetadata.alertName, sev: .BaseRuntimeMetadata.severity}'
```

Two properties set R1016 apart from the `R00xx`/`R10xx` families:

- **It is metadata-only.** R1016 has no CEL `ruleExpression` and no eBPF event type — it is emitted
  by Go when the profile fails re-verification on cache-load, not in response to a syscall. In the
  [rule catalog](../node-agent-rule-library.md) its event type shows as `—`.
- **It is independent of enforcement** (see below).

## Detection vs. enforcement

Two separate switches — don't confuse them:

| | What it does |
|---|---|
| **R1016 detection** | *Alerts* on a tampered/invalid signature. The profile still loads, the workload keeps running — you get the signal without an outage. |
| **`enableSignatureVerification`** | *Enforcement.* When on, a tampered or unsigned profile is **dropped** (not loaded at all). |

So you can run detect-only in production (alert, don't disrupt) and turn on enforcement where you
want a tampered profile to fail closed.

!!! note "Wiring detail (why it matters in sbob-rc3)"
    R1016 only reaches your exporter because `cmd/main.go` calls `SetTamperAlertExporter(...)`.
    Without that wiring the tampering is still *detected* but the alert is silently swallowed —
    `sbob-rc3` wires it, which is what makes `Test_31` pass.

## Next

- **[What is a Bill of Behavior](index.md)** — the concept and the custom resources.
- **[Quickstart](quickstart.md)** — a live Log4Shell detection against a signed profile.
- **[Node Agent Rule Library](../node-agent-rule-library.md)** — the full rule catalog, including R1016.
