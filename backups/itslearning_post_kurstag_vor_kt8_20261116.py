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
DAY_PREFIX = "07"

# Kurs-IDs (Schuljahr 26/27, stabil): 7a I=190735 7a II=190738 7b I=190741 7b II=190743
#                                     7c I=190861 7c II=190878 7d I=190860 7d II=190877
# Kurstag 7 "PowerPoint Profi: Einstieg (+ 4 Schritte)" - nur die "I"-Kurse.
# Termine: 7d I + 7b I = Mi 11.11.2026  |  7a I + 7c I = Do 12.11.2026
# Paket (discover_files 07-): 07-1 Powerpoint Profi Einstieg.pdf, 07-1.1 4 Schritte.pdf (beide 1:1-Export von Chris' PPTX),
#                             07-Praktikum.html (Handouts/Praktikum)
# Versand: Di 10.11. 11:00 (nach Chris' Freigabe am Mo 09.11.). Mitteilungen erwaehnen das Grossprojekt NICHT (Chris 07.11.).
COURSES = [
    {"id": 190860, "kuerzel": "7d I", "text":
        '🖥️ Liebe 7d, am Mittwoch, 11.11., steigen wir in PowerPoint richtig ein! 1️⃣ Ich zeige euch, was man mit PowerPoint alles machen kann – viele Beispiele, die ich komplett selbst gebastelt habe, ganz ohne KI. Lasst euch überraschen! 🤩 Dazu gibt\'s die „4 Schritte zu einer sehr guten Präsentation". 2️⃣ Zu Beginn des Praktikums laden wir gemeinsam die Folien „PowerPoint Profi: Einstieg", die „4 Schritte" und 📎 Praktikum 7 herunter. 3️⃣ Im Praktikum legt ihr dann los. Bis Mittwoch! ✨'},
    {"id": 190741, "kuerzel": "7b I", "text":
        '🎨 Hallo liebe 7b! Am Mittwoch, 11.11., lernt ihr PowerPoint von seiner spektakulären Seite kennen. 1️⃣ Ich führe euch jede Menge Beispiele vor, die ich alle selbst erstellt habe – ohne KI, nur mit PowerPoint und etwas Fantasie. Dazu verrate ich euch die „4 Schritte" zu einer richtig guten Präsentation. 2️⃣ Sobald das Praktikum beginnt, holen wir uns gemeinsam die Folien „PowerPoint Profi: Einstieg", die „4 Schritte" und 📎 Praktikum 7. 3️⃣ Danach seid ihr dran! Freu mich auf euch! 😊'},
    {"id": 190735, "kuerzel": "7a I", "text":
        '🚀 Liebe 7a, am Donnerstag, 12.11., beginnt unser PowerPoint-Abenteuer! 1️⃣ Zuerst gibt\'s viel zu sehen: Ich zeige euch Beispiele, die ich ohne KI selbst gemacht habe – damit ihr eine Idee bekommt, was mit PowerPoint alles möglich ist. Außerdem lernt ihr die „4 Schritte zu einer sehr guten Präsentation" kennen. 2️⃣ Zu Beginn des Praktikums laden wir zusammen die Folien „PowerPoint Profi: Einstieg", die „4 Schritte" und 📎 Praktikum 7 herunter. 3️⃣ Im Praktikum geht\'s dann selbst los. Bis Donnerstag! 🎉'},
    {"id": 190861, "kuerzel": "7c I", "text":
        '✨ Hallo 7c! Am Donnerstag, 12.11., schauen wir uns an, was in PowerPoint alles steckt. 1️⃣ Ich habe viele Beispiele vorbereitet – alle selbst gemacht, ohne KI – und zeige euch, welche Möglichkeiten ihr habt. Dazu kommen die „4 Schritte" zu einer sehr guten Präsentation. 2️⃣ Wenn das Praktikum startet, laden wir gemeinsam die Folien „PowerPoint Profi: Einstieg", die „4 Schritte" und 📎 Praktikum 7 herunter. 3️⃣ Dann seid ihr an der Reihe. Auf geht\'s! 🌟'},
]


