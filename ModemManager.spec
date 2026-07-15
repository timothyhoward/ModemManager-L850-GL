# ModemManager spec file for Fedora COPR
# Updated for version 1.25.95 to support Fibocom L850-GL and other modems
#
# Based on Fedora's official ModemManager spec file

%bcond check 1

%global glib2_version %(pkg-config --modversion glib-2.0 2>/dev/null || echo bad)
%global qmi_version %(pkg-config --modversion qmi-glib 2>/dev/null || echo bad)
%global mbim_version %(pkg-config --modversion mbim-glib 2>/dev/null || echo bad)
%global qrtr_version %(pkg-config --modversion qrtr-glib 2>/dev/null || echo bad)

%global forgeurl https://gitlab.freedesktop.org/mobile-broadband/ModemManager

Name:           ModemManager
Version:        1.25.95
Release:        2%{?dist}
Summary:        Mobile broadband modem management service

License:        GPL-2.0-or-later
URL:            %{forgeurl}
Source:         %{forgeurl}/-/archive/%{version}-dev/%{name}-%{version}-dev.tar.bz2

# XMM7360 response parser hardening from upstream merge request !1421.
# These changes replace assertions on modem-provided data with recoverable
# errors and add coverage for malformed XMMRPC responses.
Patch0:         %{forgeurl}/-/commit/1565e3ada74ecac6e0493a25acff3f828ff03f93.patch
Patch1:         %{forgeurl}/-/commit/07dc7e7304d81c3127d5259c309e89f819ff4ef4.patch
Patch2:         %{forgeurl}/-/commit/3f7b39075c379f31b009af7665890ef32f1591c8.patch
Patch3:         %{forgeurl}/-/commit/4fead86d247f0a5c61d57d3155e0580f8c01d9b0.patch
Patch4:         %{forgeurl}/-/commit/64d8053413b8e7583a6176e9f3397aaa4135372f.patch
Patch5:         %{forgeurl}/-/commit/d6fe0722c9b37f7adbca8f1b4155ebada23a287b.patch
Patch6:         %{forgeurl}/-/commit/a486776a445bf39a51cb9f93d4c73601329c0c7b.patch
Patch7:         %{forgeurl}/-/commit/a94dd40a2a849046510206480964a06b99118530.patch
# Ensure the new protocol test waits for its generated enum header. This is
# needed when the upstream series is applied to the 1.25.95 snapshot.
Patch8:         0009-intel-xmm7360-test-generated-header.patch

# For mbim-proxy and qmi-proxy
Requires:       libmbim-utils
Requires:       libqmi-utils
Requires:       %{name}-glib%{?_isa} = %{version}-%{release}
# Required by the Intel XMM7360 FCC-unlock helper.
Requires:       xxd

# Don't allow older versions of these than what we built against,
# because they add new API w/o versioning it or bumping the SONAME
Conflicts:      glib2%{?_isa} < %{glib2_version}
Conflicts:      libqmi%{?_isa} < %{qmi_version}
Conflicts:      libmbim%{?_isa} < %{mbim_version}
Conflicts:      libqrtr-glib%{?_isa} < %{qrtr_version}

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(glib-2.0) >= 2.56
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gudev-1.0) >= 232
BuildRequires:  pkgconfig(qmi-glib) >= 1.37.95
BuildRequires:  pkgconfig(mbim-glib) >= 1.33.1
BuildRequires:  pkgconfig(qrtr-glib) >= 1.2.0
BuildRequires:  pkgconfig(polkit-gobject-1) >= 0.97
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  gobject-introspection-devel
BuildRequires:  vala
BuildRequires:  gtk-doc
BuildRequires:  python3-dbus
BuildRequires:  python3-gobject
BuildRequires:  help2man

%if %{with check}
BuildRequires:  /usr/bin/dbus-run-session
%endif

%description
The ModemManager service provides a unified high level API for communicating
with mobile broadband modems, regardless of the protocol used to communicate
with the actual device (Generic AT, vendor-specific AT, QCDM, QMI, MBIM...).

This package includes support for the Fibocom L850-GL and FM350-GL modems
among many others.

%package glib
Summary:        Libraries for adding ModemManager support to applications that use glib
License:        LGPL-2.1-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description glib
This package contains the libraries that make it easier to use some
ModemManager functionality from applications that use glib.

%package devel
Summary:        Development files for ModemManager
License:        LGPL-2.1-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-glib%{?_isa} = %{version}-%{release}
Requires:       glib2-devel >= %{glib2_version}

