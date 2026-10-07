import sys, os
sys.path.insert(0, "/home/bolla/workspace/scripts")
import itslearning_send_private_song as sp
from playwright.sync_api import sync_playwright
B = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/"
emp = "Michel, Emma"
msg = "🎂 Alles Gute zum Geburtstag, Emma! Zwei mp4s mit Soundtrack: Download klicken, Lautstärke hoch, Nachbarn vorwarnen ⚽🎶"
songs = [B + "7b/Kurs II/Happy Birthday Emma 05.10.26.mp4", B + "7b/Kurs II/Emma – Guardian of the Line ⚽🛡️🔥.mp4"]
assert all(os.path.isfile(s) for s in songs), "Datei fehlt"
with sync_playwright() as p:
    browser, its = sp.login(p)
    try:
        print("OK" if sp.send_private_message(its, emp, msg, songs) else "FEHLER")
    finally:
        browser.close()
