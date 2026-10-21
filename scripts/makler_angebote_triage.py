#!/usr/bin/env python3
"""Angebots-Triage (Chris 15.10.2026). Makler-Mails mit Exposé/Angebot -> Haiku extrahiert Eckdaten (JSON)
-> Score wie im Excel (K.O.: Etagenwohnung / Aufzug=N) -> Fach:
  A = K.O.            -> Eintrag + Absage-ENTWURF in Outlook-Entwürfen (Versand nur nach Chris-Freigabe)
  B = Score<60 / Infos fehlen -> Rückfrage-ENTWURF
  C = Score>=60       -> Telegram-Ping + Besichtigungs-ENTWURF
Es wird NIE automatisch gesendet. Aufruf: ohne Arg = Postfach seit letztem Lauf; --dry = nur anzeigen."""
import json, re, sys, os, shutil, html, subprocess, datetime, requests
sys.path.insert(0, "/home/bolla/workspace/scripts")
from outlook_oauth2 import refresh_access_token
from job_status import report, _telegram

DATA = "/home/bolla/workspace/data/makler_status.json"
OUT = "/home/bolla/workspace/data/makler_angebote.json"
G = "https://graph.microsoft.com/v1.0"
SCHWELLE = 60
CLAUDE = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")  # Cron hat keinen PATH
SINCE = "2026-10-14T00:00:00Z"
NO_DRAFT = {"gabriela.weber@engelvoelkers.com"}  # Chris antwortet selbst (Weilheim, 15.10.2026)
KEYS = re.compile(r"exposé|expose|angebot|objekt|kaufpreis|wohnfläche|penthouse|zimmer", re.I)
today = lambda: datetime.date.today().strftime("%d.%m.%Y")
W = {"suedterrasse": 3, "lage": 3, "gesundheit": 2, "neubau": 2, "fbh": 1, "tiefgarage": 1, "keller": 1, "ruhig": 1}
PROMPT = """Extrahiere aus dieser Makler-Mail die Eckdaten EINES Wohnungsangebots. Antworte NUR mit JSON, Werte "J"/"N"/"?" wo nicht anders genannt:
{"ist_angebot":true|false,"objekt":"Kurzbeschreibung+Ort","typ":"Penthouse|Dachgeschoss|Etagenwohnung|Erdgeschoss|Gartenwohnung|Haus|?","terrasse":"J|N|?",
"preis":Zahl|null,"qm":Zahl|null,"zimmer":Zahl|null,"aufzug":"J|N|?","suedterrasse":"J|N|?","lage":"J|N|?","gesundheit":"J|N|?",
"neubau":"J|N|?","fbh":"J|N|?","tiefgarage":"J|N|?","keller":"J|N|?","ruhig":"J|N|?","provision_pct":Zahl|null,"fehlt":["Liste fehlender Angaben"]}
"provision_pct": Käuferprovision in Prozent inkl. MwSt. (0 = provisionsfrei, null = nicht genannt).\n"terrasse": J NUR bei echter großer Terrasse (Platz für Esstisch mit 6 Personen, Grill, 2 Sonnenliegen; ab ca. 20 m²). Balkon, überdachter Balkon, Loggia, kleine Terrasse = N. Keine Angabe/Größe unbekannt = ?.\n"lage": J wenn südlich A8 zwischen Lech und Bad Tölz/Garmisch bzw. westl. München. MAIL:
"""

