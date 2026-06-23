# Integrating with GitLab CI/CD

Use GitLab CI/CD to scan Kubernetes manifests, Helm charts, or other workload configuration files with Kubescape whenever a merge request is opened or the default branch is updated. The examples below install the Kubescape CLI in the job, run a scan, and publish JUnit results back to GitLab.

## Prerequisites

* A GitLab project with GitLab CI/CD enabled.
* A GitLab Runner with network access to GitHub, so it can download the Kubescape install script.
* Kubernetes manifest, Helm chart, or other workload files in the repository.

## Basic pipeline

Create a `.gitlab-ci.yml` file in the root of your repository:

```yaml
stages:
  - scan

kubescape:
  stage: scan
  image: alpine:latest
  before_script:
    - apk add --no-cache bash curl gcompat
    - curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
    - export PATH="$PATH:$HOME/.kubescape/bin"
  script:
    - kubescape scan . --format junit --output results.xml
  artifacts:
    when: always
    reports:
      junit: results.xml
    paths:
      - results.xml
    expire_in: 30 days
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

The job scans the current repository path and uploads `results.xml` as a GitLab test report.

## Add a security gate

Use `--compliance-threshold` when you want the job to fail if the compliance score is below a required percentage. The threshold applies to framework and control scans, and to resource or control views.

```yaml
stages:
  - scan

kubescape:
  stage: scan
  image: alpine:latest
  before_script:
    - apk add --no-cache bash curl gcompat
    - curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
    - export PATH="$PATH:$HOME/.kubescape/bin"
  script:
    - kubescape scan framework nsa . --format junit --output results.xml --compliance-threshold 80
  artifacts:
    when: always
    reports:
      junit: results.xml
    paths:
      - results.xml
    expire_in: 30 days
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

This job fails when the NSA framework compliance score is lower than 80%.

## Scan a specific framework

To scan against a specific compliance framework, pass the framework name to `kubescape scan framework`:

```yaml
script:
  - kubescape scan framework nsa . --format junit --output results.xml
```

Common frameworks include `nsa`, `mitre`, and `cis-v1.23-t1.0.1`. Run `kubescape list frameworks` for the complete list supported by your installed Kubescape version.

## Troubleshooting

### `kubescape: command not found`

Make sure the Kubescape binary directory is added to `PATH` before running the scan:

```yaml
before_script:
  - curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
  - export PATH="$PATH:$HOME/.kubescape/bin"
```

### The threshold does not fail the job

The default `kubescape scan [path]` command uses the security view. For score-based gates, use a framework scan, a control scan, or `--view resource`/`--view control`.

```sh
kubescape scan framework nsa . --compliance-threshold 80
kubescape scan --view resource . --compliance-threshold 80
```

## Further reading

* [Scanning your environment](../scanning.md)
* [Frameworks](../frameworks-and-controls/frameworks.md)
* [GitLab CI/CD pipelines](https://docs.gitlab.com/ci/pipelines/)
