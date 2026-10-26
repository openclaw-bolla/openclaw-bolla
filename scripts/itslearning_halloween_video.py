#!/usr/bin/env python3
"""Halloween-Mitteilung (Fr 30.10.2026) an alle 8 Kurse der 7a-7d, je Klasse ein eigenes 26-s-Video.
Stand: NUR TEXTE/Vorschau - noch nicht gepostet (wartet auf Chris' Freigabe am Freitag)."""
STAGE = "/home/bolla/workspace/state/halloween_video"
TEXTE = {
 "7a": "Buuuh, liebe 7a! 👻🎃\n\nIn der Nacht zu Samstag ist Halloween – und weil ich euch kenne, dass ihr nach Süßem lechzt wie Vampire nach … na ja, ihr wisst schon 🧛, hänge ich euch unten einen kleinen gruseligen Film an. Nur 26 Sekunden, ganz ohne Jumpscares. Versprochen!\n\nTipp: Ton an 🔊, Licht aus 🕯️ und die Süßigkeiten bitte erst NACH dem Video aufessen 🍬\n\nEuer Herr Mandel 🦇",
 "7b": "Happy Halloween, 7b! 🎃🕷️\n\nHeute Nacht gehen die Geister um – und ich habe eine Warnung für euch: Wer zu viele Süßigkeiten sammelt, wird am Montag selbst zum Zombie 🧟 Zum Aufwärmen gibt's unten ein kurzes Halloween-Video (26 Sekunden Gänsehaut, leicht gesüßt 🍭).\n\nKürbis schnitzen 🔪, Kostüm basteln 🧙, Klingeln mit Anstand – und kommt heil wieder 😉\n\nBis zum nächsten Mal! 🦇 Euer Herr Mandel",
 "7c": "Hallo 7c, hier spricht der Kürbis! 🎃🗣️\n\nOk, eigentlich Herr Mandel – aber der Kürbis hat das Video mitgebracht, das ihr unten findet: 26 Sekunden Halloween-Stimmung für euer Handy oder den Laptop.\n\nIch wünsche euch ein gruselig-schönes Wochenende 👻 mit viel Süßem 🍫, wenig Bauchweh 🤢 und Kostümen, bei denen man sich kaputtlacht 😂\n\nBleibt mir bis Montag unverwest! 🧟‍♂️🦇",
 "7d": "Grüß euch, 7d! 🦇👻\n\nZu Halloween bekommt ihr von mir ein kleines Geschenk: ein 26-Sekunden-Video (unten zum Download) – gruselig genug für Gänsehaut, harmlos genug für die Oma 👵🎃\n\nDenkt dran: Heute dürfen Skelette 💀, Hexen 🧙‍♀️ und Vampire 🧛 klingeln – aber nur bis 21 Uhr und bitte immer freundlich fragen, ob's Süßes oder Saures gibt 🍬\n\nHuhuuu und bis bald! 🕸️ Euer Herr Mandel",
}
COURSES = [
 ("7a_I", 190735, "7a"), ("7b_I", 190741, "7b"), ("7c_I", 190861, "7c"), ("7d_I", 190860, "7d"),
 ("7a_II", 190738, "7a"), ("7b_II", 190743, "7b"), ("7c_II", 190878, "7c"), ("7d_II", 190877, "7d"),
]
def files_for(k):
    return [{"path": f"{STAGE}/Halloween {k}.mp4", "basename": f"Halloween {k}", "filename": f"Halloween {k}.mp4"}]

if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from job_status import report as _r
    _r("itslearning-halloween", "Halloween-Video (8 Kurse)", "laeuft", "postet in 8 Kursen")
    from playwright.sync_api import sync_playwright
    from itslearning_post_kurstag import login, upload_files, post_message
    from itslearning_post_naechste_termine_gruppeII_nov import tg
    res = []
    try:
        with sync_playwright() as p:
            browser, its = login(p)
            try:
                for name, cid, k in COURSES:
                    print(f"\n--- {name} ({cid}) ---")
                    F = files_for(k)
                    if not upload_files(its, cid, F):
                        res.append((name, "UPLOAD FEHLGESCHLAGEN")); continue
                    res.append((name, "OK" if post_message(its, cid, TEXTE[k], F) else "POST FEHLGESCHLAGEN"))
            finally:
                browser.close()
    except Exception as e:
        res.append(("ABBRUCH", repr(e)[:200]))
    ok = len(res) == len(COURSES) and all(r == "OK" for _, r in res)
    summ = "; ".join(f"{n}: {r}" for n, r in res)
    print(summ)
    try:
        _r("itslearning-halloween", "Halloween-Video (8 Kurse)", "ok" if ok else "fehler",
           "in allen 8 Kursen gepostet" if ok else summ + " – bitte nachsehen")
        tg("✅ Halloween-Video in allen 8 Kursen gepostet" if ok else "⚠️ Halloween-Video: " + summ)
    except Exception as e:
        print("Meldung fehlgeschlagen:", e)
