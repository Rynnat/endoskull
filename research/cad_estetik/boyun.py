"""Project Bust CP3b-2: boyun mekanizmasi (N1 yaw tablasi, N2 kolon + catal, N3 U-hac, N4 kranklar, N5 kiliflar, Y1 kaplin,
yay, P1 SCM pistonlari) + kinematik (egme krank cozumu, kardan acilari) + pozlu montaj modeli.

Olculer: params_boyun.py (PB). Bas parcalari bas.py'den (B1 burada yalniz P1 dilleriyle genisletilir: B1 = bas.B1() + dil).
Cerceveler: yaw_T(p) = Ry(yaw); hac_T(p) = yaw_T Rx(-pitch); bas_T(p) = hac_T Rz(roll)  (kin.bas_T ile ayni).
"""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np

import params as P
import params_boyun as PB
from lib import (Rx, Ry, Rz, Tr, uygula, kutu, kutu_c, silindir, birlestir, cikar, cq, disk_yz, plaka_xz, plaka_yz,
                 yuvarlak_cubuk_yz, eksen_etrafi, nokta, hex_bas)
from sablonlar.servo_kolu import mg996r_disk_kol_cebi, mg996r_disk_kol
from sablonlar.baglanti import somun_tuzagi
from bas import Z2X, Z2mX, Z2Y, Z2mY, Z2mZ

M3, M4 = P.M3, P.M4
YAT = P.YATAY


# ===================================================================== cerceveler
def yaw_T(p):
    return Ry(p.get("bas_yaw", 0.0))


def hac_T(p):
    return yaw_T(p) @ Rx(-p.get("bas_pitch", 0.0))


def bas_T(p):
    return hac_T(p) @ Rz(p.get("bas_roll", 0.0))


def egme_mg_T(s):
    """MG996R mil-ucu cercevesi (yerel z = mil) -> yaw cercevesi. s=+1 sol (+X, mil -X'e), s=-1 sag."""
    e = PB.EGME
    M = np.eye(4)
    M[:3, 0] = (0, 0, 1)                 # yerel x (govde boyu) -> +Z (one)
    M[:3, 1] = (0, s, 0)
    M[:3, 2] = (-s, 0, 0)                # mil
    M[:3, 3] = (s * e["x_uc"], e["y"], e["z"])
    return M


# ===================================================================== N1 yaw tablasi
def _oval_xz(c, r, teget, y0, y1, ofs=3.0, n=7):
    """(x, z) merkezli, teget yonde +-ofs oval delik (Y boyunca)."""
    t = np.asarray(teget, float); t /= np.linalg.norm(t)
    pts = [(c[0] + t[0] * d, c[1] + t[1] * d) for d in np.linspace(-ofs, ofs, n)]
    import manifold3d as m3d
    return m3d.Manifold.batch_hull([silindir((x, y0, z), (x, y1, z), r, 16) for x, z in pts])


def _dil(c, eksen, yukari, h, w=None, t=None, pah=None, delik=None, ic=0.0):
    """Kardan ankraj dili: pim merkezi c, pim ekseni 'eksen', dilin govdeye dogru yonu -'yukari' (dil yukari'nin tersine uzanir
    degil: dil c'den 'yukari' yonunde h kadar govdeye uzanir). Kalinlik pim ekseni boyunca t, genislik w. Delik M3 + yatay pay."""
    w = w or PB.DIL["w"]; t = t or PB.DIL["t"]
    c = np.asarray(c, float); a = np.asarray(eksen, float); a /= np.linalg.norm(a)
    u = np.asarray(yukari, float); u = u - a * (u @ a); u /= np.linalg.norm(u)
    v = np.cross(u, a)
    M = np.eye(4); M[:3, 0] = a; M[:3, 1] = v; M[:3, 2] = u; M[:3, 3] = c
    # yerel: x = pim ekseni (kalinlik), y = genislik, z = govdeye dogru; pim merkezi z 0, alt uc yarim daire
    g = birlestir([kutu(-t / 2, t / 2, -w / 2, w / 2, 0, h), silindir((-t / 2, 0, 0), (t / 2, 0, 0), w / 2, 28)])
    g = g - silindir((-t, 0, 0), (t, 0, 0), (M3 + YAT) / 2, 16)
    return uygula(g, M)


