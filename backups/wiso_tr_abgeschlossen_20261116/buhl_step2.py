#!/usr/bin/env python3
"""Nutzt gespeicherten Buhl-Login-Session-State, navigiert zum WISO Mein Geld Vertrag."""
import os

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright  # noqa: E402

STATE_PATH = "/home/bolla/workspace/config/buhl_session_state.json"
SCRATCH = "/tmp/claude-1000/-mnt-c-WINDOWS-System32/3fd41fa8-a1e9-4d3b-b692-bdb072218681/scratchpad"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(storage_state=STATE_PATH, viewport={"width": 1280, "height": 1400})
    page = context.new_page()
    page.goto("https://www.buhl.de/kundencenter/", timeout=20000)
    page.wait_for_timeout(1500)
    page.click("text=Meine Anfragen")
    page.wait_for_timeout(2000)
    page.click("text=Trade Republic Depot lässt sich nicht synchronisieren")
    page.wait_for_timeout(2000)
    page.screenshot(path=f"{SCRATCH}/buhl_step5_ticket.png", full_page=True)
    print(page.url)
    browser.close()
