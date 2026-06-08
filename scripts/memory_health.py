#!/usr/bin/env python3
"""Nächtlicher Memory-Wächter (Chris-Wunsch 2026-06-08).
Misst die Größe aller Memory-Dateien, markiert Bloat und schreibt einen Report.
KOSTET KEINE QUOTA — reines Python, kein LLM. Läuft per Cron nachts.

Das eigentliche Schlankmachen (Urteilsarbeit) macht Bolla in einer Session,
wenn STATUS = ACTION NEEDED. Dieser Wächter sorgt nur dafür, dass Bloat
nie unbemerkt anwächst.
"""

import os, re, datetime, glob

MEMDIR = "/home/bolla/.claude/projects/-home-bolla/memory"
GLOBAL_CLAUDE = "/home/bolla/.claude/CLAUDE.md"
REPORT = os.path.join(MEMDIR, "_memhealth.md")

# Schwellen (Bytes)
T_AKTUELL = 8000      # aktuell.md soll schlank bleiben (rollende Momentaufnahme)
T_MEMINDEX = 16000    # MEMORY.md Index (wird bei Session-Start geladen)
T_SINGLE = 9000       # einzelne Memory (lädt nur bei Recall, aber groß = Recall-Ballast)
T_TOTAL = 260000      # Summe aller .md

def size(p):
    try: return os.path.getsize(p)
    except OSError: return 0

def read(p):
    try:
        with open(p, encoding="utf-8") as f: return f.read()
    except OSError: return ""

flags = []
mds = sorted(glob.glob(os.path.join(MEMDIR, "*.md")))
mds = [m for m in mds if os.path.basename(m) not in ("_memhealth.md",)]

total = sum(size(m) for m in mds)
count = len(mds)

aktuell = os.path.join(MEMDIR, "aktuell.md")
memindex = os.path.join(MEMDIR, "MEMORY.md")

if size(aktuell) > T_AKTUELL:
    flags.append(f"aktuell.md ist {size(aktuell)} B (>{T_AKTUELL}) — wieder aufgebläht, Erledigtes in Tagesnotiz auslagern.")
if size(memindex) > T_MEMINDEX:
    flags.append(f"MEMORY.md Index ist {size(memindex)} B (>{T_MEMINDEX}) — lädt bei jedem Session-Start; veraltete/dublette Zeilen raus.")
if total > T_TOTAL:
    flags.append(f"Summe aller Memory-.md ist {total} B (>{T_TOTAL}) bei {count} Dateien — Konsolidierung prüfen.")

big = [(size(m), os.path.basename(m)) for m in mds
       if size(m) > T_SINGLE and os.path.basename(m) not in ("MEMORY.md",)]
for b, name in sorted(big, reverse=True):
    flags.append(f"Große Memory '{name}' = {b} B — bei Recall Ballast; kürzen/aufteilen prüfen.")

# Verwaiste Dateien: name-slug nicht im MEMORY.md-Index verlinkt
index_txt = read(memindex)
orphans = []
for m in mds:
    base = os.path.basename(m)
    if base in ("MEMORY.md", "aktuell.md"): continue
    nm = re.search(r'^name:\s*(.+)$', read(m), re.M)
    slug = nm.group(1).strip() if nm else base[:-3]
    # im Index entweder als Dateiname oder als [[slug]] / (file.md) referenziert?
    if base not in index_txt and slug not in index_txt and slug.replace(' ', '-') not in index_txt:
        orphans.append(base)
if orphans:
    flags.append(f"{len(orphans)} Memory(s) nicht im MEMORY.md-Index verlinkt (evtl. vergessen/verwaist): "
                 + ", ".join(orphans[:12]) + (" …" if len(orphans) > 12 else ""))

# Mögliche Dubletten über ähnliche description-Anfänge
desc_map = {}
for m in mds:
    dm = re.search(r'^description:\s*(.+)$', read(m), re.M)
    if dm:
        key = re.sub(r'\W+', ' ', dm.group(1).lower()).strip()[:45]
        desc_map.setdefault(key, []).append(os.path.basename(m))
dups = {k: v for k, v in desc_map.items() if len(v) > 1 and k}
for k, v in list(dups.items())[:6]:
    flags.append(f"Ähnliche Beschreibung ({len(v)}x), evtl. Dublette: {', '.join(v)}")

status = "ACTION NEEDED" if flags else "OK"
today = datetime.date.today().isoformat()

top = sorted(((size(m), os.path.basename(m)) for m in mds), reverse=True)[:10]
lines = []
lines.append("---")
lines.append("name: _memhealth")
lines.append("description: Nächtlicher Memory-Größen-Wächter — bei ACTION NEEDED in einer Session aufräumen")
lines.append("metadata:")
lines.append("  node_type: memory")
lines.append("  type: reference")
lines.append("---")
lines.append("")
lines.append(f"# 🩺 Memory-Health — {today}")
lines.append("")
lines.append(f"**STATUS: {status}**  ·  {count} Memory-Dateien  ·  Summe {total} B  ·  Global CLAUDE.md {size(GLOBAL_CLAUDE)} B  ·  MEMORY.md {size(memindex)} B  ·  aktuell.md {size(aktuell)} B")
lines.append("")
if flags:
    lines.append("## ⚠️ Zu tun (von Bolla in einer Session, mit Urteilsvermögen — Git/OneDrive macht alles reversibel)")
    for f in flags:
        lines.append(f"- {f}")
    lines.append("")
else:
    lines.append("Alles im grünen Bereich. Nichts zu tun.")
    lines.append("")
lines.append("## Top 10 größte Memory-Dateien")
for b, name in top:
    lines.append(f"- {b:>6} B  {name}")
lines.append("")
lines.append(f"_Automatisch erzeugt von scripts/memory_health.py (Cron, nachts). Kein LLM/Quota. Letzter Lauf: {today}._")

with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"[{today}] memory_health: STATUS={status}, {count} Dateien, {total} B, {len(flags)} Flag(s)")