def N1():
    y0, y1 = PB.N1_Y
    g = [silindir((0, y0, 0), (0, y1, 0), PB.N1_R, 72)]
    ux, uy, uz = PB.P1_ALT
    for s in (-1, 1):
        # P1 alt dil kolu + dil
        g.append(plaka_xz([(s * 34.0, -30.0), (s * 46.0, -40.0), (s * (ux + 8.0), uz + 2.0), (s * (ux + 6.0), uz - 8.0),
                           (s * (ux - 8.0), uz - 8.0), (s * 22.0, -40.0)], y0, y1))
        g.append(_dil((s * ux, uy, uz), _p1_notr(s)[1][0], (0, -1, 0), uy - y1 + 0.01))
        # servo braketi (dik plaka) + taban
        b = PB.BRAKET
        bx = sorted((s * b["x"][0], s * b["x"][1]))
        g.append(kutu(bx[0], bx[1], y1 - 0.01, b["y"][1], b["z"][0], b["z"][1]))
        bx2 = sorted((s * (b["x"][0] - 4.0), s * (b["x"][1] + 2.0)))
        g.append(kutu(bx2[0], bx2[1], y0, y1, b["z"][0], b["z"][1]))
        # braket kosegen dayanagi (one / arkaya)
        g.append(m3d_kosegen(s, b["z"][1] - 2.0))      # yalniz on dayanak (arkada P1 dis tupu geciyor)
    # yay diregi (arka kol + dik levha, delikler yay hatti boyunca)
    d = PB.YAY_DIREK
    hs = [yay_delik(t) for t in PB.YAY_DELIKLER]
    import manifold3d as m3d
    zmin = min(h[2] for h in hs) - d["pay"]
    g.append(plaka_xz([(-10.0, -40.0), (d["x"][1] + 4.0, -40.0), (d["x"][1] + 4.0, zmin - 2.0), (-10.0, zmin - 2.0)], y0, y1))
    # delik cubugu (yay hattina paralel) + tek ayak (en alttaki delikten N1'e) + ayak dayanagi: gorsel olarak ince kafes
    g.append(m3d.Manifold.batch_hull([silindir((d["x"][0], h[1], h[2]), (d["x"][1], h[1], h[2]), d["pay"], 24) for h in hs]))
    hb = max(hs, key=lambda h: -h[2])
    g.append(m3d.Manifold.batch_hull([silindir((d["x"][0], hb[1], hb[2]), (d["x"][1], hb[1], hb[2]), d["pay"], 24),
                                      kutu(d["x"][0], d["x"][1], y1 - 0.01, y1, hb[2] - d["pay"], hb[2] + d["pay"] + 6.0)]))
    g.append(m3d.Manifold.batch_hull([kutu(d["x"][0], d["x"][1], y1 - 0.01, y1, hb[2] + d["pay"], hb[2] + d["pay"] + 26.0),
                                      kutu(d["x"][0], d["x"][1], -80.0, -78.0, hb[2] + d["pay"] - 0.5, hb[2] + d["pay"])]))
    G = birlestir(g)
    c = []
    # Y1 cebi + Oldham yariklari
    c.append(silindir((0, y0 - 1, 0), (0, y0 + PB.N1_CEP["derin"], 0), PB.N1_CEP["r"], 48))
    o = PB.OLDHAM
    for s in (-1, 1):
        c.append(kutu(*sorted((s * (o["r"] - o["yarik_L"] / 2), s * (o["r"] + o["yarik_L"] / 2))), y0 - 1, y1 + 1, -o["yarik_w"] / 2, o["yarik_w"] / 2))
    # lazy susan ust halka vidalari (oval, teget) + ustte havsa
    for x, z in PB.N1_LS_DELIK:
        teg = (-z, x)
        c.append(_oval_xz((x, z), M3 / 2, teg, y0 - 1, y1 + 1))
        c.append(_oval_xz((x, z), 3.2, teg, y1 - 2.0, y1 + 1))
    # N2 flans vidalari (somun altta, tezgahta)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        x, z = PB.N2_FLANS["vida_r"] * math.cos(a), PB.N2_FLANS["vida_r"] * math.sin(a)
        c.append(silindir((x, y0 - 1, z), (x, y1 + 1, z), M3 / 2, 16))
        c.append(cq(somun_tuzagi("M3", vida_deligi=M3), Tr(x, y0 - 0.01, z) @ Z2Y))
    # kablo deligi
    kc = PB.N1_KABLO
    c.append(silindir((kc["c"][0], y0 - 1, kc["c"][1]), (kc["c"][0], y1 + 1, kc["c"][1]), kc["r"], 24))
    # krank supurmesi (alt pozda krank ucu tablaya iner)
    for s in (-1, 1):
        x0, x1 = sorted((s * 26.5, s * 34.5))
        c.append(kutu(x0, x1, y1 - 3.0, y1 + 1, PB.EGME["z"] - 2.0, PB.EGME["z"] + 30.0))
    # servo braketi: govde penceresi + M4 kulak delikleri
    for s in (-1, 1):
        T = egme_mg_T(s)
        pp = P.MG_CEP_PAY
        c.append(uygula(kutu(-P.MG["N"] - pp / 2, P.MG["L"] - P.MG["N"] + pp / 2, -P.MG["W"] / 2 - pp / 2, P.MG["W"] / 2 + pp / 2,
                             -60, P.MG["KULAK_Z0"] + 0.01), T))
        xc = (P.MG["L"] - 2 * P.MG["N"]) / 2
        for sx in (-1, 1):
            for sy in (-1, 1):
                q = nokta(T, (xc + sx * P.MG["KULAK_DX"], sy * P.MG["KULAK_DY"], 0))
                c.append(silindir((s * 40.0, q[1], q[2]), (s * 60.0, q[1], q[2]), M4 / 2 + YAT / 2, 16))
    # yay delikleri (X ekseni)
    d = PB.YAY_DIREK
    for t in PB.YAY_DELIKLER:
        h = yay_delik(t)
        c.append(silindir((d["x"][0] - 1, h[1], h[2]), (d["x"][1] + 1, h[1], h[2]), 1.2, 12))
    # hafifletme (tabla): on yarim ay
    c.append(plaka_xz([(-30, 20), (30, 20), (34, 34), (20, 44), (-20, 44), (-34, 34)], y0 - 1, y1 + 1))
    return cikar(G, c)


