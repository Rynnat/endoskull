"""Project Bust CP3b-2 kontrolleri (boyun / egme / yay / P1). check.py main() bunu cagirir; tek basina da calisir:

  PYTHONUTF8=1 python -B check_boyun.py [--hizli]      -> out/check_report_boyun.txt
Kontroller: agent-flow/checks (strok, diferansiyel_tork, poz_kilit [YENI], yercekimi_tork, kablo, devrilme, montaj_sokme, kutle).
"""
from __future__ import annotations

import itertools
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

import params as P  # noqa: E402
import params_boyun as PB  # noqa: E402
import boyun as BY  # noqa: E402
from lib import Ry, Rx, Rz, nokta  # noqa: E402
from checks import rapor_yaz, geo  # noqa: E402
from checks.core import Sonuc  # noqa: E402
from checks.strok import kontrol_strok  # noqa: E402
from checks.diferansiyel_tork import kontrol_diferansiyel_tork, potansiyel_yuk  # noqa: E402
from checks.yercekimi_tork import kontrol_yercekimi_tork, eylemsizlik, dinamik_tork  # noqa: E402
from checks.poz_kilit import kontrol_poz_kilit  # noqa: E402
from checks.kablo import kontrol_kablo  # noqa: E402
from checks.devrilme import kontrol_devrilme  # noqa: E402
from checks.montaj_sokme import kontrol_montaj_sokme  # noqa: E402
from checks.havada import kontrol_tek_govde  # noqa: E402

HIZLI = "--hizli" in sys.argv
G = 9.80665
RHO = P.PLA / 1000.0


def _p(pt=0.0, rl=0.0, yw=0.0):
    return dict(bas_yaw=float(yw), bas_pitch=float(pt), bas_roll=float(rl))


def basili_kutle(M):
    """dilimleyici yaklasimi (check.kutle ile ayni): g."""
    V = M.volume(); A = M.surface_area()
    return RHO * (min(V, A * P.DUVAR_E) + P.DOLGU * max(0.0, V - A * P.DUVAR_E))


# ================================================================== kutle (bas tarafi boyun kalemleri)
def bas_boyun_kalemleri():
    """bas grubuyla donen CP3b-2 kalemleri: [dict(ad, kutle, konum (bas cercevesi), kaynak)]."""
    import build as BLD
    out = [dict(ad="rotil kafa ucu x2 (M3 rotil 3 g + M3x14/somun 1.5 g) [TAHMIN K3]", kutle=9.0, konum=(0.0, -6.0, -26.0), kaynak="tahmin")]
    if PB.YAY_VAR:
        out.append(dict(ad="yay yarisi + kanca [TAHMIN K6]", kutle=3.0, konum=PB.YAY_KAFA, kaynak="tahmin"))
    out.append(dict(ad="roll pimi M4x40 + nyloc [KAYNAK]", kutle=6.0, konum=(0.0, 0.0, 0.0), kaynak="celik M4x40 ~5 g"))
    m_ic = basili_kutle(BLD.yukle("P1_ic")); m_or = basili_kutle(BLD.yukle("P1_orta"))
    ust = np.array(PB.P1_UST)
    out.append(dict(ad=f"P1 ust yarisi x2 (ic tup {m_ic:.1f} + orta {m_or:.1f} + 2x M3x14/nyloc 3.2 g)", kutle=2 * (m_ic + m_or + 3.2),
                    konum=(0.0, ust[1] - 25.0, ust[2] - 8.0), kaynak="CAD hacmi + vida"))
    return out


def bas_kutle_tablosu():
    """(kalemler [(ad, g, konum bas cercevesi)], toplam) - check.kutle'nin basili + satin + boyun kalemleri."""
    import check as C
    _, kal = C.kutle()
    L = [(k["ad"], k["kutle"], np.array(k["konum"], float)) for k in kal]
    for ad, g in P.SATIN_KUTLE.items():
        if g > 0 and "REZERV" not in ad:
            L.append((ad, g, np.array(C.SATIN_KONUM[ad], float)))
        elif "yanak" in ad and "REZERV" in ad and "P2_dis" not in BLD_PARCALAR():
            L.append((ad, g, np.array(C.SATIN_KONUM[ad], float)))
    for k in bas_boyun_kalemleri():
        L.append((k["ad"], k["kutle"], np.array(k["konum"], float)))
    return L


