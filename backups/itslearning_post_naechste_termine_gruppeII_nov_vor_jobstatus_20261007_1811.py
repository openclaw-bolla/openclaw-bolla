#!/usr/bin/env python3
""""Eure naechsten Termine"-Mitteilung fuer die 4 Gruppe-II-Kurse (7a/7b/7c/7d II) nach den
Herbstferien: Gruppe I hat 28./29.10.-18./19.11., danach kommt Gruppe II wieder dran
(Kurstag 5 am 25./26.11.2026, 4 Wochen bis 16./17.12.; Weihnachtsferien ab 21.12.).
Termine gegen data/schuljahr2627.json geprueft (05.10.2026). Text-Varianten je Klasse.
Geplant: Post am Do 08.10.2026 nachmittags (Chris), VORHER Vorschau-Screenshot in Desktop\\temp.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

COURSES = [
    ("7a_II", 190738, ("Eure nächsten Termine 📅:\n\n"
                        "Do. 26.11.26\nDo. 03.12.26\nDo. 10.12.26\nDo. 17.12.26\n\n"
                        "immer 1./2. Stunde 07:50 Uhr\n\n"
                        "Ich freue mich sehr auf Euch 😊")),
    ("7b_II", 190743, ("Hier eure nächsten Termine 📅:\n\n"
                        "Mi. 25.11.26\nMi. 02.12.26\nMi. 09.12.26\nMi. 16.12.26\n\n"
                        "immer 6./7. Stunde 12:30 Uhr\n\n"
                        "Bis bald, ich freue mich auf Euch 😊")),
    ("7c_II", 190878, ("Eure nächsten Termine im Überblick 📅:\n\n"
                        "Do. 26.11.26\nDo. 03.12.26\nDo. 10.12.26\nDo. 17.12.26\n\n"
                        "immer 6./7. Stunde 12:30 Uhr\n\n"
                        "Freue mich schon auf Euch 😊")),
    ("7d_II", 190877, ("Eure nächsten Termine 📅:\n\n"
                        "Mi. 25.11.26\nMi. 02.12.26\nMi. 09.12.26\nMi. 16.12.26\n\n"
                        "immer 1./2. Stunde 07:50 Uhr\n\n"
                        "Bis dann, ich freue mich auf Euch 😊")),
]

def tg(text):
    """Rueckmeldung an Chris per Telegram (Regel: Cron-Jobs melden immer, ob vollzogen)."""
    import json
    import urllib.request
    cfg = json.load(open("/home/bolla/workspace/config/telegram_bot.json"))
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage",
        data=json.dumps({"chat_id": cfg["chris_id"], "text": text}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    from itslearning_post_kurstag import login
    from itslearning_post_erste_termine import post_text

    post_results = []
    try:
        with sync_playwright() as p:
            browser, its = login(p)
            try:
                for name, cid, text in COURSES:
                    print(f"\n--- {name} (CourseID {cid}) ---")
                    ok = post_text(its, cid, text)
                    post_results.append((name, "OK" if ok else "FEHLGESCHLAGEN"))
            finally:
                browser.close()
    except Exception as e:
        post_results.append(("ABBRUCH", repr(e)[:200]))

    print("\n=== ZUSAMMENFASSUNG POST (4 Gruppe-II-Kurse) ===")
    for name, res in post_results:
        print(f"{name}: {res}")

    ok_all = len(post_results) == len(COURSES) and all(r == "OK" for _, r in post_results)
    msg = ("✅ itslearning: 'Eure nächsten Termine' (Gruppe II) in allen 4 Kursen gepostet 🐾" if ok_all else
           "⚠️ itslearning-Post 'nächste Termine' Gruppe II NICHT sauber durch:\n" +
           "\n".join(f"{n}: {r}" for n, r in post_results) + "\nBitte nachsehen.")
    try:
        tg(msg)
    except Exception as e:
        print("Telegram fehlgeschlagen:", e)
