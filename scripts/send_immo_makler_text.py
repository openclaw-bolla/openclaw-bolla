"""Immo-Voranfrage an Makler (Freigabe Chris 14.10.2026, Entwurf v4 + 'Westen und Süden').
Einzelmails von ernstmandel@outlook.de via Graph, 30 s Abstand, Staltmayr ausgenommen.
Aufruf: --dry (nur listen) | ohne Argument = senden. Status wird je Mail in makler_status.json gesetzt."""
import json, sys, time, html, datetime, requests

DATA = "/home/bolla/workspace/data/makler_status.json"
CRIT = json.load(open("/home/bolla/workspace/config/immo_criteria.json"))
SKIP_IDS = {"staltmayr"}
must = [k for k, p in CRIT["priorities"].items() if p == "must"]
imp = [k for k, p in CRIT["priorities"].items() if p == "important"]
SUBJECT = "Suchanfrage Eigentumswohnung – Voranfrage"
INTRO = ("wir suchen eine Eigentumswohnung zur Eigennutzung im Westen und Süden von München (Details unten) — "
         "frühestens ab Herbst 2027, möglicherweise auch erst ab Herbst 2028. Es eilt also nicht; wir würden uns aber "
         "gerne frühzeitig bei Ihnen vormerken lassen.")
def ul(items): return "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"
BODY = f"""<div style="font-family:Aptos,Calibri,sans-serif;font-size:12pt">
<p>Sehr geehrte Damen und Herren,</p>
<p>{html.escape(INTRO)}</p>
<p><b>Unsere Kernanforderungen:</b></p>{ul(must)}
<p><b>Optionale Anforderungen:</b></p>{ul(imp)}
<p>Für Angebote, die diesen Kriterien entsprechen, würden wir uns sehr freuen, von Ihnen zu hören — auch wenn diese erst später verfügbar werden. Bitte nehmen Sie uns gerne in Ihre Interessentenliste auf.</p>
<p>Mit freundlichen Grüßen<br>Chris &amp; Renate Mandel<br>ernstmandel@outlook.de</p>
</div>"""

