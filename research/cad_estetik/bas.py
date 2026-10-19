"""Bas parcalari (bas cercevesi, notr poz). Her parca ayri fonksiyon -> manifold3d.Manifold.

B1 sasi (arayuz + REZERV kulaklar) | B2 yuz onu | B3L/B3R kubbe | B4 alt cene | B5 goz modulu (a cerceve, b kure, c iris,
d ust kapak, e alt kapak, f basili SG90 kollari, g halka, h pitch cubugu, i alt cubuk) | B6 mikrofon kabi | C1 cene krank.
Sablonlar: sg90_cebi, servo_kolu.*_cebi, baglanti.vida_pim_eklemi/somun_tuzagi/pahli_delik, m2.m2_somun_tuzagi [TASLAK].
"""
from __future__ import annotations

import math

import numpy as np

import params as P
from lib import (Rx, Ry, Rz, Tr, uygula, kutu, kutu_c, silindir, kure, elipsoid, birlestir, cikar, tup, hex_bas, cq,
                 disk_yz, plaka_xz, plaka_yz, yuvarlak_cubuk_yz, kafatasi, skull_pt, dis, dis_olcu)
from sablonlar import toleranslar as T
from sablonlar.sg90 import sg90_cebi, sg90_kulak_x
from sablonlar.servo_kolu import sg90_tek_kol_cebi, mg996r_disk_kol_cebi, SG_KOL
from sablonlar.baglanti import somun_tuzagi, vida_pim_eklemi, pahli_delik
from sablonlar.m2 import m2_somun_tuzagi

# yerel +Z -> bas eksenleri
Z2X = np.array([[0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1.0]])     # +Z -> +X
Z2mX = np.array([[0, 0, -1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1.0]])    # +Z -> -X
Z2Y = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1.0]])     # +Z -> +Y (yerel y -> -Z)
Z2mY = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1.0]])
Z2Z = np.eye(4)
Z2mZ = Rx(180)


def sg_T(ad):
    """SG90 servo-yerel (sablon) -> bas. yerel x (govde boyu, uzak uc) -> +Z, yerel y -> +X, yerel z (mil) -> +Y."""
    s = P.SG[ad]
    sx, sz = s["mil"]
    return np.array([[0, 1, 0, sx], [0, 0, 1, s["ped"] - T.SG90_KULAK_Z], [1, 0, 0, sz], [0, 0, 0, 1.0]])


def mg_T():
    """MG996R mil-ucu cercevesi -> bas (cene servosu): mil +X, govde -Z."""
    c = P.CENE_SERVO
    return np.array([[0, 0, 1, c["mil_x"]], [0, 1, 0, c["y"]], [-1, 0, 0, c["z"]], [0, 0, 0, 1.0]])


def m3_somun_x(x_yuz, y, z, yon, kanal=0.0, kanal_yonu=0.0):
    """x_yuz yuzeyinden yon (+1: +X'e dogru) iceri M3 somun cebi + delik."""
    k = somun_tuzagi("M3", kanal=kanal, kanal_yonu_deg=kanal_yonu, vida_deligi=P.M3)
    return cq(k, Tr(x_yuz, y, z) @ (Z2X if yon > 0 else Z2mX))


