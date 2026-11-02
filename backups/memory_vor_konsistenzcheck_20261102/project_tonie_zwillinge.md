---
name: project-tonie-zwillinge
description: Tonie-Projekt Weihnachten 2026 (Marie, Anton, Mia) — ABGESCHLOSSEN 01.11.26, MC-Werkstatt jetzt neutrale Vorlage im Archiv; offen nur Übergabe Dez.
metadata:
  type: project
---


> **STAND 01.11.2026 (maßgeblich, alles Folgende ist Historie):** Projekt abgeschlossen, alle 3 Figuren bespielt. MC-Seite „Tonie-Werkstatt" ist neutral (ohne Namen) und nur noch über die **Archiv-Übersicht** erreichbar (nicht mehr in der Sidebar/Familie). Alte Backups/Skripte: `workspace/archiv/tonies_2026_weihnachten/` (inkl. `backups/`). Aktiv bleiben nur `data/tonies.json`, `data/tonie_noten.json`, `scripts/tonie_playback.py`. OneDrive-Ordner `Bolla\Tonies` bewusst UNBERÜHRT (Chris: später aufräumen). ⏰ Übergabe an Daniel/Steffi Anfang Dez. – proaktiv erinnern.

# Tonie-Projekt Zwillinge (Weihnachten 2026)

**Ziel:** Marie und Anton (Zwillinge, geb. 21.02.2025, Kinder von Steffi & Daniel, Kaufering) bekommen zu Weihnachten je eine Toniebox. Chris will beide bis Weihnachten bespielen.

**Inhalt je Kind (je ein eigener Kreativ-Tonie):**
1. ein **Bolla-Song** (Suno/bollawave, individuell fürs Kind)
2. ein **bekanntes Kinderlied**, das Chris und Reni selbst einsingen
3. eine **Geschichte**, die Chris vorliest und die mit Bolla zusammen neu erzeugt wird

**Status 23.10.2026:** Nur definiert und angelegt — NICHT ausführen, bis Chris startet. In moin anzeigen.

**Technik-Fakten (recherchiert 23.10., Ratgeberseiten, nicht offiziell):**
- Nur der **Kreativ-Tonie** ist bespielbar; Standard-Tonies sind fest vom Hersteller belegt. Figur hat RFID-Chip mit ID, Inhalt hängt an der Figur, Box ist nur Player (speichert intern, spielt offline).
- Kreativ-Tonie muss **einmal auf eine online (WLAN) verbundene Box**, um dem Konto zugeordnet zu werden. Danach Upload per App/Browser (meine.tonies.de) ohne Box möglich: MP3/M4A/WAV, bis 90 Min pro Figur. Mikro-Direktaufnahme nur in der App.
- Starterset = Box + Kreativ-Tonie.
- Lieferung direkt nach Kaufering geht, aber Überraschung: jemand dort müsste Figur einmal auf Box stellen + WLAN. **Empfohlener Weg:** zu Chris liefern lassen, einrichten, hochladen, verpacken, mitnehmen; in Kaufering nur WLAN eintragen.

