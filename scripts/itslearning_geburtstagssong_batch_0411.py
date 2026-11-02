#!/usr/bin/env python3
"""Einmal-Batch: Geburtstagssong-Versand (04.11. Jna+Lukas, 05.11. Joana+Morten).
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
        ("Al-Maliki, Jna",
         "🎉 Alles Gute zum Geburtstag, Jna! Zwei mp4s als Soundtrack für dich: Download klicken, Lautstärke hoch, Nachbarn vorwarnen 🎤🎶",
         [B + "7d/Kurs I/Happy Birthday Jna 26.11.26.mp4", B + "7d/Kurs I/Jna, Shine On 🎂💻✨.mp4"]),
        ("Bunsen, Lukas",
         "🎂 Nachträglich alles Gute zum Geburtstag, Lukas! Hier sind deine beiden Songs. Text und Style kommen von mir, die Musik-KI hat nur das Singen übernommen 🎤🎶",
         [B + "7b/Kurs I/Happy Birthday Lukas 30.09.26.mp4", B + "7b/Kurs I/🎂 Lukas, Click Your Way to a Brilliant Year 💻🎉.mp4"]),
    ],
    "do": [
        ("Hausch, Joana",
         "🎉 Nachträglich alles Gute zum Geburtstag, Joana! Zwei mp4s, null Werbung, keine Abo-Falle – einmal davon mit Einhorn 🦄🎶",
         [B + "7a/Kurs I/Happy Birthday Joana 04.10.26.mp4", B + "7a/Kurs I/Joana's and the Unicorn 🦄🎂💻.mp4"]),
        ("Friese, Morten",
         "🎂 Alles Gute zum Geburtstag, Morten! Zwei Songs, frisch aus meinem Dateiordner in dein Postfach. Bitte nicht mit Klingeltönen verwechseln 🎶☀️",
         [B + "7c/Kurs I/Happy Birthday Morten 10.11.26.mp4", B + "7c/Kurs I/Shine On, Morten 🎂☀️💻.mp4"]),
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
report(f"itslearning-songs-0411-{tag}", "Geburtstagssongs", "laeuft", "sendet per itslearning")
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
    jid, jtitle = f"itslearning-songs-0411-{tag}", "Geburtstagssongs " + ", ".join(e.split(", ")[-1] for e, _, _ in jobs)
    if not fail:
        report(jid, jtitle, "ok", "gesendet: " + ", ".join(done))
    else:
        report(jid, jtitle, "fehler", f"gesendet {done or '–'}, NICHT gesendet/unklar {fail}. Screenshots /tmp/its_debug")
except BaseException as e:
    report(f"itslearning-songs-0411-{tag}", "Geburtstagssongs", "fehler", f"Abbruch {e!r}"[:300])
