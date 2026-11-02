---
name: book-akku-defekt
description: "Surface Book 1 — Akku 1 (Base) dauerhaft defekt, alle Fixes gesetzt + aktiver Schul-Ablauf, der den Crash umgeht"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2eda33f5-c7fc-493e-a3fb-970dac4bd7c3
  modified: 2026-08-12T17:15:30.157Z
---

# Surface Book — Akku 1 (Base-Pack) dauerhaft defekt

## Hardware & Ursache
Surface Book 1. Gen, i7-6600U, 8 GB RAM. 2 Akku-Packs — **Akku 1 (Tastatur-Base) defekt** (Voltage=0, diagnostiziert 22.04.2026), Akku 2 (Tablet-Display) funktioniert. Der Firmware-/Charging-IC-Check beim Power-On bzw. beim Laden hängt sich an dem toten Pack auf (Hardware-Ebene, **vor** Windows — kein Software-Fix möglich, nur Akku-Tausch würde es endgültig lösen; Chris will nicht tauschen, ~300€ zu teuer).

**Alle Auslöser identifiziert (Stand 23.06.2026):** echter Power-State-Wechsel (Kaltstart, Deckel-Standby) UND periodisches Nachladen durch die Charging-IC (auch am Netz im Betrieb, unabhängig vom OS) triggern den Hang/Crash. **Win+L (nur sperren, kein State-Wechsel) ist sicher.**

## Aktive Fixes (alle gesetzt + verifiziert, Stand 23.06.2026)
1. `Disable-PnpDevice -InstanceId "ACPI\PNP0C0A\1" -Confirm:$false` — versteckt Akku1 vor Windows (Identifikation bei Bedarf: `Get-CimInstance -Namespace root/wmi -ClassName BatteryStatus | Select InstanceName, Voltage` → der mit Voltage=0). Reverse: `Enable-PnpDevice ...`
2. Schnellstart aus: `powercfg /h off` (Schnellstart/Hibernate speichert Akku-Zustand in hiberfil.sys — bei totem Pack passen die Werte nicht zur Realität → Boot hängt minutenlang)
3. Modern Standby aus: `PlatformAoAcOverride=0` + STANDBYIDLE/UNATTENDSLP AC+DC=0 — killt alle schlafausgelösten Crashes
4. Deckel-Aktion = „Nichts tun" (AC+DC), NICHT Standby:
   ```
   powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS 5ca83367-6e45-459f-a27b-476b1d01c936 0
   powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS 5ca83367-6e45-459f-a27b-476b1d01c936 0
   powercfg /setactive SCHEME_CURRENT
   ```
5. `BollaTunnelBoot`-Task (Trigger „Beim Systemstart", S4U/kein Login nötig) ergänzt, da der alte `BollaTunnel`-Task nur bei Login/Entsperren feuerte — nach Crash-Reboot fehlte der SSH-Tunnel bis zum nächsten Login.
6. `BollaOfficePin`-Task (12.08.2026 ergänzt, Trigger „Bei der Anmeldung") — pinnt `C:\Users\ernst\OneDrive\Dokumente\Office\*` lokal bei jedem Login, unabhängig vom Tunnel-Status. Details: [[reference_onedrive_storage_sense]].

## Chris' gewählter Schul-Ablauf (bewusst so, funktioniert)
Win+L → Deckel zu → Transport (schläft NICHT ein, Timeout=NIE) → Strom anstecken → Deckel auf → Login. Kein Power-State-Wechsel = umgeht den Firmware-Hang komplett.
**Restrisiko:** Hitze im Rucksack falls ein CPU-Fresser (z.B. Windows Update) während des Transports anspringt (Book läuft ja durch) — Lüftungsschlitze freihalten.

## Falls doch mal ein Crash auftritt
8–15 Sek. Power+Lauter (Force-Reset) — hardwareunschädlich, Fixes bleiben nach Reset erhalten (Registry), kein manuelles Nacharbeiten nötig.

## Diagnose-Befehle (per SSH, User-Session reicht zum Lesen)
```
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /v HiberbootEnabled
powercfg /a
Get-PnpDevice -InstanceId "ACPI\PNP0C0A\1"   # soll Status=Error, Problem=CM_PROB_DISABLED zeigen
```
SSH zum Book nur möglich wenn Book an UND BollaTunnel/BollaTunnelBoot läuft (Port 2222).

## Sonstige Book-Optimierungen (21.04.–13.05.2026)
Autostart deaktiviert (Discord, Steam, Copilot, Creative Cloud, Phone Link deinstalliert, Copilot/OneNote-„Senden" aus), Defender-Scan Sa 2:00, SearchIndexer manueller Start.

## 04.10.2026 — Komplett-Hänger Book (Tastatur/Touchpad tot) + Phone Link wieder drauf
- Symptom: Tastatur+Touchpad reagierten nicht, SSH lief normal, Explorer/DWM „Responding". Vordergrund: **Store-App** (WinStore.App) festgehangen. Spotify (Store-Version, 9 Prozesse, ~800 MB, 39.000 CPU-s) + TextInputHost 347 MB bei nur ~1 GB freiem RAM von 8 GB. Weder Spotify/Store/Explorer/TextInputHost killen noch Strg+Alt+Entf halfen → erst **Power+Lauter 15 s** (Force Restart) löste es. Ursache nicht sicher bewiesen (Verdacht: RAM-Druck + hängende Store-/TextInputHost-Eingabeschicht; Kernel-Power 41 nach Reset).
- **Spotify-Autostart aus:** ist die MSIX-Version, Autostart NICHT im Run-Key, sondern `HKCU\Software\Classes\Local Settings\...\AppModel\SystemAppData\SpotifyAB.SpotifyMusic_zpdnekdrzrea0\Spotify` → `State` (2=an, 1=aus). Auf 1 gesetzt.
- **Phone Link war NICHT installiert** (für ernst); per `winget install --id 9NMPJ99VJBWV --source msstore` neu installiert (v1.26072.257.0). Falls MS es per Update wieder rauswirft/Autostart setzt: StartupApproved prüfen.
- Nach Reset war Reverse-Tunnel :2222 zunächst weg → direkt per `ssh ernst@192.168.178.38` (Heim-IP) ging es. SSH-Shell ist cmd: PowerShell-Skripte per `-EncodedCommand` (UTF-16LE base64) schicken, sonst Quoting-Chaos.
- Explorer-Neustart per SSH: `taskkill /F /IM explorer.exe` startet NICHT automatisch neu; Start via `schtasks /create ... /ru ernst /it` + `/run` (dann wieder löschen).
