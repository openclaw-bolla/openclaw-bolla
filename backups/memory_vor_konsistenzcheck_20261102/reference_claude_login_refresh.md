---
name: reference-claude-login-refresh
description: Claude Code /login API Error — Ursache & schneller Refresh-Fix (Browser-Auto-Open in WSL)
metadata: 
  node_type: memory
  type: reference
  originSessionId: de782807-0041-42c0-83e9-7a90fafaf1db
  modified: 2026-07-21T11:55:49.487Z
---

# Claude Code "/login API Error" — Ursache & Fix

## Was passiert ist (20.06.2026)
Chris bekam plötzlich einen "API Error", Claude Code verlangte `/login`. Der Browser
öffnete sich NICHT automatisch — nur ein langer Login-Link im Terminal, den er manuell
kopieren musste. Sehr frustrierend, weil Bolla in dem Moment nicht erreichbar ist
(Bolla läuft IN Claude Code → kein Login = kein Bolla).

## Zwei Ursachen
1. **Token komplett raus statt stiller Refresh:** OAuth-Token (Max Plan) lebt ~8h und
   erneuert sich im Hintergrund über das Refresh-Token, solange Claude Code läuft. Ein
   VOLLES Re-Login wird nur nötig, wenn auch das Refresh-Token ungültig wurde — passiert
   typischerweise bei einem server-seitigen Anthropic-Auth-Vorfall. Am 18.06.2026 gab es
   einen "major Service disruption on Claude services" → plausibelste Spur. Liegt bei
   Anthropic, NICHT verhinderbar von uns.
2. **Browser öffnete nicht (DAS war der Frust-Faktor, IST gefixt):** In WSL war `$BROWSER`
   leer und weder `wslview` noch `xdg-open` installiert → Claude Code hatte keinen
   Browser-Opener → warf nur den Link ins Terminal.

## Fix (eingerichtet 20.06.2026)
- Wrapper `~/bin/wslbrowser` → ruft Windows-Edge auf (`msedge.exe "$@"`).
- In `~/.bashrc`: `export BROWSER="$HOME/bin/wslbrowser"`.
- Effekt: Beim nächsten `/login` öffnet Claude Code den Link automatisch in Edge — ein
  Klick statt Link-Kopieren. (Greift ab nächstem Terminal-Neustart.)
- **Notfall-Anleitung** für den Fall, dass Bolla weg ist: steht in der MP **🚨 Recovery**-Box
  auf der 🤖 Claude-Code-Seite (`index.html`, Item "API Error / Login weg?"). KEINE
  Desktop-Datei mehr (Chris will Recovery zentral in MP, nicht als loses Word/TXT auf dem Desktop).

## Status prüfen ohne Token-Verbrauch
- Anthropic-Ausfall? → https://status.claude.com (Domain NEU: status.claude.com, nicht
  mehr status.anthropic.com — die alte leitet nur noch dorthin um).
- Quota/Plan → MC `/api/claudequota` (kostenlos). Vom Handy: bolla.chrismandel.de.

## Plan-Label in MP zeigt falschen Plan nach Tarifwechsel (19.07.2026)
Nach Chris' Wechsel Max→Pro zeigte die MP-Übersicht weiter "Max Plan" (Modell-Name Sonnet 5 war korrekt).
Ursache: `plan_label` in `get_claude_quota()` (mission_control_api.py) liest `subscriptionType`/
`rateLimitTier` NICHT live von Anthropic — die live `/api/oauth/usage`-Antwort enthält gar kein
Plan-Namensfeld (nur Prozentwerte). Die Werte kommen aus der lokalen `~/.claude/.credentials.json`,
gesetzt beim letzten Token-Login/-Refresh. Bleibt stehen, bis der Access-Token natürlich abläuft (~8h)
und sich im Hintergrund erneuert. **Bewusst NICHT manuell per Skript erzwungen** — würde den Token
austauschen, den die laufende Claude-Code-Session gerade selbst nutzt, Risiko: genau der "/login API
Error" von oben. Reine Kosmetik (Prozentzahlen/Kontingente sind live korrekt), löst sich von selbst.

## "/login" landete auf Registrierungs-Seite statt Login (21.07.2026)
Chris klickte den Login-Link, landete aber auf der claude.ai-Seite für ein **neues Konto**, kein Hinweis
was los ist. Vermutliche Ursache: Edge war in dem Moment nicht (mehr) bei Google als
`chrismandel13@gmail.com` eingeloggt — ohne aktive Google-Session zeigt claude.ai die generische
Einstiegsseite, die Login/Registrierung nicht klar genug trennt. Reines Anthropic-UX-Problem, nichts,
was wir verhindern können. **Vorbeugung fürs nächste Mal:** bei `/login` zuerst kurz auf
accounts.google.com prüfen ob mit `chrismandel13@gmail.com` eingeloggt, DANN den Link öffnen — dann
erkennt claude.ai das bestehende Konto.

## Terminal-Header zeigt "API Usage Billing" statt Pro/Max-Plan (21.07.2026)
Chris sah oben im Claude-Code-Terminal "Sonnet 5 with high effort · **API Usage Billing**" statt eines
Hinweises auf sein Abo — Sorge: zahlt er jetzt pay-per-token statt Abo-Kontingent? Geprüft: `.credentials.json`
zeigt korrekt `subscriptionType: pro`, keine `ANTHROPIC_API_KEY` gesetzt, kein `forceLoginMethod` in
Settings. Ist ein **bekannter, rein kosmetischer Anzeige-Bug in Claude Code selbst** (nicht bolla-spezifisch),
bestätigt durch zwei offene GitHub-Issues: #45572 und #20976 ("Max plan shows as 'API Usage Billing' in
CLI"). Betrifft andere Nutzer genauso, Ursache liegt im CLI-Code (Anzeigelogik unterscheidet Abo- vs.
API-Key-Login nicht zuverlässig), noch ungefixt von Anthropic. **Kein Handlungsbedarf** — Abrechnung läuft
korrekt gegen das Pro-Kontingent, nur die Anzeige lügt. Gleiche Bug-Kategorie wie der MP-Plan-Label-Bug
oben, nur diesmal im nativen Terminal-Header statt in Mission Control.

Verwandt: [[reference-mc]], [[reference-technical]], [[user_accounts]]
