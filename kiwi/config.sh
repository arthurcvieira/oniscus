#!/bin/bash
# Run by KIWI inside the image after the packages are installed.
set -euxo pipefail

test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

echo "Configuring Oniscus..."

# Services
systemctl enable NetworkManager
# Greeter: Ly on tty2 instead of openSUSE's display-manager
systemctl disable display-manager.service || true
if [ -f /usr/lib/systemd/system/ly@.service ]; then
    systemctl enable ly@tty2.service
else
    systemctl enable ly.service
fi
systemctl disable getty@tty2.service || true
systemctl set-default graphical.target

if [ -f /etc/sysconfig/windowmanager ]; then
    sed -i 's/^DEFAULT_WM=.*/DEFAULT_WM="xfce"/' /etc/sysconfig/windowmanager
fi

# Languages: English by default, Brazilian Portuguese also supported.
# Users switch with LANG=pt_BR.UTF-8 (e.g. in ~/.config/locale.conf or Xfce settings).
echo 'LANG=en_US.UTF-8' > /etc/locale.conf

# Branding: Oniscus name in os-release (and so in /etc/issue, fastfetch, GRUB),
# no openSUSE boot theme, and locks so updates don't bring openSUSE art back.
cp /usr/lib/os-release.oniscus /etc/os-release.tmp && mv -f /etc/os-release.tmp /etc/os-release
chmod 0755 /usr/libexec/oniscus/os-release
systemctl enable oniscus-os-release.service
if [ -f /etc/default/grub ]; then
    sed -i -e 's/^GRUB_DISTRIBUTOR=.*/GRUB_DISTRIBUTOR="Oniscus"/' \
           -e '/^GRUB_THEME=/d' -e '/^GRUB_BACKGROUND=/d' /etc/default/grub
    grep -q '^GRUB_DISTRIBUTOR=' /etc/default/grub || echo 'GRUB_DISTRIBUTOR="Oniscus"' >> /etc/default/grub
fi
# Removing xfce4-branding-openSUSE would also delete our overlay files at the
# same paths in /etc/xdg, so keep a copy and put it back afterwards.
cp -a /etc/xdg /tmp/oniscus-xdg
for pkg in branding-openSUSE grub2-branding-openSUSE plymouth-branding-openSUSE \
           wallpaper-branding-openSUSE xfce4-branding-openSUSE \
           MozillaFirefox-branding-openSUSE calamares-branding-openSUSE; do
    rpm -q "$pkg" && rpm -e --nodeps "$pkg" || true
    zypper --non-interactive addlock "$pkg" || true
done
cp -a /tmp/oniscus-xdg/. /etc/xdg/ && rm -rf /tmp/oniscus-xdg
find /etc/xdg -name '*.rpmsave' -delete
: > /etc/motd

# Passwordless sudo for the live user (live ISO only)
echo "live ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/10-live
chmod 0440 /etc/sudoers.d/10-live

# Copy /etc/skel to the live user, which was created before the overlay
if [ -d /home/live ]; then
    cp -a /etc/skel/. /home/live/
    chown -R live:users /home/live
fi

# Oniscus scripts (the overlay can drop the executable bit). In the Release
# profile they come from the onis/oniscus-desktop packages in /usr/bin instead.
if [ -e /usr/local/bin/onis ]; then
    chmod 0755 /usr/local/bin/*
    # "oniscus" is a long alias of the onis command
    ln -sfn onis /usr/local/bin/oniscus
fi

# System dconf defaults (Plank)
dconf update

# Remove xfwm4 and xfdesktop in case a package pulled them back in
rpm -q xfwm4 && rpm -e --nodeps xfwm4 || true
rpm -q xfdesktop && rpm -e --nodeps xfdesktop || true

exit 0