def BLD_PARCALAR():
    import build as BLD
    return BLD.PARCALAR


# ================================================================== yay modeli
def yay_L(p, t=0.0):
    return float(np.linalg.norm(nokta(BY.bas_T(p), PB.YAY_KAFA) - nokta(BY.yaw_T(p), BY.yay_delik(t))))


def yay_U(p, t=0.0, k=PB.YAY_K):
    """yay potansiyeli kg*cm (N*mm / 9.80665 / 10); F = k (L - LE) (L >= L0 her pozda: yay_ayar_sirasi olcer)."""
    L = yay_L(p, t)
    return 0.5 * k * (L - PB.YAY_LE) ** 2 / G / 10.0


def U_yer(p, L, carpan=1.0):
    T = BY.bas_T(p)
    return sum(m / 1000.0 * carpan * nokta(T, c)[1] / 10.0 for _, m, c in L)     # kg * cm


# ================================================================== 1. tork
def tork():
    out = []
    L = bas_kutle_tablosu()
    M = sum(m for _, m, _ in L)
    am = sum(m * c for _, m, c in L) / M
    # eylemsizlik (nokta kutle) pitch (X) ve roll (Z) -> dinamik ek (30 deg / 0.5 s)
    km = [(a, m, c, np.zeros((3, 3))) for a, m, c in L]
    Ip = eylemsizlik(km, (0, 0, 0), (1, 0, 0)); Ir = eylemsizlik(km, (0, 0, 0), (0, 0, 1))
    dp = dinamik_tork(Ip, PB.DINAMIK["aci"], PB.DINAMIK["sure"]); dr = dinamik_tork(Ir, PB.DINAMIK["aci"], PB.DINAMIK["sure"])
    pozlar = {f"p{pt:+.0f}_r{rl:+.0f}": np.radians([pt, rl]) for pt in PB.POZ_PITCH for rl in (-15, -10, -5, 0, 5, 10, 15)}

    def f_servo(q, r=None):
        ps = BY.egme_coz(_p(math.degrees(q[0]), math.degrees(q[1])), r)
        if any(v is None for v in ps.values()):
            return None
        return np.radians([ps[1], ps[-1]])

    kap = {f"{c:g} kg*cm": c for c in PB.EGME_KAPASITE}
    esas = f"{PB.EGME_KAPASITE[1]:g} kg*cm"
    tablo = []
    varyant = ((("yayli %75, nominal", 1.0, True, 1.5), ("yayli %75, kutle +%30", PB.KUTLE_ARTI, True, 1.5),
                ("YAYSIZ (yay kirik), nominal", 1.0, False, 1.0)) if PB.YAY_VAR else
               (("YAYSIZ (yay yok), nominal", 1.0, False, 1.5), ("YAYSIZ (yay yok), kutle +%30", PB.KUTLE_ARTI, False, 1.5)))
    for et, carpan, yay, hedef in varyant:
        def U(q, carpan=carpan, yay=yay):
            p = _p(math.degrees(q[0]), math.degrees(q[1]))
            return U_yer(p, L, carpan) + (yay_U(p) if yay else 0.0)
        ek = {0: dp * carpan + PB.SURTUNME_PITCH, 1: dr * carpan}
        s = kontrol_diferansiyel_tork(pozlar, f_servo, lambda q, U=U: potansiyel_yuk(U, q), kap, esas, hedef=hedef, ek=ek,
                                      ad=f"diferansiyel_tork [{et}]", etiket="")
        s.notlar.insert(0, f"bas kutlesi {M * carpan:.0f} g, AM {np.round(am, 1).tolist()}; I_pitch {Ip * carpan * 1e4:.1f} kg*cm2, "
                           f"dinamik pitch {dp * carpan:.3f} / roll {dr * carpan:.3f} kg*cm, surtunme {PB.SURTUNME_PITCH}; hedef {hedef}")
        if not yay and PB.YAY_VAR:
            s.olculdu.append("YAYSIZ durum hedefi 1.0 (yalniz tutabilme; KAGIT_OLCUM 'yay sart' karari): pay < 1 -> bulgu")
        out.append(s)
        tm = getattr(s, "gereken", float("nan"))
        tablo.append((et, [c / tm for c in PB.EGME_KAPASITE]))
    # yercekimi egrisi (pitch, roll 0): yaysiz / yayli
    eg = []
    for pt in range(-25, 21, 5):
        q = np.radians([pt, 0.0])
        Tg = potansiyel_yuk(lambda qq: U_yer(_p(math.degrees(qq[0]), 0), L), q)[0]
        Ty = potansiyel_yuk(lambda qq: yay_U(_p(math.degrees(qq[0]), 0)), q)[0]
        eg.append((pt, Tg, Ty))
    km0 = [(a, m / 1000.0 * 1000, c, np.zeros((3, 3))) for a, m, c in L]
    sy = kontrol_yercekimi_tork([(a, m, c, I) for a, m, c, I in km0], (0, 0, 0), (1, 0, 0), (0, 1, 0), list(range(-25, 21, 5)),
                                kapasite_kgcm=2 * PB.EGME_KAPASITE[1], hedef=1.5, ek={"dinamik": dp, "surtunme": PB.SURTUNME_PITCH},
                                ad="yercekimi_tork_pitch [yaysiz, iki servo toplam, bilgi]",
                                girdi_notu="kapasite = 2 x 2.5 (krank cos ve diferansiyel paylasim diferansiyel_tork'ta)")
    sy.notlar.append("EGRI pitch: yercekimi / yay / net (kg*cm, + = asagi devirir): " +
                     "  ".join(f"{pt:+d}: {Tg:+.2f}/{-Ty:+.2f}/{Tg + Ty:+.2f}" for pt, Tg, Ty in eg))
    tg_ = np.array([e[1] for e in eg]); ty_ = np.array([-e[2] for e in eg])
    sy.notlar.append(f"yay denge orani (nominal delik, en kucuk kareler) {float(ty_ @ tg_ / (tg_ @ tg_)):.2f} (hedef {PB.YAY_HEDEF}); "
                     f"en buyuk sapma {float(np.max(np.abs(ty_ - PB.YAY_HEDEF * tg_))):.3f} kg*cm")
    out.append(sy)
    if not PB.YAY_VAR:
        sy.notlar.append("OMURGA2: yay YOK (kaldirildi); yay sutunu bilgi amacli eski ankrajla hesaplandi")
        return out, tablo, (M, am, eg)
    # yay ayar sirasi kapsami
    sa = Sonuc("yay_ayar_sirasi")
    ors = []
    for t in PB.YAY_DELIKLER:
        tg_, ty_ = [], []
        for pt in range(-25, 21, 5):
            q = np.radians([pt, 0.0])
            tg_.append(potansiyel_yuk(lambda qq: U_yer(_p(math.degrees(qq[0]), 0), L), q)[0])
            ty_.append(-potansiyel_yuk(lambda qq, t=t: yay_U(_p(math.degrees(qq[0]), 0), t), q)[0])
        tg_, ty_ = np.array(tg_), np.array(ty_)
        o = float(ty_ @ tg_ / (tg_ @ tg_))
        Ls = [yay_L(_p(pt), t) for pt in (-25, 0, 20)]
        ors.append((t, o, min(Ls), max(Ls)))
        sa.notlar.append(f"delik t {t:+.0f}: denge orani {o:.2f}; yay boyu -25/0/+20: {Ls[0]:.0f}/{Ls[1]:.0f}/{Ls[2]:.0f} mm; "
                         f"kuvvet {PB.YAY_K * (min(Ls) - PB.YAY_LE):.2f}..{PB.YAY_K * (max(Ls) - PB.YAY_LE):.2f} N")
        if min(Ls) < PB.YAY_L0:
            sa.bulgu(f"delik t {t:+.0f}: yay boyu {min(Ls):.1f} < serbest boy {PB.YAY_L0} (gevsek -> model gecersiz)")
    lo, hi = min(o[1] for o in ors), max(o[1] for o in ors)
    if lo > PB.YAY_AYAR[0] or hi < PB.YAY_AYAR[1]:
        sa.bulgu(f"5 delik ortalama oran {lo:.2f}..{hi:.2f} araligi {PB.YAY_AYAR} hedefini kapsamiyor (k {PB.YAY_K} N/mm varsayimi)")
    sa.olculdu.append(f"{len(PB.YAY_DELIKLER)} delik x pitch -25..+20: yay torku / yercekimi orani; hedef aralik {PB.YAY_AYAR}")
    sa.olculmedi.append("yay sabiti k ve on gerilme (satin alinacak yay, K6); k x0.5..x2 sapmasi delik sirasiyla tam karsilanmaz -> makara opsiyonu (KAGIT 9)")
    out.append(sa)
    return out, tablo, (M, am, eg)


