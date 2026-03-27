Set oShell = CreateObject("WScript.Shell")
' WSL aufwecken und warten bis es bereit ist
oShell.Run "wsl -e bash -c ""echo wsl-ready""", 0, True
' 15 Sekunden warten damit WSL vollständig initialisiert ist
WScript.Sleep 15000
' Portabler Launcher starten — absoluter Pfad statt ~ (wird von bash nicht expandiert!)
oShell.Run "wsl -e bash /home/bolla/.openclaw/workspace/scripts/openclaw-launcher.sh", 0, False
