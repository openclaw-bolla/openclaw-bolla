#!/usr/bin/env python3
"""Entfernt Gmail-interne Dubletten. Gruppiert nach Mobilnr (sonst Name),
behält pro Gruppe den datenreichsten Eintrag, löscht den Rest.
DRY-RUN default; 'apply' löscht."""
import json, sys, requests
from collections import defaultdict
from pathlib import Path
import importlib.util

W = Path("/home/bolla/workspace")
APPLY = len(sys.argv) > 1 and sys.argv[1] == "apply"
spec=importlib.util.spec_from_file_location('s', str(W/'scripts/outlook_gmail_sync.py'))
s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)

def score(c):
    """je mehr befüllte Felder, desto höher (= behalten)."""
    sc=0
    sc+=len(c.get("phoneNumbers",[]))
    sc+=len(c.get("emailAddresses",[]))*2
    sc+=len(c.get("organizations",[]))
    sc+=len(c.get("biographies",[]))
    sc+=len(c.get("birthdays",[]))
    if s.get_google_photo_url(c): sc+=3
    nm=c.get("names",[{}])[0].get("displayName","") if c.get("names") else ""
    sc+=len(nm)/100.0   # bei Gleichstand: längerer Name (z.B. 'Lenny Ewald')
    return sc

def gkey(c):
    for p in c.get("phoneNumbers",[]):
        mk=s.mobile_key(p.get("value",""))
        if mk: return mk
    nm=c.get("names",[{}])[0].get("displayName","") if c.get("names") else ""
    return "NAME:"+s.name_key(nm) if nm.strip() else None

def main():
    gt=s.get_google_token(); gc=s.get_google_contacts(gt)
    W.joinpath("backups/gmail-contacts-before-dedup.json").write_text(json.dumps(gc,indent=2,ensure_ascii=False))
    groups=defaultdict(list)
    for c in gc:
        k=gkey(c)
        if k: groups[k].append(c)
    h={"Authorization":f"Bearer {gt}"}
    deleted=0; kept=0
    for k,members in groups.items():
        if len(members)<2: continue
        members.sort(key=score, reverse=True)
        keep=members[0]; drop=members[1:]
        knm=keep.get("names",[{}])[0].get("displayName","?")
        print(f"  Gruppe {k[:28]}: behalte '{knm}' (score {score(keep):.2f}), lösche {len(drop)}")
        kept+=1
        for d in drop:
            dnm=d.get("names",[{}])[0].get("displayName","?"); rn=d["resourceName"]
            print(f"      🗑️ {dnm} ({rn})")
            if APPLY:
                r=requests.delete(f"https://people.googleapis.com/v1/{rn}:deleteContact",headers=h)
                if r.status_code not in (200,204): print(f"         FEHLER {r.status_code}: {r.text[:90]}")
                else: deleted+=1
    print(f"\nGruppen bereinigt: {kept} | gelöscht: {deleted if APPLY else '(dry-run)'}")
    print(">>> "+("GELÖSCHT" if APPLY else "DRY-RUN"))

if __name__=="__main__":
    main()
