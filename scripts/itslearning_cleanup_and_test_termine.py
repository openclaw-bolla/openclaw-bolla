#!/usr/bin/env python3
"""Einmal-Aktion (12.08.2026): Chris hat in allen 8 Kursen die migrierte "erste Mitteilung des
letzten Schuljahres" mit rübergenommen - die wird hier ueberall geloescht (jeweils die aktuell
oberste/neueste Mitteilung, siehe [[project_itslearning_automation]] fuer die DOM-Fallstricke).
Vor jeder Loeschung ein Screenshot als Audit-Spur (Loeschen von Mitteilungen ist NICHT
wiederherstellbar, anders als Ressourcen).

Danach als Live-Test NUR fuer 7d I und 7d II die neue Termine-Ankuendigung posten (Text siehe
itslearning_post_termine_ankuendigung.py) - die anderen 6 Kurse bleiben unangetastet, bis der Test
von Chris abgenommen ist.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, click_first, OUT_DIR

# Kurs-IDs (Schuljahr 26/27, stabil)
ALL_COURSES = [
    ("7a_I", 190735), ("7a_II", 190738),
    ("7b_I", 190741), ("7b_II", 190743),
    ("7c_I", 190861), ("7c_II", 190878),
    ("7d_I", 190860), ("7d_II", 190877),
]

TERMIN_TEXT = (
    "📅 Kurze Ankündigung, liebe 7d: Unser EDV-Kurs findet dieses Schuljahr immer "
    "mittwochs in der 1./2. Stunde statt (7:50–9:25 Uhr). Freu mich schon auf eine "
    "spannende Zeit mit euch am Rechner! 💻✨"
)
TEST_POST_COURSES = [("7d_I", 190860), ("7d_II", 190877)]


def delete_latest_message(its, name, course_id):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)

    opt_btn = its.locator("button.itsl-announcement-drop-down-menu__button").first
    if opt_btn.count() == 0:
        print(f"  ⏭ {name}: keine Mitteilung vorhanden, nichts zu loeschen")
        return "KEINE MITTEILUNG"

    its.screenshot(path=f"{OUT_DIR}/before_delete_{name}.png")
    print(f"  📸 {name}: Screenshot vor Loeschung gespeichert")

    opt_btn.click()
    its.wait_for_timeout(500)
    del_link = its.get_by_text("Löschen", exact=True)
    if del_link.count() == 0:
        print(f"  ❌ {name}: 'Löschen' nicht im Menue gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAILDEL_{name}_menu.png", full_page=True)
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
        its.screenshot(path=f"{OUT_DIR}/FAILDEL_{name}_confirm.png", full_page=True)
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
            print("=== SCHRITT 1: Alte migrierte Mitteilungen loeschen (alle 8 Kurse) ===")
            for name, cid in ALL_COURSES:
                print(f"\n--- {name} (CourseID {cid}) ---")
                res = delete_latest_message(its, name, cid)
                del_results.append((name, res))

            print("\n=== SCHRITT 2: Test-Post Termine-Ankuendigung (nur 7d I + 7d II) ===")
            for name, cid in TEST_POST_COURSES:
                print(f"\n--- {name} (CourseID {cid}) ---")
                ok = post_text(its, cid, TERMIN_TEXT)
                post_results.append((name, "OK" if ok else "FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG LOESCHEN ===")
    for name, res in del_results:
        print(f"{name}: {res}")
    print("\n=== ZUSAMMENFASSUNG TEST-POST ===")
    for name, res in post_results:
        print(f"{name}: {res}")
