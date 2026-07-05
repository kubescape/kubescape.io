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

Signing is done with the `sign-object` CLI (shipped in the node-agent repo, image
`ghcr.io/k8sstormcenter/node-agent` under `cmd/sign-object`). Key-based ECDSA needs no Sigstore/OIDC:

```bash
# one-time: generate a keypair
sign-object generate-keypair                       # → cosign.key (private) + cosign.pub (public)

# author an ApplicationProfile, then sign it
sign-object sign --key cosign.key --output my-profile.signed.yaml my-profile.yaml
kubectl apply -f my-profile.signed.yaml
```

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

An attacker weakens the allow-list — say, whitelisting a shell so their RCE won't trip R0001:

```bash
kubectl patch applicationprofile my-profile --type=json \
  -p '[{"op":"add","path":"/spec/containers/0/execs/-","value":{"path":"/bin/sh","args":["/bin/sh"]}}]'
```

The `spec` changed, so it no longer matches the signature. On the next cache-load re-verification,
node-agent detects the mismatch (`Test_30`).

## 3. The detection — R1016

```json
{
  "RuleID": "R1016",
  "BaseRuntimeMetadata": {
    "alertName": "Signed profile tampered",
    "message": "Signed profile tampered: signature present but no longer valid",
    "severity": 10,
    "mitreTactic": "TA0005",
    "mitreTechnique": "T1562"
  },
  "RuntimeK8sDetails": { "namespace": "…", "podName": "…", "containerName": "…", "workloadName": "…" }
}
```

Read it like any other rule violation:

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
