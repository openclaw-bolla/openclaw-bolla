#!/usr/bin/env python3
"""Kurstag-Handouts (PDF + alle passenden HTML-Dateien mit gleicher Tagesnummer) in die Ressourcen
hochladen und als individuelle Mitteilung in mehreren Kursen posten.

Nachfolger von itslearning_post_kurstag01.py - generalisiert auf beliebige Kurstage/Kurse.
Siehe [[project_itslearning_automation]] fuer alle DOM-Fallstricke, die hier schon eingearbeitet sind.
"""
import json
import os

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
HANDOUTS = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts"
OUT_DIR = "/tmp/its_debug"
os.makedirs(OUT_DIR, exist_ok=True)

# Selbst-Bremse: siehe reference_wsl.md — Freeze am 23.07.2026 kam vermutlich aus genau so einem
# Lauf. Der externe wsl_memory_watchdog.py greift erst ab 88%/94%; hier soll das Skript sich VORHER
# selbst und sauber (mit browser.close()) beenden, statt vom Wächter hart abgeschossen zu werden.
MEM_ABORT_PCT = 80


def mem_ok():
    with open("/proc/meminfo") as f:
        info = {}
        for line in f:
            k, v = line.split(":")
            info[k.strip()] = int(v.strip().split()[0])
    total = info["MemTotal"]
    available = info["MemAvailable"]
    used_pct = (total - available) / total * 100
    return used_pct < MEM_ABORT_PCT, used_pct

# ⚠️ Vor jedem Lauf anpassen: Tagesnummer (zweistellig, siehe [[project_schuljahr2627]]-Konvention),
# die 4 Ziel-Kurse (Kurs-IDs bleiben das ganze Schuljahr stabil, siehe Tabelle unten) und je einen
# individuell formulierten Mitteilungstext (NIE denselben Text kopieren, NIE "vorher/schon jetzt
# herunterladen" schreiben - Download passiert am Kurstag selbst, siehe [[project_itslearning_automation]]).
DAY_PREFIX = "01"

# Kurs-IDs (Schuljahr 26/27, stabil): 7a I=190735 7a II=190738 7b I=190741 7b II=190743
#                                     7c I=190861 7c II=190878 7d I=190860 7d II=190877
COURSES = [
    {"id": 190735, "kuerzel": "7a I", "text":
        "👋 Hallo liebe 7a! Am 19.08. starten wir ins EDV-Schuljahr mit den ersten "
        "Computer-Grundbegriffen. 📎 Folien, ein Praktikum und eine kurze Editor-Anleitung liegen "
        "hier schon bereit - wir laden alles gemeinsam zu Beginn der Stunde herunter. "
        "Freu mich auf euch! 😊"},
    {"id": 190741, "kuerzel": "7b I", "text":
        "🎉 Liebe 7b, unser EDV-Abenteuer beginnt am 19.08. mit den Grundbegriffen rund um den "
        "Computer. 📎 Folien, Praktikum und eine Anleitung für den Editor findet ihr hier - "
        "heruntergeladen wird alles gemeinsam in der Stunde. Bis bald! 🙂"},
    {"id": 190861, "kuerzel": "7c I", "text":
        "💻 Hallo 7c! Zum Auftakt unseres EDV-Unterrichts am 19.08. geht's um Computer-Grundbegriffe. "
        "📎 Materialien (Folien, Praktikum, Editor-Anleitung) sind hier hinterlegt - wir holen sie "
        "uns zusammen zu Stundenbeginn. Ich freu mich drauf! 🚀"},
    {"id": 190860, "kuerzel": "7d I", "text":
        "🙌 Liebe 7d, am 19.08. starten wir mit EDV und den ersten Computer-Grundbegriffen. 📎 Ihr "
        "findet hier Folien, ein Praktikum und eine kleine Editor-Anleitung - heruntergeladen wird "
        "alles zusammen in der Stunde. Bis dann! 😊"},
]


