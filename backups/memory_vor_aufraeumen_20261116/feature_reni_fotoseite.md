---
name: feature-reni-fotoseite
description: "Renis öffentliche Foto-Diashow bolla.chrismandel.de/f — Aufbau, Tageswechsel, Access-Bypass, Regen"
metadata: 
  node_type: memory
  type: project
  originSessionId: c9877f09-01b5-4d8a-829a-ce00e734c0ff
  modified: 2026-09-02T22:02:41.937Z
---

# Renis Fotoseite — `https://bolla.chrismandel.de/f`

Vollbild-Foto-Diashow fürs Handy für Reni. Gebaut 31.08.2026, analog zur mmp-Seite `/m`.
**Öffentlich, kein Login** (siehe Access-Bypass unten).

## Aufbau
- **Seite:** `~/workspace/mission-control/f.html` — Route `/f` (+ `/f.html`) in `mission_control_api.py`
  (`MOBILE_STATIC`-Dict). Swipe/Tap-Navigation, Zoom (2-Finger-Pinch + Pan + Doppeltipp,
  Pointer-Events, kein Lib), Ende-Screen „↻ Nochmal" + „✕ Beenden".
- **Fotos:** `~/workspace/mission-control/f-photos/` — Pool **120** resized JPEGs (1600px lange
  Kante, q85) + `manifest.json` (je Eintrag `src`, `cap`, `folder`). Dateinamen sind **sprechende
  Slugs** (`elefantentor-berlin.jpg`, `wiener-riesenrad-wien-oesterreich.jpg`, `mandels-3.jpg` …),
  nicht mehr `f00`–`f45`. Ausgeliefert über den `/f-photos/`-Handler in `do_GET` (basename-Schutz,
  nur `*.jpg` + `manifest.json` + `today.json`).
- **Tageswechsel:** Endpoint `GET /f-photos/today.json` wählt **15 Fotos mit Datums-Seed**
  (`random.Random(date.toordinal())`, Europe/Berlin) → wechselt täglich um Mitternacht.
  Dedup pro Tag: eindeutiger Ordner UND eindeutiges Ort-Erstwort.
- **Rollierendes „schon gezeigt"-Gedächtnis (02.09.2026):** `f-photos/served.json`
  (`{date, served[], picks[], reset}`) merkt sich ALLE bisher ausgespielten Fotos. Jeder Tag
  zieht nur aus noch nie gezeigten. Ist der Pool durch (< 15 übrig), startet eine neue Runde —
  dann sind nur die Fotos von *gestern* gesperrt, damit an der Naht nichts doppelt kommt.
  Gleicher Tag = exakt dieselbe Auswahl (stabil, `picks` gecacht). Datei wird server-seitig
  geschrieben, **nicht** über `/f-photos/` ausgeliefert. Löschen = Gedächtnis-Reset.
  Mit **120 Fotos** im Pool (Stand 02.09.2026): **7+ Tage ohne Wiederholung** bei 15/Tag, danach
  Recycling — garantiert nie dasselbe Foto an zwei aufeinanderfolgenden Tagen.
- **Blättern (f.html):** Wischen links/rechts = weiter/zurück; **zusätzlich seit 02.09.2026**
  feste Rand-Buttons ‹ › (`#edge .ez`, je 48×96 px, halbtransparent) — rechter Rand = nächstes
  Bild, linker = zurück. Tipp auf die **Mitte** (20–80 % Breite) öffnet weiter den Zoom.
  Buttons ausgeblendet bei Zoom + Ende-Screen.
- **Cache-Buster:** `today.json` hängt an jede Bild-URL `?v=<mtime von manifest.json>`. Jeder
  Pool-Neubau ändert die mtime → alle Geräte laden die Bilder neu (Bilder liegen sonst mit
  `max-age=86400` + Cloudflare-Cache). Seit dem Slug-Rebuild ändern sich ohnehin die Dateinamen.
- **f.html Auto-Refresh:** `visibilitychange` → beim Zurückkehren zur App still `today.json`
  neu holen; bei geänderter date/src-Signatur Diashow neu aufbauen. Kein manueller Reload nötig.
