#!/usr/bin/env python3
"""
Spam Watcher — Löscht [*** SPAM ***] Mails in beiden Postfächern.
- Outlook (ernstmandel@outlook.de) via Microsoft Graph API
- wtnet (chrismandel@wtnet.de) via IMAP
Wird alle 15 Minuten per Cron ausgeführt.
"""

import imaplib
import json
import logging
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE = Path("/home/bolla/workspace")
MS_TOKEN_FILE = WORKSPACE / "config/ms_token.json"
WTNET_CONFIG = WORKSPACE / "config/wtnet_account.json"
LOG_FILE = WORKSPACE / "logs/spam_watcher.log"
CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"

SPAM_PATTERNS = [
    "[*** SPAM ***]",
    "[**SPAM**]",
    "[SPAM]",
]

SPAM_RULES_FILE = WORKSPACE / "config/spam_rules.json"
OWN_DOMAINS = {"wtnet.de", "outlook.de", "outlook.com", "gmail.com", "googlemail.com",
               "lg-n.de", "hotmail.com", "hotmail.de", "live.de", "live.com"}


def load_rules():
    """Lädt die vom Mail-Prüfen vorgeschlagenen, von Chris bestätigten Regeln."""
    if SPAM_RULES_FILE.exists():
        try:
            return json.loads(SPAM_RULES_FILE.read_text()).get("rules", [])
        except Exception as e:
            logging.getLogger("spam_watcher").error(f"spam_rules.json kaputt: {e}")
    return []


def _cyrillic_ratio(s: str) -> float:
    letters = [c for c in (s or "") if c.isalpha()]
    if not letters:
        return 0.0
    cyr = sum(1 for c in letters if "Ѐ" <= c <= "ӿ")
    return cyr / len(letters)


def rule_match(subject: str, sender_email: str, rules: list):
    """Gibt das Label der ersten passenden Regel zurück, sonst None.
    Eigene Domains werden bei sender_domain hart ignoriert (Absender ist fälschbar)."""
    s = subject or ""
    se = (sender_email or "").lower()
    _m = re.search(r"[\w.+-]+@[\w.-]+", se)   # reine Adresse aus '"Name" <a@b>' ziehen
    if _m:
        se = _m.group(0)
    for r in rules:
        typ, wert = r.get("typ"), (r.get("wert") or "")
        if typ == "cyrillic" and _cyrillic_ratio(s) >= 0.5:
            return r.get("label", "kyrillischer Betreff")
        if typ == "subject_keyword" and wert and wert.lower() in s.lower():
            return r.get("label", wert)
        if typ == "sender_domain" and wert:
            dom = wert.lower().lstrip("@")
            if dom and not any(dom == d or dom.endswith("." + d) for d in OWN_DOMAINS):
                if se.endswith("@" + dom) or se.endswith("." + dom):
                    return r.get("label", dom)
    return None

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE)],
)
log = logging.getLogger("spam_watcher")


# ── Outlook (Microsoft Graph) ────────────────────────────────────────────────

