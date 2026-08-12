#!/usr/bin/env python3
"""Schritt 7 Recon: das eigentliche Steuerelement hinter dem Status-Label (per 'for'-Attribut)
finden und anklicken."""
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
            print("for-Attribut des Status-Labels:", for_id)

            target = its.locator(f"#{for_id}")
            print("Ziel-Element Tag:", target.evaluate("el => el.tagName"))
            print("Ziel-Element outerHTML (gekuerzt):", target.evaluate("el => el.outerHTML")[:500])

            target.click(timeout=5000)
            its.wait_for_timeout(800)
            its.screenshot(path=f"{OUT_DIR}/recon_10_status_open3.png", full_page=True)

            # Nach dem Klick alle sichtbaren li/div mit Text wie Aktiv/Inaktiv/Archiviert suchen
            body_txt = its.inner_text("body")
            print("=== Body-Text nach Klick ===")
            print(body_txt)
        finally:
            browser.close()
    print("\nFERTIG - Schritt 7")
