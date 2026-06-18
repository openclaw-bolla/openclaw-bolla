#!/usr/bin/env python3
"""
AURORA Shop-Wächter
Prüft regelmäßig, ob AURORA (Chris Mandel) in den großen Shops gelistet ist,
und meldet via Telegram: die ERSTEN 3 entdeckten Shops + GARANTIERT Tolino/Thalia.
Stoppt (still) sobald 3 Shops + Tolino gemeldet sind.

Cron: 0 */6 * * * python3 /home/bolla/workspace/scripts/aurora_shop_watcher.py
"""

import json
import re
import sys
import requests
from pathlib import Path

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT_TOKEN = CFG["bot_token"]
CHRIS_ID  = CFG["chris_id"]

STATE_PATH = Path("/home/bolla/workspace/config/aurora_watcher_state.json")
TITLE = "AURORA"
AUTHOR = "Chris Mandel"
QUERY = "AURORA Chris Mandel"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"reported": [], "tolino_reported": False, "done": False}

def save_state(s):
    STATE_PATH.write_text(json.dumps(s, indent=2, ensure_ascii=False))

def tg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      json={"chat_id": CHRIS_ID, "text": text, "parse_mode": "Markdown",
                            "disable_web_page_preview": False},
                      timeout=20)
    except Exception as e:
        print("Telegram-Fehler:", e)

# ---------- einzelne Shop-Checks: geben (available, link) zurück ----------
def check_apple():
    try:
        r = requests.get("https://itunes.apple.com/search",
                         params={"term": QUERY, "media": "ebook", "entity": "ebook",
                                 "country": "DE", "limit": 25}, timeout=20)
        for it in r.json().get("results", []):
            name = (it.get("trackName") or "").lower()
            art  = (it.get("artistName") or "").lower()
            if "aurora" in name and "mandel" in art:
                return True, it.get("trackViewUrl", "https://books.apple.com")
    except Exception as e:
        print("apple err", e)
    return False, None

def check_google():
    try:
        r = requests.get("https://www.googleapis.com/books/v1/volumes",
                         params={"q": 'intitle:AURORA inauthor:"Chris Mandel"', "country": "DE"},
                         timeout=20)
        for it in r.json().get("items", []):
            vi = it.get("volumeInfo", {})
            title = (vi.get("title") or "").lower()
            authors = " ".join(vi.get("authors", [])).lower()
            if "aurora" in title and "mandel" in authors:
                return True, vi.get("infoLink", "https://play.google.com/store/books")
    except Exception as e:
        print("google err", e)
    return False, None

def _scrape_has(url):
    """True, wenn Seite sowohl AURORA als auch 'Chris Mandel'/'Mandel' enthält."""
    try:
        r = requests.get(url, headers=UA, timeout=25)
        html = r.text.lower()
        return ("aurora" in html) and ("chris mandel" in html or "mandel, chris" in html)
    except Exception as e:
        print("scrape err", url, e)
        return False

def check_kobo():
    url = "https://www.kobo.com/de/de/search?query=" + requests.utils.quote(QUERY)
    return (_scrape_has(url), url)

def check_thalia():
    # Tolino-Verbund liefert an Thalia -> bester DE-Indikator
    url = "https://www.thalia.de/suche?sq=" + requests.utils.quote(QUERY)
    return (_scrape_has(url), url)

def check_amazon():
    url = "https://www.amazon.de/s?k=" + requests.utils.quote(QUERY + " kindle")
    return (_scrape_has(url), url)

# Reihenfolge = Prioritaet fuer "erste 3"
SHOPS = [
    ("Apple Books", check_apple),
    ("Amazon Kindle", check_amazon),
    ("Kobo", check_kobo),
    ("Google Play", check_google),
    ("Tolino / Thalia", check_thalia),
]

def main():
    st = load_state()
    if st.get("done"):
        return  # fertig, nichts mehr tun

    for name, fn in SHOPS:
        if name in st["reported"]:
            continue
        try:
            available, link = fn()
        except Exception as e:
            print(name, "check exception", e)
            continue
        if not available:
            continue

        is_tolino = "tolino" in name.lower()
        # Melden, wenn noch unter 3 ODER es Tolino ist
        if len(st["reported"]) < 3 or is_tolino:
            st["reported"].append(name)
            if is_tolino:
                st["tolino_reported"] = True
                tg(f"📚 *AURORA bei Tolino/Thalia live!* 🎉\n\n"
                   f"Der deutsche Marktführer führt jetzt dein Buch:\n{link}\n\n🐾")
            else:
                n = len([x for x in st["reported"] if "tolino" not in x.lower()])
                ubl = ""
                if not st.get("ubl_announced"):
                    st["ubl_announced"] = True
                    ubl = ("\n\n🔗 Dein Books2Read-Link dürfte jetzt aktiv sein:\n"
                           "DE: https://books2read.com/u/bz0nwj\n"
                           "(EN-Link analog auf der D2D View-Book-Seite)")
                tg(f"📚 *AURORA ist live!* 🎉\n\n"
                   f"*{name}* führt jetzt dein Buch:\n{link}\n\n"
                   f"(Shop {min(n,3)}/3 entdeckt){ubl}\n🐾")
            save_state(st)

    # Abschluss: 3 Shops + Tolino gemeldet -> Waechter einstellen
    non_tolino = [x for x in st["reported"] if "tolino" not in x.lower()]
    if len(non_tolino) >= 3 and st.get("tolino_reported"):
        st["done"] = True
        save_state(st)
        tg("✅ *AURORA-Wächter fertig.*\n"
           "Die ersten 3 Shops + Tolino sind gemeldet — ich beende die Überwachung. 🐾")

if __name__ == "__main__":
    main()
