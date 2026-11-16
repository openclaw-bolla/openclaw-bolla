---
name: feedback-backup-reihenfolge
description: "Session-Ende-Sicherung — OneDrive-rsync DETACHED im Hintergrund starten, damit Chris SOFORT clearen kann (nicht warten)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5ed6001e-68ba-4c05-b86d-24cfa725c26e
---

# OneDrive-Backup detached im Hintergrund — Chris muss NICHT auf den Sync warten

Das OneDrive-rsync dauert **~4 Min** (langsamer 9p-Windows-Mount, ~4.661 Dateien stat-Scan). Chris soll **nicht** warten müssen, bis es durch ist, bevor er `/clear` / Session-Neustart macht.

**Lösung (so gewünscht):** Den OneDrive-rsync **vollständig abgekoppelt vom Claude-Prozess** starten — mit `setsid`/`nohup` + Output-Umleitung in ein Log, NICHT nur das run_in_background-Feature des Bash-Tools (das hängt an der Session und stirbt ggf. beim Clear). So läuft der Sync unabhängig weiter, **auch nachdem Chris ge-cleart oder die Session beendet hat**.

**How to apply (Session-Ende-Reihenfolge):**
1. `aktuell.md` / Memory updaten
2. Git commit + push
3. OneDrive-rsync **detached** anstoßen, z.B.:
   ```bash
   setsid bash -c 'rsync -aL /home/bolla/.claude/ "/mnt/d/OneDrive/Dokumente/Bolla/claude-code/" \
     >> /home/bolla/workspace/logs/onedrive_backup.log 2>&1' &
   ```
   (Trailing-Slash + `-aL`, KEIN `--delete` — siehe CLAUDE.md.)
4. Chris direkt sagen: **„OneDrive-Sync läuft jetzt im Hintergrund weiter — du kannst SOFORT clearen, ich warte nicht."**

**Wichtig:** Genau NICHT (wie fälschlich mal notiert) "warten bis OneDrive fertig, dann erst clearen". Der ganze Sinn ist: detached starten → Chris ist sofort frei.

Verwandt: [[feedback-clear-erinnerung]] · [[feedback-aktuell-md]] · [[reference-technical]]
