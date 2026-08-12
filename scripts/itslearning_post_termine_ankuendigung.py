#!/usr/bin/env python3
"""Erste Mitteilung an die 4 aktiven Kurse (7a/b/c/d I) mit dem festen Wochentermin fuer
EDV im Schuljahr 26/27 - reine Text-Ankuendigung, kein Datei-Anhang.

⚠️ Vorbereitet auf Chris' Anstoss (12.08.2026), noch NICHT ausgefuehrt/veroeffentlicht.
Erst nach expliziter Freigabe starten (siehe [[feedback_website_schreibzugriff]]).

Nutzt login()/click_first() aus itslearning_post_kurstag.py wieder, postet aber nur Text
(keine Ressourcen-Anhaenge, daher eigene schlanke post_text()-Variante statt post_message()).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, click_first, OUT_DIR

# Kurs-IDs (Schuljahr 26/27, stabil): 7a I=190735 7b I=190741 7c I=190861 7d I=190860
COURSES = [
    {"id": 190860, "kuerzel": "7d I", "text":
        "📅 Kurze Ankündigung, liebe 7d: Unser EDV-Kurs findet dieses Schuljahr immer "
        "mittwochs in der 1./2. Stunde statt (7:50–9:25 Uhr). Freu mich schon auf eine "
        "spannende Zeit mit euch am Rechner! 💻✨"},
    {"id": 190741, "kuerzel": "7b I", "text":
        "🕐 Liebe 7b, damit ihr Bescheid wisst: Unsere EDV-Stunden liegen dieses Schuljahr "
        "immer mittwochs in der 6./7. Stunde (12:30–14:05 Uhr). Ich freu mich auf ein "
        "tolles gemeinsames Jahr! 🚀"},
    {"id": 190735, "kuerzel": "7a I", "text":
        "👋 Hallo 7a! Damit ihr euch den Termin merken könnt: Unser EDV-Unterricht findet "
        "ab sofort jeden Donnerstag in der 1./2. Stunde statt (7:50–9:25 Uhr). Bin schon "
        "gespannt auf unser Schuljahr zusammen! 😊"},
    {"id": 190861, "kuerzel": "7c I", "text":
        "📌 Liebe 7c, hier schon mal euer fester EDV-Termin fürs neue Schuljahr: "
        "donnerstags, 6./7. Stunde (12:30–14:05 Uhr). Ich freu mich drauf, mit euch "
        "loszulegen! 💻"},
]


def post_text(its, course_id, text):
    """Wie post_message() in itslearning_post_kurstag.py, aber ohne Ressourcen-Anhang-Schritt."""
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

    print(f"  ✅ Mitteilung veroeffentlicht (Kurs {course_id})")
    return True


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    results = []
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            for c in COURSES:
                print(f"\n=== {c['kuerzel']} (CourseID {c['id']}) ===")
                ok = post_text(its, c["id"], c["text"])
                results.append((c["kuerzel"], "OK" if ok else "FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG ===")
    for kuerzel, status in results:
        print(f"{kuerzel}: {status}")
