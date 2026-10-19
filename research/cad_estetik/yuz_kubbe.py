"""B2 yuz onu + B3L/B3R kubbe yarilari (bas cercevesi, notr). Konsept v6 formu (skullWarp, goz cukuru, kas kemeri...)."""
from __future__ import annotations

import math

import manifold3d as m3d
import numpy as np

import params as P
from lib import (Tr, Ry, uygula, kutu, kutu_c, silindir, kure, elipsoid, birlestir, cikar, tup, hex_bas, cq,
                 plaka_xz, kafatasi, skull_pt, serit, yassi_tup, catmull, dis as dis_tek, dis_olcu)
from sablonlar.baglanti import somun_tuzagi
from sablonlar.m2 import m2_somun_tuzagi
import zarf_b2
from lib import kafatasi as _kafatasi0


def _gerdir_np(v):
    """ESTETIK kas_kemeri: kubbe onunu one gerer (alin kas bandina basamaksiz iner). z > 4: z' = 4 + (z-4) k(y)."""
    E = P.EST_KAS["gerdir"]
    v = np.array(v, float)
    t = np.clip((E["y_tepe"] - v[:, 1]) / (E["y_tepe"] - E["y_alt"]), 0.0, 1.0) ** E["p"]
    k = 1.0 + E["A"] * t
    on = v[:, 2] > 4.0
    v[on, 2] = 4.0 + (v[on, 2] - 4.0) * k[on]
    return v


def _gerdir(M):
    return M.warp_batch(lambda v: _gerdir_np(v))


def kafatasi(ofset=0.0):
    if not P.ESTETIK.get("kas_kemeri"):
        return _kafatasi0(ofset)
    key = ("g", round(ofset, 3))
    if key not in _CACHE:
        _CACHE[key] = _gerdir(_kafatasi0(ofset))
    return _CACHE[key]
from bas import Z2Y, Z2X, Z2mX, Z2Z, Z2mZ


# ===================================================================================================== B3 kubbe
def _bolge():
    """Kubbe kabugunun var oldugu bolge (alt kenar kurali, params)."""
    if P.ESTETIK.get("kubbe_kenar"):
        return _bolge_egri()
    return birlestir([kutu(-200, 200, P.KUBBE_Y_ON, 300, -200, 300),
                      kutu(-200, 200, P.KUBBE_Y_ALT, 300, -200, P.KUBBE_Z_ON),
                      kutu(-200, 200, P.KUBBE_ARKA_Y, 300, -200, P.KUBBE_ARKA_Z)])


# ---- ESTETIK kubbe_kenar: alt kenar basamaklari (on z 30, arka z -58) kosinus gecisli egri y_kenar(z)
def _y_kenar(z):
    y = _y_kenar0(z)
    return y


def _y_kenar0(z):
    E = P.EST_KENAR
    a0, a1 = E["on"]
    b0, b1 = E["arka"]
    if z >= a1:
        return P.KUBBE_Y_ON
    if z >= a0:
        t = (z - a0) / (a1 - a0)
        return P.KUBBE_Y_ALT + (P.KUBBE_Y_ON - P.KUBBE_Y_ALT) * (1 - math.cos(math.pi * t)) / 2
    if z >= b1:
        return P.KUBBE_Y_ALT
    if z >= b0:
        t = (z - b0) / (b1 - b0)
        return P.KUBBE_ARKA_Y + (P.KUBBE_Y_ALT - P.KUBBE_ARKA_Y) * (1 - math.cos(math.pi * t)) / 2
    return P.KUBBE_ARKA_Y


def _bolge_egri():
    """y >= y_kenar(z) bolgesi: (z, y) profil -> X boyunca ekstruzyon (devirli eksen permutasyonu, det +1)."""
    zs = np.concatenate([[-300.0], np.arange(-120.0, 120.01, 1.0), [300.0]])
    pts = [(float(_y_kenar(z)), float(z)) for z in zs] + [(400.0, 300.0), (400.0, -300.0)]
    cs = m3d.CrossSection([pts[::-1]])
    if cs.area() <= 0 or cs.is_empty():
        cs = m3d.CrossSection([pts])
    M = m3d.Manifold.extrude(cs, 400.0).translate([0, 0, -200.0])        # (a=y, b=z, h=x)
    return M.transform(np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]], float))


def _kenar_bandi(K):
    E = P.EST_KENAR
    ust = K.translate([0, E["bant"], 0]) ^ K.translate([0, 0, E["bant_z"]]) ^ K.translate([0, 0, -E["bant_z"]])
    return K - ust


