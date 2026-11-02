---
name: voice-setup
description: "Sprachnotiz + Bolla-Chat-Mic — Whisper-Pipeline, Optimierungen, F-Secure-Kontext"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2eda33f5-c7fc-493e-a3fb-970dac4bd7c3
---

# Voice in MC — wie es funktioniert

## Architektur (alles lokal, kein F-Secure-Block möglich für Mic-Eingabe)

**Frontend (index.html):**
- Drei Sprach-Buttons rufen alle den gleichen Endpoint `/api/transcribe` auf:
  - Mission Control "🎙️ Sprachnotiz" → Clipboard-Eintrag
  - Bolla-Chat "🎤" → Text in Eingabefeld (+ optional Auto-Send)
  - Kif-Block "🎙️" → Klassentexte-Eingabe
- Aufnahme via `MediaRecorder` (webm/ogg), Stille-Erkennung über AudioContext-Analyser (auto-stop nach 800ms Stille)

**Backend (mission_control_api.py):**
- `/api/transcribe` → `transcribe_audio()`
- ffmpeg konvertiert webm/ogg → 16kHz mono WAV
- faster-whisper `large-v3` CUDA float16, Fallback CPU int8
- Debug-Kopie nach `/tmp/debug_voice.wav` für Nachanalyse

## TTS (Bolla spricht Antwort)

- Frontend → `/api/bolla/tts` (Backend)
- Backend ruft Azure TTS API (Server-Side, nicht Browser) → kein F-Secure-Block weil nicht durch Browser-Extension
- Audio kommt als Blob zurück, Browser spielt ab

## F-Secure-Kontext

Memory [[fsecure_recherche]]: F-Secure blockt `speech.platform.bing.com` WebSocket (Web Speech API in Browser). Frühere Web-Speech-Implementierung wäre davon betroffen — aktuelle Whisper-Lösung ist davon **nicht** betroffen, da:
- Mic-Audio geht direkt zu lokalem 127.0.0.1:18790 (gewhitelisted)
- TTS-Call geht Server-Side raus, nicht durch Browser-Extension

## Optimierungen 2026-05-18

**Korrektur nach Live-Test (Chris hatte Halluzination in mmc):**
- `beam_size=5` — kostet nur ~160ms ggü. beam=1, aber deutlich robuster gegen Halluzinationen (Bench mit Warmup-Run)
- `vad_filter=True` mit `min_silence_duration_ms=600` (zuvor 400 — zu aggressiv, konnte Wörter abschneiden)
- `no_speech_threshold=0.7` (zuvor 0.6) — strikter gegen Halluzinationen bei Hintergrundgeräusch
- `initial_prompt="Sprachnotiz auf Deutsch."` — Bias-Hilfe für Whisper
- Latenz-Logging: `t_ffmpeg`, `t_total`, `rtf` (real-time factor) in Server-Log

## Wichtige Lesson: Whisper-Footprint

Whisper large-v3 CUDA float16 frisst ~3 GB RAM wenn das Modell geladen ist. Watchdogs die RAM überwachen müssen das berücksichtigen → mc_watchdog.sh Schwelle ist auf **4500 MB** gesetzt. **Niemals unter 4 GB ansetzen** sonst killt der Watchdog den MC-Server im Loop, jedes Mal verliert man die Warmup-Zeit (5–30s) → Sprachnotiz fühlt sich katastrophal langsam an.

## P20-Sprachnotiz: gelöst über Gboard-Cloud-STT, NICHT über Whisper-Modellwechsel (20.05.2026)

**Entscheidung:** Lokale Whisper-Modelle (distil-large-v3, turbo, medium) für die P20-Notiz **NICHT mehr verfolgen.** Beweis: Win+H (Azure-Cloud-STT, Windows-Mic) erkennt ~100%, mmc-Whisper auf P20-Mic ~10%. Der Unterschied ist Mic+Engine zugleich — das P20-Mic (-37 dB, dumpf) ist die harte Grenze, kein lokales Modell rettet das.

**Anforderung (präzisiert):** Nur P20 unterwegs, nur SPRECHEN (kein Tippen — dafür gclip). Whisper-Test: ~90% Genauigkeit, aber Audio-Upload 91 KB = 7 Sek (Roundtrip über Cloudflare-Tunnel) → zu langsam.

**Lösung (final):** Notiz-Seite in `mobile.html` (#p-notiz) nutzt **Live-Spracherkennung via Web Speech API** (`webkitSpeechRecognition`, Funktion `toggleSpeech()`): großer 🎤-Knopf → live-Erkennung über Google-Cloud → Text sofort in `#notiz-input`, KEIN Audio-Upload, keine 7-Sek-Latenz, ~100%. Web Speech braucht HTTPS (✓) + Mic-Permission. F-Secure-Block (`speech.platform.bing.com`) gilt NUR auf Windows — P20 (Android) nicht betroffen. Whisper-Aufnahme nur noch kleiner **Fallback** unten, füllt dasselbe Feld. Buttons Telegram/Speichern/Clipboard lesen `notiz-input.value`.

**Generelle Lesson:** Bei nicht-perfektem Mic schlägt Cloud-/OS-Spracherkennung (Azure/Google) lokales Whisper deutlich. Erst Mic+Engine-Confounder isolieren, bevor man am Modell schraubt.

## Optionale weitere Schritte (nur für Windows-Mic-Pfad relevant, NICHT P20)

1. **`distil-large-v3` statt `large-v3`** — ~3× schneller, ~95% Qualität. ~1.5 GB. Nur sinnvoll wenn Latenz am Studio stört, nicht für Erkennungsqualität am Handy.
2. **Streaming-Transkription** — komplexes Frontend-Refactoring (WebSocket statt POST).

## Debug

- `/tmp/debug_voice.wav` — letzte Aufnahme (zur Inspektion)
- MC-Log: `grep -E "transcribe|whisper|seg" /home/bolla/workspace/logs/mission_control_api.log`
- Live-Test im Browser: 🎤-Button in Bolla-Chat oder Sprachnotiz, dann Server-Log checken
