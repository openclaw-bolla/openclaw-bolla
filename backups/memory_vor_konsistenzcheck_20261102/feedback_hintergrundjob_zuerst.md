---
name: feedback_hintergrundjob_zuerst
description: Bei mehreren Aufgaben zuerst den Hintergrundprozess (Render, lange Skripte) anstoßen, dann den Rest selbständig abarbeiten
metadata:
  type: feedback
---

Chris 21.10.2026: „wenn einer der jobs ein hintergrundprozess ist, dann den zuerst anlegen (selbst wenn ich den nicht als erstes anstoße) und dann automatisch den rest."

**Why:** Lange Läufe (Blender-Render ~4 h) sollen so früh wie möglich laufen; die Zeit überbrückt der Rest. Chris will nicht nachfragen müssen, ob er parallel Weiteres anstoßen soll.
**How to apply:** Bei Mehrpunkt-Anfragen ([[feedback_mehrpunkt_anfragen]]) erst prüfen, welche Punkte Hintergrundprozesse sind (detached, resumable, Job-Status per `report()`, [[feedback_hintergrund_fork_lange_aktionen]]), diese zuerst starten, dann ohne Rückfrage die übrigen Punkte nacheinander erledigen. Auch die Frage „soll ich in der Zwischenzeit X machen?" entfällt — einfach machen ([[feedback_einfach_machen]]).
