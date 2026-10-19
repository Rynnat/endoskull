"""Bust SIM: gercek CAD parcalari + kinematik tablolar -> out/bust_sim.html (three.js; kamera/mikrofon/hoparlor v6 hareket motoru).

Tablolar CAD'in kendi kinematiginden (kin.py, boyun.py) ornek alinir; JS yalniz ara degerler:
  - bas ici: goz (yaw x pitch 9x9), ust kapak (0..60), alt kapak (0..40), cene (0..20) -> grup 4x4 + tel/rod uc noktalari (bas cercevesi)
  - boyun: pitch (-25..20) x roll (-15..15) -> parca 4x4 + rod/yay uc noktalari (yaw=0 dunya); yaw JS'de Ry ile
  PYTHONUTF8=1 python -B sim_export.py
"""
import base64
import json
import os

import numpy as np

import params as P
import satin as S
import build as BLD
import kin as K
import boyun as BY
import params_boyun as PB
from lib import nokta
from checks import geo
from onizleme import seyrelt

CACHE = os.path.join(P.OUT, "cache")
BAS_GRUPLARI = {"bas", "halka", "gozL", "gozR", "ustL", "ustR", "alt", "cene", "krank"} | {f"kol_{a}" for a in P.SG}
CIZGI = ("rotil", "rod", "yay")      # pozla geometrisi degisen ince parcalar -> uc noktali silindir/kure


def b64(a, T):
    return base64.b64encode(np.ascontiguousarray(a, T).tobytes()).decode()


def mesh(v, f, hedef=60000):
    v, f = seyrelt(v, f, hedef)
    return dict(v=b64(v, np.float32), f=b64(f, np.uint32))


def M(T):
    return [round(float(x), 4) for x in np.asarray(T, float).T.reshape(-1)]   # three: sutun-oncelikli


def renk(ad, g):
    if ad.startswith("B5c"):
        return "iris"
    if ad.startswith("B5b"):
        return "goz"
    if ad.startswith(("sg90", "mg996r", "egme_mg996r")):       # servolar ayri renkte (kullanici, 2026-10-17)
        return "servo"
    if ad.startswith(("kart", "pca", "hoparlor", "inmp", "kamera", "mgkol", "sgkol", "lazy")) or g == "satin":
        return "satin"
    if ad.startswith("kopuk"):
        return "kopuk"
    return "metal"