def refresh_ms_token() -> str:
    """Refresht den Microsoft Graph Access Token."""
    with open(MS_TOKEN_FILE) as f:
        token_data = json.load(f)

    data = (
        f"client_id={CLIENT_ID}"
        f"&grant_type=refresh_token"
        f"&refresh_token={token_data['refresh_token']}"
        f"&scope=https://graph.microsoft.com/Mail.Read"
        f"%20https://graph.microsoft.com/Mail.ReadWrite"
        f"%20offline_access"
    ).encode()

    req = urllib.request.Request(
        "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as r:
        new_token = json.loads(r.read())

    with open(MS_TOKEN_FILE, "w") as f:
        json.dump(new_token, f, indent=2)

    return new_token["access_token"]


def graph_get(token: str, url: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        log.error(f"GET {url} → {e.code}: {e.read().decode()[:200]}")
        return {}


def graph_delete(token: str, url: str) -> bool:
    req = urllib.request.Request(url, method="DELETE", headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return True
    except urllib.error.HTTPError as e:
        log.error(f"DELETE → {e.code}: {e.read().decode()[:200]}")
        return False


def is_spam(subject: str) -> bool:
    s = subject.upper()
    return any(p.upper() in s for p in SPAM_PATTERNS) or "*** SPAM" in s or "SPAM ***" in s


def clean_outlook():
    """Löscht Spam in Outlook (alle Ordner)."""
    log.info("[Outlook] Prüfe ernstmandel@outlook.de...")
    token = refresh_ms_token()
    rules = load_rules()

    # Alle Ordner holen
    folders = graph_get(token, "https://graph.microsoft.com/v1.0/me/mailFolders?$top=50")
    skip = {"Deleted Items", "Gesendete Elemente", "Sent Items", "Drafts", "Entwürfe", "Outbox"}
    total = 0

    for folder in folders.get("value", []):
        fname = folder.get("displayName", "")
        if fname in skip:
            continue
        fid = folder["id"]
        url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{fid}/messages?$select=id,subject,from&$top=50"

        while url:
            data = graph_get(token, url)
            for mail in data.get("value", []):
                subject = mail.get("subject") or ""
                sender  = ((mail.get("from") or {}).get("emailAddress") or {}).get("address", "")
                reason  = "Spam-Stempel" if is_spam(subject) else rule_match(subject, sender, rules)
                if reason:
                    if graph_delete(token, f"https://graph.microsoft.com/v1.0/me/messages/{mail['id']}"):
                        log.info(f"  🗑️  [{fname}] ({reason}) {subject[:60]}")
                        total += 1
            url = data.get("@odata.nextLink")

    if total:
        log.info(f"[Outlook] ✅ {total} Spam-Mail(s) gelöscht.")
    else:
        log.info("[Outlook] Kein Spam.")


# ── wtnet (IMAP) ─────────────────────────────────────────────────────────────

def clean_wtnet():
    """Löscht Spam in wtnet Postfach."""
    log.info("[wtnet] Prüfe chrismandel@wtnet.de...")
    with open(WTNET_CONFIG) as f:
        cfg = json.load(f)

    from email.header import decode_header, make_header
    rules = load_rules()
    try:
        m = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
        m.login(cfg["email"], cfg["password"])
        m.select("INBOX")

        status, data = m.search(None, "ALL")
        ids = data[0].split()
        deleted = 0

        for mid in ids:
            t, d = m.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
            if not d or not d[0]:
                continue
            raw = d[0][1].decode("utf-8", "replace")
            subject, sender = "", ""
            for line in raw.splitlines():
                low = line.lower()
                if low.startswith("subject:"):
                    try:
                        subject = str(make_header(decode_header(line[8:].strip())))
                    except Exception:
                        subject = line[8:].strip()
                elif low.startswith("from:"):
                    sender = line[5:].strip()
            reason = "Spam-Stempel" if is_spam(subject) else rule_match(subject, sender, rules)
            if reason:
                m.store(mid, "+FLAGS", "\\Deleted")
                log.info(f"  🗑️  [wtnet] ({reason}) {subject[:60]}")
                deleted += 1

        if deleted:
            m.expunge()
            log.info(f"[wtnet] ✅ {deleted} Spam-Mail(s) gelöscht.")
        else:
            log.info("[wtnet] Kein Spam.")

        m.logout()
    except Exception as e:
        log.error(f"[wtnet] Fehler: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    log.info("─" * 50)
    log.info("Spam Watcher gestartet")

    try:
        clean_outlook()
    except Exception as e:
        log.error(f"[Outlook] Fehler: {e}", exc_info=True)

    try:
        clean_wtnet()
    except Exception as e:
        log.error(f"[wtnet] Fehler: {e}", exc_info=True)

    log.info("Spam Watcher fertig.")


if __name__ == "__main__":
    main()
