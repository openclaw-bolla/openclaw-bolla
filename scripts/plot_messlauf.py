#!/usr/bin/env python3
"""Plot-Umbau AURORA II, Teil A (Messlauf, 16.11.2026): Vorhersehbarkeits-Check Schlussakt.
Ergebnis nur als Datei in scratch/plot_umbau/ (Chris will NICHT gespoilert werden -> nichts melden). aurora2.json wird nur gelesen."""
import os, sys, time
sys.path.insert(0, "/home/bolla/workspace/scripts")
import samstag_fable_lektorat as F

OUT = "/home/bolla/workspace/scratch/plot_umbau"
os.makedirs(OUT, exist_ok=True)
J = F.JSON
PROMPT = f"""Du bist Fable, Plot-Architekt fuer AURORA II (Roman von Chris Mandel, Band II der AURORA-Reihe). Arbeite selbststaendig, keine Rueckfragen. Aendere NICHTS ausser den hier genannten Ausgabedateien; {J} nur LESEN.

ZIEL des Autors: Ein voellig ueberraschendes, sensationelles Ende. Das jetzige Ende ist ihm zu langweilig, vorhersehbar, nicht spannend genug und ohne echte Ueberraschung - auch fuer ihn als Co-Autor. Auch Band I war ihm zu seicht/vorhersagbar. Kapitel davor duerfen angefasst oder komplett neu gefasst werden; der Humor-Anspruch (Maßstab Kap. 10) bleibt.

MATERIAL: {J} (Liste 'kapitel'; je Kapitel Felder titel, zusammenfassung, text), Felder 'kanon', 'protagonisten', 'antagonisten', 'nebenfiguren'; Gutachten {F.OUT}/gutachten.md; Humor-Karte {F.OUT}/humor_karte.md. Lies die Zusammenfassungen aller 38 Kapitel und den Volltext der Kapitel 28-38 (per Bash/python aus der JSON ausgeben, kapitelweise). Nicht das ganze Buch im Volltext lesen.

AUFGABE TEIL A (schreibe das Ergebnis nach {OUT}/a1_vorhersehbarkeit.md):
1. Kurz: Was passiert im Schlussakt (Kap. 28-38), welche Fragen/Erwartungen baut das Buch beim Leser auf?
2. Vorhersehbarkeits-Check: Fuer jede Stelle, an der ein aufmerksamer Leser die Aufloesung ahnt: wo, warum (welcher Hinweis/Trope), wie sicher.
3. Was das Ende schwach macht (Spannungsbogen, fehlende Fallhoehe, Erwartungserfuellung ohne Bruch).
4. Fuer die Kapitel 1-27: welche Figuren/Faeden/Objekte eignen sich als verborgene Setups fuer eine echte Wendung (ohne sie jetzt zu erfinden)?
5. Gib am Ende 3 knappe Twist-RICHTUNGEN (je 3-5 Saetze), die wirklich ueberraschen und trotzdem fair vorbereitet werden koennen, und empfiehl eine. Kein Umschreiben des Buchtextes.
Antworte im Chat nur mit 'fertig'."""

if __name__ == "__main__":
    ok, d5 = F.run_fable("plot_teil_a", PROMPT, est_pp=14.0, timeout=2400)
    open(f"{OUT}/_messung.txt", "w").write(f"ok={ok} delta5h={d5}\n{time.ctime()}\n")