def yay_delik(t=0.0):
    """yay ankraj deligi (yaw cercevesi): nominal + t * (kafa notr noktasindan ankraja birim yon)."""
    A = np.array(PB.YAY_ANKRAJ, float); H = np.array(PB.YAY_KAFA, float)
    u = (A - H) / np.linalg.norm(A - H)
    return A + t * u


def m3d_kosegen(s, zc):
    """braket dis yuzune ucgen dayanak (YZ kesitli, X'te 4 mm)."""
    b = PB.BRAKET
    y1 = PB.N1_Y[1]
    tri = plaka_xz([(s * b["x"][1] - s * 0.01, zc - 2.0), (s * (b["x"][1] + 10.0), zc - 2.0), (s * (b["x"][1] + 10.0), zc + 2.0),
                    (s * b["x"][1] - s * 0.01, zc + 2.0)], y1 - 0.01, y1 + 3.0)
    import manifold3d as m3d
    top = kutu(*sorted((s * b["x"][1] - s * 0.01, s * (b["x"][1] + 0.6))), b["y"][1] - 16.0, b["y"][1] - 15.4, zc - 2.0, zc + 2.0)
    return m3d.Manifold.batch_hull([tri, top])


# ===================================================================== N2 boyun kolonu + catal
def _kolon_kesit(y0, y1, x, z0, z1, rk):
    import manifold3d as m3d
    pts = []
    for cx, cz in ((x - rk, z1 - rk), (-x + rk, z1 - rk), (-x + rk, z0 + rk), (x - rk, z0 + rk)):
        pts.append(silindir((cx, y0, cz), (cx, y1, cz), rk, 20))
    return m3d.Manifold.batch_hull(pts)


def N2():
    y1 = PB.N1_Y[1]
    f = PB.N2_FLANS
    ct = PB.CATAL
    k = PB.N2_KOLON
    g = [silindir((0, y1, 0), (0, y1 + f["t"], 0), f["r"], 48)]
    g.append(_kolon_kesit(y1 + f["t"] - 0.01, ct["y_alt"] + 0.01, k["x"], k["z"][0], k["z"][1], k["r_kose"]))
    # omur halkalari (ince, gorsel yogunluk)
    for y, w in PB.N2_OMUR:
        g.append(_kolon_kesit(y - PB.N2_OMUR_T / 2, y + PB.N2_OMUR_T / 2, w, k["z"][0] - 1.0, k["z"][1] + 2.0, 6.0))
    # catal koprusu + kollar
    g.append(kutu(-ct["x"][1], ct["x"][1], ct["y_alt"], ct["y_alt"] + ct["kopru"], -ct["z"], ct["z"]))
    for s in (-1, 1):
        x0, x1 = sorted((s * ct["x"][0], s * ct["x"][1]))
        g.append(kutu(x0, x1, ct["y_alt"], 0.0, -ct["z"], ct["z"]))
        g.append(silindir((x0, 0, 0), (x1, 0, 0), ct["ust_r"], 32))
    # kablo kancasi
    kc = PB.N2_KABLO_KANCA["c"]
    g.append(silindir((kc[0], kc[1] - 4, kc[2]), (kc[0], kc[1] + 4, kc[2]), 4.5, 20) - silindir((kc[0], kc[1] - 5, kc[2]), (kc[0], kc[1] + 5, kc[2]), 2.7, 20))
    g.append(kutu(kc[0] + 1.5, -k["x"] + 1.0, kc[1] - 4, kc[1] + 4, kc[2] - 1.8, kc[2] + 1.8))
    G = birlestir(g)
    c = []
    for kk in range(4):
        a = math.radians(45 + 90 * kk)
        x, z = f["vida_r"] * math.cos(a), f["vida_r"] * math.sin(a)
        c.append(silindir((x, y1 - 1, z), (x, y1 + f["t"] + 1, z), M3 / 2, 16))
        c.append(silindir((x, y1 + f["t"], z), (x, y1 + f["t"] + 20, z), 3.3, 16))   # vida basi / alet
    # catal pimleri: M4 serbest (catal doner, vida hacta sabit)
    c.append(silindir((-ct["x"][1] - 1, 0, 0), (ct["x"][1] + 1, 0, 0), (M4 + YAT) / 2, 20))
    # ic bosaltma (kolon kabuk 2.4)
    c.append(_kolon_kesit(y1 - 1.0, ct["y_alt"] - 3.0, k["x"] - 2.4, k["z"][0] + 2.4, k["z"][1] - 2.4, k["r_kose"] - 2.4))
    return cikar(G, c)


