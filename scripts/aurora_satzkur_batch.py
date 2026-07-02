#!/usr/bin/env python3
"""
AURORA Satz-Kur — Fable-Batch-Runner.

Schickt Kapitel-Batches an Claude Fable 5 (CLI headless) und lässt Fable:
  1. SATZ-KUR: die echten Stolper-Schachtelsätze aufbrechen (Stufe 1 —
     Extremsätze + Kapitelschluss-Monster), Stimme & Sinn erhalten.
  2. KONSISTENZ: Namen (Personen/Orte) + Zahlen/Daten gegen die Referenzliste
     prüfen und Ungereimtheiten melden.
Fable ändert die ki_buch.json NICHT — es liefert strukturiertes JSON
(alter Satz WORTWÖRTLICH → neuer Satz + Konsistenz-Funde). Das Einspielen
macht später ein deterministisches Skript mit Backup + Verifikation.

Budget-Disziplin: vor JEDEM Batch Ampel prüfen. Stopp, wenn die Wochen-Reserve
unter RESERVE_MIN fiele (Chris: 25% Reserve fürs Tagesgeschäft).

Aufruf:
  python3 aurora_satzkur_batch.py --only 0        # nur Batch 0
  python3 aurora_satzkur_batch.py --from 1 --to 7 # Batches 1..7 nacheinander
  python3 aurora_satzkur_batch.py --check         # nur Ampel zeigen
"""
import json, os, re, sys, subprocess, datetime, urllib.request, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aurora_satzkur_parse import parse_batch

HOME = "/home/bolla"
os.environ.setdefault("HOME", HOME)
CLAUDE = f"{HOME}/.local/bin/claude"
MODEL = "claude-fable-5"
WS = f"{HOME}/workspace"
BOOK = f"{WS}/data/ki_buch.json"
OUTDIR = f"{WS}/data/satzkur"
WORKLIST = f"{OUTDIR}/satzkur_worklist.json"
LOG = f"{OUTDIR}/batch_log.txt"
QUOTA_URL = "http://127.0.0.1:18790/api/claudequota"

BATCH_SIZE = 6
RESERVE_MIN = 25   # % Wochen-Reserve, die frei bleiben MUSS (Chris' Vorgabe)
FIVEH_MAX = 90     # % 5h-Fenster Obergrenze (Chris 02.07.: hochgesetzt, nichts weiter vor heute)

# Referenz für den Konsistenz-Check
CANON_TXT = """KANONISCHE FAKTEN (Referenz — Abweichungen bitte melden):
- Marlie Braun, 34, KI-Ethikerin (Nacht-Monitoring)
- Noah Khoury, 40, Chefarchitekt von AURORA   [NICHT "Weber" o.ä.!]
- Leni Yilmaz, 27, Quantenphysikerin
- Theo Dreyer, 52, Ex-BND, Sicherheitschef NovaTech
- Maria Santos, 45, CEO von NovaTech
- Aurora Santos = Marias verstorbene Tochter (geheimer, kleingeschriebener Name der KI)
- Günter Brandt, 74, Rentner/Nachbar; Hannelore 'Hanni' Brandt, 71 (32 Jahre verheiratet)
- Zeit-Anker: AURORA "seit elf Tagen wach"; Marias Geheimnis "zweiundzwanzig Jahre";
  Prolog-Datum "Donnerstag, 3. März 2035, 02:47 Uhr".
- Firmen/Orte: NovaTech; Hamburger Forschungstrakt; Hamburg."""


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def quota():
    try:
        return json.load(urllib.request.urlopen(QUOTA_URL, timeout=10))
    except Exception as e:
        log(f"Quota nicht lesbar: {e}")
        return None


