# Vorverarbeitung AURORA-Partikelvideo QUER (16:9): Zielpunkte Gesicht I (Cover I) + Gesicht II (Cover II) -> data.npz
# python3 aurora_quer_prep.py [Spalten] -> /mnt/c/Tools/blender_proj/aurora_quer/data.npz + Vorschau-PNGs
import numpy as np, sys, os
from PIL import Image, ImageFilter, ImageDraw
COLS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
OUT = "/mnt/c/Tools/blender_proj/aurora_quer/"; os.makedirs(OUT, exist_ok=True)
C1 = "/mnt/d/OneDrive/Dokumente/Bolla/AURORA/2_eBook/AURORA_Cover.jpg"
C2 = "/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/4_Cover_Quellen/AURORA2_Cover_FINAL_1600x2560.png"
rng = np.random.default_rng(33)
SC = 0.0085   # Welteinheiten pro Cover-Pixel

def blur(a, r):
    return np.asarray(Image.fromarray((np.clip(a, 0, 1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), np.float32)/255.0

def face(path, box, center, ell, thr, local, gamma, topfade, floor=0.45, sharp=0):
    im = Image.open(path).convert("RGB"); W, H = im.size
    x0, x1, y0, y1 = [int(v) for v in (box[0]*W, box[1]*W, box[2]*H, box[3]*H)]
    cr = im.crop((x0, y0, x1, y1)); cw, ch = cr.size
    step = cw/COLS
    a = np.asarray(cr, np.float32)/255.0
    lum = a @ np.array([0.3, 0.59, 0.11], np.float32)
    if local > 0:
        lum = np.clip(lum - local*blur(lum, cw/10) + 0.35*local*lum.mean(), 0, 1)
    if sharp > 0: lum = np.clip(lum + sharp*(lum - blur(lum, cw/90)), 0, 1)
    lo, hi = np.percentile(lum, 4), np.percentile(lum, 99.9); lum = np.clip((lum-lo)/(hi-lo), 0, 1)
    ys, xs = np.mgrid[0:ch:step, 0:cw:step]
    ys = ys + (rng.random(ys.shape)-0.5)*step*0.7; xs = xs + (rng.random(xs.shape)-0.5)*step*0.7
    yi = np.clip(ys.astype(int), 0, ch-1); xi = np.clip(xs.astype(int), 0, cw-1)
    l = lum[yi, xi]
    gx = (xs+x0)/W; gy = (ys+y0)/H            # Position im Gesamtcover
    r2 = ((gx-center[0])/ell[0])**2 + ((gy-center[1])/ell[1])**2
    mask = np.exp(-r2*2.0)*np.clip(2.0-r2, 0, 1)/2.0   # gaussisch weich auslaufend, kein harter Rand
    if topfade: mask = mask*np.clip((gy-topfade[0])/topfade[1], 0, 1)
    ex = np.clip(np.minimum(np.minimum(gx-box[0], box[1]-gx), box[1]-box[0])/0.06, 0, 1); mask = mask*ex
    l = (np.clip(l, 0, 1)**gamma)*mask
    p = np.clip(mask*2.5, 0, 1)*(floor+(1-floor)*np.clip((l-thr)/0.25, 0, 1))
    sel = rng.random(l.shape) < p
    xs, ys, l = xs[sel], ys[sel], l[sel]
    col = a[np.clip(ys.astype(int), 0, ch-1), np.clip(xs.astype(int), 0, cw-1)]
    X = -(xs+x0-center[0]*W)*SC; Z = (center[1]*H-(ys+y0))*SC
    return np.stack([X, Z], 1), l.astype(np.float32), col.astype(np.float32)

# Gesicht I: breiter Ausschnitt inkl. Haarsträhnen/Linien; Gesicht II: ganzer Kopf mit Haar, weich ausgeblendet
p1, l1, c1 = face(C1, (0.12, 0.88, 0.18, 0.62), (0.50, 0.40), (0.20, 0.18), 0.02, 0.35, 0.8, None, floor=0.18)
p2, l2, c2 = face(C2, (0.00, 1.00, 0.205, 0.70), (0.46, 0.37), (0.40, 0.19), 0.02, 0.85, 1.25, (0.205, 0.07), floor=0.25, sharp=2.5)
print("Punkte I:", len(l1), "II:", len(l2))
N = max(len(l1), len(l2))
def grow(p, l, c):
    k = N-len(l)
    if k <= 0: return p, l, c
    idx = rng.choice(len(l), k, p=(l+0.02)/(l+0.02).sum())
    jit = (rng.random((k, 2))-0.5)*0.02
    return np.concatenate([p, p[idx]+jit]), np.concatenate([l, l[idx]]), np.concatenate([c, c[idx]])
p1, l1, c1 = grow(p1, l1, c1); p2, l2, c2 = grow(p2, l2, c2)
def order(p):
    band = np.floor((p[:, 1]-p[:, 1].min())/(np.ptp(p[:, 1])/45+1e-6)).astype(int)
    xk = np.where(band % 2 == 0, p[:, 0], -p[:, 0])
    return np.lexsort((xk, band))
o1, o2 = order(p1), order(p2)
P1, L1, C1c = p1[o1], l1[o1], c1[o1]
P2, L2, C2c = p2[o2], l2[o2], c2[o2]
FY = -60.0
def to3(P, L): return np.stack([P[:, 0], FY + L*0.8, P[:, 1]], 1).astype(np.float32)
F1 = to3(P1, L1); F2 = to3(P2, L2)
# Farben I: echte Cover-Farbe, kraeftig und hell (Sattheit erhalten, Helligkeit nach Gesichts-Luminanz)
mx = np.maximum(C1c.max(1, keepdims=True), 1e-3)
hue = C1c/mx
g1 = hue*np.clip(L1[:, None]*2.6+0.45, 0, 1.9)
g1 = g1*np.array([1.0, 0.92, 0.8], np.float32)
# Farben II: Nordlicht — gruene/tuerkise Baender, oben Violett/Magenta, Helligkeit nach Gesichts-Luminanz
t = (np.clip(L2/0.6, 0, 1)**0.9)[:, None]
X2, Z2 = P2[:, 0], P2[:, 1]
w = (0.5+0.5*np.sin(X2*0.55 + Z2*0.38 + 1.3*np.sin(Z2*0.21)))[:, None]
gruen = np.array([0.10, 1.00, 0.42]); tuerk = np.array([0.05, 0.80, 0.95]); violett = np.array([0.62, 0.22, 0.95]); magenta = np.array([0.95, 0.25, 0.75])
base = gruen*(1-w) + tuerk*w
vz = np.clip((Z2-0.5)/3.5, 0, 1)[:, None]*(0.7+0.3*np.sin(X2*0.4+2.0)[:, None])
vz = np.clip(vz, 0, 0.85)
viol = violett*(1-0.35*w) + magenta*0.35*w
base = base*(1-vz) + viol*vz
mx2 = np.maximum(C2c.max(1, keepdims=True), 1e-3)
base = 0.8*base + 0.2*(C2c/mx2)
hell = np.array([0.80, 1.0, 0.92])
g2 = (base*(1-0.35*t**3) + hell*0.35*t**3)*(0.25+1.2*t**1.2)
# Roehre: Punkte verteilt im Zylinder
ang = rng.random(N)*2*np.pi; rad = 3.0*np.sqrt(rng.random(N))
S0 = np.stack([rad*np.cos(ang), -6.0-rng.random(N)*64.0, rad*np.sin(ang)], 1).astype(np.float32)
d1 = np.clip(0.6*rng.random(N) + 0.4*np.clip(np.hypot(F1[:, 0]/4.0, F1[:, 2]/5.0)/1.2, 0, 1), 0, 1).astype(np.float32)
d2 = np.clip(0.5*rng.random(N) + 0.5*np.clip(np.hypot(F2[:, 0]/4.0, F2[:, 2]/5.0)/1.2, 0, 1), 0, 1).astype(np.float32)
b1 = ((rng.random((N, 3))-0.5)*2*np.array([4.0, 6.0, 4.0])).astype(np.float32)
b2 = ((rng.random((N, 3))-0.5)*2*np.array([5.0, 8.0, 5.0])).astype(np.float32)
drA = ((rng.random((N, 3))-0.5)*2*np.array([0.3, 0.6, 0.3])).astype(np.float32)
drw = (2*np.pi/(30.0*(3+7*rng.random((N, 3))))).astype(np.float32)
drph = (rng.random((N, 3))*2*np.pi).astype(np.float32)
sz = (0.75+0.5*rng.random(N)).astype(np.float32)
tx = (rng.random(N)*2*np.pi).astype(np.float32)
S0y = S0[:, 1].copy()
vy = (0.7+0.6*rng.random(N)).astype(np.float32)     # Geschwindigkeitsfaktor je Punkt
np.savez(OUT+"data.npz", S0=S0, S0y=S0y, vy=vy, F1=F1, F2=F2, col0=g1.astype(np.float32), col1=g2.astype(np.float32), d1=d1, d2=d2,
         b1=b1, b2=b2, drA=drA, drw=drw, drph=drph, sz=sz, tx=tx, L1=L1, L2=L2)
for nm, P, G in (("vorschau_I.png", P1, g1), ("vorschau_II.png", P2, g2)):
    im = Image.new("RGB", (1200, 760), (3, 6, 14)); d = ImageDraw.Draw(im)
    for (x, z), c in zip(P, G):
        px, py = 600-x*80, 380-z*80
        d.ellipse((px-1.2, py-1.2, px+1.2, py+1.2), fill=tuple(int(255*min(1, v)) for v in c))
    im.save(OUT+nm)
print("ok N =", N)
