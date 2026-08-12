#!/usr/bin/env python3
""""Eure ersten Termine"-Mitteilung fuer alle 8 Kurse (Schuljahr 26/27), im Format wie Chris es
letztes Schuljahr selbst gepostet hatte (siehe [[project_itslearning_automation]] fuer Details/
Historie). WICHTIG: I- und II-Kurs derselben Klasse bekommen JEWEILS EIGENE Termine (Gruppe I
startet 19./20.08., Gruppe II erst nach deren ersten 4-Wochen-Block ab 16./17.09. - siehe
Chris-Korrektur vom 12.08.2026, NICHT wie im ersten (fehlerhaften) Vorjahres-Muster wortgleich).

Von Chris bewusst zurueckgehalten (12.08.2026): Inhalt fertig geprueft/korrigiert, aber er wollte
die Mitteilungen selbst erst am Montag 17.08.2026 einstellen - daher aus den 8 Kursen wieder
geloescht. Dieses Skript hier ist der fertige, korrekte Post-Lauf fuer den Montag-Anstoss (keine
vorherige Loeschung mehr noetig, die Kurse sind leer).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, click_first

# Kurs-IDs (Schuljahr 26/27, stabil) + individueller Text je Kurs (I und II verschieden!)
COURSES = [
    ("7a_I", 190735, ("Eure ersten Termine 📅:\n\n"
                       "Do. 20.08.26\nDo. 27.08.26\nDo. 03.09.26\nDo. 10.09.26\n\n"
                       "immer 1./2. Stunde 07:50 Uhr\n\n"
                       "Ich freue mich sehr auf Euch 😊")),
    ("7a_II", 190738, ("Eure ersten Termine 📅:\n\n"
                        "Do. 17.09.26\nDo. 24.09.26\nDo. 01.10.26\nDo. 08.10.26\n\n"
                        "immer 1./2. Stunde 07:50 Uhr\n\n"
                        "Ich freue mich sehr auf Euch 😊")),
    ("7b_I", 190741, ("Eure ersten Termine 📅:\n\n"
                       "Mi. 19.08.26\nMi. 26.08.26\nMi. 02.09.26\nMi. 09.09.26\n\n"
                       "immer 6./7. Stunde 12:30 Uhr\n\n"
                       "Ich freue mich sehr auf Euch 😊")),
    ("7b_II", 190743, ("Eure ersten Termine 📅:\n\n"
                        "Mi. 16.09.26\nMi. 23.09.26\nMi. 30.09.26\nMi. 07.10.26\n\n"
                        "immer 6./7. Stunde 12:30 Uhr\n\n"
                        "Ich freue mich sehr auf Euch 😊")),
    ("7c_I", 190861, ("Eure ersten Termine 📅:\n\n"
                       "Do. 20.08.26\nDo. 27.08.26\nDo. 03.09.26\nDo. 10.09.26\n\n"
                       "immer 6./7. Stunde 12:30 Uhr\n\n"
                       "Ich freue mich sehr auf Euch 😊")),
    ("7c_II", 190878, ("Eure ersten Termine 📅:\n\n"
                        "Do. 17.09.26\nDo. 24.09.26\nDo. 01.10.26\nDo. 08.10.26\n\n"
                        "immer 6./7. Stunde 12:30 Uhr\n\n"
                        "Ich freue mich sehr auf Euch 😊")),
    ("7d_I", 190860, ("Eure ersten Termine 📅:\n\n"
                       "Mi. 19.08.26\nMi. 26.08.26\nMi. 02.09.26\nMi. 09.09.26\n\n"
                       "immer 1./2. Stunde 07:50 Uhr\n\n"
                       "Ich freue mich sehr auf Euch 😊")),
    ("7d_II", 190877, ("Eure ersten Termine 📅:\n\n"
                        "Mi. 16.09.26\nMi. 23.09.26\nMi. 30.09.26\nMi. 07.10.26\n\n"
                        "immer 1./2. Stunde 07:50 Uhr\n\n"
                        "Ich freue mich sehr auf Euch 😊")),
]


def post_text(its, course_id, text):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)
    click_first(its, ["text=Mitteilung schreiben", "[contenteditable='true']"])
    its.wait_for_timeout(700)
    box = its.locator("li.itsl-light-bulletins-new-item-listitem").first
    if box.count() == 0:
        print("  ❌ Mitteilungs-Box nicht gefunden")
        return False
    editor = box.locator("[contenteditable='true']").first
    editor.click()
    editor.fill(text)
    its.wait_for_timeout(500)
    published = click_first(its, ["text=Veröffentlichen"])
    its.wait_for_timeout(2000)
    if not published:
        print("  ❌ 'Veröffentlichen'-Button nicht gefunden")
        return False
    print("  ✅ Mitteilung veroeffentlicht")
    return True


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    post_results = []
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            for name, cid, text in COURSES:
                print(f"\n--- {name} (CourseID {cid}) ---")
                ok = post_text(its, cid, text)
                post_results.append((name, "OK" if ok else "FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG POST (alle 8) ===")
    for name, res in post_results:
        print(f"{name}: {res}")
