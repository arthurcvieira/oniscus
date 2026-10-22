#!/bin/bash
# Makes ly-<version>-vendor.tar.zst: the Zig dependencies of Ly, fetched once
# with network access so the OBS build (which has none) can use them.
# Needs zig, curl and zstd.  Usage: make-vendor.sh [output-dir]
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
out=$(cd "${1:-$here}" && pwd)
version=$(awk '/^Version:/ { print $2 }' "$here/ly.spec")
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
curl -fsSL "https://github.com/fairyglade/ly/archive/refs/tags/v$version.tar.gz" | tar -xz -C "$work"
cd "$work/ly-$version"
# Fetch every dependency into the project-local zig-pkg/ directories (the
# same layout as Ly's own create_vendor_tarball.sh)
zig build --fetch=all 2>/dev/null || zig build --fetch
dirs=()
for d in zig-pkg ly-ui/zig-pkg ly-core/zig-pkg; do [ -d "$d" ] && dirs+=("$d"); done
tar --zstd -cf "$out/ly-$version-vendor.tar.zst" "${dirs[@]}"
ls -lh "$out/ly-$version-vendor.tar.zst"
