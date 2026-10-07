#!/usr/bin/env python3
"""Wochenend-Ausreizung (Chris-Vereinbarung 07.10.2026): Fr 19:00 starten, bis Sa 23:50 das Kontingent sinnvoll nutzen.

Block A  Tiefere Makler-Prüfung (data/makler_status.json, Sonnet + WebSearch/WebFetch, Haiku nur für Mini-Checks nicht nötig)
Block B  AURORA II: Entwürfe Kap. 25-27 NUR in scratch (aurora2.json bleibt unberührt, weil Chris Kap. 10-24 selbst liest/bearbeitet)
Block C  Alternative Schluss-Varianten für Kap. 27 (Auswahl für Chris)
Gating/Quota/Stopp wie samstag_ausreizen.py (importiert, nicht kopiert): 5h <= 92 %, Woche < 98,5 %, Notbremse /tmp/aurora_samstag_stop.
Nur Opus/Sonnet/Haiku — NIE Fable. KEINE Mails, NICHTS löschen. Resume-fähig über state.json.

Aufruf: ausreizen_orchestrator.py [--dry-run]   (Dry-Run: keine claude-Aufrufe, keine Telegram, keine Schreibzugriffe auf data/ und Desktop)
"""
import argparse
import datetime as dt
import fcntl
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ARGS = ap.parse_args()
DRY = ARGS.dry_run

W = "/home/bolla/workspace"
sys.path.insert(0, f"{W}/scripts")

# ---- Basismodul (Gating, claude-Aufruf, Status) wiederverwenden; eigener Ausgabeordner/State
_today = dt.date.today()
TAG = os.environ.get("AUSREIZEN_TAG") or ("dry" if DRY else _today.strftime("%Y%m%d"))
os.environ["SAMSTAG_TAG"] = "wochenende_" + TAG
import samstag_ausreizen as s  # noqa: E402  (Importieren startet main() NICHT)

# Deadline: nächster Samstag 23:50 (am Freitag also morgen), per Env überschreibbar
_days = (5 - _today.weekday()) % 7
s.DEADLINE = dt.datetime.combine(_today + dt.timedelta(days=_days), dt.time(23, 50))
if os.environ.get("AUSREIZEN_DEADLINE"):
    s.DEADLINE = dt.datetime.fromisoformat(os.environ["AUSREIZEN_DEADLINE"])

OUT = s.OUT
LOGF = f"{W}/logs/ausreizen_orchestrator.log"
MAKLER = f"{W}/data/makler_status.json"
DESKTOP_WIN = r"D:\OneDrive\Desktop"
DESKTOP = "/mnt/d/OneDrive/Desktop"
log = s.log
Stop = s.Stop

CRITERIA = ("Käufer: Chris & Renate Mandel (Anfang 70/60, Rentner), Suche frühestens Herbst 2027, kein Zeitdruck. "
            "Gesucht: Eigentumswohnung ca. 100 qm, 3,5-4 Zimmer, Penthouse/Dachgeschoss mit Südterrasse, max. 3-stöckig, "
            "Neubau oder günstig + Renovierung, Tiefgarage mit Ladestation, Ort mit Gesundheitszentrum/Fitness+Sauna. "
            "Regionen: Ammersee (Herrsching, Dießen), Starnberg/Starnberger See, Landsberg, Weilheim, Fürstenfeldbruck, "
            "Gilching, westliche Peripherie (Germering, Puchheim) — nicht München Stadt.")


def telegram(msg):
    if DRY:
        log("[dry] Telegram: " + msg[:120])
        return
    try:
        import requests
        c = json.load(open(f"{W}/config/telegram_bot.json"))
        requests.post(f"https://api.telegram.org/bot{c['bot_token']}/sendMessage",
                      json={"chat_id": c["chris_id"], "text": msg[:3900]}, timeout=15)
    except Exception as e:
        log(f"Telegram fehlgeschlagen: {e}")


