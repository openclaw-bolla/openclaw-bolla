#!/usr/bin/env python3
"""REIN LESENDES Recon-Skript: findet 6a/6b/6c/6d-Kurse, listet Personen, inspiziert
7a-I-Personen-Tab und den 'Person hinzufuegen'-Dialog (OHNE etwas zu speichern/hinzuzufuegen).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, click_first, OUT_DIR

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser, its = login(p)
        try:
            # --- Schritt 1: Kursliste ansehen ---
            its.goto("https://moin.itslearning.com/CourseCards", timeout=20000)
            its.wait_for_timeout(2000)
            its.screenshot(path=f"{OUT_DIR}/recon_01_coursecards.png", full_page=True)
            print("=== Kursliste (Text-Inhalt, gekuerzt) ===")
            body_text = its.inner_text("body")
            for line in body_text.splitlines():
                if line.strip():
                    print(line)
            print("=== HREFs mit CourseID auf der Kursliste ===")
            hrefs = its.eval_on_selector_all("a[href*='CourseID']", "els => els.map(e => e.href + ' | ' + e.innerText)")
            for h in hrefs:
                print(h)

            # --- Versuch: Suche Strg+K ---
            try:
                its.keyboard.press("Control+K")
                its.wait_for_timeout(1000)
                its.screenshot(path=f"{OUT_DIR}/recon_02_search_open.png", full_page=True)
                its.keyboard.type("6a")
                its.wait_for_timeout(1500)
                its.screenshot(path=f"{OUT_DIR}/recon_03_search_6a.png", full_page=True)
                print("=== Suchergebnisse fuer '6a' (Text) ===")
                print(its.inner_text("body"))
            except Exception as e:
                print("Suche fehlgeschlagen:", e)
            its.keyboard.press("Escape")
            its.wait_for_timeout(500)

        finally:
            browser.close()
    print("\nFERTIG - Schritt 1 (Kursuebersicht/Suche)")
