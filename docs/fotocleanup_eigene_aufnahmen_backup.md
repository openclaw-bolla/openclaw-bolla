# Foto-Aufräum-Auftrag: `Eigene Aufnahmen_Backup` leeren + Screenshot-Sweep

**Erstellt:** 08.09.2026 · **Ausführung:** Samstag 12.09.2026 abends, sobald Chris „**start fotos**" tippt
**Modus:** Hintergrund-Fork (background subagent), läuft autonom durch. Report am Ende.

---

## 0. Start-Gate (VOR dem Spawn prüfen, in der Haupt-Session)

1. `curl -s http://127.0.0.1:18790/api/claudequota` → **`seven_day_rem` muss ≥ 40** sein.
   - Wochenfenster resettet **So 13.09. 00:00** → Samstag abend ist knapp, ernst nehmen.
   - `< 40` → NICHT starten, Chris melden, auf nach dem Reset (So/Mo) verschieben.
2. MC-Server (`http://127.0.0.1:18790/`) muss laufen (für Quota-Checks zwischendurch + ADB-Endpunkte).
3. Duo per ADB erreichbar? (`adb devices`) — wenn nicht, Reconnect versuchen (Port-Scan, s. [[project_handy_foto_zwischenablage]]).
   Kein Duo → Screenshot-Löschung auf dem Gerät überspringen, im Report vermerken, OneDrive-Teil trotzdem machen.
4. Modell: Bulk-Bildanalyse mit **Haiku**, unsichere Personen-/Serien-Fälle zu **Sonnet** eskalieren.

## 1. Backup ZUERST (Pflicht, nichts vorher anfassen)

