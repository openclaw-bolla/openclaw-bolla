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
  .check-liste { list-style: none; padding: 0; margin: 8px 0 0; }
  .check-liste li { margin-bottom: 8px; }
  @media print { .erkl.zu { display: block !important; } .ampel-btns { display: none; } }
"""

ZEITPLAN_SVG = """
<svg class="zeitplan" viewBox="0 0 740 70" width="100%" role="img" aria-label="Zeitplan 40 Minuten">
  <g font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">
    <rect x="0"   y="6" width="55"  height="34" rx="6" fill="#0a66c2"/><text x="27"  y="28">3'</text>
    <rect x="57"  y="6" width="147" height="34" rx="6" fill="#2e8b57"/><text x="130" y="28">A: 8'</text>
    <rect x="206" y="6" width="221" height="34" rx="6" fill="#7958aa"/><text x="316" y="28">B: 12'</text>
    <rect x="429" y="6" width="129" height="34" rx="6" fill="#c0392b"/><text x="493" y="28">C: 7'</text>
    <rect x="560" y="6" width="147" height="34" rx="6" fill="#e67e22"/><text x="633" y="28">D: 8'</text>
    <rect x="709" y="6" width="31"  height="34" rx="6" fill="#5b5f66"/><text x="724" y="28">2'</text>
  </g>
  <g font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#5b5f66" text-anchor="middle">
    <text x="27" y="58">Start</text><text x="130" y="58">Aufnehmen</text><text x="316" y="58">Schneiden</text>
    <text x="493" y="58">Recht</text><text x="633" y="58">YouTube</text><text x="724" y="58">Puffer</text>
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


AMPEL = [
    ("Du filmst deinen Handybildschirm: Wecker stellen, nur eigene Einstellungen sichtbar. Du zeigst es der Klasse.",
     "gruen", "Eigene Inhalte, nichts Fremdes sichtbar – das ist völlig in Ordnung."),
    ("Du legst einen aktuellen Chart-Hit unter dein Tutorial und lädst es <b>öffentlich</b> auf YouTube hoch.",
     "rot", "Der Song gehört nicht dir. Öffentlich hochladen ohne Erlaubnis/Lizenz ist nicht erlaubt – "
            "YouTube erkennt solche Musik meist automatisch."),
    ("Du nutzt ein Foto mit der Lizenz <b>CC BY</b> aus Wikimedia Commons und nennst Titel, Urheber, Lizenz und Quelle.",
     "gruen", "Genau dafür ist CC BY da: Nutzung erlaubt, wenn du die Quelle sauber angibst "
              "(und die weiteren Lizenzbedingungen einhältst)."),
    ("Du filmst heimlich eine Mitschülerin beim Lachen und schickst das Video in den Klassenchat.",
     "rot", "Ohne Wissen und Einwilligung geht das nicht: Recht am eigenen Bild. Erst fragen – "
            "und wenn die Person „Nein“ sagt, gilt das."),
    ("Du schneidest 10 Sekunden aus einem Kinofilm und lädst sie als „Meme“ öffentlich hoch.",
     "gelb", "Kurz heißt nicht automatisch erlaubt. Es gibt enge Ausnahmen (z. B. Zitat), aber meistens braucht man "
             "eine Erlaubnis. Im Zweifel: lieber nicht."),
    ("Ein Freund sagt mündlich „ja, passt schon“. Du willst ein Foto von euch beiden <b>öffentlich</b> posten.",
     "gelb", "Besser eine klare Einwilligung einholen (am besten schriftlich/Chat) – und bei unter 18 meist auch die Eltern fragen."),
]
FARBE = {"gruen": "🟢 Erlaubt", "gelb": "🟡 Kommt drauf an", "rot": "🔴 Nicht ohne Erlaubnis"}


def ampel_html():
    out = ""
    for i, (txt, ans, erkl) in enumerate(AMPEL):
        out += f"""
    <div class="szenario" data-antwort="{ans}">
      <div class="frage"><b>{chr(65 + i)})</b> {txt}</div>
      <div class="ampel-btns">
        <button class="gruen" onclick="ampel(this,'gruen')">🟢 Erlaubt</button>
        <button class="gelb" onclick="ampel(this,'gelb')">🟡 Kommt drauf an</button>
        <button class="rot" onclick="ampel(this,'rot')">🔴 Nicht ohne Erlaubnis</button>
      </div>
      <div class="erkl zu"><span class="ergebnis"></span> <b>Richtig: {FARBE[ans]}.</b> {erkl}</div>
    </div>"""
    return out


