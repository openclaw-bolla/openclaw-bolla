---
name: feedback-technische-fakten-verifizieren
description: Technische/vergleichende Behauptungen über Drittprodukte (Fähigkeiten, Rechtskonformität) vor dem Schreiben in Dokumente per Recherche verifizieren, nicht aus dem Gedächtnis behaupten
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-09-22T10:34:59.791Z
---

**Regel:** Technische Fähigkeits- oder Rechtskonformitäts-Behauptungen über Drittprodukte/-firmen (z.B.
„X kann das nicht, Y schon", „Firma A hat DSGVO akzeptiert, Firma B nicht") NICHT aus dem Gedächtnis in
Dokumente schreiben, die verteilt werden — erst per Websuche verifizieren, besonders bei
Vergleichsaussagen zwischen konkurrierenden Anbietern.

**Why:** 19.08.2026 — PS-Ergänzung zur Elterninfo-MS-Konto.html (Copilot vs. Duck.ai/AIS.chat) enthielt
zwei unverifizierte, falsche Behauptungen: (1) „Duck.ai kann keine Bilder" — stimmt nicht, Duck.ai hat
seit Ende 2025 Bildgenerierung (sogar mit durchdachtem Datenschutz: anonymisierte Prompts, lokale
Speicherung). (2) „Microsoft hat DSGVO akzeptiert, OpenAI (hinter Duck.ai) nicht" — auch falsch, OpenAI
hat seit 01.01.2026 einen eigenen DPA über die irische Tochtergesellschaft, DSGVO gilt ohnehin
extraterritorial für jeden Anbieter mit EU-Nutzern. Dazu ein dritter, subtilerer Fehler: „Copilot braucht
kein Login-Ritual" — in Chris' TATSÄCHLICHEM Klassenkontext (geteilte Schul-PCs, siehe
[[reference_edv_klassenausstattung]]) ist ein Konto-Tool sogar ein ZUSÄTZLICHER Abmelde-Aufwand, den ich
aus vorhandenem Kontext-Wissen hätte ableiten müssen, statt eine generische Konto-Bequemlichkeit zu
unterstellen. Chris hat alle drei Punkte in einer Antwort korrigiert — geht davon aus, dass technische
Aussagen in einem an Eltern verteilten Dokument stimmen.

**Unterschied zu [[feedback_keine_erfindungen]]:** Jene Regel gilt für erfundene Fakten ÜBER CHRIS
(Biografie, Handlungen). Diese hier gilt für unverifizierte technische/rechtliche Behauptungen über
DRITTPRODUKTE — beide Fehlerarten kommen aus derselben Wurzel (Behaupten statt Prüfen), verdienen aber
getrennte Erinnerung, weil der Verifikationsweg unterschiedlich ist (Memory-Check vs. Websuche).

**How to apply:**
- Vor jeder Vergleichsaussage zwischen Produkten/Anbietern („X kann/darf/hat ... Y nicht") in einem
  Dokument, das verteilt wird: WebSearch mit aktuellem Jahr, bevor geschrieben wird — nicht danach als
  Nachbesserung.
- Bei Aussagen zu geteilten Geräten/Infrastruktur (Schul-PCs, gemeinsame Accounts): bestehenden
  Kontext im Memory prüfen ([[reference_edv_klassenausstattung]], [[project_schuljahr2627]]), bevor eine
  generische "das ist bequemer"-Behauptung reinrutscht.
- Gilt besonders bei DSGVO-/Datenschutz-Aussagen — hohes Fehlerpotenzial, hohe Sichtbarkeit (Elterndokumente),
  und die Rechtslage ändert sich; nie aus altem Wissen zitieren ohne aktuellen Check.

**Ergänzung 22.09.2026 — WebSearch ist auch nur eine Quelle, kein Beweis:** Bei `05-Praktikum.html`
behauptet, bing.com/create verlange inzwischen ein Konto (MS/Google/Apple) — gestützt auf eine
WebSearch-Zusammenfassung. Chris hat live getestet: **bing.com/create geht bei ihm weiterhin ohne
Konto**, sogar mit MAI-2.5-Flash. Reaktion: „schon wieder eine ungeprüfte Aussage — bitte stelle das
ab." Web-Suchtreffer zu schnelllebigem Konsumentenprodukt-Verhalten (Login-Wände, Kontingente, A/B-Tests,
Region/Account-abhängig) können veraltet, regional unterschiedlich oder schlicht falsch sein — eine
WebSearch-Zusammenfassung ist eine Quelle, keine Bestätigung. **How to apply:** Bei genau so einer
Kategorie von Behauptung (Login-Pflicht/Limits/Verfügbarkeit einer Konsumenten-Webseite, die Chris in
40 Sekunden selbst aufrufen kann) das Ergebnis als „laut Websuche, Stand check das aber selbst" kennzeichnen
statt als Fakt zu präsentieren — oder, wenn möglich, direkt per WebFetch die Seite selbst prüfen statt nur
Suchtreffer-Zusammenfassungen zu zitieren.
