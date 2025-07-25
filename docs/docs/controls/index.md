# Control library

Below is a list of all controls. Click a control to view its documentation:

- [C-0001](c-0001.md): Forbidden Container Registries
- [C-0002](c-0002.md): Prevent containers from allowing command execution
- [C-0004](c-0004.md): Resources memory limit and request
- [C-0005](c-0005.md): API server insecure port is enabled
- [C-0007](c-0007.md): Roles with delete capabilities
- [C-0009](c-0009.md): Resource limits
- [C-0012](c-0012.md): Applications credentials in configuration files
- [C-0013](c-0013.md): Non-root containers
- [C-0014](c-0014.md): Access Kubernetes dashboard
- [C-0015](c-0015.md): List Kubernetes secrets
- [C-0016](c-0016.md): Allow privilege escalation
- [C-0017](c-0017.md): Immutable container filesystem
- [C-0018](c-0018.md): Configured readiness probe
- [C-0020](c-0020.md): Mount service principal
- [C-0021](c-0021.md): Exposed sensitive interfaces
- [C-0026](c-0026.md): Kubernetes CronJob
- [C-0030](c-0030.md): Ingress and Egress blocked
- [C-0031](c-0031.md): Delete Kubernetes events
- [C-0034](c-0034.md): Automatic mapping of service account
- [C-0035](c-0035.md): Administrative Roles
- [C-0036](c-0036.md): Validate admission controller (validating)
- [C-0037](c-0037.md): CoreDNS poisoning
- [C-0038](c-0038.md): Host PID/IPC privileges
- [C-0039](c-0039.md): Validate admission controller (mutating)
- [C-0041](c-0041.md): HostNetwork access
- [C-0042](c-0042.md): SSH server running inside container
- [C-0044](c-0044.md): Container hostPort
- [C-0045](c-0045.md): Writable hostPath mount
- [C-0046](c-0046.md): Insecure capabilities
- [C-0048](c-0048.md): HostPath mount
- [C-0049](c-0049.md): Network mapping
- [C-0050](c-0050.md): Resources CPU limit and request
- [C-0052](c-0052.md): Instance Metadata API
- [C-0053](c-0053.md): Access container service account
- [C-0054](c-0054.md): Cluster internal networking
- [C-0055](c-0055.md): Linux hardening
- [C-0056](c-0056.md): Configured liveness probe
- [C-0057](c-0057.md): Privileged container
- [C-0058](c-0058.md): CVE-2021-25741 - Using symlink for arbitrary host file system access.
- [C-0059](c-0059.md): CVE-2021-25742-nginx-ingress-snippet-annotation-vulnerability
- [C-0061](c-0061.md): Pods in default namespace
- [C-0062](c-0062.md): Sudo in container entrypoint
- [C-0063](c-0063.md): Portforwarding privileges
- [C-0065](c-0065.md): No impersonation
- [C-0066](c-0066.md): Secret/etcd encryption enabled
- [C-0067](c-0067.md): Audit logs enabled
- [C-0068](c-0068.md): PSP enabled
- [C-0069](c-0069.md): Disable anonymous access to Kubelet service
- [C-0070](c-0070.md): Enforce Kubelet client TLS authentication
- [C-0073](c-0073.md): Naked pods
- [C-0074](c-0074.md): Container runtime socket mounted
- [C-0075](c-0075.md): Image pull policy on latest tag
- [C-0076](c-0076.md): Label usage for resources
- [C-0077](c-0077.md): K8s common labels usage
- [C-0078](c-0078.md): Images from allowed registry
- [C-0079](c-0079.md): CVE-2022-0185-linux-kernel-container-escape
- [C-0081](c-0081.md): CVE-2022-24348-argocddirtraversal
- [C-0083](c-0083.md): Workloads with Critical vulnerabilities exposed to external traffic
- [C-0084](c-0084.md): Workloads with RCE vulnerabilities exposed to external traffic
- [C-0085](c-0085.md): Workloads with excessive amount of vulnerabilities
- [C-0087](c-0087.md): CVE-2022-23648-containerd-fs-escape
- [C-0088](c-0088.md): RBAC enabled
- [C-0089](c-0089.md): CVE-2022-3172-aggregated-API-server-redirect
- [C-0090](c-0090.md): CVE-2022-39328-grafana-auth-bypass
- [C-0091](c-0091.md): CVE-2022-47633-kyverno-signature-bypass
- [C-0092](c-0092.md): Ensure that the API server pod specification file permissions are set to 600 or more restrictive
- [C-0093](c-0093.md): Ensure that the API server pod specification file ownership is set to root:root
- [C-0094](c-0094.md): Ensure that the controller manager pod specification file permissions are set to 600 or more restrictive
- [C-0095](c-0095.md): Ensure that the controller manager pod specification file ownership is set to root:root
- [C-0096](c-0096.md): Ensure that the scheduler pod specification file permissions are set to 600 or more restrictive
- [C-0097](c-0097.md): Ensure that the scheduler pod specification file ownership is set to root:root
- [C-0098](c-0098.md): Ensure that the etcd pod specification file permissions are set to 600 or more restrictive
- [C-0099](c-0099.md): Ensure that the etcd pod specification file ownership is set to root:root
- [C-0100](c-0100.md): Ensure that the Container Network Interface file permissions are set to 600 or more restrictive
- [C-0101](c-0101.md): Ensure that the Container Network Interface file ownership is set to root:root
- [C-0102](c-0102.md): Ensure that the etcd data directory permissions are set to 700 or more restrictive
- [C-0103](c-0103.md): Ensure that the etcd data directory ownership is set to etcd:etcd
- [C-0104](c-0104.md): Ensure that the admin.conf file permissions are set to 600
- [C-0105](c-0105.md): Ensure that the admin.conf file ownership is set to root:root
- [C-0106](c-0106.md): Ensure that the scheduler.conf file permissions are set to 600 or more restrictive
- [C-0107](c-0107.md): Ensure that the scheduler.conf file ownership is set to root:root
- [C-0108](c-0108.md): Ensure that the controller-manager.conf file permissions are set to 600 or more restrictive
- [C-0109](c-0109.md): Ensure that the controller-manager.conf file ownership is set to root:root
- [C-0110](c-0110.md): Ensure that the Kubernetes PKI directory and file ownership is set to root:root
- [C-0111](c-0111.md): Ensure that the Kubernetes PKI certificate file permissions are set to 600 or more restrictive
- [C-0112](c-0112.md): Ensure that the Kubernetes PKI key file permissions are set to 600
- [C-0113](c-0113.md): Ensure that the API Server --anonymous-auth argument is set to false
- [C-0114](c-0114.md): Ensure that the API Server --token-auth-file parameter is not set
- [C-0115](c-0115.md): Ensure that the API Server --DenyServiceExternalIPs is not set
- [C-0116](c-0116.md): Ensure that the API Server --kubelet-client-certificate and --kubelet-client-key arguments are set as appropriate
- [C-0117](c-0117.md): Ensure that the API Server --kubelet-certificate-authority argument is set as appropriate
- [C-0118](c-0118.md): Ensure that the API Server --authorization-mode argument is not set to AlwaysAllow
- [C-0119](c-0119.md): Ensure that the API Server --authorization-mode argument includes Node
- [C-0120](c-0120.md): Ensure that the API Server --authorization-mode argument includes RBAC
- [C-0121](c-0121.md): Ensure that the admission control plugin EventRateLimit is set
- [C-0122](c-0122.md): Ensure that the admission control plugin AlwaysAdmit is not set
- [C-0123](c-0123.md): Ensure that the admission control plugin AlwaysPullImages is set
- [C-0124](c-0124.md): Ensure that the admission control plugin SecurityContextDeny is set if PodSecurityPolicy is not used
- [C-0125](c-0125.md): Ensure that the admission control plugin ServiceAccount is set
- [C-0126](c-0126.md): Ensure that the admission control plugin NamespaceLifecycle is set
- [C-0127](c-0127.md): Ensure that the admission control plugin NodeRestriction is set
- [C-0128](c-0128.md): Ensure that the API Server --secure-port argument is not set to 0
- [C-0129](c-0129.md): Ensure that the API Server --profiling argument is set to false
- [C-0130](c-0130.md): Ensure that the API Server --audit-log-path argument is set
- [C-0131](c-0131.md): Ensure that the API Server --audit-log-maxage argument is set to 30 or as appropriate
- [C-0132](c-0132.md): Ensure that the API Server --audit-log-maxbackup argument is set to 10 or as appropriate
- [C-0133](c-0133.md): Ensure that the API Server --audit-log-maxsize argument is set to 100 or as appropriate
- [C-0134](c-0134.md): Ensure that the API Server --request-timeout argument is set as appropriate
- [C-0135](c-0135.md): Ensure that the API Server --service-account-lookup argument is set to true
- [C-0136](c-0136.md): Ensure that the API Server --service-account-key-file argument is set as appropriate
- [C-0137](c-0137.md): Ensure that the API Server --etcd-certfile and --etcd-keyfile arguments are set as appropriate
- [C-0138](c-0138.md): Ensure that the API Server --tls-cert-file and --tls-private-key-file arguments are set as appropriate
- [C-0139](c-0139.md): Ensure that the API Server --client-ca-file argument is set as appropriate
- [C-0140](c-0140.md): Ensure that the API Server --etcd-cafile argument is set as appropriate
- [C-0141](c-0141.md): Ensure that the API Server --encryption-provider-config argument is set as appropriate
- [C-0142](c-0142.md): Ensure that encryption providers are appropriately configured
- [C-0143](c-0143.md): Ensure that the API Server only makes use of Strong Cryptographic Ciphers
- [C-0144](c-0144.md): Ensure that the Controller Manager --terminated-pod-gc-threshold argument is set as appropriate
- [C-0145](c-0145.md): Ensure that the Controller Manager --profiling argument is set to false
- [C-0146](c-0146.md): Ensure that the Controller Manager --use-service-account-credentials argument is set to true
- [C-0147](c-0147.md): Ensure that the Controller Manager --service-account-private-key-file argument is set as appropriate
- [C-0148](c-0148.md): Ensure that the Controller Manager --root-ca-file argument is set as appropriate
- [C-0149](c-0149.md): Ensure that the Controller Manager RotateKubeletServerCertificate argument is set to true
- [C-0150](c-0150.md): Ensure that the Controller Manager --bind-address argument is set to 127.0.0.1
- [C-0151](c-0151.md): Ensure that the Scheduler --profiling argument is set to false
- [C-0152](c-0152.md): Ensure that the Scheduler --bind-address argument is set to 127.0.0.1
- [C-0153](c-0153.md): Ensure that the --cert-file and --key-file arguments are set as appropriate
- [C-0154](c-0154.md): Ensure that the --client-cert-auth argument is set to true
- [C-0155](c-0155.md): Ensure that the --auto-tls argument is not set to true
- [C-0156](c-0156.md): Ensure that the --peer-cert-file and --peer-key-file arguments are set as appropriate
- [C-0157](c-0157.md): Ensure that the --peer-client-cert-auth argument is set to true
- [C-0158](c-0158.md): Ensure that the --peer-auto-tls argument is not set to true
- [C-0159](c-0159.md): Ensure that a unique Certificate Authority is used for etcd
- [C-0160](c-0160.md): Ensure that a minimal audit policy is created
- [C-0161](c-0161.md): Ensure that the audit policy covers key security concerns
- [C-0162](c-0162.md): Ensure that the kubelet service file permissions are set to 600 or more restrictive
- [C-0163](c-0163.md): Ensure that the kubelet service file ownership is set to root:root
- [C-0164](c-0164.md): If proxy kubeconfig file exists ensure permissions are set to 600 or more restrictive
- [C-0165](c-0165.md): If proxy kubeconfig file exists ensure ownership is set to root:root
- [C-0166](c-0166.md): Ensure that the --kubeconfig kubelet.conf file permissions are set to 600 or more restrictive
- [C-0167](c-0167.md): Ensure that the --kubeconfig kubelet.conf file ownership is set to root:root
- [C-0168](c-0168.md): Ensure that the certificate authorities file permissions are set to 600 or more restrictive
- [C-0169](c-0169.md): Ensure that the client certificate authorities file ownership is set to root:root
- [C-0170](c-0170.md): If the kubelet config.yaml configuration file is being used validate permissions set to 600 or more restrictive
- [C-0171](c-0171.md): If the kubelet config.yaml configuration file is being used validate file ownership is set to root:root
- [C-0172](c-0172.md): Ensure that the --anonymous-auth argument is set to false
- [C-0173](c-0173.md): Ensure that the --authorization-mode argument is not set to AlwaysAllow
- [C-0174](c-0174.md): Ensure that the --client-ca-file argument is set as appropriate
- [C-0175](c-0175.md): Verify that the --read-only-port argument is set to 0
- [C-0176](c-0176.md): Ensure that the --streaming-connection-idle-timeout argument is not set to 0
- [C-0177](c-0177.md): Ensure that the --protect-kernel-defaults argument is set to true
- [C-0178](c-0178.md): Ensure that the --make-iptables-util-chains argument is set to true
- [C-0179](c-0179.md): Ensure that the --hostname-override argument is not set
- [C-0180](c-0180.md): Ensure that the --event-qps argument is set to 0 or a level which ensures appropriate event capture
- [C-0181](c-0181.md): Ensure that the --tls-cert-file and --tls-private-key-file arguments are set as appropriate
- [C-0182](c-0182.md): Ensure that the --rotate-certificates argument is not set to false
- [C-0183](c-0183.md): Verify that the RotateKubeletServerCertificate argument is set to true
- [C-0184](c-0184.md): Ensure that the Kubelet only makes use of Strong Cryptographic Ciphers
- [C-0185](c-0185.md): Ensure that the cluster-admin role is only used where required
- [C-0186](c-0186.md): Minimize access to secrets
- [C-0187](c-0187.md): Minimize wildcard use in Roles and ClusterRoles
- [C-0188](c-0188.md): Minimize access to create pods
- [C-0189](c-0189.md): Ensure that default service accounts are not actively used
- [C-0190](c-0190.md): Ensure that Service Account Tokens are only mounted where necessary
- [C-0191](c-0191.md): Limit use of the Bind, Impersonate and Escalate permissions in the Kubernetes cluster
- [C-0192](c-0192.md): Ensure that the cluster has at least one active policy control mechanism in place
- [C-0193](c-0193.md): Minimize the admission of privileged containers
- [C-0194](c-0194.md): Minimize the admission of containers wishing to share the host process ID namespace
- [C-0195](c-0195.md): Minimize the admission of containers wishing to share the host IPC namespace
- [C-0196](c-0196.md): Minimize the admission of containers wishing to share the host network namespace
- [C-0197](c-0197.md): Minimize the admission of containers with allowPrivilegeEscalation
- [C-0198](c-0198.md): Minimize the admission of root containers
- [C-0199](c-0199.md): Minimize the admission of containers with the NET_RAW capability
- [C-0200](c-0200.md): Minimize the admission of containers with added capabilities
- [C-0201](c-0201.md): Minimize the admission of containers with capabilities assigned
- [C-0202](c-0202.md): Minimize the admission of Windows HostProcess Containers
- [C-0203](c-0203.md): Minimize the admission of HostPath volumes
- [C-0204](c-0204.md): Minimize the admission of containers which use HostPorts
- [C-0205](c-0205.md): Ensure that the CNI in use supports Network Policies
- [C-0206](c-0206.md): Ensure that all Namespaces have Network Policies defined
- [C-0207](c-0207.md): Prefer using secrets as files over secrets as environment variables
- [C-0208](c-0208.md): Consider external secret storage
- [C-0209](c-0209.md): Create administrative boundaries between resources using namespaces
- [C-0210](c-0210.md): Ensure that the seccomp profile is set to docker/default in your pod definitions
- [C-0211](c-0211.md): Apply Security Context to Your Pods and Containers
- [C-0212](c-0212.md): The default namespace should not be used
- [C-0213](c-0213.md): Minimize the admission of privileged containers
- [C-0214](c-0214.md): Minimize the admission of containers wishing to share the host process ID namespace
- [C-0215](c-0215.md): Minimize the admission of containers wishing to share the host IPC namespace
- [C-0216](c-0216.md): Minimize the admission of containers wishing to share the host network namespace
- [C-0217](c-0217.md): Minimize the admission of containers with allowPrivilegeEscalation
- [C-0218](c-0218.md): Minimize the admission of root containers
- [C-0219](c-0219.md): Minimize the admission of containers with added capabilities
- [C-0220](c-0220.md): Minimize the admission of containers with capabilities assigned
- [C-0221](c-0221.md): Ensure Image Vulnerability Scanning using Amazon ECR image scanning or a third party provider
- [C-0222](c-0222.md): Minimize user access to Amazon ECR
- [C-0223](c-0223.md): Minimize cluster access to read-only for Amazon ECR
- [C-0225](c-0225.md): Prefer using dedicated EKS Service Accounts
- [C-0226](c-0226.md): Prefer using a container-optimized OS when possible
- [C-0227](c-0227.md): Restrict Access to the Control Plane Endpoint
- [C-0228](c-0228.md): Ensure clusters are created with Private Endpoint Enabled and Public Access Disabled
- [C-0229](c-0229.md): Ensure clusters are created with Private Nodes
- [C-0230](c-0230.md): Ensure Network Policy is Enabled and set as appropriate
- [C-0231](c-0231.md): Encrypt traffic to HTTPS load balancers with TLS certificates
- [C-0232](c-0232.md): Manage Kubernetes RBAC users with AWS IAM Authenticator for Kubernetes or Upgrade to AWS CLI v1.16.156
- [C-0233](c-0233.md): Consider Fargate for running untrusted workloads
- [C-0234](c-0234.md): Consider external secret storage
- [C-0235](c-0235.md): Ensure that the kubelet configuration file has permissions set to 644 or more restrictive
- [C-0236](c-0236.md): Verify image signature
- [C-0237](c-0237.md): Check if signature exists
- [C-0238](c-0238.md): Ensure that the kubeconfig file permissions are set to 644 or more restrictive
- [C-0239](c-0239.md): Prefer using dedicated AKS Service Accounts
- [C-0240](c-0240.md): Ensure Network Policy is Enabled and set as appropriate
- [C-0241](c-0241.md): Use Azure RBAC for Kubernetes Authorization.
- [C-0242](c-0242.md): Hostile multi-tenant workloads
- [C-0243](c-0243.md): Ensure Image Vulnerability Scanning using Azure Defender image scanning or a third party provider
- [C-0244](c-0244.md): Ensure Kubernetes Secrets are encrypted
- [C-0245](c-0245.md): Encrypt traffic to HTTPS load balancers with TLS certificates
- [C-0246](c-0246.md): Avoid use of system:masters group
- [C-0247](c-0247.md): Restrict Access to the Control Plane Endpoint
- [C-0248](c-0248.md): Ensure clusters are created with Private Nodes
- [C-0249](c-0249.md)
- [C-0250](c-0250.md): Minimize cluster access to read-only for Azure Container Registry (ACR)
- [C-0251](c-0251.md): Minimize user access to Azure Container Registry (ACR)
- [C-0252](c-0252.md): Ensure clusters are created with Private Endpoint Enabled and Public Access Disabled
- [C-0253](c-0253.md): Deprecated Kubernetes image registry
- [C-0254](c-0254.md): Enable audit Logs
- [C-0255](c-0255.md): Workload with secret access
- [C-0256](c-0256.md): External facing
- [C-0257](c-0257.md): Workload with PVC access
- [C-0258](c-0258.md): Workload with ConfigMap access
- [C-0259](c-0259.md): Workload with credential access
- [C-0260](c-0260.md): Missing network policy
- [C-0261](c-0261.md): ServiceAccount token mounted
- [C-0262](c-0262.md): Anonymous user has RoleBinding
- [C-0263](c-0263.md): Ingress uses TLS
- [C-0264](c-0264.md): PersistentVolume without encyption
- [C-0265](c-0265.md): system:authenticated user has elevated roles
- [C-0266](c-0266.md): Exposure to internet via Gateway API or Istio Ingress
- [C-0267](c-0267.md): Workload with cluster takeover roles
- [C-0268](c-0268.md): Ensure CPU requests are set
- [C-0269](c-0269.md): Ensure memory requests are set
- [C-0270](c-0270.md): Ensure CPU limits are set
- [C-0271](c-0271.md): Ensure memory limits are set
- [C-0272](c-0272.md): Workload with administrative roles
- [C-0273](c-0273.md): Outdated Kubernetes version
- [C-0274](c-0274.md): Verify Authenticated Service
- [C-0275](c-0275.md): Minimize the admission of containers wishing to share the host process ID namespace
- [C-0276](c-0276.md): Minimize the admission of containers wishing to share the host IPC namespace
- [C-0277](c-0277.md): Ensure that the API Server only makes use of Strong Cryptographic Ciphers
- [C-0278](c-0278.md): Minimize access to create persistent volumes
- [C-0279](c-0279.md): Minimize access to the proxy sub-resource of nodes
- [C-0280](c-0280.md): Minimize access to the approval sub-resource of certificatesigningrequests objects
- [C-0281](c-0281.md): Minimize access to webhook configuration objects
- [C-0282](c-0282.md): Minimize access to the service account token creation
- [C-0283](c-0283.md): Ensure that the API Server --DenyServiceExternalIPs is set
- [C-0284](c-0284.md): Ensure that the Kubelet is configured to limit pod PIDS

