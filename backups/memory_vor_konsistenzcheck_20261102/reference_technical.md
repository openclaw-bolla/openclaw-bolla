---
name: Technisches Setup und Referenzen
description: E-Mail, Token, Autostart, GitHub und technische Infrastruktur aus OpenClaw-Zeiten
type: reference
originSessionId: 0624e501-3f9d-46a0-ac81-c93cf602fcb5
---
## E-Mail Setup
- Outlook: ernstmandel@outlook.de via Microsoft Graph API (OAuth Device Flow)
  - Client ID: 9e5f94bc-e8a4-4e73-b8be-63364c29d753
- Gmail: chrismandel13@gmail.com (Google OAuth verbunden)
  - Client ID: 527008391551-96d1bmosa19oqm26e8hj59rd7j73sv47.apps.googleusercontent.com
- wtnet: chrismandel@wtnet.de (IMAP/SMTP: mail.wtnet.de, 993/587)
- 145 Outlook-Kontakte, synchronisiert mit Gmail

## OpenClaw-Infrastruktur (historisch)
- GitHub Backup: https://github.com/openclaw-bolla/openclaw-bolla (privat)
- Wiederherstellungsanleitung: openclaw-wiederherstellung.pdf im Workspace
- Token Watcher: scripts/token_watcher.py (prüft Mails von Robin auf Anthropic-Token)
- Autostart: VBS-Scripts im Windows-Startup + Task Scheduler
- Gateway: openclaw-launcher.sh als portabler Mittelsmann
- Telegram Bot: @bolla_mandel_bot (Chris' Telegram ID: 8772213652)
- Telegram Gruppe "Robin, Papa & Jarvis & Bolla": Chat-ID -5107085680

## SSH-Zugang zu Book und Pro (WICHTIG — nie wieder vergessen!)
- **Surface Book** → Reverse SSH Tunnel auf Port **2222** (localhost), User **ernst@localhost**
  - `ssh -p 2222 -i /home/bolla/.ssh/id_ed25519 ernst@localhost`
  - PowerShell via EncodedCommand (base64 utf-16-le), da Windows-SSH (nicht WSL2)
- **Surface Pro** → Reverse SSH Tunnel auf Port **2223** (localhost), User **ernst@localhost**
- Tunnel läuft über `book_tunnel_watchdog.sh` (cron alle 2 min) + MC-Button "SSH-Tunnel neu starten"
- MC-Seite "Surface Book" zeigt Book-Daten live → Tunnel ist aktiv wenn diese Daten erscheinen
- Früher erfolgreich genutzt für Akku-Diagnose (Session ca. April/Mai 2026)
- **NICHT** 192.168.178.29:2200 — das ist Loopback zurück zum Studio!
- **NICHT** Tailscale — Book ist dort nicht eingetragen
- Python-Funktion im MC-Server: `get_book_health()` in `mission_control_api.py` zeigt das Pattern

## Azure Speech Services
- Config: `/home/bolla/workspace/config/azure_speech.json` (chmod 600, NIE commiten)
- Key + Region `westeurope` + Default Voice `de-DE-SeraphinaMultilingualNeural`
- Genutzt für: TTS (Bolla-Stimme) + STT (Mic in MC) — beide über denselben Key
- API-Endpunkt im MC-Server: `/api/speech/config` (gibt Key+Region an Browser)
- MC-Mic nutzt Azure Speech SDK (jsdelivr CDN), NICHT mehr Web Speech API / Google

## Technisch
- Python 3.12 (WSL2)
- Edge: /mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe
- Node via nvm: v20.20.2
- **Desktop liegt in OneDrive:** `D:\OneDrive\Desktop` (nicht C:\Users\ernst\Desktop)
- **Bilder/Pictures liegt in OneDrive:** `D:\OneDrive\Bilder` (nicht C:\Users\ernst\Pictures)
- Shortcuts/Dateien für Desktop immer nach `/mnt/d/OneDrive/Desktop/` schreiben
- Allgemein: Windows-Standardordner (Desktop, Bilder, Dokumente etc.) sind zu OneDrive umgeleitet

## Offene Todos (aus OpenClaw)
- Outlook -> Gmail Kontakte sync (inkl. Bilder) — wenn zuhause am PC
- OpenClaw Companion App auf Handy einrichten
