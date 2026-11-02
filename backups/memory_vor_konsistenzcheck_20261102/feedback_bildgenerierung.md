---
name: feedback-bildgenerierung
description: "Bildgenerierung für Covers und MC immer Pollinations.ai — kostenlos, kein API-Key nötig"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6f7a5017-294d-4876-8441-7eca934fd61a
  modified: 2026-08-17T11:28:04.817Z
---

Für Cover-Generierung (Suno) und alle anderen Bildaufgaben immer **Pollinations.ai** verwenden, nicht Gemini Image API.

**Why:** Pollinations ist kostenlos und kein API-Key nötig. Gemini kostet Geld. Explizit so vereinbart.

**How to apply:** URL: `https://image.pollinations.ai/prompt/{encoded_prompt}?width=3000&height=3000&nologo=true&enhance=true`  
⚠️ **Stand 01.07.2026:** Pollinations liefert aktuell IMMER nur **768×768** — egal was bei width/height steht (auch `model=flux` ändert nichts). Also für Release-Cover (Suno/DistroKid = 3000×3000 Pflicht) IMMER mit Pillow hochskalieren: `im.resize((3000,3000), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2.5,percent=120,threshold=2))` — die UnsharpMask fängt den 3,9×-Upscale sichtbar ab (illustrative/Pop-Art-Motive vertragen das gut, Fotos weniger). Nativ hochauflösend ginge nur über einen kostenpflichtigen Dienst (PiAPI [[reference_piapi]], oder MAI-Image-2 [[project_mai_image2]] sobald da).  
Einzige Ausnahme: wenn Pollinations down ist und Qualität kritisch — dann erst fragen.

## ⚠️ Anatomie-Fehler bei Personen/dynamischen Posen (Lehre 10.08.2026)
Pollinations (Diffusionsmodell) patzt öfter bei Menschen in Bewegungsposen (Sprung, überlappende Gliedmaßen) — z.B. fehlendes Bein bei "Back In Session"-Cover. Lässt sich NICHT zuverlässig per Prompt-Wortwahl allein verhindern (systemische Modellschwäche), aber zwei Dinge helfen:
1. Im Prompt explizit ergänzen: „anatomically correct proportions, two arms two legs clearly visible, correct human anatomy"
2. **Immer mehrere Seeds parallel generieren** (z.B. `&seed=7`, `&seed=21`, `&seed=99` an die URL anhängen) und die sauberste Variante auswählen — kostenlos, also kein Grund, sich mit dem ersten Treffer zufriedenzugeben. Bei Motiven mit Personen in Bewegung das ab jetzt standardmäßig so machen (3 Kandidaten ziehen, prüfen, beste hochskalieren), ohne dass Chris das anstoßen muss.

## ✅ MAI-Image-2.5 als Fallback freigegeben (Chris, 10.08.2026)
Wenn **3 Pollinations-Versuche** (egal ob wegen Anatomie-Fehlern, Stil passt nicht, o.ä.) nicht zum gewünschten Ergebnis führen: automatisch auf **MAI-Image-2.5** (Azure AI Foundry) wechseln, OHNE nochmal extra nachzufragen — pauschal freigegeben, gilt dauerhaft ab jetzt. Trotzdem bei jedem Einsatz kurz die Kosten nennen (Transparenz), aber nicht extra um Erlaubnis bitten.

**How to apply:** `POST http://127.0.0.1:18790/api/bildgen` mit `{"prompt": "...", "model": "mai-image-2.5", "aspect_ratio": "1:1"}` — liefert `image_b64` (PNG, 1024×1024, native Qualität deutlich besser bei Fotorealismus/Anatomie als Pollinations). Kosten automatisch verbucht (`kosten_ledger_add`), ~0,10€/Bild ([[project_mai_image2]]). Für 3000×3000-Release-Cover trotzdem mit Pillow hochskalieren (Ausgangsqualität ist aber höher, daher sanftere UnsharpMask reicht: `percent=80` statt `120`).

**Erster erfolgreicher Fall:** "Back In Session"-Cover — Pollinations lieferte bei Sprung-/Bewegungsposen wiederholt Anatomie-Fehler (auch fotorealistisch), MAI-Image-2.5 traf mit einem Versuch (stehende Pose, Gegenlicht, fliegende Hefte/Stifte) sauber.

**⚠️ Lehre 13.08.2026 — MAI proaktiv, nicht erst auf Nachfrage:** Bei "Wonderfully Scattered" 3 Pollinations-Versuche verbraten (einer davon unbrauchbar sexualisiert!) BEVOR an MAI gedacht wurde — Chris musste explizit nachfragen ("hattest du vergessen, dass wir Zugang haben?"). Die Freigabe oben ("nach 3 Pollinations-Versuchen automatisch MAI, ohne nachzufragen") gilt UNEINGESCHRÄNKT — bei jedem Cover-Auftrag von Anfang an mitdenken, dass MAI verfügbar ist, und spätestens nach dem zweiten enttäuschenden Pollinations-Ergebnis selbst wechseln, nicht auf Ansage warten.

