#!/usr/bin/env python3
""""Eure naechsten Termine"-Mitteilung fuer die 4 Gruppe-I-Kurse (7a/7b/7c/7d I), Block-Wechsel
nach den Herbstferien (naechster Kurstag 5 am 28./29.10.2026 - Gruppe I pausierte waehrend des
Gruppe-II-Blocks + Herbstferien, siehe [[project_itslearning_automation]]).

Auf Chris' Wunsch (14.09.2026) diesmal mit leichten Text-Varianten je Klasse statt 1:1 identisch
wie beim "erste Termine"-Post - Kerninfos (Termine, Uhrzeit) unveraendert.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login
from itslearning_post_erste_termine import post_text

COURSES = [
    ("7a_I", 190735, ("Eure nächsten Termine 📅:\n\n"
                       "Do. 29.10.26\nDo. 05.11.26\nDo. 12.11.26\nDo. 19.11.26\n\n"
                       "immer 1./2. Stunde 07:50 Uhr\n\n"
                       "Ich freue mich sehr auf Euch 😊")),
    ("7b_I", 190741, ("Hier eure nächsten Termine 📅:\n\n"
                       "Mi. 28.10.26\nMi. 04.11.26\nMi. 11.11.26\nMi. 18.11.26\n\n"
                       "immer 6./7. Stunde 12:30 Uhr\n\n"
                       "Bis bald, ich freue mich auf Euch 😊")),
    ("7c_I", 190861, ("Eure nächsten Termine im Überblick 📅:\n\n"
                       "Do. 29.10.26\nDo. 05.11.26\nDo. 12.11.26\nDo. 19.11.26\n\n"
                       "immer 6./7. Stunde 12:30 Uhr\n\n"
                       "Freue mich schon auf Euch 😊")),
    ("7d_I", 190860, ("Eure nächsten Termine 📅:\n\n"
                       "Mi. 28.10.26\nMi. 04.11.26\nMi. 11.11.26\nMi. 18.11.26\n\n"
                       "immer 1./2. Stunde 07:50 Uhr\n\n"
                       "Bis dann, ich freue mich auf Euch 😊")),
]

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

    print("\n=== ZUSAMMENFASSUNG POST (4 Gruppe-I-Kurse) ===")
    for name, res in post_results:
        print(f"{name}: {res}")
