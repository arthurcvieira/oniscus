#!/bin/sh
# Restarts Polybar (called by i3 with exec_always).
killall -q polybar
while pgrep -u "$(id -u)" -x polybar >/dev/null; do sleep 0.2; done
polybar xi3 >"${XDG_CACHE_HOME:-$HOME/.cache}/polybar.log" 2>&1 &
