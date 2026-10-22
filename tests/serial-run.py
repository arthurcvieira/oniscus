#!/usr/bin/env python3
"""Logs in on the VM's serial console and runs diagnostic commands.

Used by boot-test.sh. Connects to QEMU's serial socket, logs in as the live
user and prints each command with its output, so the test log shows what
happened inside the running system.
    serial-run.py <socket> <command file> [seconds per command] [--again]
--again reuses the shell that an earlier run logged in (default timeout 120).
"""
import re
import socket
import sys
import time

sock_path, cmd_file = sys.argv[1], sys.argv[2]
cmd_timeout = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 120
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(sock_path)
s.settimeout(1)
ansi = re.compile(rb"\x1b(\[[0-9;?=!]*[A-Za-z]|\][^\x07\x1b]*(\x07|\x1b\\)|P[^\x1b]*\x1b\\|[78()][0-9A-Z]?)")


def read_until(token, timeout):
    buf = b""
    end = time.time() + timeout
    while time.time() < end:
        try:
            data = s.recv(65536)
        except socket.timeout:
            continue
        buf += data
        if token in ansi.sub(b"", buf):
            break
    return ansi.sub(b"", buf).decode(errors="replace")


PROMPT = b"\xe2\x9d\xaf"  # the prompt arrow
if "--again" not in sys.argv:  # first run: log in
    s.sendall(b"\r")
    read_until(b"login:", 60)
    s.sendall(b"live\r")
    read_until(b"Password:", 30)
    s.sendall(b"live\r")
    time.sleep(5)
    read_until(PROMPT, 20)
    s.sendall(b"export TERM=dumb PAGER=cat SYSTEMD_COLORS=0; stty cols 200\r")
    time.sleep(2)
for cmd in open(cmd_file).read().splitlines():
    if not cmd.strip() or cmd.startswith("#"):
        continue
    print(f"\n$ {cmd}", flush=True)
    s.sendall(cmd.encode() + b'; echo "__DO""NE__"\r')
    out = read_until(b"__DONE__", cmd_timeout)
    # Drop the echoed command line and the marker
    lines = out.split("\n")
    lines = [l for l in lines if "__DO" not in l and "__DONE__" not in l]
    print("\n".join(l.rstrip("\r") for l in lines).strip(), flush=True)
