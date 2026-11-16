---
name: feedback_moin_offene_aktionen
description: „moin“ = nummerierte, priorisierte Gesamtliste ALLES Ausstehenden (Übergabe, Fälliges, laufende Fälle, Ideen) im Terminal; Chris wählt per Zahl
metadata:
  type: feedback
---
## Ablauf bei „moin“ (neu festgelegt 19.10.2026, ersetzt die alte „nur /jobs“-Variante)
1. `date` (Wochentag/Uhrzeit; WSL-Uhr kann driften) + Schulferien prüfen (Herbstferien SH 12.–25.10.2026; siehe [[feedback_ferien_abgleich_vorschlaege]]). In Ferien keine Kurstag-/Schul-Punkte als fällig nennen.
2. **ENDE von `aktuell.md`** lesen (`tail -60`; Pfad `projects/-home-bolla/memory/aktuell.md`) = Übergabe der letzten Session. Der SessionStart-Hook zeigt nur den veralteten Anfang!
3. Quellen für die Liste: `workspace/data/offene_punkte.json` (kuratierte Gesamtliste, bei jeder Änderung aktuell halten, auch /jobs-Block „Offen“), Übergabe aus aktuell.md, Reminder-Fristen in Memory-Dateien (z.B. Suno Premier→Pro bis 31.10.), `workspace/data/fertig_log.json` (gesehen:false → melden, auf true setzen, [[feedback_word_fertig_button]]).
4. **/jobs NUR als Zusatz** und nur Einträge mit Datum der letzten ~24 h und eindeutigem Zustand. Fehler dort erst gegenprüfen (die Übergabe in aktuell.md erklärt ihn oft, z.B. Neustart hat Job abgebrochen). Nie ungeprüft als „Problem“ melden.
5. Ausgabe im Terminal, **durchgehend nummeriert**, damit Chris mit einer Zahl („3“) anstößt. Nach Priorität sortiert, mit Überschriften:
   - **Zuerst (Übergabe letzte Session)** – was ich selbst sofort weiterführe/erledige (kurz sagen was ich tue)
   - **Fällig / Fristen** (mit Datum)
   - **Laufende Fälle** (Immo/Makler, Rechtsfälle, Geräte …)
   - **Projekte auf Zuruf** (AURORA, Trailer, Song+QR, Cover II …)
   - **Zwischendurch-Ideen** (Goodreads/LovelyBooks, Website+Reni-Rezension …)
   Pro Punkt eine Zeile (Titel + Stichwort/Stand), keine Berichte. Chris entscheidet selbst, ich starte nichts Neues ungefragt.
6. Eigene To-dos für Chris/Reni weiter als `report(..., 'aktion', notify=False)` eintragen ([[feedback_jobstatus_statt_telegram]]).

**Why:** Chris 19.10.2026: „bitte nicht nur job lesen … ich möchte bei moin an alles was aussteht erinnert werden um selbst zu entscheiden … priorisiert und mit Nummern“. Vorfall: Ich meldete einen /jobs-Fehler und einen Kurstag in den Ferien, obwohl die Übergabe das schon erklärte (Studio-Neustart, Encoding fortsetzen). Kein Telegram-Digest (Chris sitzt am Terminal).
**How to apply:** Ergänzt [[feedback_session_vorschlaege]] (die „max 3 Punkte“-Regel ist für moin durch die Vollliste ersetzt) und [[feedback_zahl_verweis_session_start]] (Zahlen-Anstoß).

## Prio-Hinweise (Chris 16.10.2026, weiter gültig)
- Auf Zuruf, nicht von selbst starten: Cover AURORA I/II ([[project_aurora_i_cover_reni_feedback]], [[project_aurora_ii_cover]]), AURORA-II-Song + QR ([[project_aurora_ii_song_qr]]), Trailer ([[project_aurora_ii_trailer_blender]]), Kili-Song.
- Zwischendurch-Ideen gelegentlich nennen, nicht drängen: [[project_aurora_goodreads_lovelybooks]], [[project_website_optimieren_reni_rezension]].
- Chris kann jederzeit „komplett raus“ sagen.

## 🔒 Verlässlichkeit (Chris 21.10.2026): Was Chris für „moin" ansagt, MUSS erscheinen
Vorfall 21.10.: Chris sagte am Vortag „chrismandel.de neu → erscheint bei moin"; Eintrag war korrekt in offene_punkte.json, aber ich antwortete auf „moin" nur mit /jobs + Kurzvorschlägen. Ursachen: (a) SessionStart-Hook nutzte `head -c` auf aktuell.md, die Datei ist aber **neu UNTEN** → veralteter Stand; (b) ich folgte dem Ablauf oben nicht.
**Fix:** Hook zeigt jetzt `tail -c 9000` + die komplette nummerierte offene_punkte.json (Backup workspace/backups/session_start_aktuell_vor_tailfix_20261021.sh).
**How to apply:** Bei „moin" IMMER die volle Liste aus offene_punkte.json (alle Einträge) nennen, nie nur 3 Vorschläge. Wenn Chris „erscheint bei moin" sagt → sofort in offene_punkte.json eintragen UND prüfen, dass er in der Hook-Ausgabe auftaucht.

