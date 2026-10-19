"""Kupon kontrol goruntuleri -> out/render/*.png (numba z-tampon, OpenGL gerekmez; Quad Spider v1 render.py deseni).

  PYTHONUTF8=1 python -B render.py [ad_filtresi]
"""
import math
import os
import sys

import numpy as np
from numba import njit
from PIL import Image, ImageDraw

import montaj as M
import build as B
from params import RENDER, TABLA, K1_KOL

BG = np.array([236, 238, 241], np.float64)
RENK = {"sabit": (150, 160, 175), "satin": (60, 60, 66), "kol": (214, 120, 60), "disk": (90, 150, 210), "diger": (120, 180, 120)}


@njit(cache=True)
def raster(tri2, depth, col, W, H, zbuf, img):
    for i in range(tri2.shape[0]):
        x0, y0 = tri2[i, 0, 0], tri2[i, 0, 1]
        x1, y1 = tri2[i, 1, 0], tri2[i, 1, 1]
        x2, y2 = tri2[i, 2, 0], tri2[i, 2, 1]
        minx = max(int(math.floor(min(x0, min(x1, x2)))), 0)
        maxx = min(int(math.ceil(max(x0, max(x1, x2)))), W - 1)
        miny = max(int(math.floor(min(y0, min(y1, y2)))), 0)
        maxy = min(int(math.ceil(max(y0, max(y1, y2)))), H - 1)
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-12:
            continue
        for py in range(miny, maxy + 1):
            for px in range(minx, maxx + 1):
                fx = px + 0.5
                fy = py + 0.5
                a = ((y1 - y2) * (fx - x2) + (x2 - x1) * (fy - y2)) / den
                b = ((y2 - y0) * (fx - x2) + (x0 - x2) * (fy - y2)) / den
                c = 1.0 - a - b
                if a < 0 or b < 0 or c < 0:
                    continue
                z = a * depth[i, 0] + b * depth[i, 1] + c * depth[i, 2]
                if z < zbuf[py, px]:
                    zbuf[py, px] = z
                    img[py, px, 0] = col[i, 0]
                    img[py, px, 1] = col[i, 1]
                    img[py, px, 2] = col[i, 2]


def look_at(eye, target, up=(0, 0, 1)):
    f = np.asarray(target, float) - np.asarray(eye, float)
    f /= np.linalg.norm(f)
    if abs(f @ np.asarray(up, float)) > 0.99:
        up = (0, 1, 0)
    r = np.cross(f, up)
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    return np.array([r, u, -f]), np.asarray(eye, float)


def render(meshes, cam, target, fname, W=1100, H=850, fov=32, title=None):
    Rc, e = look_at(cam, target)
    L1 = np.array([0.4, -0.6, 0.8]); L1 /= np.linalg.norm(L1)
    tris, cols = [], []
    for v, t, rgb in meshes:
        Tt = v[t]
        n = np.cross(Tt[:, 1] - Tt[:, 0], Tt[:, 2] - Tt[:, 0])
        nn = np.linalg.norm(n, axis=1)
        ok = nn > 1e-12
        Tt, n = Tt[ok], n[ok] / nn[ok, None]
        flip = (n * (Tt.mean(1) - e)).sum(1) > 0
        n[flip] *= -1
        sh = 0.4 + 0.6 * np.clip(n @ L1, 0, 1)
        tris.append(Tt)
        cols.append(np.clip(np.asarray(rgb, float)[None, :] * sh[:, None], 0, 255))
    Tt, Cc = np.concatenate(tris), np.concatenate(cols)
    Pp = (Tt - e) @ Rc.T
    z = -Pp[..., 2]
    f = (H / 2) / math.tan(math.radians(fov) / 2)
    zz = np.maximum(z, 1e-3)
    tri2 = np.stack([Pp[..., 0] / zz * f + W / 2, -Pp[..., 1] / zz * f + H / 2], -1).astype(np.float64)
    zbuf = np.full((H, W), 1e18)
    img = np.empty((H, W, 3), np.float64)
    img[:] = BG
    raster(tri2, z.astype(np.float64), Cc.astype(np.float64), W, H, zbuf, img)
    zb = np.nan_to_num(np.where(zbuf > 1e17, np.nan, zbuf), nan=1e5)
    dz = np.zeros_like(zbuf)
    dz[1:, :] = np.abs(np.diff(zb, axis=0))
    dz[:, 1:] = np.maximum(dz[:, 1:], np.abs(np.diff(zb, axis=1)))
    img[dz > np.maximum(1.0, 0.01 * zb)] *= 0.35
    im = Image.fromarray(img.astype(np.uint8))
    if title:
        ImageDraw.Draw(im).text((14, 10), title, fill=(20, 20, 20))
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    im.save(fname)


