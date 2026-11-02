---
name: feedback-clip-utf16
description: clip.exe braucht UTF-16LE+BOM — sonst kaputte Umlaute/Sonderzeichen beim Einfügen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a66f254d-27ef-4179-bc3d-8c2bbbb2f4e4
---

Beim Befüllen der Windows-Zwischenablage via `clip.exe` IMMER von UTF-8 nach **UTF-16LE mit BOM** konvertieren — sonst werden Umlaute und Sonderzeichen verschlüsselt eingefügt (z.B. `größten`→`gr├Â├ften`, `—`→`ÔÇö`).

**Why:** `clip.exe` interpretiert reine UTF-8-Bytes falsch. Das ist mehrfach passiert (zuletzt D2D-Klappentext 18.06.2026). Chris ärgert das zu Recht.

**How to apply:** Standard-Pattern statt `... | clip.exe`:
```bash
{ printf '\xff\xfe'; iconv -f UTF-8 -t UTF-16LE <<'EOF'
…Text mit Umlauten…
EOF
} | /mnt/c/Windows/System32/clip.exe
```
`printf '\xff\xfe'` = BOM, dann iconv-Konvertierung. Gilt für ALLE Texte mit Nicht-ASCII (Klappentexte, Mails, Briefe). Siehe [[feedback_copy_from_terminal]].

**ACHTUNG strenge Editoren (KDP!):** Manche Felder lehnen das BOM als „unsichtbares Zeichen" ab (KDP-Beschreibung 18.06.: „Beschreibung darf keine unsichtbaren Zeichen enthalten"). D2D/CKEditor war tolerant, KDP nicht. **Besserer, universeller Weg = PowerShell Set-Clipboard** (setzt sauberen Unicode-Text OHNE BOM):
```bash
cat > "/mnt/c/Users/ernst/tmp.txt" <<'EOF'
…Text…
EOF
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "Set-Clipboard -Value (Get-Content -Raw -Encoding UTF8 'C:\Users\ernst\tmp.txt')"
rm -f "/mnt/c/Users/ernst/tmp.txt"
```
Im Zweifel diesen PowerShell-Weg nehmen — funktioniert überall, Umlaute korrekt, kein BOM.