body = f"""
<div class="wrap">

  <div class="header">
    <h1>🎬 Praktikum: Handy-Video, Urheberrecht &amp; YouTube</h1>
    <div class="zeit">⏱️ insgesamt 40 Minuten &nbsp;·&nbsp; Handy (Partnerarbeit) + Schul-PC</div>
  </div>
  <div class="step" style="padding-bottom:8px">
    <b>So läuft die Zeit:</b>
    {ZEITPLAN_SVG}
  </div>

  <div class="hinweis">
    Du nimmst <b>deinen Handybildschirm</b> auf, schneidest ein kurzes Video (<b>20–30 Sekunden</b>), prüfst, was du
    damit <b>darfst</b> – und lernst am PC, wie man ein Video auf YouTube <b>teilt, einbindet und hochlädt</b>.
    Tippe Antworten <b>zuerst selbst</b> ins Feld, dann erst die Lösung anzeigen.
  </div>

  <div class="wichtig">
    📵 <b>Wichtig:</b> Das Handy wird nur benutzt, wenn es erlaubt ist &ndash; und nur für diese Aufgabe.
    Nimm <b>nichts Privates</b> auf: keine Chats, Passwörter, Fotos oder Namen anderer. Mach vorher „Nicht stören“ an.
    Dein Video wird in diesem Praktikum <b>nirgends hochgeladen</b> &ndash; es bleibt auf deinem Handy.
  </div>

  <div class="merk">
    <h2>📎 Spickzettel &ndash; Begriffe</h2>
    <table>
      <tr><td class="b">Screen Recording</td><td>Bildschirmaufnahme: das Handy filmt, was auf dem Display passiert</td></tr>
      <tr><td class="b">Trimmen</td><td>Anfang und/oder Ende eines Videos abschneiden</td></tr>
      <tr><td class="b">Urheber</td><td>die Person, die ein Bild, Lied oder Video gemacht hat &ndash; sie bestimmt, was damit passiert</td></tr>
      <tr><td class="b">Lizenz</td><td>die Erlaubnis des Urhebers, sein Werk unter bestimmten Bedingungen zu nutzen</td></tr>
      <tr><td class="b">Sichtbarkeit</td><td>wer ein YouTube-Video sehen darf: privat, nicht gelistet oder öffentlich</td></tr>
    </table>
  </div>
"""

# ---------------- START ----------------
body += teil("Start", 3)
body += schritt(1, "Startklar machen &amp; Thema wählen", """
    <p class="frage">Setz dich mit deinem Partner/deiner Partnerin zusammen. Prüft: <b>Akku</b> über 30&nbsp;%,
    etwas <b>Speicherplatz</b> frei, <b>„Nicht stören“</b> an. Wählt dann ein <b>Mini-Tutorial</b> für euer Handy,
    z.&nbsp;B.: <i>Wecker stellen</i> &middot; <i>Hintergrundbild ändern</i> &middot; <i>Helligkeit/Dunkelmodus einschalten</i>
    &middot; <i>Kamera-Modus wechseln</i>. Schreibt <b>3 kurze Schritte</b> als Drehbuch auf.</p>
""" + antwort("Mein Thema und die 3 Schritte ...") + """
    <div class="plan-b">🤝 <b>Plan B:</b> Hat dein Handy keine Bildschirmaufnahme oder ist sie gesperrt? Dann nimm das
    <b>Handy deines Partners/deiner Partnerin</b> &ndash; ihr arbeitet zusammen an einem Video.</div>""")

