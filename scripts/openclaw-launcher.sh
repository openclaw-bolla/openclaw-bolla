#!/bin/bash
# openclaw-launcher.sh
# Portabler Launcher — nutzt $HOME und sucht openclaw automatisch.
# Wird von Windows VBS aufgerufen. Keine hardcodierten Pfade nötig.

LOG="$HOME/.openclaw/workspace/logs/gateway_autostart.log"
mkdir -p "$(dirname "$LOG")"

echo "$(date): Launcher gestartet, User=$(whoami), HOME=$HOME" >> "$LOG"

# openclaw finden: erst im npm-global, dann im PATH
OPENCLAW=$(which openclaw 2>/dev/null)
if [ -z "$OPENCLAW" ]; then
    # Typische npm-global Pfade als Fallback
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
    exit 1
fi

echo "$(date): openclaw gefunden: $OPENCLAW" >> "$LOG"

# Gateway starten
"$OPENCLAW" gateway start >> "$LOG" 2>&1
echo "$(date): Gateway gestartet (Exit: $?)" >> "$LOG"

# Token Watcher starten (falls nicht läuft)
WATCHER="$HOME/.openclaw/workspace/scripts/start_token_watcher.sh"
if [ -f "$WATCHER" ]; then
    bash "$WATCHER"
else
    echo "$(date): WARNUNG - start_token_watcher.sh nicht gefunden" >> "$LOG"
fi
