#!/usr/bin/env python3
"""Schritt 5 Recon: Status-Filter (Custom-Combobox 'Aktiv') auf /AllCourses umstellen, um
archivierte Vorjahres-Kurse (6a-6d) sichtbar zu machen."""
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

            # Klick auf die 'Aktiv'-Status-Combobox, um Optionen zu oeffnen
            its.get_by_text("Aktiv", exact=True).first.click()
            its.wait_for_timeout(800)
            its.screenshot(path=f"{OUT_DIR}/recon_08_status_dropdown_open.png", full_page=True)
            print("=== Sichtbarer Text nach Klick auf Status-Dropdown ===")
            print(its.inner_text("body"))
        finally:
            browser.close()
    print("\nFERTIG - Schritt 5")
