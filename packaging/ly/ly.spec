#
# spec file for the ly package (Oniscus)
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Ly is not in openSUSE Tumbleweed, so Oniscus builds it in its own repository
# (home:oniscus on build.opensuse.org). Zig fetches dependencies over the
# network, which OBS builds don't have, so their sources come in a vendor
# tarball made by packaging/ly/make-vendor.sh.
#

Name:           ly
Version:        1.4.1
Release:        0
Summary:        TUI display manager
License:        WTFPL
URL:            https://codeberg.org/fairyglade/ly
Source0:        https://github.com/fairyglade/ly/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.zst
# Center the big clock from the first frame (it started at the middle of the screen)
Patch0:         ly-center-bigclock.patch
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(xcb)
BuildRequires:  zig >= 0.16
BuildRequires:  zstd
Requires:       xauth
Requires:       xorg-x11-server
%{?systemd_ordering}

%description
Ly is a lightweight text-based display manager (login screen) for Linux and
BSD, with X11, Wayland and shell sessions and an optional animated background.

%prep
%autosetup -p1 -n %{name}-%{version}
tar --zstd -xf %{SOURCE1}

%build
# Built in the install step (zig build installs and builds in one go)

%install
zig build installexe \
    -Doptimize=ReleaseSafe \
    -Dcpu=baseline \
    -Ddest_directory=%{buildroot} \
    -Dinit_system=systemd
# The example config is the same file as config.ini
rm -f %{buildroot}%{_sysconfdir}/ly/config.ini.example

%pre
%service_add_pre ly@tty2.service

%post
%service_add_post ly@tty2.service

%preun
%service_del_preun ly@tty2.service

%postun
%service_del_postun ly@tty2.service

%files
%license license.md
%doc readme.md
%{_bindir}/ly
%dir %{_sysconfdir}/ly
%config(noreplace) %{_sysconfdir}/ly/config.ini
%{_sysconfdir}/ly/startup.sh
%{_sysconfdir}/ly/setup.sh
%{_sysconfdir}/ly/example.dur
%{_sysconfdir}/ly/custom-sessions
%{_sysconfdir}/ly/lang
%config(noreplace) %{_sysconfdir}/pam.d/ly
%config(noreplace) %{_sysconfdir}/pam.d/ly-autologin
%{_unitdir}/ly@.service
%{_unitdir}/ly-kmsconvt@.service

%changelog
