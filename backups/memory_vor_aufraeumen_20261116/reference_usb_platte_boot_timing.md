---
name: reference-usb-platte-boot-timing
description: "Desktop/Taskleiste leer nach Boot trotz angeschlossener externer USB-Platte D: — Boot-Timing, nicht Bolla-Fehler"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7ef3d55f-1f8f-4297-a8fd-6968d4b96c65
  modified: 2026-08-03T17:35:07.881Z
---

Wenn nach dem Windows-Boot Desktop-Icons und Taskleiste leer sind, obwohl die externe USB-Platte (D:, enthält OneDrive) vor dem Booten schon angeschlossen war: Ursache ist Boot-Timing, nicht die Platte selbst und kein Bolla-Fehler.

**Warum:** Windows/Explorer startet oft schneller als die externe Platte vom System vollständig erkannt und eingebunden wird. Explorer baut Desktop (umgeleitet nach `D:\OneDrive\Desktop`, siehe [[user_desktop]]) einmal beim Start auf, findet den Pfad in dem kurzen Fenster noch nicht und zeigt dauerhaft leer an — auch wenn D: Sekunden später fertig ist. Explorer prüft danach nicht automatisch nach.

**Fix:** Explorer-Prozess neu starten (kein Reboot nötig):
```
powershell.exe -Command "Stop-Process -Name explorer -Force; Start-Sleep -Seconds 2; Start-Process explorer"
```
Vorher optional mit `Get-Volume -DriveLetter D` bestätigen, dass D: wirklich vollständig da ist.

**Vorbeugung:** Platte anschließen, ein paar Sekunden warten (bis sie erkannt ist), erst dann booten.

**Verwandt:** [[user_desktop]] (Desktop-Pfad), aktuell.md-Eintrag vom 02.08.2026 (Ersteinschlag dieses Musters, damals weil Platte komplett vergessen wurde — diesmal 03.08. trat es sogar bei angeschlossener Platte auf, also reines Timing-Problem, nicht nur "Platte vergessen").
