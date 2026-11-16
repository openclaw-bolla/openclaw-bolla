---
name: feedback-website-schreibzugriff
description: "Standing-Workflow für schreibenden Website-Zugriff (Login+Klicks+Upload) — Playwright vorhanden, immer erst Freigabe vor Live-Aktion"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dc5bcfc1-3712-4d32-a1d2-fbbb2cf1205b
  modified: 2026-07-22T16:13:24.978Z
---

Wenn Chris will, dass ich auf einer Website nicht nur lese, sondern aktiv etwas tue (einloggen, Formulare
ausfüllen, Dateien hochladen, Beiträge/Mitteilungen posten) — z.B. itslearning-Kurse mit Mitteilungen und
Ressourcen bestücken — gilt ab 18.07.2026 dauerhaft dieses Vorgehen:

1. **Playwright ist vorhanden und voll interaktionsfähig**, nicht nur für Screenshots. Basis-Skript:
   `/home/bolla/workspace/scripts/browser_screenshot.py` (zeigt LD_LIBRARY_PATH-Setup für die extrahierten
   Chromium-Libs unter `browser_libs/extracted/...`). Für echte Interaktion (Login, Klicks, Upload) ein
   neues Skript nach demselben Muster schreiben, aber mit `page.click()`, `page.fill()`,
   `page.set_input_files()` etc. statt nur `page.screenshot()`. **Nicht mehr behaupten, es gäbe kein
   Browser-Tool** — das war am 18.07.26 ein falscher erster Reflex, den Chris korrigiert hat.
2. Zugangsdaten für solche Logins **niemals in Chat oder Git-getrackte Memory-Dateien** schreiben — sofort
   in eine Datei unter `/home/bolla/workspace/config/` ablegen und `chmod 600` setzen (Muster: andere
   Dateien dort wie `cloudflare_token.json`, `gemini_api.json`).
3. Content erstellen (z.B. HTML-Praktikumsdatei) → Login-Skript ausführen → bis kurz vor der eigentlichen
   Veröffentlichungs-/Upload-Aktion alles vorbereiten.
4. **Vor dem eigentlichen Live-Schritt (Posten/Hochladen/Anhängen, das für Dritte sichtbar wird) IMMER
   Freigabe von Chris einholen** — Entwurf/Text zeigen, genau wie beim Mail-Versand
   ([[feedback_mail_freigabe]]). Erst nach "ja" wird tatsächlich gepostet.

**⚠️ Ausnahme bei MP-Anstups (Chris-Korrektur 22.07.2026 abends):** Wenn der Auftrag über die
MP-Anstups-Queue kommt (nicht spontan im Chat), gilt Punkt 4 NICHT — dann im Terminal nur knapp
**informieren, dass ich jetzt arbeite** (kein Vorab-Freigabe-Dialog, kein Entwurf-erst-zeigen-und-warten).
Einfach durchziehen und Ergebnis zeigen. Chris: "wenn das Ergebnis nicht ok wäre können wir das ja auch
nachträglich korrigieren" — bewusst in Kauf genommenes Fehlerrisiko, weil der MP-Anstups-Kanal absichtlich
so leichtgewichtig sein soll. Freigabe-vorher (Punkt 4) bleibt der Standard für spontane Chat-Aufträge
außerhalb dieses Kanals.

**Why:** Chris will ab Schuljahr 26/27 aus mp heraus Aufträge erteilen wie "erstelle eine HTML-Praktikumsdatei
und lade sie mit einem netten Text als Mitteilung in Kurs 1, 2, ... hoch" — das soll ein wiederkehrendes,
eingespieltes Muster werden, nicht jedes Mal neu verhandelt werden. Der 22.07.2026-Test lief bewusst als
Test des Anstups-Prozesses selbst, nicht als scharfer Produktiveinsatz.

**How to apply:** Gilt für JEDE künftige Website mit Login-Bedarf, nicht nur itslearning. Konkrete
itslearning-Details (SSO-Mechanismus, Zugangsdaten-Ort) stehen in [[project_itslearning_automation]].
