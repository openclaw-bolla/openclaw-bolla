"""Gemeinsames 5h-Limit-Gate fuer Hintergrund-Skripte mit `claude -p` (Chris 25.10.2026).

Regel: Hintergrundlaeufe reissen das 5h-Fenster nie.
  * vor jedem Aufruf: 5h >= GATE (75 %)  -> warten bis Reset (wait=True) bzw. sofort abbrechen (wait=False)
  * waehrend des Aufrufs: 5h >= HARD (85 %) -> Prozess killen, danach wie oben
Quota kommt aus dem MP-Endpunkt /api/claudequota (kostet keine Tokens). Ist er nicht erreichbar, laeuft der Aufruf ungegatet.

Nutzung: Drop-in fuer subprocess.run
    import limit_gate
    r = limit_gate.run([CLAUDE, "-p", prompt], capture_output=True, text=True, timeout=300)            # wartet bei Limit
    r = limit_gate.run([...], capture_output=True, text=True, timeout=90, wait=False)                  # Cron: ueberspringen
Bei wait=False und Limit kommt ein CompletedProcess mit returncode 75 und stderr "limit_gate: ..." zurueck
(bestehende Fehlerbehandlung der Aufrufer greift, der naechste Cron-Lauf versucht es erneut).
Env: LIMIT_GATE_5H (75), LIMIT_GATE_HARD (85), LIMIT_GATE_OFF=1 schaltet das Gate ab.
"""
import json
import os
import subprocess
import threading
import time
import urllib.request

QUOTA_URL = "http://127.0.0.1:18790/api/claudequota"
RC_LIMIT = 75


def _num(env, default):
    try:
        return float(os.environ.get(env, default))
    except ValueError:
        return float(default)


def quota():
    try:
        with urllib.request.urlopen(QUOTA_URL, timeout=15) as r:
            return json.load(r)
    except Exception:
        return None


def _reset_seconds(q):
    return (q.get("five_hour_reset_hours") or 0) * 3600 + (q.get("five_hour_reset_minutes") or 5) * 60 + 90


def _blocked(gate):
    """Quota-Dict, falls 5h-Fenster >= gate, sonst None (auch bei unerreichbarer API)."""
    q = quota()
    if q and (q.get("five_hour_pct") or 0) >= gate:
        return q
    return None


def _limited(cmd, msg):
    return subprocess.CompletedProcess(cmd, RC_LIMIT, "", "limit_gate: " + msg)


def run(cmd, *, input=None, timeout=None, wait=True, capture_output=True, text=True, check=False, **kw):
    if os.environ.get("LIMIT_GATE_OFF") == "1":
        return subprocess.run(cmd, input=input, timeout=timeout, capture_output=capture_output, text=text, check=check, **kw)
    gate, hard = _num("LIMIT_GATE_5H", 75), _num("LIMIT_GATE_HARD", 85)
    for _ in range(4):
        q = _blocked(gate)
        if q:
            if not wait:
                return _limited(cmd, f"5h {q.get('five_hour_pct')} % >= {gate:.0f} % - uebersprungen")
            time.sleep(_reset_seconds(q))     # Reset abwarten, danach neu pruefen
            continue
        r, killed = _watched(cmd, input, timeout, hard, text, kw)
        if not killed:
            if check and r.returncode:
                raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)
            return r
        if not wait:
            return _limited(cmd, f"5h >= {hard:.0f} % - Aufruf abgebrochen")
    return _limited(cmd, "5h-Fenster dauerhaft voll - aufgegeben")


def _watched(cmd, input, timeout, hard, text, kw):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE if input is not None else None,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text, **kw)
    out = {}

    def comm():
        out["o"], out["e"] = p.communicate(input)
    th = threading.Thread(target=comm, daemon=True)
    th.start()
    t0, nxt = time.time(), time.time() + 30
    while th.is_alive():
        th.join(2)
        if timeout and time.time() - t0 > timeout:
            p.kill(); th.join(5)
            raise subprocess.TimeoutExpired(cmd, timeout)
        if time.time() >= nxt:
            nxt = time.time() + 30
            q = quota()
            if q and (q.get("five_hour_pct") or 0) >= hard:
                p.kill(); th.join(5)
                return None, True
    return subprocess.CompletedProcess(cmd, p.returncode, out.get("o", ""), out.get("e", "")), False


if __name__ == "__main__":      # Selbsttest ohne Tokens: python3 limit_gate.py
    r = run(["echo", "ok"], timeout=10, wait=False)
    print("rc", r.returncode, r.stdout.strip(), "| Quota:", (quota() or {}).get("five_hour_pct"))
    os.environ["LIMIT_GATE_5H"] = "0"
    r = run(["echo", "nie"], timeout=10, wait=False)
    print("Gate-Test (Schwelle 0): rc", r.returncode, r.stderr.strip())
