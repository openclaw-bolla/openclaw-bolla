#!/usr/bin/env python3
"""Schritt 6 Recon: Status-Filter ueber das prom-listbox-dropdown__label Element oeffnen."""
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

            labels = its.locator(".prom-listbox-dropdown__label")
            print("Anzahl .prom-listbox-dropdown__label:", labels.count())
            for i in range(labels.count()):
                print(i, "->", labels.nth(i).inner_text())

            # Erstes Dropdown-Label ist vermutlich 'Status'
            labels.nth(0).click(timeout=5000)
            its.wait_for_timeout(800)
            its.screenshot(path=f"{OUT_DIR}/recon_09_status_open2.png", full_page=True)

            options = its.locator("[role='option'], li[role='option'], .prom-listbox-dropdown li")
            print("Anzahl Options-aehnliche Elemente:", options.count())
            for i in range(min(options.count(), 20)):
                print(i, "->", options.nth(i).inner_text())
        finally:
            browser.close()
    print("\nFERTIG - Schritt 6")
