#!/usr/bin/env python3
"""
Caption-Wächter (Cron, jede Minute).

Chris tippt am Handy in mmp ins Clipboard eine Zeile, die mit "caption:" (oder
"cap:") beginnt, z.B.:
    caption: Sommerfest 50 Jahre Lessing, Serenade im Innenhof, tolle Stimmung
Optional Plattform-Hinweis im Text ("insta"/"tiktok") und Ton ("kurz"/"lustig").

Der Wächter erkennt neue solche Einträge, erzeugt mit headless `claude -p`
(Sonnet, günstig, kein €) eine fertige Social-Media-Caption in Chris' Stil
(optimistisch, locker, Emojis + Hashtags) und legt sie zurück ins Clipboard
(source="bolla-caption"). Chris aktualisiert mmp und kopiert sie.

Kein Telegram, kein Server-Neustart nötig — nutzt nur die Clipboard-API.
Idempotent über State-Datei (verarbeitete Einträge gemerkt).
"""
import os, sys, json, re, subprocess, hashlib, datetime, urllib.request, fcntl

HOME = "/home/bolla"
os.environ.setdefault("HOME", HOME)
CLAUDE = f"{HOME}/.local/bin/claude"
MODEL = "claude-sonnet-5"
WS = f"{HOME}/workspace"
API = "http://127.0.0.1:18790"
STATE = f"{WS}/config/caption_watcher_state.json"
LOCK = f"{WS}/config/.caption_watcher.lock"
LOG = f"{WS}/data/caption_watcher.log"

TRIGGER = re.compile(r"^\s*(caption|cap)\s*:\s*(.+)", re.IGNORECASE | re.DOTALL)


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        open(LOG, "a", encoding="utf-8").write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def api_get(path):
    return json.load(urllib.request.urlopen(f"{API}{path}", timeout=10))


def api_post(path, payload):
    req = urllib.request.Request(f"{API}{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=15))


def load_state():
    try:
        return set(json.load(open(STATE)))
    except Exception:
        return set()


def save_state(s):
    json.dump(sorted(s), open(STATE, "w"))


def make_caption(context):
    plat = "Instagram/TikTok"
    low = context.lower()
    if "tiktok" in low and "insta" not in low:
        plat = "TikTok"
    elif "insta" in low and "tiktok" not in low:
        plat = "Instagram"
    prompt = (
        f"Schreibe EINE fertige Social-Media-Caption für {plat} auf Deutsch. "
        "Stil: optimistisch, locker, warmherzig-humorvoll, mit passenden Emojis und "
        "3–6 sinnvollen Hashtags am Ende. 2–4 Sätze, natürlich, keine KI-Floskeln. "
        "Gib AUSSCHLIESSLICH die Caption aus, ohne Vorrede, ohne Anführungszeichen.\n\n"
        f"Worum es geht: {context.strip()}"
    )
    r = subprocess.run([CLAUDE, "-p", "--model", MODEL, prompt],
                       capture_output=True, text=True, timeout=180, env=os.environ)
    out = (r.stdout or "").strip()
    if not out or "unavailable" in out.lower():
        log(f"claude lieferte nichts (rc={r.returncode}): {(r.stderr or '')[:150]}")
        return None
    return out


def main():
    lf = open(LOCK, "w")
    try:
        fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return
    try:
        data = api_get("/api/clipboard")
    except Exception as e:
        log(f"Clipboard nicht lesbar: {e}")
        return
    seen = load_state()
    changed = False
    for e in data.get("entries", []):
        txt = e.get("text", "")
        if e.get("source") == "bolla-caption":
            continue
        m = TRIGGER.match(txt)
        if not m:
            continue
        h = hashlib.md5((txt + str(e.get("ts", ""))).encode("utf-8")).hexdigest()[:12]
        if h in seen:
            continue
        context = m.group(2)
        log(f"Neue Caption-Anfrage: {context[:80]}")
        cap = make_caption(context)
        seen.add(h); changed = True
        if cap:
            try:
                api_post("/api/clipboard", {"text": "📣 " + cap, "append": True, "source": "bolla-caption"})
                log(f"Caption erzeugt + ins Clipboard ({len(cap)} Zeichen).")
            except Exception as ex:
                log(f"Konnte Caption nicht posten: {ex}")
        else:
            try:
                api_post("/api/clipboard", {"text": "⚠️ Caption-Erzeugung hat grad nicht geklappt — nochmal versuchen.",
                                            "append": True, "source": "bolla-caption"})
            except Exception:
                pass
    if changed:
        save_state(seen)


if __name__ == "__main__":
    main()