# ================================================================== 2. strok
def strok():
    deg, sin, bir = {}, {}, {}
    o = BY.p1_tup_olcu()
    Lalt = max(o["z0i"] + o["Li"] + o["z0d"] + 1.2, o["z0d"] + o["Ld"] + o["z0i"]) + PB.STROK_PAY
    Lust = o["z0d"] + o["z0i"] + o["Li"] + o["Ld"] - 2 * o["od_d"]       # bindirme >= 2 x OD
    pozlar = [(pt, rl) for pt in PB.POZ_PITCH for rl in (-15.0, -7.5, 0.0, 7.5, 15.0)]
    for pt, rl in pozlar:
        p = _p(pt, rl); pa = f"p{pt:+.0f}_r{rl:+.1f}"
        ps = BY.egme_coz(p)
        ra = BY.rotil_acilari(p, ps)
        for s, nm in ((1, "L"), (-1, "R")):
            deg.setdefault(f"krank_{nm} (r 22.8)", {})[pa] = ps[s]
            deg.setdefault(f"rotil_alt_{nm}", {})[pa] = None if ra[s] is None else ra[s][0]
            deg.setdefault(f"rotil_ust_{nm}", {})[pa] = None if ra[s] is None else ra[s][1]
            sol = BY.p1_coz(p, s)
            deg.setdefault(f"P1{nm} tup boyu (pim1-pim1)", {})[pa] = sol["L"]
            deg.setdefault(f"P1{nm} kardan ust pim1 (K5)", {})[pa] = sol["ust"][1]
            deg.setdefault(f"P1{nm} kardan alt pim1 (K5)", {})[pa] = sol["alt"][1]
            deg.setdefault(f"P1{nm} kardan ust pim2 (mentese)", {})[pa] = sol["ust"][0]
            deg.setdefault(f"P1{nm} kardan alt pim2 (mentese)", {})[pa] = sol["alt"][0]
    for k in deg:
        if k.startswith("krank"):
            sin[k] = (-PB.KRANK_MAKS, PB.KRANK_MAKS); bir[k] = "deg"
        elif k.startswith("rotil"):
            sin[k] = (None, PB.ROTIL_ACI_MAKS); bir[k] = "deg"
        elif "tup boyu" in k:
            sin[k] = (Lalt, Lust); bir[k] = "mm"
        elif "pim1" in k:
            sin[k] = (-PB.KARDAN_MAKS, PB.KARDAN_MAKS); bir[k] = "deg"
        else:
            sin[k] = (-45.0, 45.0); bir[k] = "deg"
    s = kontrol_strok(deg, sin, bir, ad="strok_boyun")
    s.notlar.insert(0, f"P1 tup: dis {o['Ld']} / ic {o['Li']} mm, pim1-tup {o['z0d']:.1f}/{o['z0i']:.1f}; izinli pim1-pim1 [{Lalt:.1f}, {Lust:.1f}] "
                       f"(alt: ic tup ucu dis tup tabanina / dis tup agzi ic koniye {PB.STROK_PAY} mm; ust: bindirme >= 2 x OD)")
    s.olculmedi.append("kardan pim2 (mentese) +-45 siniri geometrik tahmin; gercek sinir poz_kilit carpismasinda (orta x dil)")
    s.olculmedi.append("rotil acisal siniri 25 deg [TAHMIN K3]; P1 0.4/0.6 varyant tuplerinde boy ayni, yalniz ic OD degisir")
    # 1.5:1 deligi zarfi (bilgi): her pitch icin krank <= 60'i saglayan en buyuk roll
    zarf = []
    for pt in (PB.POZ_PITCH if PB.KRANK.get("r2_var", True) else ()):
        rmax = 0.0
        for rl in np.arange(0, 15.01, 0.5):
            ok = all(v is not None and abs(v) <= PB.KRANK_MAKS for v in list(BY.egme_coz(_p(pt, rl), PB.KRANK["r2"]).values()) +
                     list(BY.egme_coz(_p(pt, -rl), PB.KRANK["r2"]).values()))
            if not ok:
                break
            rmax = rl
        zarf.append(f"{pt:+.0f}:+-{rmax:g}")
    if zarf:
        s.notlar.append("FIRMWARE ZARFI 1.5:1 deligi (r 15.2, krank <= 60): pitch:izinli roll  " + "  ".join(zarf))
    return s


