---
name: Kostenübersicht laufende Dienste
description: Alle Dienste die Geld kosten — regelmäßig im Blick behalten und Chris informieren
type: project
originSessionId: 080984ef-5d04-4952-965e-dd355c159d3f
---
Chris will über alle anfallenden Kosten informiert werden. Immer ansprechen wenn was auffällt.

## Aktuell kostenpflichtig

### Google Gemini API (Billing aktiviert)
- **Nano Banana (BildGen)**: gemini-2.5-flash-image → kostenpflichtig, pro Bild ~Cent-Bruchteile
- **Foto-Organizer**: gemini-3-flash-preview → einmalige Aktion, ~10-15 Cent gesamt
- **TODO**: Zweiten kostenlosen Key für Analyse-Aufgaben anlegen (kein Billing), Nano Banana bleibt auf bezahltem Key
- Budget-Alert in Google Cloud auf 2€/Monat setzen empfohlen

### Anthropic / Claude
- **Suno Songs**: nutzt `claude -p` (Claude Code SDK) für jede Song-Generierung → verbraucht API-Tokens, wird über Claude Code Abo abgerechnet
- **Bolla-Chat in MC**: ebenfalls Claude Code SDK → Token-Verbrauch

### Azure
- Azure Speech (TTS): konfiguriert in config/azure_speech.json — prüfen ob aktiv genutzt wird

## Kostenlos (kein Handlungsbedarf)
- Cloudflare Tunnel: kostenloser Free-Plan
- GitHub Repo: kostenlos (privates Repo im Free-Plan)
- Claude Code Abo: Flatrate, keine Extrakosten pro Anfrage

## How to apply
Bei jeder neuen API-Integration oder größeren Aktion (wie Foto-Organizer) zuerst auf kostenlose Alternative prüfen. Chris ist Schwabe — unnötige Kosten vermeiden!
