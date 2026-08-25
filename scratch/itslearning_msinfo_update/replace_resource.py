#!/usr/bin/env python3
"""Ersetzt den Dateiinhalt der bestehenden Ressource '02-Elterninfo-MS-Konto.html' in einem itslearning-
Kurs über den 'Bearbeiten'-Weg (behaelt LearningToolElementId/Resource-ID bei, damit bestehende Links in
bereits veroeffentlichten Mitteilungen NICHT brechen)."""
import os
import sys
LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

import json
from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/home/bolla/workspace/scratch/itslearning_msinfo_update"
NEW_FILE = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts/Praktikum/02-Elterninfo-MS-Konto.html"
BASENAME = "02-Elterninfo-MS-Konto.html"

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


def click_visible_text(scope, text, timeout=5000):
    cand = scope.get_by_text(text, exact=True)
    for i in range(cand.count()):
        if cand.nth(i).is_visible():
            cand.nth(i).click(timeout=timeout)
            return True
    return False


def login(pw):
    browser = pw.chromium.launch()
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
    return browser, its


def replace_resource(its, course_id, kuerzel):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)
    click_first(its, ["text=Ressourcen"])
    its.wait_for_timeout(1500)

    row = its.get_by_text(BASENAME, exact=False)
    if row.count() == 0:
        print(f"  ❌ [{kuerzel}] Ressource '{BASENAME}' nicht gefunden")
        return False
    tr = row.first.locator("xpath=ancestor::tr[1]")
    more_btn = tr.locator("button").last
    more_btn.click(timeout=5000)
    its.wait_for_timeout(800)
    if not click_visible_text(its, "Bearbeiten"):
        print(f"  ❌ [{kuerzel}] 'Bearbeiten' im Zeilenmenue nicht gefunden")
        return False
    its.wait_for_timeout(2000)

    # Detailseite -> 'Bearbeiten'-Link im inneren Viewer-Frame
    clicked = False
    for fr in its.frames:
        try:
            if click_visible_text(fr, "Bearbeiten"):
                clicked = True
                break
        except Exception:
            pass
    if not clicked:
        print(f"  ❌ [{kuerzel}] 'Bearbeiten'-Link im Viewer-Frame nicht gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_no_edit_link.png", full_page=True)
        return False
    its.wait_for_timeout(2000)

    edit_frame = None
    for fr in its.frames:
        if "AddEdit.aspx" in fr.url:
            edit_frame = fr
            break
    if edit_frame is None:
        print(f"  ❌ [{kuerzel}] AddEdit-Frame nicht gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_no_addedit_frame.png", full_page=True)
        return False

    # Vorhandene Datei entfernen (Delete-Button), falls vorhanden
    delete_btn = edit_frame.locator("button[aria-label='Delete']")
    if delete_btn.count() > 0:
        delete_btn.first.click(timeout=5000)
        its.wait_for_timeout(500)
        print(f"  🗑️ [{kuerzel}] Alte Datei-Anlage im Edit-Formular entfernt")

    # Dropzone anklicken - je nach Zustand oeffnet das entweder direkt den nativen Dateidialog
    # (leerer Zustand nach Delete) oder ein Popover mit Quellenauswahl ('Ihr Computer - Datei' etc.)
    dz = edit_frame.locator("button.ccl-uc-dropzone-container")
    if dz.count() == 0:
        print(f"  ❌ [{kuerzel}] Dropzone-Button nicht gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_no_dropzone.png", full_page=True)
        return False

    fc = None
    try:
        with its.expect_file_chooser(timeout=4000) as fc_info:
            dz.first.click(timeout=5000)
        fc = fc_info.value
    except Exception:
        # Kein direkter Dateidialog - vermutlich Popover mit Quellenauswahl erschienen
        its.wait_for_timeout(800)
        local_picker = edit_frame.locator("#local-picker")
        if local_picker.count() == 0:
            print(f"  ❌ [{kuerzel}] Weder direkter Dateidialog noch 'local-picker' gefunden")
            its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_no_localpicker.png", full_page=True)
            return False
        try:
            with its.expect_file_chooser(timeout=5000) as fc_info:
                local_picker.first.click(timeout=5000)
            fc = fc_info.value
        except Exception as e:
            print(f"  ❌ [{kuerzel}] Datei-Auswahl ueber Popover fehlgeschlagen: {e}")
            its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_filechooser.png", full_page=True)
            return False

    try:
        fc.set_files([NEW_FILE])
    except Exception as e:
        print(f"  ❌ [{kuerzel}] set_files fehlgeschlagen: {e}")
        return False

    its.wait_for_timeout(3000)
    its.screenshot(path=f"{OUT_DIR}/{course_id}_after_new_file_selected.png", full_page=True)

    # 'Speichern' klicken - kann in der aeusseren Seite ODER im edit_frame liegen
    saved = False
    for scope_name, scope in [("outer", its)] + [(fr.url, fr) for fr in its.frames]:
        try:
            save_btn = scope.get_by_text("Speichern", exact=True)
            cnt = save_btn.count()
        except Exception:
            continue
        if cnt == 0:
            continue
        for i in range(cnt):
            try:
                if save_btn.nth(i).is_visible():
                    print(f"  [{kuerzel}] Klicke 'Speichern' in scope={scope_name!r} idx={i}")
                    save_btn.nth(i).click(timeout=5000)
                    saved = True
                    break
            except Exception:
                continue
        if saved:
            break
    if not saved:
        print(f"  ❌ [{kuerzel}] 'Speichern'-Button nicht gefunden/klickbar")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_no_save.png", full_page=True)
        return False

    its.wait_for_timeout(2500)
    its.screenshot(path=f"{OUT_DIR}/{course_id}_after_save.png", full_page=True)
    print(f"  ✅ [{kuerzel}] Datei ersetzt + gespeichert")
    return True


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    results = []
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            for c in COURSES:
                if only and c["kuerzel"] != only:
                    continue
                print(f"\n=== {c['kuerzel']} (CourseID {c['id']}) ===")
                ok = replace_resource(its, c["id"], c["kuerzel"])
                results.append((c["kuerzel"], "OK" if ok else "FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG ===")
    for kuerzel, status in results:
        print(f"{kuerzel}: {status}")
