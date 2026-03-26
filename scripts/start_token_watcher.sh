#!/bin/bash
# Startet den Token Watcher falls er nicht läuft
export PATH="$PATH:/home/bolla/.npm-global/bin"

LOG=/home/bolla/.openclaw/workspace/logs/token_watcher.log

if pgrep -f "python3.*token_watcher.py" > /dev/null; then
    echo "$(date): Token Watcher läuft bereits." >> "$LOG"
else
    echo "$(date): Token Watcher wird gestartet..." >> "$LOG"
    setsid nohup python3 /home/bolla/.openclaw/workspace/scripts/token_watcher.py >> "$LOG" 2>&1 &
    disown
fi

# wtnet Watcher starten
WTNET_LOG=/home/bolla/.openclaw/workspace/logs/wtnet_watcher.log
if pgrep -f "python3.*wtnet_watcher.py" > /dev/null; then
    echo "$(date): wtnet Watcher läuft bereits." >> "$LOG"
else
    echo "$(date): wtnet Watcher wird gestartet..." >> "$LOG"
    setsid nohup python3 /home/bolla/.openclaw/workspace/scripts/wtnet_watcher.py >> "$WTNET_LOG" 2>&1 &
    disown
fi
