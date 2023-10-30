# Automatically upgrading the Operator (Experimental)

Starting with the Helm version 1.16.1, Kubescape operator provides the Helm Release Upgrader — an experimental capability that automatically fetches the latest chart version and upgrades the installed Kubescape operator version.

## How to Use

To enable this capability, simply set the `capabilities.autoUpgrading` to `enable` and configure how often you would like to check for updates by adjusting the cron schedule:

```yaml
capabilities:
  autoUpgrading: enable

# [Omitted for brevity...]

# If necessary, adjust when you want the Helm Release Upgrader to check for
# updates and apply updates
helmReleaseUpgrader:
  schedule: "0 14 * * *"  # Check for updates every day at 14:00
```

Helm will then install the Helm Release Upgrader CronJob and its supporting resources with the Kubescape operator.
They will keep your Kubescape release up to date.

!!! warning
    Due to the way Helm works, the Helm Release Upgrader requires highly elevated RBAC permissions and leaves orphaned resources even after you uninstall the Kubescape release.

## How it Works

!!! note
    The Auto Upgrading capability is still experimental.

It works as follows:

- Creates a ClusterRole with cluster admin privileges, a ServiceAccount and a matching ClusterRoleBinding to have all the permissions necessary to create resources with Helm.
- Creates a CronJob that updates the local Kubescape Helm repo (`helm repo update`) to fetch the latest chart versions and upgrades the Helm release accordingly (`helm upgrade`).
- To account for Helm removing and re-creating the release resources during `helm upgrade`, it keeps the RBAC definitions and the CronJob in the cluster with `"helm.sh/resource-policy": keep`.

This means:

- The Helm Release Upgrader runs in a very privileged RBAC context: it can create resources, list Secrets etc.
- Even after you remove the Kubescape release with `helm -n kubescape uninstall kubescape`, it will still keep the highly privileged RBACs and CronJob in your cluster.

While the CronJob runs in a non-root security context and you can clean up the leftover resources on your own, please evaluate the risks the Helm Release Upgrader introduces against your security needs and threat model.


## How to Clean Up

To clean up the resources left by the Helm Release Upgrader, run the following command:

```
kubectl -n kubescape delete clusterrolebinding/helm-release-upgrader \
    clusterrole/helm-release-upgrader \
    serviceaccount/helm-release-upgrader \
    cj/helm-release-upgrader
```

Once it finishes, you should have no traces of the Helm Release Upgrader in your cluster.
