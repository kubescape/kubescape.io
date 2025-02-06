# Kubescape Operator vs CLI: Comparison and Functionality

The Kubescape Operator and Kubescape CLI are two different tools provided by Kubescape for securing Kubernetes environments. Here's a comparison of their functionalities and differences based on the provided documentation.

---

## **Kubescape Operator**

The Kubescape Operator is designed to integrate Kubescape's security capabilities directly into Kubernetes clusters, providing continuous security monitoring and enforcement.

### **Key Features:**

1. **Automated Scanning:**
   - Continuously scans Kubernetes resources (e.g., workloads, configurations) for misconfigurations and vulnerabilities.
   - Runs scans on a schedule or in response to changes in the cluster.

2. **Cluster Integration:**
   - Deployed as a Kubernetes Operator, meaning it runs inside the cluster and manages security tasks natively.
   - Monitors resources in real-time and enforces security policies.

3. **Policy Enforcement:**
   - Applies predefined or custom security policies to ensure compliance with frameworks like NSA-CISA, MITRE ATT&CK, and others.
   - Can block or alert on non-compliant resources.

4. **Reporting and Alerts:**
   - Provides detailed reports on security risks and compliance status.
   - Integrates with external tools (e.g., Prometheus, Slack) for alerts and notifications.

5. **Remediation Guidance:**
   - Offers actionable recommendations to fix identified issues.

6. **Multi-Cluster Support:**
   - Can manage and secure multiple Kubernetes clusters from a single control plane.

7. **Customization:**
   - Allows users to define custom policies and exceptions tailored to their environment.

### **Use Cases:**
- Continuous security monitoring for production clusters.
- Enforcing compliance with organizational or regulatory standards.
- Automating security tasks within Kubernetes.

---

## **Kubescape CLI**

The Kubescape CLI is a command-line tool that allows users to scan Kubernetes manifests, Helm charts, and running clusters for security issues from their local machine or CI/CD pipelines.

### **Key Features:**

1. **On-Demand Scanning:**
   - Scans Kubernetes YAML files, Helm charts, and live clusters for misconfigurations and vulnerabilities.
   - Can be run manually or integrated into CI/CD pipelines.

2. **Framework Compliance:**
   - Checks configurations against security frameworks like NSA-CISA, MITRE ATT&CK, and others.
   - Provides a compliance score for scanned resources.

3. **Local and Remote Scanning:**
   - Can scan local files or connect to a running cluster for analysis.

4. **Output Formats:**
   - Supports multiple output formats (e.g., JSON, JUnit, PDF) for integration with other tools.
   - Provides detailed reports with remediation guidance.

5. **Custom Policies:**
   - Allows users to define and apply custom policies for specific requirements.

6. **Ease of Use:**
   - Lightweight and easy to install, making it ideal for developers and DevOps teams.
   - Can be used in local development or CI/CD workflows.

7. **Remediation Guidance:**
   - Offers actionable recommendations to fix identified issues.

### **Use Cases:**
- Scanning Kubernetes manifests and Helm charts during development.
- Integrating security checks into CI/CD pipelines.
- Performing ad-hoc security assessments of clusters.

---

## **Key Differences**

| **Feature**                | **Kubescape Operator**                          | **Kubescape CLI**                          |
|----------------------------|------------------------------------------------|-------------------------------------------|
| **Deployment**             | Runs inside the cluster as a Kubernetes Operator. | Runs locally or in CI/CD pipelines.       |
| **Scanning**               | Continuous, automated scanning of the cluster.  | On-demand scanning of files or clusters.  |
| **Real-Time Monitoring**   | Yes, monitors resources in real-time.           | No, requires manual execution.            |
| **Policy Enforcement**     | Enforces policies automatically in the cluster. | Provides reports but does not enforce.    |
| **Integration**            | Integrates with cluster-native tools (e.g., Prometheus). | Integrates with CI/CD tools and local workflows. |
| **Use Case**               | Continuous security for production clusters.    | Development, CI/CD, and ad-hoc scanning.  |
| **Multi-Cluster Support**  | Yes, can manage multiple clusters.              | Limited to single-cluster or local scans. |

---

## **Functionality Comparison**

- **Operator:** Focuses on continuous, automated security and compliance within the cluster. It is ideal for production environments where real-time monitoring and enforcement are critical.
- **CLI:** Focuses on on-demand scanning and integration into development workflows. It is ideal for developers and DevOps teams who need to ensure security during the development and deployment process.

---

## **When to Use Which?**

- Use the **Kubescape Operator** if you need continuous security monitoring and enforcement in a production Kubernetes environment.
- Use the **Kubescape CLI** if you need to scan Kubernetes manifests, Helm charts, or clusters during development or as part of CI/CD pipelines.

Both tools complement each other and can be used together for end-to-end Kubernetes security.
