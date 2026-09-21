#!/usr/bin/env python3
"""Ersetzt eine bestehende Ressource in itslearning IN PLACE (Resource-ID bleibt, Mitteilungs-Anhang bleibt gueltig).
Ablauf siehe [[project_itslearning_automation]] Abschnitt "Datei ersetzen" (25.08.2026).
Aufruf: itslearning_replace_resource.py <basename> <lokaler_pfad> <kuerzel1,kuerzel2|all>"""
import sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
import itslearning_post_kurstag as base
from playwright.sync_api import sync_playwright

IDS = {"7a I": 190735, "7a II": 190738, "7b I": 190741, "7b II": 190743,
       "7c I": 190861, "7c II": 190878, "7d I": 190860, "7d II": 190877}
OUT = base.OUT_DIR


def replace_in_course(its, cid, basename, path):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={cid}", timeout=20000)
    its.wait_for_timeout(2000)
    base.click_first(its, ["text=Ressourcen"])
    its.wait_for_timeout(2000)
    cell = its.get_by_text(basename, exact=False)
    if cell.count() == 0:
        print("  ❌ Ressource nicht gefunden"); its.screenshot(path=f"{OUT}/FAIL_{cid}_nores.png"); return False
    if cell.count() > 1:
        print(f"  ⚠️ {cell.count()} Treffer fuer Basename - breche ab (Duplikat?)"); return False
    tr = cell.first.locator("xpath=ancestor::tr[1]")
    tr.locator("button").last.click(); its.wait_for_timeout(800)
    edit = [e for e in its.get_by_text("Bearbeiten", exact=True).all() if e.is_visible()]
    if not edit:
        print("  ❌ Menue 'Bearbeiten' nicht sichtbar"); its.screenshot(path=f"{OUT}/FAIL_{cid}_menu.png"); return False
    edit[0].click(); its.wait_for_timeout(3000)
    # zweiter Bearbeiten-Link im verschachtelten Frame resource.itslearning.com/File/View.aspx
    clicked = False
    for fr in its.frames:
        if "File/View" in fr.url:
            for e in fr.get_by_text("Bearbeiten").all():
                if e.is_visible():
                    e.click(); clicked = True; break
        if clicked: break
    if not clicked:
        print("  ❌ 2. Bearbeiten-Link nicht gefunden"); its.screenshot(path=f"{OUT}/FAIL_{cid}_edit2.png"); return False
    its.wait_for_timeout(3000)
    ed = next((fr for fr in its.frames if "AddEdit" in fr.url), None)
    if ed is None:
        print("  ❌ AddEdit-Frame fehlt"); its.screenshot(path=f"{OUT}/FAIL_{cid}_addedit.png"); return False
    ed.locator("button[aria-label='Delete']").first.click(); its.wait_for_timeout(1000)
    try:
        with its.expect_file_chooser(timeout=4000) as fc:
            ed.locator("button.ccl-uc-dropzone-container").first.click()
        fc.value.set_files([path])
    except Exception:
        ed.locator("button.ccl-uc-dropzone-container").first.click(); its.wait_for_timeout(800)
        with its.expect_file_chooser(timeout=5000) as fc:
            ed.locator("#local-picker").first.click()
        fc.value.set_files([path])
    its.wait_for_timeout(3000)
    saved = False
    for fr in list(its.frames) + [its]:
        try:
            loc = fr.get_by_text("Speichern", exact=True)
            for i in range(loc.count()):
                if loc.nth(i).is_visible():
                    loc.nth(i).click(timeout=3000); saved = True; break
        except Exception:
            continue
        if saved: break
    its.wait_for_timeout(3000)
    if not saved:
        print("  ❌ Speichern nicht gefunden"); its.screenshot(path=f"{OUT}/FAIL_{cid}_save.png"); return False
    ok = its.get_by_text("Die Datei wurde ersetzt").count() > 0
    its.screenshot(path=f"{OUT}/replace_{cid}.png")
    print("  ✅ ersetzt (Toast gesehen)" if ok else "  ⚠️ gespeichert, Toast nicht gesehen - bitte pruefen")
    return True


if __name__ == "__main__":
    basename, path, which = sys.argv[1], sys.argv[2], sys.argv[3]
    ks = list(IDS) if which == "all" else which.split(",")
    with sync_playwright() as p:
        browser, its = base.login(p)
        try:
            for k in ks:
                print(f"=== {k} ===")
                replace_in_course(its, IDS[k], basename, path)
        finally:
            browser.close()
