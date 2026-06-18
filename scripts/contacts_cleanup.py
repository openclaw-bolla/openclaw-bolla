#!/usr/bin/env python3
"""Bereinigung: (1) Nummern -> INTERNATIONAL gegliedert, (2) Anreden aus Namen
(title-Feld bleibt), (3) fileAs = 'Nachname, Vorname'.
DRY-RUN default; 'apply' schreibt."""
import json, re, sys, requests
from pathlib import Path
import phonenumbers as pn

W = Path("/home/bolla/workspace")
MS_TOKEN_FILE = W / "config/ms_token.json"
MS_CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"
APPLY = len(sys.argv) > 1 and sys.argv[1] == "apply"
ANREDE = re.compile(r"^\s*(Frau|Herrn|Herr|Dr\.?|Prof\.?|Dipl\.?-?\w*)\s+", re.I)

def get_ms_token():
    d = json.loads(MS_TOKEN_FILE.read_text())
    t = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data={
        "client_id": MS_CLIENT_ID, "grant_type": "refresh_token",
        "refresh_token": d["refresh_token"],
        "scope": "https://graph.microsoft.com/Contacts.ReadWrite offline_access"}).json()
    if "refresh_token" in t: d.update(t); MS_TOKEN_FILE.write_text(json.dumps(d, indent=2))
    return t["access_token"]

def get_contacts(token):
    h = {"Authorization": f"Bearer {token}"}; out=[]
    url=("https://graph.microsoft.com/v1.0/me/contacts?$top=100&$select="
         "id,displayName,givenName,surname,fileAs,title,companyName,"
         "mobilePhone,homePhones,businessPhones")
    while url:
        r=requests.get(url,headers=h).json(); out.extend(r.get("value",[])); url=r.get("@odata.nextLink")
    return out

def fmt_intl(num):
    if not num: return num
    try:
        x=pn.parse(num, "DE")
        if pn.is_valid_number(x):
            return pn.format_number(x, pn.PhoneNumberFormat.INTERNATIONAL)
    except Exception:
        pass
    return num  # unparsbar -> unverändert lassen

def strip_anrede(s):
    if not s: return s
    prev=None
    while s!=prev:
        prev=s; s=ANREDE.sub("", s).strip()
    return s

def main():
    token=get_ms_token(); cs=get_contacts(token)
    W.joinpath("backups/contacts-full-before-cleanup.json").write_text(json.dumps(cs,indent=2,ensure_ascii=False))
    log=[]; n_num=0; n_name=0; n_file=0; errors=0
    for c in cs:
        patch={}
        # (1) Nummern
        m=c.get("mobilePhone")
        if m:
            nm=fmt_intl(m)
            if nm!=m: patch["mobilePhone"]=nm; n_num+=1
        for fld in ("homePhones","businessPhones"):
            lst=c.get(fld) or []
            new=[fmt_intl(p) for p in lst]
            if new!=lst: patch[fld]=new; n_num+=sum(1 for a,b in zip(lst,new) if a!=b)
        # (2) Anreden aus Namen (title bleibt)
        dn=c.get("displayName") or ""; gn=c.get("givenName") or ""; sn=c.get("surname") or ""
        dn2=strip_anrede(dn); gn2=strip_anrede(gn); sn2=strip_anrede(sn)
        if dn2!=dn: patch["displayName"]=dn2; n_name+=1
        if gn2!=gn: patch["givenName"]=gn2
        if sn2!=sn: patch["surname"]=sn2
        # (3) fileAs = Nachname, Vorname
        comp=c.get("companyName") or ""
        if sn2 and gn2: fa=f"{sn2}, {gn2}"
        elif sn2: fa=sn2
        elif gn2: fa=gn2
        elif dn2: fa=dn2
        elif comp: fa=comp
        else: fa=None
        if fa and fa!=(c.get("fileAs") or ""):
            patch["fileAs"]=fa; n_file+=1
        if patch:
            label=dn2 or dn
            if len(log)<25:
                bits=[]
                if "fileAs" in patch: bits.append(f"fileAs='{patch['fileAs']}'")
                if "displayName" in patch: bits.append(f"name='{dn}'→'{dn2}'")
                nums=[k for k in patch if k in ("mobilePhone","homePhones","businessPhones")]
                if nums: bits.append("Nr gegliedert")
                log.append(f"  {label[:26]:26} {'; '.join(bits)}")
            if APPLY:
                h={"Authorization":f"Bearer {token}","Content-Type":"application/json"}
                r=requests.patch(f"https://graph.microsoft.com/v1.0/me/contacts/{c['id']}",headers=h,json=patch)
                if r.status_code not in (200,201): errors+=1; log.append(f"     FEHLER {r.status_code}: {r.text[:90]}")
    print("\n".join(log))
    print(f"\nNummern gegliedert: {n_num} | Namen entanredet: {n_name} | fileAs gesetzt: {n_file} | Fehler: {errors}")
    print(">>> "+("ANGEWENDET" if APPLY else "DRY-RUN"))

if __name__=="__main__":
    main()
