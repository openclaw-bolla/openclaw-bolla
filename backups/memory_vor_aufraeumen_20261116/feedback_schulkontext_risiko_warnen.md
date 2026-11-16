---
name: feedback-schulkontext-risiko-warnen
description: "Bei Unterrichtsmaterial/Empfehlungen, die mit SH-Schuldatenschutz oder der Landes-Open-Source-Linie kollidieren könnten, VOR dem Austeilen proaktiv warnen — Anlass: Schulleiterin rüffelte am 28.08.2026 das MS-Konto-Elterninfo"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f33aa78b-a989-4d4b-85b1-d6c39f5e398a
  modified: 2026-08-28T11:05:00.000Z
---

Wenn Chris in seiner Lehrer-Rolle etwas plant, das an Schüler oder Eltern rausgeht — Handout,
Elterninfo, „prakt XXX"-Anleitung ([[feedback_prakt_anleitungen]]), Tool-Empfehlung, itslearning-Post —
und darin **ein Drittanbieter-Konto, ein Cloud-Dienst, ein US-Anbieter, ein KI-Tool oder die
Verarbeitung personenbezogener Schülerdaten** vorkommt: **vor dem Fertigstellen/Austeilen kurz das
Risiko benennen** und die konforme Alternative gleich mit anbieten ([[reference_ais_chat]] = AIS.chat,
kontofreie Tools). Nicht erst abwarten, bis jemand aus der Schulleitung reagiert.

**Anlass (28.08.2026):** Chris hatte am ~25.08. das Blatt
`02-Elterninfo-MS-Konto.html/.pdf` austeilen lassen — ein bewusst vorsichtig formuliertes,
ausdrücklich **freiwilliges** Microsoft-Konto für Copilot (keine personenbezogenen Daten in MS 365,
kontofreie Alternative genannt). Die Schulleiterin hat ihm geschrieben, das verstoße „gegen das
Schulgesetz, die Datenschutzverordnung und die grundsätzliche Ausrichtung des Landes SH, sich in allen
Behörden von Microsoft zu lösen". Chris hat sofort mit ihr telefoniert — sie ist **nicht sauer**,
sieht auch die Schwächen von AIS.chat, verlangt aber die **Rücknahme der Empfehlung** mit Verweis auf
die Landesausrichtung. Bolla hat den Widerruf als 1-Seiten-PDF erstellt
(`02-Widerruf-MS-Konto.html/.pdf`, gleicher Verteilweg).

**Rechtslage — nüchtern (recherchiert 28.08.2026):**
- **Kein Paragraf verbietet wörtlich**, dass eine Lehrkraft ein (freiwilliges) Microsoft-Konto
  erwähnt. Die Schulleiterin kombiniert drei Ebenen:
  1. **Schulgesetz SH §§ 30–32** (Verarbeitung von Daten) + **Schul-Datenschutzverordnung (SchulDSVO)**
     — allgemeine Rahmennormen; § 30 Abs. 1 SchulG: Datenverarbeitung nur soweit zur Aufgabenerfüllung
     erforderlich. SchulDSVO § 12: externe Dienstleister nur mit AV-Vertrag + Vorprüfung, Verantwortung
     bei der Schulleitung. § 2 SchulDSVO: **alle**, die mit personenbezogenen Daten arbeiten, tragen
     Verantwortung.
  2. **Schuldatenschutz-FAQ des Bildungsministeriums** (schuldatenschutz.schleswig-holstein.de) — die
     konkrete verwaltungsinterne Auslegung: „Office 365/Microsoft 365 darf für die Verarbeitung
     personenbezogener Daten nicht verwendet werden"; bei US-Anbietern sei trotz
     Angemessenheitsbeschluss (Data Privacy Framework, Juni 2023) davon auszugehen, dass die
     Voraussetzungen für datenschutzkonforme Nutzung nicht uneingeschränkt erfüllt sind.
  3. **Politische Grundsatzlinie**: Kabinettsbeschluss vom **3. April 2024**, Digitalminister Dirk
     Schrödter, „Einstieg in den Umstieg" — Open-Source-Strategie der Landesverwaltung (MS Office →
     LibreOffice, Windows → Linux, SharePoint/Outlook → Nextcloud + Open-Xchange/Thunderbird,
     Active Directory → Open-Source-Verzeichnisdienst). Dokumentiert auf schleswig-holstein.de
     (Medieninformationen der Staatskanzlei); Stand Dez. 2025 ~80 % der Verwaltungs-Arbeitsplätze auf
     LibreOffice. **Wichtig:** die veröffentlichten Dokumente beziehen sich ausdrücklich auf die
     ~30.000 Landesbediensteten der Verwaltung — sie sagen **nicht**, dass der Beschluss formal für
     Schulen/Schüler gilt. Für Schulen: Handreichung „KI@Schule SH" + Landesdienst AIS.chat als
     bereitgestellte, DSGVO-konforme Lösung.
