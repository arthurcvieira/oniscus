# Oniscus packages and repository

[Português](packages.pt-BR.md)

Tumbleweed is a rolling release, so Oniscus's own files must update the same way
the rest of the system does. They are built as RPM packages on the
[Open Build Service](https://build.opensuse.org) (OBS), the free build service run
by openSUSE, and published in an Oniscus repository. Installed systems get new
versions with `onis update` (which runs `zypper dup`), with no reinstall.

## Packages

| Package | Contents |
|---|---|
| `onis` | the `onis` command (`/usr/bin/onis`, alias `oniscus`), man pages, app catalog, AI agent guide |
| `oniscus-branding` | os-release name and its boot service, logo, menu icon, wallpaper, Xi3 Retro GTK and Plank themes |
| `oniscus-desktop` | system defaults (XFCE settings, panel, default apps, Starship, Plank), the Ly session entry, the configs copied to new users, and `Requires` on the desktop stack (i3, Polybar, picom, Plank, rofi...) |

`packaging/manifest.tsv` says which file of `kiwi/root` goes into which package
and where. The spec (`packaging/oniscus.spec`) and `build.sh` both read it, so
adding a file to a package is one line there.

### How updates reach users

- Files in `/usr` (onis, themes, logo, wallpaper) are replaced on every update.
- Files in `/etc` are `%config(noreplace)`: if the admin changed one, the update
  keeps their file and saves the new one next to it as `.rpmnew`.
- System defaults live in `/etc/xdg/oniscus` instead of `/etc/xdg`, so they never
  clash with files owned by XFCE or openSUSE packages. The Oniscus session starts
  XFCE with `XDG_CONFIG_DIRS=/etc/xdg/oniscus:/etc/xdg`.
- New dependencies arrive too: if `oniscus-desktop` starts requiring a new
  package, `zypper dup` installs it.
- Limit: files in `/etc/skel` are copied only when a user is created. Updates to
  them reach new users, not the existing `~/.config` (i3, Polybar, picom,
  fastfetch). Moving those to system-wide defaults is a later step.

### Not packaged (image only)

`/etc/ly/config.ini` (owned by the `ly` package), `/etc/dconf/profile/user`, the
Calamares installer files and the "Install Oniscus" launcher. They stay in
`kiwi/root`. In the Release image `/etc/bash.bashrc.local` is a stub that sources
`/usr/share/oniscus/shell/bashrc.sh` from `oniscus-desktop`.

## Two ways to build the ISO

| | `./build.sh` (Dev, default) | `PROFILE=Release ./build.sh` |
|---|---|---|
| Oniscus files | copied from `kiwi/root` | installed from the Oniscus repository |
| Updates on installed systems | no (files are not owned by any package) | yes, with `onis update` |
| Use it for | trying changes before releasing them | the ISO you publish |

Release mode copies `kiwi/` to `out/description`, removes the files listed in the
manifest, adds `packaging/release-overlay/`, and builds with the `Release` KIWI
profile (Oniscus repository + `onis`, `oniscus-branding`, `oniscus-desktop`).

## One-time setup (Arthur)

Names below assume the GitHub repository `arthurcvieira/oniscus` and the OBS
project `home:oniscus` (OBS user `oniscus`). If you choose others, replace them in
`packaging/obs/*`, `packaging/oniscus.spec` (URL) and `kiwi/config.kiwi`
(repository path).

1. **GitHub**: create the repository and push the contents of `distro/` to its
   root (`kiwi/`, `packaging/`, `docs/`... at the top level). Tag the first
   release: `git tag v0.1.0 && git push --tags`.
2. **OBS account**: sign up at https://build.opensuse.org (it is the openSUSE
   account, free). Create the user `oniscus`: its home project `home:oniscus`
   holds the Oniscus packages.
3. **osc** (OBS command line), on an openSUSE machine:
   `sudo zypper install osc obs-service-obs_scm obs-service-tar obs-service-recompress obs-service-set_version`
