"""Sabit govde: G1 gogus merkezi, G2L/G2R kaburga+koprucuk+kurek+omuz, G4L/G4R kaide (dunya = notr bas cercevesi).
Konsept dunya (cm) -> mm: p*10 - (0, 130, -5). Lazy susan / yaw servo icin YER + arayuz (mekanik Y1/N1 CP3b-2)."""
from __future__ import annotations

import math

import manifold3d as m3d
import numpy as np

import params as P
from lib import Tr, Rz, Ry, uygula, kutu, kutu_c, silindir, kure, elipsoid, birlestir, cikar, tup, hex_bas, cq, plaka_xz, serit, yassi_tup
from sablonlar.baglanti import somun_tuzagi
from sablonlar.m2 import m2_somun_tuzagi
from bas import Z2X, Z2mX, Z2Y, Z2mY, Z2Z, Z2mZ


def K(x, y, z):
    """konsept dunya cm -> mm (bas pivotu orijin)"""
    return (x * 10.0, y * 10.0 - 130.0, z * 10.0 + 5.0)


Y_KAIDE = P.KAIDE["y"][1]          # -240
G1_ALT = Y_KAIDE
SPINE = dict(x=10.0, z=(-46.0, -34.0))
G2_VIDA = [("omurga", (0.0, -154.2, -40.0)), ("manubrium", (0.0, -150.0, 51.0)), ("sternum", (0.0, -205.0, 53.0))]


def _yaw_servo_T():
    """MG996R mil-ucu -> dunya: mil +Y (eksen x0 z0), govde -Z'ye (yerel x -> -Z, y -> -X, z -> +Y)."""
    return np.array([[0, -1, 0, 0], [0, 0, 1, P.YAW_SERVO["mil_y"]], [-1, 0, 0, 0], [0, 0, 0, 1.0]])


def omur(c, k=1.0):
    x, y, z = c
    g = [silindir((x, y - 3.5 * k, z), (x, y + 3.5 * k, z), 11 * k, 20)]
    g.append(tup([(x, y + 1, z - 10 * k), (x, y - 4 * k, z - 22 * k)], [3.0 * k, 1.8 * k]))
    for s in (-1, 1):
        g.append(tup([(x + s * 6 * k, y, z - 6 * k), (x + s * 17 * k, y, z - 9 * k)], [2.4 * k, 1.6 * k]))
    return birlestir(g)