def _detaylar():
    """Kabuga eklenen gorsel yogunluk (gram az): koronal/ense sirti, sakak cizgisi, sahte civatalar."""
    g = []
    cor = [skull_pt(abs(t) + 0.001, math.pi - 0.32 if t > 0 else 0.32, 1.0) for t in np.linspace(-1.2, 1.2, 25)]
    g.append(tup(cor, 1.3, n=3))
    for i in range(2, len(cor) - 2, 3):
        p = cor[i]
        n = p - np.array(P.SKULL_C); n /= np.linalg.norm(n)
        for d in (-4.5, 4.5):
            g.append(hex_bas(p + (0, 0, d) - n * 0.3, n, r=2.2, h=1.6))
    for s in (-1, 1):
        pts = []
        for t in np.linspace(0, 1, 18):
            ph = math.pi / 2 + s * (0.5 + t * 1.75)
            th = 1.30 - 0.22 * math.sin(t * math.pi) + 0.08 * t
            pts.append(skull_pt(th, ph, 0.995))
        g.append(tup(pts, 1.8, n=3))
    pts = [skull_pt(1.83, 3 * math.pi / 2 + (k / 14 - 0.5) * 1.6, 0.995) for k in range(15)]
    g.append(tup(pts, 2.2, n=3))
    return birlestir(g)


def _kubbe_ham():
    OUT, IN1, IN6 = kafatasi(0.0), kafatasi(P.KABUK), kafatasi(P.KABUK + P.KABURGA_H)
    K = _bolge()
    kabuk = (OUT - IN1) ^ K
    slab = []
    for y in P.KUBBE_KABURGA_Y:
        slab.append(kutu(-200, 200, y - P.KABURGA_T / 2, y + P.KABURGA_T / 2, -200, 200))
    for z in P.KUBBE_KABURGA_Z:
        slab.append(kutu(-200, 200, -200, 200, z - P.KABURGA_T / 2, z + P.KABURGA_T / 2))
    # alt kenar cercevesi (kenar kaburgasi)
    if P.ESTETIK.get("kubbe_kenar"):
        kenar = (IN1 - IN6) ^ _kenar_bandi(K)

    else:
        kenar = (IN1 - IN6) ^ K ^ (birlestir([kutu(-200, 200, -200, P.KUBBE_Y_ON + 4, P.KUBBE_Z_ON, 300),
                                          kutu(-200, 200, -200, P.KUBBE_Y_ALT + 4, P.KUBBE_ARKA_Z + 3, P.KUBBE_Z_ON + 1.6),
                                          kutu(-200, 200, -200, P.KUBBE_ARKA_Y + 4, -300, P.KUBBE_ARKA_Z + 1.6),
                                          kutu(-200, 200, -200, 300, P.KUBBE_ARKA_Z - 1.6, P.KUBBE_ARKA_Z + 1.6)]))
    kaburga = ((IN1 - IN6) ^ K ^ birlestir(slab)) + kenar
    det = ((_gerdir(_detaylar()) if P.ESTETIK.get("kas_kemeri") else _detaylar()) - IN1) ^ K
    # sakak sogutma yariklari (kabuk ici gecer)
    yarik = []
    for s in (-1, 1):
        for k in range(4):
            p = skull_pt(1.25 + k * 0.07, math.pi / 2 + s * (1.15 + k * 0.12), 1.0)
            n = p - np.array(P.SKULL_C); n /= np.linalg.norm(n)
            yarik.append(uygula(kutu_c((0, 0, 0), (8.0, 2.4, 22.0)), Tr(p)))
    return kabuk, kaburga, det, birlestir(yarik)


_CACHE = {}


def _kubbe_parcalari():
    if "k" not in _CACHE:
        _CACHE["k"] = _kubbe_ham()
    return _CACHE["k"]


def _sekmeler(s):
    """B1'e baglanti sekmeleri (yandan yatay M3 x2, arkadan M3 x1) - kabuk icine (IN0.6) kirpilir."""
    IN06 = kafatasi(0.6)
    g = []
    c = []
    for d in P.B3_DIREK.values():
        xi = d["x"][1] + 0.4
        x0, x1 = sorted((s * xi, s * 90))
        tab = kutu(x0, x1, P.B3_VIDA_Y - 4.0, P.KUBBE_Y_ALT + 4.0, d["z"][0], d["z"][1]) ^ IN06
        g.append(tab)
        zc = (d["z"][0] + d["z"][1]) / 2
        c.append(silindir((s * (xi - 1), P.B3_VIDA_Y, zc), (s * 90, P.B3_VIDA_Y, zc), P.M3 / 2, 16))
    b = P.B3_ARKA
    x0, x1 = sorted((s * b["x"][0], s * b["x"][1]))
    g.append(kutu(x0, x1, b["y"][0], b["y"][1] + 4, -120, b["z"][0] - 0.4) ^ IN06)
    xc = s * (b["x"][0] + b["x"][1]) / 2
    c.append(silindir((xc, b["vida_y"], b["z"][0]), (xc, b["vida_y"], -130), P.M3 / 2, 16))
    return birlestir(g), birlestir(c)


