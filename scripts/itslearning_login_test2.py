#!/usr/bin/env python3
"""Fortsetzung: nach Portal-Login auf itslearning-Kachel klicken, Kursliste ansehen. Rein lesend."""
import json
import os

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/tmp/claude-1000/-mnt-c-WINDOWS-system32/dc5bcfc1-3712-4d32-a1d2-fbbb2cf1205b/scratchpad"

with open(CREDS_PATH) as f:
    creds = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1400, "height": 1000})
    page = context.new_page()

    page.goto("https://portal.schule-sh.de/", timeout=20000)
    page.wait_for_timeout(800)
    page.locator("text=Anmelden").first.click(timeout=5000)
    page.wait_for_timeout(1000)
    page.fill("input[name='username']", creds["username"])
    page.fill("input[name='password']", creds["password"])
    for sel in ["button[type='submit']", "input[type='submit']", "text=Anmelden", "button:has-text('Anmelden')"]:
        try:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.click(timeout=5000)
                break
        except Exception as e:
            print("Submit-Versuch fehlgeschlagen fuer", sel, ":", e)
    page.wait_for_timeout(2500)
    print("Eingeloggt, URL:", page.url)

    # itslearning-Kachel anklicken -> oeffnet ggf. neuen Tab
    with context.expect_page(timeout=15000) as new_page_info:
        page.locator("text=itslearning").first.click(timeout=5000)
    its_page = new_page_info.value
    its_page.wait_for_load_state("load", timeout=20000)
    its_page.wait_for_timeout(2500)

    print("itslearning URL:", its_page.url)
    print("itslearning TITLE:", its_page.title())
    its_page.screenshot(path=f"{OUT_DIR}/its_step5_dashboard.png", full_page=True)

    browser.close()

print("FERTIG")