# ---------------- TEIL A ----------------
body += teil("Teil A &ndash; Bildschirm aufnehmen", 8)
body += schritt(2, "Bildschirmaufnahme finden &amp; starten", """
    <p class="frage">Die Funktion heißt je nach Handy etwas anders. Such dir die passende Karte:</p>
    <div class="os-grid">
      <div class="os-card android">
        <h3>🤖 Android <small>(Samsung, Pixel, Xiaomi …)</small></h3>
        <ol>
          <li>Mit <b>2 Fingern</b> von oben nach unten wischen &rarr; <b>Schnelleinstellungen</b>.</li>
          <li>Kachel <b>„Bildschirmaufnahme“</b> oder <b>„Bildschirmrekorder“</b> suchen (der Name hängt vom Hersteller ab).</li>
          <li>Nicht da? Auf das <b>Stift-/Bearbeiten-Symbol</b> tippen und die Kachel in die Leiste ziehen.</li>
          <li>Kachel antippen, bei Bedarf den <b>Ton</b> wählen, dann <b>Start</b> (es zählt kurz herunter).</li>
          <li>Aufnahme beenden: <b>rotes Symbol</b> oder Benachrichtigung antippen.</li>
        </ol>
      </div>
      <div class="os-card ios">
        <h3>🍎 iPhone</h3>
        <ol>
          <li><b>Kontrollzentrum</b> öffnen: von der <b>oberen rechten Ecke</b> nach unten wischen (mit Home-Taste: von unten nach oben).</li>
          <li>Symbol <b>Punkt im Kreis</b> antippen &rarr; Countdown 3-2-1.</li>
          <li>Mit Ton: Symbol <b>lange drücken</b> &rarr; <b>Mikrofon</b> einschalten.</li>
          <li>Beenden: <b>roten Balken</b> bzw. die rote Uhrzeit oben antippen.</li>
          <li>Symbol fehlt? <b>Einstellungen &rarr; Kontrollzentrum</b> &rarr; „Bildschirmaufnahme“ hinzufügen.</li>
        </ol>
      </div>
    </div>
    <div class="plan-b">⚠️ Manche Apps (z.&nbsp;B. Streaming oder Banking) <b>blockieren</b> die Aufnahme &ndash; das Bild bleibt dann schwarz.
    Jugendschutz oder Bildschirmzeit können die Funktion ebenfalls <b>sperren</b>. Dann: Plan B (Partner-Handy).</div>
""")
body += schritt(3, "Mini-Tutorial aufnehmen", """
    <p class="frage">Startet die Aufnahme und führt eure <b>3 Schritte</b> aus Schritt 1 vor &ndash; <b>ruhig und langsam</b>
    (20–30 Sekunden reichen!). Wollt ihr dazu sprechen, ist das <b>Mikro</b> an. Danach: Aufnahme beenden und
    das Video in <b>Fotos/Galerie</b> ansehen (oft im Ordner/Album „Bildschirmaufnahmen“).</p>
""" + antwort("Wo hat dein Handy das Video gespeichert? (Ordner/Album)",
              "Meist in <b>Fotos/Galerie</b> &ndash; iPhone: Album <b>„Bildschirmaufnahmen“</b>, Android: häufig ein Ordner "
              "namens „Bildschirmaufnahmen“/„Screen recordings“ (der Name hängt vom Hersteller ab)."))
body += schritt(4, "Ton richtig wählen", """
    <p class="frage">Du willst nur <b>deine Stimme</b> im Video, aber <b>keine Musik</b> aus einer App. Und du willst
    <b>keinen</b> Ton von anderen Leuten im Raum. Was beachtest du?</p>
""" + antwort("Meine Überlegung ...",
              "Mikro nur nutzen, wenn du sprechen willst &ndash; es nimmt <b>alles</b> im Raum mit auf. Den <b>Systemton</b> "
              "(Musik/Spiel) ausschalten bzw. „kein Ton“ wählen, wenn du keine fremde Musik brauchst. "
              "Und denk dran: Musik aus anderen Apps ist <b>urheberrechtlich geschützt</b> (siehe Teil C)."), opt=True)