def G1():
    g = []
    gy0, gy1 = P.GUVERTE["y"]
    g.append(silindir((0, gy0, 0), (0, gy1, 0), P.GUVERTE["r"], 64))
    # omurga kolonu + T1..T5
    g.append(kutu(-SPINE["x"], SPINE["x"], G1_ALT, gy0 + 0.01, *SPINE["z"]))
    for i in range(5):
        g.append(omur((0, -142 - i * 20.5, -45), 1.0))
    # manubrium + sternum + on cerceve
    g.append(kutu_c((0, -156, 51), (42, 46, 12)))
    g.append(kutu_c((0, -206, 53), (26, 60, 12)))
    g.append(kutu(-13, 13, G1_ALT, -230, 47, 59))
    g.append(kutu(-24, 24, -182, -134, 41, 45.01))                                    # hoparlor tutucu plaka
    for i in range(4):
        g.append(kutu_c((0, -184 - i * 15, 59.6), (32, 2.5, 2)))
    # boyun yuvasi govertesi -> manubriuma bag
    g.append(kutu(-20, 20, gy0, gy1, 30, 51))
    # yaw servo tasiyici plakasi (kulaklar alttan oturur) + iki yan duvar
    mt = _yaw_servo_T()
    ky = P.YAW_SERVO["mil_y"] + P.MG["KULAK_Z0"]
    g.append(kutu(-24, 24, ky - 4.0, ky, -40, 18))
    for s in (-1, 1):
        g.append(kutu(min(s * 20, s * 24), max(s * 20, s * 24), ky - 4.0, gy0 + 0.01, -40, 18))
    g.append(kutu(-24, 24, ky - 4.0, gy0 + 0.01, -44, -40))
    # kart tablasi (omurga <-> sternum arasi dikey levha) + baglanti kirisleri
    kt = P.KART_TABLA
    g.append(kutu(-kt["x"], kt["x"], kt["y"][0], kt["y"][1], *kt["z"]))
    for y in (kt["y"][0] + 3, kt["y"][1] - 3):
        g.append(kutu(-4, 4, y - 3, y + 3, SPINE["z"][1] - 0.01, 47.01))
    g.append(kutu(-4, 4, kt["y"][1] - 0.01, ky - 3.99, -8, -5))
    for ad, k in P.KARTLAR.items():                                                     # kart ayaklari
        w, h, t = k["boy"]
        z0 = kt["z"][1] if k["yuz"] > 0 else kt["z"][0]
        for sx in (-1, 1):
            for sy in (-1, 1):
                px, py = k["c"][0] + sx * (w / 2 - 3.5), k["c"][1] + sy * (h / 2 - 3.5)
                g.append(silindir((px, py, z0), (px, py, z0 + k["yuz"] * k["ayak"]), 2.8, 16))
    # alt flans (kaideye 4x M3, I2)
    g.append(kutu(-40, 40, G1_ALT, G1_ALT + 4, -48, 62))
    G = birlestir(g)
    c = []
    # servo penceresi (deck + tasiyici) + kulak delikleri M4
    xc = (P.MG["L"] - 2 * P.MG["N"]) / 2
    pp = P.MG_CEP_PAY
    c.append(uygula(kutu(-P.MG["N"] - 0.5, P.MG["L"] - P.MG["N"] + 0.5, -P.MG["W"] / 2 - 0.5, P.MG["W"] / 2 + 0.5, -45, 30), mt))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = mt[:3, :3] @ np.array([xc + sx * P.MG["KULAK_DX"], sy * P.MG["KULAK_DY"], 0]) + mt[:3, 3]
            c.append(cq(somun_tuzagi("M4", vida_deligi=P.M4), Tr(p[0], ky - 4.0 - 0.01, p[2]) @ Z2Y))
    # lazy susan vida delikleri: oval +-3 (KAGIT 10), somun alttan
    for k in range(4):
        a = math.radians(45 + 90 * k)
        for d in np.linspace(-P.LS["oval"], P.LS["oval"], 7):
            aa = a + d / P.LS["delik_r"]
            c.append(silindir((P.LS["delik_r"] * math.cos(aa), gy0 - 1, P.LS["delik_r"] * math.sin(aa)),
                              (P.LS["delik_r"] * math.cos(aa), gy1 + 1, P.LS["delik_r"] * math.sin(aa)), P.M3 / 2, 12))
    # kablo gecisi (8 iletken, servis halkasi) ve servo kablosu
    c.append(silindir((-18, gy0 - 1, 10), (-18, gy1 + 1, 10), 6.0))
    # hoparlor izgarasi (manubrium) + govde boslugu
    hp = P.HOPARLOR
    for dx in np.arange(-15, 15.1, 3.4):
        for dy in np.arange(-15, 15.1, 3.4):
            if dx * dx + dy * dy <= 15 ** 2:
                c.append(silindir((hp["c"][0] + dx, hp["c"][1] + dy, 40), (hp["c"][0] + dx, hp["c"][1] + dy, 60), 1.1, 8))
    c.append(silindir((0, hp["c"][1], 40), (0, hp["c"][1], 45.6), hp["d"] / 2 + 0.4, 48))
    # G2 vidalari (X ekseni, somun G1 icinde)
    for ad, (x, y, z) in G2_VIDA:
        xi = {"omurga": SPINE["x"], "manubrium": 21.0, "sternum": 13.0}[ad]
        for s in (-1, 1):
            c.append(silindir((-xi - 1, y, z), (xi + 1, y, z), P.M3 / 2, 16))
            c.append(cq(somun_tuzagi("M3", kanal=8.0, kanal_yonu_deg=90.0), Tr(s * (xi - 3.0), y, z) @ (Z2X if s > 0 else Z2mX)))
    # kart ayak delikleri M3 (kendinden kilavuz 2.6)
    kt = P.KART_TABLA
    for ad, k in P.KARTLAR.items():
        w, h, t = k["boy"]
        for sx in (-1, 1):
            for sy in (-1, 1):
                px, py = k["c"][0] + sx * (w / 2 - 3.5), k["c"][1] + sy * (h / 2 - 3.5)
                c.append(silindir((px, py, kt["z"][0] - 8), (px, py, kt["z"][1] + 8), 1.3, 12))
    # kaide vidalari: flansta somun cebi (ustten)
    for x, z in G1_KAIDE_VIDA:
        c.append(cq(somun_tuzagi("M3", vida_deligi=P.M3), Tr(x, G1_ALT + 4.01, z) @ Z2mY))
    # hafifletme (omurga kolonu)
    for i in range(4):
        c.append(kutu(-11, 11, -150 - i * 22, -138 - i * 22, -44, -36))
    return cikar(G, c)


