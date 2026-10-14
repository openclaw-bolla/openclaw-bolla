#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
from outlook_oauth2 import refresh_access_token
from send_aurora_epub import create_draft, send

TO = "skiffyandfanty@gmail.com"
SUBJECT = "AURORA – a human/AI-co-written thriller about an AI that stops answering and starts communicating"
BODY = """<p>Hello Shaun and Brandon,</p>
<p>My name is Chris Mandel. I'm 70, a trained secondary-school teacher with a decades-long career in IT, now teaching computer science again in retirement. Together with an AI, I wrote a thriller: <b>AURORA</b>. The heroine is not a programmer but an AI ethicist who is the first to realise that the system she works on has stopped merely answering and has started to communicate. The human/AI collaboration is declared openly in every edition.</p>
<p>I know you receive far more books than you can cover, so this is a one-time note, no follow-up. If it sounds like something for the show or the review pile, I'd be glad to send you the EPUB. The English edition is also on Amazon: <a href="https://www.amazon.com/dp/B0H6JQK6JQ">amazon.com/dp/B0H6JQK6JQ</a>.</p>
<p>A sequel, AURORA II, is currently in the writing; I'll gladly let you know if it ever sees the light of day.</p>
<p>More about the book and me: <a href="https://chrismandel.de/en">chrismandel.de/en</a></p>
<p>Kind regards<br>Chris Mandel</p>
"""
if __name__ == "__main__":
    token = refresh_access_token()
    mid = create_draft(token, TO, SUBJECT, BODY)
    send(token, mid)
    print("gesendet an", TO)
