#!/usr/bin/env python3
"""Einmal-Batch: Geburtstagssong-Versand (11.11. Noah+Henri, 12.11. Haley+Philip, 10.11. Morten).
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
        ("Li, Noah",
         "🚀 Alles Gute zum Geburtstag, Noah! Zwei mp4s im Anhang – Download klicken, Boxen hoch, Raumschiff starten 🎶",
         [B + "7d/Kurs I/Happy Birthday Noah 15.12.26.mp4", B + "7d/Kurs I/🚀 Fly, Noah, Fly! 🎂✨.mp4"]),
        ("Bratke, Henri",
         "🎂 Alles Gute zum Geburtstag, Henri! Zwei Songs, Text und Style Marke Eigenbau, vertont von der Musik-KI. Tastatur bereithalten ⌨️🎶",
         [B + "7b/Kurs I/Happy Birthday Henri 23.12.26.mp4", B + "7b/Kurs I/Henri, Hit the Key 🎂💻🔥.mp4"]),
    ],
    "do": [
        ("Brandt, Haley",
         "🎉 Alles Gute zum Geburtstag, Haley! Zwei mp4s frisch aus der Musik-KI-Werkstatt, lauter als dein Kopfhörer es mag 🎤💃",
         [B + "7a/Kurs I/Happy Birthday Haley 23.10.26.mp4", B + "7a/Kurs I/Hay-lee Dai Dai Birthday 🎂💃🎶 Haley.mp4"]),
        ("Do, Philip",
         "🔥 Alles Gute zum Geburtstag, Philip! Zwei Songs, einer davon dein Wunsch-Phonk mit Cowbell. Lautstärke auf eigene Verantwortung 🔔🎧",
         [B + "7c/Kurs I/Happy Birthday Philip 29.12.26.mp4", B + "7c/Kurs I/🔥🎂 Philip on the Beat 🔔🎧.mp4"]),
    ],
    "di": [
        ("Friese, Morten",
         "🎂🔥 Alles Gute zum Geburtstag, Morten! Hier ist dein Wunsch-Song: Phonk, Cowbell inklusive. Lautstärke auf eigene Verantwortung 🔔🎧",
         [B + "7c/Kurs I/🔥🎂 Morten Drops the Beat 🔔🎧.mp4"]),
    ],
}
CFG =json.load(open("/home/bolla/workspace/config/telegram_bot.json"))


def tg(text):
    import sys; sys.path.insert(0, "/home/bolla/workspace/scripts"); from job_status import mc_meldung  # Chris 03.11.2026: kein Telegram mehr
    return mc_meldung('itsl-geburtstagssong-1111', 'itslearning: Geburtstagssongs 11./12.11.', text)
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{CFG['bot_token']}/sendMessage",
        data=json.dumps({"chat_id": CFG["chris_id"], "text": text}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


tag = sys.argv[1]
jobs = JOBS[tag]
if datetime.datetime.now().hour < 14:
    sys.exit("vor 14 Uhr - Dauerregel")
report(f"itslearning-songs-1111-{tag}", "Geburtstagssongs", "laeuft", "sendet per itslearning")
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
    jid, jtitle = f"itslearning-songs-1111-{tag}", "Geburtstagssongs " + ", ".join(e.split(", ")[-1] for e, _, _ in jobs)
    if not fail:
        report(jid, jtitle, "ok", "gesendet: " + ", ".join(done))
    else:
        report(jid, jtitle, "fehler", f"gesendet {done or '–'}, NICHT gesendet/unklar {fail}. Screenshots /tmp/its_debug")
except BaseException as e:
    report(f"itslearning-songs-1111-{tag}", "Geburtstagssongs", "fehler", f"Abbruch {e!r}"[:300])
