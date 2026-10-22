#
# spec file for the Oniscus packages
#
# Copyright (c) 2026 the Oniscus contributors
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Builds the parts of Oniscus that are not in openSUSE Tumbleweed, so installed
# systems get them with `zypper dup` (`onis update`) like any other package.
# Which file goes to which package is listed in packaging/manifest.tsv.
#

Name:           oniscus
Version:        0.1.0
Release:        0
Summary:        Oniscus distribution files
License:        GPL-3.0-or-later AND CC-BY-SA-4.0
URL:            https://github.com/arthurcvieira/oniscus
Source0:        %{name}-%{version}.tar.xz
BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
%{?systemd_ordering}

%description
Source package for the Oniscus distribution (openSUSE Tumbleweed with XFCE and
i3). It builds onis, oniscus-branding and oniscus-desktop.

%package -n onis
Summary:        Oniscus welcome screen and system menu
License:        GPL-3.0-or-later
Requires:       bash
Requires:       coreutils
Requires:       feh
Requires:       flatpak
Requires:       gum
Requires:       i3
Requires:       libnotify-tools
Requires:       oniscus-branding = %{version}
Requires:       procps
Requires:       rofi
Requires:       rpm
Requires:       util-linux
Requires:       xdg-utils
Requires:       xfce4-terminal
Requires:       xfconf
Requires:       zypper
Recommends:     fastfetch
Recommends:     man
Recommends:     pciutils
Recommends:     snapper
Provides:       oniscus-onis = %{version}

%description -n onis
onis (alias oniscus) is the Oniscus Swiss army knife for the terminal: welcome
screen, app installer, updates, snapshots, accent color, wallpapers, i3
shortcuts, drivers and AI agent setup.

%package -n oniscus-branding
Summary:        Oniscus name, logo, mascot, wallpaper and themes
License:        GPL-3.0-or-later AND CC-BY-SA-4.0
# Boot splash with the mascot (script theme)
Requires:       plymouth-plugin-script

%description -n oniscus-branding
The Oniscus identity: os-release name (kept by a boot service, since
openSUSE-release owns /etc/os-release), mascot logo for the menu and fastfetch,
wallpaper, the boot splash (Plymouth theme "oniscus", turn it on with
"plymouth-set-default-theme -R oniscus"), and the Xi3 Retro GTK and Plank themes.

%package -n oniscus-desktop
Summary:        Oniscus desktop defaults (XFCE with i3)
License:        GPL-3.0-or-later
Requires:       dconf
Requires:       gsettings-backend-dconf
Requires:       feh
Requires:       i3
Requires:       onis = %{version}
Requires:       oniscus-branding = %{version}
Requires:       picom
Requires:       plank
Requires:       polybar
Requires:       rofi
Requires:       starship
Requires:       xdotool
Requires:       xfce4-battery-plugin
Requires:       xfce4-genmon-plugin
Requires:       xfce4-panel
Requires:       xfce4-session
Requires:       xfce4-whiskermenu-plugin
Recommends:     fastfetch

%description -n oniscus-desktop
System defaults for the Oniscus session: XFCE settings, panel layout, default
apps, Starship prompt, Plank defaults, the Ly session entry and the user
configs copied to new accounts (i3, Polybar, picom, fastfetch, Plank).
Defaults live in /etc/xdg/oniscus, which the Oniscus session puts first in
XDG_CONFIG_DIRS. Files changed by the admin are kept on update (.rpmnew).

%prep
%autosetup -p1

%build
# Nothing to build: shell scripts, configs and artwork.

%install
# Install every manifest entry and write one file list per package.
tab=$(printf '\t')
while IFS=$tab read -r pkg src dst flags; do
    case "$pkg" in ''|'#'*) continue ;; esac
    mode=0644
    case ",$flags," in *,exec,*) mode=0755 ;; esac
    attr=
    case ",$flags," in *,config,*) attr='%%config(noreplace) ' ;; esac
    if [ -d "$src" ]; then
        (cd "$src" && find . -type f ! -name .keep) | sed 's#^\./##' | while read -r f; do
            install -D -m "$mode" "$src/$f" "%{buildroot}$dst/$f"
            echo "$attr$dst/$f" >> "$pkg.files"
        done
        case ",$flags," in *,own,*)
            mkdir -p "%{buildroot}$dst"
            (cd "%{buildroot}$dst" && find . -type d) | sed "s#^\.#%%dir $dst#; s#/\$##" >> "$pkg.files" ;;
        esac
    else
        install -D -m "$mode" "$src" "%{buildroot}$dst"
        # Man pages get compressed by the build root policy scripts
        case "$dst" in %{_mandir}/*) dst="$dst*" ;; esac
        echo "$attr$dst" >> "$pkg.files"
    fi
done < packaging/manifest.tsv

# Parent directories that belong to Oniscus (shared by the packages)
for pkg in onis oniscus-branding oniscus-desktop; do
    sed -e 's/^%%[a-z(]*[a-z)]* //' "$pkg.files" | while read -r path; do
        d=$(dirname "$path")
        while case "$d" in */oniscus|*/oniscus/*) true ;; *) false ;; esac; do
            echo "%%dir $d"
            d=$(dirname "$d")
        done
    done >> "$pkg.files"
    sort -u -o "$pkg.files" "$pkg.files"
done

# "oniscus" is the long alias of onis
ln -s onis %{buildroot}%{_bindir}/oniscus
echo %{_bindir}/oniscus >> onis.files

# Enable the os-release service on first install
mkdir -p %{buildroot}%{_presetdir}
echo 'enable oniscus-os-release.service' > %{buildroot}%{_presetdir}/90-oniscus.preset
echo %{_presetdir}/90-oniscus.preset >> oniscus-branding.files

%pre -n oniscus-branding
%{?service_add_pre:%service_add_pre oniscus-os-release.service}

%post -n oniscus-branding
%{?service_add_post:%service_add_post oniscus-os-release.service}
# Apply the name now instead of at the next boot
[ -x /usr/libexec/oniscus/os-release ] && /usr/libexec/oniscus/os-release || :

%preun -n oniscus-branding
%{?service_del_preun:%service_del_preun oniscus-os-release.service}

%postun -n oniscus-branding
%{?service_del_postun_without_restart:%service_del_postun_without_restart oniscus-os-release.service}

%post -n oniscus-desktop
command -v dconf >/dev/null 2>&1 && dconf update || :

%postun -n oniscus-desktop
command -v dconf >/dev/null 2>&1 && dconf update || :

%files -n onis -f onis.files
%license COPYING
%doc docs/onis.md docs/onis.pt-BR.md

%files -n oniscus-branding -f oniscus-branding.files
%license COPYING LICENSES.md LICENSES.pt-BR.md

%files -n oniscus-desktop -f oniscus-desktop.files
%license COPYING
%doc README.md README.pt-BR.md

%changelog