# ===================================================================================================== B1 sasi
def B1():
    y0, y1 = P.B1_Y
    g = [plaka_xz(P.B1_DIS, y0, y1), kutu(-24, 24, y0, y1, P.PCA_DIK['z'][0], -42)]
    for s in (-1, 1):
        a = P.B1_ARKA_YAN
        g.append(kutu(min(s * a[0], s * a[1]), max(s * a[0], s * a[1]), y0, y1, a[2], a[3]))
        m = P.MIK_KOL
        g.append(kutu(min(s * m["x"][0], s * m["x"][1]), max(s * m["x"][0], s * m["x"][1]), y0, y1, *m["z"]))
        # mikrofon kabi plakasi (kopuk contadan M2 x2)
        g.append(kutu(min(s * 48.5, s * 50.5), max(s * 48.5, s * 50.5), 4.0, y1, m["z"][0], m["z"][1]))
        # kondil askisi (sabit) + M4 vida-pim
        a = P.ASKI
        g.append(kutu(min(s * a["x"][0], s * a["x"][1]), max(s * a["x"][0], s * a["x"][1]), a["y"][0], a["y"][1], *a["z"]))
        g.append(disk_yz(P.KONDIL[1:], 7.0, s * a["x"][0], s * a["x"][1]))
        # B3 direkleri
        for d in P.B3_DIREK.values():
            g.append(kutu(min(s * d["x"][0], s * d["x"][1]), max(s * d["x"][0], s * d["x"][1]), y1, P.B3_DIREK_UST, *d["z"]))
        # B3 arka dil
        b = P.B3_ARKA
        g.append(kutu(min(s * b["x"][0], s * b["x"][1]), max(s * b["x"][0], s * b["x"][1]), b["y"][0], y1 + 2, *b["z"]))
        # B2 kulaklari (alttan vida)
        k = P.B2_KULAK
        g.append(kutu(min(s * k["x"][0], s * k["x"][1]), max(s * k["x"][0], s * k["x"][1]), k["y"][0], y1, *k["z"]))
        # REZERV CP3b-2: roll kulaklari (Z ekseni), rotil kulaklari (X ekseni)
        r = P.RZ_ROLL
        g.append(kutu(-r["x"], r["x"], r["y"][0], y0 + 0.01, min(s * r["z"][0], s * r["z"][1]), max(s * r["z"][0], s * r["z"][1])))
        r = P.RZ_ROTIL
        g.append(kutu(min(s * r["x"][0], s * r["x"][1]), max(s * r["x"][0], s * r["x"][1]), r["y"][0], y0 + 0.01, *r["z"]))
    r = P.RZ_YAY
    g.append(kutu(-r["x"], r["x"], r["y"][0], y0 + 0.01, *r["z"]))
    # PCA#2 dik plakasi
    d = P.PCA_DIK
    g.append(kutu(-d["x"], d["x"], y0, 30.0, *d["z"]))
    g.append(kutu(-30, 30, 28.0, d["y"][1], *d["z"]))
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * P.PCA["delik"][0] / 2, P.PCA["yc"] + sy * P.PCA["delik"][1] / 2
            g.append(silindir((px, py, d["z"][0] + 0.01), (px, py, P.PCA["z"] + P.PCA["t"]), 3.0))
    # cene servosu duvari (+X)
    w0 = P.CENE_SERVO["mil_x"] + P.MG["KULAK_Z0"]          # kulak alt yuzu x
    g.append(kutu(w0 - P.CENE_DUVAR_T, w0, y0, 57.0, -58.0, -2.0))
    # SG90 pedleri (ped yuksekligi farkli olanlar)
    for ad, s in P.SG.items():
        sx, sz = s["mil"]
        if s["ped"] > y1:
            g.append(kutu(sx - 7.5, sx + 7.5, y1 - 0.01, s["ped"], sz - 12.0, sz + 21.6))
        elif s["ped"] < y1:
            g.append(kutu(sx - 8.6, sx + 8.6, s["ped"] - 3.0, y0 + 0.01, sz - 12.0, sz + 21.6))
    G = birlestir(g)
    # ---------------- kesimler
    c = []
    for ad, s in P.SG.items():
        Tsg = sg_T(ad)
        c.append(cq(sg90_cebi(kulak_delik_cap=P.M2, kulak_delik_boy=12.0, alt_acik=2.0), Tsg))
        if s["ped"] < y1:      # alcak ped: ustteki plaka servo + kulak izdusumunde acik
            c.append(uygula(kutu(-12.6, 22.5, -6.6, 6.6, T.SG90_KULAK_Z - 0.01, 40), Tsg))
        kx = sg90_kulak_x()[1]
        z0 = s["ped"] - 3.0                                     # somun tavani ile kulak arasi 1.2 plastik
        kanal = 12.0 if s["ped"] > y1 else 0.0                 # ic cep (yuksek ped) -> yandan kanal
        c.append(cq(m2_somun_tuzagi(z0=0.0, kanal=kanal, vida_deligi=False), Tr(s["mil"][0], z0 - 1.8, s["mil"][1] + kx) @ Z2Y))
    # kondil: sabit M4 (somun ic yuzde)
    vp = vida_pim_eklemi("M4", sabit_t=5.0, donen_t=4.0)
    for s in (-1, 1):
        c.append(cq(vp["sabit"], Tr(s * P.ASKI["x"][0], P.KONDIL[1], P.KONDIL[2]) @ (Z2X if s > 0 else Z2mX)))
    # cene servosu penceresi + 4x M4 kulak
    mt = mg_T()
    xc = (P.MG["L"] - 2 * P.MG["N"]) / 2
    pp = P.MG_CEP_PAY
    c.append(uygula(kutu(-P.MG["N"] - pp / 2, P.MG["L"] - P.MG["N"] + pp / 2, -P.MG["W"] / 2 - pp / 2, P.MG["W"] / 2 + pp / 2, -60, -10), mt))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = mt[:3, :3] @ np.array([xc + sx * P.MG["KULAK_DX"], sy * P.MG["KULAK_DY"], 0]) + mt[:3, 3]
            c.append(cq(somun_tuzagi("M4", vida_deligi=P.M4), Tr(w0 - P.CENE_DUVAR_T, p[1], p[2]) @ Z2X))
    # B5 ayaklari M2 x4 (somun plaka altinda)
    for x, z in B5_AYAK_VIDA:
        c.append(cq(m2_somun_tuzagi(z0=0.0), Tr(x, y0 - 0.01, z) @ Z2Y))
    # B5 sapi icin centik
    sp = P.ORTA_SAP
    for s in (-1, 1):
        dx = sorted((s * (sp["dus_x"][0] - 0.5), s * (sp["dus_x"][1] + 0.5)))
        c.append(kutu(*dx, y0 - 1, y1 + 1, sp["dus_z"][0] - 0.5, sp["dus_z"][1] + 0.5))
    # B2 kulak: dikey M3, somun yandan kanalla
    k = P.B2_KULAK
    for s in (-1, 1):
        for dx in k["delik_x"]:
            c.append(cq(somun_tuzagi("M3", kanal=8.0, kanal_yonu_deg=90.0 if s > 0 else 90.0, vida_deligi=P.M3),
                        Tr(s * dx, k["somun_y"], k["delik_z"]) @ Z2Y))
    # B3 direk: yatay M3 (X), somun ic yuzden kanalla
    for s in (-1, 1):
        for d in P.B3_DIREK.values():
            xi = d["x"][0]
            c.append(cq(somun_tuzagi("M3", kanal=6.0, kanal_yonu_deg=90.0, vida_deligi=P.M3),
                        Tr(s * (xi + 1.5), P.B3_VIDA_Y, (d["z"][0] + d["z"][1]) / 2) @ (Z2X if s > 0 else Z2mX)))
        b = P.B3_ARKA
        c.append(cq(somun_tuzagi("M3", kanal=6.0, kanal_yonu_deg=90.0, vida_deligi=P.M3),
                    Tr(s * (b["x"][0] + b["x"][1]) / 2, b["vida_y"], b["z"][1] - 1.5) @ Z2mZ))
        # mikrofon plakasi M2 x2 (X ekseni)
        for dy in (-6.0, 6.0):
            c.append(silindir((s * 47, P.MIK["c"][1] + dy, P.MIK["c"][2]), (s * 52, P.MIK["c"][1] + dy, P.MIK["c"][2]), P.M2 / 2, 16))
    # PCA direkleri M3 + somun (on yuz)
    d = P.PCA_DIK
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * P.PCA["delik"][0] / 2, P.PCA["yc"] + sy * P.PCA["delik"][1] / 2
            c.append(cq(somun_tuzagi("M3", vida_deligi=P.M3), Tr(px, py, d["z"][1] + 0.01) @ Z2mZ))
    # REZERV delikler: roll pimi (Z, y 0), rotil (X, y -6), yay (X)
    c.append(silindir((0, 0, -20), (0, 0, 20), P.M4 / 2 + 0.1))
    r = P.RZ_ROTIL
    c.append(silindir((-40, r["dy"], sum(r["z"]) / 2), (40, r["dy"], sum(r["z"]) / 2), P.M3 / 2 + 0.1))
    c.append(silindir((-6, -2, sum(P.RZ_YAY['z']) / 2), (6, -2, sum(P.RZ_YAY['z']) / 2), 1.3))
    # alt kapak teli icin plaka yarigi (tel kapali konumda plakanin onunden asagi iner)
    lx = P.ALT_KOL["x"]
    c.append(kutu(lx - 2.5, lx + 2.5, y0 - 1, y1 + 1, 46.0, 60.0))
    # alt kapak ic kolu supurmesi (kapanirken B1 on kenarina iner) icin centik
    for s in (-1, 1):
        c.append(kutu(min(s * 14.0, s * 16.6), max(s * 14.0, s * 16.6), y0 - 1, y1 + 1, 54.0, 60.0))
    # kablo cikisi (8 iletken + servo kablolari) + hafifletme
    c.append(silindir((0, y0 - 1, -50), (0, y1 + 1, -50), 7.0))
    for x0, x1, z0, z1 in ((-12, 12, -40, -22), (-30, -16, 2, 26), (16, 30, 2, 26)):
        c.append(kutu(x0, x1, y0 - 1, y1 + 1, z0, z1))
    c += _b1_hafifletme(g, c)
    return cikar(G, c)


