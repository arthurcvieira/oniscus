#!/bin/bash
# Boots an Oniscus ISO in QEMU (UEFI, headless), takes screenshots of the boot,
# the Ly greeter and the desktop after logging in as the live user, and saves
# them with the serial log in the output directory.
#   tests/boot-test.sh path/to/oniscus.iso out-dir
set -uo pipefail

iso=$1
out=$2
mkdir -p "$out"
mon=$out/qemu-monitor.sock
cp /usr/share/OVMF/OVMF_VARS_4M.fd "$out/vars.fd"

accel=()
[ -w /dev/kvm ] && accel=(-enable-kvm -cpu host)

qemu-system-x86_64 "${accel[@]}" \
    -machine q35 -m 4096 -smp 2 \
    -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd \
    -drive if=pflash,format=raw,file="$out/vars.fd" \
    -cdrom "$iso" -boot d \
    -vga std -display none \
    -netdev user,id=net0 -device virtio-net-pci,netdev=net0 \
    -serial file:"$out/serial.log" \
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
# Boot: GRUB menu, then the system until the greeter
for t in 005 020 040 060 090 120 150 180; do
    sleep $((10#$t - ${last:-0}))
    last=$((10#$t))
    shot "boot-${t}s"
done

# Ly starts with the login field focused: user, Down to password, Enter
type_text live
hmp "sendkey down"
type_text live
shot greeter-filled
hmp "sendkey ret"
sleep 30
shot desktop-030s
sleep 30
shot desktop-060s

# Terminal (Super+Enter): a few checks on screen
hmp "sendkey meta_l-ret"
sleep 5
type_text "systemctl --failed --no-pager; pgrep -l polybar; pgrep -l plank; pgrep -l picom; onis doctor"
hmp "sendkey ret"
sleep 5
shot terminal-checks

hmp "quit"
wait $qemu
grep -nE "Failed to start|FAILED|emergency|Kernel panic" "$out/serial.log" > "$out/serial-errors.txt" || true
echo "Serial log errors:"
cat "$out/serial-errors.txt"