**Konkretes Prompt-Muster, das gut funktioniert hat (MAI 2.5, "Chrome-Herz zerbirst in Konfetti"):** Statt vager abstrakter Begriffe ("light rays", "confetti bursting") ein KONKRETES, einzelnes Hauptmotiv wählen, das visuell zum Songtext passt (hier: "Heart made of confetti"-Zeile aus dem Refrain → glänzendes zerberstendes Chrome-Herz). Für US-Zielgruppe/Spotify-Tauglichkeit explizit "glossy Y2K maximalism, PC Music aesthetic, designed to stop scrolling on Spotify New Music Friday and TikTok feeds" in den Prompt aufnehmen. Traf im ersten Versuch.

**⚠️ Rückfall Nr. 3, 16.08.2026 nachts:** Chris hat in BildGen wieder Pollinations benutzt, "gaaanz schlechtes Ergebnis" — MAI-Image-2.5 stand als Alternative bereit, wurde aber nicht genutzt/vorgeschlagen (gleiches Muster wie die Lehre vom 13.08. oben, zum dritten Mal). **Verschärfung:** In BildGen künftig VOR dem ersten Pollinations-Versuch kurz abwägen (Personen/Bewegung/Fotorealismus → eher MAI), nicht erst reaktiv nach schlechtem Ergebnis wechseln. Chris hat zusätzlich gefragt, ob es inzwischen eine bessere KOSTENLOSE Alternative zu Pollinations gibt — noch unbeantwortete Recherche-Aufgabe für die nächste Session, siehe [[aktuell]].

**✅ Datenpunkt Nr. 4, 02.09.2026 — MAI gewinnt auch bei Bolla-Songs-Covern:** Nach dem Umbau von „🎨 3 Cover-Vorschläge" auf 1× Pollinations + 2× Gemini (Kostengrund: Gemini-Free-Credit weg) hat Chris die drei angesehen, dann den optionalen „🌟 +1 mit MAI" geholt: *„das mai bild war mit abstand das beste :-) habe ich genommen."* Günstigen Mix behält er als Default (bewusste Kostenentscheidung), aber: bei Cover-Aufträgen von vornherein einplanen, dass am Ende eh MAI genommen wird — den „+1 mit MAI"-Weg sichtbar/leicht halten.

## ✅ Cloudflare Workers AI (FLUX) live, 17.08.2026 — neuer kostenloser Standard-Engine-Kandidat für MP

Auf Chris' Recherche-Frage ("kostenlose Alternative zu Pollinations?") hin: **Cloudflare Workers AI** (`@cf/black-forest-labs/flux-1-schnell`) eingebaut und live getestet — echtes kostenloses Kontingent, offizielle API (kein ToS-Risiko wie Bing-Scraping, das Chris bewusst abgelehnt hat wegen Kontosperrungs-Risiko). Qualität im ersten Test (Hund mit Zauberhut, KI-Forum-Sanduhr-Motiv) deutlich besser als der zuletzt "gaaanz schlechte" Pollinations-Output.

**Eingebaut in:**
- **BildGen** (`mission-control/index.html`): neuer vierter Engine-Tab "☁️ Cloudflare" neben Pollinations/Nano Banana/MAI. Ruft `/api/bildgen` mit `model:"cloudflare-flux"` — kein Bild-Upload/Edit (nur Text→Bild), kein `kosten_ledger`-Eintrag (0€).
- **KI-Forum** (`kifPollImage()`): Cloudflare jetzt PRIMÄR (neuer Endpunkt `/api/kiforum/generate-image`), Pollinations nur noch als Fallback falls Cloudflare mal ausfällt.
- Backend-Funktion: `cf_workers_ai_generate()` in `mission_control_api.py` — Token/Account aus `config/cloudflare_token.json` (`account_id` + `api_token`, Scope seit 17.08. um "Workers AI:Edit" erweitert).

**Technische Falle:** `flux-1-schnell` akzeptiert im Cloudflare-Schema NUR `prompt` — `width`/`height` mitschicken wirft Fehler 5006 ("Additional properties not allowed"). Output ist fix ca. 1024×1024 JPEG.

**Nächster Schritt, falls Chris nach etwas Testzeit sagt "Qualität passt nicht":** Plan B ist ein NEUES kostenloses MS-Konto extra für Bing Image Creator (DALL-E 3 + MAI2.5!) — bewusst zurückgestellt, nicht das bestehende Haupt-MS-Konto nutzen (Sperr-Risiko bei automatisiertem Zugriff).

## ⚠️ Prompt-Faustregel ist ENGINE-ABHÄNGIG, nicht universell (Lehre 17.08.2026)

