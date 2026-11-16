---
name: F-Secure Internet Security
description: Chris nutzt F-Secure Internet Security seit 20+ Jahren, primär für Banking-Schutz — wichtiges Tool, Einstellungen gelegentlich prüfen
type: user
originSessionId: 46e043d1-72fc-4265-adaa-05b2246070d7
---
Chris nutzt **F-Secure Internet Security** (als WISO Internet Security installiert, powered by F-Secure) seit über 20 Jahren. Primärer Zweck: Schutz von Banking-Webseiten.

Sehr wichtig für Chris — nicht leichtfertig deaktivieren oder ändern. Bei Problemen mit Kamera/Mikrofon/Netzwerk immer auch F-Secure als mögliche Ursache prüfen.

Die Browser-Extension "Browserschutz von F-Secure" ist in Edge aktiv und hat einmal die Kamera in Bolla (127.0.0.1:18790) blockiert → Lösung: Whitelist für 127.0.0.1:18790 und bolla.chrismandel.de in F-Secure eintragen.

**Website-Ausnahmen verwalten (Zugelassen/Blockiert):**
WISO Internet Security → **Sicherer Browser** → Link "Website-Ausnahmen anzeigen" → Tab "Zugelassen" → "Neu hinzufügen"

Bekannte Ausnahmen die eingetragen sein sollten:
- `127.0.0.1:18790` — Mission Control lokal (Kamera/Mikrofon)
- `bolla.chrismandel.de` — Mission Control remote
- `speech.platform.bing.com` — Web Speech API (für Mikrofon in MC-KI-Forum)

**How to apply:** Bei unerklärlichen Verbindungs- oder Zugriffsfehlern in Edge → F-Secure prüfen. Pfad für Ausnahmen: WISO → Sicherer Browser → Website-Ausnahmen.
