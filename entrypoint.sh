#!/bin/bash
export DISPLAY=:20
Xvfb :20 -screen 0 1366x768x16 &

# Start x11vnc
x11vnc -passwd TestVNC -display :20 -N -forever &

# Run CMD command
exec "$@"