---
name: project-aurora-ii-endspurt-plan
description: AURORA II Endspurt-Plan (ab 08.11.2026) – To-dos mit Wochenlimit-% (Pp), Freitags-Freigaben, Vorziehen, Veröffentlichung DE/EN
metadata:
  type: project
---

Chris 08.11.2026: Er liest/korrigiert Kap. 1–38 voraussichtlich in **2 Wochen (bis ca. 22.11.)**. Ich lege **jeden Freitag** (13.11., 20.11., 27.11.) einen priorisierten Freigabe-Vorschlag mit Pp-Kosten (Prozentpunkte Wochenlimit) vor; Läufe dann Fr 19:00 → Sa 22:55 ([[feedback_limit_regeln]]). Wenn wenig ansteht, Punkte **vor das Lese-Ende vorziehen**. Ziel: möglichst frühe Veröffentlichung ohne Qualitätsverlust. Zweiten Spannungslauf entscheide ich.

**Kostenbasis (gemessen):** Opus-Kapitel-Neufassung ≈ 1,8 Pp; Straffung 18 Kap. + 3 Konsistenzblöcke ≈ 22 Pp; Spannungsjob komplett ≈ 30–32 Pp; Tonie-Teile ≈ 1 % für 7. Alles übrige = Schätzung (siehe unten, bei erstem Lauf nachmessen und hier korrigieren).

**Entscheidung 2. Spannungsjob:** KEIN Voll-Lauf. Nach Chris' Lesen nur gezielter Pass (~8–12 Pp) auf Kapitel 25–38, wo er Schwächen markiert/bemängelt (Kap. 1–24 nur Saat). Voll-Lauf (~30 Pp) nur, wenn Chris ausdrücklich Spannung zu schwach findet.

**Pp-Schätzungen:** Prüfpunkt+Einbau 1–2 (läuft automatisch, [[project_aurora_ii]]) · Satz-Fragen beim Lesen 5–10 (sehr grob) · Analogie-Check Kap. 25–38 14–20 · Kürzungen 25–38 12–15 (Ziel ~510 S., Stand ~525 S.) · Fehlerjagd Vollbuch 20–40 · Probesatz 11 pt/Cover-Rücken/Klappentext ~0–1 · DE-Veröffentlichung (KDP-Reihe, EPUB/Print, KDP, D2D, Google Play) 1–3 · Song/QR/Landingpage/Website 1–2 · EN: Haiku-Übersetzung ~5 + Anpassung ~20 (unsicher, mit Kap. 1 messen) · Hörbuch: ElevenLabs-Credits, ~0 bei Claude.

**Zeitplan-Entwurf:**
- Mo–Fr 09.–13.11. (Alltagsreserve, nur kleines): EN-Vorbereitung (Namensliste, Kulturcheckliste, Haiku-Workflow, Test Kap. 1 = Messung, 1–2 Pp), Klappentext-Entwurf, Song-Einreichung DistroKid (Vorlauf 1–2 Wo.), KDP-Reihe anlegen, Bauskripte für II prüfen.
- Fr 13.11. 19:00 (Freigabe 1, ~18–20 Pp): Analogie-Check für bis dahin gelesene Kapitel; EN-Übersetzung der stabilen Kap. 1–18 (Saat-Einschübe später nachziehen, ~265 W); read-only Kürzungskandidaten Kap. 25–38.
- Fr 20.11. (Freigabe 2, ~30–40 Pp): Analogie-Check Rest; Kürzungen 25–38; gezielter Spannungspass; EN Kap. 19–38 sobald Text stabil.
- Fr 27.11. (Freigabe 3, ~30–45 Pp): Fehlerjagd Vollbuch (Sonnet-Erstlauf, Opus nur bei Treffern); danach Probesatz 11 pt → echte Seitenzahl → Cover-Rücken (build_cover.py, NICHT aurora_cover_wrap.py) → QR ins Cover.
- Anfang Dez.: DE-Upload (KDP-Freigabe ~72 h; Paperback-Weihnachtslieferung braucht Veröffentlichung bis ~15.12.), EN danach/zeitgleich je nach Stand. Alles Schätzung.

**Prozess-Optimierung:** Mo–Fr max. Woche 60 % (Alltagsreserve); große Läufe Fr 19:00–Sa 22:55 (Sa ab 22:00 Gate 82/Max 95); Sonnet für mechanische Erst-/Prüfläufe, Opus nur für Prosa; Analogie-Checks wöchentlich gebündelt über die in der Woche gelesenen Kapitel; Skripte (Probesatz, EPUB, Cover) kosten kein Limit. Chris' Markierungen nie überschreiben, Backups vor jeder Übernahme.

