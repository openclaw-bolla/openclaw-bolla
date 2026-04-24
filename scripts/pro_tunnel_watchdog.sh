#!/bin/bash
# Watchdog: hält den Surface Pro Reverse-Tunnel (Port 2223) am Leben
while true; do
    if ! ss -tlnp | grep -q ':2223'; then
        # Tunnel starten (läuft im Hintergrund, bleibt aktiv)
        ssh -i ~/.ssh/id_ed25519 \
            -o ConnectTimeout=10 \
            -o StrictHostKeyChecking=no \
            renat@192.168.178.41 \
            "cmd /c \"ssh -i C:/Users/renat/.ssh/id_ed25519_bolla -N -R 2223:localhost:22 -p 2200 bolla@192.168.178.28 -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3\"" &
    fi
    sleep 30
done
