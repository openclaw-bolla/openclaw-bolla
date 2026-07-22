#!/usr/bin/env python3
"""
ADAC-Kündigungs-Wächter für Reni (renatemandel@wtnet.de, IMAP).
Prüft auf Antwort vom ADAC zur Kündigung ihrer Partner-Mitgliedschaft
(unter Mitgliedsnummer 098585320 von Chris, Mail vom 22.07.2026 an service@adac.de).
Meldet eine Antwort per Telegram und ist damit erledigt.
Kommt nach 14 Tagen keine Antwort, schickt das Skript automatisch eine
Nachfass-Mail und meldet das per Telegram. Bleibt es auch danach 14 Tage
still, kommt ein Telegram-Hinweis, dass Chris/Reni besser selbst anrufen.

Cron: 0 */4 * * * python3 /home/bolla/workspace/scripts/reni_adac_kuendigung_watcher.py
"""
import imaplib, json, ssl, sys, urllib.request
from datetime import datetime, timezone
from email import message_from_bytes
from email.header import decode_header
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from reni_mail import load as load_reni_cfg, send_mail as reni_send_mail

CFGDIR = Path("/home/bolla/workspace/config")
TG = json.loads((CFGDIR / "telegram_bot.json").read_text())
BOT, CHRIS = TG["bot_token"], TG["chris_id"]
STATE = CFGDIR / "reni_adac_kuendigung_watcher_state.json"

SENT_DATE = "2026-07-22"
MITGLIEDSNUMMER = "098585320"
FOLLOWUP_AFTER_DAYS = 14
ESCALATE_AFTER_DAYS = 14
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


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"seen": [], "done": False, "followup_sent": False, "followup_date": None, "escalated": False}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
    STATE.chmod(0o600)


def decode_str(s):
    if not s:
        return ""
    parts = decode_header(s)
    out = ""
    for text, enc in parts:
        if isinstance(text, bytes):
            out += text.decode(enc or "utf-8", errors="replace")
        else:
            out += text
    return out


def send_followup():
    body = (
        "Sehr geehrte Damen und Herren,\n\n"
        f"am {datetime.strptime(SENT_DATE, '%Y-%m-%d').strftime('%d.%m.%Y')} habe ich meine ADAC-Partner-"
        f"Mitgliedschaft (geführt unter der Mitgliedsnummer meines Mannes Ernst-Christoph Mandel, "
        f"{MITGLIEDSNUMMER}, Buchenweg 67a, 22846 Norderstedt) gekündigt, bislang aber noch keine "
        "Bestätigung erhalten.\n\n"
        "Ich bitte um kurze Bestätigung der Kündigung unter Angabe des Beendigungsdatums.\n\n"
        "Vielen Dank und freundliche Grüße\nRenate Mandel"
    )
    reni_send_mail("service@adac.de", f"Nachfrage zu meiner Kündigung, Mitgliedsnummer {MITGLIEDSNUMMER}", body)
    return True


def main():
    st = load_state()
    if st.get("done"):
        print("bereits erledigt")
        return

    d = load_reni_cfg()
    if not d.get("password"):
        print("kein Passwort gesetzt, breche ab")
        return

    seen = set(st.get("seen", []))
    found = False

    ctx = ssl.create_default_context()
    with imaplib.IMAP4_SSL(d["imap"], d["imap_port"], ssl_context=ctx) as m:
        m.login(d["email"], d["password"])
        m.select("INBOX")
        typ, data = m.search(None, 'FROM', '"adac.de"')
        ids = data[0].split() if data and data[0] else []
        for uid in ids[-30:]:
            uid_s = uid.decode()
            if uid_s in seen:
                continue
            seen.add(uid_s)
            typ, msgdata = m.fetch(uid, "(RFC822)")
            if not msgdata or not msgdata[0]:
                continue
            msg = message_from_bytes(msgdata[0][1])
            frm = (msg.get("From") or "").lower()
            if "adac.de" not in frm:
                continue
            subj = decode_str(msg.get("Subject") or "(kein Betreff)")
            preview = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            preview = part.get_payload(decode=True).decode(
                                part.get_content_charset() or "utf-8", errors="replace")
                        except Exception:
                            pass
                        break
            else:
                try:
                    preview = msg.get_payload(decode=True).decode(
                        msg.get_content_charset() or "utf-8", errors="replace")
                except Exception:
                    pass
            low = (preview + " " + subj).lower()
            if any(p in low for p in AUTOREPLY):
                continue
            when = msg.get("Date") or ""
            tg(f"📬 *ADAC hat auf Renis Kündigung geantwortet!*\n\n*{subj}*\nvon `{frm}`, {when}\n\n"
               f"{preview[:400]}\n\nRenis Partner-Mitgliedschaft (zu {MITGLIEDSNUMMER}) damit erledigt. 🐾")
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
                tg(f"📮 Keine ADAC-Antwort auf Renis Kündigung nach {days} Tagen — hab automatisch "
                   f"nachgehakt (Nachfass-Mail an service@adac.de raus). Melde mich, sobald eine Antwort kommt.")
            else:
                tg("⚠️ Wollte beim ADAC für Renis Kündigung nachhaken, Mail-Versand ist aber "
                   "fehlgeschlagen — bitte kurz selbst schauen.")
        elif st.get("followup_sent") and not st.get("escalated"):
            fu_dt = datetime.strptime(st["followup_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            days_since_fu = (datetime.now(timezone.utc) - fu_dt).days
            if days_since_fu >= ESCALATE_AFTER_DAYS:
                st["escalated"] = True
                tg(f"🤔 Auch auf die Nachfass-Mail zu Renis ADAC-Kündigung kam nach {days_since_fu} Tagen "
                   f"keine Antwort. Am besten anrufen: 089 558 95 96 97 (Mitgliedsnummer {MITGLIEDSNUMMER}).")

    save_state(st)
    print("erledigt" if st.get("done") else "läuft weiter")


if __name__ == "__main__":
    main()
