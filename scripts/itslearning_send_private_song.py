#!/usr/bin/env python3
"""Private itslearning-Nachricht mit Geburtstagssong-Anhaengen an einen einzelnen Schueler.
Nachfolger-Muster zu itslearning_post_kurstag.py, aber Ziel = 1 Person statt 1 Kurs
(private Mitteilung ueber das Nachrichten-Icon, nicht Kurs-Ankuendigung).
Siehe [[project_itslearning_automation]] fuer DOM-Fallstricke.

Vor jedem Lauf anpassen: EMPFAENGER (Anzeigename, wie er in der itslearning-Suche auftaucht,
NICHT der Login-Name!), MESSAGE, SONGS (volle Pfade)."""
import json
import os

LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
OUT_DIR = "/tmp/its_debug"
os.makedirs(OUT_DIR, exist_ok=True)

# ⚠️ Vor jedem Lauf anpassen (Test 28.09.2026: Chris' eigener Schueler-Testaccount, s.
# [[project_itslearning_automation]] - "Mandel, Chris" = Schueler-Rolle von cmandel2):
EMPFAENGER = "Mandel, Chris"
MESSAGE = "🎉 Alles Gute zum Geburtstag, Tammo! Hier sind deine beiden Songs zum Behalten 🎶🎂"
SONGS = [
    "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/7a/Schüler/Happy Birthday Tammo 28.09.26.mp4",
    "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/7a/Schüler/Tammo's Birthday Beat 🎉💻🎶.mp4",
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
    context = browser.new_context(viewport={"width": 1500, "height": 1000})
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


def send_private_message(its, empfaenger, message, songs):
    # Nachrichten-Panel oeffnen (Sprechblasen-Icon oben rechts)
    its.mouse.click(1417, 27)
    its.wait_for_timeout(1000)
    click_first(its, ["text=Neue Nachricht"])
    its.wait_for_timeout(1000)

    # Empfaenger suchen + auswaehlen (Suche geht nach ANZEIGENAME, nicht Login-Name)
    box = its.get_by_placeholder("Personen, Kurse oder Projekte suchen")
    box.click()
    box.fill(empfaenger)
    its.wait_for_timeout(1500)
    # ⚠️ Mehrere DOM-Fallen hier: (1) get_by_text(exact=False) trifft auch unsichtbare
    # Obermengen-Treffer (z.B. "Mandel, Christoph" fuer Suche "Mandel, Chris"). (2) Das sichtbare
    # Dropdown-Ergebnis hat einen unsichtbaren Zusatzpunkt im textContent ("Mandel, Chris." statt
    # "Mandel, Chris"), exact=True matcht deshalb NIE. Robuster Weg: alle exact=False-Treffer holen,
    # nur SICHTBARE nehmen, und per startswith() statt == vergleichen.
    cands = its.get_by_text(empfaenger, exact=False)
    n = cands.count()
    clicked = False
    for i in range(n):
        el = cands.nth(i)
        txt = (el.text_content() or "").strip()
        if txt.startswith(empfaenger) and el.is_visible():
            el.click()
            clicked = True
            break
    if not clicked:
        print(f"  ❌ Kein sichtbares Element fuer '{empfaenger}' gefunden ({n} Treffer im DOM)")
        its.screenshot(path=f"{OUT_DIR}/FAIL_empfaenger_unsichtbar.png", full_page=True)
        return False
    its.wait_for_timeout(800)

    # Nachrichtentext
    msgbox = its.get_by_placeholder("Nachricht schreiben")
    msgbox.click()
    msgbox.fill(message)
    its.wait_for_timeout(500)

    # Anhaenge: Buero-Klammer oeffnet ein Mini-Menue (Ihr Computer - Datei / Meine Dateien).
    # "Ihr Computer - Datei" triggert den echten filechooser (Mehrfachauswahl in einem Schritt).
    # ⚠️ NIE Koordinaten-Klicks fuer Anhang/Senden verwenden - die Buttons wandern je nach Anzahl
    # der Anhaenge/Zeilenumbruch nach oben, ein Koordinatenklick trifft dann den "X"-Button eines
    # Anhangs statt "Senden" und loescht ihn wieder (live erlebt am 28.09.2026). Stattdessen ueber
    # die stabilen aria-label-Selektoren gehen - deren Position ist unabhaengig vom Panel-Inhalt.
    its.locator("button[aria-label='Dateien an diese Nachricht anhängen']").click()
    its.wait_for_timeout(600)
    try:
        with its.expect_file_chooser(timeout=4000) as fc_info:
            its.get_by_text("Ihr Computer – Datei", exact=False).first.click()
        fc = fc_info.value
        fc.set_files(songs)
    except Exception as e:
        print("  ❌ Datei-Auswahl fehlgeschlagen:", e)
        its.screenshot(path=f"{OUT_DIR}/FAIL_attach.png", full_page=True)
        return False

    # ⚠️ KRITISCH (live erlebt 28.09.2026): Der Upload der Anhaenge braucht bei mehreren/groesseren
    # Videos laenger als ein paar Sekunden. Ein zu frueher Klick auf "Senden" schickt die Nachricht
    # OHNE die Anhaenge raus (werden dann still fallengelassen, kein Fehler sichtbar!). Erst auf
    # Netzwerkruhe warten (alle Upload-Requests fertig), dann grosszuegigen Sicherheitspuffer.
    its.wait_for_load_state("networkidle", timeout=60000)
    its.wait_for_timeout(4000)
    # Verifizieren: beide Dateien wirklich als Anhang-Chip gelistet, bevor gesendet wird
    for s in songs:
        basename = os.path.splitext(os.path.basename(s))[0]
        if its.get_by_text(basename, exact=False).count() == 0:
            print(f"  ❌ Anhang '{basename}' nicht als Chip sichtbar - breche vor dem Senden ab")
            its.screenshot(path=f"{OUT_DIR}/FAIL_anhang_fehlt.png", full_page=True)
            return False
    its.screenshot(path=f"{OUT_DIR}/vor_senden.png", full_page=True)

    # Senden (stabiler aria-label-Selektor statt Koordinaten)
    its.locator("button[aria-label='Senden']").click()

    # ⚠️ Text + jeder Anhang werden NACHEINANDER als SEPARATE Nachrichten-Blasen verschickt
    # (nicht 1 Nachricht mit N Anhaengen!). Bei mehreren/groesseren Videos dauert das pro Anhang
    # spuerbar - deshalb geduldig auf den Uebergang zur Konversationsansicht pollen (Platzhalter
    # wechselt von "Nachricht schreiben" zu "Nachricht schreiben an <Empfaenger>"), statt einer
    # kurzen Fixwartezeit zu vertrauen (live als False-Negative erlebt am 28.09.2026).
    conv_placeholder = f"Nachricht schreiben an {empfaenger}"
    switched = False
    for _ in range(20):
        its.wait_for_timeout(2000)
        if its.get_by_placeholder(conv_placeholder).count() > 0:
            switched = True
            break
    if not switched:
        print("  ❌ Panel nicht in Konversationsansicht gewechselt - vermutlich NICHT gesendet")
        its.screenshot(path=f"{OUT_DIR}/FAIL_kein_uebergang.png", full_page=True)
        return False

    # Zusaetzlicher Sicherheitspuffer, damit auch der letzte Anhang-Upload wirklich durch ist,
    # bevor der Browser (und damit die Verbindung) geschlossen wird.
    its.wait_for_timeout(4000)
    its.screenshot(path=f"{OUT_DIR}/nach_senden.png", full_page=True)

    print(f"  ✅ Nachricht + {len(songs)} Anhang/Anhaenge an '{empfaenger}' gesendet (Screenshot in {OUT_DIR})")
    return True


if __name__ == "__main__":
    # ⚠️ Chris' Dauerregel (28.09.2026): Geburtstagssongs IMMER erst nachmittags (ab 14:00 Uhr)
    # verschicken - Praesentation ist vormittags, Versand danach. Gilt ab jetzt automatisch,
    # ohne dass er es jedes Mal dazusagen muss.
    import datetime
    jetzt = datetime.datetime.now()
    if jetzt.hour < 14:
        raise SystemExit(
            f"⏰ Es ist erst {jetzt.strftime('%H:%M')} Uhr - Geburtstagssongs werden laut "
            "Chris' Dauerregel erst ab 14:00 Uhr verschickt. Skript bewusst nicht gestartet."
        )

    for s in SONGS:
        if not os.path.isfile(s):
            raise SystemExit(f"Datei nicht gefunden: {s}")

    with sync_playwright() as p:
        browser, its = login(p)
        try:
            ok = send_private_message(its, EMPFAENGER, MESSAGE, SONGS)
        finally:
            browser.close()

    print("FERTIG" if ok else "FEHLGESCHLAGEN - siehe Screenshots")
