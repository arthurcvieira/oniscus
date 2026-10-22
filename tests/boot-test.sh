#!/bin/bash
# Boots an Oniscus ISO in QEMU (UEFI, headless), takes screenshots of the boot,
# the Ly greeter and the desktop after logging in as the live user, and saves
# them with the serial log and the output of tests/checks.txt (run on the serial
# console) in the output directory. Then it installs Oniscus with the installer
# (Calamares, driven with xdotool) on an empty disk and boots the installed system.
#   tests/boot-test.sh path/to/oniscus.iso out-dir
set -uo pipefail

iso=$1
out=$2
mkdir -p "$out"
mon=$out/qemu-monitor.sock
cp /usr/share/OVMF/OVMF_VARS_4M.fd "$out/vars.fd"
# Empty disk for the installation test (Calamares asks for 20 GB)
qemu-img create -q -f qcow2 "$out/disk.qcow2" 24G

accel=()
[ -w /dev/kvm ] && accel=(-enable-kvm -cpu host)

qemu-system-x86_64 "${accel[@]}" \
    -machine q35 -m 4096 -smp 2 \
    -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd \
    -drive if=pflash,format=raw,file="$out/vars.fd" \
    -cdrom "$iso" -boot d \
    -drive file="$out/disk.qcow2",if=virtio,format=qcow2 \
    -vga std -display none \
    -netdev user,id=net0 -device virtio-net-pci,netdev=net0 \
    -chardev socket,id=ser0,path="$out/serial.sock",server=on,wait=off,logfile="$out/serial.log" \
    -serial chardev:ser0 \
    -monitor unix:"$mon",server,nowait &
qemu=$!

hmp() { echo "$1" | socat - UNIX-CONNECT:"$mon" >/dev/null; }
shot() {
    hmp "screendump $out/$1.ppm"
    sleep 1
    convert "$out/$1.ppm" "$out/$1.png" && rm -f "$out/$1.ppm"
    echo "screenshot $1"
}
type_text() {
    local s=$1 i c
    for ((i = 0; i < ${#s}; i++)); do
        c=${s:i:1}
        case "$c" in
            ' ') c=spc ;; '-') c=minus ;; ';') c=semicolon ;; '.') c=dot ;;
            '|') c=shift-backslash ;; '/') c=slash ;;
        esac
        hmp "sendkey $c"
    done
}

sleep 5
# Boot: GRUB menu, splash, then the system until the desktop
for t in 005 012 020 030 040 060 090 120; do
    sleep $((10#$t - ${last:-0}))
    last=$((10#$t))
    shot "boot-${t}s"
done

# The live ISO logs in on its own (Ly autologin), so no greeter here
sleep 30
shot desktop-030s
sleep 30
shot desktop-060s

# Diagnostics through the serial console (logs in there as live too)
python3 "$(dirname "$0")/serial-run.py" "$out/serial.sock" "$(dirname "$0")/checks.txt" \
    | tee "$out/checks.txt"
shot desktop-after-checks

# --- Installation -----------------------------------------------------------
# Runs commands in the serial shell that checks.txt left logged in
vm() {
    printf '%s\n' "$@" > "$out/cmd.txt"
    python3 "$(dirname "$0")/serial-run.py" "$out/serial.sock" "$out/cmd.txt" 150 --again \
        | tee -a "$out/install.txt"
}
# Keys for the installer window
key() { vm "timeout 20 xdotool search --sync --onlyvisible --limit 1 --class calamares windowactivate --sync key --clearmodifiers $*"; }
next_page() { key alt+n; sleep 5; shot "install-$1"; }

vm 'export DISPLAY=:0 XAUTHORITY=/run/user/$(id -u)/lyxauth' \
   'setsid -f oniscus-install; sleep 45; pgrep -a calamares'
shot install-01-welcome
next_page 02-location
next_page 03-keyboard
next_page 04-partitions
next_page 05-users
# Full name (the login name "oniscus" and the computer name follow from it),
# then the password twice
vm "xdotool type --delay 80 'Oniscus Test'" "xdotool key Tab Tab Tab" \
   "xdotool type --delay 80 'oniscus1'" "xdotool key Tab" "xdotool type --delay 80 'oniscus1'"
sleep 2
shot install-05-users-filled
next_page 06-nvidia
next_page 07-codecs
next_page 08-summary
key alt+i   # Install
sleep 4
shot install-09-confirm
key alt+i   # Install now
sleep 30
shot install-10-running
# Wait for the copy to start and then finish (target mounted, then unmounted)
started=0
for i in $(seq 1 100); do
    st=$(vm 'echo "mounts=$(findmnt -rn -o TARGET | grep -c calamares-root) procs=$(pgrep -c calamares)"' | grep -o 'mounts=[0-9]* procs=[0-9]*' | tail -1)
    echo "install wait $i: $st"
    case "$st" in
        mounts=0\ *) [ $started = 1 ] && break ;;
        mounts=*) started=1 ;;
    esac
    case "$st" in *procs=0) break ;; esac
    sleep 25
done
shot install-11-finished
vm 'sudo grep -iE "error|fail|warning" /root/.cache/calamares/session.log | tail -n 60' \
   'sudo tail -n 80 /root/.cache/calamares/session.log' \
   'tail -n 20 /tmp/oniscus-install.log' \
   'sudo fdisk -l /dev/vda'
cp "$out/install.txt" "$out/install-log.txt" 2>/dev/null

hmp "quit"
wait $qemu

# --- Boot the installed system from the disk ----------------------------------
qemu-system-x86_64 "${accel[@]}" \
    -machine q35 -m 4096 -smp 2 \
    -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd \
    -drive if=pflash,format=raw,file="$out/vars.fd" \
    -drive file="$out/disk.qcow2",if=virtio,format=qcow2 \
    -vga std -display none \
    -netdev user,id=net0 -device virtio-net-pci,netdev=net0 \
    -serial file:"$out/installed-serial.log" \
    -monitor unix:"$mon",server,nowait &
qemu=$!
last=0
for t in 008 015 030 060 090 120; do
    sleep $((10#$t - last))
    last=$((10#$t))
    shot "installed-boot-${t}s"
done
# Log in at Ly as the user created in the installer (the only user, so the
# login field already shows it)
hmp "sendkey down"
type_text oniscus1
shot installed-greeter-filled
hmp "sendkey ret"
sleep 45
shot installed-desktop-045s
sleep 30
shot installed-desktop-075s
hmp "quit"
wait $qemu
grep -nE "Failed to start|FAILED|emergency|Kernel panic" "$out/serial.log" > "$out/serial-errors.txt" || true
echo "Serial log errors:"
cat "$out/serial-errors.txt"
