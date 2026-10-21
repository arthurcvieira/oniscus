# Oniscus licenses

[Português](LICENSES.pt-BR.md)

Everything Oniscus distributes can be published and redistributed freely.

## Files created for Oniscus

| What | License |
|---|---|
| Configs, scripts, KIWI description, "Xi3 Retro" GTK theme, Plank theme | GPL-3.0-or-later (text in `COPYING`) |
| Wallpaper `xi3.jpg` and the script that generates it (`art/wallpaper.py`) | CC BY-SA 4.0 |
| Mascot, menu icon and terminal logo (`art/branding/`), including the reference photo | CC BY-SA 4.0 |

The retro look is **inspired by** the Aqua/Tiger era, but it is drawn from scratch
with CSS gradients. No Apple icon, image, font or name is used. The names "Aqua",
"Mac OS X", "Tiger" and the Apple logo don't appear in any distributed file.

## Third-party components (all from the official Tumbleweed repositories)

| Component | License |
|---|---|
| i3 | BSD-3-Clause |
| XFCE (panel, session, Thunar, etc.) | GPL-2.0-or-later / LGPL |
| picom | MPL-2.0 and MIT |
| Polybar | MIT |
| Plank | GPL-3.0-or-later |
| rofi | MIT |
| Ly | WTFPL |
| Starship | ISC |
| fastfetch | MIT |
| gum (welcome app) | MIT |
| Flatpak | LGPL-2.1-or-later (apps installed from Flathub keep their own licenses and are not shipped in the ISO) |
| Oxygen icons | LGPL-3.0-or-later |
| Noto fonts | SIL Open Font License 1.1 |
| VLC | GPL-2.0-or-later (libVLC is LGPL-2.1-or-later). Only the openSUSE build goes in the ISO; `vlc-codecs` comes from Packman during install, never in the ISO |
| Firefox | MPL-2.0 (the Firefox trademark has its own rules, but openSUSE's package can be redistributed as is) |

## Trademarks

- "openSUSE" and the openSUSE logo are SUSE trademarks. Oniscus may say "based on
  openSUSE Tumbleweed" (it does in `PRETTY_NAME`, the READMEs and the welcome
  app), but never uses the name or logo as its own brand. What the image does:
  - installs `branding-upstream`, `plymouth-branding-upstream` and
    `MozillaFirefox-branding-upstream` instead of the openSUSE variants;
  - removes and locks `grub2-`, `wallpaper-`, `xfce4-`, `calamares-` and the other
    `*-branding-openSUSE` packages, so updates don't bring them back;
  - sets `NAME="Oniscus"` and `ID=oniscus` (with `ID_LIKE=opensuse-tumbleweed`) in
    `/etc/os-release`, kept by `oniscus-os-release.service` because
    `openSUSE-release` rewrites it on updates;
  - uses no GRUB theme (`GRUB_DISTRIBUTOR="Oniscus"`), its own Calamares branding,
    its own wallpaper, menu icon and Ly greeter.
  - The repository files and package names (`repo-oss`, `openSUSE-release`,
    `download.opensuse.org`) stay as they are: they describe where packages come
    from, which the guidelines allow.
- Before publishing, confirm with `rpm -qa --qf '%{NAME} %{LICENSE}\n'` inside the
  image that no package from the `non-oss` repository forbids redistribution. If in
  doubt, remove `repo-non-oss` from `config.kiwi`.
