#!/usr/bin/env bash
# Boot-Audit: Was startet alles automatisch mit Windows?
# Ruft PowerShell auf und zeigt die Autostart-Quellen + Boot-Zeit.
set -euo pipefail

echo "═══════════════════════════════════════════════════════════"
echo "  🐾 Bolla Boot-Audit"
echo "═══════════════════════════════════════════════════════════"
echo

echo "── Letzter Boot & Uptime ──"
powershell.exe -NoProfile -Command "
  \$os = Get-CimInstance Win32_OperatingSystem
  \$boot = \$os.LastBootUpTime
  \$up = (Get-Date) - \$boot
  Write-Host ('Letzter Boot : ' + \$boot.ToString('dd.MM.yyyy HH:mm:ss'))
  Write-Host ('Uptime       : {0:N0}h {1:N0}m' -f \$up.TotalHours, \$up.Minutes)
" 2>&1 | tr -d '\r'
echo

echo "── Boot-Dauer (letzte 5 Boots, Event-Log 100) ──"
powershell.exe -NoProfile -Command "
  try {
    Get-WinEvent -LogName 'Microsoft-Windows-Diagnostics-Performance/Operational' -FilterXPath \"*[System[(EventID=100)]]\" -MaxEvents 5 -ErrorAction Stop |
      ForEach-Object {
        \$xml = [xml]\$_.ToXml()
        \$dur = (\$xml.Event.EventData.Data | Where-Object { \$_.Name -eq 'BootTime' }).'#text'
        '{0}  —  {1:N1}s' -f \$_.TimeCreated.ToString('dd.MM. HH:mm'), ([int]\$dur/1000)
      }
  } catch { Write-Host '  (Event-Log nicht zugänglich — als Admin nochmal probieren)' }
" 2>&1 | tr -d '\r'
echo

echo "── Autostart-Einträge (Registry + Startup-Ordner) ──"
powershell.exe -NoProfile -Command "
  Get-CimInstance Win32_StartupCommand |
    Sort-Object Location, Name |
    Format-Table -AutoSize Name, Location, User
" 2>&1 | tr -d '\r' | sed 's/^/  /'
echo

echo "── Geplante Tasks beim Anmelden/Boot (aktiv) ──"
powershell.exe -NoProfile -Command "
  Get-ScheduledTask |
    Where-Object { \$_.State -eq 'Ready' -and (\$_.Triggers.CimClass.CimClassName -match 'Logon|Boot') } |
    Select-Object -ExpandProperty TaskName |
    Sort-Object
" 2>&1 | tr -d '\r' | sed 's/^/  /' | head -40
echo

echo "── Langsamste Dienste beim Start (Top 15) ──"
powershell.exe -NoProfile -Command "
  try {
    Get-WinEvent -LogName 'Microsoft-Windows-Diagnostics-Performance/Operational' -FilterXPath \"*[System[(EventID=106)]]\" -MaxEvents 200 -ErrorAction Stop |
      ForEach-Object {
        \$x = [xml]\$_.ToXml()
        [PSCustomObject]@{
          Time = \$_.TimeCreated
          Name = (\$x.Event.EventData.Data | Where-Object { \$_.Name -eq 'FriendlyName' }).'#text'
          Ms   = [int]((\$x.Event.EventData.Data | Where-Object { \$_.Name -eq 'TotalTime' }).'#text')
        }
      } |
      Group-Object Name |
      ForEach-Object { [PSCustomObject]@{ Name = \$_.Name; AvgMs = [int](( \$_.Group | Measure-Object Ms -Average).Average) } } |
      Sort-Object AvgMs -Descending |
      Select-Object -First 15 |
      Format-Table -AutoSize
  } catch { Write-Host '  (Performance-Log nicht zugänglich)' }
" 2>&1 | tr -d '\r' | sed 's/^/  /'
echo

echo "═══════════════════════════════════════════════════════════"
echo "  Tipp: Autostarts deaktivieren → Task-Manager → Autostart"
echo "  Oder: Win+R → msconfig → Systemstart"
echo "═══════════════════════════════════════════════════════════"
