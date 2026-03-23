Set oShell = CreateObject("WScript.Shell")
oShell.Run "wsl -e bash -c ""nohup python3 /home/bolla/.openclaw/workspace/scripts/token_watcher.py >> /home/bolla/.openclaw/workspace/logs/token_watcher.log 2>&1 &""", 0, False
