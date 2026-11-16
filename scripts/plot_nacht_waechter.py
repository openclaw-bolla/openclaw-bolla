#!/usr/bin/env python3
"""Waechter fuer den AURORA-II-Plot-Nachtlauf (16.11.2026, Chris abwesend).
Problem: MP-Quota war wegen Anthropic-429 veraltet -> der Lauf-Gate haette zu spaet gebremst.
Ablauf: Notbremse /tmp/aurora_samstag_stop haelt den Lauf NACH Schritt b1 an. Dieser Waechter loescht die Bremse
(nur, wenn sie noch UNVERAENDERT von mir stammt) und startet plot_nacht.py neu, sobald
  (a) MP-Quota wieder frisch ist (stale=False), ODER
  (b) der 5h-Reset durch ist (ab 23:52, Chris-Screenshot: Sitzung wird um 23:50 zurueckgesetzt).
Meldungen NUR mit Verbrauchs-/Statuszahlen in MP-Jobs (Chris will nicht gespoilert werden). Nie Telegram.
Ende: alle Schritte fertig (_done_b4) oder Frist 05:30 vorbei."""
import datetime as dt, json, os, subprocess, sys, time, urllib.request

W = "/home/bolla/workspace"
OUT = f"{W}/scratch/plot_umbau"
STOP = "/tmp/aurora_samstag_stop"
LOG = f"{W}/logs/plot_nacht_waechter.log"
JOB = "plot-nacht"
TITEL = "🌙 AURORA II Plot-Nachtlauf"
DEADLINE = dt.datetime(2026, 11, 17, 5, 30)
RESET = dt.datetime(2026, 11, 16, 23, 52)
sys.path.insert(0, f"{W}/scripts")


def log(m):
    open(LOG, "a").write(f"[{dt.datetime.now():%d.%m. %H:%M:%S}] {m}\n")


def melde(text, status=None):
    try:
        from job_status import mc_meldung
        mc_meldung(JOB, TITEL, text, status)
    except Exception as e:
        log(f"Meldung fehlgeschlagen: {e!r}")


def laeuft():
    return subprocess.run(["pgrep", "-f", r"scripts/plot_nacht\.py"], capture_output=True).returncode == 0


def mp_frisch():
    try:
        d = json.load(urllib.request.urlopen("http://127.0.0.1:18790/api/claudequota", timeout=5))
        return (not d.get("stale")) and "error" not in d, d
    except Exception:
        return False, {}


def fertig(n):
    return os.path.exists(f"{OUT}/_done_{n}")


def start():
    lg = open(f"{W}/logs/plot_nacht.log", "a")
    subprocess.Popen(["/usr/bin/python3", "scripts/plot_nacht.py"], cwd=W, stdout=lg, stderr=lg, start_new_session=True)
    log("plot_nacht.py gestartet")


def main():
    mt0 = os.path.getmtime(STOP) if os.path.exists(STOP) else None
    log(f"Waechter gestartet (Bremse mtime {mt0})")
    gemeldet_b1 = False
    letzter_start = 0
    while True:
        now = dt.datetime.now()
        if fertig("b4"):
            melde("✅ Alle 4 Schritte (Twist, Gegenprüfung, Änderungsplan, Briefings) sind fertig. Ergebnisse liegen in scratch/plot_umbau/ (bewusst nicht angezeigt, kein Spoiler).", "ok")
            log("alles fertig"); return
        if now >= DEADLINE:
            n = sum(fertig(x) for x in ("b1", "b2", "b3", "b4"))
            melde(f"⚠️ Frist 05:30 erreicht, {n} von 4 Schritten fertig. Rest braucht einen neuen Start (sag „plot weiter“).", "aktion")
            log("Frist"); return
        if fertig("b1") and not gemeldet_b1:
            melde("Schritt 1 von 4 (Twist) fertig. Lauf wartet auf frische Quota-Zahlen bzw. den 5h-Reset (23:50), dann weiter.", "ok")
            gemeldet_b1 = True
        if not laeuft():
            frisch, d = mp_frisch()
            if os.path.exists(STOP):
                # nur meine eigene Bremse loesen, nie eine spaeter von Chris gesetzte
                if mt0 is not None and os.path.getmtime(STOP) == mt0 and (frisch or now >= RESET):
                    os.remove(STOP)
                    grund = f"MP frisch (5h {d.get('five_hour_pct')} %, Woche {d.get('seven_day_pct')} %)" if frisch else "5h-Reset 23:50 durch"
                    melde(f"Lauf geht weiter mit Schritt 2: {grund}.", "ok"); log(f"Bremse geloest: {grund}")
                    start(); letzter_start = time.time()
                elif mt0 is not None and os.path.getmtime(STOP) != mt0:
                    log("Bremse wurde von aussen neu gesetzt -> Waechter beendet sich"); return
            elif time.time() - letzter_start > 1800:
                # Lauf endete (z. B. Limit mitten im Schritt), keine Bremse: nach 30 Min neu versuchen
                log("Lauf nicht aktiv, kein b4 -> Neustart"); start(); letzter_start = time.time()
        time.sleep(30)


if __name__ == "__main__":
    main()
