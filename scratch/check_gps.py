import glob, os
from PIL import Image

files = ["f00.jpg", "f05.jpg", "f10.jpg", "f20.jpg", "f30.jpg", "f40.jpg"]
base = "/home/bolla/workspace/mission-control/f-photos"
with_gps = 0
with_exif_no_gps = 0
no_exif = 0
for fn in files:
    path = os.path.join(base, fn)
    im = Image.open(path)
    exif = im._getexif()
    if not exif:
        print(fn, "-> kein EXIF")
        no_exif += 1
        continue
    gps = exif.get(34853)
    if gps:
        print(fn, "-> GPS vorhanden:", dict(gps))
        with_gps += 1
    else:
        print(fn, "-> EXIF da, kein GPS")
        with_exif_no_gps += 1

print("\nZusammenfassung:", with_gps, "mit GPS,", with_exif_no_gps, "EXIF ohne GPS,", no_exif, "kein EXIF")
