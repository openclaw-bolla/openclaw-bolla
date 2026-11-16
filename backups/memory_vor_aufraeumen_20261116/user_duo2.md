---
name: Handys: Surface Duo 2 + Huawei P20
description: Chris hat zwei Handys — Surface Duo 2 (ADB via WLAN) und Huawei P20 (zweites Handy, kein ADB wegen Android 11)
type: user
originSessionId: 392e2e08-0564-42ef-9c3b-3e90798109e6
modified: 2026-07-26T18:56:54.796Z
---

## Huawei P20 — Haupt-Handy fürs Telefonieren UND Sprachaufnahmen
- **Chris nutzt das P20 zum Telefonieren** und für mmc-Sprachaufnahmen (Browser, Edge auf dem P20)
- Android 11 → **kein ADB-Management möglich** (Android 11 blockiert wireless ADB ohne USB-Debugging-Aktivierung die auf dem P20 nicht zugänglich ist)
- **Wenn mmc-Audio "dumpf/Hall/leise" klingt → kommt vom P20-Mic, nicht vom Duo 2**

## Surface Duo 2 — Smart-Device, NICHT zum Telefonieren
- **🚨 Mic ist kaputt verklebt** — Chris nutzt das Duo 2 **nicht zum Telefonieren oder für Sprachaufnahmen**
- Bleibt aber als Smart-Device im Einsatz: ADB-Steuerung, Apps, Notification-Hub
- Wenn jemand "Sprache auf dem Handy" sagt → ist es das P20

### Verbindung Duo 2 (ADB):

- **IP:** `192.168.178.20` (DHCP-fest im Heimnetz, ändert sich nie)
- **Connect-Port:** `41873`
- **Verbinden:** `adb connect 192.168.178.20:41873`
- **Pairing** (nur wenn connect fehlschlägt): Duo → Entwickleroptionen → Kabelloses Debugging → Gerät koppeln → neuen IP:Port + 6-stelligen Code verwenden, dann `echo "<code>" | adb pair <ip:port>`

### ⚠️ Unterwegs (fremdes WLAN, z.B. Hotel)
Die feste IP `.20` gilt NUR im Heimnetz. In fremden Netzen (z.B. Hotel-WLAN) bekommt das Duo eine andere
IP vom dortigen Router — Verbindung schlägt mit "No route to host" fehl, wenn man `.20` probiert.
**Ablauf:** Chris liest auf dem Duo unter „Kabelloses Debugging" → „Gerät koppeln" IP:Port + 6-stelligen
Code ab (eigener Port, anders als die Hauptanzeige) → `echo "<code>" | adb pair <ip:port>` → danach von der
**Hauptanzeige** (andere IP:Port als beim Koppeln!) den Connect-Port ablesen → `adb connect <ip>:<port>`.
Live erprobt 26.07.2026 unterwegs auf der Sommerreise (Duo hatte `.134`, Pairing-Port 39123, Connect-Port
41011) — hat auf Anhieb funktioniert, keine Client-Isolation im dortigen Netz.

### 🔒 Sicherheits-Check (14.07.2026)
Android 12, letzter Sicherheitspatch **Oktober 2024** — Microsoft-Support für Duo-Serie ist ausgelaufen, keine OS-/Kernel-Patches mehr (dauerhaft, nicht behebbar). Trotzdem sauberer Zustand: Verified Boot grün, Bootloader gesperrt, SELinux enforcing, kein Root, Verschlüsselung + Bildschirmsperre aktiv, Play Protect an, alle 156 Drittanbieter-Apps nachweislich aus dem Play Store (kein Sideloading). Chrome/WebView/Play Services aktuell (updaten unabhängig vom OS weiter). Einziger konkreter Fund: Banking-Apps (Sparkasse u.ä.) installiert, trotz abgelaufenem OS-Support — Chris nutzt das Duo eh nur als Smart-Device, keine akute Aktion gewünscht. Details/Befehle bei Bedarf reproduzierbar via ADB (siehe Verbindung unten). App-Liste (156 Stück) als möglicher Cleanup-Hebel bei Speicherproblemen vermerkt: [[feedback_adb_trim_caches]].

### ⌨️ Duo-Screenshot Hotkey („autokey")
- **`Win + Strg + S`** → Screenshot der **rechten Duo-Seite** direkt in die Windows-Zwischenablage
- AutoHotkey-Skript: `~/workspace/windows/duoclip.ahk` (+ `duoclip_launch.vbs`), Installer `duo_hotkey_install.ps1`, aktiv unter `%LOCALAPPDATA%\Bolla\`
- In **MP → Surface Duo** ganz oben als fetter lila Banner eingeblendet (damit Chris ihn nicht vergisst)
