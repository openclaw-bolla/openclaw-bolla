from PIL import Image, ImageDraw

SRC = "/home/bolla/workspace/bolla_avatar_new.png"
OUT = "/home/bolla/workspace/aurora-story/assets"
S = 512

# --- Hintergrund: diagonaler Verlauf Nacht -> Glut (Seitenfarben) ---
nacht = (13, 27, 61)
glut = (138, 74, 107)
bg = Image.new("RGB", (S, S))
px = bg.load()
for y in range(S):
    for x in range(0, S, 1):
        t = (x + y) / (2 * S)  # diagonal
        r = round(nacht[0] + (glut[0] - nacht[0]) * t)
        g = round(nacht[1] + (glut[1] - nacht[1]) * t)
        b = round(nacht[2] + (glut[2] - nacht[2]) * t)
        px[x, y] = (r, g, b)
bg = bg.convert("RGBA")

# --- Bolla laden, transparenten Rand wegtrimmen ---
bolla = Image.open(SRC).convert("RGBA")
bbox = bolla.getbbox()
if bbox:
    bolla = bolla.crop(bbox)
# auf ~82% der Canvasbreite skalieren
w = round(S * 0.82)
h = round(bolla.height * w / bolla.width)
bolla = bolla.resize((w, h), Image.LANCZOS)
# zentriert, leicht nach oben (Kopf betonen)
ox = (S - w) // 2
oy = (S - h) // 2 - round(S * 0.02)
bg.alpha_composite(bolla, (ox, oy))

# --- runde Ecken (dezent) ---
radius = round(S * 0.18)
mask = Image.new("L", (S, S), 0)
d = ImageDraw.Draw(mask)
d.rounded_rectangle([0, 0, S - 1, S - 1], radius=radius, fill=255)
icon = Image.new("RGBA", (S, S), (0, 0, 0, 0))
icon.paste(bg, (0, 0), mask)

# --- Ausgaben ---
icon.save(f"{OUT}/icon-512.png")
icon.resize((192, 192), Image.LANCZOS).save(f"{OUT}/icon-192.png")
icon.resize((180, 180), Image.LANCZOS).save(f"{OUT}/apple-touch-icon.png")
icon.resize((32, 32), Image.LANCZOS).save(f"{OUT}/icon-32.png")
# .ico mit mehreren Groessen
icon.save(f"{OUT}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("Favicons erstellt in", OUT)
