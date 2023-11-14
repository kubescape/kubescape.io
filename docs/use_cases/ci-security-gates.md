#### **Scenario**

With the rise of cybersecurity threats, users that are using ArgoCD for Kubernetes orchestration seek to ensure that their Kubernetes clusters, including manifests, Helm charts, and container images, comply with industry security standards and best practices. The development team employs a DevOps approach and uses both direct commits and pull requests to manage changes in their Kubernetes manifest repositories.


## **Objectives**



* To maintain a high security and compliance posture for Kubernetes resources.
* To integrate automated security scanning into the CI/CD pipeline.
* To provide automatic fixes and suggestions for security issues before they are merged into the production codebase.


### Scanning Kubernetes Manifests and Helm Charts

They use Kubescape to scan Kubernetes manifests and Helm charts stored in their version-controlled repositories. Whenever a developer pushes changes, Kubescape runs as part of the CI process and scans the YAML files for misconfigurations and non-compliance against industry standards such as the NSA-CISA, MITRE ATT&CK, and custom Acme policies.


#### Action Points



* Integrate Kubescape scanning into the CI pipeline.
* Configure Kubescape to scan all YAML files upon each commit.


#### Example
Use the following step in your pipeline
```
kubescape scan -f file_name.yaml
```

### Automatically Suggest Fixes for Pull Requests (GitHub Actions)

For changes submitted through pull requests, Kubescape checks the proposed infrastructure changes and automatically suggests fixes for any identified issues. These suggestions appear as comments within the pull request, guiding developers to resolve the issues before merging.


#### Action Points



* Set up Kubescape to comment on pull requests with specific instructions for remediation.


#### Example
To make Kubescape automatically suggest fixes to your pull requests by code review, use the following workflow:
```
name: Suggest autofixes with Kubescape for PR by reviews
on:
  pull_request_target:

jobs:
  kubescape-fix-pr-reviews:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write

    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
        ref: ${{github.event.pull_request.head.ref}}
        repository: ${{github.event.pull_request.head.repo.full_name}}
    - name: Get changed files
      id: changed-files
      uses: tj-actions/changed-files@v35
    - uses: kubescape/github-action@main
      with:
        account: ${{secrets.KUBESCAPE_ACCOUNT}}
        files: ${{ steps.changed-files.outputs.all_changed_files }}
        fixFiles: true
        format: "sarif"
    - name: PR Suggester according to SARIF file
      if: github.event_name == 'pull_request_target'
      uses: HollowMan6/sarif4reviewdog@v1.0.0
      with:
        file: 'results.sarif'
        level: warning
```

### Automatically Suggest Fixes for Direct Commits

When developers make direct commits to the repository, Kubescape scans the changes. If issues are detected, it triggers an automated workflow that creates a new issue in the issue-tracking system, detailing the security findings and recommended fixes.


#### Action Points



* Configure notifications to alert the responsible team members when a new security issue is created.


### Scanning Container Images

They use Kubescape to scan container images for vulnerabilities and misconfigurations as part of their CI pipeline. This ensures that only secure and compliant images are used in their Kubernetes environments.


#### Action Points



* Prevent non-compliant images from being deployed to production environments.


#### Example

##### GitHub Actions
```
name: Kubescape scanning for image vulnerabilities
on: [push, pull_request]
jobs:
  kubescape-scan-image:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    steps:
    - uses: actions/checkout@v3
    - uses: kubescape/github-action@main
      continue-on-error: true
      with:
        image: nginx
        format: sarif
        outputFile: results.sarif
        # severityThreshold: "critical"
        # # Username for a private registry with the image
        # registryUsername: ${{secrets.REGISTRY_USERNAME}}
        # # Password for a private registry with the image
        # registryPassword: ${{secrets.REGISTRY_PASSWORD}}
        # # Fail at or above the specified vulnerability severity threshold
        # Kubescape cloud account ID
        # account: ${{secrets.KUBESCAPE_ACCOUNT}}
    - name: Upload Kubescape scan results to Github Code Scanning
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: results.sarif
```

### Scan Specific File Paths

To optimize scanning and avoid unnecessary checks, Acme configures Kubescape to focus on specific file paths where Kubernetes manifests and Helm charts are stored, avoiding any unrelated directories in the repositories.


#### Action Points



* Set up Kubescape to include and exclude specific directories during the scan.
* Maintain a structured and well-documented repository layout to facilitate targeted scanning.


#### Example
```
kubescape scan -f /path/* 
```

## **Expected Outcome**

By implementing Kubescape in their CI/CD pipeline, Acme Corporation is able to:



* Continuously monitor and enforce security compliance in their Kubernetes infrastructure.
* Quickly identify and remediate security issues before they affect production systems.
* Manitain an agile DevOps workflow that balances speed and security, ensuring neither is compromised at the expense of the other.
* Ensure that developers are educated on security best practices through an automated feedback loop.

Acme's proactive approach to security with Kubescape helps to protect their critical financial services from potential threats and vulnerabilities while maintaining the pace of innovation and deployment required in their competitive industry.