def _b1_hafifletme(g, c):
    """B1 hafifletme (58 g -> <= 45 g): plaka (Y) ve PCA dik plakasi (Z) uzerinde aclgozlu daire delik yerlesimi.
    Delik + 2.4 mm et halkasi baska hicbir ozellige (kesimler dahil) ve plaka kenarinin 3 mm icine girmez."""
    import manifold3d as m3d
    y0, y1 = P.B1_Y
    et = 2.0
    keep = birlestir(g[1:] + c) ^ kutu(-200, 200, y0 - 3, y1 + 3, -200, 200)
    cs = m3d.CrossSection([[(float(x), float(z)) for x, z in P.B1_DIS]]).offset(-2.5, m3d.JoinType.Miter)
    ic = birlestir([plaka_xz([(float(a), float(b_)) for a, b_ in poly], y0 - 2, y1 + 2) for poly in cs.to_polygons()])
    secilen, delik = [], []
    for r, adim in ((10.0, 2.5), (7.5, 2.5), (5.5, 2.0), (4.0, 2.0)):
        for x in np.arange(-56, 57, adim):
            for z in np.arange(-42, 60, adim):
                if any((x - a) ** 2 + (z - b_) ** 2 < (r + rb + et) ** 2 for a, b_, rb in secilen):
                    continue
                zon = silindir((x, y0 - 1, z), (x, y1 + 1, z), r + et, 24)
                if (zon - ic).volume() > 1e-3 or (zon ^ keep).volume() > 1e-3:
                    continue
                secilen.append((x, z, r))
                delik.append(silindir((x, y0 - 1, z), (x, y1 + 1, z), r, 32))
    # PCA dik plakasi: kart arkasinda pencere (direkler + kenar 4 mm haric)
    d = P.PCA_DIK
    delik.append(kutu(-20.0, 20.0, 33.0, 55.0, d["z"][0] - 1, d["z"][1] + 1))
    return delik


# B5 ayak vidalari (B1 + B5a ortak)
B5_AYAK_VIDA = [(-50.0, 41.0), (-38.0, 44.0), (50.0, 41.0), (38.0, 44.0)]


# ===================================================================================================== B5 goz modulu
def _eye_T(i):
    return Tr(*P.GOZ[i])


def _ofs(i, x_ofs):
    """goz merkezinden x ofseti (dis taraf +): sol goz (i=0) disi -X."""
    s = -1 if i == 0 else 1
    return P.GOZ[i][0] + s * x_ofs


def _band(i, a, b, ic=False):
    """goz i icin x bandi (ofset a..b), dis ya da ic taraf -> (x0, x1)."""
    s = (-1 if i == 0 else 1) * (-1 if ic else 1)
    x0, x1 = P.GOZ[i][0] + s * a, P.GOZ[i][0] + s * b
    return min(x0, x1), max(x0, x1)


def _sektor(i, r0, r1, th0, th1, xa, xb, n=24):
    """goz ekseni (X) etrafinda halka dilimi, x bandi [xa, xb] (dunya), theta = atan2(dy, dz)."""
    E = P.GOZ[i]
    pts = []
    for k in range(n + 1):
        t = math.radians(th0 + (th1 - th0) * k / n)
        pts.append((E[1] + r1 * math.sin(t), E[2] + r1 * math.cos(t)))
    for k in range(n, -1, -1):
        t = math.radians(th0 + (th1 - th0) * k / n)
        pts.append((E[1] + r0 * math.sin(t), E[2] + r0 * math.cos(t)))
    return plaka_yz(pts, xa, xb)


