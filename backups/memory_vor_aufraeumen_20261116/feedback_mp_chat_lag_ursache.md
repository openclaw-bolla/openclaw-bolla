---
name: feedback-mp-chat-lag-ursache
description: "MP-Bolla-Chat wird zäh (Tippverzögerung) NICHT wegen offener Edge-Tabs — sondern weil jede Chat-Nachricht einen neuen `claude -p`-Prozess in WSL startet, der mit anderen parallel laufenden WSL-Prozessen um den 6GB/2GB-Deckel konkurriert"
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-09-28T08:32:54.192Z
---

Chris hatte am 28.09.2026 einen laggy MP-Bolla-Chat (Eingabefeld extrem langsam) — bereits das 3. Mal.
Meine erste Vermutung ("60+ offene Edge-Tabs") war **falsch** und wurde von Chris zu Recht korrigiert:
die Tab-Gruppen-Struktur (vertikale Tabs, thematisch organisiert) besteht seit über einem Jahr unverändert
und war nie vorher ein Problem — Korrelation ("gerade viele Tabs offen") ist keine Ursache.

**Echte Ursache, verifiziert im Code:** `mission_control_api.py:5595` (`bolla_chat_stream`) startet bei
JEDER MP-Chat-Nachricht einen **neuen** `claude -p --resume <session_id>`-Prozess — volle Claude-Code-CLI
(Node-Runtime, MCP-Server-Config, Session-Historie von der Platte), kein leichter API-Call. Das läuft
**innerhalb von WSL**, genau wie diese Terminal-Session (auch ein `claude`-Prozess) und Cron-Jobs.

**Wenn mehrere solcher Prozesse gleichzeitig aktiv sind** (z.B. Chris tippt im MP-Chat, WÄHREND parallel
eine Terminal-Session mit mir läuft und ich gerade Playwright/PowerShell/PowerPoint-Automatisierung
mache) — konkurrieren sie alle um den knappen **6GB RAM / 2GB Swap-Deckel** der WSL-VM
(siehe [[reference_wsl]], Deckel bewusst niedrig wegen der beiden dokumentierten vmmem-Freezes vom
01.05. und 23.07.2026). Das äußert sich als spürbare Zähigkeit — u.a. in der Eingabe des gerade aktiv
genutzten Chat-Fensters.

**Warum NICHT einfach den WSL-RAM-Deckel erhöhen:** Windows-Host hat nur ~16GB total. Am 28.09. waren
bereits **nur 2,6GB frei**, BEVOR WSL überhaupt mitgerechnet wird (Edge, OneDrive, svchost etc. fressen
den Rest). Jede Erhöhung des WSL-Caps ginge 1:1 von diesem ohnehin knappen Windows-Rest ab — genau das
Muster, das am 18.05.2026 zum Freeze vom 23.07. führte. Ohne mehr Windows-seitigen freien RAM ist eine
Cap-Erhöhung riskant, kein sauberer Fix.

**How to apply:**
- Bei künftigen Berichten über zähe MP-Chat-Eingabe **zuerst prüfen, ob parallel mehrere `claude`-Prozesse
  liefen** (Terminal-Session + MP-Chat gleichzeitig, oder Hintergrund-Skripte), NICHT vorschnell auf
  Edge-Tabs tippen.
- **Eigene Disziplin:** Wenn erkennbar ist, dass Chris gerade parallel im MP-Chat aktiv ist, keine
  zusätzlichen schweren Hintergrundjobs (Playwright-Renderings, PowerPoint-COM, Massen-Skripte) parallel
  dazu starten, sondern sequenziell abarbeiten oder ihn kurz vorwarnen.
- Chris selbst: Terminal-Session und MP-Chat möglichst nicht gleichzeitig intensiv nutzen, wenn's spürbar
  hakt — zwei unabhängige `claude`-Prozessbäume im selben knappen RAM-Topf.
- `wsl_memory_watchdog.py` bleibt das Sicherheitsnetz (killt Waisen-/alle Chromium-Prozesse ab 88%/94%),
  ist aber kein Fix für CPU-Kontention zwischen zwei aktiven, legitimen `claude`-Prozessen.