# ---------------- TEIL B ----------------
body += teil("Teil B &ndash; Video schneiden", 12)
body += schritt(5, "Video kürzen (Anfang &amp; Ende weg)", f"""
    <p class="frage">Fast jedes Video hat vorne und hinten „Leerlauf“ (Aufnahme starten/stoppen). Schneide beides weg:</p>
    {TRIM_SVG}
    <div class="os-grid">
      <div class="os-card ios">
        <h3>🍎 iPhone &ndash; Fotos-App</h3>
        <ol>
          <li><b>Fotos</b> &rarr; dein Video öffnen &rarr; <b>Bearbeiten</b>.</li>
          <li>Unten die <b>Zeitleiste</b>: gelben Rahmen links/rechts ziehen.</li>
          <li><b>Fertig</b> &ndash; das Original lässt sich später wiederherstellen.</li>
        </ol>
      </div>
      <div class="os-card android">
        <h3>🤖 Android &ndash; Google Fotos / Galerie</h3>
        <ol>
          <li>Video öffnen &rarr; <b>Bearbeiten</b> (Stift-Symbol).</li>
          <li>Die <b>Regler</b> an der Zeitleiste verschieben.</li>
          <li><b>Speichern</b> &ndash; wenn möglich „als Kopie“. (Samsung &amp; Co.: eigene Galerie-App, gleiche Idee.)</li>
        </ol>
      </div>
    </div>
""" + antwort("Wie lang war dein Video vorher, wie lang jetzt?"))
body += schritt(6, "Mit einer Schnitt-App: Text einblenden &amp; Clip teilen", """
    <p class="frage">Es gibt kostenlose Apps für Android <b>und</b> iPhone, z.&nbsp;B. <b>CapCut</b>, <b>InShot</b> oder
    <b>YouTube Create</b>. Funktionen, Preise und Verfügbarkeit <b>ändern sich</b> &ndash; du musst keine installieren.
    Falls <b>erlaubt</b> und schon vorhanden (oder mit Erlaubnis deiner Eltern installiert):</p>
    <p class="frage">🔹 Video laden &rarr; an einer Stelle <b>teilen (Split)</b> und ein Stück löschen<br>
    🔹 einen kurzen <b>Titel/Text</b> einblenden („So stellst du einen Wecker“)<br>
    🔹 Musik <b>nur</b> aus einer Quelle, bei der du die Nutzungsbedingungen kennst &ndash; im Zweifel ganz ohne</p>
    <div class="plan-b">🔒 <b>Datenschutz:</b> Apps fragen oft nach Zugriff auf Fotos oder Mikrofon &ndash; erlaube nur, was du wirklich brauchst.
    Achte auf die <b>Altersfreigabe</b> im Store, frag im Zweifel deine <b>Eltern</b>. „Gratis“ heißt oft: Werbung oder
    Zusatzfunktionen gegen Geld.</div>
""", opt=True)
body += schritt(7, "Speichern / Exportieren", """
    <p class="frage">Speichere dein fertiges Video (Fotos-App: <b>Fertig</b>; Schnitt-App: <b>Exportieren/Speichern</b>).
    Kurze Videos in normaler Qualität reichen &ndash; je größer, desto länger dauert das Teilen. Prüfe, ob das
    <b>geschnittene</b> Video in der Galerie liegt, und spiele es einmal komplett ab.</p>
""" + antwort("Stimmt Anfang, Ende und Länge? Was würdest du noch ändern?"))
body += schritt(8, "Privatsphäre-Check", """
    <p class="frage">Schau dein Video mit „Datenschutz-Brille“ an: Siehst du <b>Namen, Chats, Telefonnummern,
    Profilbilder</b> oder Benachrichtigungen anderer? Wie würdest du das lösen?</p>
""" + antwort("Meine Lösung ...",
              "<b>Neu aufnehmen</b> (mit „Nicht stören“), die Stelle <b>herausschneiden</b> oder – falls die App es kann – "
              "den Bereich <b>unkenntlich</b> machen. Und: Am besten gar nicht erst fremde Chats aufnehmen."))

# ---------------- TEIL C ----------------
body += teil("Teil C &ndash; Was darf ich? Urheberrecht &amp; Recht am Bild", 7)
body += """
  <div class="merk">
    <h2>📎 Das Wichtigste in Kürze (Deutschland)</h2>
    <table>
      <tr><td class="b">Urheberrecht</td><td>Wer ein Foto, Lied oder Video macht, ist <b>automatisch Urheber</b> &ndash; ohne ©-Zeichen, ohne Anmeldung. Fremdes brauchst du nur mit <b>Erlaubnis (Lizenz)</b> zu nutzen. Gilt für <b>Bild, Ton und Video</b>.</td></tr>
      <tr><td class="b">Musik &amp; YouTube</td><td>Ein bekannter Song unter deinem <b>öffentlichen</b> Video ist meist ein Problem. YouTube erkennt Musik oft automatisch (Video kann gesperrt oder stumm werden). Klassenraum ≠ öffentlich hochladen.</td></tr>
      <tr><td class="b">Recht am eigenen Bild</td><td>Menschen dürfen nur mit <b>Einwilligung</b> veröffentlicht werden &ndash; bei unter 18 meist auch mit Erlaubnis der Eltern. Heimlich filmen oder Gespräche aufnehmen ist <b>verboten</b>.</td></tr>
      <tr><td class="b">Download</td><td>Fremde YouTube-Videos <b>herunterladen</b> ist laut YouTube-Regeln nicht erlaubt &ndash; lieber <b>verlinken</b>.</td></tr>
    </table>
    <p style="font-size:15px;margin:10px 0 0;color:#7a5b00">Das ist eine Einführung &ndash; <b>keine Rechtsberatung</b>.</p>
  </div>
"""
body += schritt(9, "Ampel-Check: erlaubt oder nicht?", """
    <p class="frage">Entscheide bei jedem Fall <b>zuerst selbst</b> &ndash; klick dann deine Ampelfarbe an.</p>""" + ampel_html())
