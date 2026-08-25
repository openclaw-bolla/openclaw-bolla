#!/usr/bin/env python3
"""Verifiziert fuer alle 4 Kurse per Download, dass der neue Absatz im Inhalt steckt."""
import os
LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

import json
from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/home/bolla/workspace/scratch/itslearning_msinfo_update"
COURSES = [
    {"id": 190735, "kuerzel": "7a I"},
    {"id": 190741, "kuerzel": "7b I"},
    {"id": 190861, "kuerzel": "7c I"},
    {"id": 190860, "kuerzel": "7d I"},
]

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


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1400, "height": 1100})
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

    for c in COURSES:
        its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={c['id']}", timeout=20000)
        its.wait_for_timeout(1500)
        click_first(its, ["text=Ressourcen"])
        its.wait_for_timeout(1200)
        row = its.get_by_text("02-Elterninfo-MS-Konto.html", exact=False)
        if row.count() == 0:
            print(f"{c['kuerzel']}: ❌ Ressource nicht gefunden")
            continue
        row.first.click(timeout=5000)
        its.wait_for_timeout(1800)

        dl_btn = None
        for fr in its.frames:
            cand = fr.get_by_text("Herunterladen", exact=False)
            if cand.count() > 0 and cand.first.is_visible():
                dl_btn = cand.first
                break
        if dl_btn is None:
            print(f"{c['kuerzel']}: ❌ Download-Button nicht gefunden")
            continue
        try:
            with its.expect_download(timeout=10000) as dl_info:
                dl_btn.click(timeout=5000)
            dl = dl_info.value
            save_path = f"{OUT_DIR}/verify_{c['id']}.html"
            dl.save_as(save_path)
            content = open(save_path, encoding="utf-8", errors="replace").read()
            ok = "Microsoft-Anmeldeseite" in content
            print(f"{c['kuerzel']}: {'✅ neuer Absatz vorhanden' if ok else '❌ FEHLT'} ({len(content)} Bytes)")
        except Exception as e:
            print(f"{c['kuerzel']}: ❌ Download-Fehler: {e}")

    browser.close()
print("Fertig")