def run_claude(prompt, tag, model, web=False, timeout=1800):
    """Wie s.claude, aber mit Modellwahl + optionalen Web-Tools. Gating vor jedem Versuch."""
    if model not in ("opus", "sonnet", "haiku"):
        raise Stop(f"Modell {model} nicht erlaubt")
    if DRY:
        log(f"[dry] claude {model} web={web} {tag} ({len(prompt)} Zeichen Prompt)")
        return "{}"
    cmd = [s.CL, "-p", "--output-format", "json", "--model", model]
    if web:
        cmd += ["--allowedTools", "WebSearch", "WebFetch"]
    for attempt in range(4):
        s.gate()
        t0 = time.time()
        try:
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, cwd=s.HOME)
        except subprocess.TimeoutExpired:
            log(f"Timeout {tag} (Versuch {attempt + 1})")
            continue
        try:
            j = json.loads(r.stdout)
        except Exception:
            j = None
        text = (j or {}).get("result", "") or ""
        if r.returncode != 0 or (j or {}).get("is_error") or not text.strip():
            msg = (text or r.stderr or r.stdout)[:300].replace("\n", " ")
            log(f"Fehler {tag}: {msg}")
            if re.search(r"limit|usage|quota|rate|overload|reset", msg, re.I):
                s.sleep_chunks(300)
            else:
                s.sleep_chunks(60 * (attempt + 1))
            continue
        s.stat_add("claude_calls")
        s.stat_add(f"calls_{model}")
        log(f"ok {tag} [{model}]: {int(time.time() - t0)} s, {len(text)} Zeichen")
        return text
    log(f"AUFGEGEBEN {tag}")
    return None


def run_json(prompt, tag, model, **kw):
    t = run_claude(prompt, tag, model, **kw)
    j = s.jparse(t)
    if j is None and t is not None and not DRY:
        t = run_claude(prompt + "\n\nWICHTIG: Antworte AUSSCHLIESSLICH mit einem gültigen JSON-Objekt, ohne Text davor/danach, ohne Codeblock.",
                       tag + "-retry", model, **kw)
        j = s.jparse(t)
    return j


def backup(path, name):
    os.makedirs(f"{W}/backups", exist_ok=True)
    dst = f"{W}/backups/{name}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}{os.path.splitext(path)[1]}"
    shutil.copy2(path, dst)
    return dst


# =============================================================== Block A: Makler
BATCH = 5


def makler_liste():
    d = json.load(open(MAKLER, encoding="utf-8"))
    out = []
    for r in d["regionen"]:
        for m in r["makler"]:
            out.append({**m, "region": r["name"]})
    return d, out


def makler_batches():
    _, alle = makler_liste()
    # unklare/lückenhafte Fälle zuerst
    prio_ids = ["simone-grau", "schnellboegl-franke", "bayerische-seen", "krusemeyer", "stadler", "spk-starnberg-gilching",
                "lbs-germering", "sedlmayr", "spk-landsberg"]
    alle.sort(key=lambda m: (0 if m["id"] in prio_ids else 1))
    return [alle[i:i + BATCH] for i in range(0, len(alle), BATCH)]


def makler_prompt(batch):
    items = json.dumps([{k: m.get(k, "") for k in ("id", "firma", "ansprechpartner", "region", "email", "telefon", "mobil", "hinweis")}
                        for m in batch], ensure_ascii=False, indent=1)
    return f"""Du bist Bolla und prüfst Immobilienmakler für Chris Mandel. Nutze WebSearch und WebFetch (Firmenwebsite, Impressum, Kontaktseite, Google/Branchenbuch) und prüfe JEDEN der folgenden Makler gründlich.

KONTEXT: {CRITERIA}

MAKLER:
{items}

PRÜFE je Makler:
1. Existiert die Firma noch und ist sie unter dieser Bezeichnung aktiv (Website erreichbar, aktuelle Inserate, kein Geschäftsaufgabe/Umbenennung/Übernahme)?
2. Website-URL, Adresse, Telefon, KONTAKT-E-MAIL (nur wenn du sie wirklich auf Website/Impressum/Verzeichnis gelesen hast).
3. Ist das Einsatzgebiet passend zur Region? Verkauft die Firma Eigentumswohnungen (Neubau/Bestand/Penthouse) oder nur Häuser/Gewerbe/Vermietung?
4. Bewertung der Eignung für Chris' Suche 1-5 (5 = sehr passend) mit knapper Begründung.

STRENGE REGELN: Erfinde NICHTS. E-Mail-Adressen niemals raten oder aus Mustern ableiten — nur belegt, sonst leer lassen. Wenn Quellen widersprüchlich sind: "unklar". Gib für Funde die Quell-URL an. Keine Kontaktaufnahme, keine Formulare ausfüllen.

Antworte AUSSCHLIESSLICH mit JSON:
{{"ergebnisse":[{{"id":"...","existiert":"ja|nein|unklar","website":"","email":"","email_quelle":"","telefon":"","adresse":"","region_passt":true,"schwerpunkt":"kurz","eignung":3,"notiz":"1-2 Sätze Befund","aenderung_an_alten_daten":"was in den bisherigen Daten falsch/veraltet ist, sonst leer","entfernen_vorschlag":false,"entfernen_grund":""}}]}}"""


