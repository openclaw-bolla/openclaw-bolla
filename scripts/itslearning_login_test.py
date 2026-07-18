#!/usr/bin/env python3
"""Testet den Login-Flow Schulportal-SH -> itslearning per Playwright.
Rein lesend: kein Posting, nur Login + Screenshot zur Verifikation.
"""
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
    page = browser.new_page(viewport={"width": 1400, "height": 1000})

    page.goto("https://portal.schule-sh.de/", timeout=20000)
    page.wait_for_timeout(1000)
    page.screenshot(path=f"{OUT_DIR}/its_step1_start.png")
    print("STEP1 URL:", page.url)
    print("STEP1 TITLE:", page.title())

    # Versuche "Anmelden" zu finden und zu klicken
    clicked = False
    for sel in ["text=Anmelden", "text=Login", "a:has-text('Anmelden')", "button:has-text('Anmelden')"]:
        try:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.click(timeout=5000)
                clicked = True
                break
        except Exception as e:
            print("Klick-Versuch fehlgeschlagen fuer", sel, ":", e)

    print("Anmelden geklickt:", clicked)
    page.wait_for_timeout(1500)
    page.screenshot(path=f"{OUT_DIR}/its_step2_after_anmelden_click.png")
    print("STEP2 URL:", page.url)

    # Versuche Username/Passwort-Felder zu finden
    user_sel_candidates = ["input[name='username']", "input[type='text']", "input#username", "input[name='j_username']"]
    pass_sel_candidates = ["input[name='password']", "input[type='password']", "input#password", "input[name='j_password']"]

    user_field = None
    for sel in user_sel_candidates:
        if page.locator(sel).count() > 0:
            user_field = sel
            break
    pass_field = None
    for sel in pass_sel_candidates:
        if page.locator(sel).count() > 0:
            pass_field = sel
            break

    print("Username-Feld gefunden:", user_field)
    print("Passwort-Feld gefunden:", pass_field)

    if user_field and pass_field:
        page.fill(user_field, creds["username"])
        page.fill(pass_field, creds["password"])
        page.screenshot(path=f"{OUT_DIR}/its_step3_filled.png")

        submitted = False
        for sel in ["button[type='submit']", "input[type='submit']", "text=Anmelden", "button:has-text('Anmelden')"]:
            try:
                if page.locator(sel).count() > 0:
                    page.locator(sel).first.click(timeout=5000)
                    submitted = True
                    break
            except Exception as e:
                print("Submit-Versuch fehlgeschlagen fuer", sel, ":", e)
        print("Formular abgeschickt:", submitted)
        page.wait_for_timeout(3000)
        page.screenshot(path=f"{OUT_DIR}/its_step4_after_submit.png", full_page=True)
        print("STEP4 URL:", page.url)
        print("STEP4 TITLE:", page.title())
    else:
        print("Konnte Login-Formular nicht automatisch finden - Screenshot pruefen.")

    browser.close()

print("FERTIG")
