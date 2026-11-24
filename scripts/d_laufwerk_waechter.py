#!/usr/bin/env python3
"""Waechter fuer das D:-Laufwerk in WSL (24.11.2026): prueft alle 5 Min, ob /mnt/d lesbar ist; wenn nicht,
haengt es neu ein (wsl.exe -u root: umount -l + mount drvfs) und meldet NUR bei Ausfall/Reparatur in den MP-Jobs.
Hintergrund: nach Standby/Abkoppeln wird die 9p-Verbindung nach D: manchmal 'No such device' (Kurstag-5-Cron 24.11. lief ins Leere)."""
import fcntl, os, subprocess, sys, time, datetime
sys.path.insert(0, "/home/bolla/workspace/scripts")
LOG = "/home/bolla/workspace/logs/d_laufwerk_waechter.log"
PROBE = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts"
WSL = "/mnt/c/Windows/System32/wsl.exe"
lock = open("/tmp/d_waechter.lock", "w")
try:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except OSError:
    sys.exit(0)

def log(m):
    open(LOG, "a").write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {m}\n")

def ok():
    try:
        return subprocess.run(["ls", PROBE], capture_output=True, timeout=25).returncode == 0
    except Exception:
        return False

def meld(t):
    try:
        from job_status import mc_meldung
        mc_meldung("d-laufwerk-waechter", "D:-Laufwerk Wächter", t)
    except Exception as e:
        log(f"Meldung fehlgeschlagen {e!r}")

if ok():
    sys.exit(0)
log("D: NICHT lesbar - hänge neu ein")
for versuch in (1, 2, 3):
    try:
        subprocess.run([WSL, "-u", "root", "--", "sh", "-c",
                        "umount -l /mnt/d; mount -t drvfs D: /mnt/d -o uid=1000,gid=1000,noatime"],
                       capture_output=True, timeout=60)
    except Exception as e:
        log(f"Remount-Fehler {e!r}")
    time.sleep(3)
    if ok():
        log(f"Remount OK (Versuch {versuch})")
        meld(f"⚠️→✅ D: war nicht lesbar und wurde automatisch neu eingehängt (Versuch {versuch}).")
        sys.exit(0)
log("Remount FEHLGESCHLAGEN")
meld("❌ D: nicht lesbar, automatischer Remount fehlgeschlagen (3 Versuche) – Kurstag-/Song-Jobs gefährdet.")
sys.exit(1)
