#!/usr/bin/env python3
"""Production run: add students from old org groups (6a-6d, old-7c) into the new
7a/7b/7c/7d I/II EDV courses for Schuljahr 26/27. See fork directive for full context."""
import sys

sys.path.insert(0, "/home/bolla/workspace/scripts")
from itslearning_post_kurstag import login, OUT_DIR

COURSES = {
    "7a I": 190735, "7a II": 190738,
    "7b I": 190741, "7b II": 190743,
    "7c I": 190861, "7c II": 190878,
    "7d I": 190860, "7d II": 190877,
}

# (source_group_label, target_course, [exact display names as "Nachname[...], Vorname"])
JOBS = [
    ("6a", "7a I", [
        "Amoabing, Lordina", "Baloshi, Anesti", "Brandt, Haley", "Bronnert, Oskar",
        "Dohse, Alva", "Ehlert, Ben", "Frost, Amon", "Hausch, Joana", "Höfs, Mia",
        "Hutterer, Merle", "Jimenez Bernat, Laura", "Klein, Jasmin", "Kremer, Jamal",
        "Ludewig, Thomas",
    ]),
    ("6a", "7a II", [
        "Meinecke, Sophie", "Meyer, Lene", "Mielke, Tammo", "Möller, Felix",
        "Otte, Greta-Marie", "Petersen, Mika", "Piankov, Artjom", "Seyrek, Esma",
        "Stacke, Maximilian", "von Holt, Henning", "Waniewski, Marie",
        "Zlotopolski, Aren", "Zlotopolski, Tron", "Zock, Henny",
    ]),
    ("6b", "7b I", [
        "Bartz, Joëlle", "Bott, Lasse", "Bozhdaraj, Albina", "Bratke, Henri",
        "Bunsen, Lukas", "Exner, Mia", "Frank, Henri", "Henneberg, Mika",
        "Hölzel, Niklas", "Meisel, Nelly", "Mengden, Annemieke",
    ]),
    ("6b", "7b II", [
        "Michel, Emma", "Mielke, Oscar", "Muntean, Luan", "Pietschner, Emma",
        "Rittmüller, Chiara", "Schultze, Malija", "Schweiz, Enrico", "Sidhu, Kulraj",
        "Sielaff, Marni", "Ullrich, Neele", "Wulff, Levian",
    ]),
    ("6c", "7c I", [
        "Becker, Elisa", "Bienvenu, Louis", "Brühl, Lena-Sophie", "Do, Philip",
        "Friese, Morten", "Greß, Amelie", "Güven, Meltem", "Hagen, Marie",
        "Harms, Lea", "Helt, Julian", "Herweg, Lasse", "Holz, Emily", "Kaschka, Samuel",
    ]),
    ("6c", "7c II", [
        "Kunstmann Martinez, Evelyn", "Ljubas, Stella", "Mumm, Maarten", "Özdemir, Ayaz",
        "Reimers, Nayla", "Reinhold, Felix", "Schiele, Emily", "Schwansee, Kilian",
        "Sombrowski, Leo", "Urak, Ceyda", "Wagner, Annika", "Wassermann, Eva",
        "Yildirim, Nilay",
    ]),
    ("6d", "7d I", [
        "Al-Maliki, Jna", "Almoghrabi, Maria", "Gerlich, Jim", "Hecker, Alice",
        "Heinemann, Theo", "Helmes, Lilly", "Hirsch, Rasmus", "Hofmann, Paulina",
        "Koshkina, Daria", "Krätzschmar, Amelie", "Kuhn, Thore", "Li, Noah",
        "Löwe, Felix", "Pfeffer, Emma",
    ]),
    ("6d", "7d II", [
        "Popp, Ilvy", "Raguse, Marie", "Rakowski, Alexander", "Renger, Ben",
        "Scholz, Matilda", "Schwartau, Line", "Schwarz, Amelie", "Seiler, Leonie",
        "Spille, Julius", "Szameitat, Jacob", "Thiedeitz, Liv", "Timpner, Hanah",
        "Wagner, Frederik", "Wolf, Arthur",
    ]),
]

