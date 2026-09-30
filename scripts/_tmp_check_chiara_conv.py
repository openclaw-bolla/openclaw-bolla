"""Nur ansehen, ob mit Chiara schon eine Konversation/Nachricht existiert - sendet nichts."""
import os, json
LIBS_DIR = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
if os.path.isdir(LIBS_DIR):
    os.environ["LD_LIBRARY_PATH"] = LIBS_DIR + ":" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright

CREDS_PATH = "/home/bolla/workspace/config/itslearning_credentials.json"
with open(CREDS_PATH) as f:
    creds = json.load(f)

def click_first(page, selectors, timeout=5000):
    for sel in selectors:
        try:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.click(timeout=timeout)
                return sel
        except Exception:
            pass
    return None

with sync_playwright() as p:
    browser = p.chromium.launch()
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
    its.mouse.click(1417, 27)
    its.wait_for_timeout(1000)
    its.screenshot(path="/home/bolla/workspace/scratch/chiara_check_inbox.png", full_page=True)
    cands = its.get_by_text("Rittmüller, Chiara", exact=False)
    n = cands.count()
    print("Treffer im Nachrichten-Panel fuer 'Rittmueller, Chiara':", n)
    for i in range(n):
        el = cands.nth(i)
        print(" -", repr(el.text_content()), "visible:", el.is_visible())
    browser.close()
