"""Geometri yardimcilari: manifold3d (organik kabuk, tup) + sablon kesicileri (CadQuery -> manifold)."""
from __future__ import annotations

import math

import manifold3d as m3d
import numpy as np

import params as P
from checks import geo

m3d.set_circular_segments(28)


# ---------------------------------------------------------------- donusumler
def Rx(deg):
    a = math.radians(deg); M = np.eye(4); c, s = math.cos(a), math.sin(a)
    M[1:3, 1:3] = [[c, -s], [s, c]]; return M


def Ry(deg):
    a = math.radians(deg); M = np.eye(4); c, s = math.cos(a), math.sin(a)
    M[0, 0], M[0, 2], M[2, 0], M[2, 2] = c, s, -s, c; return M


def Rz(deg):
    a = math.radians(deg); M = np.eye(4); c, s = math.cos(a), math.sin(a)
    M[:2, :2] = [[c, -s], [s, c]]; return M


def Tr(x, y=0.0, z=0.0):
    M = np.eye(4); M[:3, 3] = (x, y, z) if np.ndim(x) == 0 else x; return M


def eksen_etrafi(nokta, R):
    """nokta etrafinda R (4x4) donusu."""
    p = np.asarray(nokta, float)
    return Tr(p) @ R @ Tr(-p)


def uygula(M: m3d.Manifold, T) -> m3d.Manifold:
    T = np.asarray(T, float)
    return M.transform(T[:3, :].tolist())


def nokta(T, p):
    T = np.asarray(T, float)
    return T[:3, :3] @ np.asarray(p, float) + T[:3, 3]


def hizala(d):
    """+Z -> d donus matrisi (3x3)."""
    d = np.asarray(d, float); d = d / np.linalg.norm(d)
    z = np.array([0, 0, 1.0])
    v = np.cross(z, d); c = float(z @ d)
    if np.linalg.norm(v) < 1e-9:
        return np.eye(3) if c > 0 else np.diag([1, -1, -1.0])
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * (1 / (1 + c))


# ---------------------------------------------------------------- ilkel cisimler
def kutu(x0, x1, y0, y1, z0, z1):
    return m3d.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def kutu_c(c, e):
    return m3d.Manifold.cube(list(e), True).translate(list(c))


def silindir(p0, p1, r, n=28, r1=None):
    p0 = np.asarray(p0, float); d = np.asarray(p1, float) - p0
    L = float(np.linalg.norm(d))
    c = m3d.Manifold.cylinder(L, r, r if r1 is None else r1, n)
    T = np.eye(4); T[:3, :3] = hizala(d); T[:3, 3] = p0
    return uygula(c, T)


def kure(c, r, n=24):
    return m3d.Manifold.sphere(r, n).translate(list(c))


def elipsoid(c, radii, n=32):
    return m3d.Manifold.sphere(1.0, n).scale(list(radii)).translate(list(c))


def birlestir(lst):
    lst = [x for x in lst if x is not None and not x.is_empty()]
    if not lst:
        return m3d.Manifold()
    return m3d.Manifold.batch_boolean(lst, m3d.OpType.Add)


def cikar(a, lst):
    lst = [x for x in lst if x is not None and not x.is_empty()]
    if not lst:
        return a
    return a - birlestir(lst)


def catmull(pts, n=8, kapali=False):
    P_ = [np.asarray(p, float) for p in pts]
    if kapali:
        P_ = [P_[-1]] + P_ + [P_[0], P_[1]]
    else:
        P_ = [2 * P_[0] - P_[1]] + P_ + [2 * P_[-1] - P_[-2]]
    out = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
        for k in range(n):
            t = k / n
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t +
                              (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P_[-2] if not kapali else P_[1])
    return out


def tup(pts, r, n=6, kapali=False, seg=16):
    """Catmull-Rom yolu boyunca r yaricapli tup (ardisik kurelerin zarfi)."""
    yol = catmull(pts, n, kapali)
    if np.ndim(r) == 0:
        rs = [r] * len(yol)
    else:
        rs = list(np.interp(np.linspace(0, 1, len(yol)), np.linspace(0, 1, len(r)), r))
    S = [m3d.Manifold.sphere(rr, seg).translate(list(p)) for p, rr in zip(yol, rs)]
    return birlestir([m3d.Manifold.batch_hull([S[i], S[i + 1]]) for i in range(len(S) - 1)])


