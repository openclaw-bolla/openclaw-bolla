#!/usr/bin/env python3
"""Zweite sichtbare Browser-Session, diesmal echtes System-Edge statt Playwright-Chromium,
weil Google Play Books den Playwright-Chromium-Fingerabdruck als 'nicht sicher' blockt.
"""
import os
import time

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright  # noqa: E402

PROFILE_DIR = "/home/bolla/workspace/config/browser_profile_aurora_publish_edge"
PORT = 9334

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        PROFILE_DIR,
        headless=False,
        channel="msedge",
        viewport={"width": 1400, "height": 950},
        args=[f"--remote-debugging-port={PORT}"],
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://play.google.com/books/publish/", timeout=30000)
    print(f"READY on port {PORT}")
    while True:
        time.sleep(3600)
