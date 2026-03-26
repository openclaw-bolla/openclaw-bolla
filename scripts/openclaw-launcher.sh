#!/bin/bash
# openclaw-launcher.sh
# Portabler Launcher — nutzt $HOME und sucht openclaw automatisch.
# Wird von Windows VBS aufgerufen. Keine hardcodierten Pfade nötig.
# v3: Wartet auf Netzwerk + Windows-Benachrichtigung wenn bereit.

LOG="$HOME/.openclaw/workspace/logs/gateway_autostart.log"
mkdir -p "$(dirname "$LOG")"

echo "$(date): Launcher gestartet, User=$(whoami), HOME=$HOME" >> "$LOG"

# ── Hilfsfunktion: Windows-Toast-Benachrichtigung ─────────────────────────────
notify_windows() {
    local title="$1"
    local message="$2"
    # PowerShell Toast Notification via Windows
    /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "
        Add-Type -AssemblyName System.Windows.Forms
        \$notify = New-Object System.Windows.Forms.NotifyIcon
        \$notify.Icon = [System.Drawing.SystemIcons]::Information
        \$notify.Visible = \$true
        \$notify.ShowBalloonTip(5000, '$title', '$message', [System.Windows.Forms.ToolTipIcon]::Info)
        Start-Sleep -Milliseconds 6000
        \$notify.Dispose()
    " >> "$LOG" 2>&1
}

# ── Warten auf Netzwerk (max. 120 Sek) ────────────────────────────────────────
WAIT=0
echo "$(date): Warte auf Netzwerkverbindung..." >> "$LOG"
while ! curl -sf --max-time 3 https://login.microsoftonline.com > /dev/null 2>&1; do
    if [ $WAIT -ge 120 ]; then
        echo "$(date): FEHLER - Kein Netzwerk nach 120 Sek. Abbruch." >> "$LOG"
        notify_windows "Bolla ❌" "Kein Netzwerk - Gateway nicht gestartet!"
        exit 1
    fi
    sleep 5
    WAIT=$((WAIT + 5))
done
echo "$(date): Netzwerk verfügbar (nach ${WAIT}s)" >> "$LOG"

# ── openclaw finden ────────────────────────────────────────────────────────────
export PATH="$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

OPENCLAW=$(which openclaw 2>/dev/null)
if [ -z "$OPENCLAW" ]; then
    for candidate in \
        "$HOME/.npm-global/bin/openclaw" \
        "$HOME/.npm/bin/openclaw" \
        "/usr/local/bin/openclaw"; do
        if [ -x "$candidate" ]; then
            OPENCLAW="$candidate"
            break
        fi
    done
fi

if [ -z "$OPENCLAW" ]; then
    echo "$(date): FEHLER - openclaw nicht gefunden!" >> "$LOG"
    notify_windows "Bolla ❌" "openclaw nicht gefunden - Gateway nicht gestartet!"
    exit 1
fi

echo "$(date): openclaw gefunden: $OPENCLAW" >> "$LOG"

# ── Gateway starten ────────────────────────────────────────────────────────────
"$OPENCLAW" gateway start >> "$LOG" 2>&1
EXIT_CODE=$?
echo "$(date): Gateway gestartet (Exit: $EXIT_CODE)" >> "$LOG"

# ── Token Watcher starten (falls nicht läuft) ──────────────────────────────────
WATCHER="$HOME/.openclaw/workspace/scripts/start_token_watcher.sh"
if [ -f "$WATCHER" ]; then
    bash "$WATCHER"
else
    echo "$(date): WARNUNG - start_token_watcher.sh nicht gefunden" >> "$LOG"
fi

# ── Benachrichtigung ───────────────────────────────────────────────────────────
if [ $EXIT_CODE -eq 0 ]; then
    notify_windows "Bolla 🐾 bereit!" "Gateway läuft. Dashboard kann geöffnet werden."
else
    notify_windows "Bolla ⚠️" "Gateway-Start fehlgeschlagen (Exit $EXIT_CODE). Log prüfen."
fi
