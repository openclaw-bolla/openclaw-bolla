#!/bin/bash
# openclaw-launcher.sh
# Portabler Launcher — wird von Windows VBS beim Login aufgerufen.
# systemd startet das Gateway bereits automatisch.
# Dieser Launcher wartet nur bis das Gateway erreichbar ist und zeigt ein Popup.
# v4: Kein doppelter Gateway-Start mehr — systemd macht das allein.

LOG="$HOME/.openclaw/workspace/logs/gateway_autostart.log"
mkdir -p "$(dirname "$LOG")"

echo "$(date): Launcher gestartet, User=$(whoami), HOME=$HOME" >> "$LOG"

# ── Hilfsfunktion: Windows-Popup ──────────────────────────────────────────────
notify_windows() {
    local title="$1"
    local message="$2"
    /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "
        \$wsh = New-Object -ComObject WScript.Shell
        \$wsh.Popup('$message', 5, '$title', 64)
    " >> "$LOG" 2>&1
}

# ── Warten bis Gateway erreichbar ist (max. 120 Sek) ─────────────────────────
# systemd startet das Gateway automatisch — wir warten nur darauf.
WAIT=0
echo "$(date): Warte bis Gateway erreichbar ist..." >> "$LOG"
while ! curl -sf --max-time 2 http://127.0.0.1:18789 > /dev/null 2>&1; do
    if [ $WAIT -ge 120 ]; then
        echo "$(date): FEHLER - Gateway nicht erreichbar nach 120 Sek." >> "$LOG"
        # Letzter Versuch: manuell starten falls systemd versagt hat
        export PATH="$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
        OPENCLAW=$(which openclaw 2>/dev/null || echo "$HOME/.npm-global/bin/openclaw")
        if [ -x "$OPENCLAW" ]; then
            echo "$(date): Fallback: Starte Gateway manuell..." >> "$LOG"
            "$OPENCLAW" gateway start >> "$LOG" 2>&1
            sleep 10
            if curl -sf --max-time 2 http://127.0.0.1:18789 > /dev/null 2>&1; then
                echo "$(date): Fallback erfolgreich." >> "$LOG"
                notify_windows "Bolla 🐾 bereit!" "Gateway läuft (Fallback). Dashboard kann geöffnet werden."
            else
                notify_windows "Bolla ❌" "Gateway nicht erreichbar. Bitte manuell prüfen."
            fi
        else
            notify_windows "Bolla ❌" "Gateway nicht erreichbar nach 120 Sek."
        fi
        exit 1
    fi
    sleep 5
    WAIT=$((WAIT + 5))
done

echo "$(date): Gateway erreichbar nach ${WAIT}s." >> "$LOG"

# ── Token Watcher starten (falls nicht läuft) ─────────────────────────────────
WATCHER="$HOME/.openclaw/workspace/scripts/start_token_watcher.sh"
if [ -f "$WATCHER" ]; then
    bash "$WATCHER" >> "$LOG" 2>&1
fi

# ── Popup ──────────────────────────────────────────────────────────────────────
notify_windows "Bolla 🐾 bereit!" "Gateway läuft. Dashboard kann geöffnet werden."
echo "$(date): Fertig." >> "$LOG"
