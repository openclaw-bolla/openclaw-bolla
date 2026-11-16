---
name: feedback-mail-html-links
description: "Marketing-/Kontakt-Mails mit Links immer als HTML senden, nicht als Text"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e33550a8-2998-406b-9a09-5373109846bb
  modified: 2026-08-15T17:26:32.624Z
---

Mails mit Links (z.B. Rezensionsexemplar-Antworten, AURORA-Marketing-Outreach) immer mit `"contentType": "HTML"` über Graph senden, mit `<a href="...">Linktext</a>` statt nackter URL im Fließtext.

**Warum:** Bei `contentType: "Text"` bleiben URLs reiner Text — Outlook macht sie beim Empfänger nicht automatisch klickbar. Chris hat das bei der ersten AURORA-Antwortmail (Ethik Digital, 09.07.2026) bemerkt: Links zu chrismandel.de/geschichte und /aurora waren nicht anklickbar.

**Wie anwenden:** Bei jeder neu zu schreibenden Mail (egal ob Ad-hoc-Skript oder bestehendes wie `send_aurora_epub.py`), die eine URL enthält, HTML-Body mit `<p>`-Absätzen und `<a href>`-Tags bauen statt Klartext-Body. `send_aurora_epub.py` ist bereits umgestellt (09.07.2026). Bei künftigen Ad-hoc-Antwort-Skripten (z.B. per `createReply`) dasselbe Muster verwenden.

**⚠️ Rückfall 13.08.2026:** Bei den ersten beiden AURORA-Sichtbarkeits-Mails des Tages (Anthropic-Presse, Mads Pankow) trotzdem `send_text_mail.py` (reiner Text) benutzt, weil es das griffbereite Standard-Skript für schnelle Mails ist — Website-Link dort vermutlich nicht klickbar angekommen, nicht mehr reparierbar. **`send_text_mail.py` ist NUR für Mails ganz ohne Links gedacht** (kurze Statusmeldungen etc.) — sobald eine URL im Text vorkommt, IMMER HTML-Body von Hand bauen (siehe Kossi/Phantastik-Couch-Mails vom selben Tag als korrektes Beispiel), nicht das Text-Skript nehmen nur weil's schneller griffbereit ist.

**15.08.2026:** Chris will das nicht mehr jedes Mal extra ansagen müssen ("den Link natürlich klickbar, möchte ich aber nicht immer dazusagen müssen") — ist ein stiller Standard, keine Bestätigungsfrage nötig. Bei jedem Entwurf mit URL automatisch HTML bauen, ohne das im Chat extra zu erwähnen oder nachzufragen.
