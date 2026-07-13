#!/usr/bin/env python3
"""
ADAC-Kündigungs-Wächter
Prüft ernstmandel@outlook.de (Graph) auf Antwort vom ADAC zur Kündigung
(Mitgliedsnummer 098585320, Mail vom 13.07.2026 an service@adac.de).
Meldet eine Antwort per Telegram und ist damit erledigt.
Kommt nach 14 Tagen keine Antwort, schickt das Skript automatisch eine
Nachfass-Mail und meldet das per Telegram. Bleibt es auch danach 14 Tage
still, kommt ein Telegram-Hinweis, dass Chris besser selbst anruft.

Cron: 0 */4 * * * python3 /home/bolla/workspace/scripts/adac_kuendigung_watcher.py
"""
import json, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from outlook_oauth2 import refresh_access_token as send_token  # Scope Mail.Send

CFGDIR = Path("/home/bolla/workspace/config")
TG = json.loads((CFGDIR / "telegram_bot.json").read_text())
BOT, CHRIS = TG["bot_token"], TG["chris_id"]
OAUTH = json.loads((CFGDIR / "outlook_oauth2.json").read_text())
TOKF = CFGDIR / "outlook_token.json"
STATE = CFGDIR / "adac_kuendigung_watcher_state.json"

SENT_DATE = "2026-07-13"
MITGLIEDSNUMMER = "098585320"
FOLLOWUP_AFTER_DAYS = 14
ESCALATE_AFTER_DAYS = 14  # nach der Nachfass-Mail
AUTOREPLY = ["this is an automated", "automatic reply", "out of office",
             "auto-reply", "automatische antwort", "abwesenheit",
             "empfangsbestätigung", "elektronisch generiert",
             "kommen unaufgefordert auf sie zu",
             "bitten wir sie, nicht an diese e-mail-adresse zu antworten"]


def tg(text):
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.telegram.org/bot{BOT}/sendMessage",
            data=json.dumps({"chat_id": CHRIS, "text": text, "parse_mode": "Markdown",
                              "disable_web_page_preview": True}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
    except Exception as e:
        print("tg err", e)


def read_token():
    """Access-Token mit Lese-Scope holen (Refresh-Token erlaubt Teilmenge der Original-Scopes)."""
    cfg, tok = OAUTH, json.loads(TOKF.read_text())
    data = urllib.parse.urlencode({'client_id': cfg['client_id'], 'client_secret': cfg['client_secret'],
                                    'refresh_token': tok['refresh_token'], 'grant_type': 'refresh_token',
                                    'scope': 'Mail.ReadWrite offline_access'}).encode()
    new = json.loads(urllib.request.urlopen(urllib.request.Request(
        'https://login.microsoftonline.com/consumers/oauth2/v2.0/token', data=data, method='POST')).read())
    tok.update(new)
    TOKF.write_text(json.dumps(tok, indent=2))
    TOKF.chmod(0o600)
    return new['access_token']


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"seen": [], "done": False, "followup_sent": False, "followup_date": None, "escalated": False}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
    STATE.chmod(0o600)


def send_followup():
    body = (
        "Sehr geehrte Damen und Herren,\n\n"
        f"am {datetime.strptime(SENT_DATE, '%Y-%m-%d').strftime('%d.%m.%Y')} habe ich meine ADAC-Mitgliedschaft "
        f"(Mitgliedsnummer {MITGLIEDSNUMMER}, Ernst Christoph Mandel, Buchenweg 67a, 22846 Norderstedt) "
        "gekündigt, bislang aber noch keine Bestätigung erhalten.\n\n"
        "Ich bitte um kurze Bestätigung der Kündigung unter Angabe des Beendigungsdatums.\n\n"
        "Vielen Dank und freundliche Grüße\nErnst Christoph Mandel"
    )
    at = send_token()
    h = {"Authorization": f"Bearer {at}", "Content-Type": "application/json"}
    msg = {"message": {"subject": f"Nachfrage zu meiner Kündigung, Mitgliedsnummer {MITGLIEDSNUMMER}",
                        "body": {"contentType": "Text", "content": body},
                        "toRecipients": [{"emailAddress": {"address": "service@adac.de"}}]},
           "saveToSentItems": True}
    r = urllib.request.urlopen(urllib.request.Request(
        "https://graph.microsoft.com/v1.0/me/sendMail", data=json.dumps(msg).encode(),
        headers=h, method="POST"))
    return r.status == 202


def main():
    st = load_state()
    if st.get("done"):
        print("bereits erledigt")
        return

    seen = set(st.get("seen", []))
    at = read_token()
    qs = urllib.parse.urlencode({'$top': '30', '$orderby': 'receivedDateTime desc',
                                  '$select': 'id,subject,from,receivedDateTime,bodyPreview'})
    url = "https://graph.microsoft.com/v1.0/me/messages?" + qs
    res = json.loads(urllib.request.urlopen(urllib.request.Request(
        url, headers={"Authorization": f"Bearer {at}"})).read())

    found = False
    for m in res.get("value", []):
        mid = m["id"]
        if mid in seen:
            continue
        seen.add(mid)
        frm = (m.get("from", {}).get("emailAddress", {}).get("address", "") or "").lower()
        if not frm.endswith("@adac.de"):
            continue
        body = (m.get("bodyPreview") or "").lower()
        if any(p in body for p in AUTOREPLY):
            continue
        subj = m.get("subject") or "(kein Betreff)"
        if any(p in subj.lower() for p in AUTOREPLY):
            continue  # Auto-Reply/OOO auch im Betreff erkennen
        when = (m.get("receivedDateTime") or "")[:16].replace("T", " ")
        preview = m.get("bodyPreview") or ""
        tg(f"📬 *ADAC hat geantwortet!*\n\n*{subj}*\nvon `{frm}`, {when}\n\n{preview[:400]}\n\n"
           f"Kündigung Mitgliedsnummer {MITGLIEDSNUMMER} damit erledigt. 🐾")
        st["done"] = True
        found = True
        break
    st["seen"] = list(seen)[-200:]

    if not found and not st.get("done"):
        sent_dt = datetime.strptime(SENT_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        days = (datetime.now(timezone.utc) - sent_dt).days
        if days >= FOLLOWUP_AFTER_DAYS and not st.get("followup_sent"):
            ok = send_followup()
            st["followup_sent"] = True
            st["followup_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            if ok:
                tg(f"📮 Keine ADAC-Antwort nach {days} Tagen — hab automatisch nachgehakt "
                   f"(Nachfass-Mail an service@adac.de raus). Melde mich, sobald eine Antwort kommt.")
            else:
                tg("⚠️ Wollte beim ADAC nachhaken, Mail-Versand ist aber fehlgeschlagen — bitte kurz selbst schauen.")
        elif st.get("followup_sent") and not st.get("escalated"):
            fu_dt = datetime.strptime(st["followup_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            days_since_fu = (datetime.now(timezone.utc) - fu_dt).days
            if days_since_fu >= ESCALATE_AFTER_DAYS:
                st["escalated"] = True
                tg(f"🤔 Auch auf die Nachfass-Mail kam nach {days_since_fu} Tagen keine Antwort vom ADAC. "
                   f"Ich würde jetzt kurz anrufen: 089 558 95 96 97 (Mitgliedsnummer {MITGLIEDSNUMMER}).")

    save_state(st)
    print("erledigt" if st.get("done") else "läuft weiter")


if __name__ == "__main__":
    main()
