#!/usr/bin/env python3
"""Erstellt ssh-tunnel-erklaerung.pdf"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/home/bolla/workspace/ssh-tunnel-erklaerung.pdf"

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
note_style = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=9, leading=13, textColor=colors.HexColor("#666666"))
bullet = ParagraphStyle("bullet", fontName="Helvetica", fontSize=10, leading=14, leftIndent=14, spaceAfter=2)

def C(text): return Paragraph(text, code_style)
def N(text): return Paragraph(text, normal)
def B(text): return Paragraph(f"• {text}", bullet)
def H1(text): return Paragraph(text, h1)
def H2(text): return Paragraph(text, h2)
def Note(text): return Paragraph(text, note_style)
def SP(n=6): return Spacer(1, n)
def HR(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=6, spaceBefore=6)

story = []

# Titel
story.append(Paragraph("Fernzugriff auf einen anderen Computer", title_style))
story.append(Paragraph("Wie Bolla das Surface Book erreicht — erklärt von Bolla · April 2026", subtitle_style))
story.append(HR())
story.append(SP(4))

# Das Problem
story.append(H1("Das Problem"))
story.append(N("Zwei Computer im selben Heimnetz können sich direkt verbinden. Sobald aber einer der beiden in einem anderen Netz ist (z.B. das Surface Book in der Schule), funktioniert eine direkte Verbindung nicht mehr — der Router blockiert eingehende Verbindungen von außen."))
story.append(SP())
story.append(N("Die Lösung heißt <b>Reverse SSH Tunnel</b>: Statt dass der Studio das Book anruft, ruft das Book von sich aus den Studio an — und hält diese Leitung offen. Der Studio kann diese offene Leitung dann jederzeit nutzen, um zurück zum Book zu gelangen."))
story.append(SP(10))

# SSH erklärt
story.append(H1("Was ist SSH?"))
story.append(N("<b>SSH (Secure Shell)</b> ist ein Protokoll für verschlüsselte Verbindungen zwischen Computern. Es ist der Standard für Fernzugriff auf Linux- und Windows-Systeme. Man kann damit:"))
story.append(SP(4))
story.append(B("Befehle auf einem anderen Computer ausführen"))
story.append(B("Dateien übertragen"))
story.append(B("Tunnel aufbauen (Ports weiterleiten)"))
story.append(SP(4))
story.append(N("SSH nutzt Schlüsselpaare zur Authentifizierung: ein <b>privater Schlüssel</b> (bleibt geheim auf dem eigenen Gerät) und ein <b>öffentlicher Schlüssel</b> (wird auf dem Zielgerät hinterlegt). Wer den passenden privaten Schlüssel hat, kommt rein — ohne Passwort."))
story.append(SP(10))

# Die Architektur
story.append(H1("Wie der Tunnel funktioniert"))

table_data = [
    ["Gerät", "Rolle", "IP"],
    ["Surface Laptop Studio (WSL2)", "Heimatbasis, läuft 24/7", "192.168.178.29"],
    ["Surface Book (Windows)", "Mobiles Gerät, baut Tunnel auf", "192.168.178.38 (zuhause)"],
]
table = Table(table_data, colWidths=[6.5*cm, 6.5*cm, 4*cm])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f9f9f9"), colors.white]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
    ("PADDING", (0, 0), (-1, -1), 6),
]))
story.append(table)
story.append(SP(10))

story.append(H2("Schritt für Schritt"))
story.append(N("1. <b>Book baut Verbindung auf:</b> Beim Windows-Start verbindet sich das Book per SSH zum Studio. Es sagt dabei: \"Öffne auf dem Studio Port 2222 und leite alles dort eingehende zu meinem eigenen Port 22 weiter.\""))
story.append(SP(4))
story.append(N("2. <b>Tunnel bleibt offen:</b> Solange das Book läuft und im Internet ist, hält es diese Verbindung aufrecht. Ein Skript stellt die Verbindung automatisch wieder her, falls sie abbricht."))
story.append(SP(4))
story.append(N("3. <b>Bolla greift zurück:</b> Wenn Bolla aufs Book zugreifen will, verbindet er sich einfach zu Port 2222 auf dem eigenen Studio — und landet automatisch auf dem Book."))
story.append(SP(8))

story.append(C("ssh -p 2222 ernst@localhost   # Bolla verbindet sich zum Book"))
story.append(SP(10))

# Was eingerichtet wurde
story.append(H1("Was konkret eingerichtet wurde"))

story.append(H2("Auf dem Surface Laptop Studio (WSL2)"))
story.append(B("OpenSSH Server installiert und gestartet (Port 22)"))
story.append(B("SSH-Schlüsselpaar generiert (~/.ssh/id_ed25519)"))
story.append(B("Windows Port Proxy: Port 2200 auf Windows leitet zu Port 22 in WSL2"))
story.append(B("Windows Firewall: Port 2200 freigegeben"))
story.append(B("Cron-Job: SSH Server startet automatisch beim WSL-Start"))
story.append(SP(6))

story.append(H2("Auf dem Surface Book (Windows)"))
story.append(B("OpenSSH Server installiert und aktiviert (Port 22)"))
story.append(B("SSH-Schlüssel hinterlegt: Studio-Key in administrators_authorized_keys"))
story.append(B("Tunnel-Skript: bolla_tunnel.ps1 unter C:\\Users\\ernst\\"))
story.append(B("Task Scheduler: 'Bolla Tunnel' startet das Skript bei jeder Anmeldung"))
story.append(SP(10))

# Das Tunnel-Skript
story.append(H1("Das Tunnel-Skript (bolla_tunnel.ps1)"))
story.append(N("Dieses PowerShell-Skript läuft dauerhaft im Hintergrund auf dem Book und hält den Tunnel aufrecht:"))
story.append(SP(4))
story.append(C("while ($true) {"))
story.append(C("    ssh -N -R 2222:localhost:22 -p 2200 bolla@192.168.178.29"))
story.append(C("        -o StrictHostKeyChecking=no"))
story.append(C("        -o ServerAliveInterval=30"))
story.append(C("        -o ServerAliveCountMax=3"))
story.append(C("    Start-Sleep -Seconds 15"))
story.append(C("}"))
story.append(SP(4))
story.append(Note("-N = kein Terminal öffnen, nur Tunnel  |  -R = Reverse-Tunnel  |  ServerAliveInterval = Verbindung alle 30s prüfen"))
story.append(SP(10))

# Einschränkungen
story.append(H1("Einschränkungen"))
story.append(N("Der Tunnel funktioniert nur, wenn das Book eine aktive Internetverbindung hat und beim Studio angemeldet ist. Wenn das Book ausgeschaltet oder im Ruhezustand ist, ist Port 2222 auf dem Studio nicht erreichbar."))
story.append(SP(4))
story.append(N("Außerdem muss der Studio dauerhaft laufen — er ist die Schaltzentrale. Das ist bei einem Heimserver (24/7 betrieb) ideal, bei einem Laptop der auch mal aus ist weniger praktisch."))
story.append(SP(10))

story.append(HR())
story.append(Note("Erstellt von Bolla · 2026-04-21 · Surface Laptop Studio / Surface Book"))

doc.build(story)
print(f"PDF erstellt: {OUTPUT}")
