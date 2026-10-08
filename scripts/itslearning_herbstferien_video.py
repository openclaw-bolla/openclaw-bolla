#!/usr/bin/env python3
"""Abschieds-Mitteilung vor den Herbstferien (12.-25.10.2026) an alle 8 Kurse, mit Video
'Aus 0 und 1 wird ein Bild (mit Ton)' (Blender-Animation + 14 s aus 'Fourteen Pairs of Eyes', ab 0:40).
Stand: NUR TEXTE/Vorschau - noch nicht gepostet (wartet auf Chris' Freigabe)."""
VIDEO = "/mnt/d/OneDrive/Desktop/temp/Aus 0 und 1 wird ein Bild (mit Ton).mp4"
COURSES = [
 ("7a_I", 190735, "Do. 29.10.", "Schöne Herbstferien, 7a 🍂\n\nZum Abschied gibt's ein kleines Geschenk: Aus lauter Nullen und Einsen wird ein Bild – so wie wir es bei der Codierung besprochen haben. Der Film ist mit einem 3D-Programm (Blender) entstanden, die Musik ist ein Ausschnitt aus meinem Song „Fourteen Pairs of Eyes“. Beides mit KI-Hilfe gemacht.\n\nZum Herunterladen hängt das Video unten dran. Tipp: Ton an 🔊\n\nWir sehen uns am Do. 29.10. wieder – ausgeruht und mit viel Elan, hoffe ich 😊"),
 ("7b_I", 190741, "Mi. 28.10.", "Liebe 7b, ab in die Herbstferien 🍁\n\nDamit euch in den zwei Wochen nicht langweilig wird, hier ein Mini-Film zum Abschied: Nullen und Einsen schwirren herum und plötzlich steckt ein Bild dahinter. Gebaut mit Blender, vertont mit einem Stück aus meinem neuen Song „Fourteen Pairs of Eyes“ (KI-unterstützt).\n\nDas Video könnt ihr unten herunterladen und gern zeigen, wem ihr wollt.\n\nBis zum Mi. 28.10.! Erholt euch gut 😊"),
 ("7c_I", 190861, "Do. 29.10.", "Hallo 7c, Herbstferien! 🎃\n\nBevor ihr verschwindet, noch ein Geschenk von mir: ein kurzer Film, in dem aus Einsen und Nullen ein Bild entsteht – Informatik, die man sich ansehen kann. Das Video habe ich mit Blender gebaut, die Musik stammt aus meinem Song „Fourteen Pairs of Eyes“ (beides mit KI-Unterstützung).\n\nDownload findet ihr unten. Kopfhörer oder Lautsprecher an, dann wirkt's am besten 🎧\n\nWiedersehen am Do. 29.10. 😊"),
 ("7d_I", 190860, "Mi. 28.10.", "Tschüss in die Herbstferien, 7d 👋🍂\n\nIhr habt gelernt, dass im Computer alles aus 0 und 1 besteht. Hier der Beweis zum Anschauen: ein kleiner Film, in dem aus den Nullen und Einsen ein Bild wird. Erstellt mit Blender, der Ton ist ein Ausschnitt aus meinem Song „Fourteen Pairs of Eyes“ (KI-unterstützt).\n\nDas Video liegt unten zum Download bereit.\n\nBis Mi. 28.10. – und lasst die Handys ruhig mal ein paar Stunden schlafen 😉"),
 ("7a_II", 190738, "Do. 26.11.", "Schöne Herbstferien, 7a 🍂\n\nWir haben uns heute erst mal für längere Zeit verabschiedet, denn bei euch geht's erst am Do. 26.11. weiter. Damit ihr mich nicht vergesst, gibt's ein kleines Geschenk: einen Film, in dem aus Nullen und Einsen ein Bild entsteht (Codierung, ihr erinnert euch!). Gemacht mit Blender, dazu ein Stück aus meinem Song „Fourteen Pairs of Eyes“ (KI-unterstützt).\n\nDas Video hängt unten zum Download an. Ton an 🔊\n\nBis dann, ich freue mich auf Euch 😊"),
 ("7b_II", 190743, "Mi. 25.11.", "Liebe 7b, Herbstferien! 🍁\n\nBei euch dauert die Pause bis zum Mi. 25.11. – damit das nicht ganz so lang wird, gibt's zum Abschied einen kleinen Film: Aus 0 und 1 wird ein Bild. Blender-Animation, Musik aus meinem Song „Fourteen Pairs of Eyes“ (beides mit KI-Hilfe).\n\nZum Herunterladen findet ihr das Video unten. Zeigt es ruhig zu Hause – Nullen und Einsen kommen bei jedem gut an 😄\n\nBis bald!"),
 ("7c_II", 190878, "Do. 26.11.", "Hallo 7c, ab in die Ferien 🎃\n\nWir sehen uns erst am Do. 26.11. wieder, deshalb bekommt ihr jetzt ein Abschiedsgeschenk: einen kurzen Film, in dem aus Nullen und Einsen ein Bild entsteht. Mit Blender gebaut, die Musik ist ein Ausschnitt aus meinem Song „Fourteen Pairs of Eyes“ (KI-unterstützt).\n\nDownload unten. Kopfhörer auf, Film ab 🎧\n\nErholt euch gut, ich freue mich auf Euch 😊"),
 ("7d_II", 190877, "Mi. 25.11.", "Tschüss, 7d, schöne Herbstferien 👋🍂\n\nEuer nächster Termin ist erst am Mi. 25.11. – da könnt ihr zwischendurch ja mal nachzählen, wie viele Nullen und Einsen ihr in der Zeit so tippt. Zum Abschied habe ich einen Film gemacht: Aus 0 und 1 wird ein Bild. Blender-Animation plus ein Stück aus meinem Song „Fourteen Pairs of Eyes“ (KI-unterstützt).\n\nDas Video liegt unten zum Download.\n\nBis dann – und bleibt neugierig 😊"),
]