def _kama(i, th0, th1, R=40.0):
    """goz X ekseni etrafinda theta [th0, th1] kamasi (tam genislik)."""
    E = P.GOZ[i]
    pts = [(E[1], E[2])]
    n = 24
    for k in range(n + 1):
        t = math.radians(th0 + (th1 - th0) * k / n)
        pts.append((E[1] + R * math.sin(t), E[2] + R * math.cos(t)))
    return plaka_yz(pts, E[0] - 30, E[0] + 30)


def _kabuk_bolge(i, ri, ro, th0, th1, xmax):
    E = P.GOZ[i]
    sh = kure(E, ro, 48) - kure(E, ri, 48)
    return sh ^ _kama(i, th0, th1) ^ kutu(E[0] - xmax, E[0] + xmax, -100, 200, -100, 200)


def B5b_kure(i):
    E = np.array(P.GOZ[i])
    g = kure(E, P.GOZ_R, 48)
    g = g + silindir(E + (0, P.YAW_KOL[1], -10.0), E + (0, P.YAW_KOL[1], -20.5), 2.2)   # yaw kolu
    c = [silindir(E + (0, 0, P.GOZ_R - P.IRIS_CEP), E + (0, 0, P.GOZ_R + 2), P.IRIS_R + 0.15),
         silindir(E + (0, P.GOZ_R - 5, 0), E + (0, P.GOZ_R + 1, 0), P.TEL_DELIK / 2, 12),
         silindir(E + (0, -P.GOZ_R - 1, 0), E + (0, -P.GOZ_R + 5, 0), P.TEL_DELIK / 2, 12),
         silindir(E + (-4, P.YAW_KOL[1], P.YAW_KOL[2]), E + (4, P.YAW_KOL[1], P.YAW_KOL[2]), P.TEL_DELIK / 2, 12)]
    c[-1] = silindir(E + (0, P.YAW_KOL[1] - 4, P.YAW_KOL[2]), E + (0, P.YAW_KOL[1] + 4, P.YAW_KOL[2]), P.TEL_DELIK / 2, 12)
    return cikar(g, c)


def B5c_iris(i):
    E = np.array(P.GOZ[i])
    z0 = E[2] + P.GOZ_R - P.IRIS_CEP
    g = silindir(E + (0, 0, P.GOZ_R - P.IRIS_CEP), E + (0, 0, P.GOZ_R - P.IRIS_CEP + P.IRIS_T), P.IRIS_R, 40)
    g = g - silindir((E[0], E[1], z0 + P.IRIS_T - 0.4), (E[0], E[1], z0 + P.IRIS_T + 1), 2.2, 28)   # bebek cukuru
    return g


def B5g_halka(i):
    E = np.array(P.GOZ[i])
    ring = silindir(E - (0, 0, P.HALKA_T / 2), E + (0, 0, P.HALKA_T / 2), P.HALKA_RO, 48) - \
        silindir(E - (0, 0, 5), E + (0, 0, 5), P.HALKA_RI, 48)
    g = [ring]
    a, b, rh = P.HALKA_GOBEK
    for ic in (False, True):
        xa, xb = _band(i, a, b, ic)
        g.append(disk_yz(E[1:], rh, xa, xb))
        g.append(kutu(xa, xb, E[1] - 2.0, E[1] + 2.0, E[2] - P.HALKA_T / 2, E[2] + P.HALKA_T / 2))
    # pitch cubugu kulagi (ic bant)
    xa, xb = _band(i, a, b, True)
    pb = P.PITCH_BAR
    t = math.radians(pb["th"])
    pc = (E[1] + pb["r"] * math.sin(t), E[2] + pb["r"] * math.cos(t))
    g.append(yuvarlak_cubuk_yz(tuple(E[1:]), pc, 3.5, xa, xb))
    G = birlestir(g)
    c = [silindir((E[0] - 20, E[1], E[2]), (E[0] + 20, E[1], E[2]), P.M3 / 2 + 0.0, 20)]
    for sy in (-1, 1):
        c.append(silindir(E + (0, sy * (P.HALKA_RI - 1), 0), E + (0, sy * (P.HALKA_RO + 1), 0), P.TEL_D / 2, 10))   # pres tel pim
    c.append(silindir((xa - 1, pc[0], pc[1]), (xb + 1, pc[0], pc[1]), pb["kal"] + 0.15, 20))
    return cikar(G, c)


def B5h_pitch_cubugu():
    pb = P.PITCH_BAR
    x0 = _band(0, *P.HALKA_GOBEK[:2], ic=True)[0]
    x1 = _band(1, *P.HALKA_GOBEK[:2], ic=True)[1]
    E = P.GOZ[0]
    t = math.radians(pb["th"])
    y, z = E[1] + pb["r"] * math.sin(t), E[2] + pb["r"] * math.cos(t)
    g = silindir((x0, y, z), (x1, y, z), pb["kal"], 24)
    lx = P.SG["pitch"]["mil"][0] + P.SG["pitch"]["yon"][0] * P.SG["pitch"]["r"]
    g = g + kutu(lx - 1.5, lx + 1.5, y - 1.0, y + 1.0, z - 6.0, z)
    g = g - silindir((lx - 3, y, z - 4.0), (lx + 3, y, z - 4.0), P.TEL_DELIK / 2, 12)
    return g