# ===================================================================== N3 U-hac
def N3():
    h = PB.HAC
    import manifold3d as m3d
    g = m3d.Manifold.batch_hull([kutu(-h["x"], h["x"], -h["y"] + 2, h["y"] - 2, -h["z"], h["z"]),
                                 kutu(-h["x"] + 2, h["x"] - 2, -h["y"], h["y"], -h["z"] + 2, h["z"] - 2)])
    c = [silindir((0, 0, -h["z"] - 1), (0, 0, h["z"] + 1), (M4 + YAT) / 2, 20)]
    for s in (-1, 1):
        x0, x1 = sorted((s * (h["x"] + 1), s * (h["x"] - PB.HAC_PIM_DERIN)))
        c.append(silindir((x0, 0, 0), (x1, 0, 0), 3.3 / 2, 16))
    # hafifletme ceplari (Y), roll/pitch deliklerine 2 mm et
    for sx in (-1, 1):
        for sz in (-1, 1):
            c.append(kutu(*sorted((sx * 4.5, sx * 10.0)), -h["y"] - 1, h["y"] + 1, *sorted((sz * 4.5, sz * 7.5))))
    return cikar(g, c)


# ===================================================================== N4 krank, N5 kilif, Y1
def krank_pimi(s, psi, r):
    e = PB.EGME
    a = math.radians(psi)
    return np.array([s * PB.ROTIL_X, e["y"] + r * math.sin(a), e["z"] + r * math.cos(a)])


def N4(s, pay=0.2):
    e = PB.EGME
    k = PB.KRANK
    xf = s * (e["x_uc"] - P.MG_KOL_DISK["Y0"])        # servo tarafi yuz
    xi = xf - s * k["t"]
    x0, x1 = sorted((xf, xi))
    g = birlestir([disk_yz((e["y"], e["z"]), k["hub_r"], x0, x1, 40),
                   yuvarlak_cubuk_yz((e["y"], e["z"]), (e["y"], e["z"] + k["r1"]), k["uc_r"], x0, x1)])
    c = [cq(mg996r_disk_kol_cebi(pay), Tr(xf, e["y"], e["z"]) @ (Z2mX if s > 0 else Z2X)),
         disk_yz((e["y"], e["z"]), 2.5, x0 - 1, x1 + 1)]
    for r in (k["r1"], k["r2"]):
        c.append(disk_yz((e["y"], e["z"] + r), M3 / 2, x0 - 1, x1 + 1, 16))
        c.append(cq(somun_tuzagi("M3", vida_deligi=M3), Tr(xf, e["y"], e["z"] + r) @ (Z2mX if s > 0 else Z2X)))
    return cikar(g, c)


def N5():
    """pushrod kilifi: O11 / et 1.2, M3 rod uzerinde (rod ortasi), uclar kapali (O3.4 delik) - yerel Z boyunca."""
    n = PB.N5
    g = silindir((0, 0, 0), (0, 0, n["boy"]), n["r"], 32) - silindir((0, 0, 1.6), (0, 0, n["boy"] - 1.6), n["r"] - n["et"], 32)
    g = g - silindir((0, 0, -1), (0, 0, n["boy"] + 1), 1.7, 16)
    for z in (6.0, n["boy"] / 2, n["boy"] - 6.0):           # gorsel halka oluklari
        g = g - (silindir((0, 0, z - 0.4), (0, 0, z + 0.4), n["r"] + 1, 32) - silindir((0, 0, z - 1), (0, 0, z + 1), n["r"] - 0.5, 32))
    return g


def Y1():
    y = P.YAW_SERVO["mil_y"] + P.MG_KOL_DISK["Y0"]
    t = PB.Y1["t"]; o = PB.OLDHAM
    g = silindir((0, y, 0), (0, y + t, 0), PB.Y1["r"], 48)
    for s in (-1, 1):
        g = g + silindir((s * o["r"], y + t - 0.01, 0), (s * o["r"], y + t + PB.Y1["pim_h"], 0), o["pim_d"] / 2, 20)
    c = [cq(mg996r_disk_kol_cebi(0.2), Tr(0, y, 0) @ Z2Y), silindir((0, y - 1, 0), (0, y + t + 1, 0), 2.5, 16),
         silindir((0, y + t - 1.5, 0), (0, y + t + 1, 0), 3.0, 16)]
    return cikar(g, c)


