# MEMORY.md - Langzeitgedächtnis

## Über Chris
- Name: Chris
- Surface Laptop, Windows + WSL2
- Timezone: Europe/Berlin
- Doktorand an der Uni Ulm
- Erstkontakt: 18.03.2026

## Familie
- **Robin Mandel** — Sohn von Chris
  - E-Mail: robinmandel@outlook.de
  - Studiert Medizin in Ulm, 10. Semester

## E-Mail Setup (19.03.2026)
- Konto: ernstmandel@outlook.de (privates Microsoft/Outlook-Konto)
- Methode: Microsoft Graph API via OAuth (Device Flow)
- Client ID: 9e5f94bc-e8a4-4e73-b8be-63364c29d753
- Token gespeichert: `/home/bolla/.openclaw/workspace/config/ms_token.json`
- Kann Mails lesen (IMAP) und senden (SMTP via Graph)
- Hinweis: Token läuft irgendwann ab → dann neuen Device Flow starten
- Skripte: config/email.json enthält Kontodaten

## Token Watcher (eingerichtet 22.03.2026)
- Script: `/home/bolla/.openclaw/workspace/scripts/token_watcher.py`
- Prüft stündlich Mails von robinmandel@outlook.de auf Anthropic-Token
- Trägt Token in auth-profiles.json ein, startet Gateway neu, löscht Mail
- Autostart via VBS: `C:\Users\ernst\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start_token_watcher.vbs`
- **WICHTIG: Ich darf KEINEN Token manuell in JSON-Dateien eintragen!** (war mal ein Problem)
- Log: `/home/bolla/.openclaw/workspace/logs/token_watcher.log`

## Technisches
- Python 3.12 (WSL2), msal installiert (--user --break-system-packages)
- pip installiert via get-pip.py
- Edge: `/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`