def ust_kol_noktasi(i, r=None):
    k = P.UST_KOL
    E = P.GOZ[i]
    t = math.radians(k["th_acik"])
    rr = k["r"] if r is None else r
    xa, xb = _band(i, *P.UST_BANT)
    return ((xa + xb) / 2, E[1] + rr * math.sin(t), E[2] + rr * math.cos(t))


def B5d_ust_kapak(i):
    """ACIK (alfa 0) konumda kurulur. Yalniz dis tarafta pivot (ic bant pitch kulagina ayrildi)."""
    E = np.array(P.GOZ[i])
    a0, a1 = P.UST_ACI[0] + P.UST_STROK, P.UST_ACI[1] + P.UST_STROK
    g = [_kabuk_bolge(i, P.UST_RI, P.UST_RO, a0, a1, P.KAPAK_X)]
    m0, m1 = 20.0 + P.UST_STROK, P.UST_ACI[1] + P.UST_STROK      # yan kopru/plaka acisal araligi (kapali [20, 60]); kol theta 120 (acik)
    xa, xb = _band(i, P.KAPAK_X - 0.5, P.UST_RI + 0.2)
    g.append(((kure(E, P.UST_RO, 48) - kure(E, P.UST_RI, 48)) ^ _kama(i, m0, m1) ^ kutu(xa, xb, -100, 200, -100, 200))
             - disk_yz(E[1:], P.HALKA_GOBEK[2] + 0.5, xa - 1, xb + 1))
    xa, xb = _band(i, *P.UST_BANT)
    g.append(_sektor(i, 0.0, 8.0, m0, m1, xa, xb))
    g.append(disk_yz(E[1:], P.KAPAK_GOBEK_R, xa, xb))
    k = ust_kol_noktasi(i)
    g.append(yuvarlak_cubuk_yz(tuple(E[1:]), (k[1], k[2]), 2.2, xa, xb))
    G = birlestir(g)
    k2 = ust_kol_noktasi(i, P.UST_KOL["r2"])
    return cikar(G, [silindir((xa - 1, E[1], E[2]), (xb + 1, E[1], E[2]), P.M3 / 2 + 0.0, 20),
                     silindir((xa - 1, k[1], k[2]), (xb + 1, k[1], k[2]), P.TEL_DELIK / 2, 12),
                     silindir((xa - 1, k2[1], k2[2]), (xb + 1, k2[1], k2[2]), P.TEL_DELIK / 2, 12)])


def alt_bar_yz(aci_ofs=0.0):
    E = P.GOZ[0]
    t = math.radians(P.ALT_BAR["th_acik"] + aci_ofs)
    return E[1] + P.ALT_BAR["r"] * math.sin(t), E[2] + P.ALT_BAR["r"] * math.cos(t)


def B5e_alt_kapak(i):
    """ACIK (beta 0) konumda; iki yanda pivot; ic kol alt cubuga uzanir."""
    E = np.array(P.GOZ[i])
    a0, a1 = P.ALT_ACI_ACIK
    g = [_kabuk_bolge(i, P.ALT_RI, P.ALT_RO, a0, a1, P.KAPAK_X)]
    for ic in (False, True):
        xa, xb = _band(i, P.KAPAK_X - 0.5, P.ALT_RI + 0.2, ic)
        g.append(((kure(E, P.ALT_RO, 48) - kure(E, P.ALT_RI, 48)) ^ _kama(i, a0, a1) ^ kutu(xa, xb, -100, 200, -100, 200))
                 - disk_yz(E[1:], P.KAPAK_GOBEK_R + 0.45, xa - 1, xb + 1))
        xa, xb = _band(i, *P.ALT_BANT, ic)
        g.append(_sektor(i, 0.0, 8.0, a0, a1, xa, xb))
        g.append(disk_yz(E[1:], P.KAPAK_GOBEK_R, xa, xb))
        if ic:
            b = alt_bar_yz()
            g.append(yuvarlak_cubuk_yz(tuple(E[1:]), b, 3.5, xa, xb))
            bar_x = (xa, xb)
    G = birlestir(g)
    c = [silindir((E[0] - 25, E[1], E[2]), (E[0] + 25, E[1], E[2]), P.M3 / 2, 20)]
    b = alt_bar_yz()
    c.append(silindir((bar_x[0] - 1, b[0], b[1]), (bar_x[1] + 1, b[0], b[1]), P.ALT_BAR["kal"] + 0.15, 20))
    return cikar(G, c)


def alt_kol_noktasi():
    """alt cubuk tel kolu deligi (bas, ACIK konum): goz ekseninin altinda, kapanirken ~+Z hareket eder."""
    k = P.ALT_KOL
    E = P.GOZ[0]
    t = math.radians(k["th_acik"])
    return (k["x"], E[1] + k["r"] * math.sin(t), E[2] + k["r"] * math.cos(t))


def B5i_alt_cubuk():
    b = alt_bar_yz()
    x0 = _band(0, *P.ALT_BANT, ic=True)[0]
    x1 = _band(1, *P.ALT_BANT, ic=True)[1]
    g = silindir((x0, b[0], b[1]), (x1, b[0], b[1]), P.ALT_BAR["kal"], 24)
    k = P.ALT_KOL
    q = alt_kol_noktasi()
    g = g + yuvarlak_cubuk_yz(b, (q[1], q[2]), k["ru"], k["x"] - k["w"] / 2, k["x"] + k["w"] / 2)
    return g - silindir((k["x"] - 3, q[1], q[2]), (k["x"] + 3, q[1], q[2]), P.TEL_DELIK / 2, 12)


