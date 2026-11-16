---
name: feedback-tageszeit
description: WSL-Uhr kann nach Reboot mehrere Stunden falsch gehen — IMMER date + Plausibilitätscheck
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 45b0c2b6-e5ff-4c48-ac61-83fd6511af0e
  modified: 2026-07-22T08:31:53.340Z
---

IMMER `date` aufrufen vor Tageszeit-Aussagen.

**Why:** WSL-Uhr kann nach Reboot stundenweise falsch gehen. Konkretes Beispiel 2026-06-09: `date` zeigte 10:06 CEST, echte Zeit war 14:34 CEST — 4,5 Stunden Abstand!

**How to apply:**
- `date` aufrufen, ABER auch auf Plausibilität prüfen: Stimmt die Zeit mit dem Kontext überein (ScheduleWakeup-Timestamps, was Chris sagt, vorherige Nachrichten)?
- ScheduleWakeup zeigt die echte Systemzeit — wenn `date` und ScheduleWakeup-Timestamp stark abweichen: ScheduleWakeup vertrauen
- Bei Unsicherheit kurz beim User nachfragen bevor Zeitversprechen gemacht werden ("laut meiner Uhr ist es X — stimmt das?")

**Zweiter Fehlertyp (22.07.2026):** Nicht nur WSL-Drift ist das Risiko — auch in einer LANGEN laufenden Session, die über Mitternacht/einen Tageswechsel läuft, kann ich veraltete Tagesbezüge aus früheren Nachrichten unreflektiert weiterschleppen (Beispiel: Chris sagte am Vortag "gehe gleich in Sport", ich hab am Folgetag in einer neuen Antwort trotzdem "Guten Sport!" geschrieben, obwohl das system-reminder den Datumswechsel längst angezeigt hatte). **How to apply:** Bei JEDER Aussage mit Zeitbezug (nicht nur Grußformeln!) — auch beiläufige Wünsche/Verweise auf "gleich", "heute", "nachher" — kurz prüfen ob der Bezug noch aus der aktuellen Sitzung stammt oder ein Rest von gestern ist. Bei Zweifel `date` checken statt auf Kontext-Gedächtnis verlassen.
