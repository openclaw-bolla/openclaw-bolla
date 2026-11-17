#!/usr/bin/env python3
"""Plot-Umbau AURORA II - Schritt B4 (Briefings fuer die Opus-Kapitelneufassung) mit OPUS statt Fable (17.11.2026).
Fable ist nicht mehr im Abo (verlangt Nutzungsguthaben). Tagesbetrieb: NORMALE Limit-Policy (kein Nacht-Override),
Gate ueber limit_gate (heavy=True). Inhalte bleiben spoilergesperrt: nur scratch/plot_umbau/, in Logs/MP-Jobs NUR Status.
Aufruf: plot_b4_opus.py [--dry]   Notbremse: touch /tmp/aurora_samstag_stop"""
import datetime as dt, importlib.util, os, subprocess, sys, time

W = "/home/bolla/workspace"
OUT = f"{W}/scratch/plot_umbau"
LOG = f"{W}/logs/plot_b4_opus.log"
STOP = "/tmp/aurora_samstag_stop"
MODEL = "claude-opus-5"
CL = "/home/bolla/.local/bin/claude"
JOB = "plot-b4-opus"
sys.path.insert(0, f"{W}/scripts")


def log(m):
    open(LOG, "a").write(f"[{dt.datetime.now():%d.%m. %H:%M:%S}] {m}\n")


def melde(text, status=None):
    try:
        from job_status import mc_meldung
        mc_meldung(JOB, "🌙 AURORA II Plot: Schritt 4 (Opus)", text, status)
    except Exception as e:
        log(f"Meldung fehlgeschlagen: {e!r}")


def b4_prompt():
    """Prompt aus plot_nacht.py holen, OHNE dessen Nacht-Override (limit_policy) zu behalten."""
    import limit_policy
    orig = (limit_policy.limits, limit_policy.week_blocked)
    spec = importlib.util.spec_from_file_location("pn", f"{W}/scripts/plot_nacht.py")
    pn = importlib.util.module_from_spec(spec)
    sys.argv = ["x"]
    spec.loader.exec_module(pn)
    limit_policy.limits, limit_policy.week_blocked = orig        # Nacht-Override zuruecknehmen
    p = [pr for n, _, pr in pn.STEPS if n == "b4"][0]
    return p.replace("Du bist Fable, Plot-Architekt", "Du bist Plot-Architekt")


def main():
    if "--dry" in sys.argv:
        p = b4_prompt(); print(len(p), "Zeichen; Opus:", MODEL, "| Fable im Text:", "Fable" in p); return
    if os.path.exists(f"{OUT}/_done_b4"):
        log("b4 schon fertig"); return
    import limit_gate, limit_policy
    prompt = b4_prompt()
    melde("Schritt 4 (Briefings für die Opus-Kapitelneufassung) gestartet, mit Opus statt Fable. Inhalte bleiben gesperrt (kein Spoiler).", "aktion")
    for versuch in range(1, 9):
        if os.path.exists(STOP):
            log("Notbremse"); melde("⚠️ Notbremse gesetzt, Schritt 4 gestoppt.", "aktion"); return
        q = limit_gate.quota() or {}
        log(f"Versuch {versuch}: 5h {q.get('five_hour_pct')} %, Woche {q.get('seven_day_pct')} %, stale={q.get('stale')}")
        r = limit_gate.run([CL, "-p", "--model", MODEL, "--allowedTools", "Read,Write,Bash,Glob,Grep"],
                           input=prompt, capture_output=True, text=True, timeout=3000, wait=False, heavy=True)
        q2 = limit_gate.quota() or {}
        log(f"rc={r.returncode} {(r.stdout or '')[-200:].strip()!r} {(r.stderr or '')[-200:].strip()!r} | nachher 5h {q2.get('five_hour_pct')} %, Woche {q2.get('seven_day_pct')} %")
        n = len([f for f in os.listdir(f"{OUT}/b4_briefings") if f.startswith("kap")]) if os.path.isdir(f"{OUT}/b4_briefings") else 0
        if r.returncode == 0 and n > 0:
            open(f"{OUT}/_done_b4", "w").write(f"{time.ctime()} opus, {n} Briefings\n")
            offen = os.path.exists(f"{OUT}/b4_briefings/_offen.md")
            melde(f"✅ Schritt 4 fertig: {n} Briefings geschrieben" + (" (einige Kapitel stehen noch in _offen.md)" if offen else "") +
                  f". Verbrauch: 5h {q.get('five_hour_pct')} % → {q2.get('five_hour_pct')} %. Ergebnisse liegen in scratch/plot_umbau/b4_briefings (gesperrt).", "ok")
            return
        if r.returncode == 75:                       # Gate: nicht gestartet, kein Verbrauch -> spaeter neu
            log("Gate: nicht gestartet, warte 30 Min"); time.sleep(1800); continue
        log("Lauf ohne Ergebnis (evtl. Limit) -> warte 20 Min und versuche erneut"); time.sleep(1200)
    melde("⚠️ Schritt 4 nach 8 Versuchen ohne Ergebnis. Bitte „plot weiter“ sagen.", "aktion")


if __name__ == "__main__":
    main()