def B5a_cerceve():
    g = []
    y0 = P.B1_Y[1]
    for i in (0, 1):
        E = P.GOZ[i]
        xa, xb = _band(i, *P.CERCEVE_X)
        xa2, xb2 = _band(i, P.CERCEVE_X[0], P.CERCEVE_X[1] + 2.0)
        g.append(plaka_yz([(y0, 40.0), (y0, 59.0), (E[1] - 4.5, E[2] - 2.0), (E[1] + 4.5, E[2] + 0.5), (E[1] + 4.5, E[2] - 9.0),
                           (y0 + 3.0, 40.0)], xa, xb))
        g.append(disk_yz(E[1:], 4.5, xa2, xb2))
        # ayak
        ax = (33.5, 54.0)
        g.append(kutu(min(np.sign(E[0]) * ax[0], np.sign(E[0]) * ax[1]), max(np.sign(E[0]) * ax[0], np.sign(E[0]) * ax[1]),
                      y0, y0 + 3.0, 36.0, 59.0))
    ob = P.ORTA_BLOK
    g.append(kutu(-ob["x"], ob["x"], ob["y"][0], ob["y"][1], *ob["z"]))
    sp = P.ORTA_SAP
    import manifold3d as m3d
    for s in (-1, 1):                                                                           # iki sap (ayak -> orta blok)
        dx = sorted((s * sp["dus_x"][0], s * sp["dus_x"][1])); ux = sorted((s * sp["x"][0], s * sp["x"][1]))
        g.append(kutu(*dx, sp["y_alt"][0], y0 + 3.0, *sp["dus_z"]))
        a = kutu(*dx, sp["y_alt"][0], sp["y_alt"][1], *sp["dus_z"])
        b = kutu(*ux, sp["y_alt"][0], sp["y_alt"][1], *sp["z_on"])
        g.append(m3d.Manifold.batch_hull([a, b]))
        g.append(kutu(*ux, sp["y_alt"][0], ob["y"][0] + 0.01, *sp["z_on"]))
    G = birlestir(g)
    c = []
    E = P.GOZ[0]
    c.append(silindir((-25, E[1], E[2]), (25, E[1], E[2]), P.M3 / 2, 20))                     # ic M3 cubuk
    for s in (-1, 1):
        c.append(cq(somun_tuzagi("M3", vida_deligi=None), Tr(s * (ob["x"] - 3.0), E[1], E[2]) @ (Z2mX if s > 0 else Z2X)))
    for i in (0, 1):
        Ei = P.GOZ[i]
        xa, xb = _band(i, P.CERCEVE_X[0], P.CERCEVE_X[1] + 2.0)
        xi = xa if Ei[0] > 0 else xb                                                            # ic yuz
        c.append(cq(somun_tuzagi("M3", vida_deligi=P.M3), Tr(xi, Ei[1], Ei[2]) @ (Z2X if Ei[0] > 0 else Z2mX)))
    for x, z in B5_AYAK_VIDA:
        c.append(silindir((x, y0 - 1, z), (x, y0 + 4, z), P.M2 / 2, 16))
    return cikar(G, c)


def B5f_kol(ad):
    """Basili SG90 kolu: kit kolu cebi (K2 [TASLAK]) + tel deligi r. Servo-yerel (sablon) cercevede, mil ekseni."""
    s = P.SG[ad]
    k = SG_KOL
    z0 = k["Z1"] - k["ARM_T"]
    r = s["r"]
    import manifold3d as m3d
    a = silindir((0, 0, z0), (0, 0, z0 + P.SG_KOL_T), 6.0, 32)
    b = silindir((r, 0, z0), (r, 0, z0 + P.SG_KOL_T), 2.6, 20)
    g = m3d.Manifold.batch_hull([a, b])
    c = [cq(sg90_tek_kol_cebi(P.SG_KOL_PAY, kit_kol(ad)), Tr(0, 0, z0)),
         silindir((r, 0, z0 - 1), (r, 0, z0 + 5), P.TEL_DELIK / 2, 12),
         silindir((0, 0, z0 - 1), (0, 0, z0 + 5), 1.6, 16)]
    # kolun yonu: servo-yerel +x = bas +Z ; kol yonu (xz, bas) -> yerel aci
    yx, yz = s["yon"]
    ang = math.degrees(math.atan2(yx, yz))       # yerel x (bas Z) -> yerel y (bas X)
    G = cikar(g, c)
    return uygula(G, sg_T(ad) @ Rz(ang))


def kit_kol(ad):
    """Kit kolu (kisaltilmis): basili kolun r + KIT_KOL_UC otesi kesilir (kol ucu basili kolun icinde kalsin)."""
    return dict(SG_KOL, ARM_L=min(SG_KOL["ARM_L"], P.SG[ad]["r"] + P.KIT_KOL_UC))


def kol_ucu(ad, phi=0.0):
    """Kol tel deligi (bas, kolun ust/alt ortasi) servo acisi phi (deg) icin."""
    s = P.SG[ad]
    k = SG_KOL
    zc = k["Z1"] - k["ARM_T"] + P.SG_KOL_T / 2
    yx, yz = s["yon"]
    ang = math.degrees(math.atan2(yx, yz)) + phi
    a = math.radians(ang)
    p = sg_T(ad) @ np.array([s["r"] * math.cos(a), s["r"] * math.sin(a), zc, 1.0])
    return p[:3]


