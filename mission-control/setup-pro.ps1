# Bolla – Surface Pro Tunnel-Setup final
Write-Host "Richte Tunnel ein (final)..." -ForegroundColor Cyan

$tunnelScript = @'
while ($true) {
    cmd /c "ssh -i C:/Users/renat/.ssh/id_ed25519_bolla -N -R 2223:localhost:22 -p 2200 bolla@192.168.178.28 -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3"
    Start-Sleep -Seconds 15
}
'@
$tunnelScript | Set-Content -Path "C:\Users\renat\surface_pro_tunnel.ps1" -Encoding UTF8

Unregister-ScheduledTask -TaskName "BollaTunnel" -Confirm:$false -ErrorAction SilentlyContinue
$action   = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File C:\Users\renat\surface_pro_tunnel.ps1"
$trigger  = New-ScheduledTaskTrigger -AtLogOn -User "renat"
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName "BollaTunnel" -Action $action -Trigger $trigger `
    -Settings $settings -RunLevel Highest -Force | Out-Null

Start-ScheduledTask -TaskName "BollaTunnel"
Write-Host "Fertig - Tunnel startet!" -ForegroundColor Green
