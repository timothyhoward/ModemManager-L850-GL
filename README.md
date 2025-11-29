# ModemManager 1.25.95 COPR Build

This repository contains the spec file and build configuration to create a Fedora COPR for ModemManager 1.25.95, which includes improved support for various modems including the Fibocom L850-GL.

## About This Version

ModemManager 1.25.95 is a **development snapshot** (not a stable release). It includes:
- Improved support for Fibocom modems (L850-GL, FM350-GL, etc.)
- Enhanced MBIM and QMI protocol support
- Various bug fixes and improvements from the 1.25.x development branch

## Prerequisites

### Kernel Requirements for Fibocom L850-GL

The Fibocom L850-GL modem requires:
- Linux kernel 5.18+ (for the `iosm` driver)
- Or Linux kernel 6.2+ for improved support

Check if your kernel has the iosm driver:
```bash
modinfo iosm
```

### Important Notes About L850-GL

The L850-GL modem has complex Linux support:

1. **PCIe vs USB Mode**: The L850-GL supports both PCIe and USB interfaces
   - On some laptops, you may need to switch from PCIe to USB mode
   - See https://github.com/xmm7360/xmm7360-usb-modeswitch for the mode-switching tool

2. **MBIM Interface**: ModemManager communicates via MBIM, but the L850-GL's MBIM support varies by firmware version

3. **SIM Detection Issues**: Some users report SIM detection issues that require additional scripts

## Building the COPR

### Option 1: Use Existing COPR (if available)

```bash
sudo dnf copr enable YOUR_USERNAME/ModemManager-1.25.95
sudo dnf upgrade ModemManager
```

### Option 2: Build Your Own COPR

1. **Fork this repository** to your GitLab/GitHub account

2. **Create a COPR project**:
   - Go to https://copr.fedorainfracloud.org
   - Click "New Project"
   - Name it (e.g., `ModemManager-1.25.95`)
   - Select target Fedora releases (e.g., Fedora 41, 42, rawhide)

3. **Add a package**:
   - Click "Packages" → "New Package"
   - Source Type: SCM
   - Clone URL: Your forked repository URL
   - Spec File: `ModemManager.spec`
   - SRPM Build Method: make srpm
   - Click "Save" then "Build"

### Option 3: Local Build

```bash
# Install build dependencies
sudo dnf install rpm-build rpmdevtools spectool

# Setup RPM build tree
rpmdev-setuptree

# Copy spec file
cp ModemManager.spec ~/rpmbuild/SPECS/

# Download sources
cd ~/rpmbuild/SOURCES
spectool -g -R ~/rpmbuild/SPECS/ModemManager.spec

# Install build dependencies
sudo dnf builddep ~/rpmbuild/SPECS/ModemManager.spec

# Build
rpmbuild -ba ~/rpmbuild/SPECS/ModemManager.spec
```

## Dependency Requirements

ModemManager 1.25.95 requires updated versions of:
- `libqmi` >= 1.35.2
- `libmbim` >= 1.29.2
- `libqrtr-glib` >= 1.2.0

If your Fedora version doesn't have these versions, you may need to build them from COPRs or source as well.

### Check Your Current Versions

```bash
rpm -q libqmi libmbim
pkg-config --modversion qmi-glib mbim-glib
```

## Installation

After building or enabling the COPR:

```bash
# Upgrade ModemManager
sudo dnf upgrade ModemManager ModemManager-glib

# Restart the service
sudo systemctl restart ModemManager

# Check status
sudo systemctl status ModemManager
mmcli -L
```

## Troubleshooting

### Modem Not Detected

```bash
# Check if kernel driver is loaded
lsmod | grep iosm
lspci | grep -i xmm

# Check ModemManager logs
sudo journalctl -u ModemManager -f

# Run ModemManager in debug mode
sudo systemctl stop ModemManager
sudo /usr/sbin/ModemManager --debug
```

### SIM Card Not Detected

Some L850-GL modems require the SIM to be inserted before boot. Try:
1. Power off completely
2. Insert SIM card
3. Power on

### USB Mode Switch (if needed)

For laptops where PCIe mode doesn't work:
```bash
# Install xmm7360-usb-modeswitch
git clone https://github.com/xmm7360/xmm7360-usb-modeswitch
cd xmm7360-usb-modeswitch
# Follow the README instructions
```

## Files in This Repository

- `ModemManager.spec` - The RPM spec file for building ModemManager 1.25.95
- `.copr/Makefile` - Build instructions for Fedora COPR
- `README.md` - This file

## References

- [ModemManager Official Site](https://modemmanager.org/)
- [ModemManager GitLab](https://gitlab.freedesktop.org/mobile-broadband/ModemManager)
- [Fibocom L850-GL on ArchWiki](https://wiki.archlinux.org/title/Xmm7360-pci)
- [xmm7360-pci Driver](https://github.com/xmm7360/xmm7360-pci)
- [xmm7360-usb-modeswitch](https://github.com/xmm7360/xmm7360-usb-modeswitch)

## License

The spec file is based on Fedora's official ModemManager package.
ModemManager itself is licensed under GPL-2.0-or-later.

## Contributing

Issues and pull requests are welcome!
