# Vorverarbeitung fuer das AURORA-Partikelvideo: Zielpunkte Gesicht I (Cover I) + Gesicht II (Cover II) -> data.npz
# python3 aurora_partikel_prep.py [Zielspalten] -> /mnt/c/Tools/blender_proj/aurora_partikel/data.npz + Vorschau-PNGs
import numpy as np, sys, os
from PIL import Image, ImageFilter, ImageDraw
COLS = int(sys.argv[1]) if len(sys.argv) > 1 else 220
OUT = "/mnt/c/Tools/blender_proj/aurora_partikel/"; os.makedirs(OUT, exist_ok=True)
C1 = "/mnt/d/OneDrive/Dokumente/Bolla/AURORA/2_eBook/AURORA_Cover.jpg"
C2 = "/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/4_Cover_Quellen/AURORA2_Cover_FINAL_1600x2560.png"
rng = np.random.default_rng(21)
SC = 0.0085   # Welteinheiten pro Cover-Pixel

def face(path, box, ell, thr, local, gamma):
    im = Image.open(path).convert("RGB"); W, H = im.size
    x0, x1, y0, y1 = [int(v) for v in (box[0]*W, box[1]*W, box[2]*H, box[3]*H)]
    cr = im.crop((x0, y0, x1, y1)); cw, ch = cr.size
    step = cw/COLS
    a = np.asarray(cr, np.float32)/255.0
    lum = a @ np.array([0.3, 0.59, 0.11], np.float32)
    if local > 0:   # Gesichtszuege gegen weiches Hintergrundleuchten absetzen
        bl = np.asarray(Image.fromarray((lum*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(cw/14)), np.float32)/255.0
        lum = np.clip(lum - local*bl + 0.35*local*bl.mean(), 0, 1)
    ys, xs = np.mgrid[0:ch:step, 0:cw:step]
    ys = ys + (rng.random(ys.shape)-0.5)*step*0.8; xs = xs + (rng.random(xs.shape)-0.5)*step*0.8
    yi = np.clip(ys.astype(int), 0, ch-1); xi = np.clip(xs.astype(int), 0, cw-1)
    l = lum[yi, xi]
    rx = (xs/cw-ell[0])/ell[2]; ry = (ys/ch-ell[1])/ell[3]
    mask = np.clip(1.15-(rx**2+ry**2), 0, 1)**(0.6 if ell[2] > 0.45 else 1.3)
    l = (np.clip(l, 0, 1)**gamma)*mask
    p = np.clip((l-thr)/0.22, 0, 1)
    sel = rng.random(l.shape) < p
    xs, ys, l = xs[sel], ys[sel], l[sel]
    col = a[np.clip(ys.astype(int), 0, ch-1), np.clip(xs.astype(int), 0, cw-1)]
    X = -(xs-cw*ell[0])*SC; Z = (ch*ell[1]-ys)*SC
    return np.stack([X, Z], 1), l.astype(np.float32), col.astype(np.float32), (cw, ch)

# Gesicht I: Cover I (orange Wireframe-Gesicht); Gesicht II: Cover II (Nordlicht-Gesicht mit Haaren)
p1, l1, c1, _ = face(C1, (0.30, 0.74, 0.22, 0.56), (0.46, 0.53, 0.50, 0.56), 0.17, 0.0, 0.8)
p2, l2, c2, _ = face(C2, (0.16, 0.72, 0.235, 0.52), (0.62, 0.50, 0.46, 0.60), 0.05, 0.8, 1.0)
print("Punkte I:", len(l1), "II:", len(l2))
N = max(len(l1), len(l2))
def grow(p, l, c):
    k = N-len(l)
    if k <= 0: return p, l, c
    idx = rng.choice(len(l), k, p=(l+0.02)/(l+0.02).sum())
    jit = (rng.random((k, 2))-0.5)*0.03
    return np.concatenate([p, p[idx]+jit]), np.concatenate([l, l[idx]]), np.concatenate([c, c[idx]])
p1, l1, c1 = grow(p1, l1, c1); p2, l2, c2 = grow(p2, l2, c2)
# Zuordnung I->II: nach Streifen (Zeile) + x sortiert -> Punkte fliessen lokal
def order(p):
    band = np.floor((p[:, 1]-p[:, 1].min())/(np.ptp(p[:, 1])/45+1e-6)).astype(int)
    xk = np.where(band % 2 == 0, p[:, 0], -p[:, 0])
    return np.lexsort((xk, band))
o1, o2 = order(p1), order(p2)
P1 = p1[o1]; L1 = l1[o1]; C1c = c1[o1]
P2 = p2[o2]; L2 = l2[o2]; C2c = c2[o2]
FY = -60.0
def to3(P, L): return np.stack([P[:, 0], FY + L*0.8, P[:, 1]], 1).astype(np.float32)
F1 = to3(P1, L1); F2 = to3(P2, L2)
# Farben: Gesicht I Orange (Cover-Farbe, aufgehellt), Gesicht II Nordlicht (Farbe nach Helligkeit)
def boost(c): return np.clip(c/max(c.max(), 1e-3), 0, 1)**0.7
g1 = boost(C1c)*1.4
orange = np.array([1.0, 0.38, 0.06], np.float32)
g1 = 0.3*g1 + 0.7*orange*np.clip(L1[:, None]*1.8+0.15, 0, 1.3)
t = (np.clip(L2/0.55, 0, 1)**1.4)[:, None]
dunkel = np.array([0.02, 0.35, 0.40]); mitte = np.array([0.10, 0.85, 0.65]); hell = np.array([0.55, 1.0, 0.85])
g2 = np.where(t < 0.5, dunkel+(mitte-dunkel)*(t/0.5), mitte+(hell-mitte)*((t-0.5)/0.5))
g2 = (0.8*g2 + 0.2*boost(C2c)*1.2)*(0.3+0.9*t)
# Tube-Startpositionen: Zylinder-Volumen
ang = rng.random(N)*2*np.pi; rad = 3.0*np.sqrt(rng.random(N))
S0 = np.stack([rad*np.cos(ang), -6.0-rng.random(N)*64.0, rad*np.sin(ang)], 1).astype(np.float32)
d1 = np.clip(0.6*rng.random(N) + 0.4*np.clip(np.hypot(F1[:, 0]/4.0, (F1[:, 2])/5.0)/1.2, 0, 1), 0, 1).astype(np.float32)
d2 = np.clip(0.5*rng.random(N) + 0.5*np.clip(np.hypot(F2[:, 0]/4.0, (F2[:, 2])/5.0)/1.2, 0, 1), 0, 1).astype(np.float32)
b1 = ((rng.random((N, 3))-0.5)*2*np.array([4.0, 6.0, 4.0])).astype(np.float32)
b2 = ((rng.random((N, 3))-0.5)*2*np.array([5.0, 8.0, 5.0])).astype(np.float32)
drA = ((rng.random((N, 3))-0.5)*2*np.array([0.35, 0.8, 0.35])).astype(np.float32)
drw = (2*np.pi/(30.0*(3+7*rng.random((N, 3))))).astype(np.float32)
drph = (rng.random((N, 3))*2*np.pi).astype(np.float32)
sz = (0.75+0.5*rng.random(N)).astype(np.float32)
tx = (rng.random(N)*2*np.pi).astype(np.float32)
np.savez(OUT+"data.npz", S0=S0, F1=F1, F2=F2, col0=g1.astype(np.float32), col1=g2.astype(np.float32), d1=d1, d2=d2,
         b1=b1, b2=b2, drA=drA, drw=drw, drph=drph, sz=sz, tx=tx, L1=L1, L2=L2)
# Vorschau
for nm, P, G in (("vorschau_I.png", P1, g1), ("vorschau_II.png", P2, g2)):
    im = Image.new("RGB", (540, 700), (3, 6, 14)); d = ImageDraw.Draw(im)
    for (x, z), c in zip(P, G):
        px, py = 270-x*60, 350-z*60
        d.ellipse((px-1.3, py-1.3, px+1.3, py+1.3), fill=tuple(int(255*min(1, v)) for v in c))
    im.save(OUT+nm)
print("ok N =", N)
