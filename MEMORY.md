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

## Outlook Kontakte (verbunden 23.03.2026)
- 145 Kontakte in ernstmandel@outlook.de
- Zugang über Microsoft Graph (Contacts.Read)
- Kann: Kontakte suchen, Geburtstage abfragen, Namen/Nummern nachschlagen
- Bekannte Kontakte: Familie Mandel (Dominik, Florian, Katharina, Ann-Kristin), Ewaldss, Ebingers, Fuß, Meichsner...
- Heute Geburtstag (23.03.): Herr Georg Ewald (Jg. 1963)

## E-Mail Setup (19.03.2026)
- Konto: ernstmandel@outlook.de (privates Microsoft/Outlook-Konto)
- Methode: Microsoft Graph API via OAuth (Device Flow)
- Client ID: 9e5f94bc-e8a4-4e73-b8be-63364c29d753
- Token gespeichert: `/home/bolla/.openclaw/workspace/config/ms_token.json`
- Kann Mails lesen (IMAP) und senden (SMTP via Graph)
- Hinweis: Token läuft irgendwann ab → dann neuen Device Flow starten
- Skripte: config/email.json enthält Kontodaten

## Token Watcher (eingerichtet 22.03.2026, verbessert 23.03.2026)
- Script: `/home/bolla/.openclaw/workspace/scripts/token_watcher.py`
- Prüft alle **15 Minuten** Mails von robinmandel@outlook.de auf Anthropic-Token
- Aktualisiert ALLE anthropic-Profile (bolla + default), sortiert Mails nach Datum (neuester Token gewinnt)
- Startet Gateway neu, löscht Mail
- Autostart via VBS: `start_token_watcher.vbs` im Windows-Startup-Ordner
- Task Scheduler: `\OpenClaw\TokenWatcher` (bei Login) + `\OpenClaw\TokenWatcherHourly` (stündlich als Wächter)
- **WICHTIG: Ich darf KEINEN Token manuell in JSON-Dateien eintragen!**
- Log: `/home/bolla/.openclaw/workspace/logs/token_watcher.log`

## Autostart (eingerichtet 23.03.2026, perfektioniert 23.03.2026 Abend)
- **Gateway:** `start_openclaw_gateway.vbs` im Windows-Startup-Ordner
- **WICHTIG:** VBS muss erst `wsl echo` ausführen (True = warten), dann 15 Sekunden schlafen, DANN Gateway starten — sonst ist WSL noch nicht bereit!
- **PATH** muss hartcodiert sein: `/usr/local/bin:/usr/bin:/bin:/home/bolla/.npm-global/bin` — kein `$PATH` in VBS (wird von Windows leer interpretiert)
- PowerShell läuft NICHT im Hintergrund — WSL startet unsichtbar direkt
- **Token Watcher:** VBS + Task Scheduler stündlich als Wächter
- Chris muss nach Neustart nichts mehr manuell starten
- Bei Windows-Update-Neustart kann es minimal länger dauern (~20 Sek nach Login)

## GitHub Backup (eingerichtet 23.03.2026)
- Repo: https://github.com/openclaw-bolla/openclaw-bolla (privat)
- Enthält: Workspace, Scripts, Memory, Config (OHNE Secrets)
- Wiederherstellungsanleitung: `openclaw-wiederherstellung.pdf` im Workspace
- Push nach wichtigen Änderungen (manuell durch Bolla)

## Telegram (eingerichtet 23.03.2026)
- Bot: @bolla_mandel_bot
- Bot Token: 8114115093:AAFvRoF_xnhshKM92bMdcwZ3DBCCe4KpwxQ
- Chris Telegram ID: 8772213652
- dmPolicy: pairing (bereits genehmigt)
- Chris kann Bolla direkt über Telegram erreichen

## Technisches
- Python 3.12 (WSL2), msal installiert (--user --break-system-packages)
- pip installiert via get-pip.py
- Edge: `/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`
- openclaw liegt unter: /home/bolla/.npm-global/bin/openclaw (PATH muss explizit gesetzt werden in VBS/Scripts)
