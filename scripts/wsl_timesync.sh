#!/bin/bash
# Setzt die WSL-Systemuhr auf die echte Windows-Host-Zeit.
# Behebt WSL2-Uhr-Drift nach Windows-Standby/Ruhezustand.
# Muss als root laufen (per sudoers NOPASSWD freigegeben).
PS="/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
WIN_TIME="$("$PS" -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss'" 2>/dev/null | tr -d '\r')"
if [ -n "$WIN_TIME" ]; then
    date -s "$WIN_TIME" >/dev/null 2>&1 && echo "WSL-Uhr gesetzt auf: $WIN_TIME"
else
    echo "FEHLER: Windows-Zeit konnte nicht gelesen werden" >&2
    exit 1
fi
