#!/usr/bin/env python3
"""
SOUL.md Watcher — loggt jede Änderung der Datei mit Zeitstempel
und Snapshot der laufenden Prozesse, damit wir herausfinden, wer sie anfasst.
Wird per Cron alle 2 Minuten aufgerufen.
"""
import os
import subprocess
import time
from pathlib import Path

TARGET = Path("/home/bolla/workspace/SOUL.md")
STATE = Path("/home/bolla/workspace/logs/soul_watcher.state")
LOG = Path("/home/bolla/workspace/logs/soul_watcher.log")


def current_mtime() -> float:
    try:
        return TARGET.stat().st_mtime
    except FileNotFoundError:
        return 0.0


def last_seen_mtime() -> float:
    if STATE.exists():
        try:
            return float(STATE.read_text().strip())
        except ValueError:
            return 0.0
    return 0.0


def snapshot_processes() -> str:
    try:
        out = subprocess.run(
            ["ps", "-eo", "pid,ppid,etime,user,cmd", "--sort=-etime"],
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout
    except Exception as e:
        return f"<ps failed: {e}>"


def main() -> None:
    now = current_mtime()
    last = last_seen_mtime()
    if now == last:
        return

    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    mtime_human = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)) if now else "<missing>"
    procs = snapshot_processes()

    with LOG.open("a") as f:
        f.write(f"\n===== {ts} — SOUL.md mtime changed =====\n")
        f.write(f"new mtime: {mtime_human}  (epoch {now})\n")
        f.write(f"prev mtime epoch: {last}\n")
        f.write("--- ps snapshot ---\n")
        f.write(procs)
        f.write("--- end snapshot ---\n")

    STATE.write_text(str(now))


if __name__ == "__main__":
    main()
