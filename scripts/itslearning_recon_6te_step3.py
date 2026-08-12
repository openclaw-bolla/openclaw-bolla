#!/usr/bin/env python3
"""Schritt 3 Recon: direkt /AllCourses aufrufen (Klick auf 'Alle Kurse' scheiterte an Banner-Overlay)."""
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
            its.screenshot(path=f"{OUT_DIR}/recon_06_allcourses.png", full_page=True)
            print("=== /AllCourses Text ===")
            print(its.inner_text("body"))
            print("=== HREFs mit CourseID ===")
            hrefs = its.eval_on_selector_all(
                "a[href*='CourseID']",
                "els => els.map(e => e.href + ' | ' + e.innerText.replace(/\\n/g,' '))")
            for h in hrefs:
                print(h)
        finally:
            browser.close()
    print("\nFERTIG - Schritt 3")
