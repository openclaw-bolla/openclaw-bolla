#!/usr/bin/env python3
"""Einmal-Batch: Geburtstagssong-Versand (18.11. Daria+Joëlle, 19.11. Jasmin+Louis).
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
        ("Koshkina, Daria",
         "🎂 Alles Gute zum Geburtstag, Daria! Zwei mp4s frisch aus der Musik-KI-Werkstatt – Download klicken, Boxen hoch, Beat genießen 🎶✨",
         [B + "7d/Kurs I/Happy Birthday Daria 12.01.26.mp4", B + "7d/Kurs I/Daria — Dah-REE-ah Birthday Beat 🎂💻✨.mp4"]),
        ("Bartz, Joëlle",
         "🎉 Alles Gute zum Geburtstag, Joëlle! Zwei Songs nur für dich, vertont von der Musik-KI. Download klicken, Boxen an und los 💻🎶",
         [B + "7b/Kurs I/Happy Birthday Joëlle 04.01.26.mp4", B + "7b/Kurs I/Happy Birthday Joëlle 🎂💻✨.mp4"]),
    ],
    "do": [
        ("Klein, Jasmin",
         "🎂 Alles Gute zum Geburtstag, Jasmin! Zwei Songs, extra für dich gemacht – Download klicken, aufdrehen, Klick-Rhythmus genießen 🖱️🎶",
         [B + "7a/Kurs I/Happy Birthday Jasmin 06.11.26.mp4", B + "7a/Kurs I/Yahs-MEEN → Jasmin, Birthday Click 🎂💻✨.mp4"]),
        ("Bienvenu, Louis",
         "🌟 Alles Gute zum Geburtstag, Louis! Zwei Songs mit Funken drin – Download klicken, Boxen hoch und strahlen 🔥🎶",
         [B + "7c/Kurs I/Happy Birthday Louis 29.01.26.mp4", B + "7c/Kurs I/Louis, Shine Your Light 🎂💻🔥.mp4"]),
    ],
}
CFG =json.load(open("/home/bolla/workspace/config/telegram_bot.json"))


def tg(text):
    import sys; sys.path.insert(0, "/home/bolla/workspace/scripts"); from job_status import mc_meldung  # Chris 03.11.2026: kein Telegram mehr
    return mc_meldung('itsl-geburtstagssong-1811', 'itslearning: Geburtstagssongs 18./19.11.', text)
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{CFG['bot_token']}/sendMessage",
        data=json.dumps({"chat_id": CFG["chris_id"], "text": text}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


tag = sys.argv[1]
jobs = JOBS[tag]
if datetime.datetime.now().hour < 14:
    sys.exit("vor 14 Uhr - Dauerregel")
report(f"itslearning-songs-1811-{tag}", "Geburtstagssongs", "laeuft", "sendet per itslearning")
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
    jid, jtitle = f"itslearning-songs-1811-{tag}", "Geburtstagssongs " + ", ".join(e.split(", ")[-1] for e, _, _ in jobs)
    if not fail:
        report(jid, jtitle, "ok", "gesendet: " + ", ".join(done))
    else:
        report(jid, jtitle, "fehler", f"gesendet {done or '–'}, NICHT gesendet/unklar {fail}. Screenshots /tmp/its_debug")
except BaseException as e:
    report(f"itslearning-songs-1811-{tag}", "Geburtstagssongs", "fehler", f"Abbruch {e!r}"[:300])
