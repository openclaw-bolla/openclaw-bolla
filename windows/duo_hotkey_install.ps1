# Bolla — Duo-Hotkey Installer (Windows, PowerShell)
# Stellt den Win+Strg+S-Duo-Screenshot-Hotkey auf einem frischen Windows wieder her.
# Voraussetzung: WSL laeuft, /home/bolla/workspace/scripts/duoclip.sh ist da.
# Ausfuehren:  powershell -ExecutionPolicy Bypass -File duo_hotkey_install.ps1
$ErrorActionPreference = "Stop"

$base    = Join-Path $env:LOCALAPPDATA "Bolla"
$ahkDir  = Join-Path $base "AutoHotkey"
$ahkExe  = Join-Path $ahkDir "AutoHotkey64.exe"
$vbs     = Join-Path $base "duoclip_launch.vbs"
$ahk     = Join-Path $base "duoclip.ahk"
New-Item -ItemType Directory -Force -Path $ahkDir | Out-Null

# 1) AutoHotkey v2 portabel laden (falls noch nicht da)
if (-not (Test-Path $ahkExe)) {
    $zip = Join-Path $env:TEMP "ahk-v2.zip"
    Write-Host "Lade AutoHotkey v2 ..."
    Invoke-WebRequest -Uri "https://www.autohotkey.com/download/ahk-v2.zip" -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath $ahkDir -Force
    Remove-Item $zip -Force
}

# 2) Launcher (.vbs) — ruft WSL -> duoclip.sh right, lautlos
@'
' Bolla — Duo-Screenshot in die Windows-Zwischenablage (lautlos, kein Fenster)
Set sh = CreateObject("WScript.Shell")
sh.Run "wsl.exe -e bash -lc ""/home/bolla/workspace/scripts/duoclip.sh right""", 0, False
'@ | Set-Content -Path $vbs -Encoding ASCII

# 3) AHK-Skript — Win+Strg+S
@"
#SingleInstance Force
A_IconTip := "Bolla: Win+Strg+S = Duo-Screenshot (rechte Seite) -> Zwischenablage"
#^s:: {
    Run('wscript.exe "$vbs"', , "Hide")
}
"@ | Set-Content -Path $ahk -Encoding ASCII

# 4) Autostart-Verknuepfung (laeuft bei jeder Anmeldung)
$ws = New-Object -ComObject WScript.Shell
$startup = [Environment]::GetFolderPath("Startup")
$lnk = Join-Path $startup "Bolla Duo-Hotkey.lnk"
$s = $ws.CreateShortcut($lnk)
$s.TargetPath = $ahkExe
$s.Arguments  = "`"$ahk`""
$s.WorkingDirectory = $base
$s.Description = "Bolla Duo-Screenshot Hotkey (Win+Strg+S)"
$s.Save()

# 5) Jetzt starten
Start-Process -FilePath $ahkExe -ArgumentList "`"$ahk`""
Write-Host "Fertig. Win+Strg+S ist aktiv (rechte Duo-Seite -> Zwischenablage)."
