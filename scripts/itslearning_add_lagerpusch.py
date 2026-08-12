#!/usr/bin/env python3
"""Einmal-Nachtrag (12.08.2026): Lagerpusch, Alea fehlte in der grossen Personen-Zuordnungsrunde -
sie wurde wie Cleo Baake nicht versetzt und steckt in derselben alten "7c"-Organisationsgruppe
(Vorjahres-7c, 28 Mitglieder). Holt sie von dort in den Kurs 7b I (CourseID 190741)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, click_first, OUT_DIR

TARGET_COURSE_ID = 190741  # 7b I
STUDENT_NAME = "Lagerpusch"
SOURCE_GROUP = "7c"  # alte Vorjahres-7c-Gruppe (dieselbe wie bei Cleo Baake)


def main():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={TARGET_COURSE_ID}", timeout=20000)
            its.wait_for_timeout(2000)
            click_first(its, ["text=Personen"])
            its.wait_for_timeout(1500)
            click_first(its, ["text=Personen hinzufügen"])
            its.wait_for_timeout(1500)
            click_first(its, ["text=Filter"])
            its.wait_for_timeout(1000)
            its.screenshot(path=f"{OUT_DIR}/lagerpusch_01_filter.png", full_page=True)

            # alte "7c"-Gruppe im Filterbaum anklicken (nicht die aktuelle 7c!)
            its.get_by_text(SOURCE_GROUP, exact=True).first.click()
            its.wait_for_timeout(1500)
            its.screenshot(path=f"{OUT_DIR}/lagerpusch_02_liste.png", full_page=True)

            row = its.get_by_text(STUDENT_NAME, exact=False)
            if row.count() == 0:
                print(f"❌ '{STUDENT_NAME}' in Gruppe '{SOURCE_GROUP}' nicht gefunden")
                its.screenshot(path=f"{OUT_DIR}/lagerpusch_FAIL_notfound.png", full_page=True)
                return
            print(f"Gefunden: {row.count()} Treffer für '{STUDENT_NAME}'")
            add_link = row.first.locator("xpath=following::*[contains(text(),'hinzufügen')][1]")
            if add_link.count() == 0:
                # Fallback: evtl. ist der ganze Zeilenbereich klickbar
                add_link = its.get_by_role("link", name="Person hinzufügen").first
            add_link.first.click()
            its.wait_for_timeout(1500)
            its.screenshot(path=f"{OUT_DIR}/lagerpusch_03_nach_add.png", full_page=True)
            print("Klick auf 'hinzufügen' ausgeführt")

            # Verifikation: Personen-Tab von 7b I erneut oeffnen und pruefen
            its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={TARGET_COURSE_ID}", timeout=20000)
            its.wait_for_timeout(2000)
            click_first(its, ["text=Personen"])
            its.wait_for_timeout(1500)
            verify = its.get_by_text(STUDENT_NAME, exact=False)
            print(f"Verifikation im 7b-I-Personen-Tab: {verify.count()} Treffer für '{STUDENT_NAME}'")
            its.screenshot(path=f"{OUT_DIR}/lagerpusch_04_verify.png", full_page=True)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