body += schritt(10, "Creative-Commons-Lizenzen", """
    <p class="frage">Manche Urheber erlauben die Nutzung unter Bedingungen (<b>CC-Lizenzen</b>). Die Kürzel:</p>
    <div class="cc-badges">
      <div class="cc" style="background:#0a66c2">BY<small>Namensnennung</small></div>
      <div class="cc" style="background:#e67e22">NC<small>nicht kommerziell</small></div>
      <div class="cc" style="background:#c0392b">ND<small>nicht verändern</small></div>
      <div class="cc" style="background:#2e8b57">SA<small>Weitergabe unter gleichen Bedingungen</small></div>
      <div class="cc" style="background:#5b5f66">CC0<small>frei, ohne Auflagen</small></div>
    </div>
    <p class="frage">Ein Foto hat die Lizenz <b>CC BY-ND</b>. Darfst du es einfügen? Darfst du es einfärben/zuschneiden?
    Was musst du angeben?</p>
""" + antwort("Meine Antwort ...",
              "<b>BY</b> = du musst den Urheber nennen, <b>ND</b> = du darfst das Bild <b>nicht verändern</b>. Also: "
              "unverändert einfügen ist okay, einfärben oder zuschneiden <b>nicht</b>. Angeben: "
              "<b>Titel, Urheber, Lizenz, Link zur Lizenz, Ursprung (Fundort)</b> – die „TULLU“-Merkregel."))
body += schritt(11, "Quellenangabe schreiben", """
    <p class="frage">Beispiel: Das Foto <i>„Sonnenuntergang am See“</i> von <i>Anna Beispiel</i> (erfunden!), Lizenz CC BY 4.0,
    gefunden auf Wikimedia Commons. Schreibe die Quellenangabe in einem Satz.</p>
""" + antwort("Meine Quellenangabe ...",
              "z.&nbsp;B.: <i>„Sonnenuntergang am See“ von Anna Beispiel, Lizenz CC BY 4.0 "
              "(creativecommons.org/licenses/by/4.0), Quelle: Wikimedia Commons.</i>"), opt=True)

# ---------------- TEIL D ----------------
body += teil("Teil D &ndash; YouTube am PC", 8)
body += schritt(12, "Ein Creative-Commons-Video finden", """
    <p class="frage">Öffne am PC <b>youtube.com</b>. Suche z.&nbsp;B. nach <b>„Big Buck Bunny“</b> (Film der Blender Foundation)
    oder einem Thema deiner Wahl. Klick auf <b>Filter</b> und wähle bei den Funktionen <b>„Creative Commons“</b>.
    (Menünamen ändern sich manchmal &ndash; schau dich um.) Öffne ein Video und lies in der <b>Beschreibung</b>:
    Welche <b>Lizenz</b> steht dort?</p>
""" + antwort("Video-Titel und Lizenz ...",
              "Bei Creative-Commons-Videos steht in der Beschreibung <b>„Lizenz: Creative Commons – Namensnennung“</b> (oder ähnlich). "
              "Bei normalen Videos: <b>„Standard-YouTube-Lizenz“</b> &ndash; die gibt <b>keine</b> Erlaubnis zum Weiterverwenden."))
body += schritt(13, "Link teilen &amp; Startzeit", """
    <p class="frage">Unter dem Video: <b>Teilen</b> &rarr; <b>Link kopieren</b>. Setze das Häkchen <b>„Beginnen bei“</b>
    (z.&nbsp;B. 0:30) und öffne den Link in einem <b>neuen Tab</b>. Startet das Video an der richtigen Stelle?
    Schau auch, was bei <b>Einbetten</b> erscheint (Code für Webseiten &ndash; du musst ihn nicht verwenden).</p>
""" + antwort("Hat es geklappt? Wofür ist ein Link mit Startzeit praktisch?",
              "Der Link springt direkt zur wichtigen Stelle &ndash; praktisch für Präsentationen, Chats oder Webseiten. "
              "<b>Link statt Kopie</b> heißt: Das Video bleibt beim Urheber, du lädst nichts Fremdes hoch."))
