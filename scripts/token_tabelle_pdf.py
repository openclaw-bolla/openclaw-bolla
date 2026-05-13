#!/usr/bin/env python3
"""Erstellt Token-Verbrauch-Tabelle als PDF auf dem Desktop."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import datetime

OUTPUT = "/mnt/d/OneDrive/Desktop/Bolla_Token_Verbrauch.pdf"

# ── Farben (passend zum MC-Stil) ──
COL_BG       = colors.HexColor('#0d1117')
COL_CARD     = colors.HexColor('#1a1f2e')
COL_ACCENT   = colors.HexColor('#ff6699')
COL_GREEN    = colors.HexColor('#22c55e')
COL_YELLOW   = colors.HexColor('#f59e0b')
COL_ORANGE   = colors.HexColor('#f97316')
COL_RED      = colors.HexColor('#ef4444')
COL_PURPLE   = colors.HexColor('#a78bfa')
COL_CYAN     = colors.HexColor('#06b6d4')
COL_BRIGHT   = colors.HexColor('#f0f6fc')
COL_DIM      = colors.HexColor('#8b949e')
COL_ZERO     = colors.HexColor('#1e3a2f')   # dunkelgrün für 0-Token-Zeilen
COL_LOW      = colors.HexColor('#1a2d1a')
COL_MID      = colors.HexColor('#2d2010')
COL_HIGH     = colors.HexColor('#2d1a0a')
COL_CRIT     = colors.HexColor('#2d0f0f')

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm,
    title="Bolla Token-Verbrauch",
    author="Bolla / Claude Code"
)

styles = getSampleStyleSheet()
normal = styles['Normal']

def P(text, size=10, color=COL_BRIGHT, bold=False, align=TA_LEFT):
    return Paragraph(
        f'<font color="#{color.hexval()[2:]}" size="{size}">{"<b>" if bold else ""}{text}{"</b>" if bold else ""}</font>',
        ParagraphStyle('x', parent=normal, alignment=align, leading=size*1.4)
    )

# ── Tabellen-Daten ──────────────────────────────────────────────────────────
# Spalten: Aktivität | Kategorie | Verbrauch (% Budget) | Bewertung | Hinweise

HEADERS = ["Aktivität / Session-Typ", "Kategorie", "Budget-Anteil\n(ca.)", "Niveau", "Hinweise & Tipps"]

rows = [
    # (Aktivität, Kategorie, %, Niveau, Hinweise, row_color)

    # ── KEIN VERBRAUCH ──
    ("Studio schläft / PC aus",
     "Inaktiv",
     "0 %",
     "✅ Null",
     "Keine aktive Claude-Session → kein Token-Verbrauch",
     COL_ZERO),

    ("Crons: Telegram-Bot, MC-Server,\nCloudflare-Tunnel",
     "Autonome Services",
     "0 %",
     "✅ Null",
     "Eigenständige Python-Prozesse, völlig unabhängig von Claude",
     COL_ZERO),

    ("Spam-Watcher, Newsletter-Scanner,\nHealthchecks, Backups, Aimor-Push",
     "Autonome Crons",
     "0 %",
     "✅ Null",
     "Laufen alle 2–15 Min per Cron, kein Claude-Aufruf",
     COL_ZERO),

    # ── MINIMAL ──
    ("Einfache Frage / kurze Info\n(z.B. Uhrzeit, Status, Erklärung)",
     "Kurze Anfrage",
     "< 0,5 %",
     "💚 Minimal",
     "~5–20k Tokens; kurzer Kontext, kurze Antwort",
     COL_LOW),

    ("Cron-Job einrichten oder ändern\n(z.B. neuer Backup-Zeitplan)",
     "Konfiguration",
     "0,5–1 %",
     "💚 Minimal",
     "~20–60k Tokens; wenige Dateien, klare Aufgabe",
     COL_LOW),

    ("Systemstatus prüfen\n(Logs lesen, Service neu starten)",
     "Diagnose",
     "0,5–1 %",
     "💚 Minimal",
     "~20–70k Tokens; Bash-Befehle + kurze Auswertung",
     COL_LOW),

    # ── NIEDRIG ──
    ("Mail / Brief schreiben\n(z.B. Robin-Mail, Elternbrief)",
     "Text-Erstellung",
     "1–3 %",
     "🟡 Niedrig",
     "~60–200k Tokens; steigt mit Iterationen und Korrekturen",
     COL_MID),

    ("Suno-Songs abholen + Cover herunterladen\n(PiAPI-Calls, Batch < 5 Songs)",
     "API-Workflow",
     "1–3 %",
     "🟡 Niedrig",
     "~50–180k Tokens; PiAPI-Calls selbst kosten keine Claude-Tokens",
     COL_MID),

    ("Kleines Windows/WSL-Problem lösen\n(z.B. GamingServices, Treiber-Fix)",
     "System-Fix",
     "1–2 %",
     "🟡 Niedrig",
     "~50–150k Tokens; klar begrenzte Aufgabe",
     COL_MID),

    ("aktuell.md + Memory updaten,\nGit-Commit, OneDrive-Backup",
     "Session-Ende-Routine",
     "0,5–1,5 %",
     "💚 Minimal",
     "~30–100k Tokens; gut für Tage mit knappem Budget",
     COL_LOW),

    # ── MITTEL ──
    ("Suno-Batch: 15–20 Songs + Cover\n(Prompt-Engineering, Stil, Titel)",
     "KI-Kreativ",
     "5–10 %",
     "🟠 Mittel",
     "~400–800k Tokens; viele Iterationen, Qualitäts-Checks",
     COL_HIGH),

    ("Neuen API-Endpunkt bauen\n(z.B. /api/recipe, /api/transcribe)",
     "Backend-Dev",
     "3–8 %",
     "🟠 Mittel",
     "~200–600k Tokens; steigt stark wenn Fehler auftreten",
     COL_HIGH),

    ("Schularbeits-Korrektur-Feature\n(Scan → Analyse → Word-Export)",
     "KI-Feature",
     "5–12 %",
     "🟠 Mittel",
     "~400–1M Tokens; Claude-subprocess + viele Dateien",
     COL_HIGH),

    # ── HOCH ──
    ("WISO-Automation (Duplikat-Cleanup\n3.400+ Adressen, pyautogui/pywinauto)",
     "Komplexes Debugging",
     "8–15 %",
     "🔴 Hoch",
     "~600k–1,5M Tokens; viele Iterationen, WPF-spezifische Probleme",
     COL_CRIT),

    ("Neue MC-Seite entwickeln\n(z.B. Foto-Analyse, Elternbrief-Entschärfer)",
     "Frontend-Dev",
     "8–18 %",
     "🔴 Hoch",
     "~700k–1,5M Tokens; HTML/CSS/JS, mehrere Debugging-Runden",
     COL_CRIT),

    ("Whisper/Mic-Setup (CUDA, ffmpeg,\nAudioContext, Stille-Erkennung)",
     "Infra-Setup",
     "10–20 %",
     "🔴 Hoch",
     "~800k–1,8M Tokens; Library-Konflikte, Pfad-Probleme, testen",
     COL_CRIT),

    # ── KRITISCH ──
    ("UI-Debugging mit vielen Iterationen\n(z.B. Sidebar Drag & Drop, CSS-Epics)",
     "UI-Debugging",
     "15–30 %",
     "🚨 Kritisch",
     "~1–3M Tokens; jede Runde liest die ganze 9000-Zeilen-HTML neu",
     COL_CRIT),

    ("Foto-Analyse-Seite entwickeln\n(8k Fotos, LM Studio, Search-Bugs)",
     "KI + Frontend",
     "15–25 %",
     "🚨 Kritisch",
     "~1,2–2,5M Tokens; komplexer Prompt-Flow + viele UI-Bugs",
     COL_CRIT),

    ("Multi-Session-Woche: täglich\ngröße neue Features + Debugging",
     "Intensiv-Woche",
     "80–120 %",
     "🚨 Limit!",
     "Wie diese Woche — Plan: große Tasks auf Mo/Di legen, Do/Fr ruhiger",
     COL_CRIT),
]

# ── Vergleichs-Referenz ─────────────────────────────────────────────────────
ref_rows = [
    ("Harmlose Session: Status abfragen,\naktuell.md lesen, kurze Antwort",
     "Referenz niedrig", "~0,5 %", "💚", "Ideal für Tage mit wenig Budget"),
    ("Mittlere Session: eine Funktion\nfixieren, einen Endpunkt anpassen",
     "Referenz mittel", "~3–6 %", "🟡", "Gut planbar, klares Ergebnis"),
    ("Große Session: komplettes Feature\nvon Grund auf neu bauen",
     "Referenz hoch", "~12–20 %", "🔴", "Lieber auf Wochenanfang legen"),
]

story = []

# ── Titel ───────────────────────────────────────────────────────────────────
title_style = ParagraphStyle(
    'title', parent=normal,
    fontSize=18, textColor=COL_ACCENT, leading=24,
    spaceAfter=4, fontName='Helvetica-Bold'
)
sub_style = ParagraphStyle(
    'sub', parent=normal,
    fontSize=10, textColor=COL_DIM, leading=14, spaceAfter=14
)

story.append(Paragraph("⚡ Bolla — Token-Verbrauch nach Aktivität", title_style))
story.append(Paragraph(
    f"Erstellt: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} Uhr  ·  "
    f"Stand: 78% des Wochenbudgets verbraucht (Samstag 10.05. bis Mittwoch 13.05.)  ·  Reset: Samstag 23:59",
    sub_style
))
story.append(HRFlowable(width="100%", thickness=1, color=COL_ACCENT, spaceAfter=14))

# ── Erklärung ────────────────────────────────────────────────────────────────
info_style = ParagraphStyle(
    'info', parent=normal,
    fontSize=9.5, textColor=COL_BRIGHT, leading=14,
    backColor=colors.HexColor('#1a1a2e'),
    borderPadding=(8, 10, 8, 10),
    spaceAfter=14
)
story.append(Paragraph(
    "<b>Wichtig:</b> Claude-Tokens entstehen <b>nur</b> wenn Claude Code aktiv in einer Session läuft. "
    "Cron-Jobs, Telegram-Bot, Cloudflare-Tunnel und alle autonomen Scripts verbrauchen <b>0 Tokens</b> — "
    "die laufen völlig unabhängig. Jede Nachricht in einer langen Session liest den gesamten "
    "bisherigen Kontext mit → lange Sessions werden exponentiell teurer.",
    info_style
))

# ── Haupt-Tabelle ──────────────────────────────────────────────────────────
col_widths = [5.2*cm, 3.0*cm, 2.5*cm, 2.2*cm, 5.8*cm]

header_style = ParagraphStyle('h', parent=normal, fontSize=8.5, textColor=COL_BRIGHT,
                               fontName='Helvetica-Bold', leading=11)
cell_style   = ParagraphStyle('c', parent=normal, fontSize=8.5, textColor=COL_BRIGHT, leading=11.5)
dim_style    = ParagraphStyle('d', parent=normal, fontSize=8,   textColor=COL_DIM,   leading=11)
pct_style    = ParagraphStyle('p', parent=normal, fontSize=9,   textColor=COL_BRIGHT,
                               fontName='Helvetica-Bold', leading=12, alignment=TA_CENTER)

table_data = [[
    Paragraph(h, header_style) for h in HEADERS
]]

row_colors = []
for i, (akt, kat, pct, niv, hint, bg) in enumerate(rows):
    table_data.append([
        Paragraph(akt, cell_style),
        Paragraph(kat, dim_style),
        Paragraph(pct, pct_style),
        Paragraph(niv, ParagraphStyle('n', parent=normal, fontSize=8.5, textColor=COL_BRIGHT, leading=11, alignment=TA_CENTER)),
        Paragraph(hint, dim_style),
    ])
    row_colors.append(('BACKGROUND', (0, i+1), (-1, i+1), bg))

base_cmds = [
    # Header
    ('BACKGROUND',  (0, 0), (-1, 0), colors.HexColor('#1e1030')),
    ('TEXTCOLOR',   (0, 0), (-1, 0), COL_ACCENT),
    ('FONTNAME',    (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE',    (0, 0), (-1, 0), 9),
    ('TOPPADDING',  (0, 0), (-1, 0), 7),
    ('BOTTOMPADDING',(0,0), (-1, 0), 7),
    # Alle Zellen
    ('FONTNAME',    (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE',    (0, 1), (-1, -1), 8.5),
    ('TOPPADDING',  (0, 1), (-1, -1), 5),
    ('BOTTOMPADDING',(0,1), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ('RIGHTPADDING',(0, 0), (-1, -1), 7),
    # Gitter
    ('GRID',        (0, 0), (-1, -1), 0.4, colors.HexColor('#2d333b')),
    ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
    # Trennlinien zwischen Kategorieblöcken
    ('LINEABOVE',   (0, 4),  (-1, 4),  1.0, colors.HexColor('#22c55e')),
    ('LINEABOVE',   (0, 8),  (-1, 8),  1.0, COL_YELLOW),
    ('LINEABOVE',   (0, 12), (-1, 12), 1.0, COL_ORANGE),
    ('LINEABOVE',   (0, 16), (-1, 16), 1.0, COL_RED),
]
ts = TableStyle(base_cmds + row_colors)

main_table = Table(table_data, colWidths=col_widths, repeatRows=1)
main_table.setStyle(ts)
story.append(main_table)
story.append(Spacer(1, 0.5*cm))

# ── Separator ────────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=1, color=COL_DIM, spaceAfter=10))
sec_style = ParagraphStyle('sec', parent=normal, fontSize=11, textColor=COL_CYAN,
                            fontName='Helvetica-Bold', spaceAfter=8, leading=14)
story.append(Paragraph("📊 Vergleichs-Referenz: 3 typische Sessions", sec_style))

ref_data = [[
    Paragraph(h, header_style) for h in ["Session-Typ", "Kategorie", "Budget-Anteil", "Niveau", "Hinweis"]
]]
ref_row_colors = []
for i, (akt, kat, pct, niv, hint) in enumerate(ref_rows):
    bg = COL_LOW if i == 0 else (COL_MID if i == 1 else COL_CRIT)
    ref_data.append([
        Paragraph(akt, cell_style),
        Paragraph(kat, dim_style),
        Paragraph(pct, pct_style),
        Paragraph(niv, ParagraphStyle('n2', parent=normal, fontSize=9, textColor=COL_BRIGHT, leading=12, alignment=TA_CENTER)),
        Paragraph(hint, dim_style),
    ])
    ref_row_colors.append(('BACKGROUND', (0, i+1), (-1, i+1), bg))

ref_ts = TableStyle([
    ('BACKGROUND',  (0, 0), (-1, 0), colors.HexColor('#0a1628')),
    ('FONTNAME',    (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE',    (0, 0), (-1, -1), 9),
    ('TOPPADDING',  (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING',(0,0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ('RIGHTPADDING',(0, 0), (-1, -1), 7),
    ('GRID',        (0, 0), (-1, -1), 0.4, colors.HexColor('#2d333b')),
    ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
] + ref_row_colors)

ref_table = Table(ref_data, colWidths=col_widths, repeatRows=1)
ref_table.setStyle(ref_ts)
story.append(ref_table)
story.append(Spacer(1, 0.4*cm))

# ── Sparplan ─────────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=1, color=COL_ORANGE, spaceAfter=10))
story.append(Paragraph("💡 Sparplan für knappe Budgetwochen", sec_style))

tips_data = [
    ["Wann", "Was tun / Was vermeiden"],
    ["Mo–Di\n(Budget frisch)", "✅ Große Features, neue Seiten, komplexes Debugging → jetzt erledigen"],
    ["Mi–Do\n(Budget 40–60%)", "⚠️  Mittlere Aufgaben OK · Keine neuen epischen Sessions starten"],
    ["Do–Fr\n(Budget > 70%)", "🔶  Nur kleine Fixes, Fragen, Konfigurationen · UI-Debugging verschieben"],
    ["Fr–Sa\n(Budget > 85%)", "🚨  Nur Notwendigstes · Crons laufen eigenständig · Session kurz halten"],
    ["Täglich\nimmer möglich", "✅  Status-Checks, Mail lesen, kurze Fragen, aktuell.md · kostet kaum was"],
    ["Token sparen\nsofort wirksam", "📝  Kurze klare Prompts · Nicht zu weit scrollen/suchen lassen · Session beenden wenn fertig"],
]

tips_ts = TableStyle([
    ('BACKGROUND',  (0, 0), (-1, 0), colors.HexColor('#1e1030')),
    ('TEXTCOLOR',   (0, 0), (-1, 0), COL_ORANGE),
    ('FONTNAME',    (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE',    (0, 0), (-1, -1), 9),
    ('TOPPADDING',  (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING',(0,0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING',(0, 0), (-1, -1), 8),
    ('GRID',        (0, 0), (-1, -1), 0.4, colors.HexColor('#2d333b')),
    ('VALIGN',      (0, 0), (-1, -1), 'TOP'),
    ('BACKGROUND',  (0, 1), (-1, 1), colors.HexColor('#1a2d1a')),
    ('BACKGROUND',  (0, 2), (-1, 2), colors.HexColor('#232010')),
    ('BACKGROUND',  (0, 3), (-1, 3), colors.HexColor('#2d1e08')),
    ('BACKGROUND',  (0, 4), (-1, 4), colors.HexColor('#2d0f0f')),
    ('BACKGROUND',  (0, 5), (-1, 5), colors.HexColor('#1a2d1a')),
    ('BACKGROUND',  (0, 6), (-1, 6), colors.HexColor('#1a1f2e')),
    ('TEXTCOLOR',   (0, 1), (0, -1), COL_DIM),
    ('TEXTCOLOR',   (1, 1), (1, -1), COL_BRIGHT),
    ('FONTNAME',    (0, 1), (0, -1), 'Helvetica-Bold'),
])

tips_table_data = [[Paragraph(r[0], dim_style), Paragraph(r[1], cell_style)] for r in tips_data]
tips_table = Table(tips_table_data, colWidths=[3.0*cm, 15.7*cm])
tips_table.setStyle(tips_ts)
story.append(tips_table)

story.append(Spacer(1, 0.4*cm))
footer_style = ParagraphStyle('ft', parent=normal, fontSize=8, textColor=COL_DIM,
                               alignment=TA_CENTER, leading=11)
story.append(Paragraph(
    "🐾 Bolla — erstellt am " + datetime.datetime.now().strftime('%d.%m.%Y') +
    "  ·  Schätzwerte auf Basis bisheriger Sessions  ·  Absolute Token-Zahlen nicht von Anthropic disclosed",
    footer_style
))

doc.build(story)
print(f"PDF erstellt: {OUTPUT}")
