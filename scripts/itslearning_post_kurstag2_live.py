#!/usr/bin/env python3
"""LIVE-Variante von itslearning_prep_kurstag2_v2.py: identischer Ablauf (PDF-Ressource
loeschen+frisch hochladen, Mitteilung mit Anhaengen komponieren), klickt am Ende aber wirklich
"Veroeffentlichen" statt nur einen Vorschau-Screenshot zu machen.

Bewusst NICHT automatisch im Cron eingetragen - Chris entscheidet den Zeitpunkt selbst und startet
das Skript manuell im Chat, sobald er heute Abend so weit ist (siehe
feedback_kein_zusatzunterricht_nachmittag.md: Zeitpunkt bewusst spaet, damit Schueler die Dateien
nicht noch zuhause bearbeiten).

Texte sind bereits korrigiert (kein "zuhause"-Hinweis mehr, siehe project_itslearning_automation).

V3 (24.08.2026): Reihenfolge umgestellt - ALLE 8 Dateien werden ZUERST heruntergeladen (2 gemeinsam
am Beamer, 6 selbststaendig), bevor irgendein Praktikum beginnt. Elterninfo-PDF bleibt draussen
(Chris druckt selbst aus), Elterninfo-HTML ist diesmal mit dabei.
"""
import os
LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

import json
from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
PRAKT_DIR = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts/Praktikum"
OUT_DIR = "/home/bolla/workspace/scratch/itslearning_kurstag2_live"
os.makedirs(OUT_DIR, exist_ok=True)

PDF_BASENAME = "02-The Basics - Grundbegriffe - II"
STUDENT_FILES = [
    {"path": os.path.join(PRAKT_DIR, "01-Download-Anleitung.html"), "basename": "01-Download-Anleitung"},
    {"path": os.path.join(PRAKT_DIR, "01-The Basics - Grundbegriffe - I.pdf"), "basename": "01-The Basics - Grundbegriffe - I"},
    {"path": os.path.join(PRAKT_DIR, "01-Editor-Anleitung.html"), "basename": "01-Editor-Anleitung"},
    {"path": os.path.join(PRAKT_DIR, "01-Praktikum.html"), "basename": "01-Praktikum"},
    {"path": os.path.join(PRAKT_DIR, "02-Elterninfo-MS-Konto.html"), "basename": "02-Elterninfo-MS-Konto"},
    {"path": os.path.join(PRAKT_DIR, "02-Fenster-Anleitung.html"), "basename": "02-Fenster-Anleitung"},
    # 02-Praktikum ersatzlos gestrichen (Chris, 28.08.2026) - nie unterrichtet, aus itslearning entfernt.
    {"path": os.path.join(PRAKT_DIR, "02-The Basics - Grundbegriffe - II.pdf"), "basename": PDF_BASENAME},
]

