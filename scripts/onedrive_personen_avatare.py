#!/usr/bin/env python3
"""Holt alle Gesichts-Avatare (256px) der OneDrive-Personen-Seite headless -> Ordner (Argument 1, Standard /tmp/claude-1000/av).
Dateiname: <Gruppenname>#<laufende Nr>.jpg. Nur lesen, nichts in OneDrive ändern.
Voraussetzung: Profil config/browser_profile_onedrive_personen_edge eingeloggt (onedrive_personen_start_edge.py, Chris loggt sich 1x ein; Fenster vorher schließen!)."""
import os, sys, base64
os.environ["LD_LIBRARY_PATH"] = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu:" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright
out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-1000/av"; os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context("/home/bolla/workspace/config/browser_profile_onedrive_personen_edge", headless=True, viewport={"width": 1400, "height": 950})
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto("https://onedrive.live.com/photos?photosData=%2Fphotos%2Fpeople"); pg.wait_for_timeout(8000)
    res = pg.evaluate("""async () => {const out={}; for (const c of document.querySelectorAll('button[aria-label]')) {const im=c.querySelector('img'); if(!im||!im.src) continue;
      try{const r=await fetch(im.src); const u=new Uint8Array(await r.arrayBuffer()); let s=''; for(let k=0;k<u.length;k+=8192) s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));
      out[c.getAttribute('aria-label')+'#'+Object.keys(out).length]=btoa(s);}catch(e){}} return out;}""")
    for k, v in res.items(): open(f"{out}/{k.replace('/','_')}.jpg", "wb").write(base64.b64decode(v))
    print(len(res), "Avatare ->", out); ctx.close()
