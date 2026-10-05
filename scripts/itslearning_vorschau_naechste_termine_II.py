#!/usr/bin/env python3
"""Vorschau-Screenshot der 4 'naechste Termine'-Mitteilungen (Gruppe II) nach Desktop\\temp."""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
LIBS = "/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu"
os.environ["LD_LIBRARY_PATH"] = LIBS + ":" + os.environ.get("LD_LIBRARY_PATH", "")
from itslearning_post_naechste_termine_gruppeII_nov import COURSES
from playwright.sync_api import sync_playwright

cards = "".join(
    f'<div class="c"><div class="h">{n.replace("_"," ")} <span>Mitteilung · Do. 08.10.26 nachmittags</span></div>'
    f'<div class="t">{html.escape(t).replace(chr(10), "<br>")}</div></div>' for n, _, t in COURSES)
page = f"""<html><meta charset=utf-8><body style="font-family:Segoe UI,sans-serif;background:#eef1f5;padding:24px;width:1100px">
<style>.g{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}.c{{background:#fff;border-radius:10px;padding:20px;box-shadow:0 1px 4px #0003}}
.h{{font-weight:700;font-size:22px;color:#1a4d8f;margin-bottom:12px}}.h span{{font-weight:400;font-size:14px;color:#777;margin-left:8px}}
.t{{font-size:18px;line-height:1.5}}</style>
<h2>Vorschau: „Eure nächsten Termine“ — Gruppe II, nach den Herbstferien</h2><div class=g>{cards}</div></body></html>"""
open("/tmp/vorschau_II.html", "w").write(page)
out = "/mnt/d/OneDrive/Desktop/temp/Mitteilungen_NaechsteTermine_GruppeII_Vorschau.png"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1150, "height": 600})
    pg.goto("file:///tmp/vorschau_II.html"); pg.screenshot(path=out, full_page=True); b.close()
print(out)