G1_KAIDE_VIDA = [(-32, -40), (32, -40), (-32, 54), (32, 54)]


# kaburgalar: (bas y, yan x, yan y, on uc (x, y)) - bas omurlar arasi bosluklarda, on uclar manubrium / sternum tablarina
KABURGA = [(-154.0, 78.0, -166.0, (24.5, -155.0)), (-173.0, 108.0, -190.0, (15.6, -192.0)), (-193.5, 128.0, -213.0, (15.6, -210.0))]


def _G2(s):
    g = []
    def m(p):
        return (s * p[0], p[1], p[2])
    def mm(ps):
        return [m(p) for p in ps]
    # kaburgalar: yassi kemik kesiti (8 x 4 -> uclara 5 x 3), arka acidan one; on ucta kikirdak (ince)
    lat = []
    for hy, rx, ly, (fx, fy) in KABURGA:
        yol = [(16.0, hy, -40.0), (rx * 0.45, hy - 2.0, -50.0), (rx * 0.85, hy - 6.0, -32.0), (rx, ly, 5.0),
               (rx * 0.86, ly - 3.0, 34.0), (rx * 0.5, fy - 1.0, 49.0)]
        g.append(yassi_tup(mm(yol), [6.0, 8.0, 8.0, 8.0, 7.5, 6.0], [3.2, 4.0, 4.0, 4.0, 3.8, 3.2], n=6))
        g.append(yassi_tup(mm([(rx * 0.5, fy - 1.0, 49.0), ((rx * 0.5 + fx) / 2, fy - 0.5, 52.0), (fx, fy, 52.5)]),
                           [5.0, 4.6, 4.6], [3.0, 3.0, 3.0], n=4))
        g.append(kure(m((rx * 0.5, fy - 1.0, 49.0)), 3.4, 14))                                   # kosto-kondral eklem
        lat.append((rx, ly, 5.0))
    # yan dikme (yassi): kaburga yan noktalarini birlestirir, ustte akromiona
    g.append(yassi_tup(mm(lat), 6.0, 3.5, yon=(1, 0, 0), n=4))
    g.append(yassi_tup(mm([lat[0], (100.0, -156.0, 0.0), (136.0, -150.0, -2.0)]), 6.0, 3.5, yon=(0, 0, 1), n=4))
    # koprucuk: hafif S, yassilasan kesit (manubrium tabindan akromiona)
    kop = [(24.5, -148.0, 50.0), (45.0, -144.0, 48.0), (75.0, -142.0, 35.0), (105.0, -143.5, 16.0), (132.0, -147.0, 4.0), (150.0, -149.0, -2.0)]
    g.append(yassi_tup(mm(kop), [7.0, 7.0, 7.0, 7.5, 8.5, 9.0], [5.5, 5.2, 4.8, 4.2, 3.8, 3.6], n=6))
    # kurek kemigi: ucgen plaka + spina -> akromion (yatay yassi plaka)
    pts = [(-26, 18), (32, 22), (-16, -65)]
    sc = m3d.Manifold.extrude(m3d.CrossSection([[(p[0], p[1]) for p in pts]]), 4.0)
    sc = uygula(sc, Tr(*m((76, -166, -56))) @ Ry(-s * math.degrees(0.4)) @ np.diag([s, 1, 1, 1.0]))
    g.append(sc)
    spina = [(55.0, -150.0, -60.0), (95.0, -148.0, -50.0), (130.0, -146.5, -30.0), (150.0, -146.5, -14.0), (157.0, -148.0, -1.0)]
    g.append(yassi_tup(mm(spina), [6.0, 8.0, 10.0, 15.0, 14.0], [3.5, 3.5, 4.0, 4.0, 4.0],
                       yon=[(0, 1, 0), (0, 1, 0), (0, 0.6, 1), (0, 0, 1), (0, 0, 1)], n=5))
    # humerus basi (acik kabuk, ic tarafta pencere) + boyun halkasi + kesik govde (kol kokii)
    hc = m((160.0, -167.5, -6.0))
    dis = birlestir([kure(hc, 19.0, 40), silindir(m((163.0, -182.0, -6.0)), m((170.0, -218.0, -6.0)), 10.0, 28, r1=8.5),
                     silindir(m((169.0, -212.0, -6.0)), m((169.6, -215.0, -6.0)), 10.2, 28)])
    ic = birlestir([kure(hc, 16.6, 40), silindir(m((163.0, -175.0, -6.0)), m((170.4, -220.0, -6.0)), 7.6, 28, r1=6.1),
                    kutu_c(m((143.0, -170.5, -6.0)), (14, 24, 24))])
    g.append(dis - ic)
    g.append(tup(mm([(152.0, -184.0, -16.0), (162.0, -188.0, -6.0), (152.0, -184.0, 6.0)]), 2.2, seg=12))
    g.append(kure(m((174.0, -158.5, 4.0)), 6.5, 20))                                           # buyuk yumru
    for k in range(4):
        a = math.radians(45 + 90 * k)
        g.append(hex_bas(m((169.3 + 9.8 * math.cos(a) * 0 + 9.6 * math.cos(a), -213.5, -6.0 + 9.6 * math.sin(a))), (0, -1, 0), r=1.4, h=1.0))
    # trapez plakasi (boyun tabani -> akromion) + kablo demeti: guverte/lazy susan (R 50) disinda
    g.append(serit([mm([(56.0, -141.0, -30.0), (95.0, -144.0, -32.0), (138.0, -148.5, -24.0)]),
                    mm([(56.0, -140.0, -6.0), (95.0, -143.0, -8.0), (138.0, -148.0, -6.0)])], 3.0))
    for k in range(3):
        g.append(tup([m((55.0, -136.5, -10 + k * 8)), m((80.0, -139.0, -12 + k * 8)), m((112.0, -146.0, -12 + k * 8))], 2.0, seg=10))
    g.append(yassi_tup(mm([(112.0, -146.0, -16.0), (112.0, -146.0, 0.0), (112.0, -145.0, 14.0)]), 5.0, 3.0, yon=(1, 0, 0), n=3))   # demet kelepcesi
    # G1 vida tablari (X yuzeyli)
    for ad, (x, y, z) in G2_VIDA:
        xi = {"omurga": SPINE["x"], "manubrium": 21.0, "sternum": 13.0}[ad] + 0.4
        dy = 4.0 if ad == "omurga" else 6.0
        z0, z1 = max(z - 6, 45.4) if ad == "manubrium" else z - 6, min(z + 6, 58.2) if ad == "sternum" else z + 6   # hoparlor plakasi / G1 sirtlari
        g.append(kutu(min(s * xi, s * (xi + 5)), max(s * xi, s * (xi + 5)), y - dy, y + dy, z0, z1))
    G = birlestir(g)
    c = []
    for ad, (x, y, z) in G2_VIDA:
        c.append(silindir((s * 5, y, z), (s * 40, y, z), P.M3 / 2, 16))
    return cikar(G, c)