# ================================================================== 3. poz kilit (tam izgara)
def _bas_parcalari(cene):
    import check as C
    import kin as K
    pz, _ = C.poz_bas(dict(K.NOTR, cene=float(cene)))
    out = {}
    for a, v in pz.items():
        m, T = (v if isinstance(v, tuple) else (v, np.eye(4)))
        M = geo.transform(geo.to_manifold(m), T)
        lo, hi = geo.bbox(M)
        if lo[1] < 16.0:                      # bas tabani alti / cene / yanlar: boyuna yaklasabilecekler
            out[a] = M
    return out


_BAS_CACHE = {}


def kur_poz(pz):
    c = pz.get("cene", 0.0)
    if c not in _BAS_CACHE:
        _BAS_CACHE[c] = _bas_parcalari(c)
    p = _p(pz["bas_pitch"], pz["bas_roll"], pz["bas_yaw"])
    Tb = BY.bas_T(p)
    out = {a: geo.transform(m, Tb) for a, m in _BAS_CACHE[c].items()}
    bp, _ = BY.poz(p)
    for a, (m, T) in bp.items():
        out[a] = geo.transform(geo.to_manifold(m), T)
    for a, m in GOV().items():
        out[a] = m
    return out


_GOV = {}


def GOV():
    if not _GOV:
        import check as C
        for a, m in C.GOV.items():          # sabit gogus + satin (lazy susan ust halkasi eksenel simetrik, yaw'dan bagimsiz)
            _GOV[a] = geo.to_manifold(m)
    return _GOV


