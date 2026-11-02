---
name: Mission Possible (MP)
description: Chris schreibt "mp" wenn er Mission Possible meint (früher Mission Control / MC) — Struktur, Zugang, Seiten und API-Endpunkte
type: reference
originSessionId: fb08c238-bdfe-4c80-ad9f-bbb99e7c8b12
modified: 2026-08-17T15:49:10.234Z
---
**MP = Mission Possible** (Chris' persönliches Dashboard, früher "Mission Control / MC")
Kürzel: **mp** (nicht mehr mc)

- Lokal: `http://127.0.0.1:18790/`
- Remote: `https://bolla.chrismandel.de`
- HTML-Quelle: `/home/bolla/workspace/mission-control/index.html`
- API-Server: `/home/bolla/workspace/scripts/mission_control_api.py`

## 🎵 „Bolla Songs"-Charts = KEIN Spotify-API-Zugang!
Die Top-10-Charts mit Vorhör-Play auf der „Bolla Songs"-Seite kommen NICHT aus einem Spotify-Konto. Quellen (beide gratis, ohne Login): **Chart-Platzierungen** via Scrape von **kworb.net** (`/api/charts`, Spotify-Chartdaten gespiegelt) + **Vorhör-Schnipsel** via **iTunes/Apple-Search-API** (`/api/charts/preview`, 30-Sek-previews frei). → NICHT behaupten, Bolla habe Spotify-API-Zugriff. Für Spotify-spezifisches Tracking (z.B. Bollawave-Releases) bräuchte es eine kostenlose Spotify-Developer-App (client_id+secret → `config/spotify_credentials.json`). Live-Signal sonst über iTunes/Apple ([[project-suno-distrokid-blocklist]], `spotify_watcher.py`).

## ⚠️ Wichtig: Vor Workarounds immer API-Liste prüfen!
MC hat bereits viele Endpunkte. Bevor ich etwas skripte oder extern abfrage → checken ob MC das schon liefert.

## API-Endpunkte (GET, sofern nicht anders)

### Claude / Token / Quota
- `/api/claudequota` — **ECHTE Anthropic OAuth-Quota** (5h + 7-Tage %, reset_label) — KEIN Token-Verbrauch! Für Limit-Checks immer dies nutzen, nie Probe-Calls!
- `/api/tokenusage` — Token-Nutzung (eigene Zählung)
- `/api/tokenusage/history` — Historische Halbtagswerte
- `/api/tokenbudget` — Budget-Übersicht
- `/api/tokenbudget/snapshot` — Budget-Snapshot

### System / Geräte
- `/api/status` — MC-Server alive check `{ok: true}`
- `/api/sysinfo` — Systeminfo (CPU, RAM, etc.)
- `/api/surfaces/book` / `/api/surfaces/pro` / `/api/surfaces/studio` — Surface-Gesundheit
- `/api/surfaces/energie` — Energiedaten
- `/api/crontab` — Aktuelle Crontab

### Kommunikation / Daten
- `/api/clipboard` (GET/POST) — Geräteübergreifendes Clipboard (gclip); POST mit `append=true`
- `/api/clipboard/trash` — Papierkorb
- `/api/clipboard/images` — Bild-Clipboard
- `/api/email` — E-Mails
- `/api/calendar` — Kalender
- `/api/calendar/search` — Kalendersuche
- `/api/birthdays` — Geburtstage
- `/api/chat-history` — Chat-Verlauf

### Inhalte / Tools
- `/api/memory` — Memory-Daten
- `/api/photo` — Foto des Tages
- `/api/recipe` — Rezept des Tages
- `/api/quicknotes` — Schnellnotizen
- `/api/robin` — Robin-Info
- `/api/newsletter` — Newsletter
- `/api/charts` — Charts
- `/api/workshop` — Workshop-Daten

### Reise / Immo
- `/api/travel` — Reiseplaner
- `/api/trip/plan` (POST) — Routenplanung
- `/api/immo-bookmarks` / `/api/immo-criteria` / `/api/immo-news` — Immobilien

### Schule / KI-Forum
- `/api/korrektur/*` — Korrektur-Tools (analyze, docx, annotate, excel)
- `/api/kiforum/*` — KI-Forum (bolla, chris, respond, add, generate, conclude, archive-delete)
- `/api/elternbrief/entschaerfen` (POST) — Elternbriefe entschärfen
- `/api/schueler/stammdaten` — Klasse+Geburtstag aller 106 Schüler 7a-7d (aus `data/schueler_stammdaten.json`), speist Tab-Autofill im Bolla-Songs-Formular

### Medien / Suno
- `/api/suno/generate` (POST) — Suno-Musik generieren
- `/api/bildgen` (POST) — Bildgenerierung
- `/api/bolla/tts` (POST) — Text-to-Speech
- `/api/photos/*` — Foto-Verwaltung (start, stop, search, export)

### ADB (Android/Duo)
- `/api/adb/devices` / `/api/adb/info` / `/api/adb/screenshot` / `/api/adb/push` / `/api/adb/pull`

## Seiten (Sidebar-Navigation)
- 📊 Dashboard · 🐾 Bolla · 🏫 Schule · 📅 Kalender · 📧 E-Mail
- 🌍 Robin · 🎂 Geburtstage · 🖧 Local Server · 📱 Surface Duo
- 🎨 Redesigns · 🍌 BildGen · 🌤️ Wetter · 🖥️ System Info · 🧠 Bolla's Brain

## Tech
- Python-Server startet @reboot per Cron
- Cloudflare Tunnel: `cloudflared tunnel run bolla-mc`
- Obsidian Vault = `/home/bolla/workspace/` (geöffnet in Obsidian)
