#!/usr/bin/env python3
"""Korrektur (12.08.2026): Die 4 "II"-Kurse hatten faelschlich dieselben Termine wie ihre
"I"-Geschwister gepostet bekommen (blind aus dem Vorjahres-Format uebernommen - das war aber
schon damals ein Fehler, kein gewolltes Muster, siehe [[project_itslearning_automation]]).
Gruppe II ist erst NACH dem ersten 4-Wochen-Block von Gruppe I dran, hat also eigene, spaetere
Termine. Dieses Skript loescht die falsche Mitteilung in den 4 II-Kursen und postet die
korrekten Termine (aus data/schuljahr2627.json, gruppe='II', erste 4 chronologisch).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, click_first, OUT_DIR

COURSES = [
    ("7a_II", 190738),
    ("7b_II", 190743),
    ("7c_II", 190878),
    ("7d_II", 190877),
]

TEXT_7A_II = ("Eure ersten Termine 📅:\n\n"
              "Do. 17.09.26\nDo. 24.09.26\nDo. 01.10.26\nDo. 08.10.26\n\n"
              "immer 1./2. Stunde 07:50 Uhr\n\n"
              "Ich freue mich sehr auf Euch 😊")
TEXT_7B_II = ("Eure ersten Termine 📅:\n\n"
              "Mi. 16.09.26\nMi. 23.09.26\nMi. 30.09.26\nMi. 07.10.26\n\n"
              "immer 6./7. Stunde 12:30 Uhr\n\n"
              "Ich freue mich sehr auf Euch 😊")
TEXT_7C_II = ("Eure ersten Termine 📅:\n\n"
              "Do. 17.09.26\nDo. 24.09.26\nDo. 01.10.26\nDo. 08.10.26\n\n"
              "immer 6./7. Stunde 12:30 Uhr\n\n"
              "Ich freue mich sehr auf Euch 😊")
TEXT_7D_II = ("Eure ersten Termine 📅:\n\n"
              "Mi. 16.09.26\nMi. 23.09.26\nMi. 30.09.26\nMi. 07.10.26\n\n"
              "immer 1./2. Stunde 07:50 Uhr\n\n"
              "Ich freue mich sehr auf Euch 😊")

TEXT_BY_PREFIX = {"7a": TEXT_7A_II, "7b": TEXT_7B_II, "7c": TEXT_7C_II, "7d": TEXT_7D_II}


def delete_latest_message(its, name, course_id):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)
    opt_btn = its.locator("button.itsl-announcement-drop-down-menu__button").first
    if opt_btn.count() == 0:
        print(f"  ⏭ {name}: keine Mitteilung vorhanden, nichts zu loeschen")
        return "KEINE MITTEILUNG"
    its.screenshot(path=f"{OUT_DIR}/before_fix_{name}.png")
    opt_btn.click()
    its.wait_for_timeout(500)
    del_link = its.get_by_text("Löschen", exact=True)
    if del_link.count() == 0:
        print(f"  ❌ {name}: 'Löschen' nicht im Menue gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAILFIX_{name}_menu.png", full_page=True)
        return "FEHLER: Loeschen-Link nicht gefunden"
    del_link.first.click()
    its.wait_for_timeout(800)
    confirm_btn = its.locator("div.prom-modal2__footer button.prom-button__destructive")
    try:
        confirm_btn.first.click(timeout=5000)
        print(f"  ✅ {name}: falsche Mitteilung geloescht")
        return "GELOESCHT"
    except Exception as e:
        print(f"  ❌ {name}: Bestaetigungs-Klick fehlgeschlagen: {e}")
        its.screenshot(path=f"{OUT_DIR}/FAILFIX_{name}_confirm.png", full_page=True)
        return f"FEHLER: {e}"


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

    del_results = []
    post_results = []
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            print("=== SCHRITT 1: falsche Mitteilung in allen 4 II-Kursen loeschen ===")
            for name, cid in COURSES:
                print(f"\n--- {name} (CourseID {cid}) ---")
                res = delete_latest_message(its, name, cid)
                del_results.append((name, res))

            print("\n=== SCHRITT 2: korrekte 'Eure ersten Termine' (Gruppe II) posten ===")
            for name, cid in COURSES:
                prefix = name.split("_")[0]
                text = TEXT_BY_PREFIX[prefix]
                print(f"\n--- {name} (CourseID {cid}) ---")
                ok = post_text(its, cid, text)
                post_results.append((name, "OK" if ok else "FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG LOESCHEN ===")
    for name, res in del_results:
        print(f"{name}: {res}")
    print("\n=== ZUSAMMENFASSUNG POST (korrigiert) ===")
    for name, res in post_results:
        print(f"{name}: {res}")
