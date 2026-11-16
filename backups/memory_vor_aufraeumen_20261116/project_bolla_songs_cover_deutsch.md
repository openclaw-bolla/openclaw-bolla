---
name: project-bolla-songs-cover-deutsch
description: "ERLEDIGT 10.09.2026 — Bolla-Songs-Cover in MP komplett auf Deutsch bedienbar (deutsches Wunsch- + Korrektur-Feld, Chris fasst nie englischen Prompt an)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0deb2e12-ac31-4014-8964-1e949e1f41e9
  modified: 2026-09-10T20:13:26.501Z
---

# Bolla Songs Cover: deutsch bedienbar in MP — ✅ ERLEDIGT (10.09.2026 ~22:00)

Chris wollte die Cover-Erstellung **komplett in MP auf Deutsch** — nie einen englischen Prompt
anfassen. O-Ton: „ich möchte das in Zukunft über MP machen" + „mein Englisch ist nicht gut genug".
[[feedback_gemini_bild_kostenpflichtig]] (Cloudflare FLUX = Gratis-Engine).

## Was jetzt steht (Schritt 3 der Cover-Karte „🎵 Song herunterladen + Cover erstellen")
3-Schritt-Flow (auf Chris' Wunsch vom 10.09. ~22:15 — er wollte den Vorschlag-Knopf sehen und
seine Korrekturen in genau diesen EN-Prompt eingebaut bekommen):
1. **„📝 Prompt-Vorschlag holen"** → `POST /api/suno/cover-prompt` (claude, gratis) → englischer
   Bild-Prompt erscheint **read-only** im Feld `#suno-cover-eng` (gestrichelter Rahmen, „musst du
   nicht anfassen"). Speichert in JS-Var `_sunoCoverEngPrompt`.
2. **✏️-Feld `#suno-cover-wish`** (deutsch) + **„🔧 In den Prompt einbauen (gratis)"** →
   `POST /api/suno/cover-wish` mit **`render:false`** → `_suno_cover_prompt_from_wish(title, lyrics,
   wish, prev_prompt=_sunoCoverEngPrompt)` baut die deutsche Änderung in den EN-Prompt ein, **kein
   Bild**, read-only Feld wird aktualisiert. Beliebig oft, 0 ct. (Ohne vorherigen Vorschlag baut es
   aus dem Wunsch den ersten Prompt.)
3. **„🎨 Cover erzeugen (gratis)"** / **„🌟 Finale in HD (~10 ct)"** → `POST /api/suno/cover-render`
   {title, prompt=Feldinhalt, engine} rendert den aktuellen EN-Prompt, setzt direkt
   `<Titel>_cover.jpg` (Suno_DistroKid + Desktop\DistroKid). `cloudflare-flux` gratis (Fallback
   Pollinations), `mai` ~10 ct.
- Chris fasst den englischen Text **nie selbst an** — Feld ist `readonly`, Änderungen nur per
  deutschem ✏️-Feld.
- Liedtext kommt aus **Schritt 2** (`#suno-pub-lyrics`, EIN Feld für alles) — kein zweites Tippen.

## Technik
- Backend `mission_control_api.py`: `_COVER_PROMPT_RULES` (Kurzregeln), `_suno_cover_prompt_from_wish()`
  (claude → 1 EN-Satz, mit/ohne `prev_prompt`), Endpoint `/api/suno/cover-wish` mit **`render`-Flag**
  (default true; `false` = nur Prompt umbauen, kein Bild). `/api/suno/cover-prompt` + `/cover-render`
  wieder aktiv verdrahtet.
- Frontend `index.html`: JS `sunoCoverSuggest()` / `sunoCoverRefine()` / `sunoCoverRenderNow()`
  (+ Helfer `_sunoCoverEngBtns()` / `_sunoCoverSetEng()`). Ersetzen die kurzlebige
  `sunoCoverWish`/`sunoCoverFix`/`_sunoCoverGo`-Fassung.
- Alte Endpunkte `/covers`, `/cover-extra`, `/pick-cover` bleiben im Code, nicht mehr verdrahtet.
- E2E getestet 10.09. ~22:12: Vorschlag „Leuchtturm im Nebel" → Korrektur „Leuchtturm weg, alte
  Laterne auf Steg, Kamera tiefer" → EN-Prompt sauber umgebaut (Nebel/Schiff/Stimmung bleiben) →
  Render gratis. Testdateien gelöscht. Server-PID nach Neustart: 176986.

## Bekannte Fallstricke / gelernt
- FLUX-1-schnell (Cloudflare, gratis) macht bei Personen kaputte Arme + erfindet Marken-Logos →
  menschenleere Motive bevorzugen (steckt in `_COVER_PROMPT_RULES`).
- Cloudflare-flux hat gelegentlich Schluckauf → Fallback Pollinations liefert trotzdem gratis.
- Cover hat ~0 Einfluss auf Spotify-Sichtbarkeit (Playlisting + Hörer-Signale zählen) — wirkt nur
  im Moment, wo jemand es sieht: „seriös vs. Massenware".

## Song „What I Master Doesn't Master Me" (bollawave, EN, KI-Thema)
Cover war zuletzt der grüne Röhrenrechner mit Abendsonne (in Suno_DistroKid). Song kann über
Schritt 4 „🚀 Für DistroKid fertig machen", sobald die Audiodatei in `Desktop\DistroKid\` liegt.
