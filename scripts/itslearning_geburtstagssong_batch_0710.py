#!/usr/bin/env python3
"""Einmal-Batch: Geburtstagssong-Versand (07.10. Matilda+Emma Michel, 08.10. Henny+Eva).
Nutzt Funktionen aus itslearning_send_private_song.py, loggt 1x ein, meldet per Telegram.
Aufruf: itslearning_geburtstagssong_batch_0710.py mi|do   (nur ab 14 Uhr, Dauerregel)"""
import datetime
import json
import os
import sys
import urllib.request

sys.path.insert(0, "/home/bolla/workspace/scripts")
import itslearning_send_private_song as sp
from playwright.sync_api import sync_playwright

B = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/"
JOBS = {
    "mi": [
        ("Scholz, Matilda",
         "🎉 Alles Gute zum Geburtstag, Matilda! Hier sind deine beiden Songs. Text und Style kommen von mir, die Musik-KI hat nur das Singen übernommen 🎤🎶",
         [B + "7d/Kurs II/Happy Birthday Matilda 02.08.26.mp4", B + "7d/Kurs II/Hey Hey Matilda! 🎂🎉💻.mp4"]),
        ("Michel, Emma Sophia",
         "🎂 Alles Gute zum Geburtstag, Emma! Zwei mp4s mit Soundtrack: Download klicken, Lautstärke hoch, Nachbarn vorwarnen ⚽🎶",
         [B + "7b/Kurs II/Happy Birthday Emma 05.10.26.mp4", B + "7b/Kurs II/Emma – Guardian of the Line ⚽🛡️🔥.mp4"]),
    ],
    "do": [
        ("Zock, Henny",
         "🎉 Alles Gute zum Geburtstag, Henny! Zwei mp4s, null Werbung, keine Abo-Falle 😄🎶",
         [B + "7a/Kurs II/Happy Birthday Henny 27.07.26.mp4", B + "7a/Kurs II/Heh-nee's Birthday Groove 🎂💻🎉 (Henny).mp4"]),
        ("Wassermann, Eva",
         "🎂 Alles Gute zum Geburtstag, Eva! Zwei Songs, frisch aus meinem Dateiordner in dein Postfach. Bitte nicht mit Klingeltönen verwechseln 🎶💻",
         [B + "7c/Kurs II/Happy Birthday Eva 19.08.26.mp4", B + "7c/Kurs II/Ay-fah Eva's Birthday Beat 🎂💻🎉.mp4"]),
    ],
}
CFG = json.load(open("/home/bolla/workspace/config/telegram_bot.json"))


def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{CFG['bot_token']}/sendMessage",
        data=json.dumps({"chat_id": CFG["chris_id"], "text": text}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


tag = sys.argv[1]
jobs = JOBS[tag]
if datetime.datetime.now().hour < 14:
    sys.exit("vor 14 Uhr - Dauerregel")
res = []
try:
    for emp, msg, songs in jobs:
        for s in songs:
            if not os.path.isfile(s):
                raise SystemExit(f"Datei fehlt: {s}")
    with sync_playwright() as p:
        browser, its = sp.login(p)
        try:
            for emp, msg, songs in jobs:
                try:
                    ok = sp.send_private_message(its, emp, msg, songs)
                except Exception as e:
                    print(emp, repr(e))
                    ok = False
                res.append((emp, ok))
                if not ok:
                    break  # Panel-Zustand unklar -> nicht blind weitersenden
        finally:
            browser.close()
    done = [e for e, o in res if o]
    fail = [e for e, _, _ in jobs if e not in done]
    tg(("✅ Geburtstagssongs gesendet: " + ", ".join(done) + " 🐾") if not fail else
       f"⚠️ Geburtstagssongs: gesendet {done or '–'}, NICHT gesendet/unklar {fail}. Screenshots /tmp/its_debug")
except BaseException as e:
    tg(f"⚠️ Geburtstagssong-Batch {tag}: Abbruch {e!r}"[:500])