%description devel
This package contains header files and pkg-config files needed for development.

%package glib-devel
Summary:        Libraries and headers for adding ModemManager support to applications that use glib
License:        LGPL-2.1-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-glib%{?_isa} = %{version}-%{release}
Requires:       glib2-devel >= %{glib2_version}
Requires:       pkgconfig

%description glib-devel
This package contains various headers for accessing some ModemManager
functionality from glib applications.

%package vala
Summary:        Vala bindings for ModemManager
License:        LGPL-2.1-or-later
Requires:       vala
Requires:       %{name}-glib%{?_isa} = %{version}-%{release}

%description vala
Vala bindings for ModemManager.

%prep
%autosetup -p1 -n %{name}-%{version}-dev

%build
# Let's avoid BuildRequiring bash-completion because it changes behavior
# of shell, at least until the .pc file gets into the -devel subpackage.
# We'll just install the bash-completion file ourselves.
%meson \
    -Ddist_version='"%{version}-%{release}"' \
    -Dudevdir=/usr/lib/udev \
    -Dsystemdsystemunitdir=%{_unitdir} \
    -Ddbus_policy_dir=%{_datadir}/dbus-1/system.d \
    -Dvapi=true \
    -Dgtk_doc=true \
    -Dpolkit=permissive \
    -Dbash_completion=false

%meson_build

%install
%meson_install

find %{buildroot}%{_datadir}/gtk-doc |xargs touch --reference meson.build

%find_lang %{name}

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
cp -a cli/mmcli-completion %{buildroot}%{_datadir}/bash-completion/completions/mmcli

%if %{with check}
%check
%meson_test
%endif

%post
%systemd_post ModemManager.service

%preun
%systemd_preun ModemManager.service

%postun
%systemd_postun ModemManager.service

%files -f %{name}.lang
%license COPYING
%doc README.md NEWS AUTHORS
%{_datadir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager1.service
%attr(0755,root,root) %{_sbindir}/ModemManager
%attr(0755,root,root) %{_bindir}/mmcli
%{_mandir}/man1/mmcli.1*
%{_mandir}/man8/ModemManager.8*
%{_unitdir}/ModemManager.service
/usr/lib/udev/rules.d/*
%dir %{_libdir}/ModemManager
%{_libdir}/ModemManager/*.so
%{_datadir}/ModemManager/fcc-unlock.available.d/*
%{_datadir}/ModemManager/connection.available.d/*
%{_datadir}/ModemManager/modem-setup.available.d/*
%{_datadir}/ModemManager/*.conf
%dir %{_sysconfdir}/ModemManager/fcc-unlock.d
%dir %{_sysconfdir}/ModemManager/connection.d
%{_datadir}/icons/hicolor/*/apps/ModemManager.png
%{_datadir}/polkit-1/actions/org.freedesktop.ModemManager1.policy
%{_datadir}/bash-completion/completions/mmcli

%files glib
%{_libdir}/libmm-glib.so.0*
%{_libdir}/girepository-1.0/ModemManager-1.0.typelib

%files devel
%{_includedir}/ModemManager/
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/dbus-1/interfaces/org.freedesktop.ModemManager1*.xml

%files glib-devel
%dir %{_includedir}/libmm-glib
%{_includedir}/libmm-glib/*.h
%{_libdir}/libmm-glib.so
%{_libdir}/pkgconfig/mm-glib.pc
%{_datadir}/gir-1.0/ModemManager-1.0.gir
%{_datadir}/gtk-doc/html/ModemManager/
%{_datadir}/gtk-doc/html/libmm-glib/

%files vala
%{_datadir}/vala/vapi/libmm-glib.deps
%{_datadir}/vala/vapi/libmm-glib.vapi

%changelog
* Wed Jul 15 2026 Tim Howard <timothyhoward@outlook.com> - 1.25.95-2
- Require xxd for the Intel XMM7360 FCC-unlock helper
- Backport upstream XMM7360 response parser hardening
- Fix the backported Intel protocol test's generated-header dependency
- Correct Fedora runtime library conflict package names

* Sat Nov 29 2025 Tim Howard <timothyhoward@outlook.com> - 1.25.95-1
- Update to 1.25.95 development release
- Added support for additional Fibocom modems including L850-GL
- Based on Debian experimental package

* Thu Jan 01 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.2-1
- Based on Fedora's ModemManager 1.24.2 spec file
