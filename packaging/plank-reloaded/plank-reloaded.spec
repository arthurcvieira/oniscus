#
# spec file for the plank-reloaded package (Oniscus)
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Plank left openSUSE Tumbleweed (upstream stopped in 2019). Plank Reloaded is
# the maintained fork: same "plank" command, same settings schema
# (net.launchpad.plank) and same theme format, so Oniscus's Plank configs work
# unchanged. Built in home:oniscus on build.opensuse.org.
#

Name:           plank-reloaded
Version:        0.11.178
Release:        0
Summary:        Simple dock for X11 desktops (maintained fork of Plank)
License:        GPL-3.0-or-later AND LGPL-2.1-or-later
URL:            https://github.com/zquestz/plank-reloaded
Source0:        https://github.com/zquestz/plank-reloaded/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Opt-in override-redirect dock window (PLANK_OVERRIDE_REDIRECT=1), for i3
Patch0:         plank-override-redirect.patch
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja
BuildRequires:  pkgconfig
BuildRequires:  vala >= 0.34
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libbamf3)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libgnome-menu-3.0)
BuildRequires:  pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
Requires:       bamf-daemon
Provides:       plank = %{version}
Obsoletes:      plank < %{version}

%description
Plank Reloaded is a fork of Plank, a simple dock for X11 desktop environments
(Xfce, MATE, Cinnamon and others). It keeps Plank's command, settings and
themes.

%package devel
Summary:        Development files for Plank Reloaded docklets
Requires:       %{name} = %{version}

%description devel
Headers, pkg-config file and Vala bindings for libplank, used to build
docklets for Plank Reloaded.

%prep
%autosetup -p1

%build
%meson \
    -Denable-apport=false \
    -Dproduction-release=true
%meson_build

%install
%meson_install
rm -f %{buildroot}%{_libdir}/*.la
# README.md goes in with %doc below
rm -rf %{buildroot}%{_datadir}/doc/%{name}
%find_lang %{name} %{?no_lang_C} || touch %{name}.lang
%fdupes %{buildroot}%{_datadir}

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING COPYING.LGPL2.1 COPYRIGHT
%doc README.md NEWS.md AUTHORS
%{_bindir}/plank
%{_libdir}/libplank.so.*
%{_libdir}/plank/
%{_datadir}/plank/
%{_datadir}/applications/net.launchpad.plank.desktop
%{_datadir}/glib-2.0/schemas/net.launchpad.plank.gschema.xml
%{_datadir}/icons/hicolor/*/apps/plank-reloaded.png
%{_datadir}/metainfo/plank.appdata.xml
%{_mandir}/man1/plank.1%{?ext_man}

%files devel
%{_includedir}/plank/
%{_libdir}/libplank.so
%{_libdir}/pkgconfig/plank.pc
%{_datadir}/vala/vapi/plank.deps
%{_datadir}/vala/vapi/plank.vapi

%changelog