def quota_ok():
    q = quota()
    if not q:
        return False, "Quota nicht lesbar"
    fh = q.get("five_hour_pct", 100)
    rem = q.get("seven_day_rem", 0)
    if fh > FIVEH_MAX:
        return False, f"5h-Fenster {fh}% (> {FIVEH_MAX})"
    if rem < RESERVE_MIN:
        return False, f"Wochen-Reserve nur {rem}% (< {RESERVE_MIN} — Chris' Deckel)"
    return True, f"5h {fh}%, Woche {rem}% frei"


def build_prompt(chapters):
    parts = [
        "Du bist Fable 5 und lektorierst den deutschen KI-Thriller AURORA. "
        "Deine Aufgabe hat ZWEI Teile für die folgenden Kapitel.\n",
        CANON_TXT,
        "\n\nTEIL 1 — SATZ-KUR (Lesbarkeit an den Höhepunkten):\n"
        "Manche Sätze sind so lang/verschachtelt, dass Leser zurückspringen müssen. "
        "Brich NUR solche Sätze auf, wo das Lesen wirklich stolpert — besonders die "
        "Extremsätze und die überlangen KAPITELSCHLUSS-Sätze. Lang ist NICHT automatisch "
        "schlecht: einen wohlklingenden langen Satz lässt du stehen. Erhalte Stimme, Rhythmus, "
        "Bedeutung und Fakten 1:1 — du darfst einen Satz in 2–3 aufteilen, umstellen, straffen, "
        "aber NICHTS an der Handlung ändern. Qualität vor Menge: lieber 3 exzellente Umbauten "
        "als 10 mittelmäßige.\n"
        "Gib den zu ersetzenden Originalsatz WORTWÖRTLICH zurück (exakt wie im Kapiteltext unten, "
        "inkl. etwaiger *Sternchen*/**Fett** und Anführungszeichen), damit er 1:1 gefunden werden kann.\n\n"
        "TEIL 2 — KONSISTENZ:\n"
        "Prüfe Namen (Personen/Orte) und Zahlen/Daten gegen die kanonischen Fakten oben und "
        "gegen den übrigen Kapiteltext. Melde jede Ungereimtheit (falscher Nachname, "
        "widersprüchliche Zahl/Alter/Zeitspanne/Datum, Ort verwechselt) mit Kapitelnummer und Zitat.\n\n"
        "AUSGABE — NUR valides JSON, exakt dieses Schema, keine Erklärtexte drumherum:\n"
        '{\n'
        '  "kapitel": [\n'
        '    {"nr": <int>, "rewrites": [\n'
        '        {"original": "<wortwörtlicher Originalsatz>", "revised": "<neuer Text>", "grund": "<kurz>"}\n'
        '    ]}\n'
        '  ],\n'
        '  "konsistenz": [\n'
        '    {"nr": <int>, "typ": "name|zahl|datum|ort", "fund": "<Zitat/Stelle>", "problem": "<was stimmt nicht>", "vorschlag": "<Korrektur>"}\n'
        '  ]\n'
        '}\n'
        "Wenn ein Kapitel keine Umbauten braucht: leeres rewrites-Array. Keine Konsistenzprobleme: leeres Array.\n\n"
        "=== KAPITEL ===\n"
    ]
    for c in chapters:
        flagged = "\n".join(
            f"  - [{s['words']} W{', SCHLUSSSATZ' if s['is_last'] else ''}] {s['sentence'][:220]}"
            for s in c["long_sentences"]
        ) or "  (keine auffällig langen Sätze)"
        parts.append(
            f"\n----- KAPITEL {c['kapitel']}: {c['titel']} -----\n"
            f"Auffällig lange Sätze (>=35 Wörter) als Anhaltspunkt:\n{flagged}\n\n"
            f"VOLLTEXT des Kapitels (Original, wortwörtlich):\n{c['_text']}\n"
        )
    return "".join(parts)


def load_batches():
    worklist = json.load(open(WORKLIST, encoding="utf-8"))
    book = json.load(open(BOOK, encoding="utf-8"))["kapitel"]
    for w in worklist:
        w["_text"] = book[w["pos"]].get("text") or ""
    batches = [worklist[i:i + BATCH_SIZE] for i in range(0, len(worklist), BATCH_SIZE)]
    return batches


