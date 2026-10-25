"""Project Bust CP3b-1 - parca uretimi.

  PYTHONUTF8=1 C:\\Users\\LENOVO\\Projeler\\epic-project\\.venv-cad\\Scripts\\python.exe -B build.py              # hepsi
  ... build.py --only B4,C1                  # yalniz bu parcalar (digerleri out/cache'ten)
  ... build.py --liste
Cikti: out/stl/<parca>.stl (BASKI YONU, z=0 tabla), out/cache/<parca>.npz (montaj konumu, notr) - check.py ve viewer.py okur.
"""
from __future__ import annotations

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

import params as P  # noqa: E402
import bas as B  # noqa: E402
import yuz_kubbe as YK  # noqa: E402
import govde as G  # noqa: E402
import boyun as BY  # noqa: E402  (CP3b-2)
from lib import Rx, Ry, Rz, uygula, mesh_bilgi  # noqa: E402

CACHE = os.path.join(P.OUT, "cache")

Y_UP = Rx(-90)          # +Y -> +Z  (Rx(-90): y'=... ) duzeltme asagida
def _yup():
    M = np.eye(4); M[1:3, 1:3] = [[0, -1], [1, 0]]     # (x, y, z) -> (x, -z, y): +Y -> +Z
    return M


YUP = _yup()
XUP = Ry(-90)          # +X -> +Z
mXUP = Ry(90)          # -X -> +Z
YDOWN = np.linalg.inv(YUP)   # -Y -> +Z (ust yuz tablada)

