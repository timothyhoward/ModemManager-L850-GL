# ModemManager 1.25.95 COPR Build

This repository contains the spec file and build configuration to create a Fedora COPR for ModemManager 1.25.95, which includes improved support for various modems including the Fibocom L850-GL.

## About This Version

ModemManager 1.25.95 is a **development snapshot** (not a stable release). It includes:
- Improved support for Fibocom modems (L850-GL, FM350-GL, etc.)
- Enhanced MBIM and QMI protocol support
- Upstream XMM7360 parser hardening that prevents malformed modem responses from crashing ModemManager
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

The Intel XMM7360 FCC-unlock helper also requires `xxd`. The COPR package
declares this as a runtime dependency, but it can be checked explicitly with:

```bash
command -v xxd
```

### Important Notes About L850-GL

The L850-GL modem has complex Linux support:

1. **PCIe vs USB Mode**: The L850-GL supports both PCIe and USB interfaces
   - On some laptops, you may need to switch from PCIe to USB mode
   - See https://github.com/xmm7360/xmm7360-usb-modeswitch for the mode-switching tool

2. **PCIe control interfaces**: In native PCIe mode, the `iosm` driver exposes
   AT, network, and XMMRPC ports. ModemManager uses XMMRPC for the L850-GL's
   modem control and data setup; it does not use MBIM on this path. MBIM is
   relevant only when a machine can switch the modem to USB mode.

3. **SIM Detection Issues**: Some users report SIM detection issues that require additional scripts

4. **FCC unlock**: The XMM7360 FCC-unlock helper is shipped disabled and must
   be explicitly enabled on systems that require it. See the installation step
   below.

## Building the COPR

### Option 1: Use Existing COPR (if available)

```bash
sudo dnf copr enable YOUR_USERNAME/ModemManager-1.25.95
sudo dnf upgrade ModemManager
```

### Option 2: Build Your Own COPR (with dependencies)

Since ModemManager 1.25.95 requires newer versions of libmbim and libqmi than may be available in your Fedora release, you'll likely need to build all three packages.

#### Step 1: Create a COPR Project

1. Go to https://copr.fedorainfracloud.org
2. Click "New Project"
3. Name it (e.g., `ModemManager-1.25.95`)
4. Select target Fedora releases (e.g., Fedora 41, 42, rawhide)
5. **Important**: Under "Build options", you may want to enable "Follow Fedora branching"

#### Step 2: Add All Three Packages

You need to add three packages to your COPR project. Go to **Packages → New Package** for each:

**Package 1: libmbim** (build this first)
- Package Name: `libmbim`
- Source Type: SCM
- Clone URL: `https://github.com/timothyhoward/ModemManager-L850-GL.git`
- Subdirectory: (leave empty)
- Spec File: `dependencies/libmbim.spec`
- SRPM Build Method: make srpm

**Package 2: libqmi** (build after libmbim completes)
- Package Name: `libqmi`
- Source Type: SCM
- Clone URL: `https://github.com/timothyhoward/ModemManager-L850-GL.git`
- Subdirectory: (leave empty)
- Spec File: `dependencies/libqmi.spec`
- SRPM Build Method: make srpm

**Package 3: ModemManager** (build after libqmi completes)
- Package Name: `ModemManager`
- Source Type: SCM
- Clone URL: `https://github.com/timothyhoward/ModemManager-L850-GL.git`
- Subdirectory: (leave empty)
- Spec File: `ModemManager.spec`
- SRPM Build Method: make srpm

#### Step 3: Build in Order

**Critical**: You must build the packages in dependency order!

1. Click on the `libmbim` package → Click "Rebuild"
2. **Wait for it to complete successfully**
3. Click on the `libqmi` package → Click "Rebuild"
4. **Wait for it to complete successfully**
5. Click on the `ModemManager` package → Click "Rebuild"

Why the order matters: Each package needs the previous one to be available in your COPR repo before it can build successfully.

#### Step 4: Enable and Install

Once all builds complete:

```bash
# Enable the COPR
sudo dnf copr enable YOUR_USERNAME/ModemManager-1.25.95

# Install/upgrade packages
sudo dnf upgrade libmbim libqmi ModemManager

# Enable the XMM7360 FCC-unlock helper
sudo install -d -m 0755 /etc/ModemManager/fcc-unlock.d
sudo ln -sfn \
  /usr/share/ModemManager/fcc-unlock.available.d/8086:7360 \
  /etc/ModemManager/fcc-unlock.d/8086:7360

# Restart ModemManager
sudo systemctl restart ModemManager
```

The helper invokes `xxd` to encode and decode XMMRPC messages. If `xxd` is
missing, the helper can wait indefinitely for a response until ModemManager's
FCC-unlock timeout kills it.

### Option 3: Local Build

```bash
# Install build dependencies
sudo dnf install rpm-build rpmdevtools spectool

# Setup RPM build tree
rpmdev-setuptree

# Build libmbim first
cp dependencies/libmbim.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild/SOURCES && spectool -g -R ~/rpmbuild/SPECS/libmbim.spec
sudo dnf builddep ~/rpmbuild/SPECS/libmbim.spec
rpmbuild -ba ~/rpmbuild/SPECS/libmbim.spec
sudo dnf install ~/rpmbuild/RPMS/x86_64/libmbim-*.rpm

# Build libqmi second
cp dependencies/libqmi.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild/SOURCES && spectool -g -R ~/rpmbuild/SPECS/libqmi.spec
sudo dnf builddep ~/rpmbuild/SPECS/libqmi.spec
rpmbuild -ba ~/rpmbuild/SPECS/libqmi.spec
sudo dnf install ~/rpmbuild/RPMS/x86_64/libqmi-*.rpm

# Build ModemManager last
cp ModemManager.spec ~/rpmbuild/SPECS/
cp patches/*.patch ~/rpmbuild/SOURCES/
cd ~/rpmbuild/SOURCES && spectool -g -R ~/rpmbuild/SPECS/ModemManager.spec
sudo dnf builddep ~/rpmbuild/SPECS/ModemManager.spec
rpmbuild -ba ~/rpmbuild/SPECS/ModemManager.spec
sudo dnf install ~/rpmbuild/RPMS/x86_64/ModemManager-*.rpm
```

## Dependency Requirements

ModemManager 1.25.95 requires updated versions of:
- `libqmi` >= 1.37.95
- `libmbim` >= 1.33.1
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

### FCC Unlock Fails or ModemManager Exits

Confirm that `xxd` is installed and that the XMM7360 helper is enabled:

```bash
rpm -q xxd
readlink -f /etc/ModemManager/fcc-unlock.d/8086:7360
journalctl -u ModemManager -b | grep -i fcc
```

The helper symlink should resolve to:

```text
/usr/share/ModemManager/fcc-unlock.available.d/8086:7360
```

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
- `patches/` - Local packaging fixes applied after the upstream backports
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
