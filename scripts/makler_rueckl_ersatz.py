#!/usr/bin/env python3
"""Rückläufer-Autopilot (Chris 15.10.2026): für unzustellbare Makler-Adressen per Impressum/Kontaktseite eine
Ersatz-Mailadresse suchen (kein LLM). Gefunden -> resend_queue; Neuversand NUR wenn config/makler_resend_freigabe.json
{"freigegeben": true} existiert (Chris-OK zum Text). Nichts gefunden -> Eintrag still auf Telefon/Formular.
Aufruf: ohne Arg = suchen (+ ggf. senden); --dry = nur suchen, nichts schreiben."""
import json, re, sys, os, time, datetime, html, requests
sys.path.insert(0, "/home/bolla/workspace/scripts")
from job_status import report
DATA = "/home/bolla/workspace/data/makler_status.json"
FREI = "/home/bolla/workspace/config/makler_resend_freigabe.json"
today = lambda: datetime.date.today().strftime("%d.%m.%Y")
PATHS = ["", "/impressum", "/kontakt", "/impressum.html", "/kontakt.html", "/contact"]
RX = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
BAD_PART = ("sentry", "example", "wixpress", "datenschutz", "noreply", "no-reply", "@2x", ".png", ".jpg", ".webp")

def domain_of(m, bad):
    e = (m.get("email_ungueltig") or bad or "").lower()
    return e.split("@")[-1] if "@" in e else ""

def find_alt(dom, bad):
    found = []
    for base in (f"https://{dom}", f"https://www.{dom}"):
        ok = False
        for p in PATHS:
            try:
                r = requests.get(base + p, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            except Exception:
                break
            if r.status_code != 200: continue
            ok = True
            t = html.unescape(r.text)
            t = re.sub(r"\s*\[?\(?at\)?\]?\s*", "@", t) if False else t
            for e in RX.findall(t):
                e = e.lower().strip(".")
                if e == bad or any(b in e for b in BAD_PART): continue
                if e.split("@")[-1].endswith(dom) or dom.endswith(e.split("@")[-1]): found.append(e)
        if ok: break
    pref = [e for e in dict.fromkeys(found) if e.split("@")[0] in ("info", "kontakt", "office", "mail", "post", "immobilien")]
    return (pref or list(dict.fromkeys(found)) or [None])[0]

def main():
    dry = "--dry" in sys.argv
    d = json.load(open(DATA)); d.setdefault("resend_queue", [])
    queued = {q["id"] for q in d["resend_queue"]}
    n_found = n_none = 0
    for r in d["regionen"]:
        for m in r["makler"]:
            bad = (m.get("email_ungueltig") or "").lower()
            if not bad or m.get("email") or m["id"] in queued or m.get("ersatz_geprueft"): continue
            dom = domain_of(m, bad)
            alt = find_alt(dom, bad) if dom else None
            m["ersatz_geprueft"] = today()
            if alt:
                d["resend_queue"].append({"id": m["id"], "firma": m["firma"], "email": alt, "alt_von": bad, "datum": today()})
                n_found += 1; print("ERSATZ", m["firma"], alt)
            else:
                st = d["statuses"].get(m["id"], {})
                if st.get("status") in (None, "neu", "email_gesendet", "nicht_interessant"):
                    d["statuses"][m["id"]] = {"status": "nicht_interessant" if not m.get("kontaktformular") else "neu",
                        "notiz": "Mail unzustellbar, keine Ersatz-Adresse gefunden " + today(), "datum": today()}
                n_none += 1; print("KEINE", m["firma"])
    n_sent = 0
    if not dry and os.path.exists(FREI) and json.load(open(FREI)).get("freigegeben"):
        import send_immo_makler_text as T
        from outlook_oauth2 import refresh_access_token
        tok = refresh_access_token()
        for q in list(d["resend_queue"]):
            msg = {"message": {"subject": T.SUBJECT, "body": {"contentType": "HTML", "content": T.BODY},
                   "toRecipients": [{"emailAddress": {"address": q["email"]}}]}, "saveToSentItems": True}
            rr = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                               headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}, json=msg)
            if rr.status_code == 202:
                for r in d["regionen"]:
                    for m in r["makler"]:
                        if m["id"] == q["id"]: m["email"] = q["email"]; m["mailen"] = True
                d["statuses"][q["id"]] = {"status": "email_gesendet", "notiz": f"Voranfrage an Ersatz-Adresse {today()}", "datum": today()}
                d["resend_queue"].remove(q); n_sent += 1; time.sleep(30)
    if not dry: json.dump(d, open(DATA, "w"), ensure_ascii=False, indent=2)
    report("makler-rueckl-ersatz", "Makler-Rückläufer-Autopilot", "ok",
           f"{n_found} Ersatz-Adressen gefunden, {n_none} ohne Ersatz, {n_sent} neu versendet")
    print(n_found, n_none, n_sent)

if __name__ == "__main__":
    main()
