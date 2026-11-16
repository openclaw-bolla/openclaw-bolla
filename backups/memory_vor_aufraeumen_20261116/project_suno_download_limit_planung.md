---
name: project-suno-download-limit-planung
description: Suno Download-Limit seit 03.09.2026 (Pro 20/Monat, Premier 60) — Chris' Planung: 1 Monat Premier ab 01.10.2026, danach zurück auf Pro, Downloads vorausplanen
metadata:
  type: project
---

**Fakten (Web, 01.10.2026):** Suno-Downloadlimit seit 03.09.2026: Pro 20/Monat, Premier 60/Monat, nicht genutzte verfallen. Zukauf ~2,99 $/Song (kein Mengenrabatt, nur Newsletter-Quelle, nicht in Suno-UI verifiziert). Hören/Teilen im Browser zählt nicht. Unklar: ob WAV/Video/Re-Download einzeln zählen, ob Reset am Abrechnungstag oder Monatsanfang → in Suno-UI (Download-Menü) prüfen.

**Chris' Entscheidung (01.10.2026):** Einen Monat auf Premier upgraden, danach zurück auf Pro, Downloads bewusst vorausplanen. Bedarf laut Chris ~32 Songs/Monat (2 Songs × 4 Schüler/Woche) — Geburtstage laut `data/schueler_stammdaten.json` pro Monat: Okt 6, Nov 8, Dez 11, Jan 7, Feb 12, Mär 9 (106 Schüler gesamt).

**Why:** Pro-Limit (20) reicht bei 32/Monat nicht; Premier-Monat soll als Vorrat dienen, weil Schüler-Geburtstagssongs zeitlos sind ([[feedback_geburtstagssong_zeitlos]]) und vorab erzeugt/heruntergeladen werden können.

**How to apply:** Während Premier-Monat Songs für Nov/Dez (ggf. Jan) vorab generieren+herunterladen. Vor Ablauf des Premier-Monats Downgrade auf Pro erinnern (Datum der Verlängerung bei Chris erfragen). Pro dann nur für das Nötigste: nur den verwendeten Take herunterladen. Siehe [[reference_suno]].

**Stand 01.10.2026:** Premier heute gebucht, Abrechnung neu auf **01.11.2026**. ⏰ **Downgrade auf Pro spätestens bis 31.10.2026 (besser ab 28.10.)**, sonst verlängert sich Premier. Bei Session-Start ab 25.10. Chris daran erinnern. Bis dahin Vorrat laden: Okt+Nov+Dez-Songs (+ evtl. Jan/Feb), max. 60 Downloads.

**Download-Planer gebaut (01.10.2026):** MP → Bolla Songs → Header-Button "🎧 Downloads". Pro Schüler DE+EN abhakbar (Geburtstage aus `schueler_stammdaten.json`, Okt 2026–Jul 2027), Periodenzähler (Premier 01.–31.10. Limit 60, Pro ab 01.11. Limit 20), "➕ Sonstiger Download", "✏️ korrigieren" (Vorab-Zähler). Daten: `data/suno_downloads.json`; API `GET /api/suno/downloads`, `POST /api/suno/downloads/{toggle,undo-sonst,vorab}` in `mission_control_api.py`; UI-JS `sunoDl*` in `index.html`. Backups `backups/*_pre-dl-planer.*`. Perioden für Dez+ müssen bei Bedarf in der JSON-Datei ergänzt werden (aktuell nur Okt+Nov).


**UPDATE 02.10.2026 — Download-Planer in MP wieder ENTFERNT (Chris' Wunsch):** Chris erzeugt die Songs NICHT nach realen Geburtstagsdaten. Er startet jede Stunde mit 2 Songs, einige Schüler hatten im Juli/August Geburtstag und kämen im laufenden Schuljahr sonst nicht dran → die Download-Rechnung macht er selbst. Er hat immer nur **einen Plan pro 4er-Block → braucht 16 Songs pro Block** (4 Stunden/Schüler × 2 Songs ×… Chris rechnet das selbst). Button „🎧 Downloads", Box, JS und API `/api/suno/downloads*` sind raus; Backups `backups/*pre-dlplaner-entfernen*`, Daten `backups/suno_downloads_*.json`. **Nicht wieder anbieten.** Premier-Monat/Downgrade-Termin 31.10. gilt weiterhin.
