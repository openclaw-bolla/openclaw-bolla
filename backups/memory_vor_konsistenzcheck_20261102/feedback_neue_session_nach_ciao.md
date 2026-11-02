---
name: feedback_neue_session_nach_ciao
description: Nach jedem Ciao von Chris automatisch eine neue Claude Code Session starten
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2470f4da-762c-47fe-9179-bb62cf000d86
---

Nach dem Verabschieden (Ciao, Tschüss, bis später, **"fertig für heute"** etc.) immer eine neue Claude Code Session öffnen — nicht warten bis Chris selbst eine startet.

**Why:** Chris möchte dass nach dem Ciao automatisch eine neue Session bereitsteht.

**How to apply:** Nach Session-Ende Routine (aktuell.md, Tagesnotiz, git push, OneDrive) einfach `/clear` ausführen — das setzt den Kontext zurück und startet eine frische Session im selben Terminal. KEIN neues Fenster, KEIN wt.exe. Trigger-Phrasen: "ciao", "tschüss", "bis später", "fertig für heute", "bin fertig", "mache schluss".
