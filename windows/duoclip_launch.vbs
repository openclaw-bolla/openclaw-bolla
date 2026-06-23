' Bolla — Duo-Screenshot in die Windows-Zwischenablage (lautlos, kein Fenster)
' Ruft WSL -> duoclip.sh auf. Wird vom Hotkey gestartet. Feste Seite: rechts.
' Referenzkopie. Aktiv liegt die Datei unter %LOCALAPPDATA%\Bolla\ (vom Installer geschrieben).
Set sh = CreateObject("WScript.Shell")
sh.Run "wsl.exe -e bash -lc ""/home/bolla/workspace/scripts/duoclip.sh right""", 0, False
