---
name: feedback-mmc
description: mmc = mobile Mission Control auf dem P20 (NICHT verwechseln mit Studio-Browser-MC)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2eda33f5-c7fc-493e-a3fb-970dac4bd7c3
  modified: 2026-09-10T09:49:06.710Z
---

# mmc — mobile Mission Control

mmc ist die mobile Version von Mission Control (mobile.html via bolla.chrismandel.de).
**Läuft auf dem P20** (nicht Duo 2 — Duo 2 Mic ist kaputt verklebt, siehe [[user_duo2]]).

⚠️ **Umzug in Arbeit (ab 10.09.2026):** Das P20 wird durch ein **Google Pixel 8** ersetzt
([[project_pixel8_p20_ersatz]], Lieferung ~11.–12.09.2026). Chris hat bestätigt: **mmc-Rolle
UND die SIM ziehen aufs Pixel 8 um.** Sobald das Pixel 8 eingerichtet ist: mmc = Pixel 8
(Chat-Alias „p8"), P20 raus. Bis dahin gilt weiter: mmc = P20.

## Begriffsklärung — Kommunikation auseinanderhalten!

- **mmc** → IMMER P20-Browser / mobile.html via bolla.chrismandel.de
- **Studio / Bolla-Chat im Studio** → 127.0.0.1:18790 im Studio-Browser, index.html
- **Bei Uneindeutigkeit IMMER zurückfragen** welche Quelle gemeint ist.

**Why:** Heute 18.05.2026 stundenlang verwechselt — Chris sagte "mmc-Audio dumpf/Hall", ich hab am Whisper-Setup gefeilt, dabei war's eine Studio-Aufnahme. mmc-Aufnahmen funktionieren am P20 schon lange gar nicht.

## Historie: Vorher kaputt, jetzt funktioniert ✓

**Bis 18.05.2026 Nachmittag:** mmc-Aufnahme über das Mic-Symbol scheiterte komplett auf dem P20 mit "Transkription fehlgeschlagen — Unexpected Token" (= JSON.parse-Fehler).

**Fix-Kombination 18.05.2026:**
- Frontend-JSON-Parse robust gemacht (zeigt jetzt echte Server-Antwort statt nur "Unexpected Token")
- ffmpeg-Filter `dynaudnorm` statt fester +18dB-Boost → intelligente Pegel-Anpassung
- Whisper-Settings: `beam_size=5`, `no_speech_threshold=0.7`, `initial_prompt="Sprachnotiz auf Deutsch."`
- MC-Watchdog-Schwelle auf 4.5 GB hochgesetzt → MC crasht nicht mehr → Whisper-Modell bleibt warm
- SO_REUSEPORT → MC-Restart-Bug behoben

**Welcher Faktor genau der entscheidende war ist unklar** — wir haben mehrere parallele Fixes gemacht.

## How to apply
- mmc-Aufnahme als KAPUTT führen bis gefixt
- Bei "Studio vs mmc"-Tests immer klären welche Quelle gemeint ist
- Wenn Chris von "Audio-Qualität" spricht, bei Unklarheit nachfragen
