#!/usr/bin/env python3
"""Notfall-Werkzeug: Loescht Ressourcen mit den angegebenen Basisnamen (ohne Dateiendung!) aus den
angegebenen Kursen. Vor Gebrauch BASENAMES und COURSES unten anpassen.
Siehe [[project_itslearning_automation]] fuer die DOM-Fallstricke."""
import json
import os

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/tmp/its_debug"
os.makedirs(OUT_DIR, exist_ok=True)

with open(CREDS_PATH) as f:
    creds = json.load(f)

# Basisnamen OHNE Dateiendung (Name+Endung stehen im DOM in getrennten <span>-Elementen)
BASENAMES = ["01-The Basics - Grundbegriffe - I", "01-Praktikum", "01-Editor-Anleitung"]

# Kurs-IDs (Schuljahr 26/27, stabil): 7a I=190735 7a II=190738 7b I=190741 7b II=190743
#                                     7c I=190861 7c II=190878 7d I=190860 7d II=190877
COURSES = [("7a_I", 190735), ("7b_I", 190741), ("7c_I", 190861), ("7d_I", 190860)]


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
    context = browser.new_context(viewport={"width": 1400, "height": 1000})
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

    try:
        for name, cid in COURSES:
            print(f"\n=== {name} ===")
            its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={cid}", timeout=20000)
            its.wait_for_timeout(2000)
            click_first(its, ["text=Ressourcen"])
            its.wait_for_timeout(1500)

            checked = 0
            for bn in BASENAMES:
                row = its.get_by_text(bn, exact=False)
                if row.count() == 0:
                    print(f"  ⏭ '{bn}' nicht (mehr) vorhanden")
                    continue
                cb = row.first.locator("xpath=preceding::input[@type='checkbox'][1]")
                cb.evaluate("el => el.click()")
                checked += 1
                its.wait_for_timeout(300)

            if checked == 0:
                print("  Nichts zu loeschen")
                continue

            del_candidates = its.get_by_role("button", name="Löschen", exact=True)
            del_btn = None
            for i in range(del_candidates.count()):
                if del_candidates.nth(i).is_visible():
                    del_btn = del_candidates.nth(i)
                    break
            if del_btn is None:
                print("  ❌ Loeschen-Aktion nicht gefunden")
                its.screenshot(path=f"{OUT_DIR}/FAILRES_{name}.png", full_page=True)
                continue
            del_btn.click()
            its.wait_for_timeout(800)

            confirm = its.locator("div.prom-modal2__footer button.prom-button__destructive")
            if confirm.count() > 0:
                confirm.first.click(timeout=5000)
                its.wait_for_timeout(1500)
                print(f"  ✅ {checked} Ressource(n) geloescht")
            else:
                print("  ❌ Bestaetigungs-Button nicht gefunden")
                its.screenshot(path=f"{OUT_DIR}/FAILRES_{name}_confirm.png", full_page=True)
    finally:
        browser.close()
print("\nFERTIG")
