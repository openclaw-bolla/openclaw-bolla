#!/usr/bin/env python3
"""Headless-Browser-Screenshot für Bolla — sichtet Webseiten fuer Chris' Terminal-Session.

Verwendung:
    python3 browser_screenshot.py <url> [--out PATH] [--width N] [--height N] [--full-page] [--wait MS]

Beispiel:
    python3 browser_screenshot.py http://127.0.0.1:18790/ --out /tmp/mp.png --full-page
"""
import argparse
import os
import sys

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--out", default="/tmp/screenshot.png")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--full-page", action="store_true")
    parser.add_argument("--wait", type=int, default=800, help="ms warten nach dem Laden")
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.goto(args.url, timeout=20000)
        page.wait_for_timeout(args.wait)
        page.screenshot(path=args.out, full_page=args.full_page)
        browser.close()

    print(args.out)


if __name__ == "__main__":
    main()
