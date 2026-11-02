#!/usr/bin/env python3
"""Kurstag 06 - Praktikum-HTML (Handy-Video, Urheberrecht, YouTube) bauen.

CSS-Grundlage = 05-Praktikum.html (gleiches Layout), dazu Zusatz-CSS. Ausgabe nur nach Handouts/Entwurf.
"""
H = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts"
OUT = f"{H}/Entwurf/06-Praktikum.html"

src = open(f"{H}/Praktikum/05-Praktikum.html", encoding="utf-8").read()
css = src[src.index("<style>") + 7:src.index("</style>")]
# Pflicht-Ausblendung beim Drucken bleibt; Zusatz-CSS
css += """
  .zeit-badge { font-size: 14px; font-weight: 700; color: #fff; background: var(--accent); padding: 3px 10px;
    border-radius: 8px; margin-left: 10px; text-transform: none; letter-spacing: 0; white-space: nowrap; }
  .zeitplan { margin: 10px 0 4px; }
  .os-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 10px 0 14px; }
  @media (max-width: 640px) { .os-grid { grid-template-columns: 1fr; } }
  .os-card { border-radius: 14px; padding: 14px 16px; font-size: 18px; border: 2px solid var(--border); background: #fff; }
  .os-card h3 { margin: 0 0 8px; font-size: 20px; }
  .os-card.android { border-color: #8fd9ad; background: #f3fbf6; }
  .os-card.ios { border-color: #b7d4f2; background: #f3f8fd; }
  .os-card ol { margin: 0; padding-left: 22px; }
  .os-card li { margin-bottom: 6px; }
  .plan-b { background: #fff8e6; border: 2px solid #f0d488; border-radius: 12px; padding: 12px 16px; margin: 10px 0; font-size: 18px; }
  .cc-badges { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 12px; }
  .cc { color: #fff; font-weight: 800; border-radius: 10px; padding: 6px 12px; font-size: 18px; }
  .cc small { font-weight: 500; font-size: 14px; display: block; }
  .vis-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 12px; }
  .vis { color: #fff; font-weight: 700; border-radius: 10px; padding: 8px 14px; font-size: 18px; }
  .vis small { font-weight: 500; font-size: 14px; display: block; }
  .szenario { border-top: 1px solid var(--border); padding: 12px 0; }
  .szenario:first-of-type { border-top: none; }
  .ampel-btns { display: flex; gap: 8px; margin: 8px 0; flex-wrap: wrap; }
  .ampel-btns button { font-size: 17px; font-weight: 700; border-radius: 10px; padding: 8px 14px; border: 2px solid var(--border);
    background: #fff; cursor: pointer; }
  .ampel-btns button.gruen { border-color: #8fd9ad; } .ampel-btns button.gelb { border-color: #f0d488; }
  .ampel-btns button.rot { border-color: #f3b8b0; }
  .ampel-btns button.sel { outline: 3px solid var(--accent); }
  .erkl { margin-top: 6px; padding: 10px 14px; border-radius: 10px; font-size: 17px; }
  .erkl.zu { display: none; }
  .erkl.ok { background: var(--loes-bg); border: 2px solid var(--loes-border); color: var(--loes-text); }
  .erkl.nein { background: #fff8e6; border: 2px solid #f0d488; color: #7a5b00; }
  ol.liste { font-size: 18px; padding-left: 24px; margin: 8px 0; } ol.liste li { margin-bottom: 8px; }
  .check-liste { list-style: none; padding: 0; margin: 8px 0 0; }
  .check-liste li { margin-bottom: 8px; }
  @media print { .erkl.zu { display: block !important; } .ampel-btns { display: none; } }
"""

