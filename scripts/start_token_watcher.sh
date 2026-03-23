#!/bin/bash
# Startet den Token Watcher falls er nicht läuft
if pgrep -f token_watcher.py > /dev/null; then
    echo "$(date): Token Watcher läuft bereits." >> /home/bolla/.openclaw/workspace/logs/token_watcher.log
else
    echo "$(date): Token Watcher wird gestartet..." >> /home/bolla/.openclaw/workspace/logs/token_watcher.log
    nohup python3 /home/bolla/.openclaw/workspace/scripts/token_watcher.py >> /home/bolla/.openclaw/workspace/logs/token_watcher.log 2>&1 &
fi