# ===================================================================== kinematik: egme
ROD_L = float(np.linalg.norm(krank_pimi(1, 0.0, PB.KRANK["r1"]) - np.array([PB.ROTIL_X, *PB.ROTIL_KAFA])))


def kafa_rotil(s):
    return np.array([s * PB.ROTIL_X, *PB.ROTIL_KAFA])


def egme_coz(p, r=None):
    """{s: psi (deg) ya da None} - krank acisi (+ = yukari). r: krank deligi (varsayilan r1)."""
    r = r or PB.KRANK["r1"]
    e = PB.EGME
    Ti = np.linalg.inv(yaw_T(p))
    out = {}
    for s in (1, -1):
        H = nokta(Ti @ bas_T(p), kafa_rotil(s))
        dx = s * PB.ROTIL_X - H[0]; dy = H[1] - e["y"]; dz = H[2] - e["z"]
        R = math.hypot(dy, dz)
        K = (r * r + dy * dy + dz * dz + dx * dx - ROD_L ** 2) / (2 * r)
        if abs(K) > R:
            out[s] = None
            continue
        phi = math.atan2(dy, dz); a = math.acos(K / R)
        cand = [math.degrees(phi + a), math.degrees(phi - a)]
        cand = [((c + 180) % 360) - 180 for c in cand]
        out[s] = min(cand, key=abs)
    return out


def rotil_acilari(p, psi, r=None):
    """her rod icin (alt rotil acisi, ust rotil acisi) deg: rod yonunun civata eksenine dik duzlemden sapmasi."""
    r = r or PB.KRANK["r1"]
    out = {}
    for s in (1, -1):
        if psi[s] is None:
            out[s] = None
            continue
        C = nokta(yaw_T(p), krank_pimi(s, psi[s], r))
        H = nokta(bas_T(p), kafa_rotil(s))
        d = (H - C) / np.linalg.norm(H - C)
        ax_y = yaw_T(p)[:3, 0]; ax_b = bas_T(p)[:3, 0]
        out[s] = (math.degrees(math.asin(abs(d @ ax_y))), math.degrees(math.asin(abs(d @ ax_b))))
    return out


# ===================================================================== kinematik: P1 kardan
def _p1_ust(s):
    u = np.array(PB.P1_UST); u[0] *= s; return u


def _p1_alt(s):
    u = np.array(PB.P1_ALT); u[0] *= s; return u


@lru_cache(maxsize=None)
def _p1_notr(s):
    """(a1_ust, n_ust) bas cercevesinde, (a1_alt, n_alt) yaw cercevesinde. n = poz izgarasindaki pim-pim yonlerinin ortalamasi,
    a1 (pim2 ekseni, dil kalinlik yonu) = X'in n'ye dik bileseni -> iki eksenin acilari aralik ortasinda (K5: pim1 ekseni +-25)."""
    du, da = [], []
    for pt in PB.POZ_PITCH:
        for rl in (-15.0, 0.0, 15.0):
            p = dict(bas_yaw=0.0, bas_pitch=pt, bas_roll=rl)
            U = nokta(bas_T(p), _p1_ust(s)); A = nokta(yaw_T(p), _p1_alt(s))
            d = (A - U) / np.linalg.norm(A - U)
            du.append(np.linalg.inv(bas_T(p))[:3, :3] @ d)
            da.append(-(np.linalg.inv(yaw_T(p))[:3, :3] @ d))
    out = []
    for dd in (du, da):
        n = np.mean(dd, 0); n /= np.linalg.norm(n)
        a = np.array([1.0, 0, 0]) - n * n[0]; a /= np.linalg.norm(a)
        out.append((tuple(a), tuple(n)))
    return tuple(out)


def _kardan(A, a1, n0, d):
    """A: pim2 merkezi (dunya), a1: pim2 ekseni, n0: notr orta yonu (a1'e dik), d: hedef yon. -> (alfa, beta, n', a2', pim1)."""
    a1 = a1 / np.linalg.norm(a1)
    b = np.cross(a1, n0)
    al = math.atan2(d @ b, d @ n0)
    n1 = math.cos(al) * n0 + math.sin(al) * b
    a2 = np.cross(n1, a1)
    be = math.asin(max(-1.0, min(1.0, d @ a1)))
    pin1 = A + (PB.KARDAN["pin1"] - PB.KARDAN["pin2"]) * n1
    return math.degrees(al), math.degrees(be), n1, a2, pin1


