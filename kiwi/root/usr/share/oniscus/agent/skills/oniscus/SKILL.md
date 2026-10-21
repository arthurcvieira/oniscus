---
name: oniscus
description: Diagnose, fix and customize this Oniscus computer (openSUSE Tumbleweed, XFCE + i3, Polybar, Plank, Ly). Use when the user talks about problems with the machine, shortcuts, theme, bars, network, sound, packages, crashes or updates.
---

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Oniscus

This computer runs Oniscus. Before acting:

1. Read the full guide at `/usr/share/oniscus/agent/AGENTS.md` (config map, safety
   rules and recipes).
2. If the user reported a problem, run `onis doctor` and start from its report.

Rules that always apply, even before reading the guide:

- You run as the user. No command with `sudo` without explaining it and getting a yes.
- Before changing the system, make a restore point: `sudo snapper create -d "before: ..."`.
- Change the user's config (`~/.config`), not the system's, and back it up first.
- Packages only from the official Tumbleweed repositories or Flathub; update with `sudo zypper dup`.
- i3 config: validate with `i3 -C -c ~/.config/i3/config` before `i3-msg reload`.
- Reply in the user's language (`$LANG`) and finish by saying how to undo.
