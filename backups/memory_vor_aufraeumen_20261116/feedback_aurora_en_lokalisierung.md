---
name: feedback-aurora-en-lokalisierung
description: "AURORA englische Ausgabe ist voll lokalisiert (andere Namen/Schauplatz), nicht nur übersetzt — vor jedem EN-Text prüfen"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0a3a1374-571a-4769-9849-3f2f624372d1
---

Die englische AURORA-Ausgabe ist keine reine Übersetzung, sondern eine vollständige Lokalisierung mit anderen Eigennamen und anderem Schauplatz:

| Deutsch | Englisch |
|---|---|
| Marlie Braun | **Marley Brown** |
| Noah Weber | **Noah Khoury** |
| Hamburg | **Boston** |
| AURORA (KI) | AURORA (bleibt gleich) |

**Why:** Bei einer Mail-Outreach-Aktion an einen englischsprachigen Buchclub hatte ich reflexhaft "Marlie Braun" (aus dem deutschen Projekt-Gedächtnis [[projekt_ki_thriller]] und einem alten Entwurf kopiert) verwendet — falsch für die EN-Ausgabe. Chris hat das zurecht scharf korrigiert ("du solltest besser aufpassen"). Verifiziert per grep in `data/ki_buch_en.json` (647× "Marley" vs. 75× "Marlie", die 75 sind vermutlich Lokalisierungs-Reste/Bugs im EN-Text selbst).

**How to apply:** Bei JEDEM englischsprachigen Text über AURORA (Mails, Posts, Anschreiben) IMMER die EN-Namen/den EN-Schauplatz verwenden, nie blind aus deutschen Notizen kopieren. Bereits veröffentlichter Essay (Medium/LinkedIn EN) nutzt fälschlich/bewusst "Marlie Braun"+"Hamburg" — mit Chris klären, ob das Absicht war (persönliche Entstehungsgeschichte) oder korrigiert werden soll. Alte Entwürfe in `Dokumente/Bolla/AURORA/6_Marketing/AURORA_Anschreiben_Top3.txt` (M(AI)VENS + WAIE) haben denselben Fehler — vor Wiederverwendung prüfen/fixen. Siehe [[project_aurora_englisch]].
