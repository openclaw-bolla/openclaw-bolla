---
name: feature-aufpeppen
description: Bild/Video „aufpeppen" für Social-Media-Posts im Feel-Good-Profil — Engine + Wächter + (geplant) mmp-Reiter
metadata:
  node_type: memory
  type: project
  originSessionId: current
  modified: 2026-09-07T11:58:43.207Z
---

**Chris-Wunsch (02.07.2026):** Analog zum `caption:`-Trick will Chris mir Bild/Video übergeben können, und ich „peppe es auf" im Sinne seines Feel-Good-Profils (sonnig, optimistisch, verspielt) für Insta/TikTok. Kostenlos (PIL + ffmpeg), kein API-€.

## Engine — `scripts/aufpeppen.py`
`python3 aufpeppen.py <datei> [--platform insta|tiktok] [--style auto|natural|vivid|spectacular] [--text "Hook"] [--music song.mp3] [--out ...]`
- **Bild** → Feel-Good-Grading (Wärme, Sättigung, Kontrast, Glow/Bloom, Vignette, Unsharp), Format insta=1080×1350 (4:5), sonst 1:1; optional Text-Overlay (gelb, schwarzer Rand, unten). Bild als `--platform tiktok` → 6s-Ken-Burns-Hochformat-Video.
- **Video** → Hochformat 1080×1920 (Blur-Fill), sonniges eq+colorbalance-Grading, optional Musikbett (`--music`) + showwaves-Wellen, optional Hook-Text.
- Presets natural/vivid/spectacular; `auto`=vivid. Gibt `RESULT:<pfad>` aus.

## Weg 1 — Eingangsordner-Wächter (LÄUFT seit 02.07., kein Neustart)
`scripts/aufpeppen_watcher.py`, Cron `* * * * *`. Chris legt Datei in `D:\OneDrive\Dokumente\Bolla\Aufpeppen_Eingang\` (Handy: OneDrive-App teilen). Wächter peppt auf → Ergebnis auf Desktop `Aufgepeppt\` + ins mmp (Clipboard-URL + grüner „Auf Handy speichern"). Original → `_verarbeitet\`. Optional gleichnamige `.txt` daneben: erste Zeile Optionen (`tiktok`/`insta`/`spectacular`/`natural`/`vivid`/`song`), Rest = Overlay-Text. State `config/aufpeppen_watcher_state.json`.

## Weg 2 — mmp-Reiter „✨ Aufpeppen" (FERTIG + LIVE seit 02.07.2026)
Reiter in `mobile.html` (`data-tab="pep"`, Seite `#p-pep`, TITLES.pep) + Backend `POST /api/aufpeppen` in `mission_control_api.py` (Datei als **base64 im JSON-Body**: file_b64/filename/platform/style/text/music; kein multipart). Chris wählt im mmp Bild/Video, Plattform (insta/tiktok), Pepp-Stärke, optional Text + Musikbett → Ergebnis direkt im Reiter mit grünem „Auf Handy speichern". Endpoint end-to-end getestet ✓.

**⚠️ MC-Neustart-Befehl (sauber detached, überlebt Session-Ende):**
`cd ~/workspace && kill <altpid>; setsid bash -c 'exec python3 scripts/mission_control_api.py >> logs/mission_control_api.log 2>&1' < /dev/null & disown` — danach `ps -o sid` prüfen: PID==SID = eigener Session-Leader = detached. (`run_in_background`/simples `nohup &` hängt sonst unter der claude-Session → MC stirbt bei Session-Ende.) Siehe [[feedback_mc_kein_restart_html]].