COURSES = [
    {"id": 190735, "kuerzel": "7a I",
     "student_text":
        "🖥️ Hallo liebe 7a! Heute geht's erstmal ums Herunterladen: 1️⃣ Wir laden gemeinsam am Beamer "
        "die Download-Anleitung und die Grundbegriffe-I-PDF herunter, damit ihr beide Dateiformate (HTML "
        "und PDF) einmal gesehen habt. 2️⃣ Danach ladet ihr selbstständig die restlichen 6 Dateien "
        "herunter. 3️⃣ Dann geht's mit 📎 Praktikum 1 los - dort lernt ihr auch, was ein Ordner ist und "
        "wie man aufräumt. Wenn noch Zeit bleibt, räumt ihr direkt auch bei 📎 Praktikum 2 auf - sonst "
        "machen wir das Schritt für Schritt in den nächsten Stunden weiter. Viel Spaß! 🎨"},
    {"id": 190741, "kuerzel": "7b I",
     "student_text":
        "🎉 Liebe 7b, heute steht erstmal das Herunterladen im Mittelpunkt: 1️⃣ Erst laden wir gemeinsam "
        "am Beamer die Download-Anleitung und die Grundbegriffe-I-PDF herunter, damit ihr beide "
        "Dateiformate (HTML und PDF) einmal gesehen habt. 2️⃣ Dann ladet ihr selbstständig die übrigen 6 "
        "Dateien herunter. 3️⃣ Danach startet 📎 Praktikum 1 - da lernt ihr auch, was ein Ordner ist und "
        "wie man ordentlich aufräumt. Bleibt Zeit, räumt ihr gleich bei 📎 Praktikum 2 mit auf - sonst "
        "machen wir in den nächsten Stunden Schritt für Schritt weiter. Bin gespannt! 😊"},
    {"id": 190861, "kuerzel": "7c I",
     "student_text":
        "🚀 Hallo 7c! Heute geht's erstmal ums Herunterladen: 1️⃣ Wir laden zusammen am Beamer die "
        "Download-Anleitung und die Grundbegriffe-I-PDF herunter - einmal vorgemacht, damit ihr beide "
        "Dateiformate (HTML und PDF) gesehen habt. 2️⃣ Danach ladet ihr die restlichen 6 Dateien "
        "selbstständig herunter. 3️⃣ Dann kommt 📎 Praktikum 1 dran - dort lernt ihr auch, was ein "
        "Ordner ist und wie man aufräumt. Wenn ihr noch Zeit/Lust habt, räumt ihr gleich bei 📎 "
        "Praktikum 2 mit auf - sonst machen wir das Schritt für Schritt in den nächsten Stunden weiter. "
        "Auf geht's! 💻"},
    {"id": 190860, "kuerzel": "7d I",
     "student_text":
        "😊 Liebe 7d, heute geht's erstmal ums Herunterladen: 1️⃣ Zuerst laden wir gemeinsam am Beamer die "
        "Download-Anleitung und die Grundbegriffe-I-PDF herunter, damit ihr beide Dateiformate (HTML und "
        "PDF) einmal gesehen habt. 2️⃣ Dann ladet ihr die übrigen 6 Dateien selbstständig herunter. 3️⃣ "
        "Danach startet 📎 Praktikum 1 - dort lernt ihr auch, was ein Ordner ist und wie man aufräumt. "
        "Wenn noch Zeit ist, räumt ihr direkt auch bei 📎 Praktikum 2 mit auf - sonst machen wir das "
        "Schritt für Schritt in den nächsten Stunden weiter. Freu mich auf euch! 🎉"},
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


def delete_stale_pdf(its, course_id, basename):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)
    click_first(its, ["text=Ressourcen"])
    its.wait_for_timeout(1500)

    row = its.get_by_text(basename, exact=False)
    if row.count() == 0:
        print(f"  ⏭ Keine bestehende '{basename}'-Ressource - nichts zu loeschen")
        return True

    cb = row.first.locator("xpath=preceding::input[@type='checkbox'][1]")
    cb.evaluate("el => el.click()")
    its.wait_for_timeout(300)

    del_candidates = its.get_by_role("button", name="Löschen", exact=True)
    del_btn = None
    for i in range(del_candidates.count()):
        if del_candidates.nth(i).is_visible():
            del_btn = del_candidates.nth(i)
            break
    if del_btn is None:
        print(f"  ❌ Loeschen-Aktion nicht gefunden fuer '{basename}'")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_delete_pdf.png", full_page=True)
        return False
    del_btn.click()
    its.wait_for_timeout(800)

    confirm = its.locator("div.prom-modal2__footer button.prom-button__destructive")
    if confirm.count() > 0:
        confirm.first.click(timeout=5000)
        its.wait_for_timeout(1500)
        print(f"  🗑️ Alte '{basename}'-Ressource geloescht (wird gleich frisch neu hochgeladen)")
        return True
    print(f"  ❌ Bestaetigungs-Button beim Loeschen nicht gefunden fuer '{basename}'")
    return False


