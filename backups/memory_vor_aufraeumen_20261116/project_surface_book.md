---
name: project_surface_book
description: "Surface Book Akku-Problem, Boot-Fix, SSH-Diagnose — alles was bei Problemen sofort bekannt sein muss"
metadata: 
  node_type: memory
  type: project
  originSessionId: ddb698ce-8e5e-4a23-9905-6d99260a7483
  modified: 2026-08-31T10:31:07.091Z
---

## Bildschirm-Timeout (geklärt 21.08.2026)
Chris erinnerte sich, der Bildschirm sei mal auf "immer an" gestellt worden — Check per `powercfg /query`
zeigte: Das stimmt nur für den **Ruhezustand** (Sleep, `STANDBYIDLE` = 0 bei AC+DC, vermutlich damit der
SSH-Reverse-Tunnel für die Fernwartung nicht abreißt). Der **Bildschirm** selbst (`VIDEOIDLE`) steht auf
Windows-Standard: 30 Min bei Netzbetrieb, 3 Min im Akkubetrieb — war nie separat auf "nie" gesetzt.
**Chris' Entscheidung:** So lassen, kein Handlungsbedarf — nutzt das Book vorwiegend in der Schule, auch
bei >30 Min Inaktivität während eines Praktikums wacht es dank Sleep=nie sofort wieder auf, kollidiert
nicht mit dem Akku-Ausfall-Problem (siehe unten), da unabhängige Einstellungen.
> ⚠️ **ÜBERHOLT am 31.08.2026:** VIDEOIDLE AC wurde auf „Nie" (0) gesetzt — es gibt einen Display-
> Aufwach-Hänger nach dem 30-min-Bildschirm-Aus. Details unten „ZWEITES Fehlerbild".

# Surface Book — Dauerproblem Akku & Boot