def discover_files(day_prefix):
    """Sammelt PDF + alle HTML-Dateien mit der Tagesnummer aus dem Handouts-Ordner (Standard-Paket).
    Durchsucht sowohl den Handouts-Ordner direkt (PDFs, PPTX-Reste) als auch den Unterordner
    Praktikum/ (seit 11.08.2026, siehe [[project_schuljahr2627]] - Praktikum-HTMLs liegen dort,
    um den Handouts-Ordner bei wachsender Kurstag-Zahl übersichtlich zu halten)."""
    files = []
    for folder in (HANDOUTS, os.path.join(HANDOUTS, "Praktikum")):
        if not os.path.isdir(folder):
            continue
        for fname in sorted(os.listdir(folder)):
            if not fname.startswith(f"{day_prefix}-"):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext not in (".pdf", ".html"):
                continue
            files.append({
                "path": os.path.join(folder, fname),
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


def files_present(its, course_id, files, tries=12):
    """Prueft (mit Neuladen), ob ALLE Dateien in den Ressourcen des Kurses liegen. Chris 03.11.2026:
    Upload gilt erst als erledigt, wenn die Dateien wirklich dort stehen (Kurstag 6: 7b/7c verloren)."""
    for _ in range(tries):
        its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
        its.wait_for_timeout(2000)
        click_first(its, ["text=Ressourcen"])
        its.wait_for_timeout(2500)
        if all(its.get_by_text(f["basename"]).count() > 0 for f in files):
            return True
        its.wait_for_timeout(4000)
    return False


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

    # "Speichern" ist gesperrt (grau), solange der Upload-Fortschrittsbalken laeuft (Kurstag 6, 03.11.2026:
    # 7b/7c verloren Dateien, weil auf den gesperrten Knopf geklickt wurde). Erst klicken, wenn aktiv.
    saved = None
    for _ in range(90):   # bis ~3 Minuten
        for fr in its.frames:
            try:
                btn = fr.locator("button:has-text('Speichern'), input[value='Speichern']").first
                if btn.count() > 0 and btn.is_enabled():
                    btn.click(timeout=3000)
                    saved = fr
                    break
            except Exception:
                continue
        if saved:
            break
        its.wait_for_timeout(2000)
    its.wait_for_timeout(8000)
    if not saved:
        print("  ❌ 'Speichern'-Button nicht gefunden")
        its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_savebtn.png", full_page=True)
        return False

    if not files_present(its, course_id, files):
        print(f"  ❌ Upload NICHT verifiziert: Dateien fehlen nach Speichern in den Ressourcen (Kurs {course_id})")
        return False
    print(f"  ✅ {len(missing)} Datei(en) hochgeladen, gespeichert und in den Ressourcen verifiziert (Kurs {course_id})")
    return True


def post_message(its, course_id, text, files):
    """Schreibt Mitteilung mit Text + haengt alle Dateien an + veroeffentlicht."""
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(2500)
    snippet = text[12:52]   # eindeutiger Textausschnitt fuer Doppelpost-Schutz + Verifikation
    if its.get_by_text(snippet, exact=False).count() > 0:
        print(f"  ⏭ Mitteilung steht schon im Kurs {course_id} - nicht doppelt gepostet")
        return True

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

    # Der Ressource-Dialog matcht Dateien nur ueber den sichtbaren Namen. Zwei Dateien mit GLEICHEM
    # Basenamen (z.B. 03-Praktikum.html + 03-Praktikum.pdf) sind dort nicht unterscheidbar - ein
    # zweiter Klick auf dieselbe Checkbox wuerde sie wieder abwaehlen. Deshalb pro Basename nur EINMAL
    # anhaengen (die PDF-Variante liegt ohnehin zusaetzlich in den Ressourcen). (Fix 31.08.2026)
    seen_basenames = set()
    for f in files:
        if f["basename"] in seen_basenames:
            print(f"  ⏭ '{f['basename']}' schon angehaengt (gleicher Name, andere Endung) - uebersprungen")
            continue
        seen_basenames.add(f["basename"])

        # In Kursen mit vielen Ressourcen ist die Dialog-Liste lang/virtualisiert - Zieldatei kann
        # ausserhalb des gerenderten Bereichs liegen. Bis zu ~20x im Dialog nach unten scrollen. (Fix 31.08.2026)
        row = its.get_by_text(f["basename"], exact=False)
        scrolls = 0
        while row.count() == 0 and scrolls < 20:
            its.mouse.move(700, 430)
            its.mouse.wheel(0, 500)
            its.wait_for_timeout(400)
            row = its.get_by_text(f["basename"], exact=False)
            scrolls += 1
        if row.count() == 0:
            print(f"  ❌ Datei '{f['basename']}' im Ressource-Dialog nicht gefunden (auch nach {scrolls}x Scrollen)")
            its.screenshot(path=f"{OUT_DIR}/FAIL_{course_id}_attachpicker.png", full_page=True)
            return False
        try:
            row.first.scroll_into_view_if_needed(timeout=2000)
        except Exception:
            pass
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

    # Verifikation: Mitteilung muss danach wirklich im Kurs stehen (Text + angehaengte Datei)
    its.wait_for_timeout(3000)
    its.goto(f"https://moin.itslearning.com/main.aspx?CourseID={course_id}", timeout=20000)
    its.wait_for_timeout(3000)
    if its.get_by_text(snippet, exact=False).count() == 0:
        print(f"  ❌ Mitteilung NICHT verifiziert (Text nicht im Kurs {course_id} zu sehen)")
        return False
    print(f"  ✅ Mitteilung veroeffentlicht und verifiziert (Kurs {course_id})")
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
                for attempt in (2, 3):   # Ressource-Dialog war manchmal nach dem Upload noch nicht aktuell -> bis zu 3 Versuche mit Neuladen
                    if post_ok:
                        break
                    print(f"  🔁 Wiederhole Mitteilung (Versuch {attempt}/3) ...")
                    its.wait_for_timeout(10000)
                    files_present(its, c["id"], files, tries=3)   # Ressourcenliste frisch laden
                    post_ok = post_message(its, c["id"], c["text"], files)
                results.append((c["kuerzel"], "OK" if post_ok else "MITTEILUNG FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG ===")
    for kuerzel, status in results:
        print(f"{kuerzel}: {status}")
