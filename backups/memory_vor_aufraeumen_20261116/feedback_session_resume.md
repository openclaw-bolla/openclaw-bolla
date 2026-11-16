---
name: feedback-session-resume
description: "Nach /clear sauber aufsetzen — aktuell.md ist die EINE Quelle, Stand IMMER dort sichern"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a791f801-1f65-410b-ab51-9759d0b9d594
---

# Sauberes Aufsetzen nach /clear

Chris verliert massiv Zeit, wenn ich nach einem `/clear` den falschen oder veralteten Stand lese und nicht da weitermache, wo wir waren.

**Why:** Claude Code legt PRO Arbeitsverzeichnis (cwd) ein eigenes `~/.claude/projects/<cwd-slug>/memory/` an. Bolla startete mal aus `/home/bolla`, mal aus `/mnt/c/Users/ernst`, mal aus System32 → mehrere divergierende `aktuell.md`/`MEMORY.md`. Nach /clear las ich je nach Startverzeichnis einen anderen/alten Stand und fragte Dinge, die längst erledigt waren.

**How to apply:**
- **Fix steht (17.06.2026):** Kanonisches Memory = `~/.claude/projects/-home-bolla/memory/`. ALLE anderen `projects/*/memory/` sowie `workspace/memory/aktuell.md` + `workspace/MEMORY.md` sind **Symlinks** darauf → egal aus welchem cwd Bolla startet, dasselbe Gedächtnis. Symlinks NICHT durch echte Dateien ersetzen (sonst driftet es wieder).
- Bei Session-Start `aktuell.md` lesen und den GENAUEN nächsten Schritt übernehmen — inkl. WIE (z.B. „leite Chris Schritt für Schritt, nicht alles auf einmal").
- Vor JEDEM `/clear` bzw. bei jeder größeren Aktion den Stand + nächsten Schritt + Arbeitsweise in `aktuell.md` schreiben — nicht in eine Nebendatei. ([[feedback_aktuell_md]])