ZEITPLAN_SVG = """
<svg class="zeitplan" viewBox="0 0 740 70" width="100%" role="img" aria-label="Zeitplan 40 Minuten">
  <g font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">
    <rect x="0"   y="6" width="55"  height="34" rx="6" fill="#0a66c2"/><text x="27"  y="28">3'</text>
    <rect x="57"  y="6" width="147" height="34" rx="6" fill="#2e8b57"/><text x="130" y="28">A: 8'</text>
    <rect x="206" y="6" width="129" height="34" rx="6" fill="#7958aa"/><text x="270" y="28">B: 6'</text>
    <rect x="337" y="6" width="92"  height="34" rx="6" fill="#c0392b"/><text x="383" y="28">C: 5'</text>
    <rect x="431" y="6" width="258" height="34" rx="6" fill="#e67e22"/><text x="560" y="28">D: 14'</text>
    <rect x="691" y="6" width="49"  height="34" rx="6" fill="#5b5f66"/><text x="715" y="28">4'</text>
  </g>
  <g font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#5b5f66" text-anchor="middle">
    <text x="27" y="58">Start</text><text x="130" y="58">Handy aufnehmen</text><text x="270" y="58">Kürzen</text>
    <text x="383" y="58">Aufs PC</text><text x="560" y="58">Am PC aufnehmen</text><text x="715" y="58">Puffer</text>
  </g>
</svg>"""

TRIM_SVG = """
<svg viewBox="0 0 700 60" width="100%" role="img" aria-label="Zeitleiste mit Reglern">
  <rect x="0" y="12" width="700" height="36" rx="8" fill="#7958aa"/>
  <rect x="0" y="8" width="60" height="44" rx="8" fill="#c0392b"/><rect x="640" y="8" width="60" height="44" rx="8" fill="#c0392b"/>
  <g font-family="Segoe UI, Arial, sans-serif" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">
    <text x="30" y="36">weg</text><text x="670" y="36">weg</text><text x="350" y="36">dein Clip &#8211; Regler ziehen</text>
  </g>
</svg>"""


def schritt(nr, titel, inhalt, opt=False):
    badge = ' <span class="opt-badge">optional</span>' if opt else ""
    return f"""
  <div class="step">
    <div class="step-head"><div class="step-num">{nr}</div><div class="step-title">{titel}{badge}</div></div>
{inhalt}
  </div>"""


def antwort(placeholder, loesung=None, btn="✅ Lösung anzeigen"):
    h = f'    <textarea class="antwort-feld" placeholder="{placeholder}"></textarea>\n'
    if loesung:
        h += (f'    <button class="loes-btn" onclick="toggleLoes(this)">{btn}</button>\n'
              f'    <div class="loesung zu">{loesung}</div>\n')
    return h


def teil(titel, minuten):
    return f'\n  <div class="teil-titel">{titel} <span class="zeit-badge">⏱️ {minuten} Min</span></div>\n'



body = f"""
<div class="wrap">

  <div class="header">
    <h1>🎬 Praktikum: Videos aufnehmen &ndash; am Handy und am PC</h1>
    <div class="zeit">⏱️ insgesamt 40 Minuten &nbsp;·&nbsp; Handy (Partnerarbeit) + Schul-PC</div>
  </div>
  <div class="step" style="padding-bottom:8px">
    <b>So läuft die Zeit:</b>
    {ZEITPLAN_SVG}
  </div>

  <div class="hinweis">
    Du nimmst <b>deinen Handybildschirm</b> auf, kürzt das Video (<b>20–30 Sekunden</b>), erfährst, wie ein Video
    <b>vom Handy auf den PC</b> kommt &ndash; und nimmst am PC <b>einen kurzen Ausschnitt</b> eines Videos mit dem
    <b>Snipping-Tool</b> auf. Tippe Antworten <b>zuerst selbst</b> ins Feld, dann erst die Lösung anzeigen.
  </div>

  <div class="wichtig">
    📵 <b>Wichtig:</b> Das Handy wird nur benutzt, wenn es erlaubt ist &ndash; und nur für diese Aufgabe.
    Nimm <b>nichts Privates</b> auf: keine Chats, Passwörter, Fotos oder Namen anderer. Mach vorher „Nicht stören“ an.
    Deine Videos werden in diesem Praktikum <b>nirgends veröffentlicht</b> &ndash; sie bleiben bei dir.
  </div>

  <div class="merk">
    <h2>📎 Spickzettel &ndash; Begriffe</h2>
    <table>
      <tr><td class="b">Screen Recording</td><td>Bildschirmaufnahme: das Gerät filmt, was auf dem Bildschirm passiert</td></tr>
      <tr><td class="b">Kürzen (Trimmen)</td><td>Anfang und/oder Ende eines Videos abschneiden</td></tr>
      <tr><td class="b">OTG-Kabel</td><td>kleiner Adapter, damit man einen USB-Stick direkt ans Handy stecken kann</td></tr>
      <tr><td class="b">Snipping-Tool</td><td>Windows-Programm für Bildschirmfotos &ndash; und für kurze Bildschirmvideos</td></tr>
    </table>
  </div>
"""