body += schritt(14, "Hochladen – wer darf was sehen?", """
    <p class="frage">Beim Hochladen (Demo am Lehrer-PC: <b>YouTube Studio &rarr; Erstellen &rarr; Video hochladen</b>) wählt man
    Titel, Beschreibung, die Zielgruppe („für Kinder?“) und die <b>Sichtbarkeit</b>:</p>
    <div class="vis-row">
      <div class="vis" style="background:#2e8b57">Privat<small>nur ich + Eingeladene</small></div>
      <div class="vis" style="background:#e67e22">Nicht gelistet<small>jeder mit dem Link</small></div>
      <div class="vis" style="background:#c0392b">Öffentlich<small>jeder kann es finden</small></div>
    </div>
    <p class="frage">Welche Sichtbarkeit passt? Begründe kurz: <b>a)</b> dein Tutorial nur für Oma &nbsp;
    <b>b)</b> ein Video, in dem Mitschüler zu sehen sind, die nicht gefragt wurden &nbsp;
    <b>c)</b> dein eigenes Lied, ohne fremde Samples, das alle hören dürfen</p>
""" + antwort("a) ... b) ... c) ...",
              "<b>a)</b> <b>Nicht gelistet</b> (oder privat mit Einladung) – nur Leute mit Link. "
              "<b>b)</b> <b>Gar nicht hochladen</b>, bis alle (bei unter 18 auch die Eltern) einverstanden sind. "
              "<b>c)</b> <b>Öffentlich</b> ist okay – wenn du wirklich alle Rechte hast. "
              "Hinweis: Für ein eigenes YouTube-Konto/einen Kanal gibt es <b>Altersgrenzen</b> &ndash; "
              "ohne Erlaubnis der Eltern also kein eigener Kanal."))
body += schritt(15, "Video auf den PC bringen", """
    <p class="frage">Wie kommt ein Handy-Video an den PC? Mögliche Wege: <b>USB-Kabel</b> (Handy auf „Dateiübertragung“),
    <b>Cloud</b> (z.&nbsp;B. Google Drive/OneDrive) oder <b>an dich selbst senden</b>. Auf Schul-PCs gilt wie immer:
    <b>auf dem Stick arbeiten</b>, nichts Privates ablegen &ndash; und nur, wenn die Lehrkraft es erlaubt.</p>
""" + antwort("Welchen Weg würdest du nehmen und warum?"), opt=True)

body += """
  <div class="gefahr">
    <h2>✅ Checkliste: Darf ich das hochladen?</h2>
    <ul class="check-liste">
      <li>☐ Habe ich es <b>selbst</b> gemacht (Bild, Ton, Video)?</li>
      <li>☐ Sind <b>Personen</b> drauf &ndash; und einverstanden (bei unter 18 auch die Eltern)?</li>
      <li>☐ Fremde Bilder/Musik: <b>Lizenz erlaubt es</b> und die Quelle ist genannt?</li>
      <li>☐ Keine <b>privaten Daten</b> sichtbar (Chats, Namen, Adresse, Kennzeichen)?</li>
      <li>☐ <b>Sichtbarkeit</b> passend gewählt (privat oder nicht gelistet)?</li>
    </ul>
  </div>

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
function ampel(btn, wahl) {
  var s = btn.closest('.szenario');
  s.querySelectorAll('.ampel-btns button').forEach(function (b) { b.classList.remove('sel'); });
  btn.classList.add('sel');
  var e = s.querySelector('.erkl');
  var richtig = s.getAttribute('data-antwort') === wahl;
  e.classList.remove('zu', 'ok', 'nein');
  e.classList.add(richtig ? 'ok' : 'nein');
  s.querySelector('.ergebnis').textContent = richtig ? '✅ Genau!' : '🤔 Nicht ganz –';
}
</script>
"""

html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Praktikum: Handy-Video, Urheberrecht &amp; YouTube</title>
<style>{css}</style>
</head>
<body>{body}</body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(html)
print("geschrieben:", OUT, len(html))
