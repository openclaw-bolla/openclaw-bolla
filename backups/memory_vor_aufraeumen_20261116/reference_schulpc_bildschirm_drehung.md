---
name: reference-schulpc-bildschirm-drehung
description: Schul-PC-Bildschirm verdreht (schon am Anmeldebildschirm) — Fix per Tastatur
metadata: 
  node_type: memory
  type: reference
  originSessionId: 159c73a4-e5c1-488b-93b0-6d00880fd6bf
  modified: 2026-09-02T12:17:57.983Z
---

# Schul-PC: Bildschirm um 90° gedreht

**Symptom (02.09.2026, ViewSonic-Monitor an Schul-PC):** Bild steht quer/gedreht, schon
am Windows-Anmeldebildschirm. Maus dabei „nicht steuerbar" — normal, weil bei gedrehtem
Bild auch die Mausachsen mitgedreht sind. Lösung geht **nur mit Tastatur**.

## Fix (hat am 02.09.2026 geklappt) — der Weg über die Einstellungen

Der Intel-Hotkey **Strg + Alt + Pfeil** funktioniert an den Lessing-Schul-PCs **NICHT**
(vom Admin gesperrt) — am 02.09. mehrfach probiert, ohne Wirkung. Es geht nur so:

1. Passwort blind eintippen, Enter → Desktop.
2. Windows-Taste + R → `ms-settings:display` → Enter.
3. Mit Tab zum Feld „Anzeigeausrichtung", Alt+Pfeil unten öffnet die Liste, mit
   Pfeiltasten „Querformat" wählen, Enter.
4. „Beibehalten?" mit Tab anwählen und Enter (innerhalb 15 Sek.). Repariert auch den
   Anmeldebildschirm dauerhaft.

Alles nur mit Tastatur machbar — die Maus ist bei gedrehtem Bild unbrauchbar.
