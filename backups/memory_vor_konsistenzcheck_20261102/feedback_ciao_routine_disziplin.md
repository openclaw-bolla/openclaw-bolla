---
name: feedback-ciao-routine-disziplin
description: Session-Ende-Routine muss bei "Ciao" SOFORT automatisch laufen, nicht erst auf Nachfrage
metadata:
  type: feedback
---

Bei "Ciao"/Verabschiedung die komplette Session-Ende-Routine aus CLAUDE.md sofort selbst ausführen
(aktuell.md updaten, Tagesnotiz schreiben, git commit+push, OneDrive-Backup) — nicht nur mit
"Ciao! Bis später 🐾" antworten und abwarten.

**Why:** Am 12.08.2026 abends nur reflexartig "Ciao" erwidert, ohne die Routine abzuarbeiten. Chris
musste explizit nachfragen ("hast du alles gesichert?") und dann korrigieren ("wir hatten doch
vereinbart, das läuft automatisch"). Dabei kam raus: letzter Commit war von morgens, der ganze
Nachmittag/Abend (Schuljahr-Termin-Fixes, itslearning Kurstag 2, OneDrive-Pin-Fix) war ungesichert,
OneDrive-Backup war ebenfalls seit dem Vormittag nicht mehr gelaufen.

**How to apply:** Sobald Chris sich verabschiedet (Ciao, Tschüss, bis später o.ä.) — BEVOR die
Abschiedsantwort rausgeht oder direkt danach im selben Zug — die Routine durchlaufen: 1) aktuell.md
Stand prüfen/updaten, 2) Tagesnotiz `memory/YYYY-MM-DD.md` um ungedeckte Aktionen seit letztem Eintrag
ergänzen, 3) `git add -A && git commit && git push` im Workspace, 4) OneDrive-rsync-Backup anstoßen
(darf im Hintergrund laufen). Erst danach "Ciao" sagen bzw. falls schon gesagt, unaufgefordert
nachschieben — nicht warten bis nachgefragt wird. Siehe auch [[feedback_neue_session_nach_ciao]].
