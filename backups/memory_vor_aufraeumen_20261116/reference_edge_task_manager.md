---
name: reference-edge-task-manager
description: Shift+Esc öffnet Edges eigenen Task-Manager (Tab/Prozess-CPU+RAM mit Titel) — Standard-erster-Schritt bei Lüftergeräusch/hoher Last im Studio
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2da1ee0d-23f9-423f-bb42-3f1b3ba4c5f9
  modified: 2026-09-16T08:11:41.996Z
---

**Shift+Esc** in Microsoft Edge öffnet den eingebauten Edge-Task-Manager — zeigt pro Tab/Extension/Prozess CPU- und RAM-Verbrauch inkl. Seitentitel. Deutlich schneller als über PowerShell (`Get-Process`) den passenden `msedge.exe`-Renderer-Prozess einer Karteikarte zuzuordnen, da PowerShell nur PID/CPU-Zeit liefert, aber keinen Tab-Titel.

**Wie es genutzt wurde (15.09.2026):** Studio-Lüfter lief laut, Diagnose per `ps aux` (WSL sauber) + PowerShell `Get-Process`/`Get-CimInstance Win32_Process` fand einen Edge-Renderer-Prozess, der seit 09:26 Uhr fast 6h durchgehend ~1 Kern ausgelastet hatte — aber ohne Fenstertitel nicht identifizierbar, welcher Tab es war. Chris fand den Tab danach selbst über Shift+Esc. Edge beruhigte sich kurz danach von selbst wieder.

**Wie anwenden:** Bei künftigem Lüfter-/Hitze-Problem am Studio-Rechner: zuerst `ps aux` (WSL) + PowerShell-Prozessliste zur groben Eingrenzung (System vs. Browser vs. sonstige App), dann bei Verdacht auf Edge sofort Chris den Shift+Esc-Weg vorschlagen statt selbst mühsam PIDs zu Tabs zurückzuverfolgen.