# ---------------- START ----------------
body += teil("Start", 3)
body += schritt(1, "Startklar machen &amp; Thema wählen", """
    <p class="frage">Setz dich mit deinem Partner/deiner Partnerin zusammen. Prüft: <b>Akku</b> über 30&nbsp;%,
    etwas <b>Speicherplatz</b> frei, <b>„Nicht stören“</b> an. Wählt dann ein <b>Mini-Tutorial</b> für euer Handy,
    z.&nbsp;B.: <i>Wecker stellen</i> &middot; <i>Hintergrundbild ändern</i> &middot; <i>Dunkelmodus einschalten</i>.
    Schreibt <b>3 kurze Schritte</b> als Drehbuch auf.</p>
""" + antwort("Mein Thema und die 3 Schritte ...") + """
    <div class="plan-b">🤝 <b>Plan B:</b> Hat dein Handy keine Bildschirmaufnahme oder ist sie gesperrt? Dann nimm das
    <b>Handy deines Partners/deiner Partnerin</b> &ndash; ihr arbeitet zusammen an einem Video.</div>""")

# ---------------- TEIL A ----------------
body += teil("Teil A &ndash; Handy-Bildschirm aufnehmen", 8)
body += schritt(2, "Bildschirmaufnahme finden &amp; starten", """
    <p class="frage">Die Funktion heißt je nach Handy etwas anders. Such dir die passende Karte:</p>
    <div class="os-grid">
      <div class="os-card android">
        <h3>🤖 Android <small>(Samsung, Pixel, Xiaomi …)</small></h3>
        <ol>
          <li>Mit <b>2 Fingern</b> von oben nach unten wischen &rarr; <b>Schnelleinstellungen</b>.</li>
          <li>Kachel <b>„Bildschirmaufnahme“</b> oder <b>„Bildschirmrekorder“</b> suchen.</li>
          <li>Nicht da? Auf das <b>Stift-Symbol</b> tippen und die Kachel in die Leiste ziehen.</li>
          <li>Kachel antippen, dann <b>Start</b> (es zählt kurz herunter).</li>
          <li>Beenden: <b>rotes Symbol</b> oder Benachrichtigung antippen.</li>
        </ol>
      </div>
      <div class="os-card ios">
        <h3>🍎 iPhone</h3>
        <ol>
          <li><b>Kontrollzentrum</b> öffnen: von der <b>oberen rechten Ecke</b> nach unten wischen (mit Home-Taste: von unten nach oben).</li>
          <li>Symbol <b>Punkt im Kreis</b> antippen &rarr; Countdown 3-2-1.</li>
          <li>Beenden: <b>roten Balken</b> bzw. die rote Uhrzeit oben antippen.</li>
          <li>Symbol fehlt? <b>Einstellungen &rarr; Kontrollzentrum</b> &rarr; „Bildschirmaufnahme“ hinzufügen.</li>
        </ol>
      </div>
    </div>
    <div class="plan-b">⚠️ Manche Apps <b>blockieren</b> die Aufnahme (Bild bleibt schwarz), und Jugendschutz kann die Funktion
    <b>sperren</b>. Dann: Plan B (Partner-Handy).</div>
""")
body += schritt(3, "Mini-Tutorial aufnehmen", """
    <p class="frage">Startet die Aufnahme und führt eure <b>3 Schritte</b> aus Schritt 1 vor &ndash; <b>ruhig und langsam</b>
    (20–30 Sekunden reichen!). Danach Aufnahme beenden und das Video in <b>Fotos/Galerie</b> ansehen.</p>
""" + antwort("Wo hat dein Handy das Video gespeichert? (Ordner/Album)",
              "Meist in <b>Fotos/Galerie</b> &ndash; iPhone: Album <b>„Bildschirmaufnahmen“</b>, Android: häufig ein Ordner "
              "„Bildschirmaufnahmen“/„Screen recordings“ (der Name hängt vom Hersteller ab)."))

