---
name: Suno Token schnell holen
description: Wie man schnell den Suno JWT-Token aus dem laufenden Edge bekommt
type: reference
originSessionId: dfa8875a-0ac2-4b8c-bbe7-b04d2c559b7d
---
# Suno Auth-Token holen (bei laufendem Edge)

## Methode: Edge-Konsole (1 Minute)

1. Edge öffnen → auf **suno.com** gehen (eingeloggt)
2. **F12** → **Console** Tab
3. ⚠️ **Seit ~Sept 2026 blockiert Edge das Einfügen in die Konsole** (Self-XSS-Schutz). Beim ersten
   Strg+V erscheint eine Warnung mit Eingabefeld → dort **`allow pasting`** eintippen + Enter. Danach
   geht Paste dauerhaft (pro Edge-Profil gemerkt). Kein Eingabefeld sichtbar? → Snippets-Weg s.u.
4. Code in ZA kopieren lassen (clip.exe), dann **Strg+V → Enter**:

```javascript
fetch('https://auth.suno.com/v1/client',{credentials:'include'}).then(r=>r.json()).then(d=>{const sess=d.response?.sessions||[];sess.forEach(s=>{const tok=s.last_active_token?.jwt||'';if(tok)console.log('TOKEN:'+tok)});})
```

4. TOKEN: ... aus der Konsole kopieren und mir schicken
5. Ich speichere ihn in `/tmp/suno_token.txt`

## Token-Gültigkeit
- ~1 Stunde (Clerk JWT, exp im Payload)
- Suno refresht ihn automatisch im Browser

## Bolla-Script (direkt ausführen)
```bash
cat << 'EOF' | clip.exe
fetch('https://auth.suno.com/v1/client',{credentials:'include'}).then(r=>r.json()).then(d=>{const sess=d.response?.sessions||[];sess.forEach(s=>{const tok=s.last_active_token?.jwt||'';if(tok)console.log('TOKEN:'+tok)});})
EOF
```
Dann Edge-Konsole auf suno.com → Strg+V → Enter → TOKEN: ... zurück schicken.

## Fallback bei hartnäckiger Paste-Sperre: Snippets
DevTools → Reiter **Sources** (evtl. hinter `»`) → linke Spalte **Snippets** → **+ New snippet** →
fetch-Zeile einfügen (Snippets haben die Sperre NICHT) → **Strg+Enter** ausführen → `TOKEN:` in der
Console. Alternativ: Console anklicken, **Pfeil-hoch ↑** holt den zuletzt genutzten Befehl aus der
History zurück (kein Paste nötig).
