# Azure Kubernetes Service integration

This uses the Kubescape CLI to scan the clusters and run commands.

## Prerequisites: collect the ClusterID and PrincipalID

In the Azure CLI, run the following commands:

1. List managed identities for the cluster.
   ```shell
   az aks show --resource-group <your_resource_group_name> --name <your_cluster_name> --query identity
   ```
2. Collect the principalID using the ID returned from the previous command.
   ```shell
   principal_id=$(az aks show --resource-group <your_resource_group_name> --name <your_cluster_name> --query 'identity.principalId' -o tsv)
   echo $principal_id
   ```
3. Collect the clusterID.
   ```shell
   cluster_id=$(az aks show --resource-group <your_resource_group_name> --name <your_cluster_name> --query id -o tsv)
   echo $cluster_id
   ```

## Use Kubescape CLI to scan the cluster

If you're running Kubescape CLI on the same computer as the Azure CLI, it can leverage the local authentication just by knowing the subscription ID and the resource group:

```shell
export AZURE_SUBSCRIPTION_ID=<your_subscription_id>
export AZURE_RESOURCE_GROUP=<your_resource_group_name>
kubescape scan framework nsa
```

In case of errors, you can troubleshoot them by enabling debug logs, for example:

```
kubescape scan framework nsa -l debug
...
 🐞  cloud. clusterName: matthias-test; provider: aks
 🐞  Collecting cloud data . resourceKind: ClusterDescribe
 🐞  failed to get cloud data. resourceKind: ClusterDescribe; error: error retrieving azure subscription id:
environment variable AZURE_SUBSCRIPTION_ID not set
...
```

## Use Kubescape inside a CI/CD job

In order to scan from a different computer, or a CI/CD worker, you have to create an App registration with read permissions on the cluster, and a secret for it.

You can then export the following variables:

```shell
export AZURE_CLIENT_ID=<your_client_id>
export AZURE_CLIENT_SECRET=<your_client_secret>
export AZURE_RESOURCE_GROUP=<your_resource_group_name>
export AZURE_SUBSCRIPTION_ID=<your_subscription_id>
export AZURE_TENANT_ID=<your_tenant_id>
```

And perform your scan as usual:

```
kubescape scan framework nsa
```

## Install Kubescape Operator with credentials

There are two ways to manage identities in Azure- [System-assigned](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-managed-identities-work-vm#system-assigned-managed-identity) and [User-assigned](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-managed-identities-work-vm#user-assigned-managed-identity).

It depends on how you manage your identities:

### System-Assigned Managed Identities

#### Assign the `Reader` role to the PrincipalID in the scope of the cluster

In the Azure CLI, run the following command:

```Text Assign Reader
az role assignment create --assignee "\<principal_id>" --role "Reader" --scope "\<cluster_id>"
```

>  You must have the ability to assign a role, if you get an authorization error while creating the role, please get in touch with your AZURE administrator.

#### Install Kubescape

Pay attention that you need to add manually the following:

1. `cloudProviderMetadata.cloudProviderEngine=aks`
2. `cloudProviderMetadata.aksSubscriptionID=<Subscription ID>`
3. `cloudProviderMetadata.aksResourceGroup=<Resource Group>`

```Text
helm repo add kubescape https://kubescape.github.io/helm-charts/ ; helm repo update ; helm upgrade --install kubescape kubescape/kubescape-operator -n kubescape --create-namespace --set clusterName=`kubectl config current-context` --set account=<ACCOUNT_ID> --set server=api.armosec.io  --set cloudProviderMetadata.aksSubscriptionID=`az account show --query id --output tsv` --set cloudProviderMetadata.aksResourceGroup=`az resource list --name \`kubectl config current-context\` --query [].resourceGroup --output tsv` --set cloudProviderMetadata.cloudProviderEngine=aks
```

### User-Assigned Managed Identities

#### Assign the `Reader` role to the Managed Identity of the kubelet to the scope of the cluster control plane.

In the Azure CLI, run the following command:

```Text Assign Reader
az role assignment create --assignee $(az aks show --resource-group $(az resource list --name $(kubectl config current-context) --query "[].resourceGroup" --output tsv) --name $(kubectl config current-context) --query "identityProfile.kubeletidentity.clientId" --output tsv) --role "Reader" --scope /subscriptions/$(az account show --query id --output tsv)/resourceGroups/$(az resource list --name $(kubectl config current-context) --query "[].resourceGroup" --output tsv)
```

>  You must have the ability to assign a role, if you get an authorization error while creating the role, please get in touch with your AZURE administrator.

#### Install Kubescape

Pay attention that you need to add manually the following:

1. `cloudProviderMetadata.cloudProviderEngine=aks`
2. `cloudProviderMetadata.aksSubscriptionID=<Subscription ID>`
3. `cloudProviderMetadata.aksResourceGroup=<Resource Group>`
4. `cloudProviderMetadata.aksTenantID=<Tenant ID>`
5. `cloudProviderMetadata.aksClientID=<Client ID>`
6. `cloudProviderMetadata.aksClientSecret=<ClientSecret>`

It should look like this:

```Text
helm repo add kubescape https://kubescape.github.io/helm-charts/ ; helm repo update ; helm upgrade --install kubescape kubescape/kubescape-operator -n kubescape --create-namespace --set clusterName=$(kubectl config current-context) --set account=<ACCOUNT_ID> --set accessKey=<ACCESSKEY> --set server=api.armosec.io  --set cloudProviderMetadata.aksSubscriptionID=$(az account show --query id --output tsv) --set cloudProviderMetadata.aksResourceGroup=$(az resource list --name $(kubectl config current-context) --query "[].resourceGroup" --output tsv) --set cloudProviderMetadata.cloudProviderEngine=aks --set cloudProviderMetadata.aksTenantID=<AZURE tenant ID> --set cloudProviderMetadata.aksClientID=$(az aks show --resource-group $(az resource list --name $(kubectl config current-context) --query "[].resourceGroup" --output tsv) --name $(kubectl config current-context) --query "identityProfile.kubeletidentity.clientId" --output tsv) --set cloudProviderMetadata.aksClientSecret=<Client secret>
```