## 🆕 Fable-Lektorat (Chris 10.11.2026) — Fable 5.2 im Plan bis 16.11.
Plan (siehe unten: Fable-Eigenlimit → früher starten): Stufe 1 Gesamtgutachten (read-only, Fable liest ganzes Buch) → Chris+Bolla entscheiden danach Umfang; Stufe 2 Kapitel-Politur als **blaue Einschübe** im Duo-Reader (nie Direkt-Überschreiben, Backup vorher), ggf. **ganzes Buch Kap. 1–38**; Stufe 3 Schachtelsätze entzerren (optional). Start Sa 14.11. (nicht Fr 19:00): tagsüber nur Luft für Kleinprojekte (5h <80 %), letztes 5h-Fenster ~18:00–23:00 maximal mit Fable (bis 22:00 Gate 67/Max 80, danach 82/95); Fortsetzung So/Mo 15./16.11. erlaubt, solange für Mo–Fr genug Wochenluft bleibt. Fr 13.11.: Fable-Test (1 Kapitel, Pp messen, Modell `claude-fable-5-2`). Woche bis Sa unter ~50–55 % halten. Ab 17.11. Fable wieder raus ([[feedback_modell_auswahl]]).

### Humor als Hauptziel der Fable-Politur (Chris 10.11.2026)
Chris: viele Humorsequenzen funktionieren (echtes Schmunzeln), aber **sehr viele Szenen sind humorschwach** → er will **deutlich mehr schmunzeln dürfen**. Humor ist damit gleichrangig mit Spannung, nicht Nebenpunkt. Vorgehen: Stufe 1 enthält eine **Humor-Kartierung** (starke Szenen = Vorbild/Maßstab, schwache Szenen = Kandidaten, Humor-Dichte pro Kapitel); Stufe 2 liefert für schwache Szenen **konkrete Humor-Einschübe als blaue Vorschläge** (Situationskomik, trockene Beobachtung, Figuren-Running-Gags, Wortwitz), im Stil der starken Szenen und des Standards aus [[feedback_aurora_ii_humor_standard]] (Kap. 10). Nicht aufgesetzt, nicht albern; Handlung/Ton in ernsten Szenen bleibt. Kein Gag ohne Figurenbezug.

### Beschlossen 10.11.2026 (Chris: „dann planen wir so")
Maßstab Humor = Kap. 10 + Kriterium `aurora2.json → kriterien.humor` (kein weiteres Chris-Lieblingskapitel bekannt; bei neuem Hinweis als 2. Maßstab ablegen). To-do Mi–Fr: Orchestrator `scripts/samstag_fable_lektorat.py` bauen (Gate/Watchdog via limit_policy, Backup, Manifest je Kapitel, Output als blaue Einschübe → Route /api/aurora2/einschub-entscheidung), Fr 13.11. Fable-Test 1 Kapitel (Pp messen), Sa ~17:45 Start Stufe 1 → Entscheidung Umfang → Stufe 2.

