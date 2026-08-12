#!/usr/bin/env python3
"""Chris möchte die "Eure ersten Termine"-Mitteilung (gerade in allen 8 Kursen live gepostet und
inhaltlich korrekt) doch erst am Montag 17.08.2026 selbst einstellen - hier wieder rausnehmen,
Inhalt bleibt fertig vorbereitet in itslearning_post_erste_termine.py fuer den Montag-Anstoss."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, OUT_DIR

COURSES = [
    ("7a_I", 190735), ("7a_II", 190738),
    ("7b_I", 190741), ("7b_II", 190743),
    ("7c_I", 190861), ("7c_II", 190878),
    ("7d_I", 190860), ("7d_II", 190877),
]


def delete_latest_message(its, name, course_id):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)
    opt_btn = its.locator("button.itsl-announcement-drop-down-menu__button").first
    if opt_btn.count() == 0:
        print(f"  ⏭ {name}: keine Mitteilung vorhanden, nichts zu loeschen")
        return "KEINE MITTEILUNG"
    opt_btn.click()
    its.wait_for_timeout(500)
    del_link = its.get_by_text("Löschen", exact=True)
    if del_link.count() == 0:
        print(f"  ❌ {name}: 'Löschen' nicht im Menue gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAILDEL3_{name}_menu.png", full_page=True)
        return "FEHLER: Loeschen-Link nicht gefunden"
    del_link.first.click()
    its.wait_for_timeout(800)
    confirm_btn = its.locator("div.prom-modal2__footer button.prom-button__destructive")
    try:
        confirm_btn.first.click(timeout=5000)
        print(f"  ✅ {name}: Mitteilung geloescht")
        return "GELOESCHT"
    except Exception as e:
        print(f"  ❌ {name}: Bestaetigungs-Klick fehlgeschlagen: {e}")
        its.screenshot(path=f"{OUT_DIR}/FAILDEL3_{name}_confirm.png", full_page=True)
        return f"FEHLER: {e}"


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    results = []
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            for name, cid in COURSES:
                print(f"\n--- {name} (CourseID {cid}) ---")
                res = delete_latest_message(its, name, cid)
                results.append((name, res))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG ===")
    for name, res in results:
        print(f"{name}: {res}")
