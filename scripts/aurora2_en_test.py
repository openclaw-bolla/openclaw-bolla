#!/usr/bin/env python3
"""AURORA II EN-Vorarbeit: Test-Uebersetzung eines Kapitels mit Haiku (Messung). Nutzung: aurora2_en_test.py <kapitelnr>"""
import json, os, shutil, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import limit_gate
CLAUDE = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
W = "/home/bolla/workspace"
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
def q():
    return json.load(urllib.request.urlopen("http://127.0.0.1:18790/api/claudequota", timeout=10))
d = json.load(open(f"{W}/data/aurora2.json"))
k = d["kapitel"][n - 1]
names = open(f"{W}/scratch/aurora2_en/namensliste_entwurf.md").read()
kultur = open(f"{W}/scratch/aurora2_en/kulturcheckliste.md").read()
p = f"""Translate this chapter of the German thriller novel AURORA II into American English AND localize it (not a literal translation).
Rules: keep literary register and rhythm; short punchy chapter endings; keep all facts, numbers, dates exact. Use these fixed names/places (FIX section) and the cultural checklist; for undecided items use the proposal and mark the chosen word with no comment.
=== NAMES ===
{names}
=== CULTURE ===
{kultur}
Output ONLY the translated chapter text (with the chapter title as first line), no commentary.
=== CHAPTER ===
{k['titel']}

{k['text']}"""
a = q()
r = limit_gate.run([CLAUDE, "-p", "--model", "haiku"], input=p, capture_output=True, text=True, timeout=900)
b = q()
out = f"{W}/scratch/aurora2_en/kap{n:02d}_en_test.txt"
open(out, "w").write(r.stdout)
print("rc", r.returncode, "chars_in", len(k["text"]), "chars_out", len(r.stdout))
print("5h", a["five_hour_pct"], "->", b["five_hour_pct"], "| Woche", a["seven_day_pct"], "->", b["seven_day_pct"])