# ===================================================================================================== B4 cene + C1
def _cene_satirlar(s, n=21):
    """Mandibula govdesi (orta hat t=0 -> ramus t=1): alt kenar B, alveol ust kenari T, orta M (hafif dis bombe)."""
    import numpy as np
    B, T, Nn = [], [], []
    arka_T = [(33.9, -47.0, 67.9), (40.0, -46.0, 52.0), (50.0, -44.5, 36.0), (57.5, -43.0, 27.0)]
    arka_B = [(28.8, -74.0, 65.1), (38.0, -70.0, 47.0), (50.0, -63.5, 26.0), (57.0, -57.0, 9.0)]
    for t in np.linspace(0, 1, n):
        if t <= 0.6:
            a = t / 0.6 * 1.15
            T.append(np.array([s * 37.0 * math.sin(a), -47.0, 51.0 + 37.0 * math.cos(a) * 1.12]))
            yb = -78.0 + 4.0 * (a / 1.15) ** 2
            B.append(np.array([s * 31.5 * math.sin(a), yb, 51.0 + 31.5 * math.cos(a) * 1.12]))
            Nn.append(np.array([s * math.sin(a), 0.0, math.cos(a)]))
        else:
            w = (t - 0.6) / 0.4 * 3
            i = min(int(w), 2); f = w - i
            T.append(np.array(arka_T[i]) * (1 - f) + np.array(arka_T[i + 1]) * f); T[-1][0] *= s
            B.append(np.array(arka_B[i]) * (1 - f) + np.array(arka_B[i + 1]) * f); B[-1][0] *= s
            d = np.array(arka_T[i + 1]) - np.array(arka_T[i]); nn = np.array([-d[2], 0.0, d[0]]); nn /= np.linalg.norm(nn)
            nn[0] *= s; Nn.append(nn if nn[2] * 0 + (nn[0] * s) >= 0 else -nn)
    M = [(b + t_) / 2 + nn * 1.2 for b, t_, nn in zip(B, T, Nn)]
    return B, M, T, Nn


def B4_cene():
    import numpy as np
    from lib import serit, yassi_tup
    J = np.array(P.KONDIL)
    g = []
    for s in (-1, 1):
        # govde plakasi (3 satir bezier -> 5) + kalin alt kenar
        Bk, Mk, Tk, Nk = _cene_satirlar(s)
        C = [2 * m - (b + t) / 2 for b, m, t in zip(Bk, Mk, Tk)]
        rows = [[(1 - v) ** 2 * b + 2 * v * (1 - v) * c + v * v * t for b, c, t in zip(Bk, C, Tk)] for v in np.linspace(0, 1, 5)]
        g.append(serit(rows, 2.8))
        # alt kenar: govde -> gonial aci (disa kivrik) -> ramus arka kenari -> kondil boynu
        alt = [tuple(p) for p in Bk[::4]] + [(s * 58.5, -52.0, 4.5), (s * 59.5, -38.0, 3.5), (s * 60.0, -22.0, 3.5), (s * 60.0, -9.0, 4.5)]
        g.append(tup(alt, [4.2, 3.8, 3.6, 3.6, 3.6, 3.8, 3.4, 3.0, 2.8], seg=12))
        g.append(kure((s * 59.0, -56.5, 6.0), 4.2, 16))                                           # gonial aci cikintisi
        # ramus plakasi (x = 59): arka kenar / orta (sigmoid centik) / on kenar (koronoid ucu)
        X = s * 59.0
        arka = [(X, -50, 5.0), (X, -38, 3.5), (X, -26, 3.5), (X, -14, 4.0), (X, -6, 5.0)]
        orta = [(X, -48, 15.0), (X, -37, 14.0), (X, -25, 14.0), (X, -13, 15.0), (X, -9, 16.0)]
        on = [(X, -45, 26.0), (X, -36, 25.0), (X, -24, 25.0), (X, -12, 26.0), (X, -2, 30.0)]
        g.append(serit([arka, orta, on], 3.0))
        g.append(tup([(X, -2, 30.0), (X, -14, 26.5), (X, -30, 25.5), (X, -44, 27.5), tuple(Tk[-1])], 2.0, seg=12))   # koronoid / on kenar
        g.append(tup([tuple(Tk[k]) for k in range(12, len(Tk))], 1.8, seg=12))                     # alveol arka kenari
        g.append(tup([(s * 57.0, -41.0, 26.0), (s * 47.0, -55.0, 38.0), (s * 33.0, -63.0, 60.0)], [1.8, 1.6, 1.2], seg=12))   # dis egik cizgi
        xa, xb = sorted((s * P.CENE_TAB_X[0], s * P.CENE_TAB_X[1]))
        g.append(yuvarlak_cubuk_yz((J[1], J[2]), (J[1] - 12, J[2] - 2), 7.0, xa, xb))           # kondil dili
        for k in range(3):
            g.append(hex_bas((s * 60.7, J[1] - 34 - k * 6, J[2]), (s, 0, 0), r=1.9, h=1.0))
        k = 6
        g.append(hex_bas(Mk[k] + Nk[k] * 1.4, Nk[k], r=2.0, h=1.0))                                # zihin delikleri yerine civata
    # cene ucu (mental cikinti): ucgen kabarti
    import manifold3d as m3d
    g.append(m3d.Manifold.batch_hull([kure(p, 2.6, 12) for p in [(-13, -77.0, 86.5), (13, -77.0, 86.5), (0, -69.0, 90.0), (0, -78.5, 89.0)]]))
    g.append(tup([(0, -48.5, 92.0), (0, -58.0, 91.2), (0, -68.0, 90.0)], [1.4, 1.8, 2.4], seg=12))            # simfiz sirti
    on_T = [(37.0 * math.sin(a), -47.0, 51.0 + 37.0 * math.cos(a) * 1.12) for a in np.linspace(-1.15, 1.15, 17)]
    g.append(tup(on_T, 1.8, seg=12))                                                              # alveol kenari (alt)
    zc = J[2] + 41.0
    wedge = plaka_xz([(0, 0)] + [(60 * math.sin(a), 60 * math.cos(a)) for a in np.linspace(-1.15, 1.15, 24)], -200, 200)
    ty = J[1] - 47.5 + 0.0
    for k in range(14):
        a = -1.15 + k * 2.3 / 13
        on = abs(a) < 0.45
        R = 36.0
        cx, cz = R * math.sin(a), zc + R * math.cos(a) * 1.12 - 1.5
        h = 9.0 if on else 8.0                                                                   # eski kutu zarfi (boy)
        tip, w, kis, d = dis_olcu(k)
        w, d = min(w, 6.0 if on else 7.5), min(d, 4.5 if on else 7.0)
        g.append(uygula(dis(tip, w, h - kis, d, uc=+1), Tr(cx, ty + h / 2 - 2.0 - kis / 2, cz) @ Ry(math.degrees(a))))
    gum = (m3d.Manifold.cylinder(6, 35.5, 35.5, 64, True).rotate([90, 0, 0]) - m3d.Manifold.cylinder(7, 31.0, 31.0, 64, True).rotate([90, 0, 0]))
    g.append((gum.scale([1, 1, 1.12]).translate([0, ty - 4.0, zc])) ^ wedge.translate([0, 0, zc]))
    # cene kolu (sag, +X): rotil pimi
    kp = (J[1] + P.CENE_KOL[0], J[2] + P.CENE_KOL[1])
    g.append(yuvarlak_cubuk_yz((J[1] - 10, J[2] - 2), kp, 4.5, *P.CENE_LEVER_X))
    G = birlestir(g)
    vp = vida_pim_eklemi("M4", sabit_t=5.0, donen_t=4.0)
    c = []
    for s in (-1, 1):
        c.append(cq(vp["donen"], Tr(s * P.ASKI["x"][0], J[1], J[2]) @ (Z2X if s > 0 else Z2mX)))
    c.append(silindir((P.CENE_LEVER_X[0] - 1, kp[0], kp[1]), (P.CENE_LEVER_X[1] + 1, kp[0], kp[1]), P.M3 / 2, 16))
    c.append(cq(somun_tuzagi("M3"), Tr(P.CENE_LEVER_X[1] + 0.01, kp[0], kp[1]) @ Z2mX))
    return cikar(G, c)