# ---------------- TEIL B ----------------
body += teil("Teil B &ndash; Video kürzen", 6)
body += schritt(4, "Anfang &amp; Ende abschneiden", f"""
    <p class="frage">Fast jedes Video hat vorne und hinten „Leerlauf“ (Aufnahme starten/stoppen). Schneide beides weg:</p>
    {TRIM_SVG}
    <div class="os-grid">
      <div class="os-card ios">
        <h3>🍎 iPhone &ndash; Fotos-App</h3>
        <ol>
          <li><b>Fotos</b> &rarr; dein Video öffnen &rarr; <b>Bearbeiten</b>.</li>
          <li>Unten die <b>Zeitleiste</b>: gelben Rahmen links/rechts ziehen.</li>
          <li><b>Fertig</b> antippen.</li>
        </ol>
      </div>
      <div class="os-card android">
        <h3>🤖 Android &ndash; Fotos / Galerie</h3>
        <ol>
          <li>Video öffnen &rarr; <b>Bearbeiten</b> (Stift-Symbol).</li>
          <li>Die <b>Regler</b> an der Zeitleiste verschieben.</li>
          <li><b>Speichern</b> &ndash; wenn möglich „als Kopie“.</li>
        </ol>
      </div>
    </div>
""" + antwort("Wie lang war dein Video vorher, wie lang jetzt?"))
body += schritt(5, "Privatsphäre-Check", """
    <p class="frage">Spiel dein Video einmal ab. Siehst du <b>Namen, Chats, Telefonnummern</b> oder Benachrichtigungen
    anderer? Wie würdest du das lösen?</p>
""" + antwort("Meine Lösung ...",
              "<b>Neu aufnehmen</b> (mit „Nicht stören“) oder die Stelle <b>herausschneiden</b>. Am besten gar nicht erst fremde Chats aufnehmen."))

# ---------------- TEIL C ----------------
body += teil("Teil C &ndash; Video vom Handy auf den PC", 5)
body += schritt(6, "Welche Wege gibt es?", """
    <p class="frage">Dein Video liegt auf dem Handy &ndash; du willst es am PC weiterverwenden. Zwei Wege:</p>
    <div class="os-grid">
    <div class="os-card android">
      <h3>🔌 Weg 1: USB-C-Stick oder OTG-Kabel</h3>
      <ol>
        <li>Hat dein Handy einen <b>USB-C-Anschluss</b>? Dann geht ein <b>USB-C-Stick</b> direkt, oder ein normaler Stick mit <b>OTG-Adapter</b> (kleines Zwischenstück).</li>
        <li>Stick ans Handy stecken, in <b>Dateien/Galerie</b> das Video <b>kopieren</b> und auf dem Stick einfügen.</li>
        <li>Stick am PC einstecken &rarr; Video im <b>Explorer</b> öffnen.</li>
      </ol>
    </div>
    <div class="os-card ios">
      <h3>🌐 Weg 2: itslearning &ndash; „Dateien“</h3>
      <ol>
        <li>In itslearning oben rechts auf dein <b>Profilbild/Namen</b> klicken (persönliches Menü) &rarr; <b>„Dateien“</b>.</li>
        <li>Am Handy (itslearning-App oder Browser) das Video dort <b>hochladen</b> (<b>Hinzufügen</b> &rarr; <b>Datei hochladen</b>).</li>
        <li>Am PC im Browser bei itslearning einloggen, wieder zu <b>„Dateien“</b> gehen und das Video <b>herunterladen</b>.</li>
        <li>✅ Das geht mit dem Handy und ist getestet. Bei großen Videos kann das Hochladen etwas dauern &ndash; warte, bis es fertig ist.</li>
      </ol>
    </div>
    </div>
    <div class="plan-b">🔒 Auf Schul-PCs gilt wie immer: nur eigene Dateien, nichts Privates ablegen &ndash; und nur, wenn die Lehrkraft es erlaubt.</div>
""" + antwort("Welchen Weg würdest du nehmen und warum?"))