def main():
    parts = []          # dict(n, kind: bas|govde|yaw|boyun, g (bas grubu), c, mesh)
    # ---- basili parcalar (cache = notr montaj)
    for ad, (_, g, _, _) in BLD.PARCALAR.items():
        fn = os.path.join(CACHE, f"{ad}.npz")
        if not os.path.exists(fn) or ad.startswith(("N", "Y1", "P1")):
            continue
        d = np.load(fn)
        if g in BAS_GRUPLARI:
            parts.append(dict(n=ad, kind="bas", g=g, c=renk(ad, g), **mesh(d["v"], d["f"], 90000 if ad == "B2" else 60000)))
        elif g == "sabit":
            parts.append(dict(n=ad, kind="govde", g="sabit", c="metal", **mesh(d["v"], d["f"])))
    # ---- satin alinanlar
    for ad, (m, g) in S.modeller().items():
        tm = geo.to_trimesh(m)
        kind = "bas" if g in BAS_GRUPLARI else ("yaw" if g == "yaw" else "govde")
        parts.append(dict(n=ad, kind=kind, g=g, c=renk(ad, "satin"), **mesh(tm.vertices, tm.faces)))

    # ---- bas ici tablolar
    NT = dict(K.NOTR)
    def grp(p):
        Tg, aci = K.grup_T(p)
        tel = {k: [list(map(float, a)), list(map(float, b))] for k, (a, b) in K.teller(p, aci).items()}
        psi = aci["cene_krank"] if aci["cene_krank"] is not None else P.C1["psi0"]
        import bas as B
        rod = [list(map(float, B.krank_pimi(psi))), list(map(float, B.cene_kol_pimi(p["cene"])))]
        return Tg, tel, rod
    gy = np.linspace(-P.GOZ_YAW, P.GOZ_YAW, 9); gp = np.linspace(-P.GOZ_PITCH, P.GOZ_PITCH, 9)
    goz = []
    for b in gp:
        row = []
        for a in gy:
            Tg, tel, _ = grp(dict(NT, goz_yaw=float(a), goz_pitch=float(b)))
            row.append(dict(m={k: M(Tg[k]) for k in ("halka", "gozL", "gozR", "kol_yaw", "kol_pitch")},
                            t={k: tel[k] for k in ("tel_yaw", "tel_yawL", "tel_pitch")}))
        goz.append(row)
    def tablo1(anahtar, vals, gruplar, teller):
        out = []
        for v in vals:
            p = dict(NT, **{k: float(v) for k in anahtar})
            Tg, tel, rod = grp(p)
            out.append(dict(m={k: M(Tg[k]) for k in gruplar}, t={k: tel[k] for k in teller}, rod=rod))
        return out
    ust_v = np.linspace(0, P.UST_STROK, 13); alt_v = np.linspace(0, P.ALT_STROK, 9); cene_v = np.linspace(0, P.CENE_ACI, 11)
    ustL = tablo1(["ust_L"], ust_v, ["ustL", "kol_ustL"], ["tel_ustL"])
    ustR = tablo1(["ust_R"], ust_v, ["ustR", "kol_ustR"], ["tel_ustR"])
    alt = tablo1(["alt"], alt_v, ["alt", "kol_alt"], ["tel_alt"])
    cene = tablo1(["cene"], cene_v, ["cene", "krank"], [])
    print("bas ici tablolar tamam")

    # ---- boyun: pitch x roll (yaw = 0)
    pv = list(range(-25, 21, 5)); rv = list(range(-15, 16, 5))
    boyun_m, boyun_l, bilinen = [], [], {}
    for pi, pt in enumerate(pv):
        rm, rl = [], []
        for r in rv:
            bp, bilgi = BY.poz(dict(bas_yaw=0.0, bas_pitch=float(pt), bas_roll=float(r)))
            mats, lines = {}, {}
            for ad, (m, T) in bp.items():
                if ad.startswith(CIZGI):
                    continue
                if ad not in bilinen:
                    tm = geo.to_trimesh(m)
                    bilinen[ad] = True
                    kind = "boyun"
                    parts.append(dict(n=ad, kind=kind, g=ad, c=renk(ad, ""), **mesh(tm.vertices, tm.faces)))
                mats[ad] = M(T)
            Ty, Tb = BY.yaw_T(dict(bas_pitch=pt, bas_roll=r)), BY.bas_T(dict(bas_pitch=pt, bas_roll=r))
            for s, nm in ((1, "L"), (-1, "R")):
                ps = bilgi["psi"][s] if bilgi["psi"][s] is not None else 0.0
                lines[f"rod_{nm}"] = [list(map(float, nokta(Ty, BY.krank_pimi(s, ps, PB.KRANK["r1"])))), list(map(float, nokta(Tb, BY.kafa_rotil(s))))]
            lines["yay"] = [list(map(float, nokta(Ty, BY.yay_delik(0.0)))), list(map(float, nokta(Tb, PB.YAY_KAFA)))]
            rm.append(mats); rl.append(lines)
        boyun_m.append(rm); boyun_l.append(rl)
        print("boyun pitch", pt)

    data = dict(parts=parts,
                goz=dict(yaw=gy.tolist(), pitch=gp.tolist(), tab=goz),
                ust=dict(v=ust_v.tolist(), L=ustL, R=ustR), alt=dict(v=alt_v.tolist(), tab=alt), cene=dict(v=cene_v.tolist(), tab=cene),
                boyun=dict(pitch=pv, roll=rv, m=boyun_m, l=boyun_l),
                lim=dict(gozYaw=P.GOZ_YAW, gozPitch=P.GOZ_PITCH, ust=P.UST_STROK, alt=P.ALT_STROK, cene=P.CENE_ACI),
                kilit=[[-25.0, -11.9], [-21.9, -1.9]])     # check_report_boyun poz_kilit: [roll 0, 15] x [cene 0, 20] -> pitch alt siniri
    tpl = open(os.path.join(os.path.dirname(__file__), "sim_sablon.html"), encoding="utf-8").read()
    html = tpl.replace("/*DATA*/null", json.dumps(data, separators=(",", ":")))
    p = os.path.join(P.OUT, "bust_sim.html")
    open(p, "w", encoding="utf-8").write(html)
    print(p, len(parts), "parca", round(os.path.getsize(p) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
