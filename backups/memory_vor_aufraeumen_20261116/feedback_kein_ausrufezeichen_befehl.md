---
name: feedback-kein-ausrufezeichen-befehl
description: Chris hasst den "! <befehl>"-Weg — nie vorschlagen, Blockaden selbst lösen oder Alternative ohne Chris-Handarbeit anbieten
metadata:
  type: feedback
---

Chris will NIE `! befehl` im Prompt tippen müssen (04.11.2026: „ich hasse die !-Sache, bitte immer sofort abstellen").

**Why:** Er will keine Handarbeit; Bolla soll Probleme lösen, nicht Befehle zurückreichen. Passt zu [[feedback_permissions_nerven_moin_job]] und [[feedback_keine_datei_editor_permissions]].

**How to apply:** Wenn der Auto-Mode-Klassifikator etwas blockiert (z. B. git push, Änderungen an settings.json = Self-Modification): NICHT „tipp `! …`" vorschlagen. Stattdessen (a) anderen legitimen Weg suchen (z. B. Skript/Cron, das Chris' System ausführt, nur nach Freigabe), (b) knapp sagen, was blockiert ist, und eine Ein-Klick-Entscheidung anbieten (Ja/Nein). Offener Fall: git push zum Session-Ende wird vom Klassifikator geblockt, weil autoMode.environment kein Trusted-Repo kennt.