def hex_bas(c, n, r=2.6, h=0.9):
    """Sahte civata basi: altigen prizma, merkez c, normal n yonunde h yukseklik (yarisi gomulu)."""
    n = np.asarray(n, float); n = n / np.linalg.norm(n)
    p0 = np.asarray(c, float) - n * h * 0.5
    return silindir(p0, p0 + n * h * 1.5, r, n=6)


def cq(wp, T=None):
    """CadQuery (sablon kesicisi / parca) -> manifold, istege bagli 4x4."""
    M = geo.to_manifold(wp)
    return uygula(M, T) if T is not None else M


def disk_yz(merkez, r, x0, x1, n=28):
    """X ekseni boyunca disk (YZ duzleminde), merkez (y, z)."""
    return silindir((x0, merkez[0], merkez[1]), (x1, merkez[0], merkez[1]), r, n)


def plaka_yz(pts_yz, x0, x1):
    """YZ duzleminde dis bukey olmayan cokgen -> X boyunca levha."""
    cs = m3d.CrossSection([[(float(z), float(y)) for y, z in pts_yz]], m3d.FillRule.NonZero)
    M = m3d.Manifold.extrude(cs, x1 - x0)          # (u=z, v=y, w=x) -> donustur
    T = np.array([[0, 0, 1, x0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1.0]])
    return uygula(M, T)


def plaka_xz(pts_xz, y0, y1):
    cs = m3d.CrossSection([[(float(x), float(z)) for x, z in pts_xz]], m3d.FillRule.NonZero)
    M = m3d.Manifold.extrude(cs, y1 - y0)          # (x, z, w=y)
    T = np.array([[1, 0, 0, 0], [0, 0, 1, y0], [0, 1, 0, 0], [0, 0, 0, 1.0]])
    M = uygula(M, T)
    # extrude -> (x, z', y) duzeltmesi: yukaridaki T x->x, w->y, v->z ; CrossSection v ekseni z'dir
    return M


def yuvarlak_cubuk_yz(a, b, r, x0, x1):
    """YZ'de iki daire (a, b; (y, z)) zarfi, X boyunca levha (kol / dil)."""
    return m3d.Manifold.batch_hull([disk_yz(a, r, x0, x1), disk_yz(b, r, x0, x1)])


# ---------------------------------------------------------------- kafatasi
def skull_warp(v):
    x, y, z = v[:, 0].copy(), v[:, 1].copy(), v[:, 2].copy()
    x *= 1 - 0.13 * np.maximum(0, z) * (1 - np.maximum(0, y))
    x *= 1 - 0.06 * (1 - y * y)
    m = (z > 0.45) & (y < 0.55)
    z[m] *= 1 - 0.07 * (1 - np.abs(y[m] - 0.05))
    m = (z < -0.4) & (y < 0.25)
    z[m] *= 1 + 0.06 * (1 - np.abs(y[m] + 0.2))
    tf = np.exp(-(((y + 0.1) / 0.28) ** 2) - (((z - 0.25) / 0.32) ** 2))
    x *= 1 - 0.09 * tf
    return np.stack([x, y, z], 1)


_SKULL = {}


