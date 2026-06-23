# 🛟 Bolla Disaster-Recovery — Bolla auf einem neuen PC wiederherstellen

> Ziel: Aus den zwei Backups (GitHub + OneDrive) die komplette Umgebung so
> nachbauen, dass `https://bolla.chrismandel.de`, alle Crons, Tokens, das
> Gedächtnis und der Duo-Hotkey wieder genau wie vorher laufen.
> **Aufwand: ~1 Stunde, geführt.** Es ist kein Knopfdruck — manche Dinge
> (Login, Pakete) müssen bewusst neu gemacht werden.

## Die zwei Quellen
| Quelle | Was | Adresse |
|---|---|---|
| **GitHub** (privat) | `workspace/` ohne `config/` — Skripte, MP, Daten, `duoclip.sh` | `github.com/openclaw-bolla/openclaw-bolla` |
| **OneDrive** | Geheimnisse + Crons + Tunnel + Gedächtnis + System-Listen | `D:\OneDrive\Dokumente\Bolla\backups\` |

OneDrive-Backup-Struktur:
```
backups/
  config-latest/     workspace/config/  (alle Tokens/Keys)
  cloudflared/       Tunnel-Credentials (UUID.json, cert.pem, config.yml)
  crontab-latest.txt alle Cron-Jobs
  claude-code/       ~/.claude  (Memory, settings, CLAUDE.md, Login)
  ssh/               ~/.ssh  (id_ed25519 etc. — privat!)
  system/            pip-freeze.txt, apt-manual.txt, wsl.conf, dotfiles/, bin/
  windows-bolla/     AutoHotkey + duoclip.ahk/.vbs (Duo-Hotkey)
  history/           wöchentliche tar-Snapshots (Rollback)
```

---

## Schritt 0 — Windows-Grundlage
1. OneDrive installieren & einrichten (Konto ernstmandel@outlook.de), Sync abwarten.
2. WSL2 + Ubuntu installieren: `wsl --install -d Ubuntu`
3. In Ubuntu denselben Benutzer **`bolla`** anlegen (Home = `/home/bolla`).

## Schritt 1 — WSL-Basis & Pakete
```bash
# /etc/wsl.conf wiederherstellen (systemd, hwclock):
sudo cp "/mnt/d/OneDrive/Dokumente/Bolla/backups/system/wsl.conf" /etc/wsl.conf
# -> danach in PowerShell: wsl --shutdown , dann WSL neu öffnen

# apt-Pakete (Liste aus Backup; Kern: android-tools-adb ffmpeg openssh-server rsync python3-pip git):
sudo apt update
xargs -a "/mnt/d/OneDrive/Dokumente/Bolla/backups/system/apt-manual.txt" sudo apt install -y

# Python-Pakete:
pip install --break-system-packages -r "/mnt/d/OneDrive/Dokumente/Bolla/backups/system/pip-freeze.txt"
```

## Schritt 2 — workspace (GitHub)
```bash
cd /home/bolla
git clone https://github.com/openclaw-bolla/openclaw-bolla.git workspace
```

## Schritt 3 — Geheimnisse & Configs (OneDrive)
```bash
B="/mnt/d/OneDrive/Dokumente/Bolla/backups"
# config/ (Tokens) — in GitHub bewusst NICHT enthalten:
mkdir -p /home/bolla/workspace/config
rsync -rt "$B/config-latest/" /home/bolla/workspace/config/

# Cloudflare-Tunnel-Creds:
mkdir -p /home/bolla/.cloudflared && rsync -rt "$B/cloudflared/" /home/bolla/.cloudflared/
chmod 600 /home/bolla/.cloudflared/*

# SSH-Keys:
mkdir -p /home/bolla/.ssh && rsync -rt "$B/ssh/" /home/bolla/.ssh/
chmod 700 /home/bolla/.ssh && chmod 600 /home/bolla/.ssh/id_ed25519

# Dotfiles + ~/bin (BROWSER-Autoopen, PATH):
cp "$B/system/dotfiles/.bashrc" /home/bolla/.bashrc
[ -f "$B/system/dotfiles/.bash_aliases" ] && cp "$B/system/dotfiles/.bash_aliases" /home/bolla/.bashrc
mkdir -p /home/bolla/bin && rsync -rt "$B/system/bin/" /home/bolla/bin/ && chmod +x /home/bolla/bin/*
```

## Schritt 4 — cloudflared-Binary
```bash
mkdir -p /home/bolla/.local/bin
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
  -o /home/bolla/.local/bin/cloudflared && chmod +x /home/bolla/.local/bin/cloudflared
# Test: /home/bolla/.local/bin/cloudflared tunnel run bolla-mc
```
> Die DNS-Route (bolla.chrismandel.de → Tunnel) und Cloudflare-Access-Policy
> liegen **im Cloudflare-Account** und überleben von selbst. Nur falls der
> Account neu ist: Tunnel `bolla-mc` + CNAME + Access-Anwendung neu anlegen.

## Schritt 5 — Claude Code
```bash
# Claude Code CLI installieren (offizieller Installer / npm), dann:
rsync -rt "$B/claude-code/" /home/bolla/.claude/
# Memory, settings.json, CLAUDE.md sind damit zurück.
```
> **Login:** `.credentials.json` ist mitgesichert, aber Tokens laufen ab →
> i.d.R. einmal `claude` starten und neu einloggen (Browser-Magic-Link).

## Schritt 6 — Crontab (startet die ganze Maschinerie)
```bash
crontab "/mnt/d/OneDrive/Dokumente/Bolla/backups/crontab-latest.txt"
crontab -l | grep -c .   # Kontrolle: ~42 Zeilen
```
> Enthält die `@reboot`-Jobs: MC-Server (Port 18790), Telegram-Bot,
> cloudflared-Tunnel, ssh. Nach einem WSL-Neustart läuft alles automatisch hoch.
> Einmal testen: `bash /home/bolla/workspace/scripts/start_mc_server.sh` und
> `http://127.0.0.1:18790/` öffnen.

## Schritt 7 — Duo-Hotkey (Windows)
```powershell
# In Windows-PowerShell (nicht WSL):
powershell -ExecutionPolicy Bypass -File "\\wsl$\Ubuntu\home\bolla\workspace\windows\duo_hotkey_install.ps1"
```
Lädt AutoHotkey portabel, schreibt Launcher + Hotkey, legt Autostart an,
startet ihn. Danach ist **Win+Strg+S** wieder aktiv (rechte Duo-Seite → Zwischenablage).
Voraussetzung: am Duo „Kabelloses Debugging" an.

---

## ✅ Fertig-Check
- [ ] `http://127.0.0.1:18790/` öffnet sich (MC-Server)
- [ ] `https://bolla.chrismandel.de` erreichbar (Tunnel + Access-Login)
- [ ] `crontab -l` zeigt ~42 Jobs
- [ ] Telegram-Bot antwortet
- [ ] `claude` startet, Memory/aktuell.md ist da
- [ ] Win+Strg+S macht Duo-Screenshot
- [ ] SSH zu Book (:2222) / Pro (:2223) geht

## Was bewusst NICHT automatisch geht
- **Claude-Login** (Token abgelaufen → neu einloggen)
- **OAuth-Tokens** (Outlook/Google/Spotify) können ablaufen → ggf. neu autorisieren
- **WSL-Distro + sudo-Setup** (passwortloses `sudo service ssh start` für @reboot-Cron)
- **Cloudflare-Account-Seite** (nur falls der Account selbst weg ist)

_Backups laufen: GitHub nächtlich 0:15 (`nacht_backup.sh`), OneDrive So 17:00 (`weekly_backup.sh`)._