def G2L():
    return _G2(1)


def G2R():
    return _G2(-1)


def _elips_bolge(a, b, y0, y1, zc):
    return m3d.Manifold.cylinder(y1 - y0, 1.0, 1.0, 96).scale([a, b, 1]).rotate([-90, 0, 0]).translate([0, y0, zc])


def _G4(s):
    k = P.KAIDE
    y0, y1 = k["y"]
    dis = _elips_bolge(k["a"], k["b"], y0, y1, k["zc"])
    ic = _elips_bolge(k["a"] - k["duvar"], k["b"] - k["duvar"], y0 - 1, y1 - k["ust"], k["zc"])
    G = dis - ic
    yari = kutu(0, 300, -400, 0, -300, 300) if s > 0 else kutu(-300, 0, -400, 0, -300, 300)
    g = [G ^ yari]
    # ic kaburgalar
    for z in (-50, 0, 50):
        g.append(_elips_bolge(k["a"] - 1, k["b"] - 1, y0, y1 - 0.5, k["zc"]) ^ kutu(-300, 300, y0, y1, z - 1.2, z + 1.2) ^ yari)
    for x in (60, 120):
        g.append(_elips_bolge(k["a"] - 1, k["b"] - 1, y0, y1 - 0.5, k["zc"]) ^ kutu(s * x - 1.2, s * x + 1.2, y0, y1, -300, 300))
    # bindirme dili + boss bolgesi (orta |x| < 12.4, dil tabaninin 0.4 alti) kaburgalardan bosaltilir (G4L x G4R)
    g = [gg - kutu(-12.4, 12.4, y1 - k["ust"] - 3.4, y1 - k["ust"] + 0.01, -300, 300) if i > 0 else gg for i, gg in enumerate(g)]
    # bindirme dili (yarilar arasi, I1): s>0 dil z<0 bolgede, s<0 dil z>0 bolgede; karsi yarida somun bossu
    dz = (-80, -10) if s > 0 else (10, 80)
    g.append(kutu(min(-s * 12, 0), max(-s * 12, 0), y1 - k["ust"] - 3, y1 - k["ust"], *dz))
    g.append(kutu(min(s * 6, 0), max(s * 6, 0), y1 - k["ust"] - 3, y1 - k["ust"] + 0.01, *dz))   # dil koku (kendi ust plakasina bagli)
    oz = (10, 80) if s > 0 else (-80, -10)
    # dilin ALTINDA tek boss blogu (iki vida), kendi yarisinin z +-50 kaburgasina bagli
    g.append(kutu(min(s * 0.4, s * 12), max(s * 0.4, s * 12), y1 - k["ust"] - 7.4, y1 - k["ust"] - 3.4, oz[0] + 9, oz[1] - 9))
    # G1 vida bossu
    for x, z in G1_KAIDE_VIDA:
        if np.sign(x) == s:
            g.append(silindir((x, y0 + 2, z), (x, y1 - 0.5, z), 4.5, 20))
    G = birlestir(g)
    c = []
    for x, z in G1_KAIDE_VIDA:
        if np.sign(x) == s:
            c.append(silindir((x, y0 - 1, z), (x, y1 + 1, z), P.M3 / 2, 16))
            c.append(silindir((x, y0 - 1, z), (x, y1 - 6, z), 3.2, 16))       # kafa havsasi (alttan)
    for z in (dz[0] + 15, dz[1] - 15):
        c.append(silindir((-s * 6, y0 - 1, z), (-s * 6, y1 + 1, z), P.M3 / 2, 16))
    for z in (oz[0] + 15, oz[1] - 15):
        c.append(silindir((s * 6, y0 - 1, z), (s * 6, y1 + 1, z), P.M3 / 2, 16))
        c.append(cq(somun_tuzagi("M3", vida_deligi=None), Tr(s * 6, y1 - k["ust"] - 7.41, z) @ Z2Y))
    if s < 0:     # DC jak + adaptor kablo cikisi (arka)
        c.append(silindir((-40, -247, k["zc"] - 95), (-40, -247, k["zc"] - 80), 4.0, 20))
        c.append(kutu(-70, -55, y0 - 1, y0 + 6, k["zc"] - 95, k["zc"] - 75))
    # on band yazi yerine oyma cizgiler (P R O J E C T  B U S T bandi gorseli)
    for i in range(9):
        a = math.radians(-36 + i * 9) * s
        zx = (k["a"] * math.sin(a), k["zc"] + k["b"] * math.cos(a))
        if np.sign(zx[0]) == s or abs(zx[0]) < 1e-6:
            c.append(uygula(kutu_c((0, 0, 0), (8, 1.2, 2.0)), Tr(zx[0], -247, zx[1]) @ Ry(math.degrees(a))))
    return cikar(G, c)


def G4L():
    return _G4(1)


def G4R():
    return _G4(-1)