def p1_coz(p, s):
    """-> dict(ust=(alfa, beta, n1, a2, pin1), alt=(...), L=pin1-pin1 mesafesi, d=yon (ust->alt))."""
    Tb, Ty = bas_T(p), yaw_T(p)
    (a1u, nu), (a1a, na) = _p1_notr(s)
    U = nokta(Tb, _p1_ust(s)); A = nokta(Ty, _p1_alt(s))
    au = Tb[:3, :3] @ np.array(a1u); aa = Ty[:3, :3] @ np.array(a1a)
    nU = Tb[:3, :3] @ np.array(nu); nA = Ty[:3, :3] @ np.array(na)
    pu, pa = U, A
    for _ in range(4):
        d = (pa - pu) / np.linalg.norm(pa - pu)
        ku = _kardan(U, au, nU, d)
        ka = _kardan(A, aa, nA, -d)
        pu, pa = ku[4], ka[4]
    d = (pa - pu) / np.linalg.norm(pa - pu)
    return dict(ust=ku, alt=ka, L=float(np.linalg.norm(pa - pu)), d=d)


# ===================================================================== P1 parcalari (yerel cerceve)
def kardan_orta():
    """K5 kuponu K5_kardan_orta (manifold'a tasindi): pim2 X ekseni z 4.5, pim1 Y ekseni z 19.1."""
    k = PB.KARDAN
    i, o = k["gap"] / 2, k["gap"] / 2 + k["ct"]
    cw = k["cw"]
    g = [kutu(-o, o, -o, o, k["b0"], k["b1"])]
    for s in (-1, 1):
        g.append(kutu(*sorted((s * i, s * o)), -cw / 2, cw / 2, 0, k["b0"] + 0.01))
        g.append(kutu(-cw / 2, cw / 2, *sorted((s * i, s * o)), k["b1"] - 0.01, k["pin1"]))
        g.append(silindir((0, min(s * i, s * o), k["pin1"]), (0, max(s * i, s * o), k["pin1"]), cw / 2, 28))
    G = birlestir(g)
    c = [silindir((-o - 1, 0, k["pin2"]), (o + 1, 0, k["pin2"]), (M3 + YAT) / 2, 16),
         silindir((0, -o - 1, k["pin1"]), (0, o + 1, k["pin1"]), (M3 + YAT) / 2, 16)]
    return cikar(G, c)


def _tup_dilli(od, et, boy, kapali=True):
    """K5 _k5_kardan_tup: dil (pim ekseni Y, z 5) + 45 deg koni + tup (yerel Z). Dil z 0..10."""
    dl = PB.DIL
    w, t, h = dl["w"], dl["t"], dl["h"]
    import manifold3d as m3d
    prof = [(-w / 2 + dl["pah"], 0), (w / 2 - dl["pah"], 0), (w / 2, dl["pah"]), (w / 2, h), (-w / 2, h), (-w / 2, dl["pah"])]
    cs = m3d.CrossSection([[(float(x), float(z)) for x, z in prof]])
    d = uygula(m3d.Manifold.extrude(cs, t), np.array([[1, 0, 0, 0], [0, 0, 1, -t / 2], [0, 1, 0, 0], [0, 0, 0, 1.0]]))
    d = d - silindir((0, -t, dl["delik"]), (0, t, dl["delik"]), (M3 + YAT) / 2, 16)
    oh = od / 2 - t / 2
    kon = silindir((0, 0, h - 0.01), (0, 0, h + oh), t / 2, 32, r1=od / 2)
    z0 = h + oh
    tup = silindir((0, 0, z0 - 0.01), (0, 0, z0 + boy), od / 2, 40) - silindir((0, 0, z0 + 1.2), (0, 0, z0 + boy + 1), od / 2 - et, 40)
    return birlestir([d, kon, tup]), z0


def p1_tup_olcu():
    """(dis OD, ic OD, Ldis, Lic, z0_dis, z0_ic, bindirme_min, bilgi) pim1-pim1 mesafesi araligindan (poz izgarasi)."""
    Ls = []
    for pt in PB.POZ_PITCH:
        for rl in (-15.0, -7.5, 0.0, 7.5, 15.0):
            Ls.append(p1_coz(dict(bas_yaw=0.0, bas_pitch=pt, bas_roll=rl), 1)["L"])
    Lmin, Lmax = min(Ls), max(Ls)
    t = PB.TUP
    od_d = t["od"]; od_i = od_d - 2 * t["et"] - 2 * t["bosluk"]
    z0d = PB.DIL["h"] + od_d / 2 - PB.DIL["t"] / 2 - PB.DIL["delik"]     # pim1 -> tup baslangici
    z0i = PB.DIL["h"] + od_i / 2 - PB.DIL["t"] / 2 - PB.DIL["delik"]
    bos = Lmin - z0d - z0i - PB.STROK_PAY - 0.5  # en kisa pozda tuplerin kullanabilecegi boy (0.5 sayisal pay)
    Ld = round(bos, 1); Li = round(bos - 1.2, 1)  # ic tup ucu dis tupun kapali tabanina STROK_PAY
    bind = Ld + Li - (Lmax - z0d - z0i)
    return dict(od_d=od_d, od_i=od_i, Ld=Ld, Li=Li, z0d=z0d, z0i=z0i, Lmin=Lmin, Lmax=Lmax, bindirme=bind)


