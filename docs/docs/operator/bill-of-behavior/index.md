# Bill of Behavior

A **Software Bill of Behavior (SBOB)** is a declarative and **abstracted** profile of what a workload is *intended* to do at runtime — the processes it spawns, the files it opens, the network destinations it reaches, and the Linux capabilities it requests.

Where a Software Bill of Materials (SBOM) describes what a workload is *made of*, a Software Bill of Behavior describes what it is *meant to do*. The SBOM is the ingredient list; the SBOB is the package insert. Anything a workload does at runtime that the SBOB does not declare is: `undesired` :
Either it points to a vendor bug and/or respectively a vendor's lack of testing the SBOB (`False Positive`), or a malicious compromise (`True Positive`).

## Validating an SBOB in your environment
To tell the difference between the *SBOB* being inadequate and there being an actual attack, it is highly recommended to run the workload with a new SBOB in a
non-productive environment under a standard test-suite.
We are actively working on providing `validation tests` for common CNCF projects to make this *contrast* between `False` and `True` Positives more achievable.

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
- **Profile compaction** via a `CollapseConfig`, folding many concrete observations into a smaller, maintainable profile — see [Profile size &amp; performance](profile-size-and-performance.md) for what it saves.
- **Signing and tamper detection** ([R1016](../node-agent-rule-library.md)), so a user-supplied profile can be cryptographically verified and any later modification is detected at runtime — see [Signing &amp; tamper detection](signing-and-tamper.md).

## Next

See **[End-to-end example](tutorial.md)** — deploy a workload, watch its profile being learned, trigger an out-of-profile behavior, see the alert, and learn the day-to-day commands, all in one walkthrough.
