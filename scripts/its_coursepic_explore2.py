#!/usr/bin/env python3
import json
import os

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/tmp/its_coursepic"
os.makedirs(OUT_DIR, exist_ok=True)

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


def login(pw):
    browser = pw.chromium.launch()
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
    return browser, its


with sync_playwright() as pw:
    browser, its = login(pw)
    try:
        its.goto("https://moin.itslearning.com/Course/Course.aspx?CourseId=190743", timeout=20000)
        its.wait_for_timeout(1500)
        click_first(its, ["text=Einstellungen"])
        its.wait_for_timeout(2000)
        print("After Einstellungen click, URL:", its.url)
        its.screenshot(path=f"{OUT_DIR}/7bII_settings.png", full_page=True)
        with open(f"{OUT_DIR}/7bII_settings.html", "w") as f:
            f.write(its.content())

        for kw in ["Kursbild", "Bild", "Foto", "Symbol", "picture", "Logo"]:
            cnt = its.get_by_text(kw, exact=False).count()
            if cnt:
                print(f"Found '{kw}': {cnt} matches")

        # list left-side settings menu items if any
        menu_items = its.locator("aside a, .itsl-settings-menu a, nav a").all_text_contents()
        print("Menu items:", [t.strip() for t in menu_items if t.strip()][:60])
    finally:
        browser.close()