def P1_dis(bosluk=None):
    o = p1_tup_olcu()
    g, _ = _tup_dilli(o["od_d"], PB.TUP["et"], o["Ld"])
    return g


def P1_ic(bosluk=None):
    b = PB.TUP["bosluk"] if bosluk is None else bosluk
    o = p1_tup_olcu()
    od = PB.TUP["od"] - 2 * PB.TUP["et"] - 2 * b
    g, _ = _tup_dilli(od, PB.TUP["et"], o["Li"])
    return g


def B1_boyun():
    """B1 (bas.py) + P1 ust dilleri (mastoid alti). Diger arayuzler (roll/rotil/yay kulaklari) bas.B1'de."""
    import bas as B
    r = P.RZ_YAY
    g = [B.B1() - kutu(-r["x"] - 0.01, r["x"] + 0.01, r["y"][0] - 0.01, P.B1_Y[0] - 0.01, r["z"][0] - 0.01, r["z"][1] + 0.01)]
    # yay kulagi x 6..10 (eski x 0 kulagi roll pimi -Z sokme yolundaydi)
    yk = PB.YAY_KAFA
    k = kutu(yk[0] - 2.0, yk[0] + 2.0, r["y"][0], P.B1_Y[0] + 1.0, r["z"][0], r["z"][1])
    g.append(k - silindir((yk[0] - 3, yk[1], yk[2]), (yk[0] + 3, yk[1], yk[2]), 1.3, 12))
    for s in (-1, 1):
        u = _p1_ust(s)
        g.append(_dil(u, _p1_notr(s)[0][0], (0, 1, 0), P.B1_Y[1] - u[1] + 1.0))
    return birlestir(g)


# ===================================================================== satin alinan + pozlu montaj
def _cerceve(o, x, y, z):
    M = np.eye(4); M[:3, 0] = x; M[:3, 1] = y; M[:3, 2] = z; M[:3, 3] = o; return M


def rotil_geo(merkez, eksen, yon):
    """M3 rotil: goz ekseni 'eksen', govde 'yon' dogrultusunda (dunya)."""
    r = P.ROTIL
    c = np.asarray(merkez, float); a = np.asarray(eksen, float); a /= np.linalg.norm(a)
    d = np.asarray(yon, float); d /= np.linalg.norm(d)
    g = silindir(c - a * r["GOZ_T"] / 2, c + a * r["GOZ_T"] / 2, r["GOZ_D"] / 2, 24)
    g = g + silindir(c + d * (r["GOZ_D"] / 2 - 1.0), c + d * (r["GOZ_D"] / 2 + r["GOVDE_L"]), r["GOVDE_D"] / 2, 16)
    return g


def statik_parcalar():
    """{ad: (Manifold, grup, cerceve)} yerel geometri; cerceve: 'yaw' | 'hac' | 'bas' | 'krankL/R' | 'sabit'."""
    import satin as S
    out = {}
    for s, nm in ((1, "L"), (-1, "R")):
        out[f"egme_mg996r_{nm}"] = (uygula(S.mg996r_model(), egme_mg_T(s)), "yaw")
        out[f"egme_mgkol_{nm}"] = (uygula(cq(mg996r_disk_kol()), egme_mg_T(s)), f"krank{nm}")
    # M4 pimler: roll (Z, bas) ve pitch saplamalari (X, hac)
    out["pim_roll_M4x40"] = (silindir((0, 0, -16.8 - 2.8), (0, 0, 16.8 + 4.5), 2.0, 16) +
                             silindir((0, 0, -16.8 - 2.8), (0, 0, -16.8), 3.5, 6), "bas")   # kafa arkada (-Z), nyloc onde
    for s, nm in ((1, "L"), (-1, "R")):
        x0 = s * (PB.CATAL["x"][1] + 0.4)
        out[f"pim_pitch_{nm}"] = (silindir((x0 - s * 14.0, 0, 0), (x0, 0, 0), 2.0, 16) + silindir((x0, 0, 0), (x0 + s * 2.8, 0, 0), 3.5, 6), "hac")
    return out