# ad: (fonksiyon, grup, baski donusu, aciklama)
PARCALAR = {
    "B1": (BY.B1_boyun, "bas", YUP, "kafatasi sasisi (arayuz, U-mafsal/rotil/yay kulaklari + P1 ust dilleri)"),
    "B2": (YK.B2, "bas", np.eye(4), "yuz onu (kas, goz cukuru, elmacik, maksilla, ust disler, kamera rezervi)"),
    "B3L": (YK.B3L, "bas", mXUP, "kubbe sol yari (1.2 kabuk + 1.6x5 kaburga, bindirme dili)"),
    "B3R": (YK.B3R, "bas", XUP, "kubbe sag yari"),
    "B4": (B.B4_cene, "cene", YUP, "alt cene + alt disler + kondil dilleri + rotil kolu"),
    "B5a": (B.B5a_cerceve, "bas", YUP, "goz cercevesi (dis plakalar, orta blok, sap, ayaklar)"),
    "B5b_L": (lambda: B.B5b_kure(0), "gozL", YUP, "goz kuresi sol"),
    "B5b_R": (lambda: B.B5b_kure(1), "gozR", YUP, "goz kuresi sag"),
    "B5c_L": (lambda: B.B5c_iris(0), "gozL", np.eye(4), "iris/lens sol (kirmizi)"),
    "B5c_R": (lambda: B.B5c_iris(1), "gozR", np.eye(4), "iris/lens sag (kirmizi)"),
    "B5g_L": (lambda: B.B5g_halka(0), "halka", np.eye(4), "gimbal halkasi sol (pitch)"),
    "B5g_R": (lambda: B.B5g_halka(1), "halka", np.eye(4), "gimbal halkasi sag"),
    "B5h": (B.B5h_pitch_cubugu, "halka", np.eye(4), "pitch cubugu (halkalari birlestirir)"),
    "B5d_L": (lambda: B.B5d_ust_kapak(0), "ustL", YUP, "ust kapak sol"),
    "B5d_R": (lambda: B.B5d_ust_kapak(1), "ustR", YUP, "ust kapak sag"),
    "B5e_L": (lambda: B.B5e_alt_kapak(0), "alt", YDOWN, "alt kapak sol"),
    "B5e_R": (lambda: B.B5e_alt_kapak(1), "alt", YDOWN, "alt kapak sag"),
    "B5i": (B.B5i_alt_cubuk, "alt", np.eye(4), "alt kapak cubugu"),
    **{f"B5f_{ad}": ((lambda ad=ad: B.B5f_kol(ad)), f"kol_{ad}", None, f"basili SG90 kolu ({ad})") for ad in P.SG},
    "C1": (B.C1_krank, "krank", XUP, "cene krank (MG996R disk kol cebi)"),
    "B6L": (lambda: B.B6_mikrofon(1), "bas", mXUP, "mikrofon kabi sol (INMP441, kopuk izolasyon)"),
    "B6R": (lambda: B.B6_mikrofon(-1), "bas", XUP, "mikrofon kabi sag"),
    "G1": (G.G1, "sabit", YUP, "gogus merkezi (guverte, yaw servo, kart tablasi, hoparlor izgarasi)"),
    "G2L": (G.G2L, "sabit", mXUP, "kaburga+koprucuk+kurek+omuz sol"),
    "G2R": (G.G2R, "sabit", XUP, "kaburga+koprucuk+kurek+omuz sag"),
    "G4L": (G.G4L, "sabit", YDOWN, "kaide sol yari"),
    "G4R": (G.G4R, "sabit", YDOWN, "kaide sag yari"),
    # ---- CP3b-2 boyun (boyun.py, params_boyun.py)
    "N1": (BY.N1, "yaw", YUP, "yaw tablasi (lazy susan ustu, sade disk r 48; OMURGA)"),
    "O1L": (lambda: BY.O1(1), "yaw", XUP, "omurga kasasi sol yari (egme MG996R dik, diken, P1 alt dili, yay diregi)"),
    "O1R": (lambda: BY.O1(-1), "yaw", mXUP, "omurga kasasi sag yari (egme MG996R dik, diken, P1 alt dili)"),
    "N2": (BY.N2, "yaw", YUP, "boyun kolonu + pitch catali (omur halkalari, kablo kancasi)"),
    "N3": (BY.N3, "hac", np.eye(4), "U-mafsal haci (roll M4 delik, pitch M4 saplama 3.3)"),
    "N4_L": (lambda: BY.N4(1), "krankL", mXUP, "egme krank sol (r 22.8 + iceri pim gobegi, disk kol cebi 0.2)"),
    "N4_R": (lambda: BY.N4(-1), "krankR", XUP, "egme krank sag"),
    "N5": (BY.N5, "rod", np.eye(4), "pushrod kilifi (x2 bas)"),
    "Y1": (BY.Y1, "yaw", YUP, "yaw Oldham kaplini (disk kol cebi + 2 pim)"),
    "P1_orta": (BY.kardan_orta, "p1", np.eye(4), "kardan orta parcasi K5 (x4 bas)"),
    "P1_dis": (BY.P1_dis, "p1", np.eye(4), "SCM piston dis tup + kardan dili (x2 bas)"),
    "P1_ic": (BY.P1_ic, "p1", np.eye(4), "SCM piston ic tup bosluk 0.5 + kardan dili (x2 bas)"),
}
# baski varyantlari (yalniz STL, out/stl_varyant): kupon sonucu secer [KAGIT 3, 7]
VARYANT = {
    **{f"N4_{nm}_pay{str(p).replace('.', '')}": ((lambda s=s, p=p: BY.N4(s, p)), (mXUP if s > 0 else XUP))
       for s, nm in ((1, "L"), (-1, "R")) for p in (0.1, 0.3)},
    **{f"P1_ic_bosluk{str(b).replace('.', '')}": ((lambda b=b: BY.P1_ic(b)), np.eye(4)) for b in (0.4, 0.6)},
}
BAS_PARCALARI = [k for k, v in PARCALAR.items() if v[1] not in ("sabit",)]


def baski_T(ad):
    T = PARCALAR[ad][2]
    if T is None:          # SG90 kolu: servo-yerel cerceve (mil +Z)
        T = np.linalg.inv(B.sg_T(ad[4:]))
    return T