- **Pool ist EINGEFROREN** (120 Fotos, neu gebaut 02.09.2026 ~20:09). `build_f_photos.py` mischt
  bei jedem Lauf neu → **nicht ungefragt erneut ausführen**, nur auf Chris' Ansage. Alte Pool-Backups (46er vom 02.09., 120er vom 21.09.) wurden auf Chris' OK gelöscht (21.09.).
  Zieht aus kuratierten OneDrive-Alben (Reise + Mandels + „Eigene Aufnahmen_Backup"
  nur Renate/Robin/Stephanie/Reisen/Natur/Events). Blockt: `*_WA0*` (WhatsApp),
  Ordner Sonstiges/Familie/Essen-und-Trinken/Küche-Mami, Architektur-Kunst, Screenshots/
  Scans/Dokumente. **Caption-Logik (`POOL_SIZE=120`):** 1. GPS-EXIF → Reverse-Geocoding (Ort,
  Land · Monat Jahr); 2. sonst `claude -p`-Vision (Sonnet) erkennt Wahrzeichen/Ort; 3. sonst
  Ordnername `Ort · Monat Jahr`. Beim Rebuild 02.09.: 35 GPS (34 geocoded), 17 per Vision erkannt,
  69 Ordner-Fallback; ~685 s Laufzeit. Robin-Altersordner → „Robin".
  ⚠️ **Datenschutz-Hinweis:** Ordner-Fallback-Captions führen teils Vor-/Nachnamen + Lebens­ereignisse
  auf einer öffentlichen Seite (z. B. „Konfirmation Steffi", „Taufe Mia", „Abschied von Philipp",
  „Doktor Harry Mandel"). Bei Bedarf `manifest.json` von Hand nachputzen — mit Chris klären.

## Cloudflare Access — Bypass
- Der CF-Token in `config/cloudflare_token.json` kann **kein** Zero-Trust/Access (nur DNS/Pages/
  WorkersAI). Access-Regeln daher nur im Dashboard (Team `mandel-bolla`) oder mit neuem Token
  (`Account > Access: Apps and Policies: Edit`).
- Aktiv seit 31.08.2026: Self-hosted-App **„Reni Fotos (öffentlich)"**, Ziele
  `bolla.chrismandel.de` Pfad `f` + Pfad `f-photos`, Richtlinie Aktion **Bypass** / Include
  **Everyone**. Access wertet Bypass zuerst → `/f` offen, Rest von MP bleibt hinter Magic-Link.

## Verwandt
[[reference_mmp_media_handoff]] · [[feedback_website_schreibzugriff]] · [[reference_mc]]

## 🔄 Umbau 21.09.2026 (Zyklus-Vorplanung + Themengruppen)
- **Auswahl-Logik neu:** `scripts/f_photos_plan.py` (`group_of`, `plan_cycle`) plant den GANZEN Pool auf einmal auf Tage (120 → 8×15), Themengruppen
  (robin, weihnachten, feiern, hamburg, norderstedt, usa, italien, oesterreich, renate, mandels, sonst 1. Ordner) gleichmäßig gestreut, gleiche Gruppe/Ordner nie
  direkt hintereinander. `served.json` = `{date, picks, queue[Tageslisten], reset}`; `queue` wird pro Tagesabruf verbraucht (nicht datumsgebunden), leer → neuer
  Zyklus (Nahtschutz: gestrige Fotos nicht am ersten Tag). Ersetzt die alte `served[]`-Logik. Test: `python3 f_photos_plan.py [manifest.json]`.
- **Pool-Build:** `build_f_photos.py` schreibt jetzt in `f-photos_staging/` (Tausch manuell nach Prüfung: `history.jsonl` rüberkopieren, `served.json` löschen,
  MC neu starten). Robin gezielt: 14 Altersordner (`ROBIN_ALT_TARGET`) + 2 aktuelle = ~15/120 (Chris 21.09.: 14-18, 2-3/Tag), `BRANCH_CAP["Mandels/Robin"]=14`, neue Wurzeln „Schladming 2008" + „Renis Camera Roll 09-06-16" (Caption „Renate", cap 3).
- Ursache der „Doppelt"-Wahrnehmung war Konstruktions-Bias (28/120 Robin, weil jeder Altersordner eigener Zweig) + zu wörtliche Caption-Dedup — echte Wiederholungen gab es nie.
- **Vision sparsam (21.09.2026):** `build_f_photos.py` nutzt jetzt Haiku (`claude-haiku-4-5-20251001`), buendelt 8 Fotos pro `claude -p` (`VISION_BATCH`) und cached Ergebnisse
  dauerhaft in `scripts/f_vision_cache.json` ({abs. Pfad: Ort | null}, geseedet aus dem letzten Lauf: 15 Treffer/69 unknown). Rebuild ~84 Fotos = ~11 statt 84 Aufrufe, Haiku statt Sonnet;
  Test an 4 bekannten Fotos identisch mit Sonnet-Ergebnis. Rebuilds trotzdem lieber nachts vorschlagen (Chris entscheidet), siehe [[feedback_claude_p_massenlaeufe_kosten]].

## 🔁 Wochen-Neubau ab 05.10.2026 (Chris-Konzept, ersetzt „Pool eingefroren")
- Chris störten Wiederholungen nach 8 Tagen (60.000 Fotos im OneDrive). Neu: **jeden Sonntag 03:00** Cron `scripts/f_photos_weekly.py` → baut 120 frische Fotos (`build_f_photos.py`), nie gezeigte (`scripts/f_used.json` = dauerhaft verbrauchte rel. Pfade ab /mnt/d/OneDrive; Manifest-Feld `orig`), wirft Beinahe-Dubletten raus (dHash ≤40/256), tauscht Pool atomar (alter → `f-photos_prev`), löscht `served.json`, meldet per Telegram. Fehler → alter Pool bleibt live.
- Rechnung: 105 Fotos/Woche aus 60.000 → ~10 Jahre ohne Wiederholung. 8. Tag des 120er-Zyklus fällt weg (nur 7 Tage genutzt, alle 120 gelten als verbraucht).
- Erstlauf manuell 05.10. ~12:50; alte 120 aus build_f.log in f_used.json eingetragen. Crontab-Backup backups/crontab_vor_fpool_weekly_*.txt. Der Satz „Pool EINGEFROREN … nur auf Ansage" oben gilt nicht mehr.
