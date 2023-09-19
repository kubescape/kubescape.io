# Installing Kubescape

The Kubescape command-line client is a single binary. Because the software is updated frequently, we recommend you install Kubescape with the package manager appropriate for your system.  

When Kubescape runs, it will check for a more recent version.

* [All platforms](#all-platforms)
* [Windows](#install-on-windows)
* [macOS](#install-on-macos)
* [Linux](#install-on-linux)
* [nix](#install-on-nixos-or-with-nix-community)
* [Manual installation](#manual-installation)


## All platforms

### krew

[Krew](https://krew.sigs.k8s.io/) is the plugin manager for the `kubectl` command-line tool.  Kubescape can be installed as a `kubectl` plugin.

First, [install Krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/) using the appropriate method for your platform. Then, to install Kubescape:

```bash
kubectl krew update
kubectl krew install kubescape
kubectl kubescape
```

## Windows

### PowerShell 

Kubescape is packaged for Windows v86_64. 

```powershell
iwr -useb https://raw.githubusercontent.com/kubescape/kubescape/master/install.ps1 | iex
```

If you get an error message, you may need to change the [execution policy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.3):

```powershell
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
```

!!! note "Note"
    The installation script requires PowerShell v5.0 or higher.

## Chocolatey
> **Note**: Chocolatey [community-supported](https://community.chocolatey.org/packages/kubescape).
```powershell
choco install kubescape
```

!!! note "Note"
    Packaging for Chocolatey is community-supported and may not be up to date with the [latest Kubescape release](https://github.com/kubescape/kubescape/tags).

## Manual installation

### X86_64 or ARM64 (M1/M2) Linux / macOS
```bash
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
```

## Linux

### Ubuntu

The Kubescape maintainers build each release and upload the packages to a [personal package archive (PPA)](https://help.launchpad.net/Packaging/PPA).

To install Kubescape with `apt`:

```bash
sudo add-apt-repository ppa:kubescape/kubescape
sudo apt update
sudo apt install kubescape
```

Kubescape can also be installed from [the Snap Store]
[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-white.svg)](https://snapcraft.io/kubescape)



### Red Hat, CentOS, Fedora and other RPM-based distributions, and Debian

The Kubescape maintainers build each release and upload the packages to the openSUSE Build Service (OBS), which builds packages in `RPM` and `deb` format for many

[Installation instructions for each platform are available on the OBS page](https://software.opensuse.org/download.html?project=home%3Akubescape&package=kubescape).

### openSUSE

Kubescape is packaged for the Zypper package manager.

```bash
sudo zypper refresh
sudo zypper install kubescape
```

!!! note "Note"
    Packaging for openSUSE is supported by the openSUSE community.

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
    Packaging for kubescape-bin is supported by the AUR community.


## Homebrew
> **Note**: The kubescape delivered by [official Homebrew](https://formulae.brew.sh/formula/kubescape#default) comes with git disabled.

```bash
brew install kubescape
```

If you want to have the git enabled one, you can install via the [homebrew-tap](https://github.com/kubescape/homebrew-tap):
```bash
brew tap kubescape/tap
brew install kubescape-cli
```


## Scoop
> **Note**: Scoop [community-supported](https://scoop.sh/#/apps?q=kubescape&s=0&d=1&o=true&id=1f5ae05eaafe3e7a26505f0889101e0da91ffe91).
```powershell
scoop install kubescape
```



## NixOS or with nix
> **Note**: This method is community-supported. If you are having trouble, please reach out to [NixOS support](https://nixos.wiki/wiki/Support).

You can use `nix` on Linux or macOS.

Try it out in an ephemeral shell: `nix-shell -p kubescape`.

NixOS:

```
  # your other config ...
  environment.systemPackages = with pkgs; [
    # your other packages ...
    kubescape
  ];
```

home-manager:

```
  # your other config ...
  home.packages = with pkgs; [
    # your other packages ...
    kubescape
  ];
```

Or, to your profile (not preferred): `nix-env --install -A nixpkgs.kubescape`.

## In-cluster installation