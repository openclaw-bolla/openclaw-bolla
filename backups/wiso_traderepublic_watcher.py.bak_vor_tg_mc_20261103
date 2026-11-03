#!/usr/bin/env python3
"""
WISO/Trade-Republic-Depotsync-Wächter
Prüft chrismandel@wtnet.de (IMAP) auf Antwort von Buhl Data Service (WISO-Support)
zur Anfrage vom 11.08.2026 ("Trade Republic Depot lässt sich nicht synchronisieren").
Meldet eine echte Antwort per Telegram und ist damit erledigt.

Cron: 0 */4 * * * python3 /home/bolla/workspace/scripts/wiso_traderepublic_watcher.py
"""
import imaplib, json, urllib.request
from datetime import datetime, timezone
from email.header import decode_header, make_header
from pathlib import Path

CFGDIR = Path("/home/bolla/workspace/config")
TG = json.loads((CFGDIR / "telegram_bot.json").read_text())
BOT, CHRIS = TG["bot_token"], TG["chris_id"]
WTNET_CONFIG = CFGDIR / "wtnet_account.json"
STATE = CFGDIR / "wiso_traderepublic_watcher_state.json"

SENT_DATE = "2026-08-11"
IMAP_SINCE = "11-Aug-2026"
NUDGE_AFTER_DAYS = 7
SENDER_MARKERS = ["finanz@buhl-data.com", "kundenbetreuung@buhl.de"]
SUBJECT_MARKERS = ["trade republic", "traderepublic", "depot", "wiso mein geld"]
AUTOREPLY = ["this is an automated", "automatic reply", "out of office",
             "auto-reply", "automatische antwort", "abwesenheit",
             "empfangsbestätigung", "elektronisch generiert",
             "kommen unaufgefordert auf sie zu", "ihre anfrage ist bei uns eingegangen",
             "wir haben ihre anfrage erhalten", "vertragsbestätigung"]


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
    return {"seen": [], "done": False, "nudged": False}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
    STATE.chmod(0o600)


def check_wtnet(seen):
    cfg = json.loads(WTNET_CONFIG.read_text())
    m = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
    m.login(cfg["email"], cfg["password"])
    m.select("INBOX")
    # UID statt Sequenznummer verwenden! Sequenznummern verschieben sich, sobald sich der
    # Mailbox-Inhalt aendert (Mails verschoben/geloescht) - dadurch wurde am 12.08.2026 eine
    # echte neue Buhl-Antwort stillschweigend uebersprungen, weil ihre (verschobene) Sequenznummer
    # zufaellig mit einer alten, bereits gesehenen Nummer kollidierte. UIDs bleiben stabil.
    status, data = m.uid("search", None, "SINCE", IMAP_SINCE)
    ids = data[0].split()

    for mid in ids:
        key = mid.decode()
        if key in seen:
            continue
        seen.add(key)
        t, d = m.uid("fetch", mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
        if not d or not d[0]:
            continue
        raw = d[0][1].decode("utf-8", "replace")
        subject, sender = "", ""
        for line in raw.splitlines():
            low = line.lower()
            if low.startswith("subject:"):
                try:
                    subject = str(make_header(decode_header(line[8:].strip())))
                except Exception:
                    subject = line[8:].strip()
            elif low.startswith("from:"):
                try:
                    sender = str(make_header(decode_header(line[5:].strip())))
                except Exception:
                    sender = line[5:].strip()
        if not any(s in sender.lower() for s in SENDER_MARKERS):
            continue
        low_combined = (subject + " " + sender).lower()
        if any(p in low_combined for p in AUTOREPLY):
            continue
        if not any(p in subject.lower() for p in SUBJECT_MARKERS):
            continue
        t2, d2 = m.uid("fetch", mid, "(BODY.PEEK[TEXT])")
        preview = ""
        if d2 and d2[0]:
            preview = d2[0][1].decode("utf-8", "replace")[:500]
        m.logout()
        return subject, sender, preview
    m.logout()
    return None


def main():
    st = load_state()
    if st.get("done"):
        print("bereits erledigt")
        return

    seen = set(st.get("seen", []))
    try:
        hit = check_wtnet(seen)
    except Exception as e:
        hit = None
        print("wtnet-Fehler:", e)

    found = False
    if hit:
        subj, frm, preview = hit
        tg(f"📬 *WISO-Support (Buhl) hat geantwortet!*\n\n*{subj}*\nvon `{frm}`\n\n{preview}\n\n"
           f"Ging um den Trade-Republic-Depotsync in WISO Mein Geld. 🐾")
        st["done"] = True
        found = True

    st["seen"] = list(seen)[-300:]

    if not found and not st.get("done"):
        sent_dt = datetime.strptime(SENT_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        days = (datetime.now(timezone.utc) - sent_dt).days
        if days >= NUDGE_AFTER_DAYS and not st.get("nudged"):
            st["nudged"] = True
            tg(f"🤔 Keine Antwort von WISO-Support (Buhl) zum Trade-Republic-Depotsync nach {days} Tagen. "
               f"Evtl. nochmal nachfassen unter finanz@buhl-data.com.")

    save_state(st)
    print("erledigt" if st.get("done") else "läuft weiter")


if __name__ == "__main__":
    main()