Erst pauschal behauptet "kurze/abstrakte deutsche Prompts sind Schrott, immer ausführlich Englisch schreiben" — Chris hat das direkt widerlegt: sein Original-Prompt "KI unterrichtet 7. Klasse eines Gymnasiums" (kurz, deutsch, abstrakt) lieferte bei **MAI-Image-2.5** ein exzellentes Ergebnis, inkl. korrekt gerendertem deutschen Text im Bild ("KI-Unterricht", Fächerliste, "7c – KI & Gesellschaft", deutsche Schulplakate/Flagge).

**Der Unterschied ist die Modell-Architektur, nicht die Sprache an sich:**
- **FLUX-artige Diffusionsmodelle** (Pollinations, Cloudflare Workers AI) — "malen wörtlich ab", brauchen ausführliche englische Szenenbeschreibung (Motiv+Handlung+Umgebung+Licht+Stil), können praktisch keinen lesbaren Text ins Bild setzen.
- **MAI-Image-2.5** (Azure) — versteht kurze/abstrakte deutsche Prompts, rendert sogar korrekten deutschen Text mit rein. Kostet dafür ~0,10€/Bild.

**How to apply:** Bei der Engine-Wahl/Prompt-Beratung IMMER zuerst fragen: braucht das Bild Text/Beschriftung ODER ist der Prompt kurz/abstrakt/deutsch? → MAI vorschlagen. Ausführliche Szene ohne Textbedarf? → Cloudflare (kostenlos) reicht, dann die ausführliche-Englisch-Faustregel anwenden. Nicht mehr pauschal "Prompt ist schuld" sagen, ohne die Engine zu nennen.

## ✅ "Prompt verbessern"-Feature in BildGen (17.08.2026)

Neuer ✨-Button neben dem BildGen-Prompt-Feld (`mission-control/index.html`, Funktion `bgImprovePrompt()`) — ruft `/api/bildgen/improve-prompt` auf, das per `claude -p` einen rudimentären Nutzer-Prompt in einen starken FLUX-Stil-Prompt umwandelt (Englisch, konkretes Hauptmotiv statt Abstraktion, Szene+Handlung+Umgebung+Licht, Stil-Schlagworte, kein Text/Beschriftung verlangt) und den Text im Feld ERSETZT statt direkt zu generieren — Chris kann vor dem Klick auf "Generieren" noch nachjustieren. Bewusst NUR bei Pollinations/Gemini/Cloudflare sichtbar (Button versteckt sich bei MAI-Tab automatisch, `bgSelectEngine()`), da MAI kurze/deutsche Prompts schon gut versteht (siehe oben). **Explizit NICHT im KI-Forum eingebaut** — dort gibt's kein manuelles Prompt-Feld, Claude generiert den `img_prompt` beim Themen-Erzeugen schon selbst.

**Gleiche Formel auch in KI-Forums `img_prompt`-Erzeugung übernommen:** Die beiden ersten Cloudflare-Bilder im KI-Forum waren spürbar schwächer als in BildGen — Ursache: die Claude-Anweisung für `img_prompt` in `/api/kiforum/generate` und `/api/kiforum/respond` war zu vage ("detaillierter Bildprompt, konkrete Szene"). Auf die gleiche ausführliche Formel wie bei `bgImprovePrompt` umgestellt (konkretes Hauptmotiv, Szene+Handlung+Umgebung+Licht, Stil-Schlagworte am Ende, kein Text/Beschriftung). Live getestet (Testeintrag danach wieder sauber aus `data/kiforum.json` entfernt) — Ergebnis deutlich atmosphärischer/konkreter als vorher, vergleichbar mit BildGen-Qualität.

## 🧮 Kosten-Self-Metering: Cover-Bilder + Terminal-MAI (03.09.2026)

Google/Azure-Rechnungen sind nicht per API-Key abrufbar (Chris: „alles nicht" — einfach mitzählen).
Bolla zählt jeden kostenpflichtigen Bild-Call selbst → `data/api_kosten_ledger.json`,
`kosten_ledger_add(service, betrag, info)` in `mission_control_api.py`. `/api/kosten` rechnet
daraus die Gemini-/Azure-Kacheln im MP-Überblick live hoch (`_kosten_inject_live`).
Preise dort: `GEMINI_IMG_PREIS=0.04`, `MAI_IMG_PREIS=0.10`, `GEMINI_ANALYSE_PREIS=0.0005`.

Gezählt wird bei: `/api/bildgen` **und** (seit 03.09.) `_suno_render_cover_bytes()` = jedes
Bolla-Songs-/DistroKid-Cover (`/api/suno/covers`, `cover-extra`, Publish-Fallback). Pollinations
+ Cloudflare = 0 €, kein Eintrag.

**⭐ Terminal-Regel:** Wenn ich MAI- (oder Gemini-)Bilder **direkt vom Terminal** erzeuge (nicht
über die MC-API), danach `python3 scripts/kosten_add.py mai <n> "Notiz"` aufrufen — sonst fehlen
die im MP-Überblick. `python3 scripts/kosten_add.py --list` zeigt den laufenden Monat.