## ⭐ Fable-Regisseur + Multi-Foto-Reel (10.07.2026, auf Chris-Feedback „Vorschau-Ergebnisse waren langweilig")
**Ursache gefunden:** `image_to_video()` (Bild→TikTok) hat den `--text`-Parameter nie genutzt — Hook-Text kam bei Foto-zu-Video NIE an, egal was Chris eingab. Gefixt.
- **`--ai`-Flag in `aufpeppen.py`:** Fable (`claude-fable-5` via `claude -p`, nutzt eigenes Read-Tool fürs Bild) schaut sich das Bild/den Video-Frame an und schreibt einen content-bezogenen Hook-Text (statt generisch) + wählt automatisch `natural/vivid/spectacular` nach Bildstimmung. Greift automatisch, wenn Chris **keinen** Text vorgibt (Watcher UND mmp-Reiter `/api/aufpeppen` — MC-Neustart dafür schon gemacht). Funktion `ai_direct()`.
- **Emoji-Fix:** ffmpeg-Drawtext und PIL-Font können keine Emoji rendern (Kästchen/„Tofu"). Neue Hilfsfunktion `for_drawtext()` entfernt Emoji + macht sauberen Zeilenumbruch (vorher: Text lief über den Rand oder wurde abgeschnitten).
- **NEU: `scripts/aufpeppen_montage.py`** — wenn Chris **mehrere** Fotos/Videos auf einmal einkippt (gleicher Wächter-Durchlauf), baut der Wächter zusätzlich zu den Einzel-Ergebnissen automatisch EIN kombiniertes Reel: Crossfade-Übergänge (0,5s), 3s pro Clip, Musikbett (neuester bollawave-Song falls keiner angegeben), Fable-Hook nur in den ersten 3s eingeblendet. Bis zu 8 Clips. Eigenständig aufrufbar: `python3 aufpeppen_montage.py <datei1> <datei2> ... --out <ziel.mp4>`.
- Getestet End-to-End (Einzelbild mit `--ai`, Video-Text-Overlay, 4-Foto-Montage, kompletter Wächter-Trockenlauf mit simuliertem Clipboard-Post) — alles funktioniert. Kein Server-Neustart nötig für den Watcher (Cron startet jede Minute neu), nur für den mmp-API-Teil in `mission_control_api.py` (bereits erledigt).
- **Noch offen:** Eingangsordner war beim Test leer (keine frischen Handy-Fotos seit ~08/2025) — die neue Technik wartet auf echten Content von Chris, noch nicht an echtem TikTok-Post verifiziert.

## 🔧 Großer Bugfix-Batch (19.07.2026, auf Chris-Feedback „funktioniert absolut nicht so wie ich mir das vorstelle")
Chris testete den mmp-Reiter zum ersten Mal wirklich und fand 6 konkrete Probleme — alle verifiziert und behoben:
1. **Mehrfachauswahl fehlte im mmp-Tab.** Die Multi-Foto-Reel-Funktion gab es bisher NUR beim OneDrive-Ordner-Wächter, nicht im mmp-UI selbst. Fix: `pep-file`-Input hat jetzt `multiple`; wählt Chris 2+ Fotos, geht's an den neuen Endpoint `/api/aufpeppen-multi` (ruft `aufpeppen_montage.py` mit den dekodierten Dateien auf), 1 Datei läuft weiter über `/api/aufpeppen` wie bisher.
2. **Effekte zu langweilig ("nicht mit CapCut konkurrieren, sondern besser").** Nur Farb-Grading + statischer Text war zu wenig. Fix: `chain_xfade()` in `aufpeppen_montage.py` variiert jetzt Übergänge (zoomin/circleopen/wipeleft/slideup/smoothleft/wiperight, kürzer 0,35s statt 0,5s) statt immer nur "fade" — fühlt sich nach echtem Edit an, nicht nach Diashow. Text hat jetzt Pop-in-Fade (`drawtext_clause()`, alpha-Animation) statt stumpf-statisch.
3. **Querformat → Hochformat zeigte Blur-Rand mit kleinem Bild in der Mitte** statt vollflächigem Zuschnitt. Bug in `image_to_video()` (aufpeppen.py) und `make_segment()` (aufpeppen_montage.py): Beide bauten einen verschwommenen Pillarbox-Hintergrund + kleines zentriertes Zoompan-Bild. Fix: erst `scale+crop=1080:1920` (voller Screen, wie TikTok/Reels), DANN Ken-Burns-Zoompan reinzoomen — kein Rand mehr, egal ob Quer- oder Hochformat-Quelle.
4. **Fertige Datei landete beim mmp-Weg NUR im Browser-Ergebnis**, nicht auf dem Desktop (im Gegensatz zum Ordner-Wächter-Weg). Fix: `/api/aufpeppen` UND `/api/aufpeppen-multi` kopieren das Ergebnis jetzt zusätzlich nach `DESKTOP_AUFGEPEPPT_DIR` = `/mnt/d/OneDrive/Desktop/Aufgepeppt/` (mission_control_api.py) — Ergebnis liegt jetzt IMMER an EINEM Ort, egal welcher Weg.
5. **Kein Reset/"Neues Projekt"-Knopf.** Neuer Button „🔄 Neu" in `p-pep` (mobile.html) — leert Dateiauswahl, Vorschau, Text, Ergebnis.
6. **Fable-Hook wurde mitten im Satz abgeschnitten + langweilige Schriftart bei Videos.** Zwei Bugs in `for_drawtext()`: (a) hartes `max_lines=2`/`max_chars=24`-Limit verschluckte Wörter kommentarlos statt umzubrechen/zu kürzen — jetzt `max_chars=30`/`max_lines=3` + „…"-Fallback bei echtem Überlauf. (b) ffmpeg-`drawtext` hatte GAR KEIN `fontfile` gesetzt → ffmpeg-Systemstandard (die "langweilige" Schrift). Neue zentrale Funktion `caption_font_path()`/`drawtext_clause()` nutzt jetzt **Impact** (`/mnt/c/Windows/Fonts/impact.ttf`, klassische Meme/TikTok-Caption-Schrift) für Video-Text UND Bild-Text (`draw_text()` hatte zudem einen Tippfehler `" ariblk.ttf"` mit führendem Leerzeichen, der Arial Black nie laden ließ — behoben). Text ist jetzt zusätzlich GROSSSCHRIFT (Caption-Look).

Alle Fixes End-to-End mit synthetischen Testbildern verifiziert (Einzelbild→TikTok-Video, 3-Foto-Reel via `/api/aufpeppen-multi`, Desktop-Kopie bestätigt, Font-Rendering per Frame-Extraktion visuell geprüft). MC-Neustart durchgeführt (mission_control_api.py geändert). Testdateien von Chris' echtem Desktop wieder entfernt.
**Noch nicht verifiziert:** echter Content von Chris (nur synthetische Testbilder) — beim nächsten echten Foto/Reel beobachten, ob die neuen Effekte/Font/Crop wirklich überzeugen.

## 🎬 CapCut-Level-Umbau (24.08.2026, auf Chris-Feedback „sehr weit weg von meiner Vorstellung")

Trotz des Juli-Bugfix-Batches war der **Einzelfoto→TikTok-Pfad** (Chris' meistgenutzter — "meist wird es
aber ein Foto sein") noch bei einem einzigen trägen 6s-Ken-Burns-Zoom hängengeblieben; die
Transitions/Effekte vom Juli galten nur für die Multi-Foto-Montage. Chris wollte echtes
CapCut/Clipchamp-Niveau: spektakuläre Effekte, echte Schnitte, witziger content-bezogener Spruch.
Umbau als Fork (Sonnet — Opus-Versuch scheiterte mit `403 Unable to verify organization membership`,
Verdacht: nicht mehr im Pro-Plan enthalten seit Max→Pro-Wechsel 19.07., noch ungeklärt).

**Neu in `aufpeppen.py`/`aufpeppen_montage.py`:**
- **Multi-Shot aus EINEM Foto** (`image_to_video()`): 3 Kamera-Einstellungen (Totale/Zwischenschnitt/
  Detail-Punch-in) aus verschiedenen Crop-Fenstern desselben Bildes, verbunden mit Flash-Cut-Übergängen
  (xfade, wiederverwendet aus der Montage-Logik — jetzt geteilter Code statt Duplikat)
- **Speed-Ramp:** schneller Punch-Zoom am Start (1.0→1.15 in ~0.3-0.4s), Rest gemächlicher Ken-Burns
- **Neue Effektbausteine** (parametrisiert, je nach Preset unterschiedlich stark): Licht-Leak-Overlay,
  Film-Grain, Kamera-Wackeln, Weißblitz bei Schnitten
- **3 neue Presets:** cinematic (Teal-Orange), golden (Golden-Hour), punch (High-Energy-Hochkontrast) —
  zusätzlich zu natural/vivid/spectacular
- **2-Beat-Captions:** Setup+Pointe (statt ein Dauertext), Pop-in/Bounce-Wirkung; `ai_direct()`/Fable
  liefert jetzt `{"setup":..., "punchline":..., "style":...}` statt nur `hook`

**Kritischer Bug gefunden+gefixt:** Licht-Leak-Filter nutzte `nullsrc` OHNE Dauer-Angabe (`d=`) →
ffmpeg deadlockte komplett (0 Frames, hängt endlos) bei JEDEM Preset außer natural (also vivid/
spectacular/cinematic/golden/punch — praktisch immer). Fix: `dur` bis zur Licht-Leak-Filterkette
durchgereicht, `nullsrc=...:d={dur}` gesetzt.

Alle Pfade mit synthetischen Testdateien end-to-end verifiziert (Frame-Extraktion): Foto→TikTok (mit/ohne
`--ai`, mit/ohne Musik), Foto→Insta, Video, Multi-Foto-Montage. Testdateien wieder entfernt.
`mission_control_api.py` unverändert (reine CLI-Aufrufe), kein MC-Neustart nötig.

**`--ai`/Fable-Pfad:** weiterhin blockiert, „Fable 5 requires usage credits" (bekannt seit 13.08., siehe
[[feedback_fable_budget_disziplin]]) — Fallback greift sauber ohne Crash, aber content-bezogene Captions
funktionieren erst wieder, wenn Fable-Guthaben da ist.

**Noch offen:** echter Content-Test durch Chris (nur synthetische Testbilder verifiziert) — beim nächsten
echten Foto/Video beobachten, ob es wirklich nach CapCut aussieht. Opus-Verfügbarkeit im Pro-Plan klären.

## 🔧 DOCTYPE-Fix Einzelvideo (07.09.2026)
`/api/aufpeppen` (Einzeldatei, mmp-Reiter) blockierte noch mit `subprocess.run()` — beim 25.08.-Fix für
`/api/aufpeppen-multi` auf Popen+Keep-Alive umgestellt, dieser Pfad dabei übersehen. Ein Video mit den
CapCut-Effekten überschreitet leicht Cloudflares ~100s-Timeout → HTML-DOCTYPE-Fehlerseite statt JSON.
Jetzt auf denselben Keep-Alive-Trick umgestellt wie `-multi`. MC neugestartet, Fix noch nicht mit echtem
Content von Chris live verifiziert.

## 🔧 Song-Länge/Text-Politur/Zieldauer/Humor-Kalibrierung (07.09.2026)
Vier Nachbesserungen am selben Tag: (1) Song-Länge-Bug in `pep_video()` gefixt (Musik-Input wurde nicht auf
Videolänge begrenzt, `overlay`-Filter stoppt nicht automatisch am kürzeren Input). (2) Eigener Textvorschlag
wird jetzt automatisch KI-poliert (`ai_polish_text()`), vorher nur bei leerem Text. (3) Neues
`--zieldauer`-Flag: echtes Video wird per `setpts` zeitgedehnt/verlangsamt auf N Sekunden, damit gezielt nur
so viel vom Song mitläuft, wie gewünscht (mmp-Feld nur bei Video+Musik sichtbar). (4) **Humor-Kalibrierung:**
KI-Captions waren zu bemüht/random (Beispiel-Fail: "Schafe, Tarifvertrag: Gras????" zu einem Heide-Video) —
beide Prompts (`ai_direct`, `ai_polish_text`) auf Chris' echten Stil umgeschrieben: trockene, tatsächlich
wahre/plausible Beobachtung statt erfundener Nicht-Sequitur-Gag, siehe [[feedback_humor]]/
[[feedback_stimme_augenzwinkern]]. Alle vier Punkte code-seitig verifiziert (synthetische Tests/py_compile).

**✅ Bestätigt (07.09.2026, gleicher Tag):** Live-Test mit echtem Chris-Video ("...sieht die Heide aus
wie ein Parkplatz mit Ambitionen") — Chris: "etwa das was ich wollte". Humor-Kalibrierung UND das neue
Captions-Feature (TikTok/Insta-Post-Captions beim Speichern-Klick, `aufpeppen_generate_captions()` in
`mission_control_api.py`) damit in der Praxis bestätigt, nicht nur synthetisch. "Etwa" = Richtung stimmt,
nicht als perfekt/abgeschlossen zu werten — bei weiteren Beispielen gegenchecken, ob's konstant trifft.

Verwandt: [[reference_mmp_media_handoff]], [[project_distrokid_promo_automation]], [[feedback_bildgenerierung]].
