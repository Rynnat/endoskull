"""Satin alinan / envanter parcalarinin carpisma modelleri (STL'e girmez) + CP3b-2 REZERV yer tutuculari (konsept konumu)."""
from __future__ import annotations

import math

import numpy as np

import params as P
from lib import Tr, Rx, Ry, Rz, uygula, kutu, kutu_c, silindir, kure, birlestir, cikar, tup, cq, disk_yz, hizala
from sablonlar.sg90 import sg90_govde
from sablonlar.servo_kolu import sg90_tek_kol, mg996r_disk_kol
import bas as B
import govde as G


def mg996r_model():
    m = P.MG
    x0, x1 = -m["N"], m["L"] - m["N"]
    xc = (x0 + x1) / 2
    g = kutu(x0, x1, -m["W"] / 2, m["W"] / 2, m["Z_ALT"], m["Z_UST"])
    k = kutu(xc - m["KULAK_BOY"] / 2, xc + m["KULAK_BOY"] / 2, -m["W"] / 2, m["W"] / 2, m["KULAK_Z0"], m["KULAK_Z0"] + m["KULAK_T"])
    for sx in (-1, 1):
        for sy in (-1, 1):
            k = k - silindir((xc + sx * m["KULAK_DX"], sy * m["KULAK_DY"], m["KULAK_Z0"] - 1), (xc + sx * m["KULAK_DX"], sy * m["KULAK_DY"], m["KULAK_Z0"] + 5), m["KULAK_DELIK"] / 2, 16)
    g = g + k + silindir((0, 0, m["Z_UST"] - 0.01), (0, 0, m["Z_BOSS"]), m["BOSS_R"]) + silindir((0, 0, m["Z_BOSS"] - 0.01), (0, 0, 0), m["SPL_R"])
    return g


def rotil(merkez, yon):
    """M3 goz tipi rotil [TAHMIN K3]: goz ekseni X, govde 'yon' (YZ duzleminde) dogrultusunda."""
    r = P.ROTIL
    c = np.asarray(merkez, float)
    d = np.asarray(yon, float); d /= np.linalg.norm(d)
    g = silindir(c - (r["GOZ_T"] / 2, 0, 0), c + (r["GOZ_T"] / 2, 0, 0), r["GOZ_D"] / 2, 24)
    g = g + silindir(c + d * (r["GOZ_D"] / 2 - 1.0), c + d * (r["GOZ_D"] / 2 + r["GOVDE_L"]), r["GOVDE_D"] / 2, 16)
    return g - silindir(c - (5, 0, 0), c + (5, 0, 0), 1.5, 12)


def cene_rod(psi, phi):
    a = B.krank_pimi(psi)
    b = B.cene_kol_pimi(phi)
    d = b - a
    L = np.linalg.norm(d); u = d / L
    r = P.ROTIL
    e0 = a + u * (r["GOZ_D"] / 2 + r["GOVDE_L"] - 0.5)
    e1 = b - u * (r["GOZ_D"] / 2 + r["GOVDE_L"] - 0.5)
    rod = silindir(e0, e1, 1.5, 12) if np.linalg.norm(e1 - e0) > 0.5 and (e1 - e0) @ u > 0 else None
    return rotil(a, u), rotil(b, -u), rod


def tel(a, b):
    return silindir(a, b, P.TEL_D / 2, 10)


