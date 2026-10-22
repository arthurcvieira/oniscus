#!/bin/bash
# Builds the packages Oniscus adds to Tumbleweed (packaging/*/<name>.spec other
# than oniscus.spec: Ly and Plank Reloaded) and makes an rpm-md repository of
# them. Runs as root in an openSUSE Tumbleweed container; rpmbuild runs without
# network, like on the Open Build Service.
#   tests/build-rpms.sh /src /out/rpms
set -euxo pipefail
src=$1
repo=$2
top=$(mktemp -d)

zypper --non-interactive install --no-recommends rpm-build systemd-rpm-macros \
    createrepo_c curl zstd util-linux tar gzip
zypper --non-interactive info zig | grep -E '^(Version|Name)' || true

for spec in "$src"/packaging/ly/ly.spec "$src"/packaging/plank-reloaded/plank-reloaded.spec; do
    dir=$(dirname "$spec")
    mkdir -p "$top/SOURCES"
    cp -a "$dir"/. "$top/SOURCES/"
    # Remote sources: "URL#/file name" or plain URL
    rpmspec -P "$spec" | awk '/^Source[0-9]*:/ { print $2 }' | while read -r url; do
        case "$url" in
            http*) file=${url##*#/}; [ "$file" = "$url" ] && file=${url##*/}
                   [ -f "$top/SOURCES/$file" ] || curl -fsSL -o "$top/SOURCES/$file" "${url%%#*}" ;;
        esac
    done
    deps=$(rpmspec -q --buildrequires "$spec" | tr -d ' ')
    # shellcheck disable=SC2086
    zypper --non-interactive install --no-recommends $deps
    # Ly: Zig dependencies come from a vendor tarball made with network access
    if [ "$(basename "$spec")" = ly.spec ]; then
        version=$(rpmspec -q --qf '%{version}\n' "$spec" | head -1)
        [ -f "$top/SOURCES/ly-$version-vendor.tar.zst" ] || "$dir/make-vendor.sh" "$top/SOURCES"
    fi
    unshare --net rpmbuild -bb --define "_topdir $top" "$spec"
done

mkdir -p "$repo"
find "$top/RPMS" -name '*.rpm' -exec cp {} "$repo/" \;
createrepo_c "$repo"
ls -l "$repo"
