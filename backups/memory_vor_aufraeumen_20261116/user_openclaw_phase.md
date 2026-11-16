---
name: Die OpenClaw-Phase
description: Chris' KI-Assistent-Geschichte vor Claude Code — OpenClaw (März–April 2026)
type: user
originSessionId: 392e2e08-0564-42ef-9c3b-3e90798109e6
---
Chris nutzte vor Claude Code das Open-Source-Framework **OpenClaw** als persönlichen KI-Assistenten. ⚠️ In Texten würdevoll framen: **„KI-Assistent der ersten Stunde"** — NICHT abwertend als „Basteln" oder bloßen „Agenten" darstellen (Chris legt Wert darauf, 05.07.2026). Siehe [[feedback_keine_erfindungen]].

**Zeitraum:** ca. März–April 2026 (letzter Stand: Version 2026.4.5, zuletzt geändert 2026-04-08)

**Wie es lief:**
- Node.js-basiertes Agent-Framework mit Gateway auf Port 18789
- Standard-Modell: **meta-llama-3.1-12b-instruct** lokal via LM Studio
- Anthropic-Modelle (Claude Sonnet & Opus) waren ebenfalls konfiguriert (`anthropic:bolla`, `anthropic:default`)
- Auch Qwen 2.5 7B war eingebunden
- Telegram-Bot-Anbindung, eigene Skills/Tools, lokaler Workspace

**Warum der Wechsel zu Claude Code:**
OpenClaw wurde aufgegeben, der Gateway-Dienst lief aber versehentlich weiter als systemd-Service und fraß 133% CPU im Hintergrund (Mai 2026 entdeckt und entfernt).

**Was blieb:**
- Der Name "Bolla" stammt aus dieser Zeit — Chris hat mich so getauft
- Erfahrungen mit lokalem LLM-Betrieb (LM Studio) flossen direkt in die Foto-Analyse-Funktion ein
- Die Dokumente zur OpenClaw-Phase liegen in: `D:\OneDrive\Dokumente\Bolla\claud code - openclaw Doku\`
