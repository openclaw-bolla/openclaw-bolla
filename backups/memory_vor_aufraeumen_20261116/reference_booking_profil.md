---
name: reference-booking-profil
description: "Chris' Booking.com-Profil — Genius Level 3, kostenlos Storno, Buchung am Handy"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b124b06b-7724-4d33-bc4e-9516baea3c17
---

# Chris' Booking.com-Buchungsweise

- **Genius Level 3** Kunde (höchste Stufe — kostenlose Frühstücks-/Upgrade-/Rabatt-Vorteile bei teilnehmenden Häusern). Aktiv automatisch, sobald im Booking-Konto eingeloggt.
- **Bucht IMMER mit kostenlosem Storno** (free cancellation) — Reservierungen sind unverbindlich bis zur Frist.
- **Buchung am Handy** (Booking-App), dort gibt's oft zusätzliche App-only-Rabatte. NICHT am Desktop.
- Bestätigungsmails landen bei **ernstmandel@outlook.de** (Absender `noreply@booking.com` / `*.property.booking.com`).

**How to apply:** Beim Reiseplaner-Booking-Suchen Genius nicht extra erwähnen (ist eh aktiv). Storno-Frist IMMER nachverfolgen — der [[reference_mc]]-Reiseplaner hat dafür Kalender+Telegram. Der Wächter `scripts/booking_watcher.py` parst Chris' Booking-Bestätigungen automatisch und ordnet sie den Etappen zu (siehe [[aktuell]]). Verbindung zu [[project_immokauf]] / Sommerreise-Etappen.

**Watcher-Fähigkeiten (Stand 01.07.2026, von mir ausgebaut):**
- **Zuordnung 50-km-Umkreis:** Erst Namens-/Alias-Abgleich, dann Geo-Fallback — Buchungsort wird via Nominatim (kostenlos) geocoded und der nächstgelegenen Etappe ≤ 50 km zugeordnet. So landen Nachbarorte (z. B. Rastatt → Baden-Baden, 11 km) automatisch richtig. Etappen-Koordinaten (lat/lon) stehen in `SR_ROUTE` in index.html.
- **Frühstück:** wird aus der Mail erkannt („im Endpreis inbegriffen" → 🍳-Zeile in der Planer-Notiz + Telegram; „ohne Frühstück" → ⚠️-Warnung). Siehe [[feedback_buchung_fruehstueck_storno]].
- **Stornierungen:** „Buchung storniert für die Unterkunft X"-Mails werden erkannt → Hotel wird aus der passenden Etappe entfernt (allgemeine Notiz bleibt), Telegram-Info. Neueste Mail zuerst → Neubuchung überschreibt vor dem Storno, Storno löscht dann nichts Falsches.
- **Storno-Frist-Parsing** erweitert: erkennt auch ausgeschriebene Daten („bis 25. Juli 2026", an „€ 0" gekoppelt) und „kostenlos bis 18:00 am Tag der Anreise" → Anreisetag.
- Reine „Sie haben eine Nachricht von …"-Chat-Mails werden ignoriert (keine Buchungen).

## Login-Code-Nerv behoben (19.07.2026)
Booking.com verlangte bei jedem Website-Aufruf einen per E-Mail zugeschickten Code (Cookie wurde offenbar
nicht gehalten). Fix in Edge (Chris hat's selbst Schritt für Schritt umgesetzt, ich konnte nur anleiten —
Playwright läuft in WSL auf einem separaten Linux-Chromium, hat keinen Zugriff auf Chris' echtes
Edge-Profil): `edge://settings/content/cookies` → Ausnahme `[*.]booking.com` bei „Websites, die Cookies von
Drittanbietern hinzufügen dürfen" + `edge://settings/privacy` → Tracking-Prävention (Stufe blieb auf
„Ausgeglichen") → Ausnahme `booking.com` hinzugefügt. **Falls der Code-Zwang trotzdem wiederkommt:** nächster
Verdächtiger ist F-Secure Browsing Protection (Cookie-/Tracking-Blocker), siehe [[user_fsecure]].
