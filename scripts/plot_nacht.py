#!/usr/bin/env python3
"""Plot-Umbau AURORA II - Nachtlauf (Chris-Freigabe Cron 16.11.2026). Chris will NICHT gespoilert werden:
Inhalte nur in scratch/plot_umbau/, in Logs/Meldungen NUR Verbrauchszahlen. aurora2.json wird nur gelesen.
Start: nach Fable-Reset (Fable-Balken < 50 % ODER Flag /tmp/fable_reset_geklickt), fruehestens 18:55.
Schritte (je 1 Fable-Aufruf, Checkpoint-Datei): b1 Twist | b2 Red-Team/Verbesserung | b3 Aenderungsplan | b4 Briefings fuer Opus.
Nacht: kein 5h-Reserve (Chris 16.11.), Gate 92 / Obergrenze 98; letzter Start 05:30 (Chris 16.11.: Frist von 04:50 auf 05:30 verschoben, damit Schritt 4 nach dem 5h-Reset ~04:52 noch startet).
Notbremse: touch /tmp/aurora_samstag_stop"""
import datetime as dt, fcntl, os, sys, time
sys.path.insert(0, "/home/bolla/workspace/scripts")
import limit_policy
limit_policy.limits = lambda now=None: (92.0, 98.0)      # Nacht: keine Reserve
limit_policy.week_blocked = lambda q, now=None: False
import samstag_fable_lektorat as F
F.DEADLINE = dt.datetime(2026, 11, 17, 5, 30)
F.WEEK_STOP = 96.0

OUT = "/home/bolla/workspace/scratch/plot_umbau"
J = F.JSON
M = "~/.claude/projects/-home-bolla/memory"
START = dt.datetime(2026, 11, 16, 18, 55)
FLAG = "/tmp/fable_reset_geklickt"
os.makedirs(f"{OUT}/b4_briefings", exist_ok=True)

