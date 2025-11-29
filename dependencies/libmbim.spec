# libmbim spec file template for COPR
# Update version as needed for ModemManager compatibility
# Check https://gitlab.freedesktop.org/mobile-broadband/libmbim for releases

%global forgeurl https://gitlab.freedesktop.org/mobile-broadband/libmbim

Name:           libmbim
Version:        1.32
Release:        1%{?dist}
Summary:        Support library for the Mobile Broadband Interface Model (MBIM) protocol

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
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  gtk-doc
BuildRequires:  help2man
BuildRequires:  bash-completion

%description
libmbim is a library for talking to WWAN devices by MBIM protocol.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       glib2-devel

%description devel
Development files for %{name}.

%package utils
Summary:        Utilities to use the MBIM protocol from the command line
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilities to use the MBIM protocol from the command line.

%prep
%autosetup -p1

%build
%meson \
    -Dgtk_doc=true \
    -Dintrospection=true

%meson_build

%install
%meson_install

%files
%license COPYING.LIB
%doc NEWS README.md
%{_libdir}/libmbim-glib.so.*
%{_libdir}/girepository-1.0/Mbim-1.0.typelib

%files devel
%{_includedir}/libmbim-glib/
%{_libdir}/libmbim-glib.so
%{_libdir}/pkgconfig/mbim-glib.pc
%{_datadir}/gir-1.0/Mbim-1.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libmbim-glib/

%files utils
%{_bindir}/mbimcli
%{_bindir}/mbim-network
%{_libexecdir}/mbim-proxy
%{_mandir}/man1/mbimcli.1*
%{_mandir}/man1/mbim-network.1*
%{_datadir}/bash-completion/completions/mbimcli

%changelog
* Sat Nov 29 2025 Tim Howard <timothyhoward@outlook.com> - 1.32
- Update to 1.32 for ModemManager 1.25.95 compatibility
