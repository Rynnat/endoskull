"""CP3b-1 ONIZLEME (kontroller TEMIZ DEGIL): out/cache montaj (notr) + satin alinanlar + CP3b-2 rezervleri -> out/onizleme.html.

  PYTHONUTF8=1 python -B onizleme.py
"""
import base64
import json
import os
import sys

import numpy as np

import params as P
import satin as S
from checks import geo

CACHE = os.path.join(P.OUT, "cache")
BOYUN_ONEK = ("N1", "N2", "N3", "N4", "N5", "Y1", "P1", "O1L", "O1R")


def grup(ad):
    if ad.startswith("B5"):
        return "goz", (200, 205, 215)
    if ad.startswith(("B2", "B3")):
        return "kabuk", (176, 184, 196)
    if ad.startswith(("B1", "B6", "C1")):
        return "sasi", (120, 128, 140)
    if ad.startswith("B4"):
        return "cene", (176, 184, 196)
    if ad.startswith("G"):
        return "govde", (150, 158, 170)
    return "diger", (180, 180, 180)


def seyrelt(v, f, hedef=120000):
    """Onizleme icin kaba seyreltme (vertex kumeleme); yalniz gorsel, STL/kontrol degismez."""
    v, f = np.asarray(v, float), np.asarray(f)
    h = 0.4
    while len(f) > hedef and h < 5:
        q = np.floor(v / h).astype(np.int64)
        _, idx, inv = np.unique(q, axis=0, return_index=True, return_inverse=True)
        inv = inv.reshape(-1)
        f2 = inv[f]
        ok = (f2[:, 0] != f2[:, 1]) & (f2[:, 1] != f2[:, 2]) & (f2[:, 0] != f2[:, 2])
        f2 = np.unique(np.sort(f2[ok], axis=1), axis=0, return_index=True)[1]
        f2 = inv[f][ok][np.sort(f2)]
        if len(f2) <= hedef:
            return v[idx], f2
        h *= 1.5
    return v, f


def kodla(v, f):
    return (base64.b64encode(np.asarray(v, np.float32).tobytes()).decode(),
            base64.b64encode(np.asarray(f, np.uint32).tobytes()).decode())


def main():
    parts = []
    for fn in sorted(os.listdir(CACHE)):
        if fn.endswith(".npz") and not fn.startswith("zarf") and not fn.startswith(BOYUN_ONEK):   # zarf_* = kontrol zarfi; boyun pozlu eklenir
            d = np.load(os.path.join(CACHE, fn))
            ad = fn[:-4]
            g, c = grup(ad)
            v, f = kodla(*seyrelt(d["v"], d["f"]))
            parts.append(dict(n=ad, g=g, c=c, v=v, f=f, k="baski"))
    for ad, (m, _) in S.modeller().items():
        tm = geo.to_trimesh(m)
        v, f = kodla(tm.vertices, tm.faces)
        parts.append(dict(n=ad, g="satin", c=(55, 58, 66), v=v, f=f, k="satin"))
    import boyun as BY
    bp, _ = BY.poz(dict(bas_yaw=0.0, bas_pitch=0.0, bas_roll=0.0))
    for ad, (m, T) in bp.items():
        tm = geo.to_trimesh(geo.transform(geo.to_manifold(m), T))
        v, f = kodla(tm.vertices, tm.faces)
        bas = ad.split("_")[0] in ("N1", "N2", "N3", "N4", "N5", "Y1", "O1L", "O1R") or ad.startswith("P1")
        parts.append(dict(n=ad, g="boyun" if bas else "satin", c=(150, 158, 170) if bas else (55, 58, 66), v=v, f=f, k="baski" if bas else "satin"))
    for ad, (m, _) in S.rezerv().items():
        tm = geo.to_trimesh(m)
        v, f = kodla(tm.vertices, tm.faces)
        parts.append(dict(n=ad, g="rezerv", c=(79, 209, 255), v=v, f=f, k="rezerv"))
    rap = open(os.path.join(P.OUT, "check_report.txt"), encoding="utf-8").read()
    sonuc = next((l for l in rap.splitlines() if "SONUC" in l), "SONUC: ?")
    tpl = open(os.path.join(os.path.dirname(__file__), "onizleme_sablon.html"), encoding="utf-8").read()
    html = tpl.replace("/*DATA*/null", json.dumps(dict(parts=parts, sonuc=sonuc), separators=(",", ":")))
    p = os.path.join(P.OUT, "onizleme.html")
    open(p, "w", encoding="utf-8").write(html)
    print(p, len(parts), "parca", round(os.path.getsize(p) / 1e6, 1), "MB", sonuc)


if __name__ == "__main__":
    main()