# ---------------- TEIL D ----------------
body += teil("Teil D &ndash; Am PC aufnehmen: Snipping-Tool", 14)
body += """
  <div class="wichtig">
    🔒 <b>Datenschutz &amp; Recht:</b> Nimm höchstens <b>15 Sekunden</b> auf und achte darauf, dass <b>keine Personen erkennbar</b>
    sind, die nicht einverstanden sind, und <b>keine privaten Daten</b> (Namen, Chats, Konten) zu sehen sind. Die Aufnahme bleibt
    <b>bei dir</b> &ndash; <b>nicht</b> weitergeben oder hochladen. Merksatz: <i>Für dich angucken und behalten &ndash; meist okay.
    Hochladen oder weitergeben &ndash; das kann richtig teuer werden, und die Rechnung kriegen eure Eltern.</i>
  </div>
"""
body += schritt(7, "Ein Video suchen", """
    <p class="frage">Öffne am PC im Browser <b>youtube.com</b> und suche ein <b>harmloses Video</b> zu einem Thema, das dich
    interessiert (z.&nbsp;B. Tiere, Natur, Technik &ndash; <b>keine Videos mit Personen aus eurer Schule</b>). Starte es und
    halte es an einer interessanten Stelle an.</p>
""" + antwort("Welches Video hast du gewählt (Titel)?"))
body += schritt(8, "Mit dem Snipping-Tool aufnehmen", """
    <p class="frage">So nimmst du einen <b>Ausschnitt</b> des Bildschirms als Video auf:</p>
    <ol class="liste">
      <li>Drücke gleichzeitig die Tasten <b>Windows + Umschalt + S</b> (<b>Umschalt</b> = die Taste mit dem dicken Pfeil nach oben).
          Alternativ: Startmenü &rarr; <b>„Snipping Tool“</b> tippen und öffnen.</li>
      <li>Oben erscheint eine kleine Leiste. Klicke auf das <b>Video-Symbol</b> (Filmkamera) und dann auf <b>„Neu“</b>
          bzw. <b>„Aufnahme“</b>.</li>
      <li>Ziehe mit der <b>linken Maustaste</b> ein Rechteck um den Teil des Bildschirms, den du aufnehmen willst
          (z.&nbsp;B. nur das Videofenster) &rarr; klicke auf <b>„Start“</b>.</li>
      <li>Es zählt <b>3-2-1</b> herunter. Spiele jetzt dein Video ab &ndash; <b>höchstens 15 Sekunden</b>!</li>
      <li>Klicke auf das <b>rote Quadrat (Stopp)</b>. Die Aufnahme öffnet sich zur Ansicht.</li>
      <li>Speichere sie mit <b>Speichern</b> (Diskettensymbol) &rarr; in deinen <b>Stick/Ordner</b>, nicht irgendwo auf dem PC.</li>
    </ol>
    <div class="plan-b">💡 <b>Klappt nicht?</b> Menüs und Symbole sehen je nach Windows-Version etwas anders aus &ndash; schau dich in der
    Leiste um. Hilft nichts: Partner fragen, dann Lehrkraft.</div>
""" + antwort("Wie lang ist deine Aufnahme? Wo hast du sie gespeichert?",
              "Die Aufnahme sollte <b>unter 15 Sekunden</b> liegen und als <b>.mp4</b>-Datei auf deinem Stick/Ordner gespeichert sein. "
              "Prüfe im Explorer, ob du sie per Doppelklick abspielen kannst."))
body += schritt(9, "Prüfen &amp; Datenschutz-Check", """
    <p class="frage">Spiel deine Aufnahme ab. Passt der Ausschnitt? Sind <b>Personen</b> oder <b>private Daten</b> zu sehen?
    Und: Was würdest du <b>nicht</b> mit dieser Aufnahme machen?</p>
""" + antwort("Meine Antwort ...",
              "Ausschnitt/Ton prüfen; ggf. <b>neu aufnehmen</b>. <b>Nicht</b> machen: öffentlich hochladen, in Chats/Social Media weitergeben &ndash; "
              "das Video gehört dem Urheber, nicht dir. Nur für dich ansehen ist okay."))

body += """

  <div class="end-box">
    <button class="print-btn" onclick="window.print()">🖨️ Antworten als PDF speichern</button>
    <div class="info">Beim Drucken/PDF-Speichern werden alle Lösungen automatisch mit ausgegeben &ndash; so hast du Fragen, deine Antworten und die Musterlösung auf einem Blatt.</div>
  </div>

</div>
<script>
function toggleLoes(btn) {
  var box = btn.nextElementSibling;
  var zu = box.classList.toggle('zu');
  btn.textContent = zu ? '✅ Lösung anzeigen' : '🙈 Lösung verbergen';
}
</script>
"""

html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Praktikum: Videos aufnehmen – Handy und PC</title>
<style>{css}</style>
</head>
<body>{body}</body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(html)
print("geschrieben:", OUT, len(html))