BOYUN_GRUP = [("N1", "yaw"), ("O1?", "yaw"), ("N2", "yaw"), ("Y1", "yaw"), ("egme_mg996r_*", "yaw"), ("lazy_susan_ust", "yaw"), ("N3", "hac"),
              ("pim_pitch_*", "hac"), ("pim_roll*", "bas"), ("N4_L", "krankL"), ("egme_mgkol_L", "krankL"), ("N4_R", "krankR"),
              ("egme_mgkol_R", "krankR"), ("rotil_*_L", "rodL"), ("rod_L", "rodL"), ("N5_L", "rodL"), ("rotil_*_R", "rodR"),
              ("rod_R", "rodR"), ("N5_R", "rodR"), ("P1L_orta_ust", "p1Lu"), ("P1L_ic", "p1Lu2"), ("P1L_orta_alt", "p1La"),
              ("P1L_dis", "p1La2"), ("P1R_orta_ust", "p1Ru"), ("P1R_ic", "p1Ru2"), ("P1R_orta_alt", "p1Ra"), ("P1R_dis", "p1Ra2"),
              ("yay", "yay")]


def grup_of(ad):
    import fnmatch
    for d, g in BOYUN_GRUP:
        if fnmatch.fnmatchcase(ad, d):
            return g
    if ad in GOV():
        return "sabit"
    return "bas"


