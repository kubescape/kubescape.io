# Connecting to providers

A provider is a service which sends and receives data from Kubescape.  To configure a provider with Kubescape, you must provide its server URL and your account ID on that service.

With a configured provider, you can download artifacts (custom frameworks, controls, attack tracks and configurations), and upload scan results.

## Compatible providers

* [ARMO Platform](https://cloud.armosec.io/account/sign-up?utm_source=kubescapeio) is an enterprise solution based on Kubescape. It’s a multi-cloud and multi-cluster Kubernetes and CI/CD security platform behind a single pane of glass. ARMO Platform includes Kubernetes hardening and compliance assistance, misconfiguration scanning and remediation, prioritized container image vulnerability reporting, an RBAC investigator and more. Using ARMO Platform, you will save valuable time and make spot-on hardening decisions with contextual insights, based on the data from your scans and environment.

_To add your own provider here, [send a pull request](https://github.com/kubescape/kubescape.io/)._

## Configuring a provider

### In the Kubescape client

You can save configuration data for providers with `kubescape config`:

```sh
kubescape config set server <server URL>
kubescape config set accountID <accountID>
```

You can override this configuration wtih `--account <accountID>` and `--server <server>` on the command line.

### In the Kubescape Operator

When installing the operator, specify your account and server as Helm values using  `--set account=<accountID>` and `--set server=<server URL>`.
