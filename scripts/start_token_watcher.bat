@echo off
REM Token Watcher - Startet den Python-Watcher in WSL2 im Hintergrund
REM Dieses Script wird beim Windows-Start via Task Scheduler ausgeführt

wsl -d Ubuntu -e bash -c "nohup python3 /home/bolla/.openclaw/workspace/scripts/token_watcher.py >> /home/bolla/.openclaw/workspace/logs/token_watcher.log 2>&1 &"
