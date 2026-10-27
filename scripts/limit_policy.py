"""Zentrale Limit-Regeln (Chris 27.10.2026) - EINE Stelle fuer alle Schwellen.

Quelle der Wahrheit fuer Menschen: memory/feedback_limit_regeln.md. Wer Schwellen braucht, importiert von hier
(limit_gate.py, samstag_ausreizen.py, ~/.claude/hooks/context_check.py, ~/.claude/hooks/agent_limit_guard.py).

5h-Fenster und Wochenlimit sind GETRENNTE Toepfe (Woche ~10x so gross, Prozente nicht vergleichbar).
  * 5h-Reserve-Tag: Mo/Di/Fr/Sa tagsueber (07:00-22:00) bleiben IMMER 20 % im 5h-Fenster frei
        -> Obergrenze (hard) 80 %; Gate 67 %, weil ein Schritt bis ~13 Pkt kostet (67 + 13 = 80).
  * Sa-Nacht (ab Sa 22:00 bis Wochenreset): Gate 82 %, Obergrenze 95 % (Chris 27.10.2026; Rest verfaellt, niemand braucht Reserve).
  * sonst (Mi/Do/So sowie nachts): Gate 75 %, Obergrenze 85 %.
  * Woche: Mo-Fr (bis Fr 19:00) schwere/optionale Jobs nur bei Woche < 60 % (40 % Reserve fuer Schule/Mails/MP).
Env-Overrides: LIMIT_GATE_5H / LIMIT_GATE_HARD (Vorrang), LIMIT_WEEK_RESERVE_PCT.
"""
import datetime as dt
import os

RESERVE_DAYS = (0, 1, 4, 5)          # Mo, Di, Fr, Sa
DAY_FROM, DAY_TO = 7, 22             # "tagsueber"
WEEK_ALLTAG_LIMIT = 60.0             # Mo-Fr: darueber keine schweren Jobs


def _env(name):
    try:
        return float(os.environ[name])
    except (KeyError, ValueError):
        return None


def reserve_day(now=None):
    now = now or dt.datetime.now()
    return now.weekday() in RESERVE_DAYS and DAY_FROM <= now.hour < DAY_TO


def limits(now=None):
    """(gate, hard) fuer das 5h-Fenster in Prozent verbraucht."""
    now = now or dt.datetime.now()
    if now.weekday() == 5 and now.hour >= DAY_TO:
        gate, hard = 82.0, 95.0
    elif reserve_day(now):
        gate, hard = 67.0, 80.0
    else:
        gate, hard = 75.0, 85.0
    return (_env("LIMIT_GATE_5H") or gate), (_env("LIMIT_GATE_HARD") or hard)


def week_blocked(q, now=None):
    """True, wenn schwere/optionale Jobs wegen der Alltagsreserve (Woche >= 60 %, Mo-Fr bis 19:00) ruhen muessen."""
    now = now or dt.datetime.now()
    if now.weekday() > 4 or (now.weekday() == 4 and now.hour >= 19):
        return False
    lim = _env("LIMIT_WEEK_RESERVE_PCT") or WEEK_ALLTAG_LIMIT
    return bool(q) and (q.get("seven_day_pct") or 0) >= lim


def describe(now=None):
    gate, hard = limits(now)
    return f"5h-Gate {gate:.0f} %, Obergrenze {hard:.0f} % ({'Sa-Nacht: Rest verfällt, bis 95 %' if limits(now)[1] == 95.0 else 'Reserve-Tag: 20 % bleiben frei' if reserve_day(now) else 'Normalmodus'})"


if __name__ == "__main__":
    print(describe(), "|", limits())