MUAF = {("rotil_ust_*", "B1"): "rotil gozu B1 kulagina M3 ile sikilir", ("rotil_alt_*", "N4_*"): "rotil gozu kranka M3 ile sikilir",
        ("rod_*", "rotil_*"): "M3 rod rotile vidalanir", ("N5_*", "rod_*"): "kilif rod uzerinde (rod kilifin ortasindan gecer)",
        ("P1?_orta_ust", "B1"): "kardan orta B1 diline M3 pimli (catal dili sarar)",
        ("P1?_orta_ust", "P1?_ic"): "orta ust catali tup dilini sarar (M3 pim)", ("P1?_orta_alt", "P1?_dis"): "orta catali tup dilini sarar",
        ("yay", "B1"): "yay kancasi B1 kulaginda",
        ("pim_pitch_*", "N2"): "M4 saplama catal deliginde", ("pim_pitch_*", "N3"): "M4 saplama hacta (3.3 kilavuz)",
        ("pim_roll*", "N3"): "M4 roll pimi hac deliginde", ("egme_mgkol_*", "N4_*"): "kit disk kolu krank cebinde",
        ("egme_mgkol_*", "egme_mg996r_*"): "disk kol spline", ("egme_mg996r_*", "O1?"): "kulaklar omur bloklarina M4 ile vidali (govde cebi +0.3)", ("O1?", "N1"): "kasa tabani N1 ustune oturur",
        ("O1?", "N2"): "kasa tabani cebi N2 flansinin arka kenarina oturur (temas)", ("O1L", "O1R"): "orta duzlemde 2x M3 ile birlesik",
        ("P1?_orta_alt", "O1?"): "kardan orta kasa diline pimli", ("yay", "O1L"): "S-kanca kasa diregi deliginde",
        ("Y1", "N1"): "Oldham pimleri N1 yariklarinda (0.2 radyal, Z4)", ("Y1", "mg996r_yaw"): "disk kol cebi servo milinde",
        ("Y1", "lazy_susan_*"): "Y1 r 16, rulman ic deligi r 28 (model halka kaba)",
        ("N1", "lazy_susan_ust"): "ust halka N1'e vidali", ("lazy_susan_ust", "lazy_susan_alt"): "rulman (satin, tek parca)",
        ("lazy_susan_*", "G1"): "alt halka guverteye vidali", ("mg996r_yaw", "lazy_susan_*"): "servo mili rulman ic deliginde",
        ("mg996r_yaw", "G1"): "servo G1 cebinde"}


def poz_kilit():
    kur = [("N3", "N2", 0.3), ("N3", "B1", 0.3), ("B4", "*", PB.CENE_BOYUN_PAY), ("*", "*", P.POZ_MIN_BOSLUK)]
    eks = {"bas_yaw": list(PB.POZ_YAW), "bas_roll": list(PB.POZ_ROLL), "cene": list(PB.POZ_CENE), "bas_pitch": list(PB.POZ_PITCH)}
    if HIZLI:
        eks = {"bas_yaw": [0.0, 70.0], "bas_roll": [0.0, 15.0], "cene": [0.0, 20.0], "bas_pitch": list(PB.POZ_PITCH)}
    gr = {}

    class GR(dict):
        def get(self, k, d=None):
            return grup_of(k)
    t0 = time.time()

    def hedef(kd):
        if kd["cene"] == 0.0 and kd["bas_roll"] == 0.0:
            return (-PB.ONE_EGILME_HEDEF, 20.0)
        return (None, None)
    s = kontrol_poz_kilit(kur_poz, eks, "bas_pitch", kur, gruplar=GR(), muaf=MUAF, notr=0.0, ince=0.5, hedef=hedef, ad="poz_kilit")
    s.notlar.insert(0, f"sure {time.time() - t0:.0f} s; bas parcalari: bas cercevesinde y_min < 16 olanlar (taban, cene, mikrofon, cene mekanizmasi)")
    s.olculmedi.append("goz yaw/pitch ve kapak pozlari izgaraya katilmadi: goz modulu bas icinde (y > 16), boyun/gogus parcalarina erisemez; "
                       "goz x kapak supurmesi check.py cakisma_goz_kapak_supurme'de")
    s.olculmedi.append("bas ici ciftler (ayni 'bas' grubu: B4 x B1 vb.) burada olculmedi - cene supurmesi check.py'de")
    return s


