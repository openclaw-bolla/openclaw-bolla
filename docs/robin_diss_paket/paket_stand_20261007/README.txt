KORREKTURPAKET FÜR DISSERTATION UND PAPER (Robin Mandel)

Inhalt dieses Ordners
- README.txt                 diese Anleitung
- korrekturen.json           die Korrekturaufträge (68 mit modus "auto", 14 mit modus "frage_robin")
- apply_korrekturen.py       das Skript, das die Aufträge anwendet
Dazu gehört die Word-Datei "Dissertation_Paper_Rechtschreibung_Grammatik.docx" (erklärt jeden Punkt mit Fundstelle).

Was gebraucht wird
- Python 3 und die Bibliothek python-docx:  pip install python-docx
- Die beiden Originaldateien im selben Ordner:
  01_Paper_EN_Mandel_CSA-AKI_Manuscript.docx
  03_Dissertation_EN_Mandel_CSA-AKI.docx
- Microsoft Word (für den letzten Schritt: Verzeichnisse aktualisieren)

Ablauf
1. Sicherung: den Ordner mit den beiden Originalen komplett kopieren. Das Skript verändert die Originale nie, aber Sicherheit schadet nicht.
2. Word-Datei lesen. Die 14 Punkte mit "Robin fragen" (gelb markiert) entscheiden:
   d20 vs./versus, d21 SIRI, d22 und p10 Doppelpunkt im Lancet-Titel, d23 Scholarship/Scholarships,
   p11 Figure 5A/5a, l01 bis l04 Layout der Verzeichnisse (nur alle vier zusammen),
   c01 bis c03 und h01 Lebenslauf (c03 nur zusammen mit c02 und h01).
3. Trockenlauf (ändert nichts):
   python3 apply_korrekturen.py --ordner "<Ordner mit den Originalen>" --ziel "<neuer Ausgabeordner>"
   Jede Zeile muss "OK" melden. Bei "FEHLER" stimmt die Trefferzahl nicht (Text wurde inzwischen geändert):
   diesen Auftrag nicht erzwingen.
4. Anwenden, in EINEM Lauf: alle auto-Aufträge plus die freigegebenen IDs:
   python3 apply_korrekturen.py --ordner "<Originale>" --ziel "<Ausgabeordner>" --anwenden --zusaetzlich d20,d23,l01,l02,l03,l04
   (ohne --zusaetzlich nur die 68 auto-Aufträge). Es entstehen Kopien mit der Endung _korrigiert.docx.
   Wichtig: Jeder Lauf startet bei den Originalen. Darum alles in einem Lauf machen, nicht zwei Läufe nacheinander.
5. In Word die _korrigiert-Dateien öffnen: Strg+A, dann F9, "Gesamtes Verzeichnis aktualisieren" (Inhalts-, Abbildungs- und Tabellenverzeichnis).
6. Änderungen prüfen: Word, Register "Überprüfen", "Vergleichen": Original und korrigierte Datei vergleichen. So sieht man jede Änderung.
7. Selbst erledigen (nicht automatisierbar): gelbe TODO-Platzhalter ausfüllen und Markierung entfernen (Paper: Funding, Acknowledgements; Dissertation: Publikationsangabe auf der Titelseite),
   Datum im Lebenslauf zum Abgabetag anpassen, beim Promotionsbüro klären, ob Adresse, Handynummer, E-Mail und Unterschrift im Lebenslauf der veröffentlichten Fassung stehen dürfen,
   p11 und die doppelt genannte Heatmap (Supplementary Figure S4 / Tabelle S8 und S9) im Paper, Abschnitt 3.5.
8. Zum Schluss kurz durchblättern, dann die Datei an den endgültigen Ort speichern.

Hinweise für einen KI-Assistenten (Jarvis)
- Zuerst den Trockenlauf ausführen und das Ergebnis berichten.
- Aufträge mit modus "frage_robin" nur nach ausdrücklicher Freigabe durch Robin ausführen, jeweils mit --zusaetzlich.
- Nie die Originaldateien überschreiben. Das Skript schreibt nur in den --ziel-Ordner.
- Jeder Auftrag hat "erwartet" (Trefferzahl). Abweichung = Auftrag überspringen und melden.