- **Fazit für Chris:** Er hat nicht „gegen ein Gesetz verstoßen" im engen Sinn; datenschutzrechtlich
  war das Blatt sauber abgesichert. Reibung entsteht am **politischen Signal** („die Schule empfiehlt
  Microsoft", während das Land das Gegenteil kommuniziert) und daran, dass die Schulleitung die
  Gesamtverantwortung trägt und das anweisen darf.

**Why:** Chris will keine zweite solche Situation. Er ist im Ruhestand freiwillig an der Schule, will
keinen Ärger mit der Leitung und keine Blätter zurückrufen müssen. Bolla soll den Riecher dafür
mitbringen, bevor Material rausgeht.

**How to apply:**
- Bei jeder Schüler-/Elternausgabe mit Konto/Cloud/US-Anbieter/KI/personenbezogenen Daten: **einen
  Satz Warnung** vor Fertigstellung („Achtung: geht Richtung Microsoft/US-Cloud — kollidiert mit der
  SH-Open-Source-Linie, sollen wir stattdessen AIS.chat/kontofrei nehmen?").
- Default für den KI-Teil des EDV-Unterrichts ist ab jetzt **AIS.chat** bzw. **kontofreie Tools** —
  Microsoft-Konto / Copilot-mit-Login nicht mehr als Weg empfehlen (überschreibt insoweit die
  Copilot-mit-Konto-Pfade in [[feedback_praktikum_geraete_check]] und
  [[reference_ms_konto_ohne_outlook]]).
- Gilt für den Schulkontext. Chris' privates Microsoft-Ökosystem (Outlook, M365) ist davon nicht
  berührt.

---

## Erweiterung 28.08.2026 — „MS-Weckruf": offensive Microsoft-Werbung raus aus allen Unterrichtsmaterialien

Chris hat den Vorfall als **Weckruf** verstanden und will es für die **restlichen Kurstage des Schuljahrs
26/27** berücksichtigt haben. Neue, feste Regel:

- **Vor JEDEM neuen PDF / jeder „prakt XXX"-Anleitung** ([[feedback_prakt_anleitungen]]): den Entwurf
  aktiv auf **offensive Microsoft-Bewerbung** durchsehen und **vor der Erzeugung** rausnehmen. Nicht nur
  Konten/Cloud (Ausgangsregel oben), sondern jedes „nutzt am besten Tool X von Microsoft", Logos,
  Anmelde-Anpreisungen, „gratis dazu"-Bonus-Absätze etc.
- **Alternativen mitliefern:** Wenn ein Material bisher auf ein MS-Tool gesetzt hat, Chris beim Planen
  des Kurstags **konkrete Ersatz-/Neutral-Optionen vorschlagen** (kontofrei, plattformneutral, oder die
  SH-Landeslösung).
- **Wissen NICHT vorenthalten:** Die Schüler sollen Copilot, Clipchamp & Co. weiterhin **kennenlernen**
  (reale, verbreitete Werkzeuge) — nur **sachlich/neutral eingeordnet**, nicht offensiv beworben. Grenze:
  „darüber informieren" ✅ vs. „dazu drängen/anpreisen" ❌.
- **Betroffene Kurstage konkret:** **Kurstag 5 und 6** (wieder Copilot bzw. Clipchamp) —
  `05-Basics Office - WebApps-Designer-Copilot.pptx` und der Clipchamp-Kurstag. Beim Planen dieser
  Kurstage entschärfen + Alternativen anbieten.
- **Timing:** Am 28.08. wurde **nur die Regel festgehalten**, KEINE inhaltliche Diskussion/Umbau. Die
  Diskussion über konkrete Alternativen findet **erst statt, wenn Chris den jeweiligen Kurstag plant**.
- **Kurstag 3** (Tastatur, `03-Praktikum.html` / `03-Basics Office - Tastatur.pptx`) läuft heute
  (28.08.), Wiederholung in den anderen Klassen nächste Woche. Chris will, dass ich das Material
  **nächste Woche in diesem Sinn checke** (MS-Werbung raus) — offener To-do in [[aktuell]].

**Why:** Nach dem Schulleiterinnen-Rüffel will Chris jeden weiteren Konflikt vermeiden und die
SH-Open-Source-Linie im Unterricht sichtbar mittragen — ohne den Schülern praxisrelevantes Wissen über
gängige Tools zu verweigern.

## Präzisierung 28.08.2026 — Mail-Antwort Schulleiterin (Marika Peters, Marika.Peters@schule.landsh.de)

Frau Peters hat Chris' Nachfrage per Mail an ernstmandel@outlook.de beantwortet (Betreff „AW: MS
Account Widerruf Mandel", 28.08. 10:26). Kernaussagen — **verbindlich**:

- **Nur AIS.chat im Unterricht.** „Laut Aussagen der Fortbilder zu AIS darf nur dieses Portal im
  Unterricht genutzt werden, also **auch kein Duck.ai**." → Duck.ai (und jedes andere externe
  KI-Tool) ist damit **nicht erlaubt**. Meine frühere Einschätzung „Duck.ai als kontofreier Fallback,
  vorher abklären" ist damit erledigt: **nein**.
- **AIS.chat-Zugang für Schüler:** Es gibt **keine Klassenkonten**. Chris muss zuerst eine
  **Fortbildung** machen, bekommt dann über das **Schulportal SH** einen Zugang und gibt den Schülern
  über **Token** Zugang. Für seine 7. Klassen ist AIS.chat also **noch nicht eingerichtet** — bis er
  die Fortbildung gemacht + Tokens verteilt hat, gibt es im Unterricht **kein** KI-Tool.
- **Widerruf-Blatt:** „grundsätzlich gern so herausgeben", aber ergänzen um einen Hinweis auf die
  **Datenschutzverordnung** (dass danach kein Microsoft-Konto / kein externer Dienst außer AIS.chat
  zulässig ist). → In `02-Widerruf-MS-Konto.html` + `-sw.html` am 28.08. eingebaut (Absatz „Hinzu
  kommt: Nach den geltenden Datenschutzvorgaben …"), „kontofreie Alternative" aus dem Blatt entfernt.
  PDFs neu erzeugt, liegen in `Desktop\temp` zur Freigabe.

**How to apply:** Für den EDV-Unterricht ab jetzt: einziges *erlaubtes* KI-Tool wäre **AIS.chat** —
kein Duck.ai, kein Copilot-mit-Login, kein anderes externes Tool.

## Entscheidung Chris 28.08.2026 — gar kein KI-Tool im Praktikum, aber KI bleibt Thema

Chris **wird AIS.chat nicht nutzen** (Gründe vielfältig, nicht weiter ausgeführt). Damit:

- **Kein KI-Werkzeug in den Hands-on-Übungen** der 7er — die praktischen Klick-Aufgaben laufen ganz
  ohne KI-Chatbot. Kurstag 5 (Copilot) und 6 (Clipchamp): die Copilot-/KI-**Benutzung durch Schüler**
  fällt komplett weg (nicht nur „nicht bewerben" — ganz raus), Ersatzaufgabe beim Planen finden.
- **KI als Unterrichts-THEMA bleibt** und ist ausdrücklich erwünscht (Handreichung „KI@Schule SH" des
  Landes). Erlaubt: darüber sprechen (Was ist KI, Sprachmodelle, Chancen/Risiken, Halluzinationen,
  Urheberrecht, Datenschutz, KI-Kompetenz) und dass **Chris selbst** vorne etwas vorführt
  (eigenes Gerät / Screenshots / AIS.chat-Lehrkraftzugang). Verboten ist nur die **aktive Nutzung
  durch die Schüler** eines externen Tools.
- Für die Elterninfo/Widerruf sauber formuliert als „die praktischen Übungen kommen ohne KI-Chatbot
  aus" — nicht „wir sprechen nicht über KI".

Details AIS.chat-Zugang (falls doch mal relevant): [[reference_ais_chat]].
