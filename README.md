<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="art/repo/banner-dark.svg">
    <img alt="Oniscus" src="art/repo/banner-light.svg" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/arthurcvieira/oniscus/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/arthurcvieira/oniscus?include_prereleases&sort=semver&style=flat-square&label=release&color=F7C948&labelColor=1C2026"></a>
  <a href="https://github.com/arthurcvieira/oniscus/releases"><img alt="Downloads" src="https://img.shields.io/github/downloads/arthurcvieira/oniscus/total?style=flat-square&label=downloads&color=F7C948&labelColor=1C2026"></a>
  <a href="https://github.com/arthurcvieira/oniscus/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/arthurcvieira/oniscus?style=flat-square&logo=github&label=stars&color=F7C948&labelColor=1C2026"></a>
  <a href="LICENSES.md"><img alt="License" src="https://img.shields.io/badge/license-GPL--3.0--or--later-4CC27A?style=flat-square&labelColor=1C2026"></a>
  <br>
  <img alt="Based on openSUSE Tumbleweed" src="https://img.shields.io/badge/based%20on-openSUSE%20Tumbleweed-73BA25?style=flat-square&labelColor=1C2026">
  <img alt="XFCE + i3" src="https://img.shields.io/badge/desktop-XFCE%20%2B%20i3-9AA4AF?style=flat-square&labelColor=1C2026">
  <a href="https://github.com/arthurcvieira/oniscus/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/arthurcvieira/oniscus?style=flat-square&label=last%20commit&color=9AA4AF&labelColor=1C2026"></a>
</p>

<p align="center">
  <b>A cozy Linux that just works.</b><br>
  <a href="https://github.com/arthurcvieira/oniscus/releases/latest">Download</a> ·
  <a href="docs/onis.md">The onis command</a> ·
  <a href="docs/development.md">Build it yourself</a> ·
  <a href="README.pt-BR.md">Português</a>
</p>

---

**Oniscus** is a Linux distribution built on openSUSE Tumbleweed, with a warm,
retro desktop that is ready the moment you log in. XFCE takes care of the
everyday things (settings, power, notifications, Wi-Fi, disks and files) while
i3 keeps your windows neatly tiled. No setup marathon, no hunting for configs:
boot it, and it feels like home.

It's named after *Oniscus*, the common woodlouse: small, sturdy and happiest in
a cozy corner. That little isopod is our mascot, and you'll find it waving from
the menu button and the terminal.

## Why Oniscus

- **Ready from the first boot.** Panel, dock, launcher, theme, prompt and apps
  are all set up. You can start working right away.
- **Rolling, but safe.** Tumbleweed brings the newest software, and every
  system update takes a [snapper](https://github.com/openSUSE/snapper) snapshot
  first. If something feels off, roll back in one command.
- **Tiling without the homework.** i3 arranges your windows, XFCE handles the
  rest. You get the speed of a tiling window manager with the comfort of a
  full desktop.
- **One friendly command.** `onis` is the welcome screen and the system's Swiss
  army knife: install apps, update, take snapshots, change colors and more.
- **Official sources only.** Packages come from the official Tumbleweed
  repositories, and Oniscus's own pieces are regular RPMs from the
  [Open Build Service](https://build.opensuse.org/project/show/home:oniscus), so
  they update together with the rest of the system.
- **Speaks your language.** English by default, with Brazilian Portuguese built
  in. The Oniscus tools follow your `LANG`.

## A look around

| | |
|---|---|
| **Login** | Ly, a calm terminal-style greeter in the Oniscus colors |
| **Top bar** | menu, focused app, Wi-Fi, battery, clock and search |
| **Bottom bar** | a floating pill with your workspaces, CPU and RAM |
| **Dock** | Plank on the left, stepping aside when a window comes near |
| **Launcher** | rofi, one keystroke away |
| **Look** | Xi3 Retro: a dark, 2000s-inspired theme with a warm yellow accent, Oxygen icons and Noto Sans |
| **Motion** | picom animations as windows open, close and resize |
| **Terminal** | Starship prompt and fastfetch with the mascot |
| **Media** | VLC for video and music, PipeWire for sound |
| **Installer** | Calamares, with optional NVIDIA drivers and extra codecs |

## Meet `onis`

`onis` opens when you log in and lives one shortcut away
(<kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>Space</kbd>). Every menu item is also a
command:

```bash
onis install gimp        # apps from Tumbleweed and Flathub, by category
onis update              # system + Flatpak, with a restore point first
onis snapshot list       # browse and roll back restore points
onis accent "#7FB4CA"    # repaint the accent color everywhere
onis drivers nvidia      # NVIDIA driver or extra codecs, any time
onis agent               # ask your AI coding agent to help with the system
onis doctor              # a quick, read-only health report
```

Prefer the long name? `oniscus` works too. See the [full guide](docs/onis.md)
or run `onis help`.

## Handy shortcuts

| Keys | What it does |
|---|---|
| <kbd>Super</kbd>+<kbd>Space</kbd> | open an app |
| <kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>Space</kbd> | the `onis` menu |
| <kbd>Super</kbd>+<kbd>Enter</kbd> | terminal |
| <kbd>Super</kbd>+<kbd>E</kbd> | files (Thunar) |
| <kbd>Super</kbd>+<kbd>1</kbd>…<kbd>9</kbd> | switch workspace |
| <kbd>Super</kbd>+<kbd>Shift</kbd>+<kbd>Q</kbd> | close a window |
| <kbd>Super</kbd>+<kbd>Shift</kbd>+<kbd>Space</kbd> | float or tile a window |
| <kbd>Super</kbd>+<kbd>F</kbd> | fullscreen |
| <kbd>Super</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> | lock the screen |

`onis keys` lists them all and lets you change them.

## Get Oniscus

1. Download the latest ISO from
   [Releases](https://github.com/arthurcvieira/oniscus/releases/latest).
2. Write it to a USB stick with Fedora Media Writer, balenaEtcher or
   `sudo dd if=oniscus.iso of=/dev/sdX bs=4M status=progress`.
3. Boot from the stick (UEFI) and log in as `live`, password `live`. The
   login screen reminds you.
4. Pick **Install Oniscus** in `onis` or the menu. The installer asks for your
   language, keyboard and time zone, and offers NVIDIA drivers and extra codecs
   if you want them.

Already installed? `onis update` keeps everything, Oniscus included, up to date.

Want to build the ISO yourself or hack on the desktop? Head to
[docs/development.md](docs/development.md) and [docs/packages.md](docs/packages.md).

## License

Oniscus's own files are [GPL-3.0-or-later](COPYING), and the artwork (mascot,
logos, wallpaper) is CC BY-SA 4.0. Everything else comes from the official
openSUSE Tumbleweed repositories under its own license. Details in
[LICENSES.md](LICENSES.md).

<sub>Oniscus is an independent project, based on openSUSE Tumbleweed and not
affiliated with or endorsed by the openSUSE Project.</sub>
