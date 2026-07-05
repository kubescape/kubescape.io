# Bill of Behavior

A **Software Bill of Behavior (SBoB)** is a declarative profile of what a workload is *intended* to do at runtime — the processes it spawns, the files it opens, the network destinations it reaches, and the Linux capabilities it requests.

Where a Software Bill of Materials (SBOM) describes what a workload is *made of*, a Bill of Behavior describes what it is *meant to do*. The SBOM is the ingredient list; the SBoB is the package insert. Anything a workload does at runtime that the SBoB does not declare is, by definition, drift — a vendor bug to fix, or a compromise to alert on.

This matters because most modern compromises leave no SBOM trace: stolen credentials, living-off-the-land, and supply-chain implants are all *behavioral*. They only show up at runtime, measured against a declaration of intent.

## How Kubescape is a reference implementation

Kubescape implements the Bill of Behavior end to end, using eBPF to observe workloads at the Linux ABI and Kubernetes custom resources to store the declaration:

| SBoB concept | Kubescape realization |
|---|---|
| declared process / file / capability behavior | `ApplicationProfile` custom resource |
| declared network behavior (egress / ingress) | `NetworkNeighborhood` custom resource |
| drift detection | CEL-based rules in the `node-agent` rule library |
| observation layer | the `node-agent`, using eBPF (no instrumentation of the workload) |
| storage / API | the Kubescape `storage` aggregated apiserver |

The lifecycle is three steps:

1. **Learn.** When a workload is first deployed, the node-agent records its behavior over a learning period (default 5 minutes) and writes it to an `ApplicationProfile` and a `NetworkNeighborhood`.
2. **Seal.** When the learning period ends the profile is marked `completed` — it now describes the workload's expected behavior.
3. **Detect.** The node-agent switches to detection. Behavior outside the sealed profile raises an alert, evaluated by the rule library.

## Beyond learned profiles

A learned profile captures what a workload *did* during learning. For production you often want to declare what a workload *should* do — more general, vendor-authored, signed. Kubescape supports this directly:

- **Wildcards** in exec arguments, file paths, and network destinations (CIDRs and DNS-label patterns), so a profile describes a *class* of behavior rather than one observed instance.
- **Profile compaction** via a `CollapseConfig`, folding many concrete observations into a smaller, maintainable profile.
- **Signing and tamper detection**, so a user-supplied profile can be cryptographically verified and any later modification is detected at runtime.

## Next

See **[End-to-end example](tutorial.md)** — deploy a workload, watch its profile being learned, trigger an out-of-profile behavior, see the alert, and learn the day-to-day commands, all in one walkthrough.