def uret(ad):
    import trimesh
    t0 = time.time()
    M = PARCALAR[ad][0]()
    gov = M.decompose()
    kirinti = [x for x in gov if abs(x.volume()) < 1.0]
    if kirinti:                       # boolean kiymiklari (hacim < 1 mm3) atilir, raporlanir
        import manifold3d as m3d
        M = m3d.Manifold.batch_boolean([x for x in gov if abs(x.volume()) >= 1.0], m3d.OpType.Add)
        print(f"   {ad}: {len(kirinti)} kiymik (< 1 mm3) atildi")
    kaydet(ad, M, t0)


SADE_ESIK, SADE_TOL = 100_000, 0.02   # zarf supurmesi B2'de ~910k ucgen birakiyordu; 0.02 mm -> ~51k, hacim farki %0.04


def kaydet(ad, M, t0):
    import trimesh
    if M.num_tri() > SADE_ESIK:
        n0 = M.num_tri()
        import manifold3d as m3d
        M = m3d.Manifold.batch_boolean([x for x in M.simplify(SADE_TOL).decompose() if abs(x.volume()) >= 1.0], m3d.OpType.Add)
        print(f"   {ad}: sadelestirildi {n0} -> {M.num_tri()} ucgen (tol {SADE_TOL} mm)")
    v, f = mesh_bilgi(M)
    os.makedirs(CACHE, exist_ok=True)
    np.savez_compressed(os.path.join(CACHE, f"{ad}.npz"), v=v, f=f)
    tm = trimesh.Trimesh(v, f, process=False)
    tm.apply_transform(baski_T(ad))
    tm.apply_translation(-tm.bounds[0])
    os.makedirs(P.STL, exist_ok=True)
    tm.export(os.path.join(P.STL, f"{ad}.stl"))
    e = tm.bounds[1] - tm.bounds[0]
    print(f"{ad:8s} hacim {M.volume() / 1000:7.2f} cm3  baski {e[0]:.0f} x {e[1]:.0f} x {e[2]:.0f}  gov {len(M.decompose())}  "
          f"{time.time() - t0:.1f} s", flush=True)


def uret_varyant(ad):
    import trimesh
    fn, T = VARYANT[ad]
    M = fn()
    v, f = mesh_bilgi(M)
    tm = trimesh.Trimesh(v, f, process=False)
    tm.apply_transform(T)
    tm.apply_translation(-tm.bounds[0])
    d = os.path.join(P.OUT, "stl_varyant")
    os.makedirs(d, exist_ok=True)
    tm.export(os.path.join(d, f"{ad}.stl"))
    print(f"{ad:18s} varyant hacim {M.volume() / 1000:6.2f} cm3")


def yukle(ad):
    """cache'ten montaj (notr) manifold."""
    from checks import geo
    d = np.load(os.path.join(CACHE, f"{ad}.npz"))
    import trimesh
    return geo.to_manifold(trimesh.Trimesh(d["v"], d["f"], process=False))


def main(argv):
    if "--liste" in argv:
        for k, v in PARCALAR.items():
            print(f"{k:8s} {v[1]:10s} {v[3]}")
        return
    sec = list(PARCALAR)
    if "--only" in argv:
        sec = argv[argv.index("--only") + 1].split(",")
        bad = [s for s in sec if s not in PARCALAR]
        if bad:
            raise SystemExit(f"bilinmeyen parca: {bad}")
    if "--sadelestir" in argv:            # yeniden kurmadan: cache'teki parcayi sadelestirip yeniden yaz
        for ad in sec:
            kaydet(ad, yukle(ad), time.time())
        return
    for ad in sec:
        uret(ad)
    if "--varyant" in argv:
        for ad in VARYANT:
            uret_varyant(ad)


if __name__ == "__main__":
    main(sys.argv[1:])