def sahne(parcalar, renkler):
    from checks import geo
    out = []
    for ad, g in parcalar.items():
        if isinstance(g, tuple):
            g, Mx = g
        else:
            Mx = np.eye(4)
        import trimesh
        tm = g if isinstance(g, trimesh.Trimesh) else geo.to_trimesh(g)
        v = np.asarray(tm.vertices) @ Mx[:3, :3].T + Mx[:3, 3]
        out.append((v, np.asarray(tm.faces), renkler(ad)))
    return out


def renk(ad):
    if ad in ("mg996r", "sg90", "rotil_A", "rotil_B", "rod", "mg_korna", "sg_korna"):
        return RENK["satin"]
    if "tutucu" in ad or "taban" in ad or "ankraj" in ad or ad.startswith("K5_dis"):
        return RENK["sabit"]
    if "disk" in ad or "orta" in ad:
        return RENK["disk"]
    return RENK["kol"]


def gorunumler():
    return [
        ("K1_on", M.k1(0), (40, -420, 110), (40, 0, 60), "K1 onden, kol 0"),
        ("K1_3q", M.k1(10), (260, -300, 260), (40, 10, 50), "K1 3/4, kol +10"),
        ("K1_arka", M.k1(0), (-150, 300, 160), (20, 10, 55), "K1 arkadan (servo, kulak)"),
        ("K2_mg_K1de", M.k1(0, "K2_mg_p0.2"), (40, -360, 120), (30, 0, 60), "K2 MG kolu K1 tutucuda"),
        ("K4_3q", M.k4(0), (120, -180, 200), (-10, -30, 20), "K4 orta konum"),
        ("K4_ust_m25", M.k4(-25), (-5, -30, 330), (-5, -30, 0), "K4 ustten servo -25"),
        ("K4_ust_p25", M.k4(25), (-5, -30, 330), (-5, -30, 0), "K4 ustten servo +25"),
        ("K4_K2sg", M.k4(0, "K2_sg_p0.2"), (120, -160, 200), (20, -10, 20), "K2 SG kolu K4 tabaninda"),
        ("K3_3q", M.k3(), (160, -170, 140), (55, 0, 10), "K3 rod + kizak"),
        ("K3_egim45", M.k3(egim=45), (30, -200, 80), (30, 0, 30), "K3 aci olcumu 45 deg"),
        ("K5_kardan", M.k5_kardan(20, 20), (70, -70, 50), (0, 0, 25), "K5 kardan a20 b20"),
        ("K5_cift", M.k5_cift(0.4), (80, -80, 90), (0, 0, 45), "K5 teleskop cifti"),
        ("K2_pim", M.k2_pim(30), (50, -60, 60), (10, 0, 5), "K2 donen M3 eklem"),
    ]


def main(filtre=None):
    import trimesh
    for ad, parcalar, cam, hedef, baslik in gorunumler():
        if filtre and filtre not in ad:
            continue
        render(sahne(parcalar, renk), cam, hedef, os.path.join(RENDER, f"{ad}.png"), title=baslik)
        print(ad)
    for f in sorted(os.listdir(TABLA)):
        if f.endswith(".stl") and (not filtre or filtre in f):
            m = trimesh.load(os.path.join(TABLA, f), force="mesh")
            render([(np.asarray(m.vertices), np.asarray(m.faces), (214, 120, 60))], (110, -150, 330), (110, 110, 0),
                   os.path.join(RENDER, f.replace(".stl", ".png")), title=f + " (220x220)")
            print(f)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