def upload_files(its, course_id, files):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)
    click_first(its, ["text=Ressourcen"])
    its.wait_for_timeout(1500)

    missing = [f for f in files if its.get_by_text(f["basename"]).count() == 0]
    if not missing:
        print(f"  ⏭ Alle {len(files)} Datei(en) liegen schon vor - Upload uebersprungen")
        return True

    click_first(its, ["text=Hinzufügen"])
    its.wait_for_timeout(700)
    click_first(its, ["text=Datei oder Ordner"])
    its.wait_for_timeout(1500)

    inner = its.frames[-1]
    dz = inner.locator("button.ccl-uc-dropzone-container")
    if dz.count() == 0:
        print("  ❌ Dropzone-Button nicht gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_dropzone.png", full_page=True)
        return False
    dz.first.click()
    its.wait_for_timeout(800)

    picker_frame = None
    for fr in its.frames:
        if fr.locator("text=Ihr Computer – Datei").count() > 0:
            picker_frame = fr
            break
    if picker_frame is None:
        print("  ❌ 'Ihr Computer – Datei' nicht gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_picker.png", full_page=True)
        return False

    try:
        with its.expect_file_chooser(timeout=5000) as fc_info:
            picker_frame.locator("text=Ihr Computer – Datei").first.click()
        fc = fc_info.value
        fc.set_files([f["path"] for f in missing])
    except Exception as e:
        print("  ❌ Datei-Auswahl fehlgeschlagen:", e)
        return False

    its.wait_for_timeout(3000)
    ok = False
    for _ in range(20):
        for fr in its.frames:
            try:
                if all(fr.locator(f"text={f['basename']}").count() > 0 for f in missing):
                    ok = True
                    break
            except Exception:
                continue
        if ok:
            break
        its.wait_for_timeout(1000)
    if not ok:
        print("  ❌ Upload-Vorschau zeigt nicht alle Dateien nach Wartezeit")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_uploadpreview.png", full_page=True)
        return False

    saved = None
    for fr in its.frames:
        try:
            if fr.locator("text=Speichern").count() > 0:
                fr.locator("text=Speichern").first.click(timeout=3000)
                saved = fr
                break
        except Exception:
            continue
    its.wait_for_timeout(2500)
    if not saved:
        print("  ❌ 'Speichern'-Button nicht gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_savebtn.png", full_page=True)
        return False

    print(f"  ✅ {len(missing)} Datei(en) hochgeladen und gespeichert")
    return True


def compose_and_publish(its, course_id, text, files, kuerzel):
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)

    click_first(its, ["text=Mitteilung schreiben", "[contenteditable='true']"])
    its.wait_for_timeout(700)

    box = its.locator("li.itsl-light-bulletins-new-item-listitem").first
    if box.count() == 0:
        print("  ❌ Mitteilungs-Box nicht gefunden")
        return False

    editor = box.locator("[contenteditable='true']").first
    editor.click()
    editor.fill(text)
    its.wait_for_timeout(500)

    box.get_by_text("Ressource", exact=False).first.click()
    its.wait_for_timeout(1200)

    dialog = its.locator("[role='dialog']")
    if dialog.count() == 0:
        print("  ❌ Kein [role=dialog]-Container gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_nodialog.png", full_page=True)
        return False
    dialog = dialog.first

    basename_seen = {}
    for f in files:
        row = dialog.get_by_text(f["basename"], exact=False)
        idx = basename_seen.get(f["basename"], 0)
        if row.count() <= idx:
            print(f"  ❌ Datei '{f['basename']}' (Index {idx}) im Ressource-Dialog nicht gefunden")
            its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_attachpicker.png", full_page=True)
            return False
        basename_seen[f["basename"]] = idx + 1
        cb = row.nth(idx).locator("xpath=preceding::input[@type='checkbox'][1]")
        cb.evaluate("el => el.click()")

    confirm = dialog.locator("input[value='Hinzufügen']")
    if confirm.count() > 0:
        confirm.first.evaluate("el => el.click()")
    else:
        click_first(its, ["text=Hinzufügen"])
    its.wait_for_timeout(1500)

    published = click_first(its, ["text=Veröffentlichen"])
    its.wait_for_timeout(2000)
    if not published:
        print("  ❌ 'Veröffentlichen'-Button nicht gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_publish.png", full_page=True)
        return False

    print(f"  ✅ Mitteilung veroeffentlicht ({kuerzel}, Kurs {course_id})")
    return True


if __name__ == "__main__":
    results = []
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            for c in COURSES:
                print(f"\n=== {c['kuerzel']} (CourseID {c['id']}) ===")

                del_ok = delete_stale_pdf(its, c["id"], PDF_BASENAME)
                up_ok = upload_files(its, c["id"], STUDENT_FILES)
                if not (del_ok and up_ok):
                    results.append((c["kuerzel"], "UPLOAD/LOESCHEN FEHLGESCHLAGEN"))
                    continue

                ok = compose_and_publish(its, c["id"], c["student_text"], STUDENT_FILES, c["kuerzel"])
                results.append((c["kuerzel"], "VEROEFFENTLICHT" if ok else "VEROEFFENTLICHEN FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG ===")
    for kuerzel, status in results:
        print(f"{kuerzel}: {status}")
