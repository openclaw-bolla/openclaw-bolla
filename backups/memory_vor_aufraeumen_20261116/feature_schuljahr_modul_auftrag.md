---
name: feature-schuljahr-modul-auftrag
description: "mp Schuljahr 26/27 — Auftragsfeld pro Vorjahres-Modul, automatisch per Cron-Wächter ausgeführt"
metadata: 
  node_type: memory
  type: project
  originSessionId: 33accb2a-0f6a-4d2c-a25a-be8944755fd0
---

Auf der mp-Seite "Schuljahr 26/27" hat die Box "Module aus dem Vorjahr (25/26)" seit 13.07.2026 pro Modul
ein Eingabefeld + 📌-Button, in das Chris einen freien Auftrag zu der jeweiligen PPT eintragen kann
(z.B. "formatier Folie X ordentlich" oder eine ganze Aufgabenstellung).

**Ablauf (vollautomatisch, kein Nachfragen nötig):**
1. Chris trägt Auftrag ein, klickt 📌 → gespeichert in `data/schuljahr2627.json` (`module_vorjahr[].auftrag`),
   zusätzlich in Bolla-Queue + Zwischenablage.
2. `scripts/schuljahr_modul_watcher.py` (Cron alle 5 Min, `*/5 * * * *`) prüft `module_vorjahr` auf offene
   Aufträge und startet bei Fund automatisch einen headless `claude -p --model claude-sonnet-5
   --dangerously-skip-permissions` Lauf mit vollem Tool-Zugriff — der Auftrag wird also wirklich ausgeführt
   (Datei suchen, bearbeiten), nicht nur geplant.
3. Der Prompt für den Wächter enthält bereits die Kernregeln: [[feedback_ppt_direkt_bearbeiten]] (direkt in
   der PPTX, kein Extra-Word-Doc, vorher Backup), plus die Anweisung bei Unklarheit lieber eine Rückfrage
   zu stellen statt zu raten (Status-Marker `STATUS: ERLEDIGT` vs. `STATUS: RUECKFRAGE` im Output).
4. Bei Erfolg: Auftragsfeld wird automatisch geleert (`/api/schuljahr2627/modul-update` mit leerem Text) +
   Telegram-Kurzmeldung an Chris. Bei Rückfrage/Unklarheit: Feld bleibt stehen, Telegram-Rückfrage statt
   "erledigt"-Meldung.

**Backend-Routen:** `/api/schuljahr2627/modul-update` (Auftrag speichern/leeren), `/api/schuljahr2627/modul-nudge`
(Prompt bauen + in Queue/Zwischenablage legen, ruft Chris NICHT automatisch etwas aus — das macht erst der
separate Watcher-Cron).

**Analog zum bestehenden Termine-Mechanismus** (Auftragsfeld pro Unterrichtstermin in derselben Seite,
dort aber noch ohne Auto-Wächter — nur manuelles 📌 + Chat-Nachfrage).

**Stolperstein-Historie:** Erster Testauftrag (13.07.26) bezog sich fälschlich auf Folie 7 (Konzept-Erklärung),
gemeint war Folie 10 ("Grundlagen - Praktikum", die eigentliche Copilot-Story-Aufgabe mit Bilder-Generierung
und Speichern auf dem Stick in Ordnerstruktur) — Chris hatte sich bei der Foliennummer vertan. Folie 10 wurde
danach korrekt direkt in der PPTX ausformuliert (Backup vorher angelegt).