### 🆕 Fable hat EIGENES Wochenlimit (Chris 10.11.2026, Screenshot Nutzungslimits)
Claude-Einstellungen zeigen getrennt: „Alle Modelle" (45 % am 10.11.) und **„Fable" (0 % verwendet), beide Zurücksetzung Sa 23:00**. Chris: Fable wird wohl So/Mo (15./16.11.) nicht mehr nutzbar → **Fable-Wochenlimit muss bis Sa 14.11. 23:00 mit AURORA-Fable-Lektorat ausgereizt werden** („wer weiß, ob ich das nochmal bekomme").
**Konsequenz für den Plan:** Fable-Lektorat nicht erst Sa 17:45, sondern so früh starten, dass der Fable-Balken bis Sa 23:00 voll wird (Start Sa morgens/vormittags; 5h-Gate/Obergrenze weiter nach [[feedback_limit_regeln]]). Fable-Balken ≠ Alle-Modelle-Balken: im Orchestrator beide beobachten, Fable-Ziel ≥ ~95 % bei Reset. Nach Sa 23:00 neuer Fable-Wochenbalken (0 %) → So/Mo weiter nutzen, falls Fable noch verfügbar. Quota-Endpunkt `/api/claudequota` liefert bisher nur 5h + Woche gesamt — Fable-Balken muss (falls API-Feld vorhanden) ergänzt oder von Chris abgelesen werden (nicht geprüft).

### 🎁 „Fable-Zurücksetzung" (Chris-Screenshot 10.11.2026, Einstellungen → Nutzungslimits)
Button **„Kostenlos zurücksetzen"**, **Ablauf 17.11.2026 08:59 MEZ**: füllt 5h-Limit + Fable-Kontingent wieder auf UND gibt dem Wochenlimit zurück, was Fable davon verbraucht hat (Wochenlimit sonst nicht komplett zurückgesetzt). Nur Chris kann klicken. Ob einmalig: nicht geprüft (vermutlich ja). **Strategie:** erst Fable-Balken leerfahren (Fable-Lektorat), dann Reset klicken lassen → zweite volle Fable-Runde, Wochenlimit-Kosten des Fable-Laufs werden erstattet. Bestes Timing: nach Leerfahren des Balkens, spätestens So/Mo 16.11. (Sa 23:00 wechselt der Fable-Balken ohnehin auf 0 %, also Reset lieber NACH dem Wochenwechsel einsetzen, wenn Chris So/Mo Zeit hat; sonst Sa tagsüber leerfahren → Reset → nochmal leerfahren bis 23:00).


### 📌 Pflicht-Aufträge für alle Läufe (Chris 11.11.2026)
Datei `workspace/scratch/aurora2_lektorat_auftraege.md` (Zwei Papiere Kap. 9–11; Kreft = Räumer aus Band I, Kap. 14/16 angleichen). Orchestrator `samstag_fable_lektorat.py` muss sie in die Prompts der betroffenen Kapitel und ins Stufe-1-Gutachten einbinden; Sichtung Sa gezielt Kap. 9–11, 14, 16. Siehe [[feedback_aurora_ii_zwei_papiere_benennung]].

## 🔁 Neuplanung 14.11.2026 (nach verbranntem Fable-Lauf)
**Was passiert ist:** Cron 07:45 → test_kap13 (+14 Pp 5h, +2 Pp Woche) → stufe1 = EIN Riesenaufruf über das ganze Buch: 5h 17→91 %, Woche 78→92 %, vom 80-%-Watchdog abgebrochen, KEIN gutachten.md. Job von Bolla gestoppt (Chris: ja). Chris: „>20 % Wochenlimit verbrannt for nothing – soll nie wieder passieren.“
**Gemessene Fakten (Anthropic /api/oauth/usage, 14.11. 10:00):** Fable hat eigenen Balken `weekly_scoped` (30 % belegt = 15 Pp der Woche; Fable-Allowance = **50 % der Woche**). Reset-Angebote (Chris sah in Abrechnung: „Limit zurücksetzen vollständig bis 10.12.“, „Fable bis 17.11.“) stehen NICHT in der API (alle Offer-Felder null) → Wortlaut nur von Chris.
**Kostenmodell Fable:** ~14 Pp 5h und ~2 Pp Woche je Kapitel-Schritt. 5h ist Engpass → max. 4–5 Kapitel pro 5h-Fenster (Gate 67/Max 80 tags, 75/85 nachts).
**Neue Regeln (verbindlich für alle AURORA-II-Läufe):**
1. Nie ein Aufruf über mehr als ~4 Kapitel; jedes Häppchen schreibt Ergebnis SOFORT in eigene Datei (Checkpoint) – Abbruch kostet max. ein Häppchen.
2. Vorab-Budgetprüfung: nur starten, wenn 5h-Stand + geschätzte Kosten ≤ Obergrenze. Nach Abbruch NIE denselben Aufruf wiederholen, sondern Häppchen halbieren.
3. Fable-Balken (weekly_scoped) mitlesen; Fable-Deckel 45 % des Fable-Anteils; bei Überschreitung stoppen.
4. Erst Dry-Run/Kostenschätzung, erst nach Chris-Freigabe Echtlauf. Kein Cron, der selbstständig Fable startet.
**Zeitfenster Fable:** Sa 14.11. 23:00 (Wochen- und Fable-Reset) bis Di 17.11. 08:59. Danach Fable raus ([[feedback_modell_auswahl]]).
**Budget:** Fable-Anteil max. ~40 Pp Woche = Gutachten+Humorkarte (~12–15 Pp, in Häppchen) + Politur der ~12 humorstärksten Kapitel (~24 Pp). Nicht ganzes Buch Kap. 1–38 (wären ~76 Pp > 50-%-Deckel).
**Reset-Knöpfe (nur Chris klickt):** „vollständig bis 12.12.“ = wohl einmalige volle Wochen+5h-Rückstellung → bester Einsatz, wenn Woche ~90 % leer UND große Arbeit offen (z. B. Fr 27.11. Fehlerjagd), NICHT direkt nach Wochenreset. „Fable bis 17.11.“ (Ablauf 17.11. 08:59) → erst Fable-Balken leerfahren, dann klicken, zweite Fable-Runde bis 17.11. (nicht geprüft, ob einmalig/Pp-Erstattung wie in Screenshot 10.11.).
**Screenshot 14.11.2026 (Chris, Einstellungen → Nutzung):** „Limit wird zurückgesetzt – 2 verfügbar“: (1) **Vollständige Zurücksetzung**, Ablauf **12.12. 23:00 MEZ**; (2) **Fable-Zurücksetzung**, Ablauf **17.11. 08:59 MEZ** – füllt 5h + Fable-Kontingent und erstattet, was Fable vom Wochenlimit verbrauchte (Woche sonst nicht komplett). Beide einmalig, nur Chris klickt (kein Zugriff für Bolla, kein Chrome-Tool in der Session).
**Entscheidung/Empfehlung 14.11.:** Vollständige NICHT jetzt (5h resettet 14:10 ohnehin, Woche in 13 h; Woche ist nie der Engpass → Wert ≈ 0). Aufheben für Mitte der Woche, wenn Woche ~90 % und große Arbeit ansteht; spätestens bis 12.12. Fable-Reset: erst Fable-Balken leerfahren (So/Mo), dann klicken, spätestens Di 17.11. 08:00.
**Umbau fertig 14.11.2026 ~10:10 (nichts gestartet):** `scripts/samstag_fable_lektorat.py` v2 (Backup backups/samstag_fable_lektorat_vor_umbau_20261114.py): Häppchen ≤4 Kap., Kapitel-Checkpoints scratch/fable_lektorat/stufe1/, lernende Kostenschätzung (state.json), Vorab-Budgetprüfung mit Selbst-Warten, Fable-Balken-Stopp 88 % + Reset-Hinweis, `--dry-run`, `--auto [--jetzt]` (Start ab Sa 23:03, Ende Di 17.11. 08:30), `--merge` (ohne Fable), Top-12-Humor→Stufe 2. Neuer Wächter `scripts/reset_hinweis_watcher.py` (Cron */15, Meldung in MC-Jobs): Fable-Reset bei Balken ≥85 % + Erinnerung Mo 18:00/Di 06:30; Voll-Reset bei Woche ≥90 % mit ≥36 h bis Reset + Erinnerung 8./10.12. Alter Cron fable-lektorat-sa-start entfernt (Crontab-Backup backups/crontab_vor_reset_hinweis_20261114.txt). Dry-Run: Stufe 1 ≈ 456 Pp 5h (UNGEMESSENE Startschätzung 12 Pp/Kap) ≈ 8 Fenster. Fable-Start per Cron/`--auto` noch NICHT freigegeben → Chris fragen.

**Messung 14.11. 18:05 (Kap. 1–5):** Kap.1: 5h +9, Woche ~0; Kap. 2–5 (4 Kap.): 5h +24 (=6/Kap), Woche +2 (0,5/Kap), Fable-Balken +4 (1/Kap). Hochrechnung Stufe 1 gesamt ≈ 38 % Fable-Balken, ~19 Pp Woche. Reset-Knopf für Stufe 1+2 NICHT nötig → Reserve für erweiterte Stufe 2. Bugfix: geplanter Stopp (Wochenlimit) zählt nicht mehr als Abbruch.

### 🆕 16.11.2026 Chris-Verdacht: Ende zu vorhersehbar / keine echte Überraschung (auch nicht für ihn als Co-Autor)
**Erweiterung (Chris 16.11. später):** Umbau der Handlung erlaubt, frühere Kapitel dürfen komplett neu gefasst werden; Fable = Plot-Architektur (Twist + Setup-Liste), Umsetzung mit Opus; Fable-Verbrauch für Plot-Lauf noch UNGEMESSEN → erst kleiner Messlauf.
Gutachten Stufe 1 bewertet pro Kapitel (Spannung Kap. 30–38: 5,5,4,5,4,5,4,3 /5), aber NICHT die Überraschungsstärke des Schlussakts. Vorschlag an Chris: Fable-Plot-Analyse (Setup-Inventar aus Gutachten/Stufe-1-JSONs + Volltext Kap. 28–38 → Vorhersehbarkeits-Check, 2–3 echte Twist-Optionen mit Plant-&-Payoff-Skizzen, KEIN Umschreiben). Umsetzung danach ohne Fable (Opus/Sonnet). Fable-Reset-Klick Chris ~19:00 (ab 20:00 Reni). Nichts gestartet, wartet auf Chris-Freigabe.