4. **Project and package**:
   ```sh
   osc meta prj home:oniscus -F packaging/obs/project-meta.xml
   osc meta pkg home:oniscus oniscus -F packaging/obs/package-meta.xml
   osc checkout home:oniscus/oniscus && cd home:oniscus/oniscus
   cp <repo>/packaging/obs/_service .
   osc add _service && osc commit -m "Build from GitHub"
   ```
   OBS runs the service (fetches GitHub, takes the spec) and builds. Follow it at
   https://build.opensuse.org/package/show/home:oniscus/oniscus
5. **Rebuild on every push**: create a token and add it as a GitHub webhook.
   ```sh
   osc token --create --operation runservice home:oniscus oniscus
   ```
   In GitHub: Settings, Webhooks, Add webhook. Payload URL
   `https://build.opensuse.org/trigger/webhook?id=<token id>`, content type
   `application/json`, secret = the token string, event "Just the push event".
6. **Repository key** for the Release ISO (OBS signs the repository):
   `osc signkey home:oniscus > packaging/oniscus-repo.asc`, then
   commit it. `build.sh` passes it to KIWI, which trusts it inside the image.

The repository is then at
`https://download.opensuse.org/repositories/home:/oniscus/openSUSE_Tumbleweed/`.

## Releasing an update

1. Change the files in `kiwi/root` (and the manifest if a file is new).
2. Add an entry to `packaging/oniscus.changes` (`osc vc` writes the header).
3. Push. The webhook rebuilds; the version is the last tag plus commits
   (`0.1.0+git3.abc1234`). Tag `vX.Y.Z` for a named release.
4. Users get it with `onis update`. OBS rebuilds the packages against new
   Tumbleweed snapshots by itself.

## Ly and Plank Reloaded

Ly (the login screen) and Plank (the dock) are not in Tumbleweed, so the Oniscus
repository builds them too, as two more packages next to `oniscus`. Both ISO
profiles install them from there.

| Package | Source | Spec |
|---|---|---|
| `ly` | [Ly](https://codeberg.org/fairyglade/ly), built with Tumbleweed's Zig | `packaging/ly/` |
| `plank-reloaded` | [Plank Reloaded](https://github.com/zquestz/plank-reloaded), the maintained Plank fork (same `plank` command, settings and themes; provides `plank`) | `packaging/plank-reloaded/` |

OBS builds have no network, and Zig downloads its dependencies while building.
`packaging/ly/ly-<version>-vendor.tar.zst` holds those dependencies; after
changing Ly's `Version:`, make a new one with `packaging/ly/make-vendor.sh` (needs
zig, curl and zstd), commit it and update the file name in `packaging/ly/_service`.

To add them to OBS (once; the specs must already be on `main`):

```sh
for p in ly plank-reloaded; do
    osc meta pkg home:oniscus $p -F - <<META
<package name="$p" project="home:oniscus"><title>$p</title><description/></package>
META
    osc checkout home:oniscus/$p && cp <repo>/packaging/$p/_service home:oniscus/$p/
    (cd home:oniscus/$p && osc add _service && osc commit -m "Build from GitHub")
done
```

Or in the web interface: in `home:oniscus`, "Create package" (`ly`), then "Add
file" and upload `packaging/ly/_service`; the same for `plank-reloaded`.
`osc` also needs `obs-service-download_files` for local builds. The ISO workflow
(`.github/workflows/iso.yml`) builds both packages from these specs, without
network, before every test ISO.

## Adding the repository to an already installed system

Systems installed from a Dev ISO have the files but no repository. To switch:

```sh
sudo zypper addrepo -f https://download.opensuse.org/repositories/home:/oniscus/openSUSE_Tumbleweed/ oniscus
sudo zypper refresh   # accept the Oniscus key
sudo zypper install --force-resolution onis oniscus-branding oniscus-desktop
```

The packages then own the files in `/usr`. Old copies in `/usr/local/bin` should
be removed (`sudo rm /usr/local/bin/{onis,oniscus,xi3-active-app}`), or they keep
shadowing the packaged ones.

## Checked so far

The spec builds with `rpmbuild` (noarch, three packages, file lists and
`%config` flags as described). Not yet checked against a real Tumbleweed: the
build on OBS (openSUSE macros, rpmlint), file conflicts with Tumbleweed
packages (`/etc/starship.toml`, `/etc/profile.d/oniscus-*`), and a Release ISO
build.
