"""Immo-Voranfrage an Makler (Freigabe Chris 14.10.2026, Entwurf v4 + 'Westen und Süden').
Einzelmails von ernstmandel@outlook.de via Graph, 30 s Abstand, Staltmayr ausgenommen.
Aufruf: --dry (nur listen) | ohne Argument = senden. Status wird je Mail in makler_status.json gesetzt."""
import json, sys, time, html, datetime, requests
from outlook_oauth2 import refresh_access_token

DATA = "/home/bolla/workspace/data/makler_status.json"
CRIT = json.load(open("/home/bolla/workspace/config/immo_criteria.json"))
SKIP_IDS = {"staltmayr"}
must = [k for k, p in CRIT["priorities"].items() if p == "must"]
imp = [k for k, p in CRIT["priorities"].items() if p == "important"]
SUBJECT = "Suchanfrage Eigentumswohnung – Voranfrage"
INTRO = ("wir suchen eine Eigentumswohnung zur Eigennutzung im Westen und Süden von München (Details unten) — "
         "frühestens ab Herbst 2027, möglicherweise auch erst ab Herbst 2028. Es eilt also nicht; wir würden uns aber "
         "gerne frühzeitig bei Ihnen vormerken lassen.")
def ul(items): return "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"
BODY = f"""<div style="font-family:Aptos,Calibri,sans-serif;font-size:12pt">
<p>Sehr geehrte Damen und Herren,</p>
<p>{html.escape(INTRO)}</p>
<p><b>Unsere Kernanforderungen:</b></p>{ul(must)}
<p><b>Optionale Anforderungen:</b></p>{ul(imp)}
<p>Für Angebote, die diesen Kriterien entsprechen, würden wir uns sehr freuen, von Ihnen zu hören — auch wenn diese erst später verfügbar werden. Bitte nehmen Sie uns gerne in Ihre Interessentenliste auf.</p>
<p>Mit freundlichen Grüßen<br>Chris &amp; Renate Mandel<br>ernstmandel@outlook.de</p>
</div>"""

d = json.load(open(DATA))
targets, seen = [], set()
for r in d["regionen"]:
    for m in r["makler"]:
        e = (m.get("email") or "").strip().lower()
        if not e or m.get("mailen") is False or m["id"] in SKIP_IDS or e in seen: continue
        if d["statuses"].get(m["id"], {}).get("status") in ("email_gesendet", "nicht_interessant"): continue
        seen.add(e); targets.append((m["id"], m["firma"], e))
print(len(targets), "Empfänger")
if "--dry" in sys.argv:
    for t in targets: print(" ", t[1], "<%s>" % t[2])
    sys.exit()
tok = refresh_access_token()
ok = fail = 0
for i, (mid, firma, e) in enumerate(targets):
    msg = {"message": {"subject": SUBJECT, "body": {"contentType": "HTML", "content": BODY},
                       "toRecipients": [{"emailAddress": {"address": e}}]}, "saveToSentItems": True}
    r = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}, json=msg)
    if r.status_code == 401:
        tok = refresh_access_token()
        r = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                          headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}, json=msg)
    if r.status_code == 202:
        ok += 1
        cur = json.load(open(DATA))
        cur["statuses"][mid] = {"status": "email_gesendet", "notiz": "Voranfrage-Mail 14.10.2026",
                                "datum": datetime.date.today().strftime("%d.%m.%Y")}
        json.dump(cur, open(DATA, "w"), ensure_ascii=False, indent=2)
        print(f"[{i+1}/{len(targets)}] OK {firma} <{e}>", flush=True)
    else:
        fail += 1
        print(f"[{i+1}/{len(targets)}] FEHLER {r.status_code} {firma} <{e}> {r.text[:150]}", flush=True)
    if i < len(targets) - 1: time.sleep(30)
print(f"FERTIG: {ok} gesendet, {fail} Fehler")
