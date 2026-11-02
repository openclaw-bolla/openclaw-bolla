---
name: E-Auto & Ladekosten
description: Chris fährt VW ID.3 1st, Ladekosten-Präferenzen für Unterwegs
type: user
originSessionId: dfa8875a-0ac2-4b8c-bbe7-b04d2c559b7d
modified: 2026-09-21T17:09:21.255Z
---
**Fahrzeug:** VW ID.3 1st, Kennzeichen **SE-RM 212E**

**Inspektion:** Letzte Inspektion **21.09.2026**. Nächste in 720 Tagen = **ca. 10.09.2028** (Sonntag → also realistisch die Woche davor/danach terminieren).

**Reichweite pro Ladung (realistisch + Puffer, für Reiseplanung):**
- **Sommer:** ~200 km pro Ladung
- **Winter:** ~160 km pro Ladung
- Danach jeweils **~30 Min laden**.
- **How to apply:** Bei Reisezeit-Schätzungen (MC-Reiseplaner) nach ca. dieser Strecke einen 30-Min-Ladestopp einplanen und in die Gesamtzeit einrechnen. Umgesetzt im Reiseplaner-Prompt in `mission_control_api.py` (`trip_plan`, Variable `ev_inst`), saison-abhängig über das Reisedatum.

**ECHTE Erfahrungswerte Langstrecke (wichtiger als Theorie!):**
- **Norderstedt ↔ Ulm (zu Robin), ~720 km:** Winter ~**10 h**, Sommer ~**9 h** (inkl. aller Ladestopps/Pausen). Effektiver Schnitt also ~72 km/h Winter / ~80 km/h Sommer.
- **How to apply:** Lange Strecken IMMER nach diesen realen Schnitten rechnen und **großzügig aufrunden** ("etwas Luft" lassen, Chris' Wunsch). Verbrenner-Fahrzeiten (z.B. „700 km = 6½ h") sind für den ID.3 zu optimistisch. Diese Werte sind seit 2026-06-07 auch in der Sommerreise-2026-Anreise (`SR_ROUTE[0]` in index.html) und im `trip_plan`-Prompt hinterlegt.

**Ladekosten-Priorität (günstigste zuerst):**
1. **EnBW** — 46 ct/kWh (mit Abstand bevorzugt)
2. **ARAL Pulse** — 55 ct/kWh (knapp dahinter, akzeptabel)
3. **Alle anderen** — min. 69 ct/kWh → nur im Notfall, zu teuer

**How to apply:** Bei Reiseplanung immer zuerst EnBW-Stationen suchen, dann ARAL Pulse. Andere Betreiber nur wenn keine Alternative vorhanden.

**Navi-Ziele ans Auto senden:** Chris nutzt die VW App auf der Duo, um Navi-Ziele direkt ans Auto zu schicken (funktioniert nur von der Duo aus, nicht vom Studio/PC). Wenn ich für unterwegs eine Adresse fürs Auto-Navi brauche, reicht eine navi-taugliche Adresse (Straße, PLZ, Ort) — Chris trägt die dann selbst über die VW App ein. Praktisch fürs gclip: einfach die fertige Adresse reinlegen, Chris übernimmt sie von dort in die App.
