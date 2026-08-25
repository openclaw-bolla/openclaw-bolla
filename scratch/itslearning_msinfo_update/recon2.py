#!/usr/bin/env python3
"""Recon 2: Optionsmenu ('...') der Zeile '02-Elterninfo-MS-Konto.html' oeffnen und Eintraege auflisten."""
import os
LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

import json
from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/home/bolla/workspace/scratch/itslearning_msinfo_update"
COURSE_ID = 190735  # 7a I

with open(CREDS_PATH) as f:
    creds = json.load(f)


def click_first(page, selectors, timeout=5000):
    for sel in selectors:
        try:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.click(timeout=timeout)
                return sel
        except Exception as e:
            print("  Klick fehlgeschlagen fuer", sel, ":", e)
    return None


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1400, "height": 1100})
    page = context.new_page()
    page.goto("https://portal.schule-sh.de/", timeout=20000)
    page.wait_for_timeout(800)
    click_first(page, ["text=Anmelden"])
    page.wait_for_timeout(1000)
    page.fill("input[name='username']", creds["username"])
    page.fill("input[name='password']", creds["password"])
    click_first(page, ["button[type='submit']", "input[type='submit']", "text=Anmelden"])
    page.wait_for_timeout(2500)
    with context.expect_page(timeout=15000) as new_page_info:
        click_first(page, ["text=itslearning"])
    its = new_page_info.value
    its.wait_for_load_state("load", timeout=20000)
    its.wait_for_timeout(2000)

    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={COURSE_ID}", timeout=20000)
    its.wait_for_timeout(2000)
    click_first(its, ["text=Ressourcen"])
    its.wait_for_timeout(1500)

    row = its.get_by_text("02-Elterninfo-MS-Konto.html", exact=False)
    print("HTML-Zeile Treffer:", row.count())
    # Finde die Tabellenzeile (tr) und darin den "..."-Button ganz rechts
    tr = row.first.locator("xpath=ancestor::tr[1]")
    print("tr gefunden:", tr.count())
    more_btn = tr.locator("text=...")
    print("'...' Button in Zeile:", more_btn.count())
    if more_btn.count() == 0:
        # evtl anderes Element (Icon-Button ohne Text)
        more_btn = tr.locator("button").last
    more_btn.first.click(timeout=5000)
    its.wait_for_timeout(1000)
    its.screenshot(path=f"{OUT_DIR}/02_options_menu.png", full_page=True)

    # Alle sichtbaren Menu-Items sammeln
    items = its.locator("[role='menuitem'], [role='menu'] li, .dropdown-menu li, li[role='presentation']")
    print("Menu-Item-Kandidaten:", items.count())
    for i in range(min(items.count(), 30)):
        try:
            txt = items.nth(i).inner_text().strip()
            if txt:
                print(f"  [{i}] {txt!r}")
        except Exception:
            pass

    browser.close()
print("Fertig - Screenshot in", OUT_DIR)