def kafatasi(ofset=0.0, nt=60, nf=120):
    """Kapali kafatasi yuzeyi (konsept skullWarp, CR yaricaplari), ofset > 0 -> ice dogru."""
    key = (round(ofset, 3), nt, nf)
    if key in _SKULL:
        return _SKULL[key]
    import trimesh
    th = np.linspace(0, math.pi, nt + 1)[1:-1]
    ph = np.linspace(0, 2 * math.pi, nf, endpoint=False)
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    u = np.stack([-np.cos(PH) * np.sin(TH), np.cos(TH), np.sin(PH) * np.sin(TH)], -1).reshape(-1, 3)
    u = np.vstack([u, [[0, 1, 0], [0, -1, 0]]])
    w = skull_warp(u) * np.array(P.SKULL_R) + np.array(P.SKULL_C)
    F = []
    for i in range(nt - 2):
        for j in range(nf):
            a, b = i * nf + j, i * nf + (j + 1) % nf
            c, d = a + nf, b + nf
            F += [[a, c, b], [b, c, d]]
    top, bot = len(w) - 2, len(w) - 1
    last = (nt - 2) * nf
    for j in range(nf):
        F.append([top, j, (j + 1) % nf])
        F.append([bot, last + (j + 1) % nf, last + j])
    tm = trimesh.Trimesh(w, np.array(F), process=True)
    if tm.volume < 0:
        tm.invert()
    if ofset:
        tm = trimesh.Trimesh(tm.vertices - tm.vertex_normals * ofset, tm.faces, process=False)
    M = geo.to_manifold(tm)
    _SKULL[key] = M
    return M


def skull_pt(theta, phi, out=1.0):
    u = np.array([[-math.cos(phi) * math.sin(theta), math.cos(theta), math.sin(phi) * math.sin(theta)]])
    w = skull_warp(u)[0]
    return np.array(P.SKULL_C) + w * np.array(P.SKULL_R) * out


def skull_yuzey_noktasi(yon):
    """Merkezden (SKULL_C) yon dogrultusundaki dis yuzey noktasi + normal (yaklasik, isin)."""
    M = kafatasi(0.0)
    c = np.array(P.SKULL_C); d = np.asarray(yon, float); d /= np.linalg.norm(d)
    lo, hi = 0.0, 200.0
    for _ in range(30):
        mid = (lo + hi) / 2
        p = c + d * mid
        inside = kure(p, 0.01, 4).__sub__(M).is_empty()
        lo, hi = (mid, hi) if inside else (lo, mid)
    return c + d * lo


def mesh_bilgi(M):
    mm = M.to_mesh()
    return np.asarray(mm.vert_properties)[:, :3], np.asarray(mm.tri_verts)


# ---------------------------------------------------------------- estetik tur: kemik plakalari (hull seritleri)
def _hull_kureler(pts, r, seg):
    return m3d.Manifold.batch_hull([m3d.Manifold.sphere(r, seg).translate(list(map(float, p))) for p in pts])


def serit(satirlar, t, seg=10):
    """Kemik plakasi: satirlar = [[p00, p01, ...], [p10, p11, ...], ...] ayni sayida nokta (u yonu) iceren
    egriler (v yonu satirlar). Her hucre (2x2 nokta) icin r=t/2 kurelerin zarfi -> t kalinlikli egri plaka."""
    S = [np.asarray(s, float) for s in satirlar]
    g = []
    for j in range(len(S) - 1):
        for i in range(len(S[j]) - 1):
            g.append(_hull_kureler([S[j][i], S[j][i + 1], S[j + 1][i], S[j + 1][i + 1]], t / 2, seg))
    return birlestir(g)


def yassi_tup(pts, h, t, yon=(0, 1, 0), n=4, seg=10):
    """Yassi kemik kesiti (stadyum h x t): Catmull-Rom yolu boyunca, kesit uzun ekseni 'yon' (tek vektor ya da
    nokta basina liste). h, t sabit ya da nokta listesi (uclara incelme)."""
    yol = catmull(pts, n)
    N = len(yol)
    def _seri(v):
        if np.ndim(v) == 0:
            return [float(v)] * N
        return list(np.interp(np.linspace(0, 1, N), np.linspace(0, 1, len(v)), v))
    hs, ts = _seri(h), _seri(t)
    if np.ndim(yon) == 1:
        us = [np.asarray(yon, float)] * N
    else:
        Y = np.asarray(yon, float)
        us = [np.array([np.interp(k, np.linspace(0, N - 1, len(Y)), Y[:, d]) for d in range(3)]) for k in range(N)]
    us = [u / np.linalg.norm(u) for u in us]
    seg_pts = []
    for p, hh, tt, u in zip(yol, hs, ts, us):
        a = max(hh - tt, 0.0) / 2
        seg_pts.append(([p + u * a, p - u * a], tt / 2))
    g = []
    for k in range(N - 1):
        (pa, ra), (pb, rb) = seg_pts[k], seg_pts[k + 1]
        g.append(m3d.Manifold.batch_hull([m3d.Manifold.sphere(ra, seg).translate(list(q)) for q in pa] +
                                         [m3d.Manifold.sphere(rb, seg).translate(list(q)) for q in pb]))
    return birlestir(g)