def _B3(s):
    kabuk, kaburga, det, yarik = _kubbe_parcalari()
    IN1, IN28 = kafatasi(P.KABUK), kafatasi(P.KABUK + 1.6)
    yari = kutu(0, 200, -200, 300, -200, 300) if s > 0 else kutu(-200, 0, -200, 300, -200, 300)
    g = [kabuk ^ yari, det ^ yari]
    if s > 0:
        g.append(kaburga ^ kutu(0.0, 200, -200, 300, -200, 300))
        g.append((IN1 - IN28) ^ _bolge() ^ kutu(-6.0, 0.01, -200, 300, -200, 300))      # bindirme dili (B3R altina)
    else:
        g.append(kaburga ^ kutu(-200, -6.4, -200, 300, -200, 300))
        g.append((IN28 ^ _bolge() ^ kutu(-9.4, -6.4, -200, 300, -200, 300)) - kafatasi(P.KABUK + P.KABURGA_H))
    tab, delik = _sekmeler(s)
    g.append(tab)
    if P.ESTETIK.get("kas_kemeri"):
        kk = _kas_kemeri() ^ yari
        if s < 0:
            kk = kk - ((kafatasi(P.KABUK - 0.4) - kafatasi(P.KABUK + 2.0)) ^ kutu(-6.4, 0.01, -200, 300, -200, 300))
        g.append(kk)
    if P.ESTETIK.get("sakak_pencere"):
        W = P.EST_PENCERE
        dudak = (kafatasi(P.KABUK - 0.3) - kafatasi(P.KABUK + W["dudak"])) ^ (_oval_x(W, W["kenar"]) - _oval_x(W, 0.0))
        g.append(dudak ^ yari)
    if P.ESTETIK.get("orbita_tavan"):
        tv = _orbita_tavan() ^ yari
        if s < 0:   # B3L bindirme dili (x -6..0, IN1..IN2.8) + 0.4 bosluk: tavanin kabuga gomulu ucu dile girmesin
            tv = tv - ((kafatasi(P.KABUK - 0.4) - kafatasi(P.KABUK + 2.0)) ^ kutu(-6.4, 0.01, -200, 300, -200, 300))
        g.append(tv)
    G = birlestir(g)
    # B1 arka plaka + arka dil + arka yan direk tabani (+0.4) icin kabuk kenar kaburgasinda bosluk (B1 x B3 arka dil kesisimi)
    e = P.EKS
    bos = kutu(-P.B1_ARKA_YAN[1] - e, P.B1_ARKA_YAN[1] + e, P.B1_Y[0] - e, P.B3_ARKA["y"][1] + e,
               P.B3_ARKA["z"][0] - e, P.B1_ARKA_YAN[3] + e)
    if P.ESTETIK.get("sakak_pencere"):
        delik = delik + _oval_x(P.EST_PENCERE, 0.0)
    return cikar(G, [delik, yarik, bos])