BASIS = f"""Du bist Fable, Plot-Architekt fuer AURORA II (Roman von Chris Mandel, Band II; Band I = Vorgaenger). Arbeite selbststaendig, keine Rueckfragen. Aendere NICHTS ausser den genannten Ausgabedateien; {J} nur LESEN (Felder: kapitel[i].titel/zusammenfassung/text, kanon, kriterien, protagonisten, antagonisten, nebenfiguren). Lies zuerst {M}/feedback_kreative_individualitaet.md, {M}/feedback_aurora_zahlen_exakt.md, {M}/feedback_aurora_ii_zwei_papiere_benennung.md, {M}/project_aurora_hardcoded_blocks.md, {M}/feedback_aurora_zielgruppe_kein_spoiler.md und {M}/feedback_aurora_ii_humor_standard.md sowie {M}/feedback_aurora_ii_leicht_lesbar.md.
ZIEL DES AUTORS (hoechste Prioritaet): ein VOELLIG UEBERRASCHENDES, SENSATIONELLES Ende. Das bisherige Ende ist ihm zu langweilig, vorhersehbar, nicht spannend genug, ohne echte Ueberraschung - auch fuer ihn als Co-Autor. Band I war ihm schon zu seicht/vorhersagbar. Kapitel vor dem Ende duerfen angefasst oder komplett neu gefasst werden. Humor-Anspruch (Massstab Kap. 10) und Figurenwaerme bleiben. Zielgruppe Frauen; Ton Spannung/Humor/Liebe.
LESBARKEIT MIT ANSPRUCH (Chris-Pflicht 16.11.2026): Chris will AURORA II LEICHTER LESBAR, aber auf literarisch hohem Niveau: Er ist ein guter, qualitativ hochwertiger Schreiber und der Stil darf NIE zum Groschenroman absinken. Es ist ausdruecklich erwuenscht, dass man ab und zu einen Satz langsam lesen muss: dichte, kunstvolle, ironische, mehrschichtige Saetze, Subtext, Rhythmus, lange Saetze mit Bogen und kurze Saetze als Pointe bleiben erhalten. Nichts glaetten, nichts vereinfachen, was gut ist; kein Floskel-Deutsch, keine Allerweltsbilder, kein Erklaerbaer-Ton. Zu beheben sind NUR Stellen, die auch nach aufmerksamem, langsamem Lesen unklar bleiben, weil man raten muss, was gemeint ist: raetselhafte Bildsprueche, die nicht aufgehen (Metapher nur, wenn sie beim Nachdenken sofort Sinn ergibt), Halbsaetze, bei denen das Gemeinte fehlt, ueberladene Schachtelsaetze, die den Faden verlieren, und Motive ohne Einordnung (z. B. Zaehlen von Ja/Nein, Strichliste, 'unentziehbar': beim Auftreten im Text kurz klaeren). Schluesselwoerter, auf die es ankommt, beim Namen nennen. Test: Geht der Satz beim aufmerksamen Lesen auf, ohne dass die Leserin raten muss? Dann bleibt er, auch wenn er Aufmerksamkeit verlangt. Geht er nicht auf, formuliere ihn so um, dass er auf gleichem sprachlichen Niveau aufgeht. Beispiel eines Fehlers: 'Zaehlen muss man, wenn man nicht weiss, wem das Ja gehoert' (Bild geht nicht auf); besser: 'Nachzaehlen muss nur einer, der nicht weiss, ob sein Ja wirklich seins ist. Meins ist meins, und mein Nein auch' (gleicher Ton, geht auf). Humor und Ton bleiben immer erhalten. Der Twist und alle Wendungen muessen fuer normale Leser nachvollziehbar und erklaerbar sein (kein Raetsel-Konstrukt, das man erst mit einer Tabelle versteht). Briefings an Opus enthalten diese Vorgabe, einschliesslich des Qualitaetsanspruchs.
RAHMEN: Fair Play (Leser kann es im Rueckblick erkennen, nicht im Voraus), emotionale Fallhoehe, kein Deus ex machina, kein Trick, der Band I oder bestaetigte Kanon-Fakten bricht; Gesamtumfang bleibt etwa gleich (Ziel ca. 128.000 Woerter, aktuell ca. 132.800), neue Szenen brauchen Kuerzungen an anderer Stelle. Analyse-Vorarbeit: {OUT}/a1_vorhersehbarkeit.md (und was dort noch fehlt, ergaenze selbst)."""