## Das Gerät
- Surface Book (Chris' Schulrechner, Hostname: Chris_Surface_B, User: ernst)
- SSH-Zugang: Port 2222 über Reverse Tunnel (siehe [[reference_technical]])

## Kernproblem: Akku 1 ist defekt
- Akku 1 (`ACPI\PNP0C0A\1`) ist physisch kaputt — verursacht Boot-Loops, Aufwach-Probleme, Systemabstürze
- **Lösung:** Akku 1 per `Disable-PnpDevice` deaktiviert → Windows sieht nur noch Akku 0
- Akku 0 (ID: `6142SMPX906980`) ist der gesunde, funktioniert normal

## Angewendete Fixes (alle aktiv, Stand 27.05.2026)

### Fix 1: Akku 1 deaktiviert
```powershell
Disable-PnpDevice -InstanceId "ACPI\PNP0C0A\1" -Confirm:$false
```
Status prüfen:
```powershell
$d = Get-PnpDevice -InstanceId "ACPI\PNP0C0A\1"
Write-Host $d.Status $d.Problem
# Soll sein: Error / CM_PROB_DISABLED
```

### Fix 2: HiberbootEnabled = 0
- Fast Startup (Hybrid Boot) deaktiviert — verhindert Boot-Probleme nach Updates
- Registry: `HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Power\HiberbootEnabled = 0`
- **Überlebt Windows Updates** via Scheduled Task `BollaKeepHiberbootOff` (läuft als SYSTEM)

### Fix 3: CPU-Fresser dauerhaft deaktiviert
- Windows Search (WSearch): `Disabled`
- Windows Widgets: Policy `AllowNewsAndInterests=0` + WebExperience Pack entfernt

## Diagnose bei neuen Problemen (Checkliste per SSH)

```powershell
# 1. Akku 1 noch deaktiviert?
$d = Get-PnpDevice -InstanceId "ACPI\PNP0C0A\1"
Write-Host "Akku1:" $d.Problem   # Soll: CM_PROB_DISABLED

# 2. HiberbootEnabled noch 0?
(Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Power" -Name HiberbootEnabled).HiberbootEnabled
# Soll: 0

# 3. Scheduled Task aktiv?
(Get-ScheduledTask -TaskName "BollaKeepHiberbootOff").State
# Soll: Ready
```

## Wenn Akku 1 wieder aktiviert wurde (z.B. nach Windows Update)
```powershell
Disable-PnpDevice -InstanceId "ACPI\PNP0C0A\1" -Confirm:$false
```
→ Kein Neustart nötig, wirkt sofort.

## ⚠️ Neuer Vorfall 23.07.2026 — 2× kompletter Stromausfall an einem Tag (KEIN Windows-Crash)

Chris fand das Book zweimal am selben Tag komplett "aus" vor, ohne selbst heruntergefahren zu haben —
brauchte jeweils den 15-Sek-Power-Button-Reset zum Wiederhochfahren. Per SSH/Event-Log verifiziert:
- EventID 41 (Kernel-Power, unsauberer Neustart) zweimal: vor 09:06 Uhr und vor 12:12 Uhr.
- **Kein Bugcheck:** `BugcheckCode = 0`, keine Bluescreen-Parameter — es war KEIN Windows-Absturz.
- `LongPowerButtonPressDetected = true` — deutet auf einen harten Stromausfall/Power-Cutoff hin, nicht auf
  ein Software-Problem.
- Die 3 Standard-Fixes (Akku 1 deaktiviert/`CM_PROB_DISABLED`, HiberbootEnabled=0, Task
  `BollaKeepHiberbootOff` aktiv) waren zu beiden Zeitpunkten intakt — also NICHT der alte Akku-1-Boot-Loop.
- Akku-Status zum Zeitpunkt der Prüfung: 100%/OK — sagt aber nichts über kurze Aussetzer.
- Ca. 3 Tage zuvor (20.07.2026) gab es ein Windows-Update (KB5121767) — zeitlich kein zwingender
  Zusammenhang erkennbar, da die Schutzmaßnahmen unberührt blieben.

**Verdacht (nicht bewiesen):** Da nur noch Akku 0 aktiv ist (Akku 1 seit Mai defekt/deaktiviert), könnte
Akku 0 selbst anfangen zu schwächeln (Wackelkontakt/kurzer Aussetzer statt sauberer Abschaltung bei
niedrigem Ladestand). Zwei Vorfälle an einem Tag sind auffällig gegenüber der bisher dokumentierten,
seltenen "Standby-Schluckauf"-Eigenheit unten.

**Nächster Schritt bei Wiederholung:** Falls sich das in den nächsten Tagen wiederholt, eher als
Hardware-Thema (Akku 0 prüfen/tauschen) einstufen statt als Software-Fix-Kandidat. Battery-Report wurde
23.07. nach `C:\Users\ernst\battery_report.html` exportiert (Design-vs-Full-Charge-Kapazität dort einsehbar,
falls es weitergeht).

## ⚠️ Vorfall 18.08.2026 — 3. Beleg für Akku-0-Verdacht (nach 3 ruhigen Wochen)

Nach dem 23.07.-Vorfall lief das Book vom 12.08. abends bis 18.08. 13:31 Uhr durchgehend ohne
Unterbrechung (kein einziger sauberer Shutdown im Log) — dann harter Stromausfall, Chris musste
15-Sek-Power-Reset machen. Per SSH verifiziert: `BugcheckCode=0` (kein Windows-Crash),
`LongPowerButtonPressDetected=True` (echter Power-Cutoff, keine Software-Ursache) — identisches
Muster wie 23.07. Frischer Battery-Report (`C:\Users\ernst\battery_report_neu.html`): Akku 0
Design Capacity 51.000 mWh, Full Charge Capacity nur noch **32.557 mWh (~64 %)** — spürbarer
Kapazitätsverlust. Kausalität nicht bewiesen, aber Verdacht bleibt: alternder Akku 0 könnte
intern wackeln (Kontakt/Spannungseinbruch) und die Charging-IC zum Hard-Cutoff bringen — analog
zum Fehlerbild, das Akku 1 vor seinem Totalausfall zeigte.

**Häufigkeit bisher:** 23.07. (2× an einem Tag), dann 3 Wochen ruhig, dann 18.08. — eher seltener,
wiederkehrender Aussetzer als tägliche Verschlechterung. Bei kürzer werdenden Abständen: Akku-0-
Tausch erwägen (Chris lehnte bei Akku 1 einen Tausch als zu teuer ab, ~300€ — Referenzpreis).

**Nächster Schritt bei Wiederholung:** Neuen Battery-Report ziehen, Full-Charge-Kapazität mit
32.557 mWh vergleichen — sinkt sie weiter deutlich, spricht das stärker für echten Akku-Defekt statt Zufall.

## Geplante 17-Tage-Abschaltung (Sommerreise, 24.07.–ca. 10.08.2026)

Chris schaltet das Book für die gesamte Dauer der Sommerreise komplett aus, danach wieder normal an. Grund
für die Nichterreichbarkeit in diesem Zeitraum ist also geplant/gewollt, kein neuer Vorfall — nicht mit dem
Stromausfall-Vorfall oben verwechseln. Beim Wiedereinschalten danach ist der bekannte 30+-Sek-Kaltstart
(wartet auf Mindestladung im defekten Tablet-Akku, siehe [[user_devices]]) normal, kein Fehler.

## ⚠️ 31.08.2026 — EventID-41-Häufung + Chris nennt erstmals „Scharnierverbindungsproblem"

Vollständige SSH-Diagnose (Skripte `scratchpad/book_diag.ps1` + `book_diag2.ps1`):
- **Alle 3 Fixes intakt:** Akku1 = Error/CM_PROB_DISABLED, HiberbootEnabled=0, Task BollaKeepHiberbootOff=Ready.
- **Akku 0:** FullChargedCapacity **36.652 mWh** (Design 51.000 → ~72 %), **Cycle Count 524**, Voltage 8515 mV,
  100 %, PowerOnline. Gegenüber 18.08. (32.557 mWh) NICHT weiter gefallen, eher leicht erholt → Kapazitäts-
  wert schwankt, kein Freefall. Kein akuter Akku-Notfall.
- **EventID 41 (unsauberer Neustart) häuft sich:** 23.07.(×2) · 18.08. · 20.08. · **26.08.(×2)** · **27.08.** ·
  **31.08. 11:18**. Von „~wöchentlich" auf „fast jeder Schultag". Alle **Bugcheck = 0** (kein Bluescreen).
- **Keine WHEA-Hardwarefehler** in 14 Tagen. **EventID 105 (Stromquellen-Wechsel)** nur 2× in 3 Tagen
  (nachts 30.08.) → Netzteil/Ladekontakt flattert NICHT dauernd. **EventID 521 (Akku-Anzahl-Änderung)**
  nur beim Booten, nie im Betrieb → Base fällt im Betrieb nicht messbar weg.
- Am 31.08. zusätzlich 2× „System-initiierter Neustart" (10:39, 11:59) — sieht nach erzwungenen/
  aufgeschobenen Reboots aus (Windows-Update-Kette oder Recovery nach Instabilität).

**Deutung:** Ausgeschlossen sind Windows-Crash (kein Bugcheck), Silizium-Fehler (kein WHEA), dauerndes
Netzteil-Wackeln (105 selten), Base-Akku-Abfall im Betrieb (521 nur Boot), alter Akku-1-Boot-Loop (Fix
intakt). Übrig bleibt: **intermittierende physische Verbindung** — alternder Akku 0 mit internem
Wackler ODER der **Tablet↔Base-Flexverbinder im Scharnier** (bekannte Schwachstelle der 1. Gen). Ein
sauberer physischer Dropout hinterlässt praktisch keine Logspur — genau das ist hier das Bild. Chris
vermutet selbst das Scharnier (erste Erwähnung 31.08.).

**Klärung „Bolla-Diagnose":** Der Befehl / die `bolla-status`-Skill prüft NUR den MC-Server (API, Tunnel,
Aufgaben) — er fasst das Book NICHT an, es läuft KEIN automatischer Book-Watcher. Book-Checks macht Bolla
manuell per SSH (Port 2222). Offen/angeboten: kleinen Scheduled-Task auf dem Book, der EventID-41-
Vorfälle + Akku-Snapshot in eine Datei schreibt, die Bolla auslesen kann.

