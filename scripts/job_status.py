#!/usr/bin/env python3
"""Gemeinsamer Job-Status fuer Bolla-Skripte (Statusseite /jobs in Mission Control).

Skripte tragen hier ihren Stand ein, statt Telegram zu bespielen:

    import sys; sys.path.insert(0, "/home/bolla/workspace/scripts")
    from job_status import report
    report("itslearning-songs", "Geburtstagssongs", "laeuft")
    report("itslearning-songs", "Geburtstagssongs", "ok", "Henny + Eva gesendet", link="...")
    report("itslearning-songs", "Geburtstagssongs", "fehler", "Eva: Timeout")   # -> Telegram

Status: laeuft | ok | fehler | aktion  (geplant kommt automatisch aus dem Crontab)
Telegram nur bei fehler/aktion (oder notify=True). Erfolg bleibt still.
"""
import datetime
import fcntl
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request

STATE = "/home/bolla/workspace/data/job_status.json"
TG_CFG = "/home/bolla/workspace/config/telegram_bot.json"
MAX_JOBS = 80
TG_STATUS = ("fehler", "aktion")


def _load():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return {}


def _telegram(text):
    try:
        cfg = json.load(open(TG_CFG))
        data = urllib.parse.urlencode({"chat_id": cfg["chris_id"], "text": text}).encode()
        urllib.request.urlopen(
            f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage", data=data, timeout=10)
    except Exception:
        pass


def report(job_id, title, status, detail="", link=None, notify=None, ts=None):
    """Status eintragen. notify=None -> Telegram nur bei fehler/aktion."""
    now = ts or datetime.datetime.now().isoformat(timespec="seconds")
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        d = _load()
        old = d.get(job_id, {})
        d[job_id] = {
            "title": title, "status": status, "detail": detail, "link": link,
            "ts": now,
            "started": now if status == "laeuft" else old.get("started"),
        }
        if len(d) > MAX_JOBS:
            for k in sorted(d, key=lambda k: d[k].get("ts", ""))[: len(d) - MAX_JOBS]:
                del d[k]
        tmp = STATE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        os.replace(tmp, STATE)
    if notify is True or (notify is None and status in TG_STATUS):
        icon = {"fehler": "⚠️", "aktion": "👉"}.get(status, "ℹ️")
        _telegram(f"{icon} {title}: {detail}"[:500])


# ---------- anstehende Einmal-Jobs aus dem Crontab ----------
_NAMES = [  # (Skript-Teil, Anzeigename)
    ("kurstag5_freigabe_check", "Kurstag 5 (Gruppe I): Freigabe-Check"),
    ("ausreizen_start_wrapper", "Wochenend-Ausreizen starten (Makler-Check + AURORA-Entwürfe)"),
    ("geburtstagssong_batch", "Geburtstagssongs senden"),
    ("naechste_termine", "Nächste Termine posten"),
    ("kurstag_cron_wrapper", "Kurstag-Mitteilungen posten"),
    ("post_kurstag", "Kurstag-Mitteilungen posten"),
]


_ARGS = {"mi": "Mittwoch", "do": "Donnerstag"}


def _name_for(cmd):
    for key, name in _NAMES:
        if key in cmd:
            return name
    m = re.search(r"([\w\-]+)\.(?:py|sh)", cmd)
    return m.group(1).replace("_", " ") if m else cmd[:40]


def upcoming(days=14):
    """Einmal-Jobs (fester Tag+Monat) der naechsten `days` Tage aus dem Crontab."""
    now = datetime.datetime.now()
    out = []
    try:
        lines = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout.splitlines()
    except Exception:
        return out
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split(None, 5)
        if len(p) < 6 or not (p[0].isdigit() and p[1].isdigit() and p[2].isdigit() and p[3].isdigit()):
            continue
        try:
            when = datetime.datetime(now.year, int(p[3]), int(p[2]), int(p[1]), int(p[0]))
        except ValueError:
            continue
        if when < now - datetime.timedelta(minutes=1) or when > now + datetime.timedelta(days=days):
            continue
        arg = re.search(r"\.py\s+(\w+)\s*(?:>>|$)", p[5])
        name = _name_for(p[5]) + (f" ({_ARGS.get(arg.group(1), arg.group(1))})" if arg else "")
        out.append({"when": when.isoformat(timespec="minutes"), "title": name})
    return sorted(out, key=lambda x: x["when"])


def snapshot():
    d = _load()
    jobs = [dict(v, id=k) for k, v in d.items()]
    jobs.sort(key=lambda j: j.get("ts", ""), reverse=True)
    return {"now": datetime.datetime.now().isoformat(timespec="seconds"),
            "jobs": jobs, "upcoming": upcoming()}


if __name__ == "__main__":
    print(json.dumps(snapshot(), ensure_ascii=False, indent=1))
