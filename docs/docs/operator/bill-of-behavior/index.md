# Bill of Behavior

A **Software Bill of Behavior (SBOB)** is a declarative and **abstracted** profile of what a workload is *intended* to do at runtime — the processes it spawns, the files it opens, the network destinations it reaches, and the Linux capabilities it requests.

Where an SBOM describes what a workload is *made of*, an SBOB describes what it is *meant to do*. The SBOM is the ingredient list; the SBOB is the package insert. 

Anything a workload does at runtime that the SBOB does not declare is `undesired`. Either  
- it points to a bug: lack of testing the software and/or the SBOB (`False Positive`), or  
- it points to a malicious compromise (`True Positive`).

In **[the SBOB log4j example](quickstart.md)**, you can try it out yourself.

## Validating an SBOB in your environment
To tell the difference between the *SBOB* being inadequate and there being an actual attack, it is highly recommended to run the workload with a new SBOB in a
non-productive environment under a standard test-suite.
We are working on providing `validation tests` for common CNCF projects to make this *contrast* between `False` and `True` Positives more achievable.

## How Kubescape is a reference implementation

Kubescape implements the SBOB end to end, using eBPF to observe workloads at the Linux ABI and Kubernetes custom resources to store the declaration, it allows signing the YAMLs and it detects tampering.[^migration]


[^migration]: The first implementation currently relies on the CRDs `ApplicationProfile`
    and `NetworkNeighborhood`, but we will migrate them to `ContainerProfile` asap.
    The functionality itself will not be affected.

    Currently, you need to apply the CRD to the cluster before the workload and ensure
    the labels are correct.

## Beyond learned profiles, a note on Usability

Kubescape-node-agent can learn a profile and it is important to note, that the learning feature is `OFF` for SBOBs.

You can however use a learnt profile and convert it to an SBOB. You do this by reducing it to translatable and deterministic content.
For this, we implemented two major concepts.

- **Wildcards** in exec arguments, file paths, and network destinations (CIDRs and DNS-label patterns), so a profile describes a *class* of behavior rather than one observed instance.
- **Plurals** for network destinations (CIDRs and DNS-label patterns): A learnt profile usually contains a specific IP, whereas it might be part of a range. E.g. `pod-cidr` or `services-cidr` for internal and `vendor ip-list` for external endpoints.[^ct]

[^ct]: Please see the component test of node-agent for a full set of examples.

## What can be tampered with, must be signed

Config, CEL rules and SBOBs determine how the detection behaves. Excluding a namespace is as dangerous as allowlisting a new binary in a profile.
Thus, we have the `experimental` feature:

- **Signing and tamper detection** ([R1016](../node-agent-rule-library.md)), so it can be cryptographically verified and any later modification is detected at runtime — see [Signing &amp; tamper detection](signing-and-tamper.md).

## Next

See **[End-to-end example](quickstart.md)** — deploy a workload, watch its profile being learned, trigger an out-of-profile behavior, see the alert, and learn the day-to-day commands, all in one walkthrough.
