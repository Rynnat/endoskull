"""Kupon montajlari (carpisma / sokme / render): her kupon icin {ad: (geometri, 4x4)} pozlari.

Basili parcalar out/stl'den (BASKI yonunde) okunur ve 4x4 ile montaj konumuna tasinir; satin alinanlar build.py modelleri.
"""
from __future__ import annotations

import functools
import os

import numpy as np

import build as B
from params import *  # noqa: F401,F403

from sablonlar.sg90 import sg90_govde
from sablonlar.servo_kolu import sg90_tek_kol, mg996r_disk_kol


@functools.lru_cache(maxsize=None)
def stl(ad):
    import trimesh
    return trimesh.load(os.path.join(STL, f"{ad}.stl"), force="mesh")


@functools.lru_cache(maxsize=None)
def model(ad):
    from checks import geo
    f = {"mg996r": B.mg996r_model, "mg_korna": mg996r_disk_kol, "sg90": lambda: sg90_govde(kablo=True),
         "sg_korna": sg90_tek_kol, "rotil": B.rotil_model}[ad]
    return geo.to_trimesh(f())


# ---------------- K1 ----------------
def k1(phi=0.0, kol="K1_kol"):
    """phi: kol ucu yukari (+) derece. kol: 'K1_kol' ya da 'K2_mg_p0.x' (ayni cerceve, t ayni)."""
    S = B.k1_servo_cerceve()
    t = K1_KOL["T"] if kol == "K1_kol" else K2_MG["T"]
    return {"K1_tutucu": (stl("K1_tutucu"), np.eye(4)),
            "mg996r": (model("mg996r"), S),
            "mg_korna": (model("mg_korna"), S @ B.Rz(90 + phi)),
            kol: (stl(kol), S @ B.k1_kol_cerceve(phi, t))}


K1_GRUP = {"K1_tutucu": "sabit", "mg996r": "sabit", "mg_korna": "kol", "K1_kol": "kol",
           **{f"K2_mg_p{p:.1f}": "kol" for p in K2_PAYLAR}}


# ---------------- K4 ----------------
def k4(theta=0.0, kol=None):
    """theta: servo (krank) acisi. kol: None -> krank + disk; 'K2_sg_p0.x' -> krank yerine K2 SG kolu (disk yok)."""
    d = {"K4_taban": (stl("K4_taban"), np.eye(4)),
         "sg90": (model("sg90"), np.eye(4)),
         "sg_korna": (model("sg_korna"), B.Rz(theta))}
    if kol is None:
        d["K4_krank"] = (stl("K4_krank"), B.k4_krank_cerceve(theta))
        d["K4_disk"] = (stl("K4_disk"), B.k4_disk_cerceve(theta))
    else:
        d[kol] = (stl(kol), B.k4_krank_cerceve(theta, K2_SG["T"]))
    return d


K4_GRUP = {"K4_taban": "sabit", "sg90": "sabit", "sg_korna": "krank", "K4_krank": "krank", "K4_disk": "disk",
           **{f"K2_sg_p{p:.1f}": "krank" for p in K2_PAYLAR}}


# ---------------- K3 ----------------
def k3(egim=0.0, kizak_dx=0.0, kaldir=0.0):
    """egim > 0: B ucu sokulu, rod + A rotil govdesi bilye etrafinda yukari egik (aci olcumu). kizak_dx: kizak kaymasi."""
    zb = B.k3_bilye_z()
    L = K3["ROD"]
    r = ROTIL
    rod_x0 = r["GOZ_D"] / 2 + r["GOVDE_L"]
    d = {"K3_taban": (stl("K3_taban"), np.eye(4))}
    if egim:
        E = B.Tx(0, 0, zb) @ B.Ry(-egim)
        d["rotil_A"] = (model("rotil"), E)
        d["rod"] = (B.silindir_eksen(1.5, (rod_x0 - 4, 0, 0), (L - rod_x0 + 4, 0, 0)), E)
        return d
    d["rotil_A"] = (model("rotil"), B.Tx(0, 0, zb))
    d["rod"] = (B.silindir_eksen(1.5, (rod_x0 - 4, 0, zb), (L - rod_x0 + 4, 0, zb)), np.eye(4))
    d["K3_kizak"] = (stl("K3_kizak"), B.Tx(L + kizak_dx, 0, K3["TABAN"][4] + kaldir))
    d["rotil_B"] = (model("rotil"), B.Tx(L + kizak_dx, 0, zb + kaldir) @ B.Rz(180))
    return d


K3_GRUP = {"K3_taban": "sabit", "rotil_A": "rod", "rod": "rod", "K3_kizak": "kizak", "rotil_B": "kizak"}


# ---------------- K5 kardan (alt eklem) ----------------
def k5_kardan(a=0.0, b=0.0, tup="K5_kardan_dis"):
    """a: orta parca ankraj pimi (X) etrafinda, b: tup orta parcanin ust pimi (Y) etrafinda (derece)."""
    _, pin2, _, _, pin1 = B.k5_orta_olcu()
    za = B.k5_ankraj_pim_z()
    Mo = B.Tx(0, 0, za) @ B.Rx(a) @ B.Tz(-pin2)
    Mt = Mo @ B.Tz(pin1) @ B.Ry(b) @ B.Tz(-K5["DIL_DELIK_Z"])
    return {"K5_kardan_ankraj": (stl("K5_kardan_ankraj"), np.eye(4)),
            "K5_kardan_orta": (stl("K5_kardan_orta"), Mo),
            tup: (stl(tup), Mt)}


K5_GRUP = {"K5_kardan_ankraj": "ankraj", "K5_kardan_orta": "orta", "K5_kardan_dis": "tup", "K5_kardan_ic": "tup"}


# ---------------- K5 teleskop cifti ----------------
def k5_cift(c, cekme=20.0):
    """Ic tup (flansi ustte, ters) dis tupun icinde; cekme = ic tup ucunun dis tup flansindan yuksekligi."""
    ft = K5["FLANS"][4]
    ust = ft + K5["BOY"]
    # ic tup ters: flans yuzu (z=0) yukarida; ic tup acik ucu z = ust - (BOY - cekme)
    Mi = B.Tx(0, 0, ust + cekme + ft) @ B.Rx(180)
    return {f"K5_dis_{c:.1f}": (stl(f"K5_dis_{c:.1f}"), np.eye(4)),
            f"K5_ic_{c:.1f}": (stl(f"K5_ic_{c:.1f}"), Mi)}


# ---------------- K2 donen pim ----------------
def k2_pim(aci=0.0, cap=3.3):
    vz = K2_PIM["SABIT"][2] + T.EKSENEL_BOSLUK
    return {"K2_pim_sabit": (stl("K2_pim_sabit"), np.eye(4)),
            f"K2_pim_donen_{cap:.1f}": (stl(f"K2_pim_donen_{cap:.1f}"), B.Rz(aci) @ B.Tz(vz))}