def poz(p, r=None, p1=True):
    """{ad: (Manifold, 4x4)} dunya cercevesinde, boyun tarafi (basili N + satin + rod/rotil/yay/P1). Basili bas parcalari dahil degil.
    Doner: (parcalar, bilgi) bilgi: psi, rotil acilari, P1 cozumleri, yay boyu."""
    import build as BLD
    r = r or PB.KRANK["r1"]
    Ty, Th, Tb = yaw_T(p), hac_T(p), bas_T(p)
    out = {}
    psi = egme_coz(p, r)
    for ad in ("N1", "N2", "Y1"):
        out[ad] = (BLD.yukle(ad), Ty)
    out["N3"] = (BLD.yukle("N3"), Th)
    for s, nm in ((1, "L"), (-1, "R")):
        ps = psi[s] if psi[s] is not None else 0.0
        Tk = Ty @ eksen_etrafi((0, PB.EGME["y"], PB.EGME["z"]), Rx(-ps))
        out[f"N4_{nm}"] = (BLD.yukle(f"N4_{nm}"), Tk)
        C = nokta(Ty, krank_pimi(s, ps, r)); H = nokta(Tb, kafa_rotil(s))
        u = (H - C) / np.linalg.norm(H - C)
        out[f"rotil_alt_{nm}"] = (rotil_geo(C, Ty[:3, 0], u), np.eye(4))
        out[f"rotil_ust_{nm}"] = (rotil_geo(H, Tb[:3, 0], -u), np.eye(4))
        rl = P.ROTIL["GOZ_D"] / 2 + P.ROTIL["GOVDE_L"] - 0.5
        out[f"rod_{nm}"] = (silindir(C + u * rl, H - u * rl, 1.5, 12), np.eye(4))
        L = float(np.linalg.norm(H - C)); n = PB.N5
        k0 = C + u * (L - n["boy"]) / 2
        out[f"N5_{nm}"] = (BLD.yukle("N5"), _cerceve(k0, *_dik_taban(u)))
    for ad, (m, g) in statik_parcalar().items():
        T = {"yaw": Ty, "hac": Th, "bas": Tb}.get(g)
        if T is None:      # krank grubu
            nm = g[-1]; s = 1 if nm == "L" else -1
            ps = psi[s] if psi[s] is not None else 0.0
            T = Ty @ eksen_etrafi((0, PB.EGME["y"], PB.EGME["z"]), Rx(-ps))
        out[ad] = (m, T)
    # yay
    Hy = nokta(Tb, PB.YAY_KAFA); Ay = nokta(Ty, yay_delik(0.0))
    out["yay"] = (silindir(Ay, Hy, 4.0, 16), np.eye(4))
    bilgi = dict(psi=psi, yay_L=float(np.linalg.norm(Hy - Ay)))
    if p1:
        o = p1_tup_olcu()
        bilgi["p1"] = {}
        for s, nm in ((1, "L"), (-1, "R")):
            sol = p1_coz(p, s)
            bilgi["p1"][s] = sol
            for uc, kk, T0 in (("ust", sol["ust"], Tb), ("alt", sol["alt"], Ty)):
                al, be, n1, a2, pin1 = kk
                a1 = T0[:3, :3] @ np.array(_p1_notr(s)[0 if uc == "ust" else 1][0])
                pin2 = nokta(T0, _p1_ust(s) if uc == "ust" else _p1_alt(s))
                # orta: yerel X = a1, Z = n1, Y = n1 x a1 ; yerel (0,0,pin2) -> pin2
                Mo = _cerceve(pin2 - n1 * PB.KARDAN["pin2"], a1, np.cross(n1, a1), n1)
                out[f"P1{nm}_orta_{uc}"] = (BLD.yukle("P1_orta"), Mo)
                dd = sol["d"] if uc == "ust" else -sol["d"]      # tup yonu: kendi pim1'inden diger uca (d = ust -> alt)
                # tup yerel: Y = a2 (pim1 ekseni), Z = dd ; yerel (0,0,dil delik) -> pin1
                yv = a2 - dd * (a2 @ dd); yv /= np.linalg.norm(yv)
                xv = np.cross(yv, dd)
                Mt = _cerceve(pin1 - dd * PB.DIL["delik"], xv, yv, dd)
                out[f"P1{nm}_{'ic' if uc == 'ust' else 'dis'}"] = (BLD.yukle("P1_ic" if uc == "ust" else "P1_dis"), Mt)
    return out, bilgi


def _dik_taban(z):
    z = np.asarray(z, float); z /= np.linalg.norm(z)
    t = np.array([1.0, 0, 0]) if abs(z[0]) < 0.9 else np.array([0, 1.0, 0])
    x = np.cross(t, z); x /= np.linalg.norm(x)
    return x, np.cross(z, x), z


GRUP_ONEK = {"N1": "yaw", "N2": "yaw", "Y1": "yaw", "N3": "hac", "egme_mg996r": "yaw", "pim_pitch": "hac", "pim_roll": "bas"}
