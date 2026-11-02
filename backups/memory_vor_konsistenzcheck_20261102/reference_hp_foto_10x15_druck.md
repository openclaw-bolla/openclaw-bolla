---
name: reference-hp-foto-10x15-druck
description: 10x15-Fotos auf HP ENVY Inspire 7900 drucken — HP Smart App wählt falsches Fach; Windows-Skript mit Fotofach/Fotopapier/randlos
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9612f629-ca4f-4ff2-a268-8d0028b938f0
  modified: 2026-09-22T07:50:59.994Z
---

HP ENVY Inspire 7900 (Windows-Name `HPCE59BF (HP ENVY Inspire 7900 series)`): Die **HP Smart App** kann das Fach nicht wählen und meldet "Papier in Fach einlegen" (sucht im Hauptfach); Windows-Treiber steht auf **Normalpapier** → Foto verschmiert.

**Lösung (20.09. + 22.09.2026 bewährt, Gutschein gedruckt):** `workspace/scripts/print_foto_10x15.ps1` — WPF-PrintTicket: 4x6, `JobInputBin=ns0000:_6` (Fotofach), Medientyp `_5_1069…` (HP Fotopapiere), randlos, Optimal, quer. Aufruf: `powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File print_foto_10x15.ps1 -File 'D:\...\bild.png' -Go` (ohne `-Go` nur Trockenlauf).
**Aus WSL-Bash konkret (22.09. so gemacht, ab jetzt Standard):** `powershell.exe` liegt NICHT im Bash-PATH → vollen Pfad nehmen: `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -ExecutionPolicy Bypass -File "$(wslpath -w /home/bolla/workspace/scripts/print_foto_10x15.ps1)" -File "$(wslpath -w '/mnt/d/OneDrive/Desktop/temp/bild.png')" -Go`. Ohne `-ExecutionPolicy Bypass` blockt Windows das Skript als „nicht digital signiert" (UnauthorizedAccess).

**Papier:** Glänzende Seite bei Fotofach UND Hauptfach nach UNTEN. Nicht "oben" sagen (Fehler vom 20.09.).
**Falle:** Hängende Alt-Jobs (HP Smart "Simple photo print", Status Retained) blockieren die Schlange → `Remove-PrintJob`. Nach OK am Drucker kam Fehler erst, als der Alt-Job weg war.

Bezug: [[feedback_drucken]]
