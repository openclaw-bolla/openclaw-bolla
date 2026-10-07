import sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
import itslearning_send_private_song as sp
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser, its = sp.login(p)
    try:
        its.mouse.click(1417, 27)
        its.wait_for_timeout(1000)
        sp.click_first(its, ["text=Neue Nachricht"])
        its.wait_for_timeout(1000)
        box = its.get_by_placeholder("Personen, Kurse oder Projekte suchen")
        for q in ["Zock", "Zock, Henny", "Zock, Henny Jasmin", "Wassermann", "Wassermann, Eva"]:
            box.click()
            box.fill("")
            box.fill(q)
            its.wait_for_timeout(2500)
            its.screenshot(path=f'/tmp/its_debug/probe_{q.replace(" ","_").replace(",","")}.png', clip={'x':1100,'y':60,'width':400,'height':400})
    finally:
        browser.close()
