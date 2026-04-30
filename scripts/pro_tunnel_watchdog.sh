#!/bin/bash
# Watchdog: hält den Surface Pro Reverse-Tunnel (Port 2223) am Leben
while true; do
    if ! ss -tlnp | grep -q ':2223'; then
        ssh -i ~/.ssh/id_ed25519 \
            -o ConnectTimeout=10 \
            -o StrictHostKeyChecking=no \
            ernst@192.168.178.41 \
            "ssh -i C:/ProgramData/Bolla/id_ed25519 -N -R 2223:localhost:22 -p 2200 -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 bolla@192.168.178.29 &" 2>/dev/null
    fi
    sleep 30
done
