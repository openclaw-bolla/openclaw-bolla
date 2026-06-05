#!/usr/bin/env python3
"""Erfindet EINMALIG die geheime Master-Wendung für AURORA, webt Saatkörner in den
Prolog ein und erstellt einen pointenfreien Überblick. Schreibt direkt in ki_buch.json.
Gibt NICHTS Spoilerndes aus — nur Status/Längen. So bleibt der Twist geheim."""
import json, os, subprocess, shutil, re, sys

BF = os.path.join(os.path.expanduser("~/workspace"), "data/ki_buch.json")
d = json.load(open(BF))

prolog = next((k for k in d["kapitel"] if k["titel"] == "Prolog"), None)
if not prolog:
    print("FEHLER: kein Prolog gefunden"); sys.exit(1)

krit = json.dumps(d.get("kriterien", {}), ensure_ascii=False, indent=2)
prots = json.dumps(d.get("protagonisten", []), ensure_ascii=False, indent=2)
anta = json.dumps(d.get("antagonist", {}), ensure_ascii=False, indent=2)

prompt = f"""Du bist ein erfahrener Thriller-Autor und Plot-Architekt. Du entwickelst die GEHEIME Master-Wendung für einen deutschen KI-Thriller im Stil von Ken Follett.

BUCH: {d.get('titel')} — {d.get('untertitel')}

KRITERIEN:
{krit}

PROTAGONISTEN:
{prots}

ANTAGONISTIN:
{anta}

AKTUELLER PROLOG:
{prolog['text']}

DEINE AUFGABE — drei Dinge:

1) MASTER-WENDUNG: Erfinde eine starke, ANTI-MAINSTREAM Master-Wendung für das ganze Buch. Der Prolog bedient bewusst das Klischee "KI erwacht im Rechenzentrum, nimmt Kontakt auf" (Bist du allein? / Ich auch.). Deine Wendung muss genau diese Erwartung UNTERLAUFEN und den Prolog rückwirkend in einem völlig anderen Licht erscheinen lassen. KEIN ausgelutschtes "KI wird böse / will die Weltherrschaft / täuscht alle". Geh tiefer, überraschender, menschlicher — etwas, das einen erfahrenen Leser wirklich umhaut und emotional trifft (auch passend zur Liebes-Ebene). Beschreibe die Wendung klar und konkret in 8-15 Sätzen: WAS die Wahrheit ist, WANN/WIE sie enthüllt wird, und WARUM sie den Prolog umdeutet.

2) SAATKÖRNER: Webe in den Prolog 1-3 UNAUFFÄLLIGE Saatkörner ein, die die Wendung später glaubwürdig und rückwirkend stimmig machen. Ändere so WENIG wie möglich — bewahre Ton, Qualität, Humor, Länge und jeden guten Satz des Originals. Füge nur subtile Halbsätze/Details hinzu, die ein Erstleser NICHT als Hinweis erkennt, die aber beim Wiederlesen aufleuchten. Der Prolog muss sich für den Erstleser GENAUSO gut und unverdächtig lesen wie jetzt.

3) ÜBERBLICK: Schreibe einen STRIKT POINTENFREIEN Überblick des Prologs (3-5 Zeilen): wer, wo, welche Stimmung, was passiert grob. NIEMALS die Wendung, den Twist oder den unheimlichen Clou verraten. Das liest der Auftraggeber zum Steuern, OHNE sich zu spoilern.

Antworte AUSSCHLIESSLICH in genau diesem Format:

###WENDUNG###
(die geheime Master-Wendung, 8-15 Sätze)
###SAATKOERNER###
(Notiz: welche Saatkörner du wo eingewoben hast und wie sie später aufgehen)
###PROLOG_NEU###
(der vollständige Prolog-Text mit subtil eingewobenen Saatkörnern — minimal verändert)
###PROLOG_UEBERBLICK###
(pointenfreier Überblick, 3-5 Zeilen)
###ENDE###"""

cl = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
r = subprocess.run([cl, "-p", "--output-format", "json", "--model", "claude-opus-4-8", prompt],
                   capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL,
                   cwd=os.path.expanduser("~"))
if r.returncode != 0:
    print("CLAUDE-FEHLER:", r.stderr[:300]); sys.exit(1)

raw = json.loads(r.stdout).get("result", "")

def ext(a, b):
    m = re.search(re.escape(a) + r'(.*?)' + re.escape(b), raw, re.DOTALL)
    return m.group(1).strip() if m else ""

wendung = ext("###WENDUNG###", "###SAATKOERNER###")
saat = ext("###SAATKOERNER###", "###PROLOG_NEU###")
prolog_neu = ext("###PROLOG_NEU###", "###PROLOG_UEBERBLICK###")
ueberblick = ext("###PROLOG_UEBERBLICK###", "###ENDE###")

# Plausibilitätsprüfung bevor wir den Prolog überschreiben
orig_len = len(prolog["text"])
ok_prolog = prolog_neu and (0.7 * orig_len) <= len(prolog_neu) <= (1.6 * orig_len)

if not wendung:
    print("FEHLER: keine Wendung extrahiert. Rohlänge:", len(raw)); sys.exit(1)

# Backup des Prologs in geheim, dann schreiben
d.setdefault("geheim", {})
d["geheim"]["wendung"] = wendung
d["geheim"]["hinweise_gesaet"] = saat
d["geheim"]["prolog_original"] = prolog["text"]   # Sicherung des Originals

if ok_prolog:
    prolog["text"] = prolog_neu
if ueberblick:
    prolog["ueberblick"] = ueberblick

# Statistik Wörter neu
d.setdefault("statistik", {})["woerter_gesamt"] = sum(len(k["text"].split()) for k in d["kapitel"])

json.dump(d, open(BF, "w"), ensure_ascii=False, indent=2)

# NUR spoilerfreie Status-Ausgabe
print("OK.")
print("  Wendung gesetzt    :", len(wendung), "Zeichen")
print("  Saatkörner-Notiz   :", len(saat), "Zeichen")
print("  Prolog justiert    :", "ja ("+str(len(prolog_neu))+" Z., orig "+str(orig_len)+")" if ok_prolog else "NEIN (Plausi-Check fehlgeschlagen, Original behalten)")
print("  Prolog-Überblick   :", len(ueberblick), "Zeichen", "(gesetzt)" if ueberblick else "(LEER!)")
