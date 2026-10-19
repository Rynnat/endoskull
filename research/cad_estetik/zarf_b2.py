"""B2 yuz kabugu icin MEKANIZMA YASAK ZARFI (orbita turu, 2026-10-17).

Yeni yuz kabugu + orbita duvarlari bu zarftan cikarilir; boylece kabuk mekanizmaya (sabit) uyar:
  - goz/kapak supurmesi (81 poz, check.py ile ayni) ve cene supurmesi (0..CENE_ACI): hareketli gruplar
  - montaj-sokme: B2 -Y ile cikar (B2'ye gore digerleri +Y kayar) -> B1, servolar, B5 grubu, kollar +Y supurulur
    (0..SOKME_BOY, 1 mm adim); B3L/B3R +-X supurulur (once sokulur); B4 -Y supurulur
  - P2 yanak pistonu rezervi (statik)
Hepsi +-0.6 mm eksen kaydirmasiyla buyutulur (POZ_MIN_BOSLUK 0.4 + pay).
Cikti: out/_cache/zarf_b2.npz (B2 build bunu okur). Mekanizma degisirse yeniden calistir:
  PYTHONUTF8=1 python -B zarf_b2.py
"""
from __future__ import annotations

import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import manifold3d as m3d  # noqa: E402

YOL = os.path.join(HERE, "out", "cache", "zarf_b2.npz")
SOKME_BOY, ADIM, BUYUT = 50.0, 1.0, 0.6


def _sup(M, d, boy=SOKME_BOY, adim=ADIM):
    d = np.asarray(d, float)
    return m3d.Manifold.batch_boolean([M.translate(list(d * t)) for t in np.arange(0, boy + 0.01, adim)], m3d.OpType.Add)


def hesapla():
    import check as C
    import kin as K
    import satin as S
    import params as P
    from checks import geo
    from lib import mesh_bilgi
    M = lambda v: geo.transform(geo.to_manifold(v[0]), v[1]) if isinstance(v, tuple) else geo.to_manifold(v)
    g = []
    # 1) supurmeler (statik birlesim)
    yaws, pits = (-P.GOZ_YAW, 0, P.GOZ_YAW), (-P.GOZ_PITCH, 0, P.GOZ_PITCH)
    usts, alts = (0, P.UST_STROK / 2, P.UST_STROK), (0, P.ALT_STROK / 2, P.ALT_STROK)
    for gy, gp, u, al in itertools.product(yaws, pits, usts, alts):
        poz, _ = C.poz_bas(dict(K.NOTR, goz_yaw=gy, goz_pitch=gp, ust_L=u, ust_R=u, alt=al))
        g += [M(v) for a, v in poz.items() if a != "B2" and C.GRUP.get(a) != "bas"]
    for ph in np.arange(0, P.CENE_ACI + 0.01, 5.0):
        poz, _ = C.poz_bas(dict(K.NOTR, cene=float(ph)))
        g += [M(v) for a, v in poz.items() if a != "B2" and C.GRUP.get(a) != "bas"]
    # 2) montaj-sokme supurmeleri (notr)
    poz, _ = C.poz_bas(K.NOTR)
    for a, v in poz.items():
        if a == "B2":
            continue
        m = M(v)
        if a in ("B3L", "B3R"):
            g += [_sup(m, (1, 0, 0), 40), _sup(m, (-1, 0, 0), 40)]
        elif a in ("B4", "C1", "mgkol_cene") or a.startswith(("rotil", "cene_rod")):
            g.append(_sup(m, (0, -1, 0)))
        else:
            g.append(_sup(m, (0, 1, 0)))
    for s in ("L", "R"):
        g.append(geo.to_manifold(S.rezerv()[f"P2_yanak_{s}"][0]))
    Z = m3d.Manifold.batch_boolean(g, m3d.OpType.Add)
    Zb = m3d.Manifold.batch_boolean([Z.translate([BUYUT * e for e in d]) for d in
                                     [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]] + [Z], m3d.OpType.Add)
    v, f = mesh_bilgi(Zb)
    os.makedirs(os.path.dirname(YOL), exist_ok=True)
    np.savez_compressed(YOL, v=v, f=f)
    print(f"zarf_b2: {len(g)} govde, hacim {Zb.volume() / 1000:.1f} cm3 -> {YOL}")


def yukle():
    from checks import geo
    import trimesh
    if not os.path.exists(YOL):
        raise FileNotFoundError("zarf_b2.npz yok: once 'python -B zarf_b2.py'")
    d = np.load(YOL)
    return geo.to_manifold(trimesh.Trimesh(d["v"], d["f"], process=False))


if __name__ == "__main__":
    hesapla()


YOL2 = os.path.join(HERE, "out", "cache", "zarf_b2_yuz.npz")


def yukle_yuz():
    """Yuz bolgesine kirpilmis zarf + 26 yonlu ek buyutme (0.45): eksen kaydirmasi kosegen yuzeylerde yalniz
    0.6/sqrt3 = 0.35 buyutur (< POZ_MIN_BOSLUK 0.4, ilk tam taramada B2 x B5e 0.000 mm bulgusu). Cache'li."""
    from checks import geo
    import trimesh
    if os.path.exists(YOL2) and os.path.getmtime(YOL2) > os.path.getmtime(YOL):
        d = np.load(YOL2)
        return geo.to_manifold(trimesh.Trimesh(d["v"], d["f"], process=False))
    from lib import mesh_bilgi, kutu
    Z = yukle() ^ kutu(-80, 80, -5, 65, 40, 115)
    Zb = m3d.Manifold.batch_boolean([Z.translate([0.45 * e for e in d]) for d in itertools.product((-1, 0, 1), repeat=3)], m3d.OpType.Add)
    v, f = mesh_bilgi(Zb)
    np.savez_compressed(YOL2, v=v, f=f)
    return Zb
