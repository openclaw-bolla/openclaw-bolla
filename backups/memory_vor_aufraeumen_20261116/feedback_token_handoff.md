---
name: feedback-token-handoff
description: "Wie Chris Tokens/Schlüssel übergibt, die Bolla nicht selbst holen kann — direkt im Chat, Bolla legt sie sicher ab"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d7ae8944-e5da-4f65-ba4d-ec39ee6e4c6a
---

# Token-Übergabe: Chris schickt sie im Chat (Standard ab 05.07.2026)

**Wenn Bolla einen Token/API-Schlüssel braucht, den es NICHT selbst holen kann** (z.B. muss Chris ihn in einem externen Dashboard erzeugen): Chris will ihn **direkt in den Chat schreiben** — der Datei-Umweg (Notepad → .txt speichern) ist ihm zu umständlich.

**Why:** Bequemlichkeit schlägt hier den minimalen Sicherheitsgewinn des Datei-Wegs — Chris hat das bewusst abgewogen und so entschieden.

**How to apply — Bollas Pflicht bei jedem Chat-übergebenen Token:**
1. **Sofort** in eine geschützte lokale Datei legen: `workspace/config/<dienst>_token.json`, danach **`chmod 600`**. `config/` steht komplett in `.gitignore` → geht NICHT nach GitHub. Die `.claude/`-OneDrive-Sicherung erfasst `workspace/` ohnehin nicht.
2. **NIE** in Memory speichern. **NIE** in Git/GitHub. **NIE** im Klartext in Logs/Skripte/Chat-Antworten zurückschreiben.
3. **Ehrlich bleiben (kein falsches Versprechen):** Der Token steht danach im **Sitzungsprotokoll** dieser Session (das kann Bolla nicht zeilenweise löschen); das Protokoll wird beim Session-Ende mit nach OneDrive gesichert. Chris einmal darauf hinweisen + betonen, dass scoped/widerrufbare Tokens dieses Restrisiko klein halten (jederzeit im Dashboard neu erzeugbar).

Bezug: [[reference_technical]], globale Regel „Tokens/Passwörter nie in Config eintragen/wiedergeben" — der Chat-Weg ist die von Chris freigegebene Ausnahme, ABER die sichere Ablage + Nicht-in-GitHub/Memory bleibt Pflicht.
