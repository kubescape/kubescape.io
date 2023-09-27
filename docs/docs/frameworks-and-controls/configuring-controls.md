## Customizing control configurations

While most of the controls look for specific parameters and their values, which are predefined and determined by Kubernetes, some of the controls look for certain values which change from cluster to cluster or from one environment to the other. We recommend that you adjust these controls to your specific use case, as the default settings can lead to false positive results.

If a control supports configuration, the parameters will be listed on its page in the [control library](../controls/index.md).

### Downloading your control configuration

If you are connected to a [provider](../providers.md), you can download the control configuration file associated with your account ID. All other users will receive the default control configuration from GitHub.

```sh
kubescape download controls-inputs
```

The file will be saved as `~/.kubescape/controls-inputs.json`. You can configure a different download location with the `-o` flag.

Edit this file to define configuration parameters for Kubescape scans.