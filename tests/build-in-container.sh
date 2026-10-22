#!/bin/bash
# Builds the Oniscus ISO inside an openSUSE Tumbleweed container. Used by the
# ISO workflow (.github/workflows/iso.yml); run as root in a privileged
# container with the repository at /src and the output directory at /out.
#   SERIAL=1      also send kernel messages to the serial port (boot test logs)
#   LOCAL_RPMS=1  build Ly and Plank Reloaded here instead of using OBS
set -euxo pipefail

zypper --non-interactive --gpg-auto-import-keys refresh
zypper --non-interactive install --no-recommends python3-kiwi kiwi-systemdeps

# LOCAL_RPMS=1: build Ly and Plank Reloaded from packaging/ and use them instead
# of the Oniscus repository on OBS (tests the spec files before they go there)
if [ "${LOCAL_RPMS:-0}" = 1 ]; then
    bash /src/tests/build-rpms.sh /src /out/rpms
    zypper --non-interactive addrepo --no-gpgcheck /out/rpms oniscus-local
fi

# Report every package name in config.kiwi that the repositories don't have
# (Release-only packages come from the Oniscus repository and are skipped)
python3 - /src/kiwi/config.kiwi > /tmp/packages <<'PY'
import sys, xml.etree.ElementTree as ET
for p in ET.parse(sys.argv[1]).getroot().iter("packages"):
    if p.get("type") in ("image", "bootstrap") and p.get("profiles") != "Release":
        for pkg in p.iter("package"):
            print(pkg.get("name"))
PY
missing=()
for pkg in $(cat /tmp/packages); do
    zypper --non-interactive --quiet search --match-exact --type package "$pkg" >/dev/null 2>&1 \
        || missing+=("$pkg")
done
[ ${#missing[@]} -gt 0 ] && echo "Packages not in the repositories: ${missing[*]}"
for pkg in "${missing[@]}" ${SEARCH:-}; do zypper --non-interactive search "$pkg" || true; done

desc=/out/description
rm -rf "$desc" /out/image
cp -a /src/kiwi "$desc"
if [ "${SERIAL:-0}" = 1 ]; then
    sed -i 's/kernelcmdline="splash quiet"/kernelcmdline="splash quiet console=tty0 console=ttyS0,115200"/' \
        "$desc/config.kiwi"
fi
if [ "${LOCAL_RPMS:-0}" = 1 ]; then
    python3 - "$desc/config.kiwi" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p).read()
s = re.sub(r'<repository ([^>]*alias="oniscus"[^>]*)>\s*<source path="[^"]*"/>',
           r'<repository \1 package_gpgcheck="false" repository_gpgcheck="false">\n        <source path="dir:///out/rpms"/>',
           s)
# A local directory can't be kept in the image's repository list
s = s.replace('alias="oniscus" imageinclude="true"', 'alias="oniscus"')
open(p, "w").write(s)
PY
    grep -A1 'alias="oniscus"' "$desc/config.kiwi"
fi

kiwi-ng --profile "${PROFILE:-Dev}" system build \
    --description "$desc" \
    --target-dir /out/image
ls -lh /out/image/*.iso
# A few facts about the built system, for the log
root=/out/image/build/image-root
rpm --root "$root" -q ly plank-reloaded kf6-oxygen-icons || true
ls -l "$root"/etc/systemd/system/*.wants/ly* 2>&1 || true
