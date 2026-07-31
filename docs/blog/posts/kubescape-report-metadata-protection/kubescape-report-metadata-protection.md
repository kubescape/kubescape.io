---
date: 2026-07-24
categories:
  - Announcements
  - Project
authors:
  - jijo-OO7
slug: "kubescape-report-metadata-protection"
---

# Protecting Sensitive Metadata in Kubescape Reports

The Kubescape community is excited to introduce **report metadata protection**, a new capability that helps users safely share Kubescape scan reports without exposing sensitive infrastructure details.

This feature introduces two new mechanisms:

- **`--hide`** for deterministic metadata pseudonymization
- **`--encrypt`** for reversible metadata encryption, together with the new **`kubescape decrypt`** command

Whether you're sharing reports across teams, collaborating with customers, or publishing security findings, Kubescape now makes it easier to protect sensitive metadata while preserving the value of the security analysis.

---

## A Quick Background: Why It Was Needed

Kubescape reports often contain metadata such as Kubernetes resource names, namespaces, repository metadata, source paths, annotations, and other identifiers that can reveal details about an organization's internal infrastructure.

While this metadata is valuable during security investigations, it isn't always appropriate to expose when reports are shared outside a trusted environment.

Until now, users had to choose between sharing complete reports or manually removing sensitive information before distribution.

With report metadata protection, Kubescape now provides built-in mechanisms to protect this information while preserving the rest of the security findings.

---

## Why It Matters

Report metadata protection allows organizations to safely share security reports without unnecessarily exposing sensitive identifiers.

This means:

* **Deterministic pseudonymization** using `--hide` for reports that need consistent identifiers while reducing incidental exposure
* **Strong metadata encryption** using `--encrypt` when confidentiality is required
* **Metadata restoration** through the new `kubescape decrypt` command when authorized users need access to the original information
* Protection of sensitive metadata while preserving the complete security analysis and scan results

---

## How to Use It

The following examples demonstrate the three primary workflows supported by report metadata protection.

Generate a report with pseudonymized metadata:

```bash
kubescape scan --hide --format json --output report.json
```

Generate a report with encrypted metadata:

```bash
# The key is used as raw bytes and must be exactly 32 bytes (32 ASCII characters) long.
# Replace the placeholder below with your own unique key and store it securely.
# Note: `openssl rand -base64 32` (44 chars) and `openssl rand -hex 32` (64 chars)
# are NOT valid—they exceed 32 bytes once passed through as raw text.
export KUBESCAPE_MASTER_KEY="<your-32-byte-master-key>"

kubescape scan \
  --encrypt \
  --format json \
  --output encrypted-report.json
```

Restore encrypted metadata:

```bash
# Use the same 32-byte key that was used with `kubescape scan --encrypt`,
# retrieved securely from where you stored it.
export KUBESCAPE_MASTER_KEY="<your-32-byte-master-key>"

kubescape decrypt encrypted-report.json > decrypted-report.json
```

When both `--hide` and `--encrypt` are specified, encryption takes precedence.

---

## What’s Next?

Report metadata protection is another step toward making Kubescape security reports easier to share across teams while respecting organizational confidentiality requirements.

We look forward to seeing how the community uses this capability in CI/CD pipelines, security assessments, compliance workflows, and collaborative security reviews.

If you have feedback or ideas for future improvements, we'd love to hear from you on [GitHub](https://github.com/kubescape/kubescape/issues) or [Discussions](https://github.com/kubescape/kubescape/discussions).
