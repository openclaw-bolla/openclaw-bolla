#!/bin/bash
# Startet den Token Watcher falls er nicht läuft
export PATH="$PATH:/home/bolla/.npm-global/bin"

LOG=/home/bolla/.openclaw/workspace/logs/token_watcher.log

if pgrep -f token_watcher.py > /dev/null; then
    echo "$(date): Token Watcher läuft bereits." >> "$LOG"
else
    echo "$(date): Token Watcher wird gestartet..." >> "$LOG"
    setsid nohup python3 /home/bolla/.openclaw/workspace/scripts/token_watcher.py >> "$LOG" 2>&1 &
    disown
fi
