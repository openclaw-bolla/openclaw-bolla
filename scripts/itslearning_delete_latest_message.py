#!/usr/bin/env python3
"""Notfall-Werkzeug: Loescht die JEWEILS NEUESTE Mitteilung in den angegebenen Kursen wieder.
Vorsicht: 'Nach dem Loeschen ist die Wiederherstellung nicht moeglich' (itslearning-eigene Warnung).
Vor Gebrauch COURSES unten anpassen. Siehe [[project_itslearning_automation]] fuer die DOM-Fallstricke."""
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

    for name, cid in COURSES:
        print(f"\n=== {name} ===")
        its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={cid}", timeout=20000)
        its.wait_for_timeout(2000)

        opt_btn = its.locator("button.itsl-announcement-drop-down-menu__button").first
        if opt_btn.count() == 0:
            print("  ❌ Kein Options-Button gefunden (evtl. keine Mitteilung vorhanden)")
            continue
        opt_btn.click()
        its.wait_for_timeout(500)

        del_link = its.get_by_text("Löschen", exact=True)
        if del_link.count() == 0:
            print("  ❌ 'Löschen' nicht im Menue gefunden")
            its.screenshot(path=f"{OUT_DIR}/FAILDEL_{name}_menu.png", full_page=True)
            continue
        del_link.first.click()
        its.wait_for_timeout(800)

        confirm_btn = its.locator("div.prom-modal2__footer button.prom-button__destructive")
        try:
            confirm_btn.first.click(timeout=5000)
            print("  ✅ Mitteilung geloescht")
        except Exception as e:
            print("  ❌ Bestaetigungs-Klick fehlgeschlagen:", e)
            its.screenshot(path=f"{OUT_DIR}/FAILDEL_{name}_confirm.png", full_page=True)
        its.wait_for_timeout(1000)

    browser.close()
print("\nFERTIG")
