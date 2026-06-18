#!/usr/bin/env python3
"""
Telefonnummern in Outlook-Kontakten auf wählbares E.164-Format bringen.
- mobilePhone, homePhones, businessPhones
- Deutsche Nummern: führende 0 -> +49, kaputtes "+49 (040)" -> "+4940..."
DRY-RUN per Default. Mit Argument "apply" werden Änderungen geschrieben.
"""
import json, re, sys, requests
from pathlib import Path

WORKSPACE = Path("/home/bolla/workspace")
MS_TOKEN_FILE = WORKSPACE / "config/ms_token.json"
MS_CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"
APPLY = len(sys.argv) > 1 and sys.argv[1] == "apply"

def get_ms_token():
    data = json.loads(MS_TOKEN_FILE.read_text())
    r = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data={
        "client_id": MS_CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": data["refresh_token"],
        "scope": "https://graph.microsoft.com/Contacts.ReadWrite offline_access"
    })
    token = r.json()
    if "access_token" not in token:
        raise RuntimeError(f"MS Token Fehler: {token}")
    if "refresh_token" in token:
        data.update(token)
        MS_TOKEN_FILE.write_text(json.dumps(data, indent=2))
    return token["access_token"]

def get_contacts(token):
    headers = {"Authorization": f"Bearer {token}"}
    contacts, url = [], ("https://graph.microsoft.com/v1.0/me/contacts?$top=100"
        "&$select=id,displayName,mobilePhone,homePhones,businessPhones")
    while url:
        d = requests.get(url, headers=headers).json()
        contacts.extend(d.get("value", []))
        url = d.get("@odata.nextLink")
    return contacts

def normalize(raw):
    """Gibt (neu, status) zurück. status: 'ok', 'changed', 'review', 'empty'.
    Ziel: wählbares E.164, z.B. +494030852883."""
    if not raw or not raw.strip():
        return raw, "empty"
    orig = raw.strip()
    # Buchstaben drin? (z.B. "Festnetz", "Durchwahl") -> nicht anfassen
    if re.search(r"[A-Za-zÄÖÜäöü]", orig):
        return orig, "review"
    starts_plus = orig.startswith("+")
    digits = re.sub(r"\D", "", orig)            # nur Ziffern

    if starts_plus or digits.startswith("00"):
        cc = digits[2:] if digits.startswith("00") else digits   # ohne 00-Präfix
        # nationale Trunk-0 direkt nach deutscher Ländervorwahl entfernen: 490... -> 49...
        if cc.startswith("490"):
            cc = "49" + cc[3:]
        new = "+" + cc
    elif digits.startswith("0"):
        new = "+49" + digits[1:]                # nationale deutsche Nummer
    elif digits == "":
        return orig, "review"
    elif orig.startswith("("):
        # Vorwahl in Klammern ohne Trunk-0, z.B. "(40) 5479828" -> +49405479828
        new = "+49" + digits
    elif digits.startswith("1") and len(digits) >= 10:
        # Handynummer ohne führende 0 (DE-National beginnt nie mit 1) -> +49 1..
        new = "+49" + digits
    else:
        # ohne Vorwahl / Kurzwahl / Ausland ohne + / mehrere Nummern -> Prüfung
        return orig, "review"

    return new, ("ok" if new == orig else "changed")

def main():
    token = get_ms_token()
    contacts = get_contacts(token)
    # Backup
    bdir = WORKSPACE / "backups"
    (bdir / "contacts-phones-before.json").write_text(json.dumps(contacts, indent=2, ensure_ascii=False))
    changes = []
    review = []
    for c in contacts:
        name = c.get("displayName", "?")
        patch = {}
        # mobilePhone
        m = c.get("mobilePhone")
        if m:
            nv, st = normalize(m)
            if st == "changed":
                patch["mobilePhone"] = nv
                changes.append((name, "mobile", m, nv))
            elif st == "review":
                review.append((name, "mobile", m))
        # homePhones / businessPhones (Listen)
        for fld in ("homePhones", "businessPhones"):
            lst = c.get(fld) or []
            newlst, any_change = [], False
            for p in lst:
                nv, st = normalize(p)
                if st == "changed":
                    changes.append((name, fld, p, nv)); newlst.append(nv); any_change = True
                elif st == "review":
                    review.append((name, fld, p)); newlst.append(p)
                else:
                    newlst.append(nv if st == "ok" else p)
            if any_change:
                patch[fld] = newlst
        if patch and APPLY:
            hdr = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            r = requests.patch(f"https://graph.microsoft.com/v1.0/me/contacts/{c['id']}",
                               headers=hdr, json=patch)
            if r.status_code not in (200, 201):
                print(f"  FEHLER {name}: {r.status_code} {r.text[:120]}")

    out = []
    out.append(f"Kontakte gesamt: {len(contacts)}")
    out.append(f"Nummern zu ändern: {len(changes)}")
    out.append(f"Zur Prüfung (nicht angefasst): {len(review)}")
    out.append("")
    out.append("=== ÄNDERUNGEN ===")
    for n, f, a, b in changes:
        out.append(f"  [{f:12}] {n[:28]:28}  {a:24} -> {b}")
    if review:
        out.append("")
        out.append("=== ZUR PRÜFUNG (Buchstaben/Kurzwahl/unklar) ===")
        for n, f, a in review:
            out.append(f"  [{f:12}] {n[:28]:28}  {a}")
    report = "\n".join(out)
    (WORKSPACE / "logs/phone_normalize_report.txt").write_text(report)
    print(report)
    print("\n>>> " + ("ANGEWENDET" if APPLY else "DRY-RUN (nichts geändert)"))

if __name__ == "__main__":
    main()
