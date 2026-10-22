#!/bin/bash
# Builds the Oniscus live ISO. Run it on openSUSE (Tumbleweed or Leap) with:
#   sudo zypper install python3-kiwi kiwi-systemdeps
#
#   ./build.sh                  Dev profile: Oniscus files from kiwi/root
#   PROFILE=Release ./build.sh  Release profile: Oniscus files from the Oniscus
#                               package repository (see docs/packages.md)
set -euo pipefail

cd "$(dirname "$0")"
OUT=${OUT:-out}
PROFILE=${PROFILE:-Dev}
# Public key of the Oniscus repository on build.opensuse.org (both profiles:
# Ly and Plank Reloaded come from there). Downloaded when missing.
KEY=${KEY:-packaging/oniscus-repo.asc}
KEY_URL=https://download.opensuse.org/repositories/home:/oniscus/openSUSE_Tumbleweed/repodata/repomd.xml.key

sudo rm -rf "$OUT"
mkdir -p "$OUT"
args=()

if [ "$PROFILE" = Release ]; then
    # Build from a copy of kiwi/ without the files the packages install, so the
    # image holds only the packaged copies and updates can replace them.
    desc="$OUT/description"
    cp -a kiwi "$desc"
    tab=$(printf '\t')
    while IFS=$tab read -r pkg src dst flags; do
        case "$pkg" in ''|'#'*) continue ;; esac
        case "$src" in kiwi/root/*) rm -rf "$desc/root/${src#kiwi/root/}" ;; esac
    done < packaging/manifest.tsv
    # Image-only files that replace overlay files in this profile
    cp -a packaging/release-overlay/. "$desc/root/"
    find "$desc/root" -depth -type d -empty -delete
else
    desc=kiwi
fi

if [ ! -f "$KEY" ] && ! curl -fsSL -o "$KEY" "$KEY_URL"; then
    rm -f "$KEY"
    echo "Missing $KEY and could not download it from $KEY_URL (see docs/packages.md)." >&2
    exit 1
fi
args+=(--signing-key "$KEY")

sudo kiwi-ng --profile "$PROFILE" system build \
    --description "$desc" \
    --target-dir "$OUT/image" \
    ${args[@]+"${args[@]}"}

ls -lh "$OUT"/image/*.iso
