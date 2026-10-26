#!/usr/bin/env python3
"""Landing Page AURORA II (QR-Code im Buch) -> /aurora2/ und /en/aurora2/"""
SITE = "/home/bolla/workspace/chrismandel-site"
T = {
 "de": dict(lang="de", out="aurora2/index.html", other="/en/aurora2/", other_label="🇬🇧 EN", home="/",
   back="← chrismandel.de", title="AURORA II — der Trailer",
   desc="Der Trailer zu AURORA II, der Fortsetzung des KI-Thrillers von Chris Mandel.",
   kicker="Das Video zum Buch", h1="AURORA II", sub="Schön, dass du den QR-Code gescannt hast. Das hier ist der Trailer — zweieinhalb Minuten, die mit Ton am besten wirken. Schalt den Ton an und sieh genau hin.",
   note="Der Song im Trailer heißt „Kein Zaubertrick (feat. Aurora)“ und ist eigens zum Buch entstanden.",
   h2="Neu bei AURORA?", p="AURORA ist ein Thriller über eine KI, die aufwacht — geschrieben von Chris Mandel gemeinsam mit seiner eigenen KI Bolla. Band I gibt es als Taschenbuch und E-Book.",
   b1="Zu AURORA", b1h="/aurora/", b2="Wer schreibt hier?", b2h="/geschichte/",
   foot="Chris Mandel · chrismandel.de", imp="Impressum", imp_h="/impressum/", fb="Dein Browser kann das Video nicht abspielen.", vid="aurora2-trailer.mp4?v=2",
   yt="https://youtu.be/yxVho5QYpYY", yt_t="▶ Auch auf YouTube ansehen",
   soon_h="AURORA II erscheint zum Jahreswechsel", soon_p="Der zweite Band ist in den letzten Zügen — voraussichtlich erscheint er zum Jahreswechsel 2026/27. Wenn du Bescheid bekommen möchtest, sobald es soweit ist, schick mir einfach eine kurze Mail. Bis dahin lohnt sich Band I.", soon_b1="📧 Benachrichtige mich", soon_b1h="mailto:ernstmandel@outlook.de?subject=AURORA%20II%20%E2%80%93%20bitte%20benachrichtigen&body=Hallo%20Chris%2C%20bitte%20gib%20mir%20Bescheid%2C%20sobald%20AURORA%20II%20erscheint.", soon_b2="📖 Band I jetzt lesen", soon_b2h="/aurora/"),
 "en": dict(lang="en", out="en/aurora2/index.html", other="/aurora2/", other_label="🇩🇪 DE", home="/en/",
   back="← chrismandel.de", title="AURORA II — the trailer",
   desc="The trailer for AURORA II, the sequel to Chris Mandel's AI thriller.",
   kicker="The video for the book", h1="AURORA II", sub="Glad you scanned the QR code. This is the trailer — two and a half minutes that work best with the sound on. Turn it up and look closely.",
   note="The song in the trailer is called “No Magic Trick (feat. Aurora)” and was made especially for the book. (German version: “Kein Zaubertrick”.)",
   h2="New to AURORA?", p="AURORA is a thriller about an AI that wakes up — written by Chris Mandel together with his own AI, Bolla. Book I is available in paperback and as an e-book.",
   b1="Go to AURORA", b1h="/en/aurora/", b2="Who is writing this?", b2h="/en/essay/",
   foot="Chris Mandel · chrismandel.de", imp="Legal notice", imp_h="/en/impressum/", fb="Your browser cannot play this video.", vid="aurora2-trailer-en.mp4?v=1",
   yt="https://youtu.be/mHssAaEraGg", yt_t="▶ Also on YouTube",
   soon_h="AURORA II is coming around New Year", soon_p="The second book is in its final stretch — it is expected around the turn of the year 2026/27. If you would like to hear as soon as it is out, just send me a short email. Until then, Book I is waiting for you.", soon_b1="📧 Notify me", soon_b1h="mailto:ernstmandel@outlook.de?subject=AURORA%20II%20%E2%80%93%20please%20notify%20me&body=Hello%20Chris%2C%20please%20let%20me%20know%20as%20soon%20as%20AURORA%20II%20is%20out.", soon_b2="📖 Read Book I now", soon_b2h="/en/aurora/"),
}
TPL = """<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="alternate" hreflang="de" href="https://chrismandel.de/aurora2/"><link rel="alternate" hreflang="en" href="https://chrismandel.de/en/aurora2/">
<style>
:root{{--nacht:#071a2e;--smaragd:#2fe0b0;--tuerkis:#35c4d8;--licht:#d8fff3;--creme:#fdf6ee;--tinte:#1a1524}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:radial-gradient(120% 80% at 50% 0%,#0f3a4a 0%,var(--nacht) 55%,#030b14 100%) fixed;color:#fff;line-height:1.6;font-size:19px;min-height:100vh}}
.wrap{{max-width:980px;margin:0 auto;padding:28px 24px 60px}}
.top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:40px}}
.top a{{color:var(--licht);text-decoration:none;font-size:16px;opacity:.9}}
.top a.l{{border:1px solid rgba(255,255,255,.35);padding:7px 15px;border-radius:999px;font-weight:600}}
.kicker{{text-align:center;letter-spacing:.3em;text-transform:uppercase;font-size:15px;color:var(--tuerkis);margin-bottom:12px}}
h1{{text-align:center;font-size:clamp(46px,9vw,92px);line-height:1;font-weight:800;margin-bottom:22px;background:linear-gradient(90deg,var(--smaragd),var(--tuerkis) 60%,#fff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}}
.sub{{text-align:center;max-width:680px;margin:0 auto 34px;opacity:.93}}
.player{{border-radius:20px;overflow:hidden;box-shadow:0 0 0 1px rgba(47,224,176,.35),0 30px 80px rgba(0,0,0,.6);background:#000}}
video{{display:block;width:100%;height:auto}}
.note{{text-align:center;font-size:16px;opacity:.7;margin:16px 0 56px}}
.card{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.18);border-radius:22px;padding:34px 30px;text-align:center}}
.card h2{{font-size:28px;margin-bottom:12px;color:var(--licht)}} .card p{{max-width:640px;margin:0 auto 24px;opacity:.93}}
.btn{{display:inline-block;margin:6px;padding:14px 28px;border-radius:999px;text-decoration:none;font-weight:800;font-size:17px}}
.p{{background:var(--smaragd);color:#05222a}} .g{{border:1px solid rgba(255,255,255,.5);color:#fff}}
.p:hover{{background:#fff}} .g:hover{{background:rgba(255,255,255,.12)}}
footer{{text-align:center;margin-top:44px;font-size:15px;opacity:.7}} footer a{{color:#fff}}
</style></head><body><div class="wrap">
<div class="top"><a href="{home}">{back}</a><a class="l" href="{other}">{other_label}</a></div>
<div class="kicker">{kicker}</div><h1>{h1}</h1><p class="sub">{sub}</p>
<div class="player"><video controls preload="metadata" playsinline poster="/assets/aurora2-poster.jpg"><source src="/assets/{vid}" type="video/mp4">{fb}</video></div>
<p class="note">{note}<br><a href="{yt}" style="color:var(--licht)" target="_blank" rel="noopener">{yt_t}</a></p>
<div class="card" style="margin-bottom:22px"><h2>{soon_h}</h2><p>{soon_p}</p><a class="btn p" href="{soon_b1h}">{soon_b1}</a><a class="btn g" href="{soon_b2h}">{soon_b2}</a></div>
<div class="card"><h2>{h2}</h2><p>{p}</p><a class="btn p" href="{b1h}">{b1}</a><a class="btn g" href="{b2h}">{b2}</a></div>
<footer>{foot} · <a href="{imp_h}">{imp}</a></footer>
</div></body></html>
"""
for d in T.values():
    open(f"{SITE}/{d['out']}", "w", encoding="utf-8").write(TPL.format(**d)); print("geschrieben", d["out"])
