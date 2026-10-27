#!/usr/bin/env python3
"""
UserPromptSubmit-Hook: injiziert kritische Regeln + Kernfakten in jeden Prompt
und warnt EINMAL pro Session, wenn der Kontext wirklich voll wird.

WICHTIG (Lehre 18.06.2026): Die Warnung darf sich NICHT auf einen blinden,
sessionübergreifenden Zähler stützen. Der alte Hook zählte in /tmp/bolla_msg_count
über ALLE Sessions hinweg hoch (nie zurückgesetzt) und meldete dann z.B.
"435 Nachrichten" in einer 10-Minuten-Session -> 5× Fehlalarm.

Jetzt: echte Kontextgröße (Tokens) aus dem Transkript DIESER Session
(via stdin 'transcript_path'). Neue Session/`/clear` -> neue session_id ->
neues Transkript -> Zähler de facto bei 0. Kein globaler State mehr.
"""
import json, os, sys
from collections import deque

MEM = "/home/bolla/.claude/projects/-home-bolla/memory"
WARN_AT_TOKENS = 400_000          # ab hier lohnt /clear. 150k war viel zu früh (1M-Kontext = 15%). 400k = selten genug, aber Puffer vor WSL-RAM-Crash. 1× pro Session.
MARK = "/tmp/bolla_ctxwarn_"      # pro-Session-Markierung, damit nur 1× gewarnt wird
NUDGES = "/home/bolla/workspace/data/board_nudges.json"

# 5h-Reserve-Wächter (Chris 03.09.2026): NUR wenn das 5-Stunden-Fenster fast
# leer ist — Restbudget < 10 %, also five_hour_pct > 90. Grund: Chris will in der
# Schule am Book nicht plötzlich ohne Bolla dastehen. Seltenes Ereignis → darf
# ruhig in jedem Prompt stehen, aber Re-Warnung erst bei je +3 Punkten (90/93/96/99),
# damit es bei bewusstem Weiterarbeiten nicht komplett zutextet.
FIVEH_MARK = "/tmp/bolla_5hlow_"
FIVEH_WARN_ABOVE = 90.0

def five_hour_reserve_warning(sid):
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:18790/api/claudequota", timeout=2) as r:
            q = json.loads(r.read().decode())
    except Exception:
        return ""
    pct = float(q.get("five_hour_pct") or 0)   # % verbraucht
    if pct <= FIVEH_WARN_ABOVE:
        return ""
    rest = max(0.0, 100.0 - pct)
    mark = FIVEH_MARK + str(sid).replace("/", "_")
    last = 0.0
    try:
        last = float(open(mark).read().strip())
    except Exception:
        pass
    if last and pct < last + 3:
        return ""
    try:
        open(mark, "w").write(str(pct))
    except Exception:
        pass
    reset = q.get("five_hour_reset_label") or "?"
    rh, rm = q.get("five_hour_reset_hours"), q.get("five_hour_reset_minutes")
    wann = f"{reset}" + (f" (in ~{rh}h {rm}min)" if rh is not None else "")
    return (
        f"\n\n=== 🚨 5h-RESERVE FAST WEG ===\n"
        f"Das 5-Stunden-Nutzungsfenster ist zu ~{pct:.0f} % voll — nur noch ~{rest:.0f} % übrig. "
        f"Reset: {wann}. Chris SOFORT warnen (er will am Book in der Schule nicht ohne Bolla "
        f"dastehen): jetzt nur noch Nötigstes, größere Aktionen bis zum Reset zurückstellen.\n"
    )

def read(p):
    try:
        return open(p).read()
    except Exception:
        return ""

# stdin: Claude Code liefert session_id + transcript_path
data = {}
try:
    data = json.loads(sys.stdin.read() or "{}")
except Exception:
    pass

context = ("=== KRITISCHE REGELN ===\n" + read(f"{MEM}/rules_kritisch.md")
           + "\n=== KERNFAKTEN ===\n" + read(f"{MEM}/facts_kern.md"))

def ctx_tokens(transcript):
    """Echte aktuelle Kontextgröße aus der letzten assistant-usage im Transkript."""
    if not transcript or not os.path.exists(transcript):
        return None
    try:
        with open(transcript) as fh:
            last = deque(fh, maxlen=60)   # nur die letzten Zeilen, auch bei 16-MB-Files schnell
        for line in reversed(last):
            line = line.strip()
            if not line:
                continue
            try:
                u = (json.loads(line).get("message") or {}).get("usage")
            except Exception:
                continue
            if u:
                return (u.get("input_tokens", 0)
                        + u.get("cache_read_input_tokens", 0)
                        + u.get("cache_creation_input_tokens", 0))
    except Exception:
        return None
    return None

def pop_nudges():
    """Liest offene MP-Board-Anstupser, leert die Queue, liefert deduplizierte Prompts."""
    try:
        with open(NUDGES) as fh:
            raw = json.load(fh).get("nudges", [])
    except Exception:
        return []
    if not raw:
        return []
    try:
        with open(NUDGES, "w") as fh:
            json.dump({"nudges": []}, fh, ensure_ascii=False, indent=2)
    except Exception:
        pass
    seen, out = set(), []
    for n in raw:
        key = (n.get("projId"), n.get("prompt"))
        if key in seen:
            continue
        seen.add(key)
        out.append(n)
    return out

nudges = pop_nudges()
if nudges:
    context += "\n\n=== 📌 NEUE ANSTUPS-QUEUE (live) ===\n"
    for n in nudges:
        context += f"\n• {n.get('title','')} ({n.get('ts','')})\n{n.get('prompt','')}\n"

sid = data.get("session_id") or "nosession"
context += five_hour_reserve_warning(sid)

tok = ctx_tokens(data.get("transcript_path", ""))
mark = MARK + str(sid).replace("/", "_")

if tok and tok >= WARN_AT_TOKENS and not os.path.exists(mark):
    try:
        open(mark, "w").write(str(tok))
    except Exception:
        pass
    context += (
        f"\n\n=== KONTEXT-HINWEIS ===\n"
        f"Der Kontext dieser Session ist bei ~{tok//1000}k Tokens — langsam ein guter "
        f"Zeitpunkt für /clear, bevor Auto-Compacting greift. Einmal kurz & locker erwähnen, "
        f"NICHT wiederholen. (Stand ist in aktuell.md gesichert.)\n"
    )

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": context,
    }
}))
