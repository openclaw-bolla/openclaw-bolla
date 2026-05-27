#!/usr/bin/env python3
"""Wöchentliches Update der Claude Code Seite in Mission Control.
Aktualisiert: Memory-Box (aus MEMORY.md), CLAUDE.md-Highlights, Zeitstempel.
Cron: jeden Sonntag 10:00 Uhr
"""

import re
import os
from datetime import datetime

INDEX_HTML = "/home/bolla/workspace/mission-control/index.html"
MEMORY_MD  = "/home/bolla/.claude/projects/-mnt-c-WINDOWS-system32/memory/MEMORY.md"
CLAUDE_MD  = "/home/bolla/.claude/CLAUDE.md"

ICON_MAP = {
    "user_":      ("👤", "#a78bfa"),
    "feedback_":  ("💬", "#f59e0b"),
    "project_":   ("📋", "#06b6d4"),
    "reference_": ("📌", "#22c55e"),
}

def parse_memory_entries(md_text):
    """Listet alle Memory-Einträge aus MEMORY.md als (title, file, description) zurück."""
    entries = []
    for line in md_text.splitlines():
        m = re.match(r"^- \[(.+?)\]\((.+?)\)\s*[—–-]+\s*(.+)$", line.strip())
        if m:
            entries.append((m.group(1), m.group(2), m.group(3)))
    return entries

def entry_html(title, filename, description):
    prefix = next((k for k in ICON_MAP if filename.startswith(k)), None)
    icon, color = ICON_MAP.get(prefix, ("📄", "#818cf8"))
    desc_safe = description.replace("<", "&lt;").replace(">", "&gt;")
    title_safe = title.replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<div style="padding:7px 10px;background:rgba(129,140,248,0.06);border-radius:6px;'
        f'border-left:2px solid {color}">'
        f'<div style="font-size:12px;font-weight:600;color:var(--bright)">{icon} {title_safe}</div>'
        f'<div style="font-size:11px;color:var(--dim);margin-top:2px">{desc_safe}</div>'
        f"</div>"
    )

def parse_claude_md_rules(md_text):
    """Extrahiert Wichtige Regeln und Kommunikationsstil aus CLAUDE.md."""
    items = []

    # Kommunikationsstil — erste 2 Zeilen zusammenfassen
    m2 = re.search(r"## Kommunikationsstil\n(.*?)(?=\n## |\Z)", md_text, re.DOTALL)
    if m2:
        lines = [re.sub(r"\*+", "", l.lstrip("- ").strip()) for l in m2.group(1).splitlines() if l.strip().startswith("-")]
        if lines:
            items.append(("Sprache & Stil", " · ".join(lines[:2])))

    # Wichtige Regeln — jede Zeile parsen, flexibles Format
    m = re.search(r"## Wichtige Regeln\n(.*?)(?=\n## |\Z)", md_text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            line = line.lstrip("- ").strip()
            if not line:
                continue
            # Format: **Key:** Value oder **Key** (Value): Rest
            match = re.match(r"\*\*(.+?)\*\*[:\s]*(.*)", line)
            if match:
                key = match.group(1).strip()
                val = re.sub(r"\*+", "", match.group(2)).strip()
                # Klammern vom Key entfernen falls vorhanden
                key = re.sub(r"\s*\(.*?\)", "", key).strip()
                items.append((key, val[:80] + ("…" if len(val) > 80 else "")))

    return items[:6]  # max 6 Einträge

def rule_html(key, val):
    key_safe = key.replace("<", "&lt;").replace(">", "&gt;")
    val_safe = val.replace("<", "&lt;").replace(">", "&gt;")
    # Icon-Mapping
    icons = {"Sprache": "🗣", "E-Mail": "📧", "Tokens": "🔑", "Passwort": "🔑",
             "Backup": "💾", "Vor": "💾", "Session": "🌙", "Erst": "🧠", "Gedächtnis": "🧠"}
    icon = next((v for k, v in icons.items() if key.startswith(k)), "⚙️")
    return (
        f'<div style="display:flex;gap:8px;align-items:flex-start">'
        f'<span style="color:var(--accent);font-size:14px">{icon}</span>'
        f'<div><span style="color:var(--bright);font-weight:600">{key_safe}</span>'
        f'<br><span style="color:var(--dim)">{val_safe}</span></div></div>'
    )

def replace_between(html, start_marker, end_marker, new_content):
    if start_marker not in html:
        print(f"  WARNUNG: Marker nicht gefunden: {start_marker}")
        return html
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL
    )
    replacement = start_marker + "\n              " + new_content + "\n              " + end_marker
    return pattern.sub(lambda m: replacement, html)

def main():
    print(f"MC Weekly Update — {datetime.now().strftime('%d.%m.%Y %H:%M')}")

    with open(INDEX_HTML, encoding="utf-8") as f:
        html = f.read()

    # 1. Memory-Box
    if os.path.exists(MEMORY_MD):
        with open(MEMORY_MD, encoding="utf-8") as f:
            memory_text = f.read()
        entries = parse_memory_entries(memory_text)
        print(f"  Memory: {len(entries)} Einträge gefunden")
        cards = "\n              ".join(entry_html(t, fn, d) for t, fn, d in entries)
        memory_html = f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;font-size:13px">\n                {cards}\n              </div>'
        html = replace_between(html, "<!-- BOLLA-MEMORY-START -->", "<!-- BOLLA-MEMORY-END -->", memory_html)
    else:
        print("  WARNUNG: MEMORY.md nicht gefunden")

    # 2. CLAUDE.md Highlights
    if os.path.exists(CLAUDE_MD):
        with open(CLAUDE_MD, encoding="utf-8") as f:
            claude_text = f.read()
        rules = parse_claude_md_rules(claude_text)
        print(f"  CLAUDE.md: {len(rules)} Regeln extrahiert")
        rules_html = '<div style="display:flex;flex-direction:column;gap:7px;font-size:13px">\n                '
        rules_html += "\n                ".join(rule_html(k, v) for k, v in rules)
        rules_html += "\n              </div>"
        html = replace_between(html, "<!-- BOLLA-CLAUDEMD-START -->", "<!-- BOLLA-CLAUDEMD-END -->", rules_html)
    else:
        print("  WARNUNG: CLAUDE.md nicht gefunden")

    # 3. Zeitstempel
    ts = datetime.now().strftime("%d.%m.%Y")
    html = replace_between(
        html,
        "<!-- BOLLA-UPDATED-START -->",
        "<!-- BOLLA-UPDATED-END -->",
        f'<span style="font-size:11px;color:var(--dim)">Aktualisiert: {ts}</span>'
    )
    print(f"  Zeitstempel: {ts}")

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("  index.html aktualisiert ✓")

if __name__ == "__main__":
    main()