def discover_files(day_prefix):
    """Sammelt PDF + alle HTML-Dateien mit der Tagesnummer aus dem Handouts-Ordner (Standard-Paket)."""
    files = []
    for fname in sorted(os.listdir(HANDOUTS)):
        if not fname.startswith(f"{day_prefix}-"):
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext not in (".pdf", ".html"):
            continue
        files.append({
            "path": os.path.join(HANDOUTS, fname),
            "basename": os.path.splitext(fname)[0],  # DOM splittet Name/Erweiterung in 2 <span> - nie mit Endung suchen
            "filename": fname,
        })
    return files


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
    context = browser.new_context(viewport={"width": 1400, "height": 1000})
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


def upload_files(its, course_id, files):
    """Laedt alle Dateien (Standard-Paket) in den Ressourcen-Ordner des Kurses hoch, falls noch nicht da."""
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2000)
    click_first(its, ["text=Ressourcen"])
    its.wait_for_timeout(1500)

    missing = [f for f in files if its.get_by_text(f["basename"]).count() == 0]
    if not missing:
        print(f"  ⏭ Alle {len(files)} Datei(en) liegen in Kurs {course_id} schon vor - Upload uebersprungen")
        return True
    if len(missing) != len(files):
        print(f"  ⚠️ Nur {len(missing)}/{len(files)} fehlen noch - lade nur diese nach")

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

    print(f"  ✅ {len(missing)} Datei(en) hochgeladen und gespeichert (Kurs {course_id})")
    return True


def post_message(its, course_id, text, files):
    """Schreibt Mitteilung mit Text + haengt alle Dateien an + veroeffentlicht."""
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

    for f in files:
        row = its.get_by_text(f["basename"], exact=False)
        if row.count() == 0:
            print(f"  ❌ Datei '{f['basename']}' im Ressource-Dialog nicht gefunden")
            its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_attachpicker.png", full_page=True)
            return False
        # Checkbox links vom Dateinamen anklicken. Playwright haelt sie faelschlich fuer
        # "outside of viewport" (verschachtelter Modal-Scroll-Container) - daher nativer JS-Klick.
        cb = row.first.locator("xpath=preceding::input[@type='checkbox'][1]")
        cb.evaluate("el => el.click()")

    # Der eigentliche Bestaetigungs-Button im Dialog ist ein <input value="Hinzufügen">, nicht das
    # erste "text=Hinzufügen"-Treffer (das waere eine gleichnamige unsichtbare Ueberschrift anderswo im DOM).
    confirm = its.locator("input[value='Hinzufügen']")
    if confirm.count() > 0:
        confirm.first.evaluate("el => el.click()")
    else:
        click_first(its, ["text=Hinzufügen"])
    its.wait_for_timeout(1500)

    published = click_first(its, ["text=Veröffentlichen"])
    its.wait_for_timeout(2000)
    if not published:
        print("  ❌ 'Veröffentlichen'-Button nicht gefunden")
        return False

    print(f"  ✅ Mitteilung veroeffentlicht (Kurs {course_id})")
    return True


if __name__ == "__main__":
    files = discover_files(DAY_PREFIX)
    print(f"Standard-Paket fuer Tag {DAY_PREFIX}: {[f['filename'] for f in files]}")
    if not files:
        raise SystemExit(f"Keine Dateien mit Praefix '{DAY_PREFIX}-' im Handouts-Ordner gefunden.")

    results = []
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            for c in COURSES:
                ok, used_pct = mem_ok()
                if not ok:
                    print(f"\n⚠️ Speicher bei {used_pct:.0f}% (Abbruch-Schwelle {MEM_ABORT_PCT}%) "
                          f"— breche VOR '{c['kuerzel']}' sauber ab, statt weiterzumachen.")
                    results.append((c["kuerzel"], f"ABGEBROCHEN (Speicher {used_pct:.0f}%)"))
                    break
                print(f"\n=== {c['kuerzel']} (CourseID {c['id']}) ===")
                up_ok = upload_files(its, c["id"], files)
                if not up_ok:
                    results.append((c["kuerzel"], "UPLOAD FEHLGESCHLAGEN"))
                    continue
                post_ok = post_message(its, c["id"], c["text"], files)
                results.append((c["kuerzel"], "OK" if post_ok else "MITTEILUNG FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG ===")
    for kuerzel, status in results:
        print(f"{kuerzel}: {status}")