STEPS = [
 ("b1", 40.0, f"""{BASIS}
AUFGABE B1: Entwirf DIE Wendung. Pruefe mindestens 6 verschiedene Ansaetze (auch radikale: Rollen-/Identitaets-/Perspektivwechsel, falsche Erzaehlannahme des Lesers, umgekehrte Kausalitaet, die Hauptfigur selbst als Teil der Loesung), verwirf vorhersehbare, waehle den besten. Schreibe nach {OUT}/b1_twist.md: (1) gewaehlter Twist in 10-15 Saetzen, (2) Warum er ueberrascht UND fair ist, (3) die komplette neue Auflaufstrecke des Schlussakts als Beat-Liste (Kapitel fuer Kapitel, was passiert, wo die Enthuellung sitzt, wo falsche Faehrten liegen), (4) die 6 verworfenen Ansaetze mit Grund (je 1-2 Saetze). Im Chat nur 'fertig'."""),
 ("b2", 40.0, f"""{BASIS}
AUFGABE B2 (Red-Team): Lies {OUT}/b1_twist.md. Greife den Entwurf als misstrauischer, krimierfahrener Leser an: Wo ahnt man ihn? Wo ist er logisch undicht? Wo bricht er Kanon/Band I? Ist es wirklich SENSATIONELL oder nur 'okay'? Verbessere ihn so lange, bis er die Gegenprobe besteht - bei Bedarf Twist deutlich staerker oder anders. Schreibe nach {OUT}/b2_twist_final.md die FINALE Fassung: Twist, Beat-Liste Schlussakt, Setup-/Payoff-Tabelle (welches Detail wird in welchem Kapitel gesaet, wo ausgezahlt), Liste der Risiken. Im Chat nur 'fertig'."""),
 ("b3", 40.0, f"""{BASIS}
AUFGABE B3: Lies {OUT}/b2_twist_final.md. Erstelle nach {OUT}/b3_aenderungsplan.md den kapitelgenauen Aenderungsplan fuer ALLE 38 Kapitel: je Kapitel Eintrag 'unveraendert' | 'Setup einflechten (genau welche Saetze/Stellen)' | 'Szene aendern' | 'komplett neu fassen' mit knapper Begruendung, neuer Wortzahl-Schaetzung und Konsistenzfolgen (welche anderen Kapitel/Zahlen/Daten betroffen). Am Ende: Gesamtwortbilanz und empfohlene Reihenfolge der Umsetzung. Beachte schon eingebaute blaue Einschuebe (Humor) in den Kapiteln - sie nicht beschaedigen. Im Chat nur 'fertig'."""),
 ("b4", 40.0, f"""{BASIS}
AUFGABE B4: Lies {OUT}/b2_twist_final.md und {OUT}/b3_aenderungsplan.md. Schreibe fuer JEDES Kapitel, das dort Aenderungen hat, ein praezises Umsetzungs-Briefing nach {OUT}/b4_briefings/kapNN.md (NN zweistellig), so dass ein anderes Modell (Opus) es ohne eigene Plotentscheidung umsetzen kann: Ziel des Kapitels, exakte Beats, Pflichtsaetze/Schluesselzeilen woertlich, zu erhaltende Humor-Stellen, Figurenstimmen, Zahlen/Daten, Uebergaenge zum Vorher/Nachher-Kapitel; ausserdem in JEDEM Briefing wortgleich die Vorgabe an Opus: 'Schreibe auf hohem literarischem Niveau (kein Groschenroman, Stil nicht glaetten; Saetze duerfen Aufmerksamkeit verlangen), aber so, dass jede Stelle beim aufmerksamen Lesen aufgeht: keine raetselhaften Bildsprueche, die nicht aufgehen, keine Halbsaetze ohne erkennbares Gemeintes, Schluesselwoerter beim Namen nennen, Motive im Text kurz einordnen. Rhythmus und Humor bleiben (Chris-Pflicht).' Bei 'komplett neu fassen' zusaetzlich Absatz fuer Absatz Gliederung und 3-5 Beispiel-Humorpointen im Stil von Kap. 10. Beginne mit den wichtigsten (Enthuellung, Schlussakt) und arbeite die uebrigen ab; wenn Platz fehlt, schreibe nach {OUT}/b4_briefings/_offen.md welche Kapitel noch fehlen. Im Chat nur 'fertig'."""),
]


def main():
    lock = open("/tmp/plot_nacht.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return
    if all(os.path.exists(f"{OUT}/_done_{n}") for n, _, _ in STEPS):
        return
    fb = None
    while True:                                   # Warten auf Reset-Klick
        now = dt.datetime.now()
        if os.path.exists("/tmp/aurora_samstag_stop") or now >= F.DEADLINE:
            F.log("plot_nacht: Notbremse/Deadline vor Start")
            return
        fb = F.fable_pct()
        if now >= START and (os.path.exists(FLAG) or (fb is not None and fb < 50)):
            break
        time.sleep(300)
    F.log(f"plot_nacht: Start (Fable-Balken {fb}, Flag {os.path.exists(FLAG)})")
    outs = {"b1": "b1_twist.md", "b2": "b2_twist_final.md", "b3": "b3_aenderungsplan.md"}
    for name, est, prompt in STEPS:
        if os.path.exists(f"{OUT}/_done_{name}"):
            continue
        ok, d5 = F.run_fable(f"plot_{name}", prompt, est_pp=est, timeout=3000)
        if ok and (name == "b4" or os.path.exists(f"{OUT}/{outs[name]}")):
            open(f"{OUT}/_done_{name}", "w").write(f"{time.ctime()} d5h={d5}\n")
        else:
            F.log(f"plot_nacht: {name} ohne Ergebnis/Stopp -> Ende (naechster --ensure-Lauf versucht es erneut)")
            return
    F.log("plot_nacht: alle Schritte fertig")


if __name__ == "__main__":
    main()
