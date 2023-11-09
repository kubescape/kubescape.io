#### **Scenario**

Development teams are looking to incorporate security practices early in the software devlopment lifecycle. By integrating Kubescape into their local development environments, they can scan Kubernetes manifests, Helm charts, and container images for security misconfigurations and vulnerabilities before these elements are committed to version control or reach the CI/CD pipeline.


## **Why Integrate Kubescape?**



* **Preventative Security:** Integrating Kubescape early in the development process allows teams to catch and remediate security issues before they escalate into larger problems in production.
* **Shift-Left Culture:** It fosters a security-conscious culture where developers are equipped to address security as an integral part of the development lifecycle, not an afterthought.
* **Cost Efficiency:** Resolving issues early is far less costly and time-consuming than addressing them after deployment, where they might disrupt operations or require more complex mitigation strategies.
* **Compliance Assurance:** Early scanning helps ensure that the developed applications comply with regulatory requirements and organizational security policies from the start.
* **Automation and Consistency:** Automated scanning with integrated tools reduces the likelihood of human error and maintains consistency in security practices across the development team.


## **Available Integrations**



1. Visual Studio Code Plugin:
    * Developers can use the Kubescape VS Code extension to scan Kubernetes manifests and Helm charts directly within their IDE.
    * The extension provides immediate feedback on potential security risks, offering suggestions and fixes as code is being written.
2. Docker Desktop Extension:
    * With the Docker Desktop extension, developers can scan container images for vulnerabilities during the build process.
    * It enables them to update Dockerfiles with secure base images and avoid using versions of images that contain known vulnerabilities.
3. Lens Extension:
    * The Lens extension for Kubescape allows developers to scan Kubernetes clusters directly from the Lens IDE.
    * This is particularly useful for ensuring that the Kubernetes configurations and runtime environment adhere to best practices and are free from misconfigurations.
4. Command-Line Interface (CLI):
    * The CLI allows developers to run Kubescape against local manifest files as part of their pre-commit or pre-push git hooks, ensuring scans are performed automatically before code is contributed to the repository.
    * It can also be incorporated into scripts or manual processes that are part of the developer's workflow.


## **Expected Outcome**



* Security scans are a regular part of the development workflow, occurring in real-time as code is written and applications are containerized.
* Developers are immediately aware of security issues and can address them promptly, significantly reducing the risk of vulnerabilities reaching production.
* The development lifecycle includes a standardized and automated approach to security, leading to a robust and secure end product.


## **Call to Action (CTA) for Users**


### Embed Security Into Your Workflow



* Integrate Kubescape into your IDE and local development environments to proactively address security concerns.
* Utilize Kubescape's extensions and plugins to ensure that your Kubernetes resources are secure by design.
* Embrace proactive hardening by incorporating Kubescape scans into your daily development practices.


## **What’s Next?**



* Regularly update your local Kubescape tooling to benefit from the latest vulnerability databases and scanning capabilities.
* Collaborate with your security team to tailor Kubescape's scanning policies to match organizational security requirements.
* Share knowledge and best practices with your team to cultivate a shared responsibility model for security within your development process.