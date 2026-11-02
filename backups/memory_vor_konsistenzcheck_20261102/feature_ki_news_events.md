---
name: feature-ki-news-events
description: Struktur & Workflow der KI-News-Seite in MP (Top-Nachricht, Event-Archiv, Recap-Boxen) — inkl. offener Recap-Termine
metadata:
  node_type: memory
  type: project
  originSessionId: current
  modified: 2026-08-16T07:41:35.188Z
---

Am 16.08.2026 komplett neu aufgebaut, `data/ki_news.json` + `mission-control/index.html` (Seite `page-ki-news`).

## Struktur
- **🔥 Heute wichtig** (`ki-top-box`, ganz oben): rotiert deterministisch nach Kalendertag durch einen Pool aus allen `news[].punkte`-Stichpunkten + Event-Beschreibungen (`kiRenderTopBox()`). Kein täglicher Rechercheaufwand — reine Rotation durch Vorhandenes, Chris-Entscheidung 15.08.2026.
- **📅 Kommende Events**: Events aus `events[]`, deren Datum < 30 Tage in der Vergangenheit liegt. Events, deren Datum bereits verstrichen ist, zeigen ihren Status im Badge ("War am ..." wenn Recap vorhanden, sonst "vor X Tagen · Recap folgt").
- **📦 Archiv** (`ki-events-archive-toggle/-list`): Events älter als 30 Tage, ausklappbar unten in derselben Karte (kein Popup — Chris-Entscheidung 15.08.2026), nur Datum + Titel pro Zeile.
- **Recap-Verknüpfung**: Ein Event wird klickbar, sobald sein Datum verstrichen ist UND ein `news[]`-Eintrag mit **derselben `id`** existiert. Klick öffnet `#ki-recap-modal` mit der vollen Detail-Box (Video, Stichpunkte, Ampel-Bewertung — Vorbild war der bestehende `ms-build-2026`-Eintrag). Funktioniert auch aus dem Archiv heraus.
- Rendering-Funktionen: `kiRenderNewsCard()` (eine News-Karte, wiederverwendet für Featured-Liste UND Modal), `kiRenderTopBox()`, `kiEventCard()`, `kiToggleArchive()`, `kiOpenRecap()/kiCloseRecap()`.

## ⚠️ Standing Workflow — MEINE Aufgabe, nicht Chris'
Chris' Entscheidung 15.08.2026: **Ich recherchiere proaktiv**, sobald ein Event stattgefunden hat — nicht erst auf Ansage warten. Sobald ein Event-Datum verstrichen ist, echten YouTube-Video-Link + Stichpunkte + Ampel-Bewertung recherchieren (WebSearch, kostenlos) und als neuen `news[]`-Eintrag mit **passender `id`** (identisch zur Event-`id`) in `data/ki_news.json` eintragen — dann verknüpft sich das Event automatisch. NIE Inhalte erfinden (Video-ID, Bewertung) — nur wenn echte Quellen auffindbar sind.

**Offene Recap-Termine (nach Event-Datum aktiv werden):**
- `meta-connect-2026` — Meta Connect, 23.–24.09.2026
- `openai-devday-2026` — OpenAI DevDay, 29.09.2026
- `ai-conference-2026` — The AI Conference, 29.09.–01.10.2026
- `mcp-dev-summit-toronto-2026` — MCP Dev Summit Toronto, 05.–06.10.2026

Bei Session-Start ab Ende September: kurz prüfen, ob eines dieser Daten verstrichen ist und der Recap noch fehlt.

Die 4 alten Juni-Events (Apple WWDC, AI Summit London, SuperAI Singapore, Databricks Summit) sind bewusst OHNE Recap im Archiv gelassen — keine Erfindung nachträglich, da keine echte Recherche dazu vorliegt.
