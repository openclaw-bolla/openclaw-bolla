#!/usr/bin/env python3
"""Recon: pruefen ob es fuer eine bestehende Ressource eine 'Datei ersetzen'-Option gibt,
bevor wir auf das Loesch+Neu-Hochladen-Muster ausweichen."""
import os
LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

import json
from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/home/bolla/workspace/scratch/itslearning_msinfo_update"
COURSE_ID = 190735  # 7a I
BASENAME = "02-Elterninfo-MS-Konto"

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

    row = its.get_by_text(BASENAME, exact=False)
    print("Treffer fuer Basename:", row.count())
    if row.count() > 0:
        its.screenshot(path=f"{OUT_DIR}/01_resource_row.png", full_page=True)
        # Versuche, das Options-Menu/Chevron in der Zeile zu finden
        row_el = row.first
        box = row_el.bounding_box()
        print("Row bounding box:", box)
        # Suche nach typischen Options-Buttons in der Naehe (gleiche Zeile, oft rechts)
        candidates = its.locator("button[aria-label*='ption'], button[aria-label*='ehr'], button.itsl-more-actions, [role='button'][aria-label]")
        print("Kandidaten fuer Optionsmenu-Buttons (gesamte Seite):", candidates.count())
        for i in range(min(candidates.count(), 40)):
            try:
                al = candidates.nth(i).get_attribute("aria-label")
                bb = candidates.nth(i).bounding_box()
                if bb and box and abs(bb["y"] - box["y"]) < 40:
                    print(f"  NAHE Zeile -> idx={i} aria-label={al!r} bbox={bb}")
            except Exception as e:
                pass
    else:
        print("Ressource nicht gefunden - evtl. anderer Basename oder liegt woanders (Plan?)")
        its.screenshot(path=f"{OUT_DIR}/01_no_resource.png", full_page=True)

    browser.close()
print("Fertig - Screenshots in", OUT_DIR)
