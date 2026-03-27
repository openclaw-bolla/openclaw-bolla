#!/usr/bin/env python3
"""Erstellt openclaw-wiederherstellung.pdf mit aktuellem Stand."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/home/bolla/.openclaw/workspace/openclaw-wiederherstellung.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

styles = getSampleStyleSheet()
normal = styles["Normal"]
normal.fontName = "Helvetica"
normal.fontSize = 10
normal.leading = 14

title_style = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=18, leading=22, spaceAfter=4)
subtitle_style = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=11, leading=14, textColor=colors.HexColor("#555555"), spaceAfter=12)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor("#1a1a2e"))
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#16213e"))
code_style = ParagraphStyle("code", fontName="Courier", fontSize=9, leading=13, backColor=colors.HexColor("#f0f0f0"), borderPadding=6, spaceAfter=4)
warn_style = ParagraphStyle("warn", fontName="Helvetica-BoldOblique", fontSize=10, leading=13, textColor=colors.HexColor("#c0392b"))
note_style = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=9, leading=13, textColor=colors.HexColor("#666666"))
bullet = ParagraphStyle("bullet", fontName="Helvetica", fontSize=10, leading=14, leftIndent=14, spaceAfter=2)

def C(text): return Paragraph(text, code_style)
def N(text): return Paragraph(text, normal)
def B(text): return Paragraph(f"• {text}", bullet)
def H1(text): return Paragraph(text, h1)
def H2(text): return Paragraph(text, h2)
def W(text): return Paragraph(f"⚠️  {text}", warn_style)
def Note(text): return Paragraph(text, note_style)
def SP(n=6): return Spacer(1, n)
def HR(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=6, spaceBefore=6)

story = []

# ── Titel ──────────────────────────────────────────────────────────────────────
story.append(Paragraph("🐾 Bolla – Wiederherstellungsanleitung", title_style))
story.append(Paragraph("OpenClaw KI-Assistent · Stand: März 2026 · Für Chris Mandel", subtitle_style))
story.append(HR())
story.append(SP(4))

# ── Übersicht ──────────────────────────────────────────────────────────────────
story.append(H1("Was ist Bolla?"))
story.append(N("Bolla ist ein persönlicher KI-Assistent auf Basis von OpenClaw (Claude). Er läuft lokal auf dem Surface-Laptop unter WSL2 (Ubuntu) und ist erreichbar über den Browser (Dashboard) sowie Telegram."))
story.append(SP())

data = [
    ["Komponente", "Beschreibung"],
    ["OpenClaw Gateway", "Node.js-Dienst in WSL2, Port 18789"],
    ["Dashboard", "http://172.20.108.84:18789/ (lokale IP kann variieren)"],
    ["Telegram Bot", "@bolla_mandel_bot"],
    ["WSL-User", "bolla"],
    ["Windows-User", "ernst"],
    ["Workspace", "/home/bolla/.openclaw/workspace/"],
    ["GitHub Backup", "https://github.com/openclaw-bolla/openclaw-bolla (privat)"],
]
t = Table(data, colWidths=[5*cm, 10.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
    ("FONTNAME", (1,1), (1,-1), "Courier"),
    ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#f9f9f9")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f4ff")]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("PADDING", (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(SP(10))

# ── Autostart ─────────────────────────────────────────────────────────────────
story.append(H1("Autostart – wie Bolla beim Windows-Start automatisch läuft"))
story.append(N("Beim Windows-Login starten zwei VBS-Dateien im Windows-Startup-Ordner:"))
story.append(SP(4))
story.append(C("C:\\Users\\ernst\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"))
story.append(SP(4))

data2 = [
    ["Datei", "Funktion"],
    ["start_openclaw_gateway.vbs", "Startet WSL, wartet auf Netzwerk, startet Gateway"],
    ["start_token_watcher.vbs", "Startet den Token-Watcher-Python-Prozess"],
]
t2 = Table(data2, colWidths=[6.5*cm, 9*cm])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#16213e")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("FONTNAME", (0,1), (0,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f4ff")]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("PADDING", (0,0), (-1,-1), 5),
]))
story.append(t2)
story.append(SP(6))

story.append(H2("Ablauf des Gateway-Starts"))
story.append(B("VBS weckt WSL auf (wsl echo) und wartet 15 Sekunden"))
story.append(B("bash-Script /home/bolla/.openclaw/workspace/scripts/openclaw-launcher.sh wird aufgerufen"))
story.append(B("Launcher wartet bis zu 120 Sekunden auf Netzwerk (testet login.microsoftonline.com)"))
story.append(B("openclaw gateway start wird ausgeführt"))
story.append(B("Windows-Popup erscheint: 'Bolla 🐾 bereit!' (verschwindet nach 5 Sek)"))
story.append(SP(4))
story.append(W("Die VBS verwendet ABSOLUTEN Pfad: /home/bolla/.openclaw/workspace/scripts/openclaw-launcher.sh"))
story.append(Note("Grund: 'wsl -e bash' expandiert keine ~ – daher muss der vollständige Pfad angegeben werden."))
story.append(SP(4))

story.append(H2("Log-Datei prüfen (bei Problemen)"))
story.append(C("/home/bolla/.openclaw/workspace/logs/gateway_autostart.log"))
story.append(SP(4))

story.append(H2("Gateway manuell starten (falls Autostart fehlschlug)"))
story.append(N("Terminal in WSL öffnen und eingeben:"))
story.append(C("openclaw gateway start"))
story.append(SP(10))

# ── Token Watcher ─────────────────────────────────────────────────────────────
story.append(H1("Token Watcher – Automatische API-Key-Erneuerung"))
story.append(N("Der Token Watcher überwacht das E-Mail-Postfach auf neue Anthropic API-Tokens und aktualisiert OpenClaw automatisch."))
story.append(SP(4))
story.append(B("Script: /home/bolla/.openclaw/workspace/scripts/token_watcher.py"))
story.append(B("Prüft alle 15 Minuten Mails von robinmandel@outlook.de"))
story.append(B("Erkennt Anthropic-Tokens, aktualisiert ALLE Profile (bolla + default)"))
story.append(B("Startet Gateway neu, löscht die Token-Mail danach"))
story.append(B("Sortiert nach Datum – neuester Token gewinnt"))
story.append(SP(4))
story.append(W("Token NIEMALS manuell in JSON-Dateien eintragen! Immer per Mail senden."))
story.append(SP(4))
story.append(H2("Token erneuern"))
story.append(N("Neuen Anthropic-Token einfach per E-Mail von robinmandel@outlook.de an ernstmandel@outlook.de senden. Der Watcher erkennt ihn automatisch innerhalb von 15 Minuten."))
story.append(SP(4))
story.append(H2("Task Scheduler (Wächter-Job)"))
story.append(B("Aufgabe: \\OpenClaw\\TokenWatcher (startet bei Login)"))
story.append(B("Aufgabe: \\OpenClaw\\TokenWatcherHourly (stündlich, prüft ob Watcher läuft)"))
story.append(B("Log: /home/bolla/.openclaw/workspace/logs/token_watcher.log"))
story.append(SP(10))

# ── E-Mail ────────────────────────────────────────────────────────────────────
story.append(H1("E-Mail Konten"))
data3 = [
    ["Konto", "Protokoll", "Verwendung"],
    ["ernstmandel@outlook.de", "Microsoft Graph API", "Primär – Lesen & Senden"],
    ["chrismandel@wtnet.de", "IMAP/SMTP (mail.wtnet.de)", "Sekundär – Spam-Watcher aktiv"],
]
t3 = Table(data3, colWidths=[5.5*cm, 4.5*cm, 5.5*cm])
t3.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f4ff")]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("PADDING", (0,0), (-1,-1), 5),
]))
story.append(t3)
story.append(SP(4))
story.append(Note("Microsoft Graph Token: ~/.openclaw/workspace/config/ms_token.json (läuft irgendwann ab → neuen Device Flow starten)"))
story.append(Note("wtnet Zugangsdaten: ~/.openclaw/workspace/config/wtnet_account.json (chmod 600, NICHT im Git-Repo)"))
story.append(SP(4))
story.append(N("Standard-Absender ist immer ernstmandel@outlook.de. Bei wtnet-Konto zuerst nachfragen."))
story.append(SP(10))

# ── Umzug auf neuen Rechner ───────────────────────────────────────────────────
story.append(H1("Umzug auf einen neuen Rechner"))
story.append(W("Bei Umzug müssen absolute Pfade in der VBS angepasst werden!"))
story.append(SP(6))

story.append(H2("Schritt 1 – WSL2 + Ubuntu einrichten"))
story.append(B("Windows Feature: WSL2 aktivieren (wsl --install)"))
story.append(B("Ubuntu aus Microsoft Store installieren"))
story.append(B("WSL-User anlegen: bolla (oder neuen Namen wählen)"))
story.append(SP(4))

story.append(H2("Schritt 2 – Node.js + OpenClaw installieren"))
story.append(C("curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -\nsudo apt-get install -y nodejs\nnpm install -g openclaw"))
story.append(SP(4))

story.append(H2("Schritt 3 – Workspace aus GitHub wiederherstellen"))
story.append(C("cd ~/.openclaw\ngit clone https://github.com/openclaw-bolla/openclaw-bolla workspace"))
story.append(SP(4))

story.append(H2("Schritt 4 – Secrets wiederherstellen (NICHT im Git-Repo!)"))
story.append(Note("Diese Dateien sind NICHT im GitHub-Backup. Sie müssen manuell übertragen werden:"))
story.append(B("~/.openclaw/workspace/config/ms_token.json  (Microsoft Graph Token)"))
story.append(B("~/.openclaw/workspace/config/wtnet_account.json  (wtnet Passwort)"))
story.append(B("~/.openclaw/workspace/config/google_token.json  (Google OAuth Token)"))
story.append(B("~/.openclaw/openclaw.json  (OpenClaw Config mit API-Key)"))
story.append(SP(4))
story.append(Note("Alternativ: Neuen Anthropic-Token per Mail schicken, wtnet-Passwort neu einrichten, Google OAuth neu durchlaufen."))
story.append(SP(4))

story.append(H2("Schritt 5 – OpenClaw konfigurieren"))
story.append(C("openclaw gateway start\nopenclaw status"))
story.append(SP(4))

story.append(H2("Schritt 6 – VBS-Dateien anpassen und in Startup-Ordner kopieren"))
story.append(W("Absoluten Pfad in start_openclaw_gateway.vbs anpassen!"))
story.append(SP(4))
story.append(N("Die VBS liegt im Workspace: scripts/start_openclaw_gateway.vbs"))
story.append(N("Zeile die angepasst werden muss:"))
story.append(C('oShell.Run "wsl -e bash /home/NEUER-WSL-USER/.openclaw/workspace/scripts/openclaw-launcher.sh", 0, False'))
story.append(SP(4))
story.append(N("Dann beide VBS-Dateien in den Windows Startup-Ordner kopieren:"))
story.append(C("C:\\Users\\WINDOWS-USER\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"))
story.append(SP(4))

story.append(H2("Schritt 7 – Task Scheduler für Token Watcher einrichten"))
story.append(N("PowerShell als Administrator:"))
story.append(C("wsl -e bash /home/NEUER-WSL-USER/.openclaw/workspace/scripts/start_token_watcher.sh"))
story.append(Note("Details: scripts/register_token_watcher.ps1 im Workspace"))
story.append(SP(4))

story.append(H2("Schritt 8 – Telegram Bot prüfen"))
story.append(B("Bot @bolla_mandel_bot läuft unabhängig – Token in openclaw.json"))
story.append(B("Beim ersten Start: Bolla in Telegram anschreiben und Pairing bestätigen"))
story.append(SP(10))

# ── Troubleshooting ───────────────────────────────────────────────────────────
story.append(H1("Troubleshooting"))

story.append(H2("Dashboard nicht erreichbar nach Neustart"))
story.append(B("Log prüfen: /home/bolla/.openclaw/workspace/logs/gateway_autostart.log"))
story.append(B("Log enthält Timestamps? → Launcher hat gestartet"))
story.append(B("Log leer oder nur 'command not found'? → VBS-Problem (Pfad prüfen!)"))
story.append(B("Manuell starten: WSL öffnen → openclaw gateway start"))
story.append(SP(4))

story.append(H2("Token abgelaufen / Bolla antwortet nicht"))
story.append(B("Neuen Token per Mail von robinmandel@outlook.de senden"))
story.append(B("Watcher prüft alle 15 Min – oder manuell: python3 token_watcher.py"))
story.append(SP(4))

story.append(H2("Microsoft Graph Token abgelaufen"))
story.append(B("In WSL: python3 ~/.openclaw/workspace/scripts/google_auth.py  (oder neu: Device Flow)"))
story.append(Note("Genauere Anleitung wird von Bolla geführt – einfach fragen"))
story.append(SP(4))

story.append(H2("VBS startet nicht / kein Popup beim Login"))
story.append(B("Startup-Ordner prüfen: Windows + R → shell:startup"))
story.append(B("VBS doppelklicken zum Testen"))
story.append(B("Wichtig: Pfad in VBS muss absolut sein – kein ~ erlaubt!"))
story.append(SP(10))

# ── Dateipfade ────────────────────────────────────────────────────────────────
story.append(H1("Wichtige Dateipfade auf einen Blick"))
data4 = [
    ["Datei/Ordner", "Pfad"],
    ["Workspace", "/home/bolla/.openclaw/workspace/"],
    ["OpenClaw Config", "/home/bolla/.openclaw/openclaw.json"],
    ["Gateway-Launcher", "/home/bolla/.openclaw/workspace/scripts/openclaw-launcher.sh"],
    ["Gateway-VBS", "...\\Startup\\start_openclaw_gateway.vbs"],
    ["Token-Watcher VBS", "...\\Startup\\start_token_watcher.vbs"],
    ["Token-Watcher Script", "/home/bolla/.openclaw/workspace/scripts/token_watcher.py"],
    ["wtnet-Watcher", "/home/bolla/.openclaw/workspace/scripts/wtnet_watcher.py"],
    ["MS Graph Token", "/home/bolla/.openclaw/workspace/config/ms_token.json"],
    ["wtnet Konto", "/home/bolla/.openclaw/workspace/config/wtnet_account.json"],
    ["Gateway Log", "/home/bolla/.openclaw/workspace/logs/gateway_autostart.log"],
    ["Token Watcher Log", "/home/bolla/.openclaw/workspace/logs/token_watcher.log"],
    ["GitHub Backup", "https://github.com/openclaw-bolla/openclaw-bolla"],
]
t4 = Table(data4, colWidths=[5*cm, 10.5*cm])
t4.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("FONTNAME", (1,1), (1,-1), "Courier"),
    ("FONTSIZE", (1,1), (1,-1), 8),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f4ff")]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("PADDING", (0,0), (-1,-1), 5),
]))
story.append(t4)
story.append(SP(10))

# ── Footer ────────────────────────────────────────────────────────────────────
story.append(HR())
story.append(Note("Erstellt von Bolla 🐾 · Automatisch generiert · Bei Fragen einfach Bolla fragen"))

doc.build(story)
print(f"PDF erstellt: {OUTPUT}")
