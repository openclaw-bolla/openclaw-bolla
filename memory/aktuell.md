# Aktuell — 2026-06-16

## AURORA — Welle A (Blocker-Fixes) LÄUFT (16.06. nachm.)
- Entscheidung Chris: **DE zuerst, dann EN-Sync. Welle B kreativ mit Opus.** Quota grün.
- ✅ **Blocker #2 (Tippfehler): 15 Stück gefixt** in `ki_buch.json` (Script mit Count-Assert). Backup: `ki_buch_backup_wellea_20260616_135930.json`.
- ✅ **Blocker #1 (Timeline): ERLEDIGT.** Chris wählte **Option A** (alles rund um Verlust = 22 J., Tochter starb mit 4 J. 7 Mon., Trennung = Tod ~22 J., Theos Beruf bleibt 30 J., Kennenlernen 30 J.). Opus-Agent erstellte 99 Edit-Liste → 96 angewendet (3 „beruf-korrektur" 20→30 verworfen, Scope-Creep) + 2 Prosa-Umformulierungen (K17 Rechen-Beat „8 J. später"→„im selben Jahr"; K34 Doppelzahl raus). Verifiziert: 0 Reste „einundzwanzig", Sterbealter 4J7M, Noah-Bug K23 (zehn→fünfzehn). Backup: `ki_buch_backup_vor_timeline_*`. Liste: `timeline_edits.json`.
- ⚠️ NEBENBEFUND (separat, später): Theos Berufsdauer ist im Buch mal 20/30/40 J. — eigene kleine Inkonsistenz, NICHT im Timeline-Fix angefasst.
- ✅ **WELLE A KOMPLETT (alle 5 Blocker):** #1 Timeline, #2 Tippfehler(15), #3 POV-Bruch K9 (Inferenz nach vorne), #4 Personenzahl (K26 „sechs Gesichter"→„vier", K29 „Sechs"→„Vier erwachsene Menschen"; Opus-Agent verifizierte Bühnenbesetzung), #5 Nachname Marlie=Braun (Fehlalarm, durchgängig konsistent). Backups: `ki_buch_backup_wellea_*`, `ki_buch_backup_vor_timeline_*`.
- ✅ **DE-EPUB neu gebaut + verifiziert** (`AURORA_deutsch.epub`, 3,1MB). Auch Epilog im Generator-Script gefixt (Theo „zwanzig"→„zweiundzwanzig Jahre", Z.50). EPUB-Check: 0 „einundzwanzig", 0 alte Tippfehler, alle Fixes drin. Vorheriges EPUB gesichert als `AURORA_deutsch_vor_wellea.epub`. **→ DE ist jetzt einreichungsreif.**
- ✅ **WELLE B (Kür) KOMPLETT in DE** (Chris: „alles + Ton passt"). 19 Edits + 3 „Weg"-Quotes angewendet, DE-EPUB neu gebaut + verifiziert:
  - Noah belebt K12/18/24/32/33/34 (Opus, roter Faden „der Macher, der baut statt redet"). Backup `ki_buch_backup_vor_welleb_*`.
  - Humor K41 (Ellie/Leni trockener Galgenhumor), K46 gestrafft (3 Schnitte: doppeltes „vorsichtig", „am Grab"-Wdh., Maschinen-Aufzählung).
  - Notstrom-Logik K11/24/45 erklärt, K40 Sekunden auf „achtzig" vereinheitlicht (6×, 0 Reste) + 100km-Hauptschalter entschärft. Redundanzen K5/20/43.
  - Chris-Wunsch: AURORAs Begriff „das Weg" (K24) in Anführungszeichen „Weg" (auch im AURORA-Dialog).
- ✅ **EN-SYNC KOMPLETT.** 4 Opus-Agenten spiegelten DE→EN auf `ki_buch_en_adapted.json` (Namen Marley/Ellie/Howell/Boston; AURORAs Wort „Gone"). 119 Edits angewendet (en_timeline 97, en_noah 6, en_narrativ 7, en_technik 9) + 2 „Gone"-Quotes im AURORA-Dialog. Backup `ki_buch_en_backup_vor_sync_*`. EN-EPUB `AURORA_english.epub` (3111KB) neu gebaut + verifiziert: 0× „twenty-one years", Sterbealter „four years and seven months", Noah-Bug→fifteen, „Gone"-Quotes drin (escaped), K40 „eighty seconds" 6×, four faces/Four adults.

## AURORA — KOMPLETT FERTIG (16.06.) 🎉
**Beide Ausgaben (DE + EN) verkaufsreif, alle 5 Blocker + komplette Kür (Welle B) erledigt und synchron, beide EPUBs neu gebaut + verifiziert.**
- DE: `AURORA_deutsch.epub`, EN: `AURORA_english.epub` (beide in `/mnt/d/OneDrive/Dokumente/AURORA/`).
- Pre-Edit-Backups: `AURORA_deutsch_vor_wellea.epub`, JSON-Backups `ki_buch_backup_vor_timeline/wellea/welleb_*`, `ki_buch_en_backup_vor_sync_*`.
- Edit-Listen als Doku: `timeline_edits.json`, `welleb_*_edits.json`, `en_*_edits.json` (workspace/data).
- OFFEN/optional für später: Theos Berufsdauer-Inkonsistenz (20/30/40 J.) — eigene kleine Sache, nie kritisch. Welle 3 (Foreshadowing Folgeband) weiter optional.
- ✅ **Beide EPUBs an Kindle gesendet** (16.06. abends) via neues Skript `scripts/kindle_send.py` (Graph Upload-Session, da >4MB-sendMail-Limit; Doku in `reference_kindle.md`). Amazon-Verifikationsmail an ernstmandel@outlook.de → Chris muss klicken (48h).
- Nächster realer Schritt = Publishing (KDP + D2D, €4.99/$4.99 — Plan steht im Memory).

## AURORA — Verkaufsreife-Check + Lektorat ✅ (16.06.)
- **Mechanischer Wort-Check** (zusammengeschriebene Wörter) auf beide Sprachen:
  - DE: 1 Fehler `einGeständnis` (Kap22) → gefixt zu „ein Geständnis", DE-EPUB neu gebaut + verifiziert (0 Fehler, 3× korrekt). Backup: `ki_buch_backup_tippfix_*`.
  - EN: 0 echte Fehler (nur „PhD", korrekt). EN-EPUB unverändert.
- **Inhaltl. Einschätzung** (Basis: AURORA_Spannungslandkarte.md vom 14.06, Sonnet+Opus, + aktueller Status):
  - Status JSON: „Lektorat Welle 1+2 abgeschlossen", `buch_fertig: True`. Ende löst auf (Maria+AURORA), kein Cliffhanger.
  - Spannung stark (kein Hook <8), Twist-Mechanik (AURORA=verlorenes Kind) sauber gepflanzt. Keine Plotlöcher.
  - Die 2 „offenen Köder" aus Bericht (Kap13 „zweite Lüge", Kap32 „Zahl") sind real KEINE Löcher — szenenintern bzw. in Kap33/34 weitergeführt.
  - **Verdict: verkaufsreif.** Welle 3 (Foreshadowing f. Folgeband) optional, kein Blocker.
- **Gegencheck FERTIG** (47 Kapitel + Opus-Synthese, ~984k Tokens). Report: `/mnt/d/OneDrive/Dokumente/AURORA/AURORA_Gegencheck_16-06.md`.
  - **Urteil: VERKAUFSREIF — MIT AUFLAGEN** (nicht „glatt verkaufsreif" wie meine erste Einschätzung!).
  - Welle 1 sitzt (Spannungstäler weg, kein Kap <7 im Hauptkörper). Welle 2 nur halb: **Marlie ja, Noah nein** (noch in ~1/3 der Kap blass).
  - **5 BLOCKER vor Einreichung (offen, mechanisch lösbar):** (a) Timeline-Chaos 20/21/22/12/10 Jahre quer durchs Schlussdrittel, Kap23 im selben Absatz widersprüchlich → Master-Chronologie festlegen. (b) ~15 echte Tippfehler/Grammatik (zurueknehmen, Junihaft, „großgezogen hätte können") — meine Regex fand nur Klebungen, DIESE nicht! (c) POV-Bruch Kap9. (d) Personenzahl Kap26/29 geht nicht auf. (e) Nachname-Kanon Marlie („Braun"?).
  - Neu: Kap41 Humor 2→1 (Sorgenkind), Kap46 Sp5 (schwächstes Kap, Ausklang straffen).
  - **NÄCHSTER SCHRITT:** Die 5 Blocker abarbeiten (am besten gezielter Fix-Durchlauf), dann EPUBs neu bauen.
- **Korrektorat-Tool (LanguageTool):** Chris gefragt — Antwort: lohnt für diesen KI-Text kaum (gratis/lokal, aber dass/das etc. macht KI eh richtig; mechan. Klebungen schon gecheckt). Nicht eingerichtet.

## MC „Failed to fetch" behoben ✅ (Bolla-Kachel, lokal)
- **Ursache:** ZWEI mission_control_api.py-Prozesse lauschten gleichzeitig auf 18790 (SO_REUSEPORT). Race beim Reboot: @reboot-Start + */2-Watchdog feuerten gleichzeitig, Watchdog (`pgrep|head -1`) sah Doppelstart nie. Kernel-Round-Robin → ~50% Requests beim hakeligen Prozess → sporadisch „Failed to fetch".
- **Fix:** SO_REUSEPORT aus `mission_control_api.py` (~Z.7330) entfernt — nur noch SO_REUSEADDR. Zweitstart scheitert jetzt sauber mit „Address already in use". Beide Prozesse gekillt, einen frisch gestartet.
- **Verifiziert:** 1 Prozess (PID 545083), 1 Listener, /api/status 200, Bolla-Chat end-to-end success.
- **Defense-in-Depth ✅:** `mc_watchdog.sh` erweitert — erkennt jetzt Doppelstart: ermittelt echten Port-Inhaber (ss), behält ihn, killt überzählige Prozesse. Fälle: kein Prozess→start, Prozess(e) ohne Listener→kill+restart, mehrere→Listener behalten. Live getestet mit Fake-Doppelgänger: korrekt gekillt, echter Server unversehrt.

---

# Aktuell — 2026-06-15 (Nacht)

## Status: Übersetzungs-Workflow läuft im Hintergrund

### EPUB Deutsch ✅ FERTIG
- `/mnt/d/OneDrive/Dokumente/AURORA/AURORA_deutsch.epub`
- 1,18 MB, MAI-Cover (Atmosph. Hintergrundbild + CSS-Titeloverlay)
- 47 Kapitel + Prolog + Vorspann + Vorwort + Impressum
- Kindle: EPUB an @kindle.com senden oder in Kindle-App importieren (P20)

### AURORA Englisch — Übersetzungs-Workflow (Workflow-ID: wf_a35c2870-694)
- **Läuft gerade:** 48 Kapitel parallel mit Sonnet
- **Cache:** `/home/bolla/workspace/data/ki_buch_en_cache/` (Kapitel für Kapitel)
- **Ausgabe:** `ki_buch_en.json` nach Workflow-Ende
- **Dann:** Englisches EPUB generieren (aurora_epub_en_gen.py — noch zu schreiben)

### Figuren-Anpassungen Englisch (Translation Bible)
- Leni Yilmaz → Ellie Yilmaz
- Marlie Braun → Marley Brown
- Noah Khoury → unverändert
- Vogt → Director Howell
- Hamburg → Boston MA, NovaTech HQ = Boston Seaport
- BND → NSA/CIA je Kontext
- AURORA-Stil: Englisch mit leichter Nicht-Muttersprachler-Eigenheit

### Nächste Schritte (nach Workflow)
- [ ] Englisches EPUB aus ki_buch_en.json generieren
- [ ] Vorspann EN prüfen (Sleeping-Beauty-Motiv, nicht Etymologie)
- [ ] Beide EPUBs an Chris melden

### Sonstiges erledigt heute
- ISBN/Publishing-Planung: KDP + D2D, €4.99 / $4.99 → in Memory gespeichert
- Haiku → Sonnet für Übersetzung korrigiert in Memory
- Git-Commit + OneDrive-Backup ✅