# ================================================================== 4. kablo, devrilme, montaj
def kablo():
    pozlar = {}
    for yw, pt, rl in itertools.product((-70, 0, 70), (-25, 0, 20), (-15, 0, 15)):
        p = _p(pt, rl, yw)
        pozlar[f"yaw{yw}_p{pt}_r{rl}"] = {"bas": BY.bas_T(p), "yaw": BY.yaw_T(p), "sabit": np.eye(4)}
    kc = PB.N1_KABLO["c"]; kk = PB.N2_KABLO_KANCA["c"]
    kab = [dict(ad="boyun 8 iletken (5V, GND, SDA, SCL, I2S SCK/WS/SD, 3V3)", boy=P.KABLO_8["boy"], servis=P.KABLO_8["servis"],
                noktalar=[("bas", (0, 44, -66)), ("bas", (0, 16, -50)), ("bas", (-10, -8, -40)), ("yaw", kk), ("yaw", (kc[0], -112, kc[1])),
                          ("yaw", (kc[0], -124, kc[1])), ("sabit", (-18, -134, 10)), ("sabit", (-8, -222, -2))])]
    for s, nm in ((1, "L"), (-1, "R")):
        kab.append(dict(ad=f"egme servo {nm} kablosu (30 cm + 30 cm uzatma)", boy=600.0, servis=40.0,
                        noktalar=[("yaw", (s * 24, -102, -58)), ("yaw", (s * 6, -108, -62)), ("yaw", (kc[0], -116, kc[1])),
                                  ("yaw", (kc[0], -124, kc[1])), ("sabit", (-18, -134, 10)), ("sabit", (0, -192, -2))]))
    s = kontrol_kablo(kab, pozlar, ad="kablo_boyun")
    s.olculmedi.append("kablo ile hareketli parcalar arasindaki carpisma (esnek) olculmedi; kanca/delik konumlari kablo yolu noktasi")
    return s


def devrilme():
    import build as BLD
    import check as C
    L = bas_kutle_tablosu()
    ks = []
    for a in ("G1", "G2L", "G2R", "G4L", "G4R"):
        M = BLD.yukle(a); ks.append((basili_kutle(M), geo.to_trimesh(M).center_mass))
    for a, g, c in (("yaw MG996R", 55, (0, -150, -10)), ("lazy susan", 150, (0, -128, 0)), ("kartlar", 60, (0, -205, -8)), ("hoparlor", 30, (0, -160, 35))):
        ks.append((g, np.array(c, float)))
    yaw0 = []
    for a in ("N1", "N2", "Y1", "N3", "O1L", "O1R"):
        M = BLD.yukle(a); yaw0.append((basili_kutle(M), geo.to_trimesh(M).center_mass))
    for s in (1, -1):
        yaw0.append((55.0, nokta(BY.egme_mg_T(s), (10.0, 0, -25.0))))
    pozlar = {}
    for yw, pt in itertools.product((-70, 0, 70), (-25, 0, 20)):
        p = _p(pt, 0, yw)
        kl = [(m, c) for m, c in ks] + [(m, nokta(BY.yaw_T(p), c)) for m, c in yaw0] + [(m, nokta(BY.bas_T(p), c)) for _, m, c in L]
        pozlar[f"yaw{yw}_p{pt}"] = [(m, (c[0], c[2], c[1] - P.KAIDE["y"][0])) for m, c in kl]     # masa: x, y = z, h = y - taban
    a, b, zc = P.KAIDE["a"], P.KAIDE["b"], P.KAIDE["zc"]
    destek = [(a * math.cos(t), zc + b * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 48, endpoint=False)]
    s = kontrol_devrilme(pozlar, destek, min_mesafe=15.0, min_aci=15.0, ad="devrilme")
    s.olculmedi.append("gogus satin kalemleri (lazy susan 150 g, kartlar, hoparlor) ve adaptor kablosu cekmesi TAHMIN")
    return s


def _dil_v(s, uc):
    """kardan ortasinin dile takilma yonu: ortanin kendi yerel Y'si (catal yanaklari arasi acik yon), notr pozda."""
    a1 = np.array(BY._p1_notr(s)[0 if uc == "ust" else 1][0])
    n1 = BY.p1_coz(_p(), s)[uc][2]
    v = np.cross(n1, a1)
    return tuple(v / np.linalg.norm(v))