def run_batch(idx, chapters):
    nums = [c["kapitel"] for c in chapters]
    log(f"Batch {idx}: Kapitel {nums} — Prompt bauen…")
    prompt = build_prompt(chapters)
    log(f"Batch {idx}: Prompt {len(prompt)} Zeichen (~{len(prompt)//4} Tokens) → Fable-Aufruf…")
    t0 = datetime.datetime.now()
    r = subprocess.run(
        [CLAUDE, "-p", "--model", MODEL, "--dangerously-skip-permissions", prompt],
        capture_output=True, text=True, timeout=2400, env=os.environ)
    dur = (datetime.datetime.now() - t0).total_seconds()
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if not out or "unavailable" in out.lower():
        log(f"Batch {idx}: KEIN Ergebnis (rc={r.returncode}, {dur:.0f}s). stderr: {err[:200]}")
        return False
    # rohes Ergebnis sichern
    raw_path = f"{OUTDIR}/batch_{idx:02d}_raw.txt"
    open(raw_path, "w", encoding="utf-8").write(out)
    # Toleranter Parse (robust gegen gerade Anführungszeichen in Dialogen)
    res_path = f"{OUTDIR}/batch_{idx:02d}.json"
    try:
        parsed = parse_batch(out)
        json.dump(parsed, open(res_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        nrw = sum(len(k.get("rewrites", [])) for k in parsed.get("kapitel", []))
        nks = len(parsed.get("konsistenz", []))
        log(f"Batch {idx}: OK ({dur:.0f}s) → {nrw} Satz-Umbauten, {nks} Konsistenz-Funde. {res_path}")
        if nrw == 0 and nks == 0:
            log(f"Batch {idx}: ⚠️ 0/0 — evtl. Format abweichend, Rohdatei prüfen: {raw_path}")
    except Exception as e:
        log(f"Batch {idx}: Antwort da ({dur:.0f}s), aber Parse scheiterte ({e}). Roh: {raw_path}")
    return True


def extract_json(text):
    # 1) ```json fences
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    cand = m.group(1) if m else None
    # 2) erstes { bis letztes }
    if cand is None:
        i, j = text.find("{"), text.rfind("}")
        if i != -1 and j != -1 and j > i:
            cand = text[i:j + 1]
    if cand is None:
        return None, "kein JSON-Block gefunden"
    try:
        return json.loads(cand), "ok"
    except Exception as e:
        return None, str(e)[:120]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int)
    ap.add_argument("--from", dest="frm", type=int, default=0)
    ap.add_argument("--to", type=int)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    if a.check:
        ok, msg = quota_ok()
        log(f"Ampel: {'🟢 OK' if ok else '🔴 STOPP'} — {msg}")
        return

    batches = load_batches()
    total = len(batches)
    log(f"Insgesamt {total} Batches (à {BATCH_SIZE} Kapitel).")

    if a.only is not None:
        rng = [a.only]
    else:
        end = a.to if a.to is not None else total - 1
        rng = list(range(a.frm, end + 1))

    for idx in rng:
        if idx < 0 or idx >= total:
            log(f"Batch {idx} existiert nicht (0..{total-1}) — übersprungen.")
            continue
        if os.path.exists(f"{OUTDIR}/batch_{idx:02d}.json"):
            log(f"Batch {idx} schon fertig (JSON vorhanden) — übersprungen (idempotent).")
            continue
        ok, msg = quota_ok()
        if not ok:
            log(f"🔴 STOPP vor Batch {idx}: {msg}. Reserve schützen — Rest später.")
            break
        log(f"🟢 Ampel vor Batch {idx}: {msg}")
        if not run_batch(idx, batches[idx]):
            log(f"Batch {idx} fehlgeschlagen — Abbruch der Kette (nächster Versuch später).")
            break
    log("Lauf beendet.")


if __name__ == "__main__":
    main()