STAGED = "/home/bolla/workspace/state/herbst_video/Aus 0 und 1 wird ein Bild - Herbstferien.mp4"
FILES = [{"path": STAGED, "basename": "Aus 0 und 1 wird ein Bild - Herbstferien",
          "filename": "Aus 0 und 1 wird ein Bild - Herbstferien.mp4"}]

if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from job_status import report as _r
    _r("itslearning-herbst-video", "Herbstferien-Video (8 Kurse)", "laeuft", "postet in 8 Kursen")
    from playwright.sync_api import sync_playwright
    from itslearning_post_kurstag import login, upload_files, post_message
    from itslearning_post_naechste_termine_gruppeII_nov import tg
    res = []
    try:
        with sync_playwright() as p:
            browser, its = login(p)
            try:
                for name, cid, _, text in COURSES:
                    print(f"\n--- {name} ({cid}) ---")
                    if not upload_files(its, cid, FILES):
                        res.append((name, "UPLOAD FEHLGESCHLAGEN")); continue
                    res.append((name, "OK" if post_message(its, cid, text, FILES) else "POST FEHLGESCHLAGEN"))
            finally:
                browser.close()
    except Exception as e:
        res.append(("ABBRUCH", repr(e)[:200]))
    ok = len(res) == len(COURSES) and all(r == "OK" for _, r in res)
    summ = "; ".join(f"{n}: {r}" for n, r in res)
    print(summ)
    try:
        _r("itslearning-herbst-video", "Herbstferien-Video (8 Kurse)", "ok" if ok else "fehler",
           "in allen 8 Kursen gepostet" if ok else summ + " – bitte nachsehen")
        tg("✅ Herbstferien-Video in allen 8 Kursen gepostet" if ok else "⚠️ Herbstferien-Video: " + summ)
    except Exception as e:
        print("Meldung fehlgeschlagen:", e)
