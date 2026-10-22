#!/bin/bash
# Builds the Oniscus ISO inside an openSUSE Tumbleweed container. Used by the
# ISO workflow (.github/workflows/iso.yml); run as root in a privileged
# container with the repository at /src and the output directory at /out.
#   SERIAL=1  also send kernel messages to the serial port (boot test logs)
set -euxo pipefail

zypper --non-interactive --gpg-auto-import-keys refresh
zypper --non-interactive install --no-recommends python3-kiwi kiwi-systemdeps

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
if [ ${#missing[@]} -gt 0 ]; then
    echo "Packages not in the repositories: ${missing[*]}"
    for pkg in "${missing[@]}" ${SEARCH:-}; do zypper --non-interactive search "$pkg" || true; done
fi

desc=/out/description
rm -rf "$desc" /out/image
cp -a /src/kiwi "$desc"
if [ "${SERIAL:-0}" = 1 ]; then
    sed -i 's/kernelcmdline="splash quiet"/kernelcmdline="splash quiet console=tty0 console=ttyS0,115200"/' \
        "$desc/config.kiwi"
fi

kiwi-ng --profile "${PROFILE:-Dev}" system build \
    --description "$desc" \
    --target-dir /out/image
ls -lh /out/image/*.iso
# A few facts about the built system, for the log
root=/out/image/build/image-root
grep -E '^(greeter|live):' "$root/etc/passwd" || echo "no greeter user"
ls -l "$root"/etc/systemd/system/display-manager.service "$root"/etc/systemd/system/*.wants/greetd* 2>&1 || true
