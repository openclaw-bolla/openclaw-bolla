#!/bin/bash
# Watchdog: hält den Surface Book Reverse-Tunnel (Port 2222) am Leben
#
# Begrenzung: Funktioniert nur wenn das Book online ist UND eine SSH-Verbindung steht
# (also der "halb-tote" Zustand wo ssh.exe läuft aber -R nicht durchkam).
# Wenn das Book gar nicht erreichbar ist (z.B. tunnel.ps1 hat nicht gestartet weil
# kein User angemeldet), kann der Watchdog nichts ausrichten — dann muss
# der MC-Button (vom Studio aus) oder der BollaTunnel-Task am Book greifen.

LOG=/home/bolla/workspace/logs/book_tunnel_watchdog.log
STATE=/tmp/book_tunnel_watchdog.fail
log_w() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

# Port 2222 in WSL prüfen — wenn ssh-Server lauscht, alles ok
if ss -tln 2>/dev/null | grep -q ':2222 '; then
    [ -f "$STATE" ] && rm -f "$STATE"
    exit 0
fi

# Port 2222 down. Prüfen ob Book per Port 2200 (Inbound zum Studio) Connect hat.
# Wenn ja: ssh-Prozess am Book ist da aber ohne -R. → MC-Restart-Logik triggern.
BOOK_CONN=$(/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command \
    "(Get-NetTCPConnection -LocalPort 2200 -State Established -ErrorAction SilentlyContinue | Where-Object RemoteAddress -eq '192.168.178.38').Count" 2>/dev/null | tr -d '\r')

if [ "${BOOK_CONN:-0}" -gt 0 ]; then
    # Book hat SSH-Connection zum Studio → "halb-tot"-Zustand → MC-Restart probieren
    log_w "Port 2222 down, Book aber connected (Port 2200, $BOOK_CONN Sessions) → MC-Restart triggern"
    curl -s -X POST -H "Content-Type: application/json" \
        -d '{"action":"restart_tunnel"}' \
        http://127.0.0.1:18790/api/surfaces/book/action >> "$LOG" 2>&1
    echo "$(date +%s)" > "$STATE"
else
    # Book scheint offline oder hat noch nie connected — wir können nichts tun
    PREV=$(cat "$STATE" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    # Nur alle 5 Min loggen damit Log nicht zuläuft
    if [ $((NOW - PREV)) -gt 300 ]; then
        log_w "Port 2222 down, Book nicht connected (Port 2200 leer) — Book vermutlich offline/ungeloggt, kein Auto-Fix möglich"
        echo "$NOW" > "$STATE"
    fi
fi
