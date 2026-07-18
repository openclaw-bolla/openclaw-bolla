#!/usr/bin/env python3
"""Schritt 3: Kurs oeffnen, Mitteilungs-/Update-Bereich und Ressourcen/Upload-UI ansehen. Rein lesend."""
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


def click_first(page, selectors, timeout=5000):
    for sel in selectors:
        try:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.click(timeout=timeout)
                return sel
        except Exception as e:
            print("Klick fehlgeschlagen fuer", sel, ":", e)
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
    print("itslearning URL:", its.url)

    # Kurs "Computer Basics 7a I" oeffnen
    opened = click_first(its, ["text=Computer Basics 7a I (26/27)", "text=Computer Basics 7a I"])
    print("Kurs geklickt:", opened)
    its.wait_for_timeout(2500)
    print("Kurs-URL:", its.url)
    its.screenshot(path=f"{OUT_DIR}/its_step6_course_home.png", full_page=True)

    # Navigation innerhalb des Kurses ausgeben (Links/Tabs sichtbar)
    nav_texts = its.locator("nav a, [role='tablist'] *, header a").all_inner_texts()
    print("NAV-TEXTE:", [t.strip() for t in nav_texts if t.strip()][:40])

    browser.close()

print("FERTIG")