**Offene Entscheidungen:** eine Box je Kind (ja, laut Chris „zwei Boxen") — Kaufering-Lieferweg; welches Kinderlied; Geschichten-Thema; Terminplan rückwärts ab Weihnachten (Bestellung rechtzeitig, Aufnahmen, Suno-Download-Limit beachten [[project_suno_download_limit_planung]]).

**Why:** Chris-Wunsch Weihnachtsgeschenk. **How to apply:** bei moin als offenen Punkt zeigen; Songstil/Regeln aus [[feedback_geburtstagssong_zeitlos]], [[feedback_suno_lyrics_qualitaet]], [[user_familie]] beachten.


## Update 24.10.2026
Chris: Mia kommt dazu — auch fuer sie ein Kreativ-Tonie mit allem (Bolla-Song+Kinderlied+Geschichte). Jetzt 3 Kinder: Marie, Anton, Mia. Weiterhin NICHT gestartet.

## Attribute für Songs/Geschichten (Chris sammelt laufend, 24.10.2026)
Chris wirft mir Attribute zu, die später eingebaut werden (Song-Lyrics + Geschichte). Hier fortschreiben:
- **Anton:** Autos, Elefanten
- **Marie:** Tiere
- **Mia:** (noch nichts)

## Festlegungen 24.10.2026 (Chris)
- Kinderlied: **jedes Kind ein anderes**.
- Geschichte: Chris+Reni lesen selbst vor, **Opa und Oma im Wechsel**. Texte zusätzlich als **Word** (wenn fertig), **Opa/Oma farbig markiert** (Rollen je Absatz/Satz).
- **Mia: nur Kreativ-Tonie** (ohne Box), wir kaufen und lassen zu uns liefern.
- Marie+Anton: je Box + Kreativ-Tonie. 9 Teilprojekte = 3 Kinder × (Song, Lied, Geschichte).
- Umsetzung: eigene MP-Seite „🎁 Tonies" unter Familie (Raster 9 Kacheln, Status, Attribute, Wünsche-Feld+Speichern, Anstups). Board bleibt stillgelegt.

## ✅ MP-Seite gebaut 24.10.2026
MP → Familie → 🎁 Tonies. Daten `workspace/data/tonies.json`, API `/api/tonies` (GET), `/api/tonies/save`, `/api/tonies/nudge` (nutzt board_nudges.json-Queue, Session-Hook zeigt sie). Attribute/Wünsche/Titel dort lesen, wenn Chris „Tonie" sagt. Backups: workspace/backups/*_vor_tonies_20261024.*. TODO: Word-Export Geschichten mit Opa/Oma-Farben, wenn Texte fertig.

## v2 Tonie-Seite 24.10.2026 (nach Chris-Feedback)
Anstups = jetzt „Erzeugen/Verbessern" (Hintergrund-Thread, `claude -p --model sonnet`, Ergebnis direkt auf der Seite). Song: Style+Lyrics getrennt kopierbar (Suno), Verwerfen, Verbessern (Wunsch ersetzt Fassung). Lied: nur 1 Vorschlag (nicht doppelt zu anderen Kindern) + „Nehmen wir". Geschichte: nur Word `D:\OneDrive\Dokumente\Bolla\Tonies\Geschichte_<Name>.docx` (Opa blau/Oma magenta, Aptos 14, überschreibt bei Verbessern, liest Chris' Handkorrekturen aus Word mit ein). Endpunkte /api/tonies/generate|verwerfen|uebernehmen|open. Anton-Testlauf liegt drin (Song, Lied, Geschichte).

## Altersgerecht (24.10.2026)
Marie+Anton (geb. 21.02.2025) ≈ knapp 2 Jahre zu Weihnachten → Geschichte ca. 350–450 Wörter/4 Min, Kleinkind-Sprache. **Mia geb. 22.12.2021 → wird 5**: Geschichte ca. 800–1000 Wörter/7–8 Min, Spannungsbogen, Rätsel. Steht in `_TONIES_ALTER` in mission_control_api.py. Fehler vorher: Mia-Alter "unbekannt" angenommen, obwohl in user_familie.md.

## Kinderlied = Auswahlliste (24.10.2026, Chris-Korrektur)
KI-Vorschlag war erfunden ("Fahr, fahr, fahr mit dem Auto" gibt es nicht). Jetzt: festes Katalog `TONIE_LIEDER` in mission-control/index.html (~34 echte bekannte Lieder, Tags tiere/auto/elefant/klein/gross), passende zuerst, bereits gewählte anderer Kinder ausgeblendet; Button "▶ Anhören" = YouTube-Suche, "✅ Nehmen wir" speichert lied.titel. Kein Claude-Generieren mehr fürs Lied. Backup: workspace/backups/index_vor_tonie_lieder_20261024.html

## Lied-Kachel v3 (24.10.2026, Chris)
Begriffe-Feld + "📌 Erzeugen" (Claude nennt 6 echte bekannte Lieder, Unsicheres wird serverseitig gefiltert), "🗑 Verwerfen", "▶ Reinhören" = 30-Sek-Vorschau direkt auf der Seite via iTunes-Search-API (kein YouTube; Fallback-Link wenn nichts gefunden). Katalog TONIE_LIEDER bleibt darunter. Marie hat Testvorschläge drin.
- Opa Chris trägt Mützen, keine Hüte; keine erfundenen Details über Opa/Oma in Tonie-Texten, im Zweifel fragen (25.10.26).

## Stand Kinderlied-Tools 26.10.2026 abends (Chris will bei „moin“ nochmal ran)
- Lied-Kachel (MP → Familie → 🎁 Tonies) hat jetzt nach „Nehmen wir“: **📄 Liedtext (Word)** (`/api/tonies/liedtext`, Claude aus dem Gedächtnis, nur gemeinfreie Lieder, Ordner Tonies) und **🎹 Playback** (`/api/tonies/playback`).
- **Playback = selbst gerendert, nicht Suno:** Suno kennt Melodien nicht anhand des Titels („Alle meine Entchen“ war nicht erkennbar, Chris 26.10.). `scripts/tonie_playback.py` rendert Spieluhr-Melodie + Harfen-Arpeggio per numpy → MP3, Tempo 120 bpm (84 war zu langsam), Runden = Strophenzahl (Claude gefragt, Fallback 2). Noten NUR für „Alle meine Entchen“ (SONGS-Dict). Klang gefiel Chris.
- Button-Weg Playback → MP3 noch NICHT getestet (nur py_compile + Serverstart). Fehlt: Noten für die 3 gewählten Lieder (Chris hat noch nicht gesagt, welche), Tempo-Feedback, Aufnahme-Setup (Audacity, Studio-Mikro statt Kopfhörer, Lautsprecher leise).
- Chris-Regel: bei allen Datei-Erzeugungen in MP Mouseover mit Zielordner (Tonie-Buttons + Word/PDF-Downloads erledigt; andere Dateiarten evtl. noch offen).

## Tonie-Seite v4 Umbau 27.10.2026 (Chris: Buttons unklar, „Alles neu“ tat nichts)
- Seite neu strukturiert (index.html, Backup workspace/backups/index_vor_tonie_umbau_20261027.html): Erklärbox oben, kein „Speichern“-Knopf mehr (alles autosave, Attribute onchange), „Gesamt anstupsen“ + Allgemein-Wünsche entfernt, Dropdown „Bearbeitungsstand“ ersetzt durch Status-Badge + 2 Häkchen (Audio fertig / Im Tonie). Pro Teil: Erzeugen/Neu erzeugen, Verbessern (nur mit Wunsch), Löschen. Toast-Rückmeldung bei jedem Start.
- Entscheidung: „Alles neu“ erzeugt NUR Song + Geschichte neu; das gewählte Kinderlied bleibt (Auswahl aus echtem Katalog, nicht generierbar). Alte Fassungen bleiben sichtbar (abgedunkelt), bis die neue fertig ist (kein vorheriges Verwerfen mehr).
- Ursache „nichts passiert“ nicht sicher geklärt (Log leer); vermutlich Alt-Version im Browser-Cache/Dialog. Neuer Code gibt immer sichtbares Feedback.

## Playback ohne Suno, Liedtext pro Lied (27.10.2026, Chris-Korrektur)
- **Chris: Suno-Style für Playback ist gestrichen** (Suno-Playbacks waren „Schrott“, schon früher entschieden) → Playback immer selbst gerendert (`scripts/tonie_playback.py`). Suno-Fallback im API-Code entfernt.
- Für Lieder ohne Noten schreibt Sonnet die Melodie einmalig als Noten (C-Dur, Takte werden geprüft) → Cache `data/tonie_noten.json` (Quelle „ungeprüft“), dann Rendering. Chris hört Probe und entscheidet. Hänschen klein getestet (Melodie plausibel, MP3 erzeugt, Klang von Chris noch nicht gehört).
- Pro Lied in jeder Listenzeile: ▶ Reinhören · ✅ Dieses nehmen · 📄 Liedtext (kompletter Text als Word) · 🎹 Playback. API nimmt optional `titel`. Bug behoben: `import re` fehlte in mission_control_api.py (Liedtext/Playback-Dateinamen schlugen fehl).
- Falle: `pkill/pgrep -f mission_control_api` killt die eigene Bash-Shell (Exit 144) → Server stattdessen per ps-PID beenden, Watchdog `mc_watchdog.sh` startet neu.

## Klärung 30.10.2026 (Chris) — Ablauf Haushalt/Übergabe
- Alle 3 Kreativ-Tonies werden in **Norderstedt bespielt** (heute 30.10.: 2 Tonieboxen mit je 1 Kreativ-Tonie per Post; Mia-Einhorn mittags im Shop abgeholt) und zu Weihnachten an Steffi geschickt; Verwaltung danach in Kaufering. Nachträgliche Inhalte unwahrscheinlich.
- Chris hat sich bei Tonies registriert, um Daniels Einladung (Kreativ-Tonie-Mitglied im Haushalt daniel.garschagen@gmail.com) anzunehmen — **irrelevant für uns, ignorieren, nicht verlassen**. Missverständnis: Bolla hatte das als Upload-Abkürzung gedeutet; falsch.
- Einrichtung heute mit Chris' eigenem Konto/Haushalt; Mia-Einhorn einmal auf eine online-Box stellen. Chris versteht Haushalts-Technik nicht → keine Fachbegriffe, einfache Schritte.
- **Offen (vor Weihnachten):** Übergabe an Daniel = Haushalt-Eigentümerschaft übertragen (Daniel in unseren Haushalt einladen → Eigentümer). Ob Inhalt der Kreativ-Tonies dabei erhalten bleibt, UNGEKLÄRT → offizielle Tonies-Hilfe prüfen, ggf. mit Testfigur. Erinnerung Anfang Dezember (offene_punkte p_tonie_uebergabe).

## ✅ Abschluss 01.11.2026
Marie, Anton, Mia sind komplett bespielt (Song → Geschichte → Kinderlied), Upload über my.tonies.com (Kreativ-Tonies → Pfeil-Symbol), Haushalt „meins“, Box „Marie“. Offen nur noch Übergabe an Daniel/Steffi (Dez., offene_punkte p_tonie_uebergabe).
**Aufgeräumt/archiviert:** Daten `workspace/data/archiv/tonies_weihnachten2026_marie_anton_mia.json` + `tonie_noten_20261101.json`; Einmal-Skripte+Logs und OneDrive-Kopie in `workspace/archiv/tonies_2026_weihnachten/`; Backups `workspace/backups/*_vor_tonie_neutral_20261101*`.
**MC-Tonie-Seite neu:** neutrale Werkstatt – ein Kind `neu` (Name, Attribute, optional Alter) → „Alles erzeugen“ → 3 Boxen (Song, Geschichte, Kinderlied); Backend `tonies_save` kennt name/alter, `_tonies_alter()` leitet Sprache/Länge vom Alter ab; Generieren ohne Name wird abgelehnt. Oben aufklappbare Karte „Bedienung Toniebox 2“. Playback-Noten (tonie_noten.json) bleiben für alle Lieder nutzbar.
