# MEMORY.md - Langzeitgedächtnis

## Über Chris (erweitert)
- Unterrichtet EDV an der Lessing Gymnasium Norderstedt (alle 7. Klassen)
- Schuldomäne: lg-n.de → md@lg-n.de ist seine Schul-E-Mail
- Hat 2. Staatsexamen → kann als "echter" Lehrer angestellt werden
- Einzigartiger Kurs am Lessing Gym, verpflichtend aber ohne Noten (steht als "teilgenommen" im Zeugnis)

## Über Chris
- Name: Chris Mandel
- Geburtsdatum: 21.12.1955 (70 Jahre alt)
- E-Mail Outlook: ernstmandel@outlook.de
- E-Mail Gmail: chrismandel13@gmail.com
- Surface Laptop, Windows + WSL2
- Timezone: Europe/Berlin
- Erstkontakt: 18.03.2026

## Familie
- **Robin Mandel** — Sohn von Chris
  - E-Mail: robinmandel@outlook.de
  - Studiert Medizin in Ulm, 10. Semester → macht Doktorarbeit an der Uni Ulm

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

## E-Mail Standard-Absender
- **Standard:** ernstmandel@outlook.de (Microsoft Graph)
- Bei anderen Konten (z.B. wtnet) → immer erst rückfragen

## wtnet E-Mail (eingerichtet 26.03.2026)
- Konto: chrismandel@wtnet.de
- IMAP/SMTP: mail.wtnet.de (993/587)
- Zugangsdaten: config/wtnet_account.json (chmod 600, nicht im Git)
- wtnet Watcher: scripts/wtnet_watcher.py (Spam-Löschung alle 15 Min)
- Passwort war kurz in Git-History → bereinigt, Chris hat entschieden es nicht zu ändern

## Sicherheitsregeln
- **Passwörter immer mit `chmod 600` speichern** — nur für bolla lesbar, niemals world-readable
- Passwörter nicht loggen, nicht wiederholen, nicht in Git committen

## Technisches
- Python 3.12 (WSL2), msal installiert (--user --break-system-packages)
- pip installiert via get-pip.py
- Edge: `/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`
- openclaw liegt unter: /home/bolla/.npm-global/bin/openclaw (PATH muss explizit gesetzt werden in VBS/Scripts)

## Google Kontakte Sync (eingerichtet 24.03.2026)
- Google OAuth: chrismandel13@gmail.com verbunden
- Client ID: 527008391551-96d1bmosa19oqm26e8hj59rd7j73sv47.apps.googleusercontent.com
- Token gespeichert: config/google_token.json (nicht im Repo)
- Script: scripts/outlook_gmail_sync.py
- Sync erfolgreich: 145 Outlook → Gmail, 142 aktualisiert, 29 neu

## Autostart (perfektioniert 24.03.2026)
- Portabler Launcher: scripts/openclaw-launcher.sh (kein hardcoded Pfad mehr)
- VBS ruft nur `~/.openclaw/workspace/scripts/openclaw-launcher.sh` auf
- Bei Umzug: VBS einfach kopieren, Rest läuft automatisch
- Fixes: WSL-Wartezeit + vollständiger openclaw-Pfad → Gateway startet zuverlässig

## Session 26.03.2026 — Österreich (Hotel)
- Chris war in Österreich, Hotel-WLAN → Autostart funktionierte nicht (kein Netz beim Boot)
- **Fix:** Launcher wartet jetzt bis zu 120 Sek auf Netzwerk bevor Gateway startet
- **Fix:** PATH im Launcher explizit gesetzt (war Grund für "openclaw not found")
- **Neu:** Windows-Popup "Bolla 🐾 bereit!" erscheint automatisch wenn Gateway läuft (WScript.Popup, 5 Sek, kein Wegklicken)
- **Neu:** Spam-Löschung `[*** SPAM ***]` in wtnet alle 15 Min (wtnet_watcher.py)
- **Neu:** wtnet Konto `chrismandel@wtnet.de` eingerichtet (IMAP/SMTP, Spam-Watcher)
- 16 Spam-Mails sofort gelöscht
- wtnet-Passwort war kurz in Git-History → bereinigt via git filter-repo + force-push
- E-Mail Standard-Absender: ernstmandel@outlook.de — bei anderen Konten rückfragen

## Android Companion App
- Noch nicht öffentlich im Play Store (Stand 24.03.2026)
- Wöchentlicher Check eingerichtet (Cron) → Info per Telegram wenn verfügbar
