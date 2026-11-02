---
name: project-handy-foto-zwischenablage
description: Foto-Button live verifiziert (14.07.2026); Rest (Reconnect-Watcher, Commit) weiter geparkt
metadata:
  node_type: memory
  type: project
  originSessionId: current
  modified: 2026-08-23T17:38:11.231Z
---

# 📷 Handy-Foto → Studio-Zwischenablage (Duo/P20)

**Status: Ausbaustufe 1 GEBAUT + LIVE GETESTET (14.07.2026) — Rest weiter geparkt.**

## Was funktioniert (der Gewinner-Weg)
**ADB-Pull ist DER Weg:** Duo per mp gekoppelt+verbunden, neuestes Kamerafoto via `adb pull` → PowerShell `Clipboard::SetImage` → in Windows-Zwischenablage. Live bewährt (ganzer Amazon-Chat lief darüber). Verworfen: Web-Share-Target (mmp) — am Duo nicht im Teilen-Menü aufgetaucht (kein PWA-Manifest mit share_target); Endpoint `/api/share` bleibt harmlos im Server drin.

## Ausbaustufe 1 — FERTIG + VERIFIZIERT (14.07.2026)
**📷 mp-Knopf „Neuestes Foto → Zwischenablage"** gebaut, in der Duo-Funktionen-Karte (Surfaces-Seite) direkt unter Screenshot.
- Backend `mission_control_api.py`: `_adb_latest_photo_path()` (MediaStore-Query `content query --uri content://media/external/images/media`, Fallback `ls -t` in DCIM/Camera), `_set_windows_clipboard_image()` (gleiche PowerShell-STA-Technik wie `/api/share`), `adb_latest_photo_to_clipboard()` — Route `POST /api/adb/latest-photo`.
- Foto landet zusätzlich als Datei in `/mnt/d/OneDrive/Bilder/Handy-Clip/` (Historie), Dateiname `handy_YYYYMMDD_HHMMSS_xxxx.ext`.
- **14.07.2026 live getestet:** Duo war per ADB verbunden (`192.168.178.20:40691`), Endpoint per curl aufgerufen → `{"ok": true, "filename": "IMG_20260714_111811.jpg", ...}`, Foto landete korrekt in Windows-Zwischenablage + als Kopie in `Handy-Clip/`. Funktioniert wie geplant.

## Aufräumen — FERTIG (14.07.2026)
`scripts/handy_clip_cleanup.py`, Cron `0 8 * * *`: löscht Dateien in `Handy-Clip/` älter als 14 Tage (Original bleibt eh auf dem Handy, kein Verlust). Log `logs/handy_clip_cleanup.log`.

## ✅ WhatsApp-Medien-Archivierung via ADB (23.08.2026, manuell/einmalig)

Robin hat vom Kilimanjaro (Famulatur-Trip, [[project_robin]]) 150 Fotos/Videos per WhatsApp geschickt. Chris wollte sie in `Mandels/Robin/23-24/Kilimanjaro/` archiviert haben. Der Windows-WhatsApp-Desktop-Weg (Store-App, WebView2-basiert) speichert Medien NICHT als lose Dateien — nur Einzeldownload über die App-UI möglich. **Der ADB-Weg über den Duo ist deutlich besser:** Android legt WhatsApp-Medien als echte Dateien ab unter `/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images/` bzw. `.../WhatsApp Video/` — direkt per `adb pull` abgreifbar, sortiert/gefiltert nach Dateiname (`IMG-YYYYMMDD-WAxxxx.jpg`).

**Ablauf, der funktioniert hat:**
1. Duo per ADB verbinden (`adb devices`, IP+Port aus Wireless-Debugging-Screen falls nicht schon verbunden)
2. `adb shell ls .../WhatsApp Images/` bzw. `.../WhatsApp Video/`, nach Datum filtern (`grep YYYYMMDD`)
3. Einzeln per `adb pull` in Staging-Ordner (Desktop\temp, [[feedback_pruef_ordner_temp]]) ziehen
4. Umbenennen in schönes Schema (`Kilimanjaro 2026-08-23 (001).jpg`, `... Video (001).mp4`) + ins Zielarchiv verschieben
5. Staging aufräumen

**Einschränkung:** Kann NICHT nach Chat/Absender filtern, nur nach Datum — bei mehreren Chats am selben Tag können fremde Bilder mit reinrutschen, Chris muss kurz drüberschauen. Voraussetzung: Medien müssen auf dem Handy tatsächlich heruntergeladen sein (bei Videos oft nicht automatisch).

**Nebenfund:** Nach dem Schreiben aus WSL zeigte Chris' bereits offenes Explorer-Fenster zunächst nur ~30 von 150 Dateien — kein Datenfehler, nur Anzeige-Lag, siehe [[reference_wsl_explorer_refresh]].

## Offene Ausbaustufen (Reihenfolge)
1. ~~📷 mp-Knopf „Neuestes Foto holen"~~ ✅ erledigt + verifiziert, s.o.
2. ~~🧹 Aufräumen alter Dateien in Handy-Clip~~ ✅ erledigt, s.o.
3. **🔄 ADB-Reconnect-Watcher** (Cron) — hält Duo-Verbindung, Port-Scan nach Reboot. mDNS geht in WSL NICHT → Port muss aktiv gesucht werden. Nachtfenster-tauglich [[feedback_wartungsfenster_surfaces]].
4. **Code committen** — Share-Target-Endpoint bleibt drin (stört nicht).

## Fallen (gelernt)
- ⚠️ `pkill -f mission_control_api.py` killt die EIGENE Bash-Shell mit → **Server-Kill immer numerisch** über Port-Inhaber (`ss -tlnpH 'sport = :18790'` → `kill <PID>`). [[feedback_crontab_pipe_falle]]
- ADB-Port ist dynamisch (hier 40921) → nach Reboot neu ermitteln.

Bezug: [[user_duo2]] (Duo 2 hat ADB via WLAN, P20 nicht).
