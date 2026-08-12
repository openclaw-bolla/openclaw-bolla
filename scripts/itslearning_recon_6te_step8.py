#!/usr/bin/env python3
"""Schritt 8 Recon: Status-Filter 'Archiviert' zusaetzlich anhaken + 'Anwenden' klicken,
um archivierte Vorjahres-Kurse (6a-6d) sichtbar zu machen. Reines Ansehen, keine Kurs-Aenderung."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, OUT_DIR

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser, its = login(p)
        try:
            its.goto("https://moin.itslearning.com/AllCourses", timeout=20000)
            its.wait_for_timeout(2500)

            label = its.locator(".prom-listbox-dropdown__label").nth(0)
            for_id = label.get_attribute("for")
            its.locator(f"#{for_id}").click(timeout=5000)
            its.wait_for_timeout(600)

            its.get_by_text("Archiviert", exact=True).first.click()
            its.wait_for_timeout(400)
            its.screenshot(path=f"{OUT_DIR}/recon_11_archiviert_checked.png", full_page=True)

            its.get_by_role("button", name="Anwenden").click(timeout=5000)
            its.wait_for_timeout(2000)
            its.screenshot(path=f"{OUT_DIR}/recon_12_nach_anwenden.png", full_page=True)

            print("=== Body-Text nach Anwenden (Status: Aktiv+Archiviert) ===")
            print(its.inner_text("body"))
            print("=== HREFs mit CourseID ===")
            hrefs = its.eval_on_selector_all(
                "a[href*='CourseID']",
                "els => els.map(e => e.href + ' | ' + e.innerText.replace(/\\n/g,' '))")
            for h in hrefs:
                print(h)
        finally:
            browser.close()
    print("\nFERTIG - Schritt 8")