def modeller():
    """{ad: (Manifold notr, grup)} satin alinan, montaj konumunda (notr)."""
    out = {}
    for ad in P.SG:
        T = B.sg_T(ad)
        out[f"sg90_{ad}"] = (cq(sg90_govde(kulak_delik=2.0), T), "bas")
        yx, yz = P.SG[ad]["yon"]
        out[f"sgkol_{ad}"] = (cq(sg90_tek_kol(B.kit_kol(ad)), T @ Rz(math.degrees(math.atan2(yx, yz)))), f"kol_{ad}")
    out["mg996r_cene"] = (uygula(mg996r_model(), B.mg_T()), "bas")
    out["mgkol_cene"] = (uygula(cq(mg996r_disk_kol()), B.mg_T()), "krank")
    pc = P.PCA
    out["pca2"] = (kutu(-pc["w"] / 2, pc["w"] / 2, pc["yc"] - pc["h"] / 2, pc["yc"] + pc["h"] / 2, pc["z"] - 8, pc["z"] + pc["t"]) -
                   kutu(-pc["w"] / 2 - 1, pc["w"] / 2 + 1, pc["yc"] - pc["h"] / 2 - 1, pc["yc"] + pc["h"] / 2 + 1, pc["z"] - 9, pc["z"] - 0.01) +
                   kutu(-pc["w"] / 2 + 4, pc["w"] / 2 - 4, pc["yc"] - pc["h"] / 2 + 3, pc["yc"] + pc["h"] / 2 - 3, pc["z"] - 8, pc["z"]), "bas")
    m = P.MIK
    for s, nm in ((1, "L"), (-1, "R")):
        cx, cy, cz = m["c"]
        x0 = 52.0 + m["kopuk"] + 2.0
        out[f"inmp441_{nm}"] = (kutu(min(s * x0, s * (x0 + 1.6)), max(s * x0, s * (x0 + 1.6)), cy - 7, cy + 7, cz - 7, cz + 7), "bas")
        out[f"kopuk_{nm}"] = (disk_yz((cy, cz), m["od"] / 2, min(s * 52.0, s * (52.0 + m["kopuk"])), max(s * 52.0, s * (52.0 + m["kopuk"]))) -
                              disk_yz((cy, cz), 3.0, -100, 100), "bas")
    k = P.KAMERA
    cx, cy, cz = k["c"]
    out["kamera_rezerv"] = (kutu(cx - k["w"] / 2, cx + k["w"] / 2, cy - k["w"] / 2, cy + k["w"] / 2, cz, cz + k["t"]) +
                            silindir((cx, cy, cz + k["t"] - 0.01), (cx, cy, cz + k["t"] + k["lens"][1]), k["lens"][0] / 2, 20), "bas")
    # gogus
    ls = P.LS
    out["lazy_susan_alt"] = (silindir((0, ls["y_alt"], 0), (0, ls["y_alt"] + ls["h"] / 2, 0), ls["od"] / 2, 64) -
                             silindir((0, ls["y_alt"] - 1, 0), (0, ls["y_alt"] + ls["h"], 0), ls["id"] / 2, 64), "sabit")
    out["lazy_susan_ust"] = (silindir((0, ls["y_alt"] + ls["h"] / 2 + 0.3, 0), (0, ls["y_alt"] + ls["h"], 0), ls["od"] / 2, 64) -
                             silindir((0, ls["y_alt"] - 1, 0), (0, ls["y_alt"] + ls["h"] + 1, 0), ls["id"] / 2, 64), "yaw")
    out["mg996r_yaw"] = (uygula(mg996r_model(), G._yaw_servo_T()), "sabit")
    hp = P.HOPARLOR
    out["hoparlor"] = (silindir((0, hp["c"][1], hp["c"][2] - hp["boy"]), (0, hp["c"][1], hp["c"][2] - 0.4), hp["d"] / 2, 40), "sabit")
    kt = P.KART_TABLA
    for ad, kk in P.KARTLAR.items():
        w, h, t = kk["boy"]
        z0 = (kt["z"][1] + kk["ayak"]) if kk["yuz"] > 0 else (kt["z"][0] - kk["ayak"] - t)
        bileşen = 12.0 if ad == "uno" else 8.0
        zb = (z0, z0 + t + bileşen) if kk["yuz"] > 0 else (z0 - bileşen, z0 + t)
        out[f"kart_{ad}"] = (kutu(kk["c"][0] - w / 2, kk["c"][0] + w / 2, kk["c"][1] - h / 2, kk["c"][1] + h / 2, z0, z0 + t) +
                             kutu(kk["c"][0] - w / 2 + 6, kk["c"][0] + w / 2 - 6, kk["c"][1] - h / 2 + 6, kk["c"][1] + h / 2 - 6, *zb), "sabit")
    return out


def rezerv():
    """CP3b-2'de gercek parcaya cevrilmemis kalan yer tutucular (yari saydam; STL yok). N1-N5, Y1, yay, P1, egme MG996R -> boyun.py."""
    out = {}
    for s, nm in ((1, "L"), (-1, "R")):
        out[f"P2_yanak_{nm}"] = (silindir((s * 46, 8, 70), (s * 48, -48, 52), 4.0, 16), "cene")
    return out