# ---------------------------------------------------------------- estetik tur 2: tek tek insan disleri
# dis tipi (orta hattan 0..6): 0-1 kesici (yassi, keski uc), 2 kopek (sivri), 3-4 kucuk azi (iki tepecik), 5-6 azi (kare, dort tepecik)
DIS_TIP = ("kesici", "kesici", "kopek", "kucuk_azi", "kucuk_azi", "azi", "azi")


def dis(tip, w, h, d, uc=-1):
    """Tek dis, yerel cerceve: x genislik (kavis teget), y boy (uc yonu 'uc' = -1 asagi / +1 yukari), z derinlik (radyal).
    Butun govde [-w/2, w/2] x [-h/2, h/2] x [-d/2, d/2] kutusunun ICINDE kalir (eski kutu disin zarfi)."""
    r = 0.55
    kx, kz = w / 2 - r, d / 2 - r
    ky = -uc * (h / 2 - r)                       # kok (dis eti) tarafi
    ty = uc * (h / 2 - r)                        # uc tarafi
    kok = [(sx * kx, ky, sz * kz) for sx in (-1, 1) for sz in (-1, 1)]
    if tip == "kesici":                          # yassi kurek: uc keski, kalinlik uca dogru incelir
        orta = [(sx * kx, ky + uc * (h * 0.45), sz * kz * 0.8) for sx in (-1, 1) for sz in (-1, 1)]
        uc_ = [(sx * kx * 0.92, ty, sz * min(kz, 0.35)) for sx in (-1, 1) for sz in (-1, 1)]
        pts = kok + orta + uc_
    elif tip == "kopek":                         # sivri tek tepe, govde yuvarlak
        orta = [(sx * kx * 0.9, ky + uc * (h * 0.45), sz * kz * 0.9) for sx in (-1, 1) for sz in (-1, 1)]
        pts = kok + orta + [(0.0, ty, 0.0)]
        r = 0.5
    elif tip == "kucuk_azi":                     # iki tepecik (yanak / dil)
        orta = [(sx * kx, ky + uc * (h * 0.55), sz * kz) for sx in (-1, 1) for sz in (-1, 1)]
        pts = kok + orta + [(sx * kx * 0.4, ty, sz * kz * 0.55) for sx in (-1, 1) for sz in (-1, 1)]
    else:                                        # azi: kare, dort tepecik
        orta = [(sx * kx, ky + uc * (h * 0.6), sz * kz) for sx in (-1, 1) for sz in (-1, 1)]
        pts = kok + orta + [(sx * kx * 0.6, ty, sz * kz * 0.6) for sx in (-1, 1) for sz in (-1, 1)]
    return m3d.Manifold.batch_hull([m3d.Manifold.sphere(r, 10).translate([float(a), float(b), float(c)]) for a, b, c in pts])


def dis_olcu(k, n=14):
    """k. dis (kavis boyunca 0..n-1) -> (tip, genislik, boy_kisalt, derinlik). Eski kutularin (on 6.2x4.5 / yan 8x7.5)
    icinde kalan olculer; aralarda >= 0.6 mm bosluk (aci adimi 2.3/13 rad, R 36..38.5 -> ~6.8 mm)."""
    i = min(k, n - 1 - k)                        # 0 = en arka azi
    j = (n // 2 - 1) - i                         # 0 = orta kesici
    tip = DIS_TIP[j]
    w, kis, d = {"kesici": (5.6 if j == 0 else 5.0, 1.2, 3.4), "kopek": (5.4, 0.0, 4.2),
                 "kucuk_azi": (6.0, 1.4, 5.4), "azi": (6.4, 1.2, 6.4)}[tip]
    return tip, w, kis, d
