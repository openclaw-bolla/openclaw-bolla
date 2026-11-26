#!/usr/bin/env python3
"""Einmal-Batch: Geburtstagssong-Versand (02.12. Arthur+Emma, 03.12. Felix+Ceyda).
Nutzt Funktionen aus itslearning_send_private_song.py, loggt 1x ein, meldet per Telegram.
Aufruf: itslearning_geburtstagssong_batch_0212.py mi|do   (nur ab 14 Uhr, Dauerregel)"""
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
SUCHE = {"Urak, Ceyda": "Ceyda"}  # voller Name liefert keine Treffer
JOBS = {
    "mi": [
        ("Wolf, Arthur",
         "🎩 Alles Gute zum Geburtstag, Arthur! Kleiner Zaubertrick: eine Nachricht, zwei Songs. Download klicken, Lautsprecher an, Simsalabim ✨🎶",
         [B + "7d/Kurs II/Happy Birthday Arthur 10.12.26.mp4", B + "7d/Kurs II/Abracadabra, Arthur! 🎩✨💻🎂.mp4"]),
        ("Pietschner, Emma",
         "🎉 Alles Gute zum Geburtstag, Emma! Hier kommen zwei MP4s mit eingebauter guter Laune. Systemanforderung: nur Ohren und ein bisschen Lautstärke 💻🎶",
         [B + "7b/Kurs II/Happy Birthday Emma 22.10.26.mp4", B + "7b/Kurs II/Emma, the Computer Class Star 💻🎉.mp4"]),
    ],
    "do": [
        ("Möller, Felix",
         "🥳 Alles Gute zum Geburtstag, Felix! Dein Download-Ordner bekommt heute Party-Besuch: zwei Songs, bitte nicht leise abspielen 🔊🎂",
         [B + "7a/Kurs II/Happy Birthday Felix 27.11.26.mp4", B + "7a/Kurs II/Feh-liks Never Stops the Party 🎂💻🎉 (Felix).mp4"]),
        ("Urak, Ceyda",
         "🌟 Alles Gute zum Geburtstag, Ceyda! Zwei Songs frisch aus der Musik-KI-Werkstatt. Einmal Download, beliebig oft Replay 🎧🎂",
         [B + "7c/Kurs II/Happy Birthday Ceyda 12.12.26.mp4", B + "7c/Kurs II/🎂 Ceyda, Birthday Star of the Computer Class 💻🎉.mp4"]),
    ],
}
CFG =json.load(open("/home/bolla/workspace/config/telegram_bot.json"))


def tg(text):
    import sys; sys.path.insert(0, "/home/bolla/workspace/scripts"); from job_status import mc_meldung  # Chris 03.11.2026: kein Telegram mehr
    return mc_meldung('itsl-geburtstagssong-0212', 'itslearning: Geburtstagssongs 02./03.12.', text)
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{CFG['bot_token']}/sendMessage",
        data=json.dumps({"chat_id": CFG["chris_id"], "text": text}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


tag = sys.argv[1]
jobs = JOBS[tag]
if datetime.datetime.now().hour < 14:
    sys.exit("vor 14 Uhr - Dauerregel")
report(f"itslearning-songs-0212-{tag}", "Geburtstagssongs", "laeuft", "sendet per itslearning")
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
                    ok = sp.send_private_message(its, emp, msg, songs, SUCHE.get(emp))
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
    jid, jtitle = f"itslearning-songs-0212-{tag}", "Geburtstagssongs " + ", ".join(e.split(", ")[-1] for e, _, _ in jobs)
    if not fail:
        report(jid, jtitle, "ok", "gesendet: " + ", ".join(done))
    else:
        report(jid, jtitle, "fehler", f"gesendet {done or '–'}, NICHT gesendet/unklar {fail}. Screenshots /tmp/its_debug")
except BaseException as e:
    report(f"itslearning-songs-0212-{tag}", "Geburtstagssongs", "fehler", f"Abbruch {e!r}"[:300])
