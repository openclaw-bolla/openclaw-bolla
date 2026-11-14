#!/usr/bin/env python3
"""Sagt Chris Bescheid, WANN er einen der beiden Claude-Zuruecksetzen-Knoepfe druecken sollte (Cron alle 15 Min, kostet keine Token).
Meldungen landen ganz oben in MC-Jobs (job_status, kein Telegram). Nur Hinweise - der Klick bleibt bei Chris.

Angebote (Chris-Screenshot 14.11.2026, Einstellungen -> Nutzung):
  Vollstaendige Zuruecksetzung  Ablauf 10.12.2026 23:00   (einmalig)
  Fable-Zuruecksetzung          Ablauf 17.11.2026 08:59   (einmalig; fuellt 5h + Fable, erstattet Fable-Anteil der Woche)
Regeln:
  FABLE  - Fable-Balken >= 85 % (und Angebot offen)            -> 'jetzt klicken'
         - Mo 16.11. 18:00 / Di 17.11. 06:30 noch ungenutzt     -> Erinnerung (Verfall 08:59)
  VOLL   - Woche >= 90 % UND bis zum Wochenreset noch >= 36 h   -> 'lohnt sich jetzt' (sonst Verschenken)
         - 8.12. 09:00 / 10.12. 08:00 ungenutzt                  -> Erinnerung (Verfall 10.12. 23:00)
Nutzung erkannt: Fable-Balken faellt >= 30 Pp bzw. Woche faellt >= 40 Pp bei gleichem Reset-Zeitpunkt (state/reset_hinweis.json).
Chris kann auch manuell setzen:  python3 reset_hinweis_watcher.py --genutzt fable|voll
"""
import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from job_status import mc_meldung  # noqa: E402

W = "/home/bolla/workspace"
STATE = f"{W}/state/reset_hinweis.json"
FABLE_ABLAUF = dt.datetime(2026, 11, 17, 8, 59)
VOLL_ABLAUF = dt.datetime(2026, 12, 10, 23, 0)
LOG = f"{W}/logs/reset_hinweis.log"


def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{dt.datetime.now():%d.%m. %H:%M:%S}] {m}\n")


def load():
    try:
        return json.load(open(STATE))
    except Exception:
        return {"fable_genutzt": False, "voll_genutzt": False, "last": {}, "gemeldet": {}}


def save(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, "w"), indent=1)


def usage():
    t = json.load(open(os.path.expanduser("~/.claude/.credentials.json")))["claudeAiOauth"]["accessToken"]
    r = urllib.request.Request("https://api.anthropic.com/api/oauth/usage", headers={
        "Authorization": "Bearer " + t, "anthropic-beta": "oauth-2025-04-20", "Accept": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=10))


def melden(s, key, titel, text, min_stunden=6):
    """Hoechstens alle min_stunden je Schluessel."""
    last = s["gemeldet"].get(key)
    if last and (dt.datetime.now() - dt.datetime.fromisoformat(last)).total_seconds() < min_stunden * 3600:
        return
    mc_meldung(f"reset-hinweis-{key}", titel, text, "aktion")
    s["gemeldet"][key] = dt.datetime.now().isoformat(timespec="seconds")
    log(f"gemeldet {key}: {titel}")


def main():
    s = load()
    if len(sys.argv) == 3 and sys.argv[1] == "--genutzt":
        s[("fable" if sys.argv[2] == "fable" else "voll") + "_genutzt"] = True
        save(s)
        print("vermerkt")
        return
    now = dt.datetime.now()
    try:
        d = usage()
    except Exception as e:
        log(f"Usage nicht lesbar: {e!r}")
        return
    wk = float(d["seven_day"]["utilization"])
    wk_reset = d["seven_day"]["resets_at"]
    fb = None
    for lim in d.get("limits", []):
        if ((lim.get("scope") or {}).get("model") or {}).get("display_name", "").lower() == "fable":
            fb = float(lim.get("percent") or 0)
    last = s.get("last", {})
    # Nutzung erkennen
    if fb is not None and last.get("fb") is not None and last["fb"] - fb >= 30 and not s["fable_genutzt"] and now < FABLE_ABLAUF \
            and not (now.weekday() == 5 and now.hour == 23 and now.minute < 20):
        s["fable_genutzt"] = True
        log("Fable-Zuruecksetzung als genutzt erkannt")
    if last.get("wk") is not None and last["wk"] - wk >= 40 and last.get("wk_reset") == wk_reset and not s["voll_genutzt"]:
        s["voll_genutzt"] = True
        log("Vollstaendige Zuruecksetzung als genutzt erkannt")
    s["last"] = {"fb": fb, "wk": wk, "wk_reset": wk_reset}

    # FABLE
    if not s["fable_genutzt"] and now < FABLE_ABLAUF:
        if fb is not None and fb >= 85:
            melden(s, "fable-jetzt", "🔄 Fable-Zurücksetzung jetzt klicken",
                   f"Fable-Balken bei {fb:.0f} %. Claude → Einstellungen → Nutzung → „Fable-Zurücksetzung → Kostenlos zurücksetzen“. "
                   f"Verfällt Di 17.11. 08:59. Die Nutzung wird automatisch erkannt.", 3)
        if (now.date() == dt.date(2026, 11, 16) and now.hour >= 18) or (now.date() == dt.date(2026, 11, 17) and now.hour >= 6 and (now.hour, now.minute) >= (6, 30)):
            melden(s, "fable-frist", "⏰ Fable-Zurücksetzung läuft bald ab",
                   f"Noch ungenutzt, Verfall Di 17.11. 08:59 (Fable-Balken {fb if fb is not None else '?'} %). Jetzt klicken, wenn noch Fable-Arbeit ansteht – sonst verfällt sie.", 4)
    # VOLL
    if not s["voll_genutzt"] and now < VOLL_ABLAUF:
        rest_h = (dt.datetime.fromisoformat(wk_reset.replace("Z", "+00:00")).astimezone().replace(tzinfo=None) - now).total_seconds() / 3600
        if wk >= 90 and rest_h >= 36:
            melden(s, "voll-jetzt", "🔄 Vollständige Zurücksetzung lohnt sich jetzt",
                   f"Woche bei {wk:.0f} %, bis zum Wochenreset noch {rest_h:.0f} h. Jetzt klicken bringt eine volle Woche zusätzlich "
                   f"(Claude → Einstellungen → Nutzung → „Vollständige Zurücksetzung“). Verfällt 10.12. 23:00.", 8)
        if (now.date() == dt.date(2026, 12, 8) and now.hour >= 9) or (now.date() == dt.date(2026, 12, 10) and now.hour >= 8):
            melden(s, "voll-frist", "⏰ Vollständige Zurücksetzung läuft bald ab",
                   f"Noch ungenutzt, Verfall Do 10.12. 23:00 (Woche {wk:.0f} %). Letzte Chance, sie sinnvoll einzusetzen.", 12)
    save(s)


if __name__ == "__main__":
    main()
