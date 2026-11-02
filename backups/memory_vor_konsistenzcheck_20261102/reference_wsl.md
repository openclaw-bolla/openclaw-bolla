---
name: WSL2 Setup & RAM-Limits
description: .wslconfig Konfiguration, vmmem-Freeze-Historie (01.05. + 23.07.2026), Windows-PC hat nur ~16GB RAM total
type: reference
originSessionId: 27bdbc7b-4e9a-4642-a895-df7c4ce6dd2e
modified: 2026-07-23T08:59:00.028Z
---
## RAM-Limit Konfiguration (Stand 23.07.2026)

`C:\Users\ernst\.wslconfig`:
```
[wsl2]
memory=6GB
swap=2GB
processors=4
```

Windows-Host hat insgesamt nur **~16GB RAM**. Das ist die harte Grenze für jede zukünftige Anpassung —
bei 6GB+2GB Swap-Deckel bleiben Windows + Apps noch ~8GB, das ist ein vernünftiger Sicherheitsabstand.

## Freeze-Historie — WICHTIG vor jeder Änderung lesen

**01.05.2026:** vmmem fraß ~10GB RAM ohne Limit, PC fror komplett ein. Fix: `.wslconfig` auf
`memory=4GB/swap=2GB` gedeckelt. Doku: `/mnt/d/OneDrive/Dokumente/WSL_Crash_Erklaerung.docx`

**18.05.2026:** Limit wurde (ohne dokumentierten Grund, in keinem Memory-Eintrag festgehalten) auf
`memory=10GB/swap=4GB` hochgesetzt — damit war der Mai-Schutz wieder aufgehoben.

**23.07.2026:** Exakt derselbe Freeze wieder — diesmal mitten in itslearning-Playwright-Arbeit. WSL ließ
sich danach nicht mehr starten, ca. 30 Min Reparatur nötig (inkl. nachgeholtem `claude doctor`-Update).
Kernel-Log zeigte keinen OOM-Kill, das alte Boot-Log brach um 09:35 Uhr abrupt ohne sauberes Shutdown ab —
klassisches Bild eines VM-Level-Freeze, kein normaler Linux-Crash. Mit nur 16GB Host-RAM war ein
10GB+4GB-Deckel für die WSL-VM allein schlicht zu aggressiv. Limit wieder auf 6GB/2GB runtergesetzt.

Zusätzlich gefixt: 3 itslearning-Playwright-Skripte (`itslearning_post_kurstag.py`,
`itslearning_delete_latest_message.py`, `itslearning_delete_resources.py`) schlossen den Chromium-Browser
nur am Ende eines *erfolgreichen* Laufs — bei Abbruch/Absturz blieb er als Waisenprozess im RAM hängen.
Jetzt in try/finally verpackt.

## Frühwarn-Wächter (seit 23.07.2026, erweitert nach Chris' Nachfrage)

`scripts/wsl_memory_watchdog.py`, Cron alle 2 Min. Prüft `free -m` gegen den 6144MB-Deckel, 3 Stufen:
- **≥75% (WARN):** Telegram-Warnung (nur beim Überschreiten, kein Dauerspam), Log.
- **≥88% (CRITICAL):** Killt NUR eindeutig verwaiste Chromium/Playwright-Prozesse (PPID=1 — Elternskript
  bereits tot). Telegram-Alarm mit Top-Verbrauchern.
- **≥94% (EMERGENCY):** Killt ALLE Chromium/Playwright-Prozesse, auch lebende — also auch mitten in
  einer laufenden Aktion (z.B. itslearning-Upload). **Chris hat zurecht nachgehakt:** die reine
  Waisen-Logik hätte NICHT geholfen, wenn der Speicher gerade durch eine aktive, noch laufende Aktion
  hochläuft — deshalb diese dritte Stufe als echte Notbremse. Kein automatisches `wsl --shutdown` — das
  bleibt Chris' Entscheidung, nur als Option im Alarm genannt.
- Status in `state/wsl_memory_watchdog.json`. Schwellen im Skript bei künftigen `.wslconfig`-Änderungen
  mit anpassen (`WSLCONFIG_MEM_MB`).

**Zusätzlich in `itslearning_post_kurstag.py` (proaktive Selbst-Bremse):** vor jedem Kurs in der Schleife
prüft das Skript `/proc/meminfo` selbst; bei ≥80% bricht es sauber ab (mit `browser.close()` über das
bestehende try/finally) statt vom Wächter-Cron hart abgeschossen zu werden. Das ist die bevorzugte erste
Verteidigungslinie — der externe Wächter ist das Netz darunter, falls das Skript selbst nicht mehr
reagiert (z.B. bei einem echten Hänger/Deadlock in Playwright).

## Nützliche Befehle
- WSL sofort beenden (gibt RAM frei): `wsl --shutdown`
- WSL neu starten: `wsl` im Terminal
- RAM-Verbrauch prüfen: Task-Manager → vmmem
- Nach `.wslconfig`-Änderung ist ein `wsl --shutdown` nötig, damit sie greift — killt aber laufende Sessions,
  also mit Chris timen, nicht einfach mittendrin ausführen.

**Why:** vmmem kann ohne enges Limit einen Großteil des Host-RAM fressen → kompletter PC-Freeze, nicht nur
ein WSL-Absturz. Bei nur 16GB Host-RAM ist der Sicherheitsabstand schmal.
**How to apply:** Vor JEDER künftigen Änderung an `.wslconfig` diese Historie lesen und die 16GB-Grenze im
Kopf behalten. Falls Chris wieder über langsamen PC/Einfrieren klagt: `.wslconfig`, vmmem-Auslastung UND ob
gerade Playwright/Chromium-Automatisierung lief, prüfen. [[project_itslearning_automation]]
