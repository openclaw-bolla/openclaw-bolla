# register_token_watcher.ps1
# Registriert den Token Watcher als Windows Startup Task
# Einmalig als Administrator ausführen!

$TaskName = "OpenClaw Token Watcher"
$BatchFile = "\\wsl.localhost\Ubuntu\home\bolla\.openclaw\workspace\scripts\start_token_watcher.bat"

# Prüfen ob das Batch-File erreichbar ist
if (-not (Test-Path $BatchFile)) {
    Write-Warning "Batch-File nicht gefunden: $BatchFile"
    Write-Warning "Stelle sicher, dass WSL2/Ubuntu läuft und der Pfad stimmt."
    exit 1
}

# Alten Task entfernen falls vorhanden
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# Aktion: Batch-File ausführen
$Action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c `"$BatchFile`""

# Trigger: Bei Windows-Start, 30 Sekunden Verzögerung (WSL braucht Zeit)
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Trigger.Delay = "PT30S"

# Einstellungen: Im Hintergrund, auch ohne Benutzer-Login
$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# Als aktueller Benutzer registrieren
$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Überwacht E-Mails von Robin und aktualisiert den Anthropic API Key automatisch" `
    -Force

Write-Host "✅ Task '$TaskName' erfolgreich registriert!" -ForegroundColor Green
Write-Host ""
Write-Host "Der Watcher startet automatisch beim nächsten Windows-Neustart." -ForegroundColor Cyan
Write-Host "Zum sofortigen Starten:"
Write-Host "  wsl -d Ubuntu -e bash -c `"nohup python3 /home/bolla/.openclaw/workspace/scripts/token_watcher.py > /home/bolla/.openclaw/workspace/logs/token_watcher.log 2>&1 &`""
