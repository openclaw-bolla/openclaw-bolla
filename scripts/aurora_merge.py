#!/usr/bin/env python3
"""Zieht alle gecachten Lektorat-Kapitel in ki_buch.json nach — idempotent."""
import json, os, glob

buch_path = os.path.expanduser('~/workspace/data/ki_buch.json')
cache_dir  = os.path.expanduser('~/workspace/data/aurora_lektorat')

with open(buch_path) as f:
    buch = json.load(f)
kapitel = buch['kapitel']

merged = 0
for cf in sorted(glob.glob(os.path.join(cache_dir, 'kap_*.json'))):
    with open(cf) as f:
        cd = json.load(f)
    idx  = cd.get('kapitel_idx')
    text = cd.get('text_verbessert', '').strip()
    if idx is None or not text or idx >= len(kapitel) or len(text) < 100:
        continue
    if kapitel[idx].get('text', '')[:80] != text[:80]:
        kapitel[idx]['text'] = text
        merged += 1

if merged:
    tmp = buch_path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(buch, f, ensure_ascii=False, indent=2)
    os.replace(tmp, buch_path)
    print(f'Merge: {merged} Kapitel aktualisiert')
else:
    print('Alles aktuell — kein Merge nötig')
