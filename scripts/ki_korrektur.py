#!/usr/bin/env python3
"""
KI-Korrektur & Benotung — Demo für Lessing-Schulung
Lädt eine Klassenarbeit (Foto/PDF/Scan) hoch und gibt Korrektur + Note aus.
"""
import sys, os, json, base64, pathlib, subprocess, tempfile

# ── API Setup ──────────────────────────────────────────────────────────────────
def get_api_key():
    cred = pathlib.Path("/home/bolla/.claude/.credentials.json")
    if cred.exists():
        d = json.loads(cred.read_text())
        oauth = d.get("claudeAiOauth", {})
        return oauth.get("accessToken", "")
    return os.environ.get("ANTHROPIC_API_KEY", "")

def get_client():
    import anthropic
    key = get_api_key()
    return anthropic.Anthropic(api_key=key)

# ── Datei → Base64 ─────────────────────────────────────────────────────────────
def file_to_image(path: str):
    """Gibt (base64_data, media_type) zurück. PDF → erste Seite als PNG."""
    p = pathlib.Path(path)
    suffix = p.suffix.lower()

    if suffix == ".pdf":
        # Erste Seite als PNG extrahieren
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        result = subprocess.run(
            ["pdftoppm", "-r", "200", "-png", "-singlefile", str(p), tmp_path.replace(".png", "")],
            capture_output=True
        )
        if result.returncode != 0:
            # Fallback: convert (ImageMagick)
            subprocess.run(["convert", "-density", "200", f"{p}[0]", tmp_path], check=True)
        data = base64.standard_b64encode(pathlib.Path(tmp_path).read_bytes()).decode()
        os.unlink(tmp_path)
        return data, "image/png"

    elif suffix in (".jpg", ".jpeg"):
        data = base64.standard_b64encode(p.read_bytes()).decode()
        return data, "image/jpeg"
    elif suffix == ".png":
        data = base64.standard_b64encode(p.read_bytes()).decode()
        return data, "image/png"
    elif suffix == ".webp":
        data = base64.standard_b64encode(p.read_bytes()).decode()
        return data, "image/webp"
    else:
        raise ValueError(f"Dateiformat nicht unterstützt: {suffix} (unterstützt: PDF, JPG, PNG)")

# ── Korrektur-Prompt ───────────────────────────────────────────────────────────
def build_prompt(klassenstufe, fach, thema, erwartungshorizont):
    erw = f"\n\nErwartungshorizont / Aufgabenstellung:\n{erwartungshorizont}" if erwartungshorizont else ""
    return f"""Du bist ein erfahrener Lehrer an einem deutschen Gymnasium und korrigierst eine Klassenarbeit.

**Fach:** {fach}
**Klassenstufe:** {klassenstufe}
**Thema:** {thema}{erw}

Bitte korrigiere die vorliegende Klassenarbeit sorgfältig und strukturiert.

## Deine Aufgabe:

1. **Lesbarkeit:** Lies den handgeschriebenen Text so gut wie möglich. Weise auf unleserliche Stellen hin.

2. **Inhaltliche Korrektur:** Gehe Aufgabe für Aufgabe durch:
   - Was hat der Schüler richtig gemacht? ✅
   - Was ist falsch oder unvollständig? ❌
   - Was fehlt? ➕
   - Kurze, konstruktive Anmerkung zu jeder Aufgabe

3. **Bewertungsübersicht:**
   | Aufgabe | Max. Punkte | Erreicht | Kommentar |
   Schätze die Punkte sinnvoll ein wenn kein Erwartungshorizont gegeben.

4. **Gesamtnote:**
   - Gesamtpunkte: X von Y
   - Prozentzahl: XX%
   - Note nach deutschem Gymnasium-Schema (1–6):
     - Note 1: ≥ 87%
     - Note 2: ≥ 73%
     - Note 3: ≥ 59%
     - Note 4: ≥ 45%
     - Note 5: ≥ 30%
     - Note 6: < 30%
   - **Empfohlene Note: [X]** mit kurzer Begründung

5. **Pädagogisches Feedback (3–4 Sätze):**
   Was hat der Schüler gut gemacht? Wo sollte er sich verbessern?
   Motivierend und konstruktiv formulieren.

Antworte auf Deutsch. Sei fair, präzise und pädagogisch sinnvoll."""

# ── Hauptprogramm ──────────────────────────────────────────────────────────────
def main():
    print("\n" + "═"*60)
    print("  🤖  KI-Korrektur & Benotung  —  powered by Claude")
    print("═"*60 + "\n")

    # Datei
    if len(sys.argv) > 1:
        datei = sys.argv[1]
    else:
        datei = input("📎  Pfad zur Klassenarbeit (JPG/PNG/PDF): ").strip().strip('"')

    if not pathlib.Path(datei).exists():
        print(f"❌  Datei nicht gefunden: {datei}")
        sys.exit(1)

    # Parameter
    klassenstufe = input("📚  Klassenstufe (z.B. '9' oder 'Klasse 9'): ").strip() or "9"
    fach         = input("📖  Fach (z.B. WiPo, Geschichte, Deutsch): ").strip() or "WiPo"
    thema        = input("📝  Thema / Aufgabe (kurz): ").strip() or "Allgemein"
    erw_input    = input("📋  Erwartungshorizont eingeben? (Enter = KI schätzt selbst): ").strip()

    print("\n⏳  Claude liest und korrigiert die Arbeit ...\n")

    # Bild laden
    try:
        img_data, media_type = file_to_image(datei)
    except Exception as e:
        print(f"❌  Fehler beim Laden der Datei: {e}")
        sys.exit(1)

    # API-Aufruf
    client = get_client()
    prompt = build_prompt(klassenstufe, fach, thema, erw_input)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2500,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": img_data,
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )
        result = response.content[0].text
    except Exception as e:
        print(f"❌  API-Fehler: {e}")
        sys.exit(1)

    # Ausgabe
    print("\n" + "═"*60)
    print("  📊  KORREKTUR-ERGEBNIS")
    print("═"*60 + "\n")
    print(result)

    # Optional: als Textdatei speichern
    print("\n" + "─"*60)
    save = input("💾  Ergebnis als Textdatei speichern? (j/n): ").strip().lower()
    if save == "j":
        out_path = pathlib.Path(datei).stem + "_korrektur.txt"
        pathlib.Path(out_path).write_text(result, encoding="utf-8")
        print(f"✅  Gespeichert: {out_path}")

    print("\n✅  Fertig!\n")

if __name__ == "__main__":
    main()
