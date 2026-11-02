---
name: feature-gluecksrad-klassenzimmer
description: "Glücksrad-Feature (Musikstile) fürs Klassenzimmer — hat gut geklappt, für nächsten Einsatz aufheben"
metadata: 
  node_type: memory
  type: project
  originSessionId: 299154db-e5b8-4271-80c2-778b501eaa4c
---

# 🎡 Glücksrad Musikstile — Klassenzimmer-Tool

Chris hat im Unterricht ein **Glücksrad mit Musikstilen** (Blues, Rock'n'Roll, Jazz, Hip-Hop, Metal, Techno, Reggae, Rap, K-Pop, Latin … 24 Stile mit Kurz-Beschreibung + Künstler-Beispielen) eingesetzt. **Hat gut geklappt** — für den nächsten Einsatz aufheben, nicht wegwerfen.

## Wie es funktioniert(e)
- **Beamer-Rad:** in `mission-control/index.html` (Rad dreht sich, wählt Stil+Nummer) → POST `/api/gluecksrad/state`.
- **Backend:** `mission_control_api.py` — `_gluecksrad_state`, GET/POST `/api/gluecksrad/state`, `/api/gluecksrad/stile`, `/api/gluecksrad/music`. **Bleibt alles intakt.**
- **Handy-Spiegel (mmp):** Der „Lösung"-Tab in `mobile.html` zeigte live den aktuell gedrehten Stil + Beschreibung (Polling alle 2 s) — damit Chris am Handy die Auflösung sah, während die Klasse aufs Rad schaute.

## Stand 01.07.2026
- **Handy-„Lösung"-Tab aus mmp entfernt** (Chris wollte mmp aufräumen). Der Beamer-Teil + Backend laufen weiter.
- **Wiederaufbau des Handy-Tabs:** kompletter Code (Tab-Button, Seite, `GW_BESCHREIBUNG`-Dict mit allen 24 Stilen, `loadGluecksradLoesung()`, Auto-Refresh-Timer) steckt im Backup `mission-control/mobile.html.bak-mmp-redesign-20260701-204607`. Bei erneutem Bedarf einfach von dort zurückholen.

Verwandt: [[reference_mc]], [[user_chris_teacher]].
