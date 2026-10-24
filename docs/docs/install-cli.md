# Installing Kubescape

The Kubescape command-line client is a single binary. Because the software is updated frequently, we recommend you install Kubescape with the package manager appropriate for your system.  

When Kubescape runs, it will check for a more recent version.

## Cross-platform

### Script install

!!! info "Supported platforms"
    This script is supported on Linux (x86_64 and arm64), macOS (Intel or Apple Silicon) and `bash` on Windows (x86_64).

You can automatically download and install Kubescape using our installer script.  We encourage you to read it before executing it.

If run as root, the script will install the `kubescape` binary in `/usr/local/bin`.  If run as a user, it will put the binary in `/.kubescape/bin`.

```bash
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
```

### krew

[Krew](https://krew.sigs.k8s.io/) is the plugin manager for the `kubectl` command-line tool.  Kubescape can be installed as a `kubectl` plugin.

First, [install Krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/) using the appropriate method for your platform. Then, install Kubescape:

```bash
kubectl krew update
kubectl krew install kubescape
```

To invoke Kubescape when installed with krew, use `kubectl kubescape` instead of `kubescape`.


## Windows

!!! info "Supported platforms"
    Kubescape is supported on Windows x64.


### PowerShell 

Similar to the [bash installation script](#manual-install), you can install Kubescape using PowerShell on Windows: 

```powershell
iwr -useb https://raw.githubusercontent.com/kubescape/kubescape/master/install.ps1 | iex
```

If you get an error message, you may need to change the [execution policy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.3):

```powershell
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
```

!!! note "Note"
    The installation script requires PowerShell v5.0 or higher.

### Chocolatey

[Chocolatey](https://chocolatey.org/) is a package manager for Windows.  To install Kubescape using Chocolatey, open a PowerShell terminal and run:

```powershell
choco install kubescape
```

!!! note "Note"
    Packaging for Chocolatey is [community supported](https://community.chocolatey.org/packages/kubescape) and may not always be up-to-date with the [latest Kubescape release](https://github.com/kubescape/kubescape/tags).

### Scoop

[Scoop](https://scoop.sh/) is a command-line installer for Windows.  To install Kubescape using Scoop, open a PowerShell terminal and run:

```powershell
scoop install kubescape
```

!!! note "Note"
    Packaging for Scoop is [community supported](https://scoop.sh/#/apps?q=kubescape&s=0&d=1&o=true&id=1f5ae05eaafe3e7a26505f0889101e0da91ffe91) and may not always be up-to-date with the [latest Kubescape release](https://github.com/kubescape/kubescape/tags).

## macOS

### Homebrew

Kubescape is available in the [official Homebrew repository](https://formulae.brew.sh/formula/kubescape#default) or through a [Kubescape tap](https://github.com/kubescape/homebrew-tap). The version from the official repository does not include support for scanning Git repositories, due to [an upstream packaging issue](https://github.com/kubescape/kubescape/issues/1014). For full functionality, use the [install script](#quick-install) or a [GitHub release](#manual-installation).

```bash
brew install kubescape
```

## Linux

### openSUSE

Kubescape is packaged for the Zypper package manager.

```bash
sudo zypper refresh
sudo zypper install kubescape
```

!!! note "Note"
    Packaging for openSUSE is supported by the openSUSE community and may not always be up-to-date with the [latest Kubescape release](https://github.com/kubescape/kubescape/tags).

### Arch

Kubescape is available in the [Arch Linux User Repository (AUR)](https://aur.archlinux.org/). To download and compile Kubescape on Arch Linux:

```bash
yay -S kubescape
```

If you would like to save some time and do not want to compile, you can install `kubescape-bin` instead:

```bash
yay -S kubescape-bin
```

!!! note "Note"
    Packaging for kubescape-bin is supported by the [AUR community](https://aur.archlinux.org/packages?O=0&K=kubescape) and may not always be up-to-date with the [latest Kubescape release](https://github.com/kubescape/kubescape/tags).


### NixOS, or using nix on Windows or Linux

You can use `nix` on Linux or macOS.

To try it out in an ephemeral shell, run `nix-shell -p kubescape`.

To install Kubescape on NixOS, add the following configuration to your [`/etc/nixos/configuration.nix`](https://nixos.org/manual/nixos/stable/#ch-configuration) file:

```
  # your other config ...
  environment.systemPackages = with pkgs; [
    # your other packages ...
    kubescape
  ];
```

Alternatively, if using [Home Manager](https://nixos.wiki/wiki/Home_Manager):

```
  # your other config ...
  home.packages = with pkgs; [
    # your other packages ...
    kubescape
  ];
```

Or, to install your profile (not recommended): 

```bash
nix-env --install -A nixpkgs.kubescape
```

!!! note "Note"
    Packaging for Nix is [community supported](https://github.com/NixOS/nixpkgs/blob/master/pkgs/tools/security/kubescape/default.nix) and may not always be up-to-date with the [latest Kubescape release](https://github.com/kubescape/kubescape/tags). If you are having trouble, please reach out to [NixOS support](https://nixos.wiki/wiki/Support).

## Offline/air-gapped environment support

When it runs, Kubescape downloads *artifacts* (frameworks, controls and configurations) from the [control library](frameworks-and-controls/index.md) or from a configured [provider](providers.md).

You can download these files manually, so that Kubescape can run offline, or in an "air-gapped" environment.

### Download all artifacts

1. Download the controls and save them in the local directory.  If no path is specified, they will be saved in `~/.kubescape`.

    ```sh
    kubescape download artifacts --output path/to/local/dir
    ```

2. Copy the downloaded artifacts to the offline system.
  
3. Scan using the downloaded artifacts:

    ```sh
    kubescape scan --use-artifacts-from path/to/local/dir
    ```

### Download a single artifact

You can also download a single artifact, and scan with the `--use-from` flag:

1. Download and save in a file. If no file name is specified, the artifact will be saved as `~/.kubescape/<framework name>.json`.

    ```sh
    kubescape download framework nsa --output /path/nsa.json
    ```

2. Copy the downloaded artifacts to the offline system.

3. Scan using the downloaded framework:

    ```sh
    kubescape scan framework nsa --use-from /path/nsa.json
    ```

## Next steps

* [Learn how to install the Kubescape Operator in your Kubernetes cluster](install-operator.md)