def block_a_check():
    for i, batch in enumerate(makler_batches()):
        key = f"A:batch{i}"
        if s.is_done(key):
            continue
        ids = [m["id"] for m in batch]
        j = run_json(makler_prompt(batch), f"Makler-Check {i} {','.join(ids)}", "sonnet", web=True, timeout=2400)
        if j is None:
            log(f"Makler-Batch {i} ohne Ergebnis")
            s.ST["stats"]["makler_batches_fehlgeschlagen"] = s.ST["stats"].get("makler_batches_fehlgeschlagen", 0) + 1
            s.mark(key)  # nicht endlos wiederholen; Report nennt die Lücke
            continue
        json.dump(j, open(f"{OUT}/makler_batch_{i}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        s.stat_add("makler_geprueft", len(j.get("ergebnisse", [])))
        s.mark(key)


REGIONEN_SUCHE = [
    "Ammersee (Herrsching, Dießen, Utting, Schondorf, Inning, Andechs, Seefeld)",
    "Starnberger See (Starnberg, Tutzing, Feldafing, Berg, Pöcking, Gauting, Weßling, Wörthsee)",
    "Landsberg am Lech, Weilheim, Penzberg",
    "Fürstenfeldbruck, Germering, Puchheim, Gröbenzell, Olching, Gilching",
]


def block_a_neue():
    _, alle = makler_liste()
    bekannt = ", ".join(sorted({m["firma"] for m in alle}))
    for i, reg in enumerate(REGIONEN_SUCHE):
        key = f"A:neue{i}"
        if s.is_done(key):
            continue
        prompt = f"""Du bist Bolla. Suche mit WebSearch/WebFetch weitere GUTE Immobilienmakler (Schwerpunkt Eigentumswohnungen, bevorzugt Neubau/Bauträger-Vertrieb/Penthouse) für die Region: {reg}.

KONTEXT: {CRITERIA}

BEREITS IN DER LISTE (nicht erneut nennen): {bekannt}

Nenne maximal 4 neue Kandidaten, nur wenn: Firma aktiv (aktuelle Inserate/Website), Eigentumswohnungen im Portfolio, verifizierte Kontaktdaten. Achte auch auf Bauträger/Projektentwickler mit Neubau-Penthouses (zählen als Kandidat, Typ angeben).
STRENG: nichts erfinden, E-Mail nur wenn belegt (sonst leer), Quell-URL angeben. Lieber 0 Kandidaten als schlechte.

Antworte AUSSCHLIESSLICH mit JSON:
{{"kandidaten":[{{"firma":"","typ":"Makler|Bauträger|Bank-Immobilien","ansprechpartner":"","email":"","telefon":"","website":"","adresse":"","ort":"","schwerpunkt":"","eignung":4,"begruendung":"","quelle":""}}]}}"""
        j = run_json(prompt, f"Neue Makler {i}", "sonnet", web=True, timeout=2400)
        if j:
            json.dump(j, open(f"{OUT}/makler_neue_{i}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            s.stat_add("makler_kandidaten", len(j.get("kandidaten", [])))
        s.mark(key)


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")).strip("-")[:40]


def block_a_merge():
    """Ergebnisse in makler_status.json einarbeiten: nur ergänzen, nie löschen. Liefert Bericht-Daten."""
    if s.is_done("A:merge"):
        return
    datum = dt.date.today().strftime("%d.%m.%Y")
    ergebnisse = {}
    for fn in sorted(os.listdir(OUT)):
        if fn.startswith("makler_batch_"):
            for e in json.load(open(f"{OUT}/{fn}", encoding="utf-8")).get("ergebnisse", []):
                ergebnisse[e.get("id")] = e
    kandidaten = []
    for fn in sorted(os.listdir(OUT)):
        if fn.startswith("makler_neue_"):
            kandidaten += json.load(open(f"{OUT}/{fn}", encoding="utf-8")).get("kandidaten", [])
    if not DRY:
        bk = backup(MAKLER, "makler_status_vor_tiefenpruefung")
        log(f"Backup {bk}")
    d = json.load(open(MAKLER, encoding="utf-8"))  # frisch lesen (MP könnte Status geändert haben)
    gefuellt, vorschlaege, neu_n = [], [], 0
    bekannt = {m["firma"].lower() for r in d["regionen"] for m in r["makler"]}
    for r in d["regionen"]:
        for m in r["makler"]:
            e = ergebnisse.get(m["id"])
            if not e:
                continue
            ch = []
            for feld, quelle in (("email", "email"), ("telefon", "telefon")):
                neu = (e.get(quelle) or "").strip()
                if neu and not (m.get(feld) or "").strip() and (feld != "email" or e.get("email_quelle")):
                    m[feld] = neu
                    ch.append(feld)
            for feld in ("website", "adresse"):
                neu = (e.get(feld) or "").strip()
                if neu and not (m.get(feld) or "").strip():
                    m[feld] = neu
                    ch.append(feld)
            note = f"Tiefencheck {datum}: existiert={e.get('existiert')}, Eignung {e.get('eignung')}/5 — {e.get('notiz', '')}".strip()
            if e.get("aenderung_an_alten_daten"):
                note += f" | Alte Daten: {e['aenderung_an_alten_daten']}"
            m["hinweis"] = (m.get("hinweis", "") + " | " if m.get("hinweis") else "") + note
            m["geprueft"] = datum
            m["eignung"] = e.get("eignung")
            if ch:
                gefuellt.append((m["firma"], ch))
            if e.get("entfernen_vorschlag") or e.get("existiert") == "nein":
                vorschlaege.append((m["firma"], e.get("entfernen_grund") or e.get("notiz", "")))
    # neue Kandidaten: nur gut belegte (Eignung >= 4, Kontakt vorhanden), einer eigenen Region zuordnen
    neu_region = "Weitere Kandidaten (Tiefencheck " + datum + ")"
    reg = next((r for r in d["regionen"] if r["name"] == neu_region), None)
    for k in kandidaten:
        firma = (k.get("firma") or "").strip()
        if not firma or firma.lower() in bekannt or (k.get("eignung") or 0) < 4 or not (k.get("email") or k.get("telefon")):
            continue
        if reg is None:
            reg = {"name": neu_region, "makler": []}
            d["regionen"].append(reg)
        reg["makler"].append({"id": slug(firma), "firma": firma, "ansprechpartner": k.get("ansprechpartner", ""),
                              "email": k.get("email", ""), "telefon": k.get("telefon", ""), "mobil": "",
                              "website": k.get("website", ""), "adresse": k.get("adresse", ""),
                              "hinweis": f"Neu (Tiefencheck {datum}, {k.get('typ', '')}, {k.get('ort', '')}): {k.get('begruendung', '')} — Quelle: {k.get('quelle', '')}",
                              "geprueft": datum, "eignung": k.get("eignung")})
        bekannt.add(firma.lower())
        neu_n += 1
    d["geprueft"] = datum
    if DRY:
        json.dump(d, open(f"{OUT}/makler_status_PREVIEW.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    else:
        tmp = MAKLER + ".tmp_ausreizen"
        json.dump(d, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        os.replace(tmp, MAKLER)
    s.ST["stats"]["makler_neu_eingetragen"] = neu_n
    json.dump({"gefuellt": gefuellt, "vorschlaege": vorschlaege, "neu": neu_n, "ergebnisse": ergebnisse},
              open(f"{OUT}/makler_merge_info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    s.mark("A:merge")


def block_a_report():
    if s.is_done("A:report"):
        return
    info = json.load(open(f"{OUT}/makler_merge_info.json", encoding="utf-8")) if os.path.exists(f"{OUT}/makler_merge_info.json") else {}
    erg = info.get("ergebnisse", {})
    datum = dt.date.today().strftime("%d.%m.%Y")
    _, alle = makler_liste()
    namen = {m["id"]: m["firma"] for m in alle}
    zeilen = []
    for mid, e in sorted(erg.items(), key=lambda kv: -(kv[1].get("eignung") or 0)):
        zeilen.append(f"<tr><td>{html.escape(namen.get(mid, mid))}</td><td>{html.escape(str(e.get('existiert')))}</td>"
                      f"<td>{e.get('eignung')}</td><td>{html.escape(e.get('email') or '')}</td>"
                      f"<td>{html.escape(e.get('website') or '')}</td><td>{html.escape(e.get('notiz') or '')}</td></tr>")
    vor = "".join(f"<li><b>{html.escape(f)}</b>: {html.escape(g)}</li>" for f, g in info.get("vorschlaege", [])) or "<li>keine</li>"
    fill = "".join(f"<li>{html.escape(f)}: {', '.join(c)}</li>" for f, c in info.get("gefuellt", [])) or "<li>keine</li>"
    doc = f"""<!doctype html><html lang="de"><meta charset="utf-8"><title>Makler-Prüfung {datum}</title>
<style>body{{font:16px/1.5 Segoe UI,Arial;margin:24px;max-width:1200px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:6px 8px;vertical-align:top;font-size:15px}}th{{background:#eee}}</style>
<h1>🏡 Makler-Tiefenprüfung {datum}</h1>
<p>{len(erg)} Makler geprüft · {info.get('neu', 0)} neue Makler eingetragen · Stand in MP: Zeitstempel oben auf der Immobilien-Seite. Nichts gelöscht, keine Mails gesendet.</p>
<h2>Entfernungs-Vorschläge (nichts entfernt — du entscheidest)</h2><ul>{vor}</ul>
<h2>Neu ergänzte Kontaktdaten</h2><ul>{fill}</ul>
<h2>Alle Befunde (nach Eignung)</h2>
<table><tr><th>Makler</th><th>Existiert</th><th>Eignung</th><th>E-Mail</th><th>Website</th><th>Befund</th></tr>{''.join(zeilen)}</table>
<p>Neue Kandidaten stehen in MP unter „Weitere Kandidaten (Tiefencheck {datum})“. Rohdaten: {OUT}</p></html>"""
    p = f"{OUT}/Makler_Pruefung_{TAG}.html"
    open(p, "w", encoding="utf-8").write(doc)
    if not DRY:
        try:
            dst = rf"{DESKTOP_WIN}\Makler_Pruefung_{TAG}.html"
            src = subprocess.run(["wslpath", "-w", p], capture_output=True, text=True).stdout.strip()
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Copy-Item -LiteralPath '{src}' -Destination '{dst}' -Force"],
                           capture_output=True, text=True, timeout=60)
        except Exception as e:
            log(f"Desktop-Kopie fehlgeschlagen: {e}")
    telegram(f"🏡 Makler-Prüfung fertig: {len(erg)} geprüft, {info.get('neu', 0)} neu, "
             f"{len(info.get('vorschlaege', []))} Entfernungs-Vorschläge. Bericht: Desktop\\Makler_Pruefung_{TAG}.html")
    s.mark("A:report")


def block_a():
    block_a_check()
    block_a_neue()
    block_a_merge()
    block_a_report()


# =============================================================== Block B/C: AURORA-Entwürfe (nur scratch!)
def aurora_ctx(d, n):
    """Kontext für Kap. n aus aurora2.json (read-only) + ggf. bereits fertige Entwürfe."""
    plan = (d["geheim"].get("bogenplan_19_27") or {})
    pk = next((x for x in plan.get("kapitel", []) if x.get("nr") == n), {})
    teile = []
    for k in d["kapitel"][-4:]:
        teile.append(f"=== {k['titel']} (VOLLTEXT) ===\n{k['text']}")
    for m in range(25, n):
        p = f"{OUT}/entwurf_kap{m}.md"
        if os.path.exists(p):
            teile.append(f"=== ENTWURF Kapitel {m} (noch nicht im Buch) ===\n{open(p, encoding='utf-8').read()}")
    return plan, pk, "\n\n".join(teile)


def prep_bible():
    src = f"{W}/scratch/aurora_samstag_20261003/bible.json"
    dst = f"{OUT}/bible.json"
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)


def draft_chapter(n):
    key = f"B:{n}"
    if s.is_done(key):
        return
    d = s.load()
    plan, pk, ctx = aurora_ctx(d, n)
    if not pk:
        log(f"Kein Bogenplan für Kap. {n} — übersprungen")
        s.mark(key)
        return
    k10 = s.kap_by_nr(d, 10)
    prompt = f"""Du bist Bolla und schreibst mit Chris Mandel die Fortsetzung des deutschen KI-Thrillers AURORA. Schreibe jetzt einen ENTWURF für KAPITEL {n} von AURORA II. Wichtig: Chris liest und überarbeitet die Kapitel davor noch selbst; dieser Entwurf liegt nur als Vorschlag in einer Datei und wird erst nach seinem OK eingebaut.

BUCHKRITERIEN: {json.dumps(d['kriterien'], ensure_ascii=False)}
FIGUREN: {s.figuren_ctx(d)}
STEUERUNG & ROTE LINIEN: {json.dumps(d.get('steuerung'), ensure_ascii=False)}
KANON (Fest-Fakten, nicht widersprechen): {json.dumps(d.get('kanon'), ensure_ascii=False)}
GEHEIME MASTER-WENDUNG (nur für dich; nichts davon vorwegnehmen außer wie im Plan): {d['geheim'].get('wendung', '')}
BEREITS GESÄTE HINWEISE: {json.dumps(d['geheim'].get('hinweise_gesaet'), ensure_ascii=False)}

PRIVATER BOGENPLAN FÜR DIESES KAPITEL (verbindlich, Feinheiten darfst du dramaturgisch verbessern):
{json.dumps(pk, ensure_ascii=False, indent=1)}
GESAMTBOGEN 19-27: {plan.get('gesamtbogen', '')}

ZUSAMMENFASSUNGEN ALLER KAPITEL IM BUCH:
{s.summaries(d)}

FAKTEN-BIBEL: {s.bible_txt()}

STIL-HYGIENE: {s.stil_hygiene()}

HUMOR-TONPROBE (Kapitel 10, Anfang): {k10['text'][:4200] if k10 else ''}

{ctx}

AUFGABE: Kapitel {n}, 5.500-7.500 Wörter, Titel exakt „Kapitel {n}: <Titel>". Erste Textzeile = Kopfzeile im Format der letzten Kapitel (*Datum, Uhrzeit — AURORA: geschätzt …*), Zahlen/Wochentage/Tageszähler exakt gegen Kanon, Fakten-Bibel und Vorkapitel. Humor-Standard Kap. 10 (6-9 Momente je 1000 Wörter, warmherzig, KEIN Slapstick, jugendfrei), letzte 400-600 Wörter vor dem Cliffhanger humorfrei. Ken-Follett-Spannung, endet mit Cliffhanger/Sog-Satz. Keine Plot-Weichen außerhalb des Plans.

Format (keine Erklärungen drumherum):
###TITEL###
Kapitel {n}: ...
###INHALT###
(Kapiteltext inkl. Kopfzeile)
###ZUSAMMENFASSUNG###
(2-3 Sätze)
###FAKTEN###
(15-30 Fakten, je Zeile "- ")
###GLOSSAR###
(max. 6 Einträge NAME|KATEGORIE|BESCHREIBUNG oder KEINE)
###ENDE###"""
    for versuch in range(2):
        raw = run_claude(prompt, f"Entwurf Kap. {n} (Versuch {versuch + 1})", "opus", timeout=2400)
        if not raw:
            continue
        if DRY:
            break
        p = s.parse_marked(raw, s.TAGS)
        titel, text = p["###TITEL###"].strip().split("\n")[0].strip(), p["###INHALT###"].strip()
        problems = []
        if not re.match(rf"^Kapitel {n}: .+", titel):
            problems.append("Titelformat")
        if s.wc(text) < 4300:
            problems.append(f"zu kurz ({s.wc(text)} Wörter)")
        if not text.lstrip().startswith("*"):
            problems.append("Kopfzeile fehlt")
        if problems:
            log(f"Entwurf Kap {n} Validierung: {problems}")
            prompt += f"\n\nKORREKTUR: Mängel im letzten Versuch: {', '.join(problems)}. Format/Länge exakt einhalten."
            continue
        body = (f"<!-- ENTWURF {dt.datetime.now():%Y-%m-%d %H:%M} · NICHT im Buch · Basis: Kap. 1-24 Stand {d['statistik'].get('letzte_session')} -->\n"
                f"# {titel}\n\n{text}\n\n---\nZusammenfassung: {p['###ZUSAMMENFASSUNG###'].strip()}\n\nFakten:\n{p['###FAKTEN###'].strip()}\n\nGlossar:\n{p['###GLOSSAR###'].strip()}\n")
        open(f"{OUT}/entwurf_kap{n}.md", "w", encoding="utf-8").write(body)
        fakten = [x.strip().lstrip("-").strip() for x in p["###FAKTEN###"].splitlines() if x.strip()]
        if fakten:
            s.bible_set(n, fakten)
        s.stat_add("entwuerfe_geschrieben")
        log(f"Entwurf Kap. {n}: {titel} ({s.wc(text)} Wörter)")
        break
    else:
        log(f"Entwurf Kap. {n} nicht erzeugt")
        s.stat_add("entwuerfe_fehlgeschlagen")
        s.mark(key)
        return
    s.mark(key)


def check_draft(n):
    """Selbstlektorat des Entwurfs: Konsistenz gegen Kanon/Fakten/Vorkapitel -> Prüfnotiz (Entwurf selbst bleibt unverändert)."""
    key = f"B:check{n}"
    if s.is_done(key):
        return
    p = f"{OUT}/entwurf_kap{n}.md"
    if not os.path.exists(p):
        s.mark(key)
        return
    d = s.load()
    prompt = f"""Du bist kritischer Lektor von AURORA II. Prüfe den ENTWURF von Kapitel {n} gegen Kanon, Fakten-Bibel und die letzten Kapitel. Suche Widersprüche (Zahlen, Uhrzeiten, Wochentage, Namen, Orte, Figuren-Wissensstand), Logiklöcher, Wiederholungen, Humor-Wüsten über 900 Wörter, Floskeln. Nur belegbare Befunde, mit wörtlichem Zitat der Textstelle und konkretem Verbesserungsvorschlag.

KANON: {json.dumps(d.get('kanon'), ensure_ascii=False)}
FAKTEN-BIBEL: {s.bible_txt()}
ZUSAMMENFASSUNGEN: {s.summaries(d)}
LETZTES BUCHKAPITEL: {d['kapitel'][-1]['text'][-6000:]}

ENTWURF:
{open(p, encoding='utf-8').read()}

Antworte als knappes Markdown: Abschnitt "Befunde" (nummeriert: Zitat → Problem → Vorschlag) und "Gesamteindruck" (3 Sätze). Keine Befunde erfinden; wenn nichts: "Keine belegbaren Befunde"."""
    t = run_claude(prompt, f"Prüfnotiz Entwurf {n}", "opus", timeout=1800)
    if t and not DRY:
        open(f"{OUT}/entwurf_kap{n}_PRUEFNOTIZ.md", "w", encoding="utf-8").write(t)
        s.stat_add("pruefnotizen")
    s.mark(key)


def block_b():
    prep_bible()
    for n in (25, 26, 27):
        draft_chapter(n)
        check_draft(n)


def block_c():
    key = "C:varianten"
    if s.is_done(key):
        return
    p27 = f"{OUT}/entwurf_kap27.md"
    d = s.load()
    plan, pk, ctx = aurora_ctx(d, 27)
    if not os.path.exists(p27) and not DRY:
        s.mark(key)
        return
    prompt = f"""Du bist Bolla, Co-Autor von AURORA II. Chris möchte bei den Plot-Weichen am Ende von Kap. 27 mitentscheiden. Entwirf ZWEI alternative Cliffhanger-Schlüsse/Weichen für das Ende von Kap. 27 (zusätzlich zum Entwurf), jeweils ca. 400-600 Wörter ausgeschriebene Schlussszene plus 3 Sätze Folgen für Kap. 28+. Sie müssen mit Master-Wendung, Kanon, Figuren und Humor-Ton vereinbar sein und dürfen die Wendung nicht verraten.

MASTER-WENDUNG (privat): {d['geheim'].get('wendung', '')}
KANON: {json.dumps(d.get('kanon'), ensure_ascii=False)}
BOGENPLAN 27: {json.dumps(pk, ensure_ascii=False)}
ENTWURF KAP. 27: {open(p27, encoding='utf-8').read() if os.path.exists(p27) else '(fehlt)'}

Format: Markdown mit "## Variante A", "## Variante B" und je einem Satz "Warum diese Weiche spannend ist"."""
    t = run_claude(prompt, "Schluss-Varianten Kap. 27", "opus", timeout=1800)
    if t and not DRY:
        open(f"{OUT}/entwurf_kap27_VARIANTEN.md", "w", encoding="utf-8").write(t)
    s.mark(key)


# =============================================================== Plan, Abschluss
def write_plan():
    q = s.quota() or {}
    txt = f"""# Wochenend-Ausreizung {TAG} — PLAN
Start {dt.datetime.now():%a %d.%m. %H:%M} · Deadline {s.DEADLINE:%a %d.%m. %H:%M}
Limits: 5h {q.get('five_hour_pct')} % · Woche {q.get('seven_day_pct')} % (Reset {q.get('reset_label')})

Reihenfolge (alles im Hintergrund, ein Prozess zur Zeit, Opus/Sonnet, nie Fable):
1. Block A — Makler-Tiefenprüfung (Sonnet + Web): alle Makler in Batches à {BATCH}, danach Suche weiterer Kandidaten je Region,
   Einarbeitung in data/makler_status.json (nur ergänzen, nichts löschen, Backup vorher), Bericht als Desktop-HTML + Telegram.
2. Block B — AURORA II (Opus): Entwürfe Kap. 25-27 NUR als Dateien in {OUT} (aurora2.json bleibt unberührt, Kap. 10-24 gehören Chris), je Entwurf eine Prüfnotiz.
3. Block C — zwei alternative Schlüsse für Kap. 27 (Auswahl für Chris).
Danach Ende — was an Kontingent übrig bleibt, bleibt übrig (keine Fake-Arbeit). Sonntag/Montag läuft nichts weiter.
Gating: 5h-Fenster <= 92 %, danach Pause bis Reset; Woche Stopp bei 98,5 %; Notbremse: touch /tmp/aurora_samstag_stop
Status: {OUT}/STATUS.md · Log: {LOGF}
"""
    open(f"{OUT}/PLAN.md", "w", encoding="utf-8").write(txt)
    if not DRY:
        try:
            src = subprocess.run(["wslpath", "-w", f"{OUT}/PLAN.md"], capture_output=True, text=True).stdout.strip()
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Copy-Item -LiteralPath '{src}' -Destination '{DESKTOP_WIN}\\Ausreizen_Plan_{TAG}.md' -Force"],
                           capture_output=True, text=True, timeout=60)
        except Exception as e:
            log(f"Plan-Kopie fehlgeschlagen: {e}")
    telegram(f"🐾 Ausreizen startet ({dt.datetime.now():%a %H:%M}). Plan: 1) Makler-Tiefenprüfung 2) AURORA-Entwürfe Kap. 25–27 (nur als Datei) "
             f"3) Schluss-Varianten. 5h {q.get('five_hour_pct')} %, Woche {q.get('seven_day_pct')} %. Deadline {s.DEADLINE:%a %H:%M}. "
             f"Notbremse: touch /tmp/aurora_samstag_stop")


def abschluss(grund):
    q = s.quota() or {}
    txt = f"""# Wochenend-Ausreizung {TAG} — Abschlussbericht
Ende: {dt.datetime.now():%a %d.%m. %H:%M} · Grund: {grund}
Limits jetzt: 5h {q.get('five_hour_pct')} % · Woche {q.get('seven_day_pct')} %
Statistik: {json.dumps(s.ST['stats'], ensure_ascii=False)}
Erledigte Schritte: {len(s.ST['done'])}: {', '.join(s.ST['done'])}

Ergebnisse in {OUT}:
- Makler: Makler_Pruefung_{TAG}.html (auch Desktop), makler_batch_*.json, makler_neue_*.json; Backup in workspace/backups/makler_status_vor_tiefenpruefung_*
- AURORA (nur Dateien, NICHT im Buch): entwurf_kap25.md/26/27 (+ _PRUEFNOTIZ.md), entwurf_kap27_VARIANTEN.md — Einbau nur nach Chris' OK
"""
    open(f"{OUT}/ABSCHLUSSBERICHT.md", "w", encoding="utf-8").write(txt)
    if not DRY:
        try:
            p = f"{s.HOME}/.claude/projects/-home-bolla/memory/aktuell.md"
            old = open(p, encoding="utf-8").read()
            note = (f"## ✅ {dt.date.today():%d.%m.%Y} — Wochenend-Ausreizung beendet ({grund})\n\n"
                    f"Makler-Tiefenprüfung + AURORA-Entwürfe Kap. 25–27 (nur Dateien, nicht im Buch) + Schluss-Varianten. Details: `{OUT}/ABSCHLUSSBERICHT.md`. "
                    f"Makler-Bericht: Desktop `Makler_Pruefung_{TAG}.html`. Entfernungs-Vorschläge warten auf Chris' Entscheidung.\n\n---\n\n")
            open(p, "w", encoding="utf-8").write(note + old)
        except Exception as e:
            log(f"aktuell.md nicht aktualisiert: {e}")
    telegram(f"🐾 Ausreizen beendet ({grund}). 5h {q.get('five_hour_pct')} %, Woche {q.get('seven_day_pct')} %. "
             f"Bericht: {OUT}/ABSCHLUSSBERICHT.md")
    log("ABSCHLUSSBERICHT geschrieben")


def main():
    lock = open(f"{OUT}/.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("läuft bereits")
        return
    grund = "fertig"
    try:
        log(f"START Ausreizen-Orchestrator{' [DRY-RUN]' if DRY else ''} — Deadline {s.DEADLINE}")
        if not s.is_done("plan"):
            write_plan()
            s.mark("plan")
        block_a()
        block_b()
        block_c()
    except Stop as e:
        grund = f"gestoppt: {e}"
        log(f"STOP: {e}")
    except Exception:
        import traceback
        grund = "Fehler (siehe Log)"
        log("FEHLER: " + traceback.format_exc())
        telegram("⚠️ Ausreizen-Orchestrator: Fehler, siehe logs/ausreizen_orchestrator.log")
    finally:
        abschluss(grund)


if __name__ == "__main__":
    main()
