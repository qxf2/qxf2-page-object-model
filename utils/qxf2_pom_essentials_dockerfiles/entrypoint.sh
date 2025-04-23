#!/bin/bash
export DISPLAY=:99
Xvfb :99 -screen 0 1366x768x16 2>/dev/null &

# Start x11vnc
x11vnc -display :99 -forever -nopw -quiet -rfbport 5999 &

# Run CMD command
exec "$@"