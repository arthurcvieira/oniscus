#!/bin/bash
# Builds the Oniscus ISO inside an openSUSE Tumbleweed container. Used by the
# ISO workflow (.github/workflows/iso.yml); run as root in a privileged
# container with the repository at /src and the output directory at /out.
#   SERIAL=1  also send kernel messages to the serial port (boot test logs)
set -euxo pipefail

zypper --non-interactive --gpg-auto-import-keys refresh
zypper --non-interactive install --no-recommends python3-kiwi kiwi-systemdeps

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
