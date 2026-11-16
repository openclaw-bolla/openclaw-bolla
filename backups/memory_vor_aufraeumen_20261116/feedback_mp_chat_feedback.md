---
name: feedback_mp_chat_feedback
description: Im MP-Bolla-Chat immer sichtbares Abschluss-Feedback geben — nie mit einer ⏳-Tool-Karte als letztes sichtbares Element enden
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4216decc-1a13-4b1b-b65f-51eca2180cd4
  modified: 2026-08-17T10:59:44.908Z
---

Im MP-UI-Chat (bollaSend() in mission-control/index.html, gespeist von `bolla_chat_stream()`/`/api/bolla/chat`) muss am Ende jedes Turns sichtbares Feedback stehen — nie stillschweigend nach einem Tool-Call aufhören.

**Auslöser:** Chris beobachtete am 06.07.2026, dass die letzte Aktion im Chat dauerhaft eine Sanduhr (⏳) statt einen grünen Haken (✓) zeigte.

**Fix (06.07.2026, in `index.html`/`bollaSend()`):**
- Restpuffer nach Stream-Ende wird jetzt noch verarbeitet (NDJSON-Zeile ohne trailing `\n` ging vorher beim `done`-Break verloren).
- Sicherheitsnetz: nach Turn-Ende werden alle noch auf ⏳ stehenden `.bolla-tool-status`-Spans hart auf ✓ nachgezogen.
- Falls ein Turn rein aus Tool-Calls ohne abschließenden Text bestand, wird zusätzlich automatisch eine Bolla-Textblase (`finalText` oder "✅ Fertig.") angehängt.

**Wie anwenden:** Als Verhaltensregel gilt zusätzlich: eigene Antworten in MP-Sessions immer mit einem kurzen Abschluss-Satz beenden (nicht mitten in einem Tool-Call/ohne Kommentar aufhören) — das UI-Sicherheitsnetz fängt Ausnahmefälle ab, aber die primäre Erwartung ist ein klar sichtbares "fertig"-Signal von mir selbst.

**Reconfirmed 06.07.2026:** Chris hat das nochmal explizit eingefordert — sobald ein Prompt/Auftrag komplett fertig bearbeitet ist (auch bei langen Multi-Tool-Aufgaben, die über mehrere Antworten/Session-Resumes laufen), muss im MP-Bolla-Chat eine klare Status-Meldung erscheinen ("fertig, das und das wurde gemacht"), nicht nur stillschweigend aufhören oder auf Rückfrage warten. Gilt besonders bei langen Hintergrund-Umbauten (z.B. UI-Rework), wo Chris zwischendurch nachfragt "wie weit bist du" — dann aktiven Stand + verbleibende Schritte nennen, und beim tatsächlichen Abschluss nochmal aktiv melden statt nur zu warten.

**Reconfirmed 17.08.2026:** Chris fragte "bist du fertig?" und bat danach explizit darum, sich das zu merken — d.h. er musste aktiv nachfragen statt von selbst eine klare Abschluss-Meldung im MP-UI-Chat zu sehen. Bestätigt: die Regel gilt weiterhin uneingeschränkt, unabhängig davon ob es sich um eine reine Text-Antwort, eine Code-Änderung oder einen Server-Neustart handelt — jede abgeschlossene Aktion braucht eine unmissverständliche "fertig"-Meldung direkt im Chat, ohne dass Chris nachfragen muss.
