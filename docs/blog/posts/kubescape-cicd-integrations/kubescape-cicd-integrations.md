---
date: 2026-06-09
categories:
  - CI/CD
authors:
  - ivaresarthak-cloud
slug: 'kubescape-cicd-integrations'
---

# Integrating Kubescape into Your CI/CD Pipeline

Kubernetes security should not be an afterthought. By integrating Kubescape into your CI/CD pipeline, you can catch misconfigurations and compliance violations before they reach production. This post walks through how to add Kubescape to the three most common CI/CD platforms: GitHub Actions, GitLab CI/CD, and Jenkins.

## Why Shift Security Left?

Every misconfiguration that reaches a production cluster costs more to fix than one caught during a pull request. Kubescape scans your Kubernetes manifests, Helm charts, and Kustomize configurations against security frameworks including NSA-CISA, MITRE ATT&CK, and CIS Benchmarks — and it runs in seconds. Adding it to your pipeline means every commit is checked automatically.

## GitHub Actions

GitHub Actions is the most common CI/CD platform for open source projects. Kubescape integrates natively via the [kubescape/github-action](https://github.com/kubescape/github-action) and also supports SARIF output for GitHub's native Code Scanning dashboard.

### Basic workflow

```yaml
name: Kubescape

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  kubescape:
    name: Scan Kubernetes manifests
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Kubescape
        run: |
          curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | bash
          echo "$HOME/.kubescape/bin" >> "$GITHUB_PATH"

      - name: Run Kubescape scan
        run: |
          kubescape scan . \
            --format sarif \
            --output results.sarif
        continue-on-error: true

      - name: Upload SARIF to GitHub Code Scanning
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
```

The SARIF upload pushes every finding directly into the **Security → Code scanning** tab of your repository, where you can triage, dismiss, and track alerts over time. For a full guide including compliance thresholds and branch protection rules, see the [GitHub Code Scanning integration guide](https://github.com/kubescape/kubescape/blob/master/docs/github-code-scanning.md).

## GitLab CI/CD

For GitLab, Kubescape fits naturally into a `.gitlab-ci.yml` pipeline. The example below runs on every push and merge request:

```yaml
kubescape:
  image: ubuntu:22.04
  stage: test
  before_script:
    - apt-get update -qq && apt-get install -y -qq curl
    - curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | bash
    - export PATH=$PATH:$HOME/.kubescape/bin
  script:
    - kubescape scan framework nsa . --format pretty-printer --compliance-threshold 80
  allow_failure: true
```

Set `allow_failure: false` to block merge requests that fall below your compliance threshold. Note: `--compliance-threshold` only takes effect with `scan framework <name>` or `--view resource|control` — a plain `kubescape scan .` exits 0 regardless of score. For a full guide including framework-specific scans and troubleshooting, see the [GitLab CI/CD integration guide](https://github.com/kubescape/kubescape/blob/master/docs/gitlab-ci.md).

## Jenkins

Jenkins users can add a Kubescape scan stage to any declarative pipeline. The example below runs after the build stage and archives the scan output as a build artifact:

```groovy
pipeline {
    agent { label 'linux' }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Kubescape Scan') {
            steps {
                sh '''
                    curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | bash
                    export PATH=$PATH:$HOME/.kubescape/bin
                    kubescape scan framework nsa . \
                        --format sarif \
                        --output results.sarif \
                        --compliance-threshold 80
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'results.sarif', allowEmptyArchive: true
        }
    }
}
```

For a full guide including multi-branch pipelines and failure handling, see the [Jenkins integration guide](https://github.com/kubescape/kubescape/blob/master/docs/jenkins.md).

## Choosing the Right Framework

Kubescape supports several security frameworks out of the box:

| Framework | Use case |
|---|---|
| `nsa` | NSA-CISA Kubernetes Hardening Guidance |
| `mitre` | MITRE ATT&CK for Kubernetes |
| `cis-v1.23-t1.0.1` | CIS Kubernetes Benchmark |

Run `kubescape list frameworks` to see the full list available in your installation.

To scan against a specific framework, pass it as a subcommand:

```bash
kubescape scan framework nsa ./k8s/
```

## What's Next

The Kubescape team is working on a [Harbor scanner adapter](https://github.com/Onyx2406/harbor-scanner-kubescape) that will allow Harbor to use Kubescape as a pluggable scanner alongside Trivy and Clair — bringing the same misconfiguration and vulnerability scanning directly into your container registry workflow. Stay tuned for a dedicated guide once the adapter is accepted by the Harbor project.

In the meantime, pick the platform that matches your stack, add Kubescape to your pipeline, and start catching misconfigurations before they reach production.
