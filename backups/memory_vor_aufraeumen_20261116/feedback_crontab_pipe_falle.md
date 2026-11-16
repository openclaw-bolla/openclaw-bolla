---
name: feedback-crontab-pipe-falle
description: NIE crontab über eine Pipe bearbeiten, deren Fehler die ganze Crontab leeren kann
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
---

⚠️ **`crontab -l | <filter> | crontab -` ist gefährlich:** Schlägt der Filter mitten in der Pipe fehl (z.B. `sed` mit kaputtem Delimiter/Regex), kommt **leerer stdout** bei `crontab -` an → die **komplette Crontab wird gelöscht**. Genau das passierte am 24.06.2026: ein `sed 's#...#...#'` mit `#`-Delimiter UND `#`-Kommentar im Cron-Eintrag → „unknown option to `s'" → 0 Zeilen Crontab. Alle ~45 Jobs (MC-Server, Telegram-Bot, Cloudflared, Backups, Watchdogs) weg.

**Why:** `crontab -` ersetzt bedingungslos durch das, was reinkommt — auch wenn das nichts ist. Eine fehlgeschlagene Pipe-Stufe gibt nichts aus, der Fehler-Exit-Code wird von der Pipe verschluckt.

**How to apply — Crontab IMMER über eine Datei + Verifikation ändern:**
1. `crontab -l > /tmp/.../cur.txt` (Snapshot)
2. Datei mit Edit-Tool / grep -v / cat >> bearbeiten — **kein** sed-in-der-Pipe
3. Vor dem Installieren prüfen: `grep -c` Zeilenzahl plausibel? Kritische Jobs (`start_mc_server`, `telegram_bot.py`, `cloudflared`, `nacht_backup`, `mc_watchdog`) noch drin?
4. `crontab datei.txt` (aus Datei, nicht aus Pipe)
5. Danach `diff` gegen vorher + frisches Backup ziehen.

**⚠️ Pfadlängen-Bug (22.07.2026):** `crontab <pfad>` bricht mit „No such file or directory" ab, wenn der Pfad zu lang ist (~100+ Zeichen, z.B. voller Scratchpad-Pfad) — die Fehlermeldung zeigt einen sichtbar abgeschnittenen Dateinamen. Datei existiert wirklich, `crontab` truncatet nur intern. **Fix:** Datei vorher nach `/tmp/crontab_new.txt` (kurzer Pfad) kopieren, von dort installieren, danach löschen.

**Rettung wenn's doch passiert:** Backup liegt in `/mnt/d/OneDrive/Dokumente/Bolla/backups/crontab-latest.txt` (vom `weekly_backup.sh`, So 17:00 — also evtl. ein paar Tage alt). Seither dazugekommene Jobs aus der Session/`state/capabilities_snapshot.json` (Cron-Liste vom letzten `capabilities_drift.py`-Lauf) rekonstruieren. Verwandte Eigentor-Lehre: [[aktuell]] (pkill matcht eigene Shell).
