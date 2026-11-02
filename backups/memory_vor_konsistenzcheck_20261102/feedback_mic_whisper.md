---
name: feedback-mic-whisper
description: Mic im Bolla Chat nutzt Azure Speech SDK (seit 27.05.2026) — Whisper und Web Speech API sind keine Option mehr
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e7c5cd24-7705-4855-82d9-31abaf36ffab
---

**GELÖST 27.05.2026:** Mic in MC nutzt jetzt **Azure Speech SDK** (microsoft-cognitiveservices-speech-sdk via CDN). Funktioniert sofort auf Book und Studio. Key in `config/azure_speech.json` (Region: westeurope).

**Was NICHT verwenden / nicht vorschlagen:**
- Whisper / `/api/transcribe` — dreimal abgelehnt
- Web Speech API (Google) — gibt auf beiden Rechnern "network"-Fehler, Ursache nie vollständig geklärt
- Windows "Online-Spracherkennung" prüfen — war schon AN
- F-Secure / WISO deinstallieren — hat nichts gebracht

**Why:** Web Speech API (Chromium) ist fest auf Google verdrahtet. Azure ist zuverlässiger und bereits konfiguriert.

**How to apply:** Bei Mic-Problemen → Azure Speech SDK. Nicht zurück zu Web Speech API. Nicht Whisper.
