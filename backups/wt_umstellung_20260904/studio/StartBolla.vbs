Set WshShell = CreateObject("WScript.Shell")

' WSL versteckt starten, damit @reboot Cron-Jobs anlaufen (cloudflared, mc_api, telegram...)
WshShell.Run "wsl.exe -d Ubuntu", 0, False

' Warten bis alle @reboot Jobs hochgefahren sind (cloudflared braucht ~20s)
WScript.Sleep 50000

' Mission Control in Edge oeffnen
WshShell.Run """C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"" http://127.0.0.1:18790/", 1, False

WScript.Sleep 2000

' Windows Terminal mit WSL + Bolla starten
WshShell.Run """C:\Users\ernst\AppData\Local\Microsoft\WindowsApps\wt.exe"" -p ""Ubuntu"" -- wsl -- /home/bolla/.local/bin/claude", 1, False
