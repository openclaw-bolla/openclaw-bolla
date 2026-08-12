#!/usr/bin/env python3
"""Schritt 2 Recon: 'Alle Kurse' ansehen + echtes Suchfeld 'Kurse suchen' benutzen, um 6a-6d zu finden."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, click_first, OUT_DIR

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser, its = login(p)
        try:
            its.goto("https://moin.itslearning.com/CourseCards", timeout=20000)
            its.wait_for_timeout(1500)

            # "Alle Kurse" anklicken
            click_first(its, ["text=Alle Kurse"])
            its.wait_for_timeout(2000)
            its.screenshot(path=f"{OUT_DIR}/recon_04_alle_kurse.png", full_page=True)
            print("=== 'Alle Kurse' Text ===")
            print(its.inner_text("body"))
            print("=== HREFs ===")
            hrefs = its.eval_on_selector_all("a[href*='CourseID']", "els => els.map(e => e.href + ' | ' + e.innerText.replace(/\\n/g,' '))")
            for h in hrefs:
                print(h)

            # Echtes Suchfeld "Kurse suchen"
            search_box = its.locator("input[placeholder*='Kurse suchen'], input[placeholder*='suchen']")
            print("\nSuchfeld gefunden:", search_box.count())
            if search_box.count() > 0:
                search_box.first.click()
                search_box.first.fill("6")
                its.wait_for_timeout(2000)
                its.screenshot(path=f"{OUT_DIR}/recon_05_search_6.png", full_page=True)
                print("=== Suchergebnis fuer '6' ===")
                print(its.inner_text("body"))
                hrefs2 = its.eval_on_selector_all("a[href*='CourseID']", "els => els.map(e => e.href + ' | ' + e.innerText.replace(/\\n/g,' '))")
                print("=== HREFs nach Suche ===")
                for h in hrefs2:
                    print(h)
        finally:
            browser.close()
    print("\nFERTIG - Schritt 2")
