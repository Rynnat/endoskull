"""Kinematik: poz -> grup donusumleri; SG90 tel baglantilari ve cene krank-rod cozumu (sabit tel/rod boyu)."""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np

import params as P
import bas as B
from lib import Tr, Rx, Ry, Rz, eksen_etrafi, nokta

E0 = np.array(P.GOZ[0]); E1 = np.array(P.GOZ[1])
GOZ_EKSEN = (0.0, P.GOZ[0][1], P.GOZ[0][2])
NOTR = dict(goz_yaw=0.0, goz_pitch=0.0, ust_L=0.0, ust_R=0.0, alt=0.0, cene=0.0, bas_yaw=0.0, bas_pitch=0.0, bas_roll=0.0)


def bas_T(p):
    return Ry(p["bas_yaw"]) @ Rx(-p["bas_pitch"]) @ Rz(p["bas_roll"])


def halka_T(p):
    return eksen_etrafi(GOZ_EKSEN, Rx(-p["goz_pitch"]))


def goz_T(p, i):
    E = P.GOZ[i]
    return halka_T(p) @ eksen_etrafi(E, Ry(p["goz_yaw"]))


def ust_T(p, i):
    return eksen_etrafi(GOZ_EKSEN, Rx(p["ust_L" if i == 0 else "ust_R"]))


def alt_T(p):
    return eksen_etrafi(GOZ_EKSEN, Rx(-p["alt"]))


def cene_T(p):
    return eksen_etrafi(P.KONDIL, Rx(p["cene"]))


# --------------------------------------------------------- surulen noktalar (bas cercevesi)
def surulen(ad, p):
    if ad == "yaw":
        return nokta(goz_T(p, 1), E1 + np.array(P.YAW_KOL))
    if ad == "pitch":
        pb = P.PITCH_BAR; t = math.radians(pb["th"])
        lx = P.SG["pitch"]["mil"][0] + P.SG["pitch"]["yon"][0] * P.SG["pitch"]["r"]
        q = (lx, E0[1] + pb["r"] * math.sin(t), E0[2] + pb["r"] * math.cos(t) - 4.0)
        return nokta(halka_T(p), q)
    if ad == "alt":
        return nokta(alt_T(p), B.alt_kol_noktasi())
    i = 0 if ad == "ustL" else 1
    return nokta(ust_T(p, i), B.ust_kol_noktasi(i))


TEL_BOY = {ad: float(np.linalg.norm(B.kol_ucu(ad, 0.0) - surulen(ad, NOTR))) for ad in P.SG}


def _coz(f, lo=-85.0, hi=85.0, n=171):
    xs = np.linspace(lo, hi, n)
    ys = np.array([f(x) for x in xs])
    kok = []
    for a, b, fa, fb in zip(xs[:-1], xs[1:], ys[:-1], ys[1:]):
        if fa == 0 or fa * fb < 0:
            for _ in range(40):
                m = (a + b) / 2
                if f(a) * f(m) <= 0:
                    b = m
                else:
                    a = m
            kok.append((a + b) / 2)
    return kok


def servo_acisi(ad, p):
    P_ = surulen(ad, p)
    L = TEL_BOY[ad]
    kok = _coz(lambda phi: float(np.linalg.norm(B.kol_ucu(ad, phi) - P_)) - L)
    if not kok:
        return None
    return min(kok, key=abs)


C_ROD = float(np.linalg.norm(B.krank_pimi(P.C1["psi0"]) - B.cene_kol_pimi(0.0)))


def krank_acisi(phi):
    q = B.cene_kol_pimi(phi)
    kok = _coz(lambda psi: float(np.linalg.norm(B.krank_pimi(psi) - q)) - C_ROD, -60, 100, 161)
    return min(kok, key=lambda k: abs(k - P.C1["psi0"])) if kok else None


def krank_T(psi):
    c = P.CENE_SERVO
    return eksen_etrafi((0, c["y"], c["z"]), Rx(P.C1["psi0"] - psi))


def kol_T(ad, phi):
    T = B.sg_T(ad)
    return T @ Rz(phi) @ np.linalg.inv(T)


def grup_T(p):
    """{grup: 4x4} bas cercevesinde (bas grubu = birim); bas_T ayrica uygulanir (yalniz kablo/rezerv)."""
    out = {"bas": np.eye(4), "halka": halka_T(p), "gozL": goz_T(p, 0), "gozR": goz_T(p, 1), "ustL": ust_T(p, 0),
           "ustR": ust_T(p, 1), "alt": alt_T(p), "cene": cene_T(p)}
    aci = {}
    for ad in P.SG:
        phi = servo_acisi(ad, p)
        aci[ad] = phi
        out[f"kol_{ad}"] = kol_T(ad, phi if phi is not None else 0.0)
    psi = krank_acisi(p["cene"])
    aci["cene_krank"] = psi
    out["krank"] = krank_T(psi if psi is not None else P.C1["psi0"])
    return out, aci


def teller(p, aci):
    """{tel_ad: (a, b)} uc noktalari (bas cercevesi)."""
    import bas as B_
    out = {}
    for ad in P.SG:
        h = B_.kol_ucu(ad, aci[ad] if aci[ad] is not None else 0.0)
        out[f"tel_{ad}"] = (h, surulen(ad, p))
    h = B_.kol_ucu("yaw", aci["yaw"] if aci["yaw"] is not None else 0.0)
    out["tel_yawL"] = (h, nokta(goz_T(p, 0), E0 + np.array(P.YAW_KOL)))
    return out