**Chris' Beobachtungen (31.08.2026, nach Rückfrage):**
- Scharnier: **wackelt NICHT**, Bild flackert nicht, kein Aussetzer beim Bewegen → mechanisch/
  elektrisch im Betrieb solide. „Scharnier reinigen" ist damit vom Tisch (Chris' eigenes Fazit).
- **Detach-Taste löst das Tablet seit JAHREN nicht** (Chris: „hatte ich dir schon mal mitgeteilt" —
  war nicht/nicht auffindbar im Memory, jetzt hier festgehalten). Also KEIN neues Problem.
- Eben getestet: Detach gedrückt → Taste **leuchtet kurz ROT** → Display-Meldung **„Tablet-Akku ist
  niedrig. Laden Sie den Akku jetzt, …"** — und das bei **Windows-Anzeige 100 %** (Akku 0).

**Deutung dazu:** Die Detach-Verriegelung (Muskeldraht-Latch) ist eine Sicherheits-Interlock, die auf
den Zustand BEIDER Akkus schaut und einen kräftigen Stromimpuls braucht. Rot + „Akku niedrig" trotz
100 % passt zu zwei sich ergänzenden Ursachen:
1. **Toter Base-Akku (Akku 1)** wird vom Embedded-Controller weiterhin gesehen (das `Disable-PnpDevice`
   versteckt ihn nur vor Windows, nicht vor der Detach-Firmware) → Interlock verweigert generisch mit
   „Akku niedrig". Passt zu „geht seit Jahren nicht" — Base-Akku war wohl schon lange die Schwachstelle.
