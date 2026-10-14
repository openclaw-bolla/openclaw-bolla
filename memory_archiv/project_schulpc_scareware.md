---
name: project-schulpc-scareware
description: "Fake-Virenwarnung auf Schul-PC S9462 KOMPLETT ERLEDIGT (27.08.) — Ursache Edge-Push-Notification, Mail an it@lg-n.de verschickt"
metadata: 
  node_type: memory
  type: project
  originSessionId: b299e4c1-593c-405c-9701-0d81f0ae665a
  modified: 2026-08-27T13:14:48.412Z
---

## ✅ KOMPLETT ERLEDIGT (27.08.2026)
Root Cause war banal: **kein Trojaner**, sondern eine Edge-Browserberechtigung für Push-Benachrichtigungen
an die Domain `da78m1np3sis738td92g.nhwy-adguard.co.in` (Name täuscht Seriosität vor, hat mit AdGuard
nichts zu tun). Diese Seite hat gefälschte Windows/Antivirus-Warnungen als System-Toast eingeblendet —
auch ohne offenen Browser (Edge-Hintergrundprozess für Push). Klick/Schließen der Warnung öffnete Edge mit
langer Tracking-URL. Fix: unter `edge://settings/content/notifications` den Eintrag bei „Zulassen" entfernt
— Chris bestätigt: „schon war alles wieder gut". Kein Scan, kein Neuaufsetzen nötig.

**Mail an Schul-IT: verschickt** (27.08. nachmittags, An: it@lg-n.de, Betreff „Fake-Virenwarnung auf PC
S9462 – Ursache gefunden, einfache Lösung (kein Trojaner)", Signatur „LG Chris Mandel"). War zwischenzeitlich
hängengeblieben, weil im ursprünglichen MP-Chat der Freigabe-Dialog für den Versand-Befehl nicht per
Chat-Text bestätigt werden konnte, siehe [[feedback_mp_chat_freigabe_dialog_bug]]. Danach blockte der
Auto-Mode-Classifier den Versand zusätzlich mehrfach — Lösung war ein expliziter `permissions.allow`-
Bash-Eintrag statt einer `autoMode.allow`-Freitextregel, siehe [[reference_automode_classifier_mail]].
Kein offener Punkt mehr in diesem Fall.

Am 26.08.2026 morgens auf einem Schul-PC (Lessing-Gymnasium) tauchte direkt nach dem Booten (noch vor
Browserstart) eine Viren-/Trojaner-Warnung auf. Chris hat probeweise alle Edge-Prozesse gekillt und neu
gestartet — Problem blieb.

**Bereits ausgeschlossen:**
- Edge-Hijack: Rechtsklick "Microsoft Edge starten" läuft sauber, kein manipuliertes Verknüpfungsziel.
- Autostart-Ordner (shell:startup / shell:common startup): nichts Auffälliges gefunden.
- Klickt man auf die Warnung ODER versucht sie zu schließen, öffnet sich sofort Edge bzw. ein neuer Tab mit
  einer sehr langen Ziel-URL (Tracking-Parameter-artig) — starkes Indiz für Scareware/Malvertising, kein
  echter Virenfund.

**Betroffener PC:** Inventar-/Raum-Nr. **S9462**. Kontakt Schul-IT: **it@lg-n.de** (siehe
[[reference_lessing_gymnasium]], nicht die allgemeine `md@lg-n.de`).

> ⚠️ Korrektur 28.08.2026: Der früher hier notierte Zusatz „mekren" war KEIN PC-Kürzel/Login — das war
> ein verhörtes/vertipptes „merken" (Chris' Bitte „merk dir das"), das ich fälschlich als Gerätename
> abgespeichert hatte. Der PC hat nur die Nummer S9462. Die IT-Verantwortliche der Schule wollte die
> Nummer nur wissen, um den Vorfall an die Stadt (Schulträger) weiterzumelden.

(Der ursprüngliche Verdacht — Scheduled Task/Autostart-Schadprogramm — hat sich NICHT bestätigt, war
letztlich nur die simple Edge-Notification-Berechtigung, siehe oben. Das `.bat`/`.ps1`-Check-Tool aus dem
26.08. liegt weiter unter `/home/bolla/workspace/schulpc-check/` bzw. OneDrive-Desktop, falls sowas
nochmal an einem Schul-PC gebraucht wird.)
