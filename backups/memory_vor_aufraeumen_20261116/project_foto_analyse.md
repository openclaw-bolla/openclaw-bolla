---
name: Foto-Analyse Feature
description: KI-gestützte Foto-Suche in Mission Control via LM Studio (lokal)
type: project
originSessionId: 392e2e08-0564-42ef-9c3b-3e90798109e6
---
Vollständig implementiertes Feature in MC (`#page-fotoanalyse`).

**Wie es funktioniert:**
- LM Studio (lokal, Port 1234) analysiert Fotos und erzeugt englische Beschreibungen
- Ergebnisse in `/home/bolla/workspace/data/photo_analysis.json` (kumulativ, alle Läufe)
- Suche: Claude übersetzt deutschen Begriff → englische Suchterme → filtert Beschreibungen
- ~2.1s pro Foto, 8000 Fotos ≈ 4.8 Stunden

**API-Endpunkte:**
- `GET /api/photos/status` — Analyse-Fortschritt
- `GET /api/photos/results` — alle analysierten Fotos
- `POST /api/photos/start` — Analyse starten (folder, prompt, model, lmstudio_url)
- `POST /api/photos/stop` / `clear` / `remove` / `rename`
- `POST /api/photos/search` — Claude-Übersetzung + Suche
- `POST /api/photos/export` — Treffer nach `D:\OneDrive\Suchergebnisse\<Begriff>\` kopieren
- `GET /api/photos/thumb?path=` — Thumbnail
- `GET /api/fs/dirs?path=` — Ordner-Browser (allowed: OneDrive, Users/ernst, ~)

**Wichtige Bugs/Fixes (Stand 2026-05-04):**
- Poll darf nie selbst `faSearch()` aufrufen → löst "Wi"-Bug beim Tippen
- `_faSearchInFlight` hat 25s Safety-Timeout
- Such-Prompt: einfache Grundbegriffe zuerst ("wood" vor "timber")
- Treffer-Klick: globales `_faShown[]` + Index statt JSON.stringify inline

**Export:**
- CSV → Browser-Download `Downloads\foto-analyse-<datum>.csv`
- OneDrive → `D:\OneDrive\Suchergebnisse\<Suchbegriff>\`

**Why:** Großer Foto-Bestand (OneDrive), keine Cloud-KI gewünscht, alles lokal via LM Studio.
**How to apply:** Bei Änderungen an der Foto-Suche immer den Poll-Bug im Kopf behalten.
