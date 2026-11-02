---
name: mp-chat-freigabe-dialog-bug
description: "MP-Chat-Session hängt, wenn ein Bash-Befehl Freigabe braucht und Chris \"zulassen\"/\"ja\" nur als Chat-Text tippt statt den echten Freigabe-Button zu klicken"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3351b954-2154-4453-8190-34ed805ad93d
  modified: 2026-08-27T12:50:15.765Z
---

Wenn in einem MP-Chat (`bolla_chat_stream`, `claude -p --resume`) ein Tool-Aufruf (z.B. Mail-Versand
per `send_text_mail.py`) eine Berechtigung braucht, poppt im MC-UI eine Freigabe-Box mit dem Befehl auf.
Tippt Chris die Bestätigung ("zulassen", "ja", "ok") als normale Chat-Nachricht ins Textfeld, kommt das
NICHT beim Permission-Prompt an — der `claude -p`-Subprozess wartet weiter auf die echte Tool-Freigabe,
die neue Chat-Nachricht wird nur als neue User-Message behandelt (führt oft zu einer zweiten, verwirrten
Antwort "Der Versand hängt weiter fest, klick den Button"). Der ursprüngliche Tool-Call bleibt unbestätigt
hängen → wirkt wie ein Freeze der Session, obwohl es die Wartestellung des Freigabe-Dialogs ist.

Konkret aufgetreten: 27.08.2026, Session `4fb9cf9c-...` (Schul-PC-Scareware-Mail an it@lg-n.de) — Chris
schrieb nach dem Mail-Entwurf "zulassen" in den Chat, der Bash-Befehl blieb trotzdem im
Freigabe-Zustand hängen. Chris ist dann per "Failed to fetch" in eine neue Session gerutscht (`5ab65402-...`),
die den Kontext nicht mehr hatte und fälschlich meinte, es sei noch gar kein Entwurf geschrieben worden
(stimmte nur zufällig in der Konsequenz: Mail wurde tatsächlich nie verschickt).

**Why:** MC-UI trennt Chat-Textfeld und Permission-Button als zwei verschiedene UI-Elemente/Kanäle — der
zugrunde liegende `claude -p`-Prozess bekommt Freigaben nur über den tatsächlichen Tool-Approval-Mechanismus,
nicht über Konversationstext.

**How to apply:** Wenn Chris in einem MP-Chat auf einen mailversand-/schreibaktion-artigen Vorschlag mit
"ja"/"zulassen"/"ok" antwortet und danach nichts passiert bzw. die Session hängt: proaktiv erklären, dass
er den echten Freigabe-Button in der Box klicken muss (nicht ins Textfeld tippen). Bei wiederkehrendem
Ärgernis ggf. vorschlagen, unkritische, wiederkehrende Skripte (z.B. `send_text_mail.py` nur lesend/an
bekannte interne Adressen) dauerhaft freizuschalten, um den Dialog ganz zu vermeiden — aber nur nach
Rückfrage, da [[feedback_mail_freigabe]] weiterhin gilt (Mail-Entwurf immer zeigen vor Versand).

Verwandt: [[project_schulpc_scareware]], [[feedback_mail_freigabe]]
