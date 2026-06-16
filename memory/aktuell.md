# Aktuell — 2026-06-16

## AURORA — Verkaufsreife-Check + Lektorat ✅ (16.06.)
- **Mechanischer Wort-Check** (zusammengeschriebene Wörter) auf beide Sprachen:
  - DE: 1 Fehler `einGeständnis` (Kap22) → gefixt zu „ein Geständnis", DE-EPUB neu gebaut + verifiziert (0 Fehler, 3× korrekt). Backup: `ki_buch_backup_tippfix_*`.
  - EN: 0 echte Fehler (nur „PhD", korrekt). EN-EPUB unverändert.
- **Inhaltl. Einschätzung** (Basis: AURORA_Spannungslandkarte.md vom 14.06, Sonnet+Opus, + aktueller Status):
  - Status JSON: „Lektorat Welle 1+2 abgeschlossen", `buch_fertig: True`. Ende löst auf (Maria+AURORA), kein Cliffhanger.
  - Spannung stark (kein Hook <8), Twist-Mechanik (AURORA=verlorenes Kind) sauber gepflanzt. Keine Plotlöcher.
  - Die 2 „offenen Köder" aus Bericht (Kap13 „zweite Lüge", Kap32 „Zahl") sind real KEINE Löcher — szenenintern bzw. in Kap33/34 weitergeführt.
  - **Verdict: verkaufsreif.** Welle 3 (Foreshadowing f. Folgeband) optional, kein Blocker.
- **Gegencheck LÄUFT** (Workflow wf_3462dc13-b5d, gestartet 16.06 ~13:15): 47 frische Kapitel-Leser (Sonnet) + Opus-Synthese. Frische Kapitel-Exporte in `data/aurora_chapters_aktuell/`. Report-Ziel: `/mnt/d/OneDrive/Dokumente/AURORA/AURORA_Gegencheck_16-06.md`. Prüft ob Welle 1+2 gelandet + Verkaufsreife-Urteil. Ergebnis landet als Datei (übersteht /clear).
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
