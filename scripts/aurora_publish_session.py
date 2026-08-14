#!/usr/bin/env python3
"""Sichtbare, persistente Playwright-Session für den gemeinsamen AURORA-Republish (Kap. 47 Update).
Läuft headed (WSLg DISPLAY), Profil bleibt zwischen Aufrufen erhalten -> Login-Session übersteht Neustarts.

Nutzung: python3 aurora_publish_session.py <url>
"""
import os
import sys

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright  # noqa: E402

PROFILE_DIR = "/home/bolla/workspace/config/browser_profile_aurora_publish"

url = sys.argv[1] if len(sys.argv) > 1 else "https://kdp.amazon.com/en_US/bookshelf"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        PROFILE_DIR,
        headless=False,
        viewport={"width": 1400, "height": 950},
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(url, timeout=30000)
    print("Browser offen, bleibt bestehen bis Enter gedrückt wird...")
    input()
    ctx.close()
