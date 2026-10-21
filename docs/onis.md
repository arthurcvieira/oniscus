# onis: welcome screen and system Swiss army knife

[Português](onis.pt-BR.md)

`onis` is a terminal app (bash + [gum](https://github.com/charmbracelet/gum))
inspired by the Omarchy menu. Every menu item is also an English subcommand.
`oniscus` is a longer alias of the same command.
Screens: https://claude.ai/artifact/QfMMoxgQ4zfsemw85F8gTq

## Files

| File | What |
|---|---|
| `kiwi/root/usr/local/bin/onis` | the app |
| `kiwi/root/usr/share/oniscus/catalog.tsv` | install catalog by category (format documented in the file) |
| `kiwi/root/usr/share/oniscus/agent/AGENTS.md` | guide for AI agents (config map, safety rules, recipes) |
| `kiwi/root/usr/share/oniscus/agent/skills/oniscus/SKILL.md` | the same guide as an agent skill |
| `kiwi/root/etc/profile.d/oniscus-local-bin.sh` | puts `~/.local/bin` on PATH (agent installers use it) |
| `kiwi/root/etc/profile.d/oniscus-starship.sh` | uses the user's prompt copy after an accent change |

Packages added to `config.kiwi`: `gum`, `xdg-utils`, `libnotify-tools`, `flatpak`.

## How it opens

- At every login, in a floating terminal titled "Oniscus Welcome"
  (`exec onis welcome --autostart` in the i3 config). Turn it off in
  Preferences or with `onis welcome off`.
- `Super+Alt+Space` opens the same menu in rofi (`onis menu`); actions that need a
  terminal open a floating one. `Super+Space` is the app launcher.
- On the live ISO, the first item is "Install Oniscus to this computer" (`pkexec calamares`).

## Language

English is the default. When the session `LANG` starts with `pt`, the menu text
is shown in Brazilian Portuguese. Commands, file names, code comments, the agent
guide and `onis doctor` output are always in English. Every string lives in
the script as `t "English" "Português"`.

## Commands

```
onis                           welcome screen
onis menu                      same menu in rofi
onis install [app]             catalog by category, or search Tumbleweed + Flathub
onis uninstall [--purge] [app]   remove an app; --purge also removes orphaned deps, user data and cache
onis uninstall --cleanup       remove orphaned packages, unused Flatpak runtimes and package caches
onis agent [ask "task"]        default AI agent with the Oniscus guide
onis agent default [command]   claude, codex, gemini, opencode or hermes
onis agent crashes on|off      offer the agent when an app crashes
onis doctor                    read-only system report
onis accent [#hex|default]     accent color across the theme
onis wallpaper [--apply]       pick or apply the wallpaper
onis keys [show|change|new|remove|restore]
onis update [--yes]            zypper dup (with snapper restore point) + Flatpak apps (user and system)
onis drivers [nvidia|codecs]   NVIDIA driver and Packman codecs (optional, same commands as the installer)
onis snapshot [list|create|diff|delete|rollback]  snapper restore points
onis restart-bars | about | welcome on|off
onis help [command]            full help; also onis <command> --help
```

## Help and manual

- `onis help` lists every command grouped by area; `onis help <command>` and
  `onis <command> --help` show the details of one command, in the menu language.
- `man onis` (English) and, with a Portuguese session, `man onis` in pt_BR.
  Files: `kiwi/root/usr/local/share/man/man1/onis.1` and
  `kiwi/root/usr/local/share/man/pt_BR/man1/onis.1` (plus `oniscus.1` aliases).
  The `man` package was added to `config.kiwi`.

## Snapshots

`onis snapshot` is a front end for snapper on `/` (the user's `/home` is a
separate subvolume and is never touched):

- `list` shows snapshots newest first, `*` running, `+` next boot.
- `create [description]`, `diff <n> [m]` (files changed, default against now),
  `delete <n>` (refuses the running and default snapshots).
- `rollback <n>` runs `snapper rollback`, explains that the system returns to
  that snapshot at the next restart and that the current state is kept, then
  offers to restart.
- All of it uses sudo; on the live ISO there are no snapshots and onis says so.

## Install

- Categories: AI agents, Browsers, Office, Design, Development, Communication,
   Media, Games, Utilities. Rows come from `catalog.tsv`.
- Sources, in order of preference: Tumbleweed repositories (`zypper`), Flathub
  (`flatpak --user`, no sudo; the flathub remote is added per user on first use),
  and for AI agents the project's official installer or npm into `~/.local`.
  The exact command is shown before it runs.
- "Install another package" searches `zypper search` and `flatpak search` together.
- Claude Desktop is not listed: its Linux build is an Ubuntu/Debian `.deb` only.

## Uninstall

- Lists AI agents, Flatpak apps and system packages in one filtered list.
- "Remove the app only" or "Remove and purge": purge uses `zypper remove --clean-deps`
  (orphaned dependencies), `flatpak uninstall --delete-data` + `--unused`, and offers
  to delete the app's folders in `~/.config`, `~/.local/share` and `~/.cache`.
- Before removing a system package it runs a zypper dry run, shows the list and
  refuses if anything in the protected list (kernel, systemd, zypper, i3, XFCE,
  Ly, gum, flatpak...) would go.
- "Clean up" removes `zypper packages --unneeded`, runs `zypper clean --all`,
  `flatpak uninstall --unused` and prunes old i3 config backups.

## AI agents at system level

Like Omarchy, agents can take care of the machine itself:

- The guide is linked as `AGENTS.md`, `CLAUDE.md` and `GEMINI.md` in
  `~/.local/share/oniscus/agent/` (the agent's working folder), and the skill into
  `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`,
  `~/.config/opencode/skills` and `~/.hermes/skills` (`onis agent link`, at every login).
- `Super+Ctrl+Shift+a` or `onis agent` opens the default agent and asks what to solve.
- `onis agent watch-crashes` (started by i3) follows the user journal and shows
  an "Ask the agent" notification when an app dumps core.
- Safety: agents run as the user, never as root. The guide requires a yes before
  any `sudo`, a snapper snapshot before system changes, and official sources only.
  Unlike Omarchy, Oniscus does not start agents in "don't ask" mode. On the live ISO
  the `live` user has passwordless sudo, so the user's yes inside the agent is the
  only gate there.

## Accent color

Swaps Yellow/Honey/Amber by key, not by value (so ANSI yellow and other palette
colors stay put) in the user's copies: the `client.focused` line of the i3
config, Polybar `accent`, fastfetch colors, `~/.config/oniscus/starship.toml`, a
GTK theme copy in `~/.local/share/themes/Xi3-Retro` and the terminal cursor
(xfconf). The Ly login screen changes only if the user accepts (sudo). State
lives in `~/.config/oniscus/`.

## i3 shortcuts

Edits `~/.config/i3/config`, keeps a `config.oniscus-<date>` backup, refuses a
combination already in use, validates with `i3 -C` and restores the backup if
i3 rejects the change.

## To check on the first real build

- Catalog package names (`zypper info`), especially `ollama`, `steam` (non-oss),
  `xournalpp`, `docker`, `chromium`.
- `zypper install /usr/bin/npm` resolves the npm package.
- `journalctl --user` receives systemd-coredump messages; `notify-send --action`
  works with xfce4-notifyd.
- Gemini CLI and Hermes read the skill folders above.
- rofi accepts the `-theme-str` values used by `onis menu`.
