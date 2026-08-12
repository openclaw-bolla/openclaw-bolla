#!/usr/bin/env python3
"""Schritt 4 Recon: Status-Filter auf /AllCourses von 'Aktiv' auf 'Alle'/'Inaktiv' umstellen,
um archivierte Vorjahres-Kurse (6a-6d, Schuljahr 25/26) zu finden."""
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

            # Alle <select>-Elemente auf der Seite auflisten, um den Status-Filter zu finden
            selects = its.eval_on_selector_all(
                "select",
                "els => els.map(e => ({id: e.id, name: e.name, options: Array.from(e.options).map(o => o.text)}))")
            print("=== <select>-Elemente auf /AllCourses ===")
            for s in selects:
                print(s)

            its.screenshot(path=f"{OUT_DIR}/recon_07_before_filter.png", full_page=True)
        finally:
            browser.close()
    print("\nFERTIG - Schritt 4 (nur Analyse, kein Filterklick)")
