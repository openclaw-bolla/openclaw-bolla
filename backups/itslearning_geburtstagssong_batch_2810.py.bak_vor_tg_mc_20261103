#!/usr/bin/env python3
"""Einmal-Batch: Geburtstagssong-Versand (28.10. Thore+Mika, 29.10. Merle+Lena).
Nutzt Funktionen aus itslearning_send_private_song.py, loggt 1x ein, meldet per Telegram.
Aufruf: itslearning_geburtstagssong_batch_0710.py mi|do   (nur ab 14 Uhr, Dauerregel)"""
import datetime
import json
import os
import sys
import urllib.request

sys.path.insert(0, "/home/bolla/workspace/scripts")
import itslearning_send_private_song as sp
from job_status import report
from playwright.sync_api import sync_playwright

B = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/"
JOBS = {
    "mi": [
        ("Kuhn, Thore",
         "🎉 Alles Gute zum Geburtstag, Thore! Zwei mp4s mit Soundtrack: Download klicken, Lautstärke hoch, Nachbarn vorwarnen 🎤🎶",
         [B + "7d/Kurs I/Happy Birthday Thore 25.11.26.mp4", B + "7d/Kurs I/Thore Without Limits 🎂🎤🎉.mp4"]),
        ("Henneberg, Mika",
         "🎂 Alles Gute zum Geburtstag, Mika! Hier sind deine beiden Songs. Text und Style kommen von mir, die Musik-KI hat nur das Singen übernommen 🎤🎶",
         [B + "7b/Kurs I/Happy Birthday Mika 24.07.26.mp4", B + "7b/Kurs I/Happy Birthday, Mika 🎂💻🎶.mp4"]),
    ],
    "do": [
        ("Hutterer, Merle",
         "🎉 Alles Gute zum Geburtstag, Merle! Zwei mp4s, null Werbung, keine Abo-Falle 😄🎶",
         [B + "7a/Kurs I/Happy Birthday Merle 14.09.26.mp4", B + "7a/Kurs I/Hey Merle, It's Your Birthday Time! 🎂💻🎉.mp4"]),
        ("Brühl, Lena-Sophie",
         "🎂 Alles Gute zum Geburtstag, Lena! Zwei Songs, frisch aus meinem Dateiordner in dein Postfach. Bitte nicht mit Klingeltönen verwechseln 🎶💻",
         [B + "7c/Kurs I/Happy Birthday Lena-Sophie 23.10.26.mp4", B + "7c/Kurs I/Lena-Sophie — Lena, Lena Shine On 🎂💻🎶.mp4"]),
    ],
}
CFG =json.load(open("/home/bolla/workspace/config/telegram_bot.json"))


def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{CFG['bot_token']}/sendMessage",
        data=json.dumps({"chat_id": CFG["chris_id"], "text": text}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


tag = sys.argv[1]
jobs = JOBS[tag]
if datetime.datetime.now().hour < 14:
    sys.exit("vor 14 Uhr - Dauerregel")
report(f"itslearning-songs-2810-{tag}", "Geburtstagssongs", "laeuft", "sendet per itslearning")
res = []
try:
    for emp, msg, songs in jobs:
        for s in songs:
            if not os.path.isfile(s):
                raise SystemExit(f"Datei fehlt: {s}")
    with sync_playwright() as p:
        browser, its = sp.login(p)
        try:
            for k, (emp, msg, songs) in enumerate(jobs):
                if k:  # 2. Empfaenger: Panel haengt nach dem Senden -> Seite frisch laden (Fix 08.10.)
                    its.reload()
                    its.wait_for_timeout(4000)
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
    jid, jtitle = f"itslearning-songs-2810-{tag}", "Geburtstagssongs " + ", ".join(e.split(", ")[-1] for e, _, _ in jobs)
    if not fail:
        report(jid, jtitle, "ok", "gesendet: " + ", ".join(done))
    else:
        report(jid, jtitle, "fehler", f"gesendet {done or '–'}, NICHT gesendet/unklar {fail}. Screenshots /tmp/its_debug")
except BaseException as e:
    report(f"itslearning-songs-2810-{tag}", "Geburtstagssongs", "fehler", f"Abbruch {e!r}"[:300])
