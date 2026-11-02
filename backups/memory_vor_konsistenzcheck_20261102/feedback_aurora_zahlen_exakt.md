---
name: feedback-aurora-zahlen-exakt
description: "AURORA II — Zahlen/Zeitangaben müssen exakt zu Band I passen, nicht nur intern konsistent sein"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 441484f4-5164-4481-b26d-a5b297779248
  modified: 2026-09-14T08:23:38.405Z
---

Bei AURORA II müssen alle Zahlen- und Zeitangaben (Alter, Zeiträume, Daten) nicht nur *innerhalb*
Band II konsistent sein, sondern auch an bereits etablierte Fakten aus Band I anschließen — auch
wenn Band II intern hundertprozentig stimmig wirkt.

**Warum:** Kapitel 1 von AURORA II öffnete mit „AURORA: geschätzt 3 Jahre, 4 Monate" als eingefrorenem
Entwicklungsalter-Stempel (durchgängig korrekt über alle 8 fertigen Kapitel, inkl. akkurat mitgezählter
„unverändert seit X Tagen"-Reihe 19→22→23→24). Trotzdem falsch: Band I (Kap. 46) hatte bereits exakt
festgelegt, dass die reale Tochter, aus deren Daten AURORA rekonstruiert wurde, mit „4 Jahre, 7 Monate"
gestorben ist. Die neue Zahl in Band II war nicht bewusst gewählt, sondern schlicht neu erfunden, ohne
Band I gegenzuchecken — am 14.09.2026 entdeckt, weil Chris explizit nachfragte. Gefixt: alle 8
Kapitelköpfe auf „4 Jahre, 7 Monate" umgestellt (Chris' Entscheidung, von mir bestätigt: es macht die
Zahl zu einer bewusst gesetzten, düsteren Aussage — AURORA kommt nicht über das Alter hinaus, in dem
die Tochter starb — statt einer beliebigen Zahl).

Bekannter Nebenfund: Band I selbst hat einen Zahlendreher (Kap. 35 nennt „sechs Jahre und vier Monate",
Kap. 46 „vier Jahre und sieben Monate" — Chris hat entschieden: Kap. 46 ist die kanonische Zahl, Kap. 35
war ein Versprecher und wird NICHT nachträglich korrigiert.

**How to apply:** Bei jedem neuen AURORA-II-Kapitel (oder Überarbeitung bestehender) Alters-, Datums-
und Zeitraumangaben, die sich auf Band-I-Fakten beziehen (Todesalter der Tochter = 4 Jahre 7 Monate,
Zeitpunkt von Theos Tod, Zeitspannen wie "gut drei Jahre vergangen" seit Band I), aktiv gegen die
Band-I-Kapiteltexte (`/home/bolla/workspace/data/aurora_chapters_aktuell/kap_*.json`) prüfen, nicht nur
gegen sich selbst. Nicht auf reine interne Konsistenz-Prüfung von Band II beschränken — die kann
tadellos sauber sein und trotzdem am falschen Anker hängen.

**Explizite Chris-Vorgabe (14.09.2026):** Genau so ein Fehler wie in Band I selbst (Kap. 35 vs. Kap. 46,
zwei widersprüchliche Altersangaben für dieselbe Sache, nie bemerkt bis zur nachträglichen Frage) soll
in Band II NICHT nochmal passieren — gründlich checken heißt hier: Jede neu geschriebene Zahl (Alter,
Datum, Zeitspanne, Tage-/Wochen-/Jahreszählung) bei Fertigstellung eines Kapitels gegen ALLE anderen
Stellen im Buch abgleichen, an denen dieselbe Größe vorkommt oder aus denen sie sich herleiten lässt —
nicht nur gegen Band I, sondern auch Kapitel von Band II untereinander. Lieber einmal mehr mit `grep`
gezielt nachschauen (wie bei diesem Fix: Datumsheader, "unverändert seit X Tagen"-Kette durchgezählt)
als eine hübsch klingende Zahl unverifiziert stehen lassen.
