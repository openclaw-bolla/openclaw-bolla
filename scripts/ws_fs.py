#!/usr/bin/env python3
"""Schreibt den Workshop-Fortschritt für die MC-Anzeige.
   Nutzung:  ws_fs.py <pct> "<label>"   → aktiv, Balken auf pct%
             ws_fs.py done               → Anzeige ausblenden
"""
import json, sys, datetime
F = "/home/bolla/workspace/projektwoche-ki-workshop/fortschritt.json"
if len(sys.argv) >= 2 and sys.argv[1] == "done":
    data = {"active": False, "pct": 100, "label": "", "ts": datetime.datetime.now().isoformat(timespec="seconds")}
else:
    pct = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    label = sys.argv[2] if len(sys.argv) > 2 else ""
    data = {"active": True, "pct": pct, "label": label,
            "ts": datetime.datetime.now().isoformat(timespec="seconds")}
json.dump(data, open(F, "w"), ensure_ascii=False)
print(f"fortschritt: {data['pct']}% · {data['label']}")
