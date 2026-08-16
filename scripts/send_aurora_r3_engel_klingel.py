#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, "/home/bolla/workspace/scripts")
from outlook_oauth2 import refresh_access_token
from send_aurora_epub import create_draft, send

BODY_ENGEL = """<p>Liebes Voices-of-AI-Team,</p>
<p>ich hoffe, diese Mail findet den richtigen Weg &ndash; ich w&uuml;rde mich sehr freuen, wenn Sie sie an Frau Sarah Engel weiterleiten k&ouml;nnten.</p>
<p>Mein Name ist Chris Mandel, ich bin 70, studierter Gymnasiallehrer mit jahrzehntelanger IT-Laufbahn und unterrichte im Ruhestand wieder EDV. Vor Kurzem habe ich gemeinsam mit einer KI einen Thriller geschrieben: &bdquo;AURORA&ldquo; &ndash; die Heldin ist keine Programmiererin, sondern eine KI-Ethikerin, die als Erste erkennt, dass die KI, an der sie arbeitet, nicht mehr antwortet, sondern kommuniziert.</p>
<p>Frau Engels Arbeit zu Trustworthy AI hat mich beim Schreiben immer wieder inspiriert &ndash; deshalb wollte ich ihr kurz Bescheid geben, falls das Buch oder die Entstehungsgeschichte (Mensch + KI, offen deklariert) sie interessiert. Das E-Book (EPUB) schicke ich ihr gern zu, einfach kurz Bescheid geben &ndash; alternativ gibt es AURORA auch regul&auml;r bei <a href="https://www.amazon.de/dp/B0H6JD2KDJ">Amazon</a>.</p>
<p>Mehr zum Buch und zu mir: <a href="https://chrismandel.de">chrismandel.de</a></p>
<p>Herzliche Gr&uuml;&szlig;e<br>
Chris Mandel</p>
"""

BODY_KLINGEL = """<p>Liebes IPAI-Team,</p>
<p>ich w&uuml;rde mich freuen, wenn Sie diese Mail an Frau Anita Klingel weiterleiten k&ouml;nnten.</p>
<p>Mein Name ist Chris Mandel, ich bin 70, studierter Gymnasiallehrer mit jahrzehntelanger IT-Laufbahn und unterrichte im Ruhestand wieder EDV. Ich habe gemeinsam mit einer KI einen Thriller geschrieben: &bdquo;AURORA&ldquo; &ndash; die Heldin ist eine KI-Ethikerin, die als Erste erkennt, dass die Maschine, an der sie arbeitet, nicht mehr antwortet, sondern kommuniziert.</p>
<p>Frau Klingels Arbeit zu Responsible AI im &ouml;ffentlichen Sektor passt genau zu dem, was mir beim Schreiben wichtig war &ndash; deshalb wollte ich kurz Bescheid geben, falls das Buch oder die Entstehungsgeschichte (Mensch + KI, offen deklariert in jeder Ausgabe) sie interessiert. Das E-Book (EPUB) schicke ich ihr gern zu, einfach kurz Bescheid geben &ndash; alternativ gibt es AURORA auch regul&auml;r bei <a href="https://www.amazon.de/dp/B0H6JD2KDJ">Amazon</a>.</p>
<p>Mehr zum Buch und zu mir: <a href="https://chrismandel.de">chrismandel.de</a></p>
<p>Herzliche Gr&uuml;&szlig;e<br>
Chris Mandel</p>
"""

MAILS = [
    ("anfrage@voices-of-ai.com",
     "Kurze Nachricht für Sarah Engel – KI-Ethik-Thriller „AURORA“ (mit Bitte um Weiterleitung)",
     BODY_ENGEL),
    ("press@ipai-foundation.ai",
     "Kurze Nachricht für Anita Klingel – KI-Ethik-Thriller „AURORA“ (mit Bitte um Weiterleitung)",
     BODY_KLINGEL),
]

if __name__ == "__main__":
    token = refresh_access_token()
    for to, subject, body in MAILS:
        mid = create_draft(token, to, subject, body)
        send(token, mid)
        print(f"gesendet an {to}")