def _oval_x(W, ek):
    """Sakak penceresi: (z, y) duzleminde elips, X boyunca (yan duvarlar). ek: yari eksenlere ek."""
    pts = [(W["zc"] + (W["a"] + ek) * math.cos(t), W["yc"] + (W["b"] + ek) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 72, endpoint=False)]
    cs = m3d.CrossSection([pts])
    if cs.area() <= 0:
        cs = m3d.CrossSection([pts[::-1]])
    M = m3d.Manifold.extrude(cs, 400.0).translate([0, 0, -200.0])        # (a=z, b=y, h=x)
    M = M.transform(np.array([[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], float))
    return M - kutu(-40, 40, -300, 300, -300, 300)                       # yalniz yan duvarlar


# ---- ESTETIK orbita_tavan: goz cukuru tavani (orbita tavani = on kafatasi cukuru tabani) B3'e bagli yatay plaka.
# B5 +Y ile cikarildigi icin B2'de goz ustu malzeme olamaz (supurme kesigi = ustten acik yarik). B3 en son takilir (+-X);
# plaka B2 ust siniri (y 54.3) + 0.7 ustunde, z>40'ta baska parca y > 49 degil -> +-X kayarken temas yok.
def _kubbe_on_z(x, y):
    """Kafatasi dis yuzeyinin on (z > 0) noktasi z(x, y): kafatasi(0) agindan en yakin (x, y) komsulari (yaklasik)."""
    if "on_z" not in _CACHE:
        from lib import mesh_bilgi
        v, _ = mesh_bilgi(kafatasi(0.0))
        _CACHE["on_z"] = v[v[:, 2] > 0]
    v = _CACHE["on_z"]
    d = (v[:, 0] - x) ** 2 + (v[:, 1] - y) ** 2
    k = np.argsort(d)[:4]
    w = 1.0 / (np.sqrt(d[k]) + 0.3)
    return float(np.sum(v[k, 2] * w) / np.sum(w))


def _orbita_tavan():
    """Alin plakasi: on kenar kas ustunde (y 55.8, B2 kas satiri 49.5'in 3 mm gerisi), geriye/yukari kubbe yuzeyine egimle
    kaynar (son satir kabugun icinde). Tum noktalar y >= 55.0 (B2 ust siniri 54.3) -> B3 +-X sokme yolu B2'ye degmez."""
    E = P.EST_TAVAN
    row = dict(_YUZ)[49.5]
    xs = np.concatenate([np.linspace(-E["x"], E["x"], 29)])
    zf = [float(np.interp(abs(x), [p[0] for p in row], [p[1] for p in row])) - E["geri"] for x in xs]
    rows = []
    for y, t in zip(E["satir_y"], E["satir_t"]):
        rows.append([np.array([x, y, z0 + (_kubbe_on_z(x, y) - E["gom"] - z0) * t]) for x, z0 in zip(xs, zf)])
    return serit(rows, E["t"])


# ---- ESTETIK kas_kemeri (TUR 2): kas bandi + alin tek serit; profil (v) her x icin: tavan arkasi -> kas alti -> kas onu ->
# kas ustu -> alin satirlari -> kubbeye gomulu son satir. Tum noktalar y >= y_alt + 0.7 (B2 y <= 47 kirpilir).
def _kas_kemeri():
    E = P.EST_KAS
    xs = np.linspace(-E["x"], E["x"], 31)
    rows = {}
    for x in xs:
        ax = abs(x)
        zf = min(E["z_on"], _kubbe_on_z(x, E["y_ust"] - 2.0) + E["on_ofs"])      # kubbe egrisini izler (yanda geri doner)
        ya = E["y_alt"] + E["kemer"] * math.exp(-((ax - abs(P.GOZ[0][0])) / 12.0) ** 2) + E["t"] / 2   # orbita kemeri
        yt = E["y_ust"]
        z0, z1 = min(E["z_tavan"], zf - 12.0), zf - 7.0
        if ax <= E["pitch_x"]:            # goz pitch +-24: B5g kulagi / B5h z 60..80'de y 51.5'e cikar, z > 80'de <= 46.2
            if z1 < E["pitch_z"] + 1.0:
                ya = max(ya, E["pitch_y"])
            else:
                z0 = max(z0, E["pitch_z"]); z1 = max(z1, z0 + 1.0)
        prof = [(ya, z0), (ya, z1), (ya + 1.6, zf - 1.8), ((ya + yt) / 2, zf), (yt - 1.2, zf - 0.8)]
        prof.append((yt + 2.5, _kubbe_on_z(x, yt + 2.5) - 1.2))     # kubbeye gomulu (gerdirilmis kubbe)
        rows[x] = prof
    nv = len(rows[xs[0]])
    satir = [[np.array([x, rows[x][k][0], rows[x][k][1]]) for x in xs] for k in range(nv)]
    uc = []
    for x in (xs[0], xs[-1]):                                      # yan uclar: acik C-kesit yerine dolu kapak
        sx = 1.0 if x > 0 else -1.0
        pts = [np.array([x - sx * dx, y, z]) for y, z in rows[x] for dx in (0.0, E["t"])]
        uc.append(m3d.Manifold.hull_points([list(map(float, p)) for p in pts]))
    return serit(satir, E["t"]) + birlestir(uc)


def B3L():
    return _B3(1)


def B3R():
    return _B3(-1)


# ===================================================================================================== B2 yuz
RIM = (22.5, 20.5)
MAKS_R = 39.5            # alveol kenari yaricapi (on disler R 38.5 + 2.25: kemik disle hizali)
MAKS_T = 2.8              # maksilla plaka kalinligi (eski kova kabugu 3.0)
# maksilla ust kenari (u: 0 orta hat -> 1 elmacik): armut acikligi tabani/yani, goz cukuru tabani, elmacik
_MAKS_U = [(0.00, (0.0, -11.6, 91.0)), (0.12, (6.0, -11.8, 90.8)), (0.26, (14.6, -6.0, 90.2)), (0.40, (15.8, 6.0, 89.6)),
           (0.55, (22.0, 8.2, 87.8)), (0.70, (32.5, 7.6, 87.6)), (0.85, (42.0, 7.0, 85.5)), (1.00, (48.0, 4.5, 81.5))]
# orta satir ofseti (+ ice): kopek disi cikintisi (u 0.3) disari, kopek cukuru (u 0.6-0.8) ice
_MAKS_OFS = [(0.0, 0.0), (0.2, -0.5), (0.3, -1.3), (0.45, 0.5), (0.6, 3.5), (0.75, 4.2), (0.9, 2.0), (1.0, 0.0)]


def _hull_kureler(pts, r, seg=12):
    return m3d.Manifold.batch_hull([kure(p, r, seg) for p in pts])


def _maks_satirlar(s, n=19):
    us = np.linspace(0, 1, n)
    uk = [k for k, _ in _MAKS_U]
    L, M, U, N = [], [], [], []
    for u in us:
        a = u * 1.15
        nrm = np.array([s * math.sin(a), 0.0, math.cos(a)])
        lo = np.array([s * MAKS_R * math.sin(a), -19.5, 51.0 + MAKS_R * math.cos(a) * 1.12])
        up = np.array([np.interp(u, uk, [p[d] for _, p in _MAKS_U]) for d in range(3)]); up[0] *= s
        of = np.interp(u, [k for k, _ in _MAKS_OFS], [v for _, v in _MAKS_OFS])
        L.append(lo); U.append(up); M.append((lo + up) / 2 - nrm * of); N.append(nrm)
    return us, L, M, U, N


def _maksilla():
    g = []
    for s in (-1, 1):
        us, L, M, U, N = _maks_satirlar(s)
        C = [2 * m - (l + u) / 2 for l, m, u in zip(L, M, U)]
        rows = [[(1 - v) ** 2 * l + 2 * v * (1 - v) * c + v * v * u for l, c, u in zip(L, C, U)] for v in np.linspace(0, 1, 5)]
        g.append(serit(rows, MAKS_T))
        g.append(tup([U[k] for k in range(len(us)) if us[k] >= 0.38], 1.8, seg=12))                 # goz cukuru taban kenari
        k3 = int(np.argmin(np.abs(us - 0.3)))
        g.append(tup([L[k3] + N[k3] * 0.6, M[k3] + N[k3] * 0.4, U[k3]], [2.2, 2.0, 1.6], seg=12))   # kopek disi cikintisi
        for uu in (0.62, 0.9):
            k = int(np.argmin(np.abs(us - uu)))
            g.append(hex_bas(M[k] + N[k] * (MAKS_T / 2), N[k], r=2.0, h=1.0))
    al = [(MAKS_R * math.sin(a), -19.5, 51.0 + MAKS_R * math.cos(a) * 1.12) for a in np.linspace(-1.15, 1.15, 17)]
    g.append(tup(al, 2.0, seg=12))                                                              # alveol kenari (kalin)
    return g
        # goz cukuru kenari merkez cizgisi yari eksenleri (lid supurmesi icin konseptten buyutuldu)



# ---- orbita turu (2026-10-17): ust yuz = TEK SUREKLI kemik kabugu (alin alt kenari, glabella, burun koku, kas, elmacik,
# sakak duvari); goz cukurlari bu kabuktan OYULUR (boolean), ic duvarlari (tavan/taban/yan) kabuk olarak goze dogru
# iner. Mekanizma ile cakisan her yer zarf_b2 (supurme + montaj-sokme + P2, +0.6) ile kesilir. Eski huni/kas bandi YOK.
YUZ_T = 1.6                                    # kabuk + orbita duvari (B2 et_yapisal 1.6)
# yuz kabugu satirlari: (y, [(x, z), ...]) yarim profil, orta hattan sakaga (son 3 nokta sakak duvari, geri kivrilir)
_YUZ = [
    (53.5, [(0, 93.0), (6, 92.5), (12, 91.5), (20, 89.0), (28, 84.5), (36, 78.0), (44, 69.5), (50, 62.0), (54, 56.0), (57, 50.0), (59, 45.0), (60, 40.0)]),
    (49.5, [(0, 99.5), (6, 100.0), (12, 100.5), (20, 100.0), (28, 99.0), (36, 97.0), (44, 92.5), (50, 86.5), (55, 80.5), (58.5, 73.0), (60.5, 63.0), (61.5, 53.0)]),
    (44.0, [(0, 95.0), (6, 96.0), (12, 97.5), (20, 97.5), (28, 96.5), (36, 94.5), (44, 90.5), (50, 85.5), (54.5, 80.0), (57.0, 72.0), (58.0, 62.0), (58.5, 53.0)]),
    (30.0, [(0, 94.0), (6, 94.0), (12, 93.0), (20, 92.5), (28, 91.0), (36, 89.0), (44, 86.5), (50, 83.0), (54.5, 79.0), (56.5, 71.0), (57.0, 62.0), (57.0, 53.0)]),
    (16.0, [(0, 93.0), (6, 93.0), (12, 92.5), (20, 92.0), (28, 91.0), (36, 89.5), (44, 87.0), (50, 83.5), (55, 79.0), (59.0, 72.5), (60.5, 62.5), (61.5, 49.0)]),
    (7.0, [(0, 91.0), (6, 91.0), (12, 90.5), (20, 89.0), (28, 88.5), (36, 88.0), (44, 85.5), (50, 81.5), (55.5, 77.5), (60.5, 72.0), (63.0, 62.0), (65.0, 48.0)]),
]
ORB_C = (32.5, 28.5)                           # cukur merkezi |x|, y (goz 30: cukur hafif asagi)
ORB_F = dict(lat=20.5, med=18.5, ust=19.0, alt=19.5)   # kenar (yuvarlanma) yari eksenleri; yuz yuzeyinde +ORB_YUV
ORB_N = 48
ORB_YUV = (4.0, 2.0, 3.0, 2.0)      # (yanal, medial, ust, alt): yuz yuzeyinde cukur bu kadar genis, kenar ice yuvarlanir


def _yuz_satirlar():
    """ESTETIK sakak: son 3 nokta (sakak duvari) EST_SAKAK ile degisir. _zyuz/orbita eski tabloyu kullanir."""
    if not P.ESTETIK.get("sakak"):
        return _YUZ
    return [(y, half[:-3] + P.EST_SAKAK[y]) if y in P.EST_SAKAK else (y, half) for y, half in _YUZ]


def _zyuz(x, y):
    """Yuz kabugu on yuzu z(x, y) (satir tablosundan, |x| <= 55 on bolge)."""
    ys = [r[0] for r in _YUZ]
    zs = [np.interp(abs(x), [p[0] for p in r[1]], [p[1] for p in r[1]]) for r in _YUZ]
    return float(np.interp(y, ys[::-1], zs[::-1]))


def _yuz_kabugu():
    rows = []
    for y, half in _yuz_satirlar():
        full = [(-x, z) for x, z in reversed(half)] + [(x, z) for x, z in half[1:]]
        rows.append([np.array([x, y, z]) for x, z in full])
    return serit(rows, YUZ_T)


def _halka(s, cy, rx, ry, z_f, dz=0.0, n=2.4, k=ORB_N):
    """Superelips halka: rx/ry = (yanal, medial) / (ust, alt); z = z_f(x, y) + dz."""
    out = []
    for i in range(k):
        u = 2 * math.pi * i / k
        c, sn = math.cos(u), math.sin(u)
        ax = rx[0] if c >= 0 else rx[1]
        ay = ry[0] if sn >= 0 else ry[1]
        x = s * (ORB_C[0] + ax * math.copysign(abs(c) ** (2 / n), c))
        y = cy + ay * math.copysign(abs(sn) ** (2 / n), sn)
        out.append(np.array([x, y, z_f(x, y) + dz]))
    return out


def _loft(halkalar):
    """Ardisik halkalarin dis bukey zarflari (halkalar bukey) -> oyuk hacmi."""
    g = []
    for a, b in zip(halkalar, halkalar[1:]):
        g.append(m3d.Manifold.hull_points([list(map(float, p)) for p in a + b]))
    return birlestir(g)


def _orbita_halkalari(s, ek=0.0):
    """Oyuk kesitleri (on -> arka). ek > 0: duvar dis yuzu. Yuz yuzeyinde genis (ORB_YUV), 5 mm iceride kenar
    (yuvarlanma), 12 mm geride yeniden genisler (gercek orbita kenarin arkasinda en genis), 40 mm derinde daralir."""
    F = ORB_F
    def on(dz, b, cy=None, z=None):
        zf = _zyuz if z is None else (lambda x, y: z)
        return _halka(s, ORB_C[1] if cy is None else cy, (F["lat"] + b[0] + ek, F["med"] + b[1] + ek),
                      (F["ust"] + b[2] + ek, F["alt"] + b[3] + ek), zf, dz)
    Y = ORB_YUV
    return [on(25.0, Y), on(0.0, Y), on(-5.0, (0, 0, 0, 0)), on(-12.0, (1.5, 1.0, 1.0, 1.0)),
            on(0, (0.5, 0.5, 0.5, 0.5), 29.0, 66.0)]                 # 66'nin arkasi mekanizma bolgesi (gorunmez)


def _orbita_kemik(s):
    """(oyuk, duvar) bir goz icin. Kenar = oyugun kenari (ekli tup/halka YOK)."""
    oyuk = _loft(_orbita_halkalari(s))
    dis = _loft(_orbita_halkalari(s, YUZ_T)[1:])
    return oyuk, dis - oyuk


def _kas_dolgu(t=5.0):
    """Kas/alin kemigi dolu kutle: ust 3 satirin arkasi t mm dolu (kenar kesildiginde kalin kemik kesiti gorunur)."""
    g = []
    rows = []
    for y, half in _yuz_satirlar()[:3]:
        full = [(-x, z) for x, z in reversed(half)] + [(x, z) for x, z in half[1:]]
        rows.append([np.array([x, y, z]) for x, z in full])
    for j in range(2):
        for i in range(len(rows[j]) - 1):
            q = [rows[j][i], rows[j][i + 1], rows[j + 1][i], rows[j + 1][i + 1]]
            n = np.array([0, 0, -t]) if abs(q[0][0]) < 50 else np.array([-np.sign(q[0][0]) * t, 0, 0])
            g.append(_hull_kureler(q + [p + n for p in q], 0.8, 8))
    return birlestir(g)


def _armut(s=1.0):
    pts = [(0, 16), (7, 14), (12.5, 2), (12, -6), (11, -13), (5, -14.5), (0, -12)]
    full = [(x * s, y * s) for x, y in pts] + [(-x * s, y * s) for x, y in reversed(pts[1:-1])]
    return full[::-1]                 # CCW (manifold CrossSection: CW poligon bos alan -> eski armut kenari hic olusmuyordu)


def B2():
    g = []
    g.append(elipsoid((0, 47.5, 98.0), (9, 5.0, 3.0)))                                          # glabella (kas kutlesine gomulu)
    # orbita turu: yuz kabugu + oyulmus goz cukurlari (ayri liste: mekanizma zarfi yalniz bunlardan cikar)
    yuz, oyuk = [_yuz_kabugu()], []
    for E in P.GOZ:
        s = float(np.sign(E[0]))
        oy, duvar = _orbita_kemik(s)
        oyuk.append(oy)
        yuz.append(duvar)
    yuz.append(_kas_dolgu())
    for E in P.GOZ:
        s = float(np.sign(E[0]))
        # elmacik govdesi (zigoma): yassi kemik govdesi, ust ucu goz cukuru dis-alt kenarina, arka ucu kemere
        g.append(_hull_kureler([(s * 44, 10.0, 83.0), (s * 57, 9.5, 77.0), (s * 60, 0.0, 72.5), (s * 47, -2.0, 80.0)], 2.0))
        g.append(elipsoid((s * 52.5, 4.5, 80.0), (6.5, 5.5, 4.0), 24))                              # elmacik cikintisi
        # zigomatik kemer: yassi kesit (yuksek 9 -> 6.5), kulaga (kondil onu) uzanir
        g.append(yassi_tup([(s * 57, 7, 74), (s * 63, 8, 62), (s * 67, 9, 42), (s * 67, 9, 26)], [9.0, 8.0, 7.0, 6.5],
                           [4.4, 4.0, 3.6, 3.4]))
        for k in range(3):
            g.append(hex_bas((s * (68.3 - 0.1 * k), 9, 48 - k * 9), (s, 0, 0), r=1.8, h=1.0))
        # B1 kulaklarina tab (alttan M3 x2)
        k = P.B2_KULAK
        x0, x1 = sorted((s * k["x"][0], s * k["x"][1]))
        g.append(kutu(x0, x1, *P.B2_TAB_Y, *k["z"]))
        g.append(tup([(s * 45, 1.8, 56.5), (s * 53, -0.5, 63.5), (s * 58.5, -1.0, 71.5)], 2.6))
    # burun kemigi (nasal): ustte dar, armut ustunde genis; iki orbitanin ic duvarlari buna kaynar
    g.append(_hull_kureler([(-3.0, 45.0, 96.0), (3.0, 45.0, 96.0), (-6.5, 21.5, 92.5), (6.5, 21.5, 92.5),
                            (-3.0, 44.0, 91.0), (3.0, 44.0, 91.0), (-6.0, 22.0, 89.0), (6.0, 22.0, 89.0)], 1.5))
    # burun koprusu baglantilari: ust uc kas kemerine, alt uc armut kenarina (B2 tek govde)
    g.append(kutu(-4.0, 4.0, 19.5, 23.0, 88.0, 95.0))
    dis = m3d.CrossSection([_armut(1.0)]).offset(1.8, m3d.JoinType.Round)
    ic = m3d.CrossSection([_armut(1.0)])
    # armut kenari + burun boslugu ic perdesi (1.8): kamera cercevesinin kare kenarini ortur, merceğe yuvarlak pencere (r 6; 70 deg
    # gorus konisi mercek onunden 1.5 mm'de r 5.1) -> pencere r 8. z >= mercek ucu + 0.4 -> B2 +Y sokmede mercege degmez.
    kc = P.KAMERA
    zl = kc["c"][2] + kc["t"] + kc["lens"][1] + 0.4
    g.append(m3d.Manifold.extrude(dis - ic, 3.9).translate([0, 5, zl]))                      # armut kenari (mercegin onunde)
    perde = m3d.Manifold.extrude(ic, 1.8).translate([0, 5, zl]) - silindir((kc["c"][0], kc["c"][1], zl - 1), (kc["c"][0], kc["c"][1], zl + 3), 8.0, 32)
    g.append(perde)
    # ust cene (maksilla): dis kavsi ustunden goz cukuru tabanina / armut acikligina / elmacige kemik plakalari
    zc, yc = 51.0, -14.0
    wedge = plaka_xz([(0, 0)] + [(70 * math.sin(a), 70 * math.cos(a)) for a in np.linspace(-1.2, 1.2, 24)], -200, 200)
    g.extend(_maksilla())
    for k in range(14):
        a = -1.15 + k * 2.3 / 13
        on = abs(a) < 0.45
        R = 38.5
        h = 10.5 if on else 9.0                                                                 # eski kutu zarfi (boy)
        tip, w, kis, d = dis_olcu(k)
        g.append(uygula(dis_tek(tip, w, h - kis, d, uc=-1), Tr(R * math.sin(a), -28.0 + kis / 2, zc + R * math.cos(a) * 1.12 - 1.5) @ Ry(math.degrees(a))))
    gum = (m3d.Manifold.cylinder(7, 37.5, 37.5, 64, True).rotate([90, 0, 0]) -
           m3d.Manifold.cylinder(8, 33.5, 33.5, 64, True).rotate([90, 0, 0])).scale([1, 1, 1.12]).translate([0, -23, zc])
    g.append(gum ^ wedge.translate([0, 0, zc]))
    # kamera rezervi (OV5640, 32x32): cerceve + 4x M2 + lens deligi
    kc = P.KAMERA
    cx, cy, cz = kc["c"]
    z0 = cz + kc["t"] + 0.4
    g.append(kutu(cx - 14, cx + 14, cy - 14, 10.5, z0, z0 + 2.0) - kutu(cx - 8, cx + 8, cy - 8, cy + 8, z0 - 1, z0 + 3))
    for s in (-1, 1):                                                                           # cerceve -> maksilla baglantisi
        g.append(kutu(min(s * 13.0, s * 16.5), max(s * 13.0, s * 16.5), -10.0, 4.0, z0 + 0.4, z0 + 2.9))
    ic_armut = m3d.Manifold.extrude(m3d.CrossSection([_armut(1.0)]), 40.0).translate([0, 5, 70.0])   # burun acikligi yuzden de acik
    YUZ = cikar(birlestir(yuz), oyuk + [ic_armut, zarf_b2.yukle_yuz()])
    G = cikar(birlestir(g), oyuk) + YUZ
    gov = sorted(G.decompose(), key=lambda m: -m.volume())
    if len(gov) > 1:                                  # zarf kesiminden kopan kabuk adaciklari atilir (rapor)
        print("   B2: zarf adaciklari atildi (mm3):", [round(m.volume(), 1) for m in gov[1:]])
        G = gov[0]
    c = []
    for sx in (-1, 1):
        for sy in (-1,):
            c.append(silindir((cx + sx * kc["delik"] / 2, cy + sy * kc["delik"] / 2, z0 - 1), (cx + sx * kc["delik"] / 2, cy + sy * kc["delik"] / 2, z0 + 3), P.M2 / 2, 12))
    if P.ESTETIK.get("kas_kemeri"):          # kas B3'te: B2 ust siniri y 47 (B3 kas alti y >= 49.3)
        G = G ^ kutu(-200, 200, -200, P.EST_KAS["b2_y"], -200, 300)
        gov = sorted(G.decompose(), key=lambda m: -m.volume())
        if len(gov) > 1:
            print("   B2 (kas_kemeri kirpma) adaciklar atildi (mm3):", [round(m.volume(), 1) for m in gov[1:]])
            G = gov[0]
    k = P.B2_KULAK
    for s in (-1, 1):
        for dx in k["delik_x"]:
            c.append(silindir((s * dx, P.B2_TAB_Y[0] - 1, k["delik_z"]), (s * dx, P.B2_TAB_Y[1] + 1, k["delik_z"]), P.M3 / 2, 16))
    return cikar(G, c)
