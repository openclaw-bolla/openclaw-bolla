#!/usr/bin/env python3
"""Trägt alle Termine aus data/schuljahr2627.json als Outlook-Kalendereinträge ein — im selben
Stil wie im Vorjahr (Subject "<Klasse> <Gruppe> - <Thema>", Kategorie "Lessing I"/"Lessing II" je
nach Gruppe, kein Ort/Reminder, siehe Vorjahres-Vergleich vom 12.08.2026). Termine mit leerem
Thema (Reserve-Slots am Schuljahresende) werden übersprungen, nicht geraten.
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

CFGDIR = Path("/home/bolla/workspace/config")
OAUTH = json.loads((CFGDIR / "outlook_oauth2.json").read_text())
TOKF = CFGDIR / "outlook_token.json"
DATA_FILE = "/home/bolla/workspace/data/schuljahr2627.json"
GRAPH = "https://graph.microsoft.com/v1.0/me"

CATEGORY_BY_GRUPPE = {"I": "Lessing I", "II": "Lessing II"}


def get_token():
    tok = json.loads(TOKF.read_text())
    data = urllib.parse.urlencode({
        "client_id": OAUTH["client_id"], "client_secret": OAUTH["client_secret"],
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
        "scope": "Calendars.ReadWrite offline_access",
    }).encode()
    new = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
        data=data, method="POST")).read())
    tok.update(new)
    TOKF.write_text(json.dumps(tok, indent=2))
    TOKF.chmod(0o600)
    return new["access_token"]


def graph_post(path, body, token):
    data = json.dumps(body).encode()
    req = urllib.request.Request(f"{GRAPH}{path}", data=data, method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def clean_thema(thema):
    if " – " in thema:
        return thema.split(" – ", 1)[1]
    return thema


def build_event(t):
    klasse, gruppe = t["klasse"], t["gruppe"]
    thema = clean_thema(t["thema"])
    subject = f"{klasse} {gruppe} - {thema}"
    start_str, end_str = t["uhrzeit"].split("–")
    datum = t["datum"]
    return {
        "subject": subject,
        "start": {"dateTime": f"{datum}T{start_str}:00", "timeZone": "Europe/Berlin"},
        "end": {"dateTime": f"{datum}T{end_str}:00", "timeZone": "Europe/Berlin"},
        "categories": [CATEGORY_BY_GRUPPE[gruppe]],
        "isReminderOn": False,
        "showAs": "busy",
    }


def main():
    termine = json.loads(Path(DATA_FILE).read_text())["termine"]
    token = get_token()

    created, skipped, failed = [], [], []
    for t in termine:
        if not t.get("thema", "").strip():
            skipped.append(t)
            continue
        event = build_event(t)
        try:
            result = graph_post("/events", event, token)
            if result.get("id"):
                created.append(event["subject"])
            else:
                failed.append((event["subject"], str(result)[:200]))
        except Exception as e:
            failed.append((event.get("subject", "?"), str(e)[:200]))

    print(f"\n=== ZUSAMMENFASSUNG ===")
    print(f"Erstellt: {len(created)}")
    print(f"Übersprungen (leeres Thema): {len(skipped)}")
    for t in skipped:
        print(f"  - {t['datum']} {t['klasse']} {t['gruppe']} {t['zeit']}")
    print(f"Fehlgeschlagen: {len(failed)}")
    for subj, err in failed:
        print(f"  - {subj}: {err}")


if __name__ == "__main__":
    main()
