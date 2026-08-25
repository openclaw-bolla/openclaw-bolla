#!/usr/bin/env python3
"""Recon 5: Im 'Bearbeiten'-Formular auf das 'X' neben dem Dateinamen klicken - prueft, ob danach eine
Upload-Dropzone erscheint, mit der man die Datei ERSETZEN kann, ohne die Resource-ID/den Link zu verlieren."""
import os
LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

import json
from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/home/bolla/workspace/scratch/itslearning_msinfo_update"
COURSE_ID = 190735  # 7a I

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

    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={COURSE_ID}", timeout=20000)
    its.wait_for_timeout(2000)
    click_first(its, ["text=Ressourcen"])
    its.wait_for_timeout(1500)

    row = its.get_by_text("02-Elterninfo-MS-Konto.html", exact=False)
    tr = row.first.locator("xpath=ancestor::tr[1]")
    more_btn = tr.locator("button").last
    more_btn.click(timeout=5000)
    its.wait_for_timeout(800)
    bearbeiten_candidates = its.get_by_text("Bearbeiten", exact=True)
    for i in range(bearbeiten_candidates.count()):
        if bearbeiten_candidates.nth(i).is_visible():
            bearbeiten_candidates.nth(i).click(timeout=5000)
            break
    its.wait_for_timeout(2000)

    clicked = False
    for fr in its.frames:
        try:
            cand = fr.get_by_text("Bearbeiten", exact=True)
            for i in range(cand.count()):
                if cand.nth(i).is_visible():
                    cand.nth(i).click(timeout=5000)
                    clicked = True
                    break
        except Exception:
            pass
        if clicked:
            break
    its.wait_for_timeout(2000)

    # Im Edit-Frame das 'X' neben dem Dateinamen klicken
    edit_frame = None
    for fr in its.frames:
        if "AddEdit.aspx" in fr.url:
            edit_frame = fr
            break
    if edit_frame is None:
        print("AddEdit-Frame nicht gefunden!")
    else:
        html = edit_frame.locator("body").evaluate("el => el.innerHTML")
        with open(f"{OUT_DIR}/05_edit_frame.html", "w") as f:
            f.write(html)
        print("HTML-Dump gespeichert:", f"{OUT_DIR}/05_edit_frame.html", "Laenge:", len(html))
        edit_frame.screenshot(path=f"{OUT_DIR}/05_edit_frame_before_x.png")

        buttons = edit_frame.locator("button")
        print("Anzahl <button> im Edit-Frame:", buttons.count())
        for i in range(buttons.count()):
            try:
                al = buttons.nth(i).get_attribute("aria-label")
                txt = buttons.nth(i).inner_text().strip()
                bb = buttons.nth(i).bounding_box()
                print(f"  [{i}] aria-label={al!r} text={txt!r} bbox={bb}")
            except Exception as e:
                print(f"  [{i}] Fehler: {e}")

    browser.close()
print("Fertig - Screenshots in", OUT_DIR)
