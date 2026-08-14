#!/usr/bin/env python3
"""Startet eine sichtbare, dauerhafte Chromium-Session (WSLg) mit Remote-Debugging-Port,
damit spätere Aufrufe sich per CDP wieder anklinken können, während Chris im selben
Fenster Logins/2FA selbst erledigt. Läuft im Hintergrund weiter (run_in_background).
"""
import os
import time

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright  # noqa: E402

PROFILE_DIR = "/home/bolla/workspace/config/browser_profile_aurora_publish"
PORT = 9333

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        PROFILE_DIR,
        headless=False,
        viewport={"width": 1400, "height": 950},
        args=[f"--remote-debugging-port={PORT}"],
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://kdp.amazon.com/en_US/bookshelf", timeout=30000)
    print(f"READY on port {PORT}")
    while True:
        time.sleep(3600)
