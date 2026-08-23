import subprocess
r = subprocess.run(
    ["claude", "-p",
     "Lies das Bild /home/bolla/workspace/scratch/test_page1.jpg. Das ist eine Seite aus einem "
     "Aldi-Nord-Prospekt. Extrahiere ALLE Produkte mit Preis. Antworte NUR mit einem JSON-Array: "
     '[{"name":"...","brand":"...","price":1.99,"old_price":null,"valid_from":"TT.MM.","valid_to":"TT.MM."}]. '
     "Kein Text außerhalb des JSON."],
    capture_output=True, text=True, timeout=120)
print("RC:", r.returncode)
print("STDOUT:", r.stdout[:3000])
print("STDERR:", r.stderr[:1000])