SKIPPED_KNOWN = {
    "6a": ["Benken, Jacob (nicht promoviert)"],
    "6b": ["Gödecke, Felix", "Mahboub Nikou, Taha", "Mehra, Avni", "Stöver, Lukas",
           "Timm, Marie", "Zuther, Louisa", "Lagerpusch, Alea (in KEINER geprueften Gruppe gefunden: 6a-6d, alte 7a/7b/7c, globale Suche - uebersprungen)"],
    "6c": ["Reimer, Konstantin (nicht promoviert, Vorsicht Verwechslung mit Reimers)"],
    "6d": [],
}


def open_group(its, course_id, group_label):
    its.goto(f"https://moin.itslearning.com/CourseParticipantsV2/AddParticipants?CourseID={course_id}&selectedTabIndex=0",
              timeout=20000)
    its.wait_for_timeout(1800)
    its.get_by_text("Filter", exact=True).first.click()
    its.wait_for_timeout(1200)
    li = its.locator("li")
    target = None
    for i in range(li.count()):
        t = li.nth(i).inner_text().strip()
        if t.startswith(group_label + "\n") or t == group_label:
            target = li.nth(i)
            break
    if target is None:
        return False
    target.click()
    its.wait_for_timeout(1200)
    sel = its.locator("select").first
    if sel.count() > 0:
        try:
            sel.select_option("50")
            its.wait_for_timeout(1000)
        except Exception:
            pass
    return True


def add_person(its, name):
    row = its.locator("li").filter(has_text=name)
    if row.count() == 0:
        return "NICHT GEFUNDEN"
    # pick the row whose first line matches exactly (avoid partial collisions)
    match = None
    for i in range(row.count()):
        first_line = row.nth(i).inner_text().split("\n")[0].strip()
        if first_line == name:
            match = row.nth(i)
            break
    if match is None:
        match = row.first
    txt_before = match.inner_text()
    if "hinzugefügt" in txt_before:
        return "BEREITS VORHANDEN"
    add_link = match.get_by_text("Person hinzufügen", exact=False)
    if add_link.count() == 0:
        return "KEIN ADD-LINK"
    add_link.first.click()
    its.wait_for_timeout(900)
    txt_after = match.inner_text()
    if "hinzugefügt" in txt_after:
        return "OK"
    return f"UNSICHER (nachher: {txt_after[:80]!r})"


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    results = {}
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            for source_group, target_name, names in JOBS:
                course_id = COURSES[target_name]
                print(f"\n=== {source_group} -> {target_name} (CourseID {course_id}) ===")
                ok = open_group(its, course_id, source_group)
                if not ok:
                    print(f"  ❌ Gruppe '{source_group}' im Filterbaum nicht gefunden!")
                    results[(source_group, target_name)] = [("GRUPPE NICHT GEFUNDEN", "-")]
                    continue
                job_results = []
                for name in names:
                    res = add_person(its, name)
                    print(f"  {name}: {res}")
                    job_results.append((name, res))
                results[(source_group, target_name)] = job_results
        finally:
            browser.close()

    print("\n\n=== GESAMTZUSAMMENFASSUNG ===")
    ok_count = 0
    problem_count = 0
    for (sg, tn), job_results in results.items():
        for name, res in job_results:
            if res == "OK":
                ok_count += 1
            else:
                problem_count += 1
                print(f"PROBLEM: {sg}->{tn}: {name}: {res}")
    print(f"\nErfolgreich hinzugefuegt: {ok_count}, Probleme: {problem_count}")

    print("\n=== FINALE PERSONENZAHL PRO KURS ===")
    with sync_playwright() as p:
        browser, its = login(p)
        try:
            for name, cid in COURSES.items():
                its.goto(f"https://moin.itslearning.com/CourseParticipantsV2?CourseID={cid}", timeout=20000)
                its.wait_for_timeout(1500)
                rows = its.locator("li").filter(has_text="Schüler")
                print(f"{name}: {rows.count()} Schüler-Zeilen im Personen-Tab")
        finally:
            browser.close()
