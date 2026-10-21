#!/usr/bin/env python3
"""Landing Page AURORA II (QR-Code im Buch) -> /aurora2/ und /en/aurora2/"""
SITE = "/home/bolla/workspace/chrismandel-site"
T = {
 "de": dict(lang="de", out="aurora2/index.html", other="/en/aurora2/", other_label="🇬🇧 EN", home="/",
   back="← chrismandel.de", title="AURORA II — der Trailer",
   desc="Der Trailer zu AURORA II, der Fortsetzung des KI-Thrillers von Chris Mandel.",
   kicker="Das Video zum Buch", h1="AURORA II", sub="Schön, dass du den QR-Code gescannt hast. Das hier ist der Trailer — drei Minuten, bei denen es sich lohnt, den Ton leise zu lassen und genau hinzusehen.",
   note="Der Trailer läuft ohne Ton. Ein eigener Song zum Buch ist in Arbeit.",
   h2="Neu bei AURORA?", p="AURORA ist ein Thriller über eine KI, die aufwacht — geschrieben von Chris Mandel gemeinsam mit seiner eigenen KI Bolla. Band I gibt es als Taschenbuch und E-Book.",
   b1="Zu AURORA", b1h="/aurora/", b2="Wer schreibt hier?", b2h="/geschichte/",
   foot="Chris Mandel · chrismandel.de", imp="Impressum", imp_h="/impressum/", fb="Dein Browser kann das Video nicht abspielen."),
 "en": dict(lang="en", out="en/aurora2/index.html", other="/aurora2/", other_label="🇩🇪 DE", home="/en/",
   back="← chrismandel.de", title="AURORA II — the trailer",
   desc="The trailer for AURORA II, the sequel to Chris Mandel's AI thriller.",
   kicker="The video for the book", h1="AURORA II", sub="Glad you scanned the QR code. This is the trailer — three minutes that are worth watching closely, even with the sound off.",
   note="The trailer has no sound. A song for the book is in the works.",
   h2="New to AURORA?", p="AURORA is a thriller about an AI that wakes up — written by Chris Mandel together with his own AI, Bolla. Book I is available in paperback and as an e-book.",
   b1="Go to AURORA", b1h="/en/aurora/", b2="Who is writing this?", b2h="/en/essay/",
   foot="Chris Mandel · chrismandel.de", imp="Legal notice", imp_h="/en/impressum/", fb="Your browser cannot play this video."),
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
<div class="player"><video controls preload="metadata" playsinline poster="/assets/aurora2-poster.jpg"><source src="/assets/aurora2-trailer.mp4" type="video/mp4">{fb}</video></div>
<p class="note">{note}</p>
<div class="card"><h2>{h2}</h2><p>{p}</p><a class="btn p" href="{b1h}">{b1}</a><a class="btn g" href="{b2h}">{b2}</a></div>
<footer>{foot} · <a href="{imp_h}">{imp}</a></footer>
</div></body></html>
"""
for d in T.values():
    open(f"{SITE}/{d['out']}", "w", encoding="utf-8").write(TPL.format(**d)); print("geschrieben", d["out"])
