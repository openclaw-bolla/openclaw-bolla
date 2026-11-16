---
name: reference-stop-bolla
description: Wie Chris eine laufende Bolla-Aktion/WSL bei drohendem Problem zuverlässig stoppen kann
metadata:
  type: reference
  originSessionId: current
  modified: 2026-07-23T09:01:55.150Z
---

## Gestufte Notbremse, wenn Chris Anzeichen für ein drohendes Problem sieht (z.B. PC wird langsam)

1. **Esc / Strg+C** im Claude-Code-Terminal — bricht die aktuelle Operation ab (`app:interrupt`).
   Schneller erster Versuch, kostet nichts.
2. **Zuverlässiger, wenn's wirklich zählt: neues PowerShell-Fenster öffnen (NICHT im
   hängenden Fenster rumhämmern) → `wsl --shutdown`.** Fährt die komplette WSL-VM sauber runter,
   killt dabei alle Kindprozesse (auch Chromium/Playwright), gibt sofort RAM frei. Funktioniert
   unabhängig davon, ob Bolla/die Session noch reagiert, weil rein Windows-seitig.
3. **Notnagel:** Task-Manager → Prozess `vmmem` (manchmal `vmmemWSL`) → Task beenden.

**Why:** Recherche via claude-code-guide-Subagent (23.07.2026) ergab: Esc/Strg+C sind bei Claude Code
gut dokumentiert (`chat:cancel`, `app:interrupt`), aber **ob dabei ein von Bolla per Bash gestarteter
Kindprozess (z.B. ein laufendes Playwright/Chromium-Skript) sauber mitbeendet wird oder als Waise
weiterläuft, ist nirgends dokumentiert**. Also keine Garantie, worauf man sich in einem echten
Notfall verlassen sollte. `wsl --shutdown` ist der einzige Schritt, der sicher unabhängig von Bollas
eigenem Zustand funktioniert — genau das war beim [[reference_wsl]]-Vorfall vom 23.07.2026 der Kern
von Chris' Frage.

**How to apply:** Diese 3 Stufen bei Bedarf direkt an Chris ausgeben, wenn er nach "wie stoppe ich
dich/das" fragt. Der neue [[reference_wsl]]-Wächter (`wsl_memory_watchdog.py`) soll idealerweise
Vorwarnung geben, BEVOR Chris überhaupt zu Stufe 2/3 greifen muss.
