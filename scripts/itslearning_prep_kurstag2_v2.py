#!/usr/bin/env python3
"""V2: Nur noch EINE Mitteilung pro Kurs (Schueler, keine Eltern-Mitteilung mehr).
Anhaenge: 02-Praktikum.html, 02-The Basics - Grundbegriffe - II.pdf (frisch ersetzt, alte
Version wird vorher geloescht), 02-Fenster-Anleitung.html. 01-* Dateien NICHT erneut anhaengen
(schon seit 17.08. gepostet). Text beschreibt neuen 4-Schritte-Ablauf. Kein Veroeffentlichen."""
import os
LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

import json
from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
PRAKT_DIR = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts/Praktikum"
OUT_DIR = "/home/bolla/workspace/scratch/itslearning_kurstag2_vorschau"
os.makedirs(OUT_DIR, exist_ok=True)

PDF_BASENAME = "02-The Basics - Grundbegriffe - II"
STUDENT_FILES = [
    {"path": os.path.join(PRAKT_DIR, "02-Praktikum.html"), "basename": "02-Praktikum"},
    {"path": os.path.join(PRAKT_DIR, "02-The Basics - Grundbegriffe - II.pdf"), "basename": PDF_BASENAME},
    {"path": os.path.join(PRAKT_DIR, "02-Fenster-Anleitung.html"), "basename": "02-Fenster-Anleitung"},
]

COURSES = [
    {"id": 190735, "kuerzel": "7a I",
     "student_text":
        "🖥️ Hallo liebe 7a! So geht's heute weiter: 1️⃣ Wir laden gemeinsam am Beamer eine Datei aus "
        "itslearning herunter, ich zeig's euch einmal. 2️⃣ Danach macht ihr Praktikum 1 (liegt schon "
        "hier aus der letzten Mitteilung). 3️⃣ Wenn noch Zeit ist - oder auch zuhause bzw. in einer der "
        "nächsten Stunden, kein Zeitdruck: die restlichen Dateien (Folien, Anleitungen) auf euren Stick "
        "laden und dafür eine eigene Ordnerstruktur anlegen. 4️⃣ Zum Schluss dann 📎 Praktikum 2. Viel "
        "Spaß! 🎨"},
    {"id": 190741, "kuerzel": "7b I",
     "student_text":
        "🎉 Liebe 7b, unser Fahrplan für heute: 1️⃣ Erst zeige ich euch gemeinsam am Beamer, wie der "
        "Download aus itslearning geht. 2️⃣ Dann macht ihr Praktikum 1 (schon aus der letzten Mitteilung "
        "hier vorhanden). 3️⃣ Falls Zeit bleibt - sonst auch gerne zuhause oder in einer der nächsten "
        "Stunden, kein Stress: die übrigen Dateien auf den Stick laden und eine eigene Ordnerstruktur "
        "dafür anlegen. 4️⃣ Danach geht's mit 📎 Praktikum 2 weiter. Bin gespannt! 😊"},
    {"id": 190861, "kuerzel": "7c I",
     "student_text":
        "🚀 Hallo 7c! Ablauf für heute: 1️⃣ Wir laden zusammen am Beamer eine Datei aus itslearning "
        "herunter - einmal vorgemacht. 2️⃣ Danach kommt Praktikum 1 dran (liegt schon aus der letzten "
        "Mitteilung bereit). 3️⃣ Wenn ihr noch Zeit/Lust habt - auch später zuhause oder in einer der "
        "nächsten Stunden möglich, kein Muss sofort: die restlichen Dateien auf den Stick laden und eine "
        "eigene Ordnerstruktur dafür bauen. 4️⃣ Zum Abschluss 📎 Praktikum 2. Auf geht's! 💻"},
    {"id": 190860, "kuerzel": "7d I",
     "student_text":
        "😊 Liebe 7d, so läuft's heute: 1️⃣ Zuerst zeige ich euch gemeinsam am Beamer den Download aus "
        "itslearning. 2️⃣ Dann macht ihr Praktikum 1 (schon aus der letzten Mitteilung vorhanden). 3️⃣ "
        "Wenn noch Zeit ist - sonst auch zuhause oder in einer der kommenden Stunden, ganz ohne Eile: die "
        "übrigen Dateien auf den Stick laden und eine eigene Ordnerstruktur anlegen. 4️⃣ Zuletzt 📎 "
        "Praktikum 2. Freu mich auf euch! 🎉"},
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
    """Loescht die alte Version der PDF-Ressource (falls vorhanden), damit der Upload weiter unten
    garantiert eine frische Kopie hochlaedt statt die veraltete stehen zu lassen."""
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


def compose_message_no_publish(its, course_id, text, files, kuerzel):
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

    shot_path = f"{OUT_DIR}/PREVIEW_{kuerzel.replace(' ','_')}_schueler.png"
    its.screenshot(path=shot_path, full_page=True)
    print(f"  📸 Vorschau-Screenshot gespeichert: {shot_path} — NICHT veroeffentlicht.")
    return True


if __name__ == "__main__":
    results = []
    texts_log = []
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

                ok = compose_message_no_publish(its, c["id"], c["student_text"], STUDENT_FILES, c["kuerzel"])
                results.append((c["kuerzel"], "VORSCHAU OK" if ok else "MITTEILUNG FEHLGESCHLAGEN"))
                if ok:
                    texts_log.append({
                        "kurs": c["kuerzel"], "course_id": c["id"],
                        "schueler_text": c["student_text"],
                        "schueler_anhaenge": [f["basename"] for f in STUDENT_FILES],
                        "hinweis": "PDF wurde vor dem Upload geloescht+neu hochgeladen (frische Version, Folie 6 ueberarbeitet). Keine Eltern-Mitteilung mehr (Chris druckt das selbst aus).",
                    })
        finally:
            browser.close()

    with open(f"{OUT_DIR}/texte_und_anhaenge.json", "w", encoding="utf-8") as f:
        json.dump(texts_log, f, ensure_ascii=False, indent=2)

    print("\n=== ZUSAMMENFASSUNG ===")
    for kuerzel, status in results:
        print(f"{kuerzel}: {status}")
    print(f"\nTexte+Anhaenge-Protokoll: {OUT_DIR}/texte_und_anhaenge.json")