def montaj():
    import check as C
    out = []
    bp, _ = BY.poz(_p())
    P_ = {a: geo.transform(geo.to_manifold(m), T) for a, (m, T) in bp.items()}
    X, mX, D = (1, 0, 0), (-1, 0, 0), (0, -1, 0)
    tez = [("N1", None), ("N2", D), ("O1L", D), ("O1R", D), ("egme_mg996r_L", mX), ("egme_mg996r_R", X), (["egme_mgkol_L", "N4_L"], mX),
           (["egme_mgkol_R", "N4_R"], X)]
    s = kontrol_montaj_sokme(tez, {a: P_[a] for a in ("N1", "N2", "O1L", "O1R", "egme_mg996r_L", "egme_mg996r_R", "egme_mgkol_L", "egme_mgkol_R", "N4_L", "N4_R")},
                             ad="montaj_sokme_boyun_tezgah")
    s.olculmedi.append("OMURGA: servolar kasa cebine DISARIDAN (+-X) takilir, kulak M4 somunlari yan girisli; sokme: krank vidasi -> 4 kulak vidasi -> servo; "
                       "M4/M3 alet koridoru elle (olculmedi)")
    out.append(s)
    # son montaj: gogus -> Y1 -> boyun alt montaji -> N3 -> bas -> roll pimi -> rodlar -> P1
    bas = {}
    pz, _ = C.poz_bas(dict(__import__("kin").NOTR))
    for a, v in pz.items():
        if a.startswith("tel_"):
            continue
        m, T = (v if isinstance(v, tuple) else (v, np.eye(4)))
        bas[a] = geo.transform(geo.to_manifold(m), T)
    parca = {**{a: m for a, m in GOV().items()}, **P_, **{f"bas:{a}": m for a, m in bas.items()}}
    alt = ["N1", "N2", "O1L", "O1R", "egme_mg996r_L", "egme_mg996r_R", "egme_mgkol_L", "egme_mgkol_R", "N4_L", "N4_R"]
    U = (0, 1, 0)
    sira = [(list(GOV()), None), ("Y1", D), (alt, D), ("N3", D), ("pim_pitch_L", mX), ("pim_pitch_R", X),
            (["rotil_alt_L", "rotil_ust_L", "rod_L", "N5_L"], D),
            (["rotil_alt_R", "rotil_ust_R", "rod_R", "N5_R"], D),
            ([f"bas:{a}" for a in bas], D), ("pim_roll_M4x40", (0, 0, 1)),
            ("P1L_orta_ust", _dil_v(1, "ust")), ("P1R_orta_ust", _dil_v(-1, "ust")), ("P1L_orta_alt", _dil_v(1, "alt")), ("P1R_orta_alt", _dil_v(-1, "alt")),
            (["P1L_ic", "P1L_dis"], mX), (["P1R_ic", "P1R_dis"], X)]
    m = {("bas:rotil_*", "*"): "cene rod/rotil bas tezgah montajinda", ("yay", "*"): "yay esnek, kanca ile en son takilir (montaj_sokme disi)"}
    s = kontrol_montaj_sokme(sira, parca, ad="montaj_sokme_boyun", muaf=m)
    s.olculmedi.append("yay (esnek, S-kanca) ve kablo montaj sokmeye girmedi; rod grubu once kranka (asagi + yana), bas sonra iner, ust rotil vidasi "
                       "sonra; P1: ortalar dillere, sonra kisaltilmis teleskop yandan catallara (pimler sokulu degil)")
    out.append(s)
    return out


def parca():
    import build as BLD
    ad = ["N1", "O1L", "O1R", "N2", "N3", "N4_L", "N4_R", "N5", "Y1", "P1_orta", "P1_dis", "P1_ic", "B1"]
    return [kontrol_tek_govde({a: BLD.yukle(a) for a in ad}, ad="tek_govde_boyun")]


def kontroller():
    t0 = time.time()
    out = parca()
    tk, tablo, _ = tork(); out += tk; print("tork", round(time.time() - t0), flush=True)
    out.append(strok()); print("strok", round(time.time() - t0), flush=True)
    out.append(kablo()); out.append(devrilme()); print("kablo/devrilme", round(time.time() - t0), flush=True)
    out += montaj(); print("montaj", round(time.time() - t0), flush=True)
    out.append(poz_kilit()); print("poz_kilit", round(time.time() - t0), flush=True)
    ozet = Sonuc("tork_pay_ozeti_CP3b-2")
    for et, pays in tablo:
        ozet.notlar.append(f"{et}: " + "  ".join(f"{c:g} kg*cm -> pay {p:.2f}" for c, p in zip(PB.EGME_KAPASITE, pays)))
    ozet.olculdu.append("pitch/roll en kotu servo payi 3 kapasite satiri (KAGIT 1: 2.0 / 2.5 / 3.5)")
    out.append(ozet)
    return out


if __name__ == "__main__":
    res = kontroller()
    print(rapor_yaz(res, os.path.join(P.OUT, "check_report_boyun.txt"), baslik="Project Bust CP3b-2 boyun")[:6000])