def strip(m):
    b = re.sub(r"<(style|script).*?</\1>", "", m.get("body", {}).get("content", ""), flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", b))).strip()

def score(a):
    # No-Go: nur Penthouse/Dachgeschoss (Chris 15.10.2026: Erdgeschoss auch nicht); Terrasse Pflicht
    if a.get("typ") not in ("Penthouse", "Dachgeschoss", "?", None) or a.get("aufzug") == "N" or a.get("terrasse") == "N": return 0
    v = lambda k: 1 if a.get(k) == "J" else 0 if a.get(k) == "N" else 0.5
    pr = "?" if not a.get("preis") else ("J" if a["preis"] <= 1250000 else "N")
    gr = "?" if not a.get("qm") else ("J" if 90 <= a["qm"] <= 115 else "N")
    parts = sum(W[k] * v(k) for k in W) + 2 * v2(pr) + 3 * v2(gr)
    return round(100 * parts / (sum(W.values()) + 5))
def v2(x): return 1 if x == "J" else 0 if x == "N" else 0.5

def draft(H, to, subj, body):
    html_b = "<div style='font-family:Aptos,Calibri,sans-serif;font-size:12pt'>" + body.replace("\n", "<br>") + "</div>"
    requests.post(f"{G}/me/messages", headers=H, json={"subject": subj, "body": {"contentType": "HTML", "content": html_b},
                  "toRecipients": [{"emailAddress": {"address": to}}]})

def main():
    dry = "--dry" in sys.argv
    H = {"Authorization": "Bearer " + refresh_access_token()}
    st = json.load(open(OUT)) if __import__("os").path.exists(OUT) else {"done": [], "angebote": []}
    d = json.load(open(DATA)); mk = {}
    for r in d["regionen"]:
        for m in r["makler"]:
            if m.get("email"): mk[m["email"].lower()] = m
    u = (f"{G}/me/mailFolders/inbox/messages?$top=50&$orderby=receivedDateTime desc"
         f"&$select=id,subject,from,receivedDateTime,body&$filter=receivedDateTime ge {SINCE}")
    n = 0
    for m in requests.get(u, headers=H).json().get("value", []):
        if m["id"] in st["done"]: continue
        frm = m["from"]["emailAddress"]["address"].lower()
        mkl = mk.get(frm) or next((v for k, v in mk.items() if k.split("@")[-1] == frm.split("@")[-1]), None)
        txt = strip(m)
        if not mkl or not KEYS.search(m.get("subject", "") + " " + txt): continue
        if dry: print("KANDIDAT:", mkl["firma"], "|", m["subject"][:70]); continue
        r = subprocess.run([CLAUDE, "-p", PROMPT + txt[:6000], "--model", "haiku"], capture_output=True, text=True, timeout=180)
        j = re.search(r"\{.*\}", r.stdout, re.S)
        st["done"].append(m["id"])
        if not j: continue
        try: a = json.loads(j.group(0))
        except Exception: continue
        if not a.get("ist_angebot"): continue
        s = score(a); ko = s == 0
        fach = "A" if ko else ("C" if s >= SCHWELLE else "B")
        a.update({"makler": mkl["firma"], "datum": today(), "score": s, "fach": fach, "mail_id": m["id"], "von": frm})
        st["angebote"].append(a); n += 1
        if frm in NO_DRAFT:
            continue
        sal = "Sehr geehrte Damen und Herren,\n\n"
        sig = "\n\nMit freundlichen Grüßen\nChris & Renate Mandel"
        if fach == "A":
            draft(H, frm, "Re: " + m["subject"], sal + "vielen Dank für Ihr Angebot. Leider entspricht das Objekt nicht unseren Anforderungen (wir suchen ausschließlich ein Penthouse bzw. eine Dachgeschosswohnung mit großer Terrasse und Aufzug), sodass wir davon absehen müssen. Wir bleiben aber gerne in Ihrer Interessentenliste." + sig)
        elif fach == "B":
            fehlt = ", ".join(a.get("fehlt") or ["Etage/Aufzug, Hausgeld, Verfügbarkeit"])
            draft(H, frm, "Re: " + m["subject"], sal + f"vielen Dank für Ihr Angebot. Können Sie uns bitte noch folgende Angaben nennen: {fehlt}?" + sig)
        else:
            draft(H, frm, "Re: " + m["subject"], sal + "vielen Dank, das Objekt interessiert uns. Gerne würden wir es besichtigen — welche Termine kämen in Frage?" + sig)
            _telegram(f"🏠 Treffer ({s}/100): {a.get('objekt','')[:80]} · {a.get('preis') or '?'} € · {a.get('qm') or '?'} m² · {mkl['firma']} — Entwurf liegt in Outlook")
    if not dry:
        st["done"] = st["done"][-1500:]; json.dump(st, open(OUT, "w"), ensure_ascii=False, indent=2)
        xl = ""
        if n:  # Excel automatisch nachziehen (Chris 21.10.2026: nichts von Hand eintragen)
            r = subprocess.run([sys.executable, "/home/bolla/workspace/scripts/makler_excel_bauen_v2.py"], capture_output=True, text=True, timeout=300)
            xl = ", Excel aktualisiert" if r.returncode == 0 else ", EXCEL-FEHLER: " + r.stderr[-150:]
        report("makler-angebote-triage", "Angebots-Triage", "fehler" if "FEHLER" in xl else "ok", f"{n} neue Angebote bewertet{xl}")
    print("neue Angebote:", n)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # Absturz darf nie still bleiben (Cron 19.-21.10.2026: 'claude' nicht im PATH)
        report("makler-angebote-triage", "Angebots-Triage", "fehler", f"{type(e).__name__}: {e}"[:300])
        raise
