#!/usr/bin/env python3
"""Buhl-Kundencenter Login (einmalig) + Screenshot des Zustands danach.
Speichert Session-State, damit Folge-Skripte nicht erneut einloggen müssen.
"""
import json
import os

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright  # noqa: E402

CREDS = json.load(open("/home/bolla/workspace/config/buhl_konto.json"))
STATE_PATH = "/home/bolla/workspace/config/buhl_session_state.json"
OUT = "/tmp/claude-1000/-mnt-c-WINDOWS-System32/3fd41fa8-a1e9-4d3b-b692-bdb072218681/scratchpad/buhl_step2.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1280, "height": 1400})
    page = context.new_page()
    page.goto("https://www.buhl.de/anfrage-stellen", timeout=20000)
    page.wait_for_timeout(1000)
    page.click("text=Anmelden")
    page.wait_for_timeout(1500)
    page.screenshot(path="/tmp/claude-1000/-mnt-c-WINDOWS-System32/3fd41fa8-a1e9-4d3b-b692-bdb072218681/scratchpad/buhl_login_form.png", full_page=True)

    page.fill("#eml-user-login", CREDS["email"])
    page.fill("#psw-user-login", CREDS["password"])
    page.screenshot(path=OUT, full_page=True)

    page.click("button:has-text('Anmelden')")
    page.wait_for_timeout(2500)
    page.screenshot(path="/tmp/claude-1000/-mnt-c-WINDOWS-System32/3fd41fa8-a1e9-4d3b-b692-bdb072218681/scratchpad/buhl_step3_afterlogin.png", full_page=True)

    context.storage_state(path=STATE_PATH)
    os.chmod(STATE_PATH, 0o600)

    browser.close()

print(OUT)