def cene_kol_pimi(phi=0.0):
    J = np.array(P.KONDIL)
    p = np.array([P.ROTIL_X, J[1] + P.CENE_KOL[0], J[2] + P.CENE_KOL[1]])
    a = math.radians(phi)
    d = p - J
    return J + np.array([d[0], d[1] * math.cos(a) - d[2] * math.sin(a), d[1] * math.sin(a) + d[2] * math.cos(a)])


def krank_pimi(psi):
    c = P.CENE_SERVO
    a = math.radians(psi)
    return np.array([P.ROTIL_X, c["y"] - P.C1["r"] * math.cos(a), c["z"] + P.C1["r"] * math.sin(a)])


def C1_krank():
    """Notr (psi0) konumda. Disk kol cebi (servo_kolu [TASLAK]) + M3 rotil deligi r 20."""
    c = P.CENE_SERVO
    x0 = c["mil_x"] + P.MG_KOL_DISK["Y0"]
    x1 = x0 + P.C1["t"]
    pin = krank_pimi(P.C1["psi0"])
    g = yuvarlak_cubuk_yz((c["y"], c["z"]), (pin[1], pin[2]), 7.0, x0, x1)
    g = g + disk_yz((c["y"], c["z"]), 12.5, x0, x1)
    cut = [cq(mg996r_disk_kol_cebi(0.2), Tr(x0, c["y"], c["z"]) @ Z2X),
           disk_yz((c["y"], c["z"]), 2.5, x0 - 1, x1 + 1),
           disk_yz((pin[1], pin[2]), P.M3 / 2, x0 - 1, x1 + 1),
           cq(somun_tuzagi("M3"), Tr(x0 - 0.01, pin[1], pin[2]) @ Z2X)]
    return cikar(g, cut)


# ===================================================================================================== B6 mikrofon kabi
def B6_mikrofon(s):
    m = P.MIK
    cx, cy, cz = m["c"]
    x0 = 52.0 + m["kopuk"]
    x1 = x0 + m["boy"]
    r = m["od"] / 2
    g = disk_yz((cy, cz), r, s * x0, s * x1) if s > 0 else disk_yz((cy, cz), r, s * x1, s * x0)
    lo, hi = sorted((s * x0, s * x1))
    g = g - (disk_yz((cy, cz), r - 1.6, lo + (1.6 if s > 0 else 2.0), hi - (2.0 if s > 0 else 1.6)))
    # izgara: dis yuz delikleri
    xo = hi if s > 0 else lo
    c = []
    for dy in np.arange(-6, 6.1, 3.0):
        for dz in np.arange(-6, 6.1, 3.0):
            if dy * dy + dz * dz <= 40:
                c.append(silindir((xo - 3 * s, cy + dy, cz + dz), (xo + 3 * s, cy + dy, cz + dz), 0.75, 8))
    for dy in (-6.0, 6.0):
        xi = lo if s > 0 else hi
        c.append(silindir((xi - 2 * s, cy + dy, cz), (xi + 4 * s, cy + dy, cz), P.M2 / 2, 12))
    g = cikar(g, c)
    for k in range(6):                                                     # dis halka civatalari (gorsel)
        a = k * math.pi / 3
        g = g + hex_bas((xo, cy + 9.3 * math.sin(a), cz + 9.3 * math.cos(a)), (s, 0, 0), r=1.3, h=0.8)
    return g
