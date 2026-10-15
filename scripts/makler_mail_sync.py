#!/usr/bin/env python3
"""Makler-Mail-Sync (Chris 14.10.2026: "Status immer automatisch").
Liest Posteingang (+ Gelöschte) und
 - Antworten von Maklern -> Status feedback_erhalten (nur wenn noch neu/email_gesendet), Notiz
 - Rückläufer (Unzustellbar) -> Adresse ungültig, mailen=false, Eintrag in 'unzustellbar' (rote Box in MP),
   Rückläufer-Mail danach in Ordner Projekte/Immos 2027-28 verschieben.
Status in data/makler_status.json, Job-Status via job_status.report (Telegram nur bei Fehler)."""
import json, re, sys, html, datetime, requests
sys.path.insert(0, "/home/bolla/workspace/scripts")
from outlook_oauth2 import refresh_access_token
from job_status import report

DATA = "/home/bolla/workspace/data/makler_status.json"
STATE = "/home/bolla/workspace/state/makler_mail_sync.json"
FOLDER_NAME = "Immos 2027-28"
SINCE = "2026-10-14T00:00:00Z"
G = "https://graph.microsoft.com/v1.0"
BOUNCE_FROM = ("postmaster@", "mailer-daemon@", "mailer-daemon")
BOUNCE_SUBJ = re.compile(r"unzustellbar|undeliverable|delivery status notification|undelivered|returned mail", re.I)
today = lambda: datetime.date.today().strftime("%d.%m.%Y")

def text_of(m):
    b = re.sub(r"<(style|script).*?</\1>", "", m.get("body", {}).get("content", ""), flags=re.S)
    b = html.unescape(re.sub(r"<[^>]+>", " ", b))
    return re.sub(r"\s+", " ", b).strip()

def main():
    try:
        H = {"Authorization": "Bearer " + refresh_access_token()}
        st = {}
        try: st = json.load(open(STATE))
        except Exception: pass
        done = set(st.get("done", []))
        d = json.load(open(DATA))
        d.setdefault("unzustellbar", [])
        by_email, by_dom = {}, {}
        for r in d["regionen"]:
            for m in r["makler"]:
                for e in (m.get("email"), m.get("email_ungueltig")):
                    if e: by_email[e.lower()] = (r, m); by_dom.setdefault(e.lower().split("@")[-1], (r, m))
        # Zielordner
        fid = None
        def find_folder(url):
            nonlocal fid
            for f in requests.get(url, headers=H).json().get("value", []):
                if f["displayName"] == FOLDER_NAME: fid = f["id"]; return
                if f.get("childFolderCount"): find_folder(f"{G}/me/mailFolders/{f['id']}/childFolders?$top=100")
                if fid: return
        find_folder(f"{G}/me/mailFolders?$top=100")
        msgs = []
        for folder in ("inbox", "deleteditems", "junkemail"):
            u = (f"{G}/me/mailFolders/{folder}/messages?$top=100&$orderby=receivedDateTime desc"
                 f"&$select=id,subject,from,receivedDateTime,body,conversationId&$filter=receivedDateTime ge {SINCE}")
            msgs += [(folder, x) for x in requests.get(u, headers=H).json().get("value", [])]
        sent = {}
        su = (f"{G}/me/mailFolders/sentitems/messages?$top=100&$orderby=sentDateTime desc"
              f"&$select=conversationId,sentDateTime&$filter=sentDateTime ge {SINCE}")
        for x in requests.get(su, headers=H).json().get("value", []):
            c = x.get("conversationId")
            if c and x.get("sentDateTime", "") > sent.get(c, ""): sent[c] = x["sentDateTime"]
        n_reply = n_bounce = n_moved = n_spam = 0
        for folder, m in msgs:
            if folder == "inbox" and fid and sent.get(m.get("conversationId"), "") > m.get("receivedDateTime", "~"):
                frm0 = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
                if (by_email.get(frm0) or by_dom.get(frm0.split("@")[-1])) and not frm0.startswith(BOUNCE_FROM):
                    requests.post(f"{G}/me/messages/{m['id']}/move", headers=H, json={"destinationId": fid}); n_moved += 1
                    done.add(m["id"]); continue
            if m["id"] in done: continue
            frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
            subj = m.get("subject") or ""
            body = text_of(m)
            is_bounce = frm.startswith(BOUNCE_FROM) and BOUNCE_SUBJ.search(subj)
            if is_bounce:
                mm = re.search(r"recipients or groups:\s*([\w.+-]+@[\w.-]+)", body) or re.search(r"([\w.+-]+@[\w.-]+\.\w+)", body)
                bad = mm.group(1).lower() if mm else ""
                hit = by_email.get(bad)
                if hit and bad and not any(u["adresse"].lower() == bad for u in d["unzustellbar"]):
                    r, mk = hit
                    grund = re.sub(r"\s+", " ", body[body.find(bad) + len(bad):][:160]).strip(" :.-")
                    d["unzustellbar"].append({"firma": mk["firma"], "ort": r.get("name", ""), "adresse": bad,
                        "grund": grund or "Zustellung fehlgeschlagen", "datum": today(),
                        "folge": "automatisch erkannt – Adresse deaktiviert, Alternative (Tel./Formular) prüfen"})
                    if (mk.get("email") or "").lower() == bad:
                        mk["email_ungueltig"] = mk["email"]; mk["email"] = ""; mk["mailen"] = False
                    d["statuses"][mk["id"]] = {"status": "nicht_interessant" if not mk.get("kontaktformular") else "neu",
                                               "notiz": "Mail unzustellbar " + today(), "datum": today()}
                    n_bounce += 1
                if fid:
                    requests.post(f"{G}/me/messages/{m['id']}/move", headers=H, json={"destinationId": fid}); n_moved += 1
                done.add(m["id"]); continue
            if folder not in ("inbox", "junkemail"): continue
            hit = by_email.get(frm) or by_dom.get(frm.split("@")[-1])
            if folder == "junkemail":
                if not hit: continue  # fremder Spam bleibt liegen
                requests.post(f"{G}/me/messages/{m['id']}/move", headers=H, json={"destinationId": "inbox"}); n_spam += 1
            if hit:
                r, mk = hit
                cur = d["statuses"].get(mk["id"], {}).get("status")
                if cur in (None, "neu", "email_gesendet"):
                    snippet = re.sub(r"\s+", " ", body)[:180]
                    d["statuses"][mk["id"]] = {"status": "feedback_erhalten", "datum": today(),
                        "notiz": f"Antwort {today()}: {subj[:60]} – {snippet}"}
                    n_reply += 1
            done.add(m["id"])
        json.dump(d, open(DATA, "w"), ensure_ascii=False, indent=2)
        st["done"] = sorted(done)[-1500:]; st["last"] = datetime.datetime.now().isoformat(timespec="seconds")
        json.dump(st, open(STATE, "w"))
        report("makler-mail-sync", "Makler-Mail-Sync", "ok",
               f"{n_reply} neue Antworten, {n_bounce} Rückläufer, {n_moved} nach '{FOLDER_NAME}' verschoben, {n_spam} aus Spam ins Postfach")
        print(n_reply, n_bounce, n_moved, n_spam)
    except Exception as e:
        report("makler-mail-sync", "Makler-Mail-Sync", "fehler", str(e)[:200]); raise

if __name__ == "__main__":
    main()