## 🔒 Hook-Ausgabe vollständig lesen (Chris 21.10.2026, 2. Vorfall)
Claude Code zeigt von langer Hook-Ausgabe nur die ersten ~2 KB inline, der Rest steht in einer Datei („Output too large … saved to"). Ich habe nur den Anfang (alter Montagsstand) gelesen und das als aktuell gemeldet. **Regel:** Steht dort „Output too large", ERST die ganze Datei mit Read lesen, dann antworten. Hook jetzt umgebaut: nummerierte offene_punkte.json steht ZUERST, aktuell.md-Tail nur 3500 Bytes (Backup workspace/backups/session_start_aktuell_vor_reihenfolge_20261021.sh).

## 📑 Kategorien Pflicht (Chris 21.10.2026)
„bitte in zukunft die punkte wieder in kategorien einteilen" — bei moin die Liste IMMER mit Überschriften (Zuerst / Fällig & Fristen / Laufende Fälle / Projekte auf Zuruf / Zwischendurch-Ideen), Nummerierung durchgehend. Vorfall: Am 21.10. kam eine flache 1–12-Liste, obwohl die Kategorien in offene_punkte.json (Feld „[Kategorie / Unterkategorie]") schon standen. Nie wieder flach ausgeben.

## 📚 Montags-Reminder + Prio-Sortierung (Chris 26.10.2026)
- **Montags** steht bei „moin" als ERSTER Punkt (Kategorie „Zuerst"): „itslearning-Mitteilung steht an" — aber NUR wenn in der Woche Kurstage sind. Der SessionStart-Hook (`session_start_aktuell.sh`) prüft das selbst (termine[] in schuljahr2627.json, Ferien sind dort schon ausgenommen) und gibt dann eine Zeile „>>> MONTAGS-ERINNERUNG …" aus. Fehlt die Zeile, nichts erwähnen. Backup: workspace/backups/session_start_aktuell_vor_montag_prio_20261026.sh.
- **Priorisiert:** offene_punkte.json hat Feld `prio` (1 = wichtigste), Hook sortiert danach und zeigt „[prio N | Kategorie / Gruppe]". Beim Eintragen neuer Punkte `prio` mit einsortieren (alle durchnummerieren, Backup in workspace/backups/). Reihenfolge innerhalb der Kategorien beibehalten.
- **Dienstags-Eintrag (Chris 26.10.2026):** Gepostet wird die itslearning-Mitteilung immer **DIENSTAG** der Kurstag-Woche (Kurse Mi/Do), nachmittags (Standard 14:30, spät wegen [[feedback_kein_zusatzunterricht_nachmittag]]). Der Hook gibt dienstags die Zeile „>>> DIENSTAGS-ERINNERUNG …" aus → als ersten moin-Punkt nennen, Post-Status prüfen. Ablauf pro Kurstag: Mo moin-Reminder + Texte/PDF/Screenshot vorbereiten + Freigabe → Di posten (Cron). Backup Hook: workspace/backups/session_start_aktuell_vor_dienstag_20261026.sh.

## 🧭 Gruppierte Hook-Ausgabe (Chris 27.10.2026)
„bei 18 punkten habe ich keinen schnellen überblick" → Hook gibt jetzt Überschriften mit Anzahl (## Zuerst (4) …) und Unterthema in [Klammern], AURORA-II-Punkte zusammenhängend. In der Antwort Überschriften mit Zähler übernehmen, Nummern durchgehend. Backup: workspace/backups/session_start_aktuell_vor_gruppierung_20261027.sh
**Format bestätigt (Chris 27.10.2026):** Pro Kategorie fett mit Emoji + Zähler (z. B. „**📚 Projekte auf Zuruf (7)**"), Unterthemen (AURORA II, Website) als einfache Zeile, Punkte eingerückt, KEINE Leerzeilen zwischen den Punkten, Nummern durchgehend. AURORA II bleibt unter „Projekte auf Zuruf" (keine eigene Kategorie).

## 🔴 Kosten-Angabe bei Tokenfresser-Projekten (Chris 31.10.2026)
Bei „moin" hinter dem Jobhinweis von Token-intensiven Projekten (Welle 7, 510-Seiten-Straffung, Trailer/Blender, Massenläufe) in Klammern die geschätzten Prozente für **5h und Woche**, wenn möglich rot: `🔴 (5h ca. X %, Woche ca. Y %)`. Terminal kann kein echtes Rot → 🔴 + ANSI `\033[31m` nur falls es rendert. Schätzwerte stehen im Feld `kosten` in offene_punkte.json (Hook-Ausgabe prüfen, ggf. Hook um `kosten` ergänzen); bei neuen Tokenfresser-Punkten selbst schätzen und eintragen.
**Welle 7 (Chris 31.10.2026):** NICHT automatisch nach dem Wochenreset (Sa 23:00) starten, auch nicht per Cron — nur auf Zuruf, frühestens nächste Woche. Heute Abend läuft nur der read-only Job ausreizen_sa31.py (20:00–22:55).
