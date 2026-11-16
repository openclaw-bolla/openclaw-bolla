import os, sys, json
os.environ["LD_LIBRARY_PATH"]="/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
B="https://onedrive.live.com/personal/52539b07421473cf/_api/v2.1/drives/52539b07421473cf"
with sync_playwright() as p:
    ctx=p.chromium.launch_persistent_context("/home/bolla/workspace/config/browser_profile_onedrive_personen_edge",headless=True,viewport={"width":1400,"height":1000})
    pg=ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto("https://onedrive.live.com/photos?photosData=%2Fphotos%2Fpeople"); pg.wait_for_timeout(6000)
    r=pg.evaluate("async(u)=>{const a=await fetch(u,{credentials:'include'});return await a.text()}",B+"/recognizedEntities?top=500")
    open("ents.json","w").write(r)
    ctx.close()
