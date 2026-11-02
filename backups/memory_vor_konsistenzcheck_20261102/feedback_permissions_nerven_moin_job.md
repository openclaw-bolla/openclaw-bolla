---
name: feedback_permissions_nerven_moin_job
description: Chris nervt das ständige Permission-Nachfragen/Classifier-Blocken — bei „moin“ als Job angehen (Regeln setzen)
metadata:
  type: feedback
---

Chris 20.10.2026: „das mit den ständigen permissions neuerdings nervt. merk dir das als job wenn ich mich mit moin melde.“ Auslöser: Auto-Mode-Classifier blockte `rm`/`rm -rf` (AURORA-Video-Aufräumen, ~60 GB), obwohl Chris das Löschen ausdrücklich wollte.

**Why:** Blockaden unterbrechen Aufträge, wenn Chris nicht am Rechner ist; er bearbeitet keine .json selbst ([[feedback_keine_datei_editor_permissions]]).
**How to apply:** Bei „moin“ unter den offenen Punkten aufführen: „Permission-Nerverei beheben“ — gehäufte Blocks aus den letzten Sessions sammeln (Skill `fewer-permission-prompts`, [[reference_automode_classifier_mail]]) und Regeln selbst per Edit in settings.json vorschlagen/eintragen (z. B. `rm` unter `C:\Tools\blender_proj`, Trailer-Ordner, Desktop\temp). Sofort offen: `scripts/aufraeumen_aurora_videos.sh` nach fertigem v4-Lauf. Siehe [[feedback_moin_offene_aktionen]].