2. **Verschlissener Tablet-Akku (Akku 0):** ~72 % der Design-Kapazität, 524 Zyklen, und der
   Kapazitätswert springt (18.08. 32.557 → 31.08. 36.652 mWh) → die Fuel-Gauge ist dekalibriert, die
   „100 %" also unzuverlässig; unter dem Latch-Stromimpuls sackt die alte Zelle weg.

**Fazit / Handlungsoptionen:**
- Der EINZIGE echte Fix wäre ein **Akku-Tausch** (Akku 1 bzw. Akku 0) — Chris hat das bei Akku 1
  wegen ~300 € abgelehnt. Beim Book 1 ist v. a. der Tablet-Akku ein aufwändiger Eingriff (verklebtes
  Display). Bleibt abgelehnt.
- **Detach braucht Chris nicht** (nutzt das Book als Laptop) → kein Handlungsdruck.
- Real relevant bleibt die **EventID-41-Häufung im Unterricht** (kein BSOD, kein WHEA = Spannungs-
  einbruch unter Last, weil nur noch der eine, schwächelnde Akku puffert). Gleiche Wurzel wie die
  Detach-Verweigerung.
- **✅ Auto-Watcher eingerichtet (31.08.2026, Chris „ja"):**
  - Skript `C:\Users\ernst\bolla_book_health.ps1` (Quelle: `scratchpad/bolla_book_health.ps1` bzw.
    Deploy via `scratchpad/deploy_book_watch.ps1` — base64-eingebettet, damit SSH-Quoting egal ist).
  - 2 Scheduled Tasks (nicht-elevated, „nur interaktiv", laufen als User ernst):
    `BollaBookHealthWatch` (Trigger onlogon — fängt den Login nach einem Crash) +
    `BollaBookHealthWatchDaily` (täglich 07:15).
  - Schreibt bei jedem Lauf einen Block nach `C:\Users\ernst\bolla_book_health.log` (Akku-Snapshot:
    Charge/Voltage/Charging/PowerOnline/FullCharge, EventID-41-Zähler 7d/30d, Fix-Status). NEUE
    EventID-41 seit letztem Lauf → zusätzlich in `C:\Users\ernst\bolla_book_health_ALERTS.log`.
    State in `…health.state` (seeded auf 2026-08-31T11:18:39 = neuester bekannter 41). Frischer
    Battery-Report bei jedem Lauf → `C:\Users\ernst\bolla_book_battery_report.html`. Log kappt sich
    bei >1200 Zeilen auf 1000.
  - **Bolla liest ihn per SSH:**
    `ssh -p 2222 -i /home/bolla/.ssh/id_ed25519 ernst@localhost 'powershell -Command "Get-Content C:\Users\ernst\bolla_book_health_ALERTS.log -Tail 40; Write-Output ---; Get-Content C:\Users\ernst\bolla_book_health.log -Tail 30"'`
  - **Baseline 31.08.2026:** EventID-41 7d=4 / 30d=6, Akku0 100 % / 8515 mV / FullCharge 36.652 mWh.
    Beobachten: steigt 7d weiter (Richtung täglich) ODER FullCharge fällt klar unter ~30.000 →
    dann Akku-Tausch/Book-Ablösung ernsthaft anstoßen. ALERTS.log hat einen einmaligen Seeding-
    Eintrag mit allen 6 Alt-Crashes (Rauschen, ignorieren).
- Frischer Battery-Report: `C:\Users\ernst\battery_report_20260831.html` (Detail-Laufzeiten dort,
  bei Bedarf per SSH auslesen).

## 🖥️ 31.08.2026 (nachmittags) — ZWEITES Fehlerbild: Display-Aufwach-Hänger (≠ Cutoff)

Chris' Vorfall: Win+L gedrückt, später Bildschirm komplett schwarz, Enter → weißes Kamera-Symbol
(Windows Hello) kurz, dann wieder tot. **Kein 15-Sek-Reset — nur Deckel zu + auf → Bild zurück,
Hello-Login direkt auf den Desktop.**

**SSH-Befund (17:56):** LastBoot 14:01 (EC-Reset), **seither KEIN EventID 41 / kein Reboot / keine
System-Warnung 14:05–17:56** — Book lief ~4 h durch, quer durch den Vorfall. Kein 4101/4102
(Display-Treiber-TDR) in 3 Tagen. → **Dieser Vorfall war KEIN Stromausfall.**

**Ursache:** `VIDEOIDLE` (Bildschirm ausschalten nach) stand auf **AC 1800 s / DC 180 s** — aktiv,
nicht „nie". (Die 21.08.-Notiz „30/3 min, so lassen" war korrekt beobachtet, aber die Entscheidung
„kein Handlungsbedarf" ist mit diesem neuen Fehlerbild überholt.) Nach dem 30-min-Display-Aus
kommt **Panel / eDP-Link manchmal nicht sauber zurück**: Enter weckt das System (Hello-Kamera
flackert), Bildausgabe bleibt tot. **Deckel zu/auf erzwingt echten eDP-Neuanlauf** — was
Tastatur/Maus nicht auslösen. Kein Log-Eintrag, kein Datenverlust.
→ Wahrscheinlich waren **einige frühere „Abstürze" mit 15-Sek-Reset in Wahrheit DAS** (nicht die
mit EventID 41 + LongPowerButtonPress — die waren echte Cutoffs).

**Gemacht (Chris „mach", 31.08. ~18:00):**
```
powercfg /setacvalueindex SCHEME_CURRENT SUB_VIDEO VIDEOIDLE 0
powercfg /setactive SCHEME_CURRENT
```
→ **AC-Bildschirm-Timeout = „Nie"** (verifiziert: Wechselstrom-Index 0x00000000). DC bleibt 3 min.
Schule = immer Netz → Auslöser dort weg.

**Regel für Chris ab jetzt:** schwarzes Bild → **ERST Deckel zu + auf**. 15-Sek-Power-Reset
(Power + Lautstärke hoch) nur noch für echten Stromausfall: rote Detach-Taste, KEINE Kamera-LED,
komplett tot. Wenn Display-Hänger trotz VIDEOIDLE=Nie weitergeht → Windows Hello Gesichts-
anmeldung testweise aus, nur PIN (Kamera-Frame-Server als Verdächtiger).

**Lernpunkt Bolla:** Die 14:08-Analyse („Win+L / Standby irrelevant, Book kann sich gar nicht
schlafen legen") war zu absolut — hat übersehen, dass VIDEOIDLE (reines Bildschirm-Aus)
unabhängig von den fehlenden S3/S0-Zuständen läuft und selbst ein Fehlerpunkt ist. Chris hat den
Fehler zu Recht angemerkt.

## Bekannte Eigenheiten
- Nach ~20 Min Akkubetrieb + Transport: gelegentlicher Standby-Schluckauf beim Strom-Einstecken → einmaliger Force-Reset (15 Sek Power + Lautstärke hoch) löst das
- Windows Update kann HiberbootEnabled kurz zurücksetzen — Task korrigiert das bei nächstem Start
- Akku 1 wird durch Windows Updates NICHT wieder aktiviert (getestet 27.05.2026)

**Why:** Akku 1 ist physisch defekt und verursacht seit Wochen Boot-Loops und Absturz-Probleme in der Schule.
**How to apply:** Bei jedem Surface Book Problem zuerst diese Checkliste per SSH abarbeiten, bevor neue Hypothesen aufgestellt werden.
