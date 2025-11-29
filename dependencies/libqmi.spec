# libqmi spec file template for COPR
# Update version as needed for ModemManager compatibility
# Check https://gitlab.freedesktop.org/mobile-broadband/libqmi for releases

%global forgeurl https://gitlab.freedesktop.org/mobile-broadband/libqmi

Name:           libqmi
Version:        1.35.6
Release:        1%{?dist}
Summary:        Support library to use the Qualcomm MSM Interface (QMI) protocol

License:        LGPL-2.1-or-later
URL:            %{forgeurl}
Source:         %{forgeurl}/-/archive/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  meson >= 0.53.0
BuildRequires:  gcc
BuildRequires:  pkgconfig(glib-2.0) >= 2.56
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(qrtr-glib) >= 1.2.0
BuildRequires:  pkgconfig(mbim-glib) >= 1.28.0
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  gtk-doc
BuildRequires:  help2man
BuildRequires:  bash-completion

%description
libqmi is a library for talking to WWAN devices by QMI protocol.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       glib2-devel

%description devel
Development files for %{name}.

%package utils
Summary:        Utilities to use the QMI protocol from the command line
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilities to use the QMI protocol from the command line.

%prep
%autosetup -p1

%build
%meson \
    -Dgtk_doc=true \
    -Dmbim_qmux=true \
    -Dqrtr=true \
    -Dintrospection=true

%meson_build

%install
%meson_install

%files
%license COPYING.LIB
%doc NEWS README.md
%{_libdir}/libqmi-glib.so.*
%{_libdir}/girepository-1.0/Qmi-1.0.typelib

%files devel
%{_includedir}/libqmi-glib/
%{_libdir}/libqmi-glib.so
%{_libdir}/pkgconfig/qmi-glib.pc
%{_datadir}/gir-1.0/Qmi-1.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libqmi-glib/

%files utils
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_bindir}/qmi-firmware-update
%{_libexecdir}/qmi-proxy
%{_mandir}/man1/qmicli.1*
%{_mandir}/man1/qmi-network.1*
%{_mandir}/man1/qmi-firmware-update.1*
%{_datadir}/bash-completion/completions/qmicli

%changelog
* Sat Nov 29 2025 Tim Howard <timothyhoward@outlook.com> - 1.35.6-1
- Update to 1.35.6 for ModemManager 1.25.95 compatibility
