#!/usr/bin/env python3
"""WSL-Speicher-Wächter — Frühwarnung + Sofort-Aufräumen vor dem naechsten vmmem-Freeze.

Hintergrund: 23.07.2026 kompletter PC-Freeze mitten in itslearning-Playwright-Arbeit,
~30 Min Reparatur noetig (siehe reference_wsl.md). .wslconfig-Limit ist jetzt 6GB/2GB
Swap gedeckelt, aber ein Wächter der VOR dem Anschlag warnt und eindeutig verwaiste
Chromium-Prozesse (PPID=1, d.h. das Elternskript ist schon tot) selbst aufräumt, ist
die zusätzliche Sicherung.

Läuft alle 2 Min per Cron. Sendet Telegram-Alarm nur beim ÜBERSCHREITEN einer Schwelle
(kein Dauerspam), Status in state/wsl_memory_watchdog.json.
"""
import json
import subprocess
import time
from pathlib import Path

WORKSPACE = Path("/home/bolla/workspace")
STATE_FILE = WORKSPACE / "state/wsl_memory_watchdog.json"
LOG_FILE = WORKSPACE / "logs/wsl_memory_watchdog.log"

WSLCONFIG_MEM_MB = 6144  # muss zu memory=6GB in C:\Users\ernst\.wslconfig passen
WARN_PCT = 75
CRITICAL_PCT = 88  # killt nur eindeutige Waisen (PPID=1), warnt
EMERGENCY_PCT = 94  # killt ALLE Chromium/Playwright-Prozesse, auch lebende — letzte Bremse vorm Freeze


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def read_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"last_level": "ok"}


def write_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def mem_used_pct():
    out = subprocess.run(["free", "-m"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("Mem:"):
            parts = line.split()
            total, available = int(parts[1]), int(parts[6])
            used = total - available
            return round(used / WSLCONFIG_MEM_MB * 100, 1), used, total
    return 0, 0, 0


def top_processes(n=5):
    out = subprocess.run(
        ["ps", "-eo", "pid,ppid,rss,comm", "--sort=-rss"],
        capture_output=True, text=True
    ).stdout.splitlines()[1:n + 1]
    lines = []
    for l in out:
        parts = l.split(None, 3)
        if len(parts) == 4:
            pid, ppid, rss, comm = parts
            lines.append(f"{comm} (PID {pid}, {int(rss) // 1024}MB)")
    return lines


def _chromium_processes():
    out = subprocess.run(
        ["ps", "-eo", "pid,ppid,comm"], capture_output=True, text=True
    ).stdout.splitlines()[1:]
    procs = []
    for l in out:
        parts = l.split(None, 2)
        if len(parts) != 3:
            continue
        pid, ppid, comm = parts
        if "chrome" in comm.lower() or "chromium" in comm.lower():
            procs.append((pid, ppid, comm))
    return procs


def kill_orphaned_chromium():
    """Killt nur Chromium/Playwright-Prozesse deren Elternprozess bereits tot ist (PPID=1) —
    das ist eindeutig ein Waisenprozess von einem abgestürzten Skript, kein laufender Job."""
    killed = []
    for pid, ppid, comm in _chromium_processes():
        if ppid == "1":
            subprocess.run(["kill", "-9", pid], check=False)
            killed.append(f"{comm}(PID {pid})")
    return killed


def kill_all_chromium():
    """Letzte Bremse vor dem Freeze: killt ALLE Chromium/Playwright-Prozesse, auch lebende —
    also auch mitten in einer laufenden Aktion. Ein abgebrochenes Skript ist billiger als ein
    weiterer 30-Min-WSL-Reparatur-Vorfall wie am 23.07.2026."""
    killed = []
    for pid, ppid, comm in _chromium_processes():
        subprocess.run(["kill", "-9", pid], check=False)
        killed.append(f"{comm}(PID {pid}, PPID {ppid})")
    return killed


def telegram(msg):
    try:
        cfg = json.loads((WORKSPACE / "config/telegram_bot.json").read_text())
        import requests
        requests.post(
            f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage",
            json={"chat_id": cfg["chris_id"], "text": msg, "parse_mode": "HTML"},
            timeout=10,
        )
    except Exception as e:
        log(f"Telegram-Versand fehlgeschlagen: {e}")


def main():
    pct, used, total = mem_used_pct()
    state = read_state()
    prev_level = state.get("last_level", "ok")

    if pct >= EMERGENCY_PCT:
        level = "emergency"
    elif pct >= CRITICAL_PCT:
        level = "critical"
    elif pct >= WARN_PCT:
        level = "warn"
    else:
        level = "ok"

    if level == "emergency":
        killed = kill_all_chromium()
        top = top_processes()
        log(f"NOTBREMSE {pct}% ({used}/{total}MB) — ALLE Chromium-Prozesse gekillt: {killed}")
        if prev_level != "emergency":
            msg = (
                f"🆘 <b>WSL-Notbremse bei {pct}%</b> ({used}/{total}MB)\n"
                f"Alle Chromium/Playwright-Prozesse beendet, auch laufende — ein Skript ist ggf. "
                f"gerade mitten in einer Aktion abgebrochen (z.B. itslearning-Upload).\n"
                + (f"Beendet: {', '.join(killed)}\n" if killed else "")
                + "Top-Verbraucher:\n" + "\n".join(top)
            )
            telegram(msg)
    elif level == "critical":
        killed = kill_orphaned_chromium()
        top = top_processes()
        if killed:
            log(f"KRITISCH {pct}% ({used}/{total}MB) — verwaiste Prozesse gekillt: {killed}")
        else:
            log(f"KRITISCH {pct}% ({used}/{total}MB) — keine Waisenprozesse gefunden. Top: {top}")
        if prev_level not in ("critical", "emergency"):
            msg = (
                f"🚨 <b>WSL-Speicher kritisch: {pct}%</b> ({used}/{total}MB)\n"
                + (f"Verwaiste Chromium-Prozesse gekillt: {', '.join(killed)}\n" if killed else "")
                + f"Top-Verbraucher:\n" + "\n".join(top)
                + f"\n\nBei ≥{EMERGENCY_PCT}% killt der Wächter notfalls auch laufende Prozesse."
            )
            telegram(msg)
    elif level == "warn":
        log(f"Warnung {pct}% ({used}/{total}MB)")
        if prev_level == "ok":
            telegram(f"⚠️ WSL-Speicher bei {pct}% ({used}/{total}MB) — im Blick behalten.")
    else:
        if prev_level != "ok":
            log(f"Entwarnung — wieder bei {pct}%")
            telegram(f"✅ WSL-Speicher wieder normal ({pct}%).")

    state["last_level"] = level
    state["last_pct"] = pct
    state["last_check"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    write_state(state)


if __name__ == "__main__":
    main()
