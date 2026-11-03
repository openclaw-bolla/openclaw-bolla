#!/usr/bin/env python3
"""Wöchentlicher Check: ist Fable im Pro-Plan enthalten? (kein Token-Verbrauch, nur Support-Artikel lesen)
Quelle: support.claude.com "Claude Fable models on your plan". Meldet per Telegram NUR bei Änderung."""
import json, re, html, urllib.request, datetime
from pathlib import Path
W = Path("/home/bolla/workspace")
URL = "https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan"
STATE = W / "state/fable_pro_check.json"
cfg = json.loads((W / "config/telegram_bot.json").read_text())

def tg(msg):
    import requests
    requests.post(f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage",
                  json={"chat_id": cfg["chris_id"], "text": msg}, timeout=10)

def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    s = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))

def main():
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    prev = json.loads(STATE.read_text()) if STATE.exists() else {}
    try:
        t = fetch()
    except Exception as e:
        STATE.write_text(json.dumps({**prev, "last_run": now, "last_error": str(e)}, ensure_ascii=False))
        print(now, "Fehler:", e); return
    excluded = bool(re.search(r"Pro plans[^:]{0,80}: Fable 5.{0,40}?(aren.t|are not) included", t))
    status = "pro_excluded" if excluded else "CHANGED"
    if status == "CHANGED" and prev.get("status") != "CHANGED":
        tg("🐾 Fable-Hint: Der Anthropic-Support-Artikel zu Fable im Pro-Plan klingt anders als bisher "
           "(\"aren't included in your plan's usage limits\" nicht mehr gefunden). "
           f"Bitte prüfen, ob Fable jetzt im Pro-Plan enthalten ist: {URL}")
    STATE.write_text(json.dumps({"status": status, "last_run": now}, ensure_ascii=False))
    print(now, status)

main()