```
tar -cf /home/bolla/workspace/backups/Eigene_Aufnahmen_Backup_vor_cleanup_20260912.tar \
    -C "/mnt/d/OneDrive/Bilder" "Eigene Aufnahmen_Backup"
```
Zusätzlich vor dem Screenshot-Sweep: Liste **aller** zu löschenden Screenshot-Pfade (OneDrive-weit) in
`workspace/backups/screenshots_geloescht_20260912.txt` schreiben, und `D:\OneDrive\Bilder\Screenshots\`
mit in ein tar sichern (`screenshots_ordner_vor_cleanup_20260912.tar`).
Byte-Summe Quelle prüfen, tar-Inhalt gegenzählen. Erst dann weiter.

---

## JOB 1 — Echte Screenshots löschen

### Was ist ein „echter Screenshot"
- Dateiname matcht `Screenshot[-_]…` (jede App-Endung: `_com.huawei.camera`, `-edit-…`, `.png`, `.jpg`,
  `.png.jpg`-Doppelendung usw.), **oder**
- Seitenverhältnis == exakte Handy-/Desktop-Bildschirmauflösung **und** erkennbare UI-Leiste/Statusbar.
- Kaputte Mini-Dateien (`< 2 KB`, die 195-Byte-Artefakte) im Screenshot-Schwung → als Müll mitlöschen.
- Im Zweifel (könnte ein abfotografierter Bildschirm / ein bewusst behaltenes Beleg-Foto sein) →
  **nicht löschen**, in den Report unter „Screenshots übersprungen (unsicher)".

### Geltungsbereich
- **Ganzer OneDrive-Baum** unter `D:\OneDrive\` …
- … **AUSGENOMMEN** (dort nichts anfassen):
  - `D:\OneDrive\Mandels\**` (Chris archiviert Screenshots dort bewusst)
  - `D:\OneDrive\Mandels\Robin\**` bzw. jeder Pfad der `Robin` als Ordner enthält
    (Robins Daten grundsätzlich nicht ungefragt anfassen, [[feedback_robin_daten_onedrive_schuetzen]])
- `D:\OneDrive\Bilder\Screenshots\` → komplett leeren (reiner Screenshot-Dump).
- `Eigene Aufnahmen_Backup` → alle Screenshots raus (Teil von Job 2 sowieso).
- **NICHT** `D:\OneDrive\Bilder\Eigene Aufnahmen\` (ohne `_Backup`) anfassen — Windows-Systemordner,
  automatischer Handy-Einlauf, tabu ([[feedback_eigene_aufnahmen]]).

### Auf den Handys
- **Duo:** Screenshots per ADB löschen — `/sdcard/DCIM/Screenshots/` und
  `/sdcard/Pictures/Screenshots/` (beide prüfen). Vorher `ls` → Liste in den Report, dann löschen,
  dann Gegen-`ls` (muss leer sein).
- **P20:** hat kein ADB. Liste der P20-Screenshots (aus den OneDrive-Dateinamen ableitbar:
  `…_com.huawei…`) in den Report unter „P20 — bitte selbst am Gerät löschen".

### Native Windows-Löschung
Alle OneDrive-Löschungen per PowerShell (`Remove-Item -LiteralPath`), nicht über den WSL-Mount —
sonst merkt OneDrive/Explorer die Änderung evtl. tagelang nicht ([[reference_wsl_explorer_refresh]]).

---

## JOB 2 — `D:\OneDrive\Bilder\Eigene Aufnahmen_Backup\` restlos auflösen

**Bestand (Stand 08.09.2026):** 714 Dateien / 548 MB. Root: ~280 rohe `IMG_2026*.jpg` (Datum im Namen),
~60 Screenshots, ein paar `PANO_*`, `SVID_*.mp4`, `video_*.mp4`. Unterordner mit von Bolla vergebenen
Beschreibungsnamen: `Robin` (57), `Renate` (11), `Stephanie und Familie` (151), `Natur und Landschaft` (24),
`Reisen und Ausflüge` (27), `Sonstiges` (59, `IMG_YYYYMMDD_WA*`), `Robin BeReal` (15).

### Ablauf pro Datei

**Schritt A — Screenshots** raus (siehe Job 1). Löschen.

**Schritt B — Interne Dubletten entdoppeln** (vor allem anderen):
- `-edit-<timestamp>`-Ketten (z.B. `IMG_20260524_131341` + 3× `…-edit-…`): **beste behalten**
  (größte Auflösung / schärfste / letzte sinnvolle Bearbeitung), Rest löschen.
- Von Bolla umbenannte Beschreibungs-Datei, die inhaltsgleich zu einer rohen `IMG_*` ist:
  eine behalten (die mit besserer Qualität / dem sprechenden Namen), andere löschen.
- Erkennung: exakter MD5 **oder** perceptual-Hash sehr nah (dHash-Distanz ≤ ~10, Positivkontrolle
  wie beim Tansania-Job) **und** Sichtprüfung bei Grenzfällen.
- Jede interne Löschung in den Report.

**Schritt C — Bibliotheks-Dubletten** (gibt's das Foto schon einsortiert?):
- Abgleich **nur** gegen: `Mandels\2025\**`, `Mandels\2026\**`, `Mandels\Robin\22-23 Jahre\**`,
  `Mandels\Robin\23-24 Jahre\**`. (Nicht mehr — Chris' Vorgabe.)
- Methode: MD5 exakt + perceptual-Hash (EXIF-Orientierung + 4 Rotationen, wie Tansania-Job),
  Treffer-Schwelle konservativ, Grenzfälle per Montage sichtprüfen.
- Treffer → Datei aus `_Backup` **löschen**, Report-Zeile: `<_Backup-Datei>  ==  <Fundstelle>`.

**Schritt D — Rest einsortieren.** Für jede verbleibende Datei:

1. **Personen bestimmen (ALLE Personen-Fotos neu prüfen, Bildanalyse):**
   bekannte Gesichter = Chris, Reni (Renate), Robin, Steffi, Anne, Dani (Daniel Garschagen),
   Enkel Emma / Mia / Marie / Anton.
   - Bolla hat früher **oft Chris mit Dani verwechselt** → besonders die `dani_*`-Namen kritisch prüfen.
   - Dateinamen entsprechend korrigieren (`dani_beim_fruehstueck.jpg` → `chris_beim_fruehstueck.jpg` etc.).
   - Person nicht eindeutig → best guess + Report-Eintrag „Personen-Zuordnung unsicher".

2. **Robin oder nicht:**
   - Foto zeigt Robin (allein oder klar Robin-zentriert) → **`Mandels\Robin\<Altersordner>\`**
   - sonst (Familie ohne Robin-Fokus, Reni, Steffi-Familie, Deko, Landschaft) → **`Mandels\<Jahr>\`**
   - Familien-Event mit Robin UND allen anderen → Mandels-Event-Logik, Robin-Anteil im Report notieren.

3. **Datum / Jahr bestimmen:**
   - `IMG_YYYYMMDD_*` / `…_WA*` / `PANO_YYYYMMDD*` → Datum aus dem Namen.
   - EXIF `DateTimeOriginal` wenn vorhanden (nur ~28 der umbenannten haben das).
   - **Sonst (≈316 Dateien): schätzen** aus Bildinhalt/Kontext (Kleidung, Jahreszeit, Anlass, wie alt
     wirken die Enkel, bekannte Events) + `mtime` als **groben** Zusatzhinweis (mtime ist teils
     Sync-Zeit, nicht Aufnahme — nie allein darauf verlassen). **Jede Schätzung** in den Report:
     `datei | geschätztes Jahr | Begründung`.

4. **Altersordner Robin** (Geburtstag 30.09.2002):
   - `22-23 Jahre` = 30.09.2024 – 29.09.2025
   - `23-24 Jahre` = 30.09.2025 – 29.09.2026
   - (Fast alles aus `_Backup` ist 2026 → `23-24 Jahre`.)

5. **Unterordner wählen (wenn vorhanden UND passend):**
   - `Mandels\Robin\23-24 Jahre\`: `Events und Feiern`, `Tansania 08-09`
   - `Mandels\Robin\22-23 Jahre\`: `Medis`, `Adventskalender`, `Waken Turncable Thannhausen`
   - `Mandels\2026\`: u.a. `Anne und Bene bei uns`, `Bei Steffi`, `Essen und Trinken`, `Vitalia Neu`,
     `Lüneburger Heide`, `Kaminholz 2026`, `Gymnasium Harksheide Renis Büro` — nur bei klarer Passung.
   - `Mandels\2025\`: u.a. `Anne und Benne`, `Hagenbeck`, `Holland bei Steffi`, `Plöner Seen`,
     `Weihnachten`, `60er - 70er Feier in Kaufering`.
   - Sonst direkt in den Jahres-/Altersordner (kein neuer loser Ordner nur für 1–2 Bilder).

6. **Reise-/Natur-Fotos** (`Natur und Landschaft`, `Reisen und Ausflüge`, oder als solche erkannt):
   - Passt's zu einer **bestehenden Reise** → dorthin. Kandidaten OneDrive-Root:
     `Damüls 2026`, `Süddeutschland 2026`, `Kreuzfahrt 2025`, `Harz 2024`, `Schladming 2024`,
     `Zillertal 2024`, `West Deutschland Städte 2024`. (Datum + Bildinhalt matchen — z.B. Skifotos
     Winter 2026 → `Damüls 2026`; Bodensee/Ulm-Ausflug → evtl. `Süddeutschland 2026`.)
   - Sonst → `Mandels\<Jahr>\` (bzw. `Robin\<Alter>\` wenn Robin drauf).
   - **Vorher `ls`/`find` auf den Zielordner** — existierenden, plausibel gefüllten Ordner treffen,
     keinen Parallelordner anlegen ([[feedback_pfad_verifizieren_vor_schreiben]],
     [[reference_onedrive_mandels_pfad]] — `Mandels` liegt DIREKT unter OneDrive-Wurzel, NICHT unter `Bilder\`).

7. **Serie > 5 Bilder zu einer Situation** → eigenen Unterordner:
   - „Eine Situation" = **gleicher Kalendertag** + Zeitstempel innerhalb ~3 h + visuell kohärent
     (bei undatierten: visuell + inhaltlich klar ein Ereignis).
   - Ordner im jeweiligen Zielordner (`Mandels\2026\<Name>\` bzw. `Robin\23-24 Jahre\<Name>\`).
   - **Name** = kurze deutsche Inhaltsbeschreibung (Bolla, aus Bildanalyse), z.B.
     `Grillen mit Freunden`, `Robin OP-Praktikum`, `Wanderung Bodensee`.
   - Dateien darin `Name (1).jpg`, `Name (2).jpg` … chronologisch.

8. **Umbenennung generell:** sprechendes deutsches Schema, keine Bolla-Rohnamen mehr.
   Personen-Vornamen korrekt (Chris nie „Dani"). Bei Serien s.o.

9. **Verschieben nativ** (PowerShell `Move-Item -LiteralPath`), nicht über WSL-Mount.

### Zielzustand
- `Eigene Aufnahmen_Backup` und alle seine Unterordner **leer** → Ordner per PowerShell löschen.
- Bleibt wider Erwarten was übrig (nicht zuordenbar, nicht datierbar trotz Schätzung, kaputte Datei):
  in `Eigene Aufnahmen_Backup\_Rest\` sammeln, Ordner NICHT löschen, im Report groß markieren.

---

## 3. Report (am Ende)

Markdown-Datei `workspace/docs/fotocleanup_report_20260912.md`, zusätzlich Kopie nach
`D:\OneDrive\Desktop\` und per **SendUserFile** an Chris (sieht er am Handy). Inhalt:

1. **Screenshots gelöscht** — Tabelle: Pfad | Ort (OneDrive-Ordner / Duo) | Größe. Summe + MB.
2. **Screenshots übersprungen (unsicher)** — Pfad + warum.
3. **P20 — bitte selbst löschen** — Liste.
4. **Interne Dubletten gelöscht** — behalten ↔ gelöscht.
5. **Bibliotheks-Dubletten gelöscht** — `_Backup`-Datei == Fundstelle.
6. **Einsortiert** — Tabelle: alt (Name) → neu (Zielpfad + neuer Name). Gruppiert nach Zielordner.
7. **Personen-Korrekturen** — alt → neu, v.a. Dani→Chris. Separat: „Zuordnung unsicher".
8. **Jahres-Schätzungen** (die ~316) — Datei | Jahr | Begründung. Chris liest gegen.
9. **Neu angelegte Serien-Ordner** — Name | Zielort | Anzahl.
10. **Reise-Zuordnungen** — Datei → Reiseordner, mit Begründung.
11. **`_Rest\`** — was übrig blieb (Ziel: leer).
12. **Ordner gelöscht:** ja/nein + finale Gegenprobe (`find` = 0 Dateien).
13. **Budget:** `seven_day_rem` bei Start / bei Ende.

## 4. Fallen (aus früheren Foto-Jobs)

- Leerzeichen in Pfaden: `find … -print0 | while IFS= read -r -d '' f`.
- Große Dateien über 9p-Mount reißen den 2-Min-Bash-Timeout → Batches, Zwischenstand prüfen,
  lange Läufe (Hashing, Bildanalyse) selbst im Fork als Hintergrund-Job mit until-Loop pollen.
- Nach jedem Kopier-/Löschschritt Gegenprobe (Byte-Summe / leere Kontroll-Suche).
- `adb shell` in `while read`-Schleife → `< /dev/null` anhängen.
- Server-Kill nie `pkill -f` → numerisch über Port-Inhaber.
- `aktuell.md` (Symlink → `projects/-home-bolla/memory/aktuell.md`) laufend fortschreiben, damit ein
  Fork-Absturz nicht den ganzen Fortschritt kostet.

## 5. Entscheidungen (von Chris am 08.09.2026 bestätigt)

| Frage | Antwort |
|---|---|
| Ausführung | **komplett autonom**, tar-Backup vorher, Report hinterher |
| Screenshot-Umfang | ganz OneDrive **außer** `Mandels\**` und `Robin\**`; + `Bilder\Screenshots\`; + Duo |
| Undatierte Fotos (~316) | **Jahr schätzen** (Inhalt + mtime-Hinweis), verschieben, jede Schätzung in den Report |
| Reise-/Naturfotos | passenden bestehenden Reiseordner, sonst `Mandels\<Jahr>` |
| Personen-Check | **alle** Personen-Fotos per Bildanalyse neu prüfen, Namen korrigieren |
| Interne Dubletten | beste Version behalten, Rest löschen (auch edit-Ketten) |
| Bibliotheks-Dupe-Scope | nur `Mandels\2025`, `Mandels\2026`, `Robin\22-23 Jahre`, `Robin\23-24 Jahre` |
| Budget-Gate | Start nur wenn `seven_day_rem` ≥ 40 % |
| Trigger | Chris tippt Samstag abend „**start fotos**" |
