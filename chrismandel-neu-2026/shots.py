import subprocess, time, sys
from playwright.sync_api import sync_playwright
site = "/home/bolla/workspace/chrismandel-site"
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "-d", site], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
pages = {"aurora": "/aurora/", "geschichte": "/geschichte/", "ki-forum": "/ki-forum/",
         "en-aurora": "/en/aurora/", "en-essay": "/en/essay/", "en-dialogue": "/en/dialogue/"}
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 760})
        for n, u in pages.items():
            pg.goto("http://127.0.0.1:8765" + u); pg.wait_for_timeout(700)
            pg.screenshot(path=f"{site}/assets/shot-{n}.jpg", type="jpeg", quality=82)
            print("ok", n)
        b.close()
finally:
    srv.terminate()
