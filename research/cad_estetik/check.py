"""Project Bust CP3b-1 kontrol raporu -> out/check_report.txt (1. satir SONUC, sonra KAPSAM).

  PYTHONUTF8=1 python -B check.py [--hizli]
Kontroller agent-flow/checks'ten + YENI kutle_butce. CP3b-2'ye ertelenenler KAPSAM'da OLCULMEDI "CP3b-2".
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
import build as BLD  # noqa: E402
import bas as B  # noqa: E402
import kin as K  # noqa: E402
import satin as S  # noqa: E402
from lib import Tr, Rx, Ry, Rz, nokta  # noqa: E402

from checks import rapor_yaz, geo  # noqa: E402
from checks.core import Sonuc  # noqa: E402
from checks.havada import kontrol_tek_govde, kontrol_ada  # noqa: E402
from checks.sarkma import kontrol_sarkma  # noqa: E402
from checks.tabla import kontrol_tabla, kontrol_et  # noqa: E402
from checks.cakisma import kontrol_cakisma  # noqa: E402
from checks.montaj_sokme import kontrol_montaj_sokme  # noqa: E402
from checks.tolerans import kontrol_tolerans  # noqa: E402
from checks.giris_yolu import kontrol_giris_yolu, alet_silindiri  # noqa: E402
from checks.kablo import kontrol_kablo  # noqa: E402
from checks.vida_envanter import kontrol_vida_envanter  # noqa: E402
from checks.kutle_butce import kontrol_kutle_butce  # noqa: E402
from checks.plan_sapma import kontrol_plan_sapmasi  # noqa: E402

HIZLI = "--hizli" in sys.argv
CP = "CP3b-2"

# ------------------------------------------------------------------ parcalar
BASILI = {ad: BLD.yukle(ad) for ad in BLD.PARCALAR}
GRUP = {ad: v[1] for ad, v in BLD.PARCALAR.items()}
SAT = S.modeller()
for ad, (m, g) in SAT.items():
    GRUP[ad] = g
REZ = S.rezerv()
BAS_GRUPLARI = {"bas", "halka", "gozL", "gozR", "ustL", "ustR", "alt", "cene", "krank"} | {f"kol_{a}" for a in P.SG}
BAS = {**{a: m for a, m in BASILI.items() if GRUP[a] in BAS_GRUPLARI}, **{a: m for a, (m, g) in SAT.items() if g in BAS_GRUPLARI}}
GOV = {**{a: m for a, m in BASILI.items() if GRUP[a] == "sabit"}, **{a: m for a, (m, g) in SAT.items() if g in ("sabit", "yaw")}}


def poz_bas(p):
    """{ad: (geo, T)} bas cercevesinde + teller + cene rodu."""
    Tg, aci = K.grup_T(p)
    out = {a: (m, Tg[GRUP[a]]) for a, m in BAS.items()}
    for t, (a, b) in K.teller(p, aci).items():
        out[t] = S.tel(a, b)
    psi = aci["cene_krank"]
    r1, r2, rod = S.cene_rod(psi, p["cene"])
    out["rotil_krank"], out["rotil_cene"] = r1, r2
    if rod is not None:
        out["cene_rod"] = rod
    return out, aci


def gruplar_bas():
    g = dict(GRUP)
    for t in ["tel_" + a for a in P.SG] + ["tel_yawL"]:
        g[t] = t
    g.update({"rotil_krank": "rod", "rotil_cene": "rod", "cene_rod": "rod"})
    return g


MUAF_BAS = {
    **{(f"sg90_{a}", f"sgkol_{a}"): "kit kolu servo miline (spline) gecer - satin alinan cift" for a in P.SG},
    ("mg996r_cene", "mgkol_cene"): "MG996R disk kolu spline - satin alinan cift",
    ("tel_yaw", "B5f_yaw"): "tel Z-bukumu bu kolun deliginde", ("tel_yawL", "B5f_yaw"): "tel Z-bukumu bu kolun deliginde",
    ("tel_yaw", "tel_yawL"): "iki tel ayni kol deliginde", ("tel_yaw", "B5b_R"): "tel Z-bukumu goz yaw kolunda",
    ("tel_yawL", "B5b_L"): "tel Z-bukumu goz yaw kolunda", ("tel_pitch", "B5f_pitch"): "tel bu kolda",
    ("tel_pitch", "B5h"): "tel pitch cubugu kulaginda", ("tel_alt", "B5f_alt"): "tel bu kolda", ("tel_alt", "B5i"): "tel alt cubuk kulaginda",
    ("tel_ustL", "B5f_ustL"): "tel bu kolda", ("tel_ustL", "B5d_L"): "tel kapak kolunda", ("tel_ustR", "B5f_ustR"): "tel bu kolda",
    ("tel_ustR", "B5d_R"): "tel kapak kolunda",
    ("tel_*", "sgkol_*"): "tel basili kolun deliginde, kit kolu ayni gobekte (kol ile birlikte doner)",
    ("rotil_krank", "C1"): "rotil gozu krank yuzune M3 ile sikilir (0.4 pul payi, temas tasarim geregi)",
    ("rotil_cene", "B4"): "rotil gozu cene koluna M3 ile sikilir",
    ("cene_rod", "rotil_*"): "M3 rod rotil govdesine vidalanir",
    ("B5h", "B5g_*"): "pitch cubugu halka kulagindaki O4.3 delige yapistirilir (ayni rijit grup)",
    ("B5i", "B5e_*"): "alt cubuk alt kapak kolu deligine yapistirilir (ayni rijit grup)",
}


def sonuc_bilgiye(s: Sonuc, neden: str) -> Sonuc:
    """CP3b-2 rezerv kontrolu: bulgulari bilgi notuna cevir (sonucu etkilemez) + OLCULMEDI satiri."""
    t = Sonuc(s.ad, True, [], s.olculdu, s.olculmedi + [neden], s.notlar + [f"BILGI ({CP}): {b}" for b in s.bulgular])
    return t


# ================================================================== 1. parca kontrolleri
def parca_kontrolleri():
    stl = geo.yukle_stl_klasoru(P.STL)
    ada = kontrol_ada(stl)
    # DESTEK KARARI (DECISIONS 'Destek listesi'): bu parcalarin adalari agac destekle basilir -> bulgu degil, not
    kalan = [b for b in ada.bulgular if b.split(":")[0] not in P.DESTEKLI]
    dest = [b for b in ada.bulgular if b.split(":")[0] in P.DESTEKLI]
    ada = Sonuc(ada.ad, not kalan, kalan, ada.olculdu, ada.olculmedi, ada.notlar + [f"AGAC DESTEK ({P.DESTEKLI[b.split(':')[0]]}): {b}" for b in dest])
    if dest:
        ada.olculmedi.append(f"{len(dest)} parcada ada agac destekle basilacak (P.DESTEKLI); destekli baskinin basarisi / destek izi OLCULMEDI (Orca onizleme + baski)")
    out = [kontrol_tek_govde(stl), ada, kontrol_tabla(stl, xy=P.TABLA_XY)]
    sk = kontrol_sarkma(stl)
    # ust kapaklar / kubbe / omuz: dilimleyicide agac destek planli (PLAN §2) -> bulgu yerine liste
    destekli = [b for b in sk.bulgular]
    sk2 = Sonuc("sarkma", True, [], sk.olculdu, sk.olculmedi, sk.notlar)
    for b in destekli:
        sk2.notlar.append("DESTEK GEREKLI: " + b)
    sk2.olculmedi.append(f"{len(destekli)} parcada konsol var -> agac destekle basilacak (PLAN §2 'tepede agac destek'); "
                         "desteksiz basilabilirlik OLCULMEDI, destek izi/temizlik kullanicida")
    out.append(sk2)
    kab = {a: m for a, m in stl.items() if a.startswith(("B3", "B5d", "B5e"))}
    yap = {a: m for a, m in stl.items() if not a.startswith(("B3", "B5d", "B5e", "B5c", "B5f", "B5h", "B5i", "P1_dis", "P1_ic", "N5", "P2_dis", "P2_ic"))}
    out.append(kontrol_et(kab, min_et=P.KABUK - 0.05, n=1500, ad="et_kabuk_1.2"))
    out.append(kontrol_et(yap, min_et=T_MIN_ET, n=1500, ad="et_yapisal_1.6"))
    out[-1].olculmedi.append("kozmetik ince parcalar (iris 1.6, kol 3, cubuk O4, piston tuplari 0.8, N5 kilif 1.2) et kontrolune alinmadi; kabuk 1.2 ayri esikte")
    return out


T_MIN_ET = 1.6


# ================================================================== 2. kutle
def kutle():
    import trimesh
    import yuz_kubbe as YK
    kal = []
    rho = P.PLA / 1000.0
    kabuk, _, _, _ = YK._kubbe_parcalari()
    from lib import kutu
    for ad in BLD.PARCALAR:
        if GRUP[ad] not in BAS_GRUPLARI:        # CP3b-2: yalniz bas ile donenler (N1/N2/N3/P1 vb. haric)
            continue
        M = BASILI[ad]
        V = M.volume(); A = M.surface_area()
        if ad in ("B3L", "B3R"):
            yari = kutu(0, 300, -300, 300, -300, 300) if ad == "B3L" else kutu(-300, 0, -300, 300, -300, 300)
            sh = kabuk ^ yari
            a_dis = sh.surface_area() / 2.0
            ek = max(0.0, V - sh.volume() - a_dis * P.KABURGA_T * 0.0)
            m = P.KABUK_G_CM2 * a_dis / 100.0 + 0.0
            kaynak = f"kabuk alani {a_dis / 100:.0f} cm2 x {P.KABUK_G_CM2} g/cm2 [KAGIT 8 kotu uc]"
        else:
            m = rho * (min(V, A * P.DUVAR_E) + P.DOLGU * max(0.0, V - A * P.DUVAR_E))
            kaynak = f"CAD hacmi {V / 1000:.1f} cm3, dilimleyici yaklasimi (cevre {P.DUVAR_E} mm + %{P.DOLGU * 100:.0f})"
        tm = geo.to_trimesh(M)
        kal.append(dict(ad=ad, kutle=m, butce=None, kaynak=kaynak, konum=tuple(tm.center_mass)))
    # plan butce gruplari
    grp = {"B3L": ["B3L"], "B3R": ["B3R"], "B2": ["B2"], "B4": ["B4"], "B1": ["B1"],
           "B5": [a for a in BLD.PARCALAR if a.startswith(("B5", "B6"))] + ["C1"]}
    top = []
    for g, uy in grp.items():
        ms = [k for k in kal if k["ad"] in uy]
        mm = sum(k["kutle"] for k in ms)
        am = tuple(np.sum([np.array(k["konum"]) * k["kutle"] for k in ms], 0) / mm)
        top.append(dict(ad=g + (" (+B6 mikrofon kabi, C1)" if g == "B5" else ""), kutle=mm, butce=P.KUTLE_BUTCE[g],
                        kaynak="; ".join(sorted({k["kaynak"].split(",")[0] for k in ms}))[:80], konum=am))
    konum = SATIN_KONUM
    _ = {"SG90 x5": (0, 10, 40), "cene MG996R + C1": (25, 44, -30), "PCA#2": (0, 44, -68), "vida+somun": (0, 20, 10),
             "kablo+LED": (0, 30, 10), "rotil kafa ucu x2 [REZERV]": (0, -6, -26), "yay kafa ucu [REZERV]": (0, -2, -64),
             "SCM piston yarisi x2 [REZERV]": (0, -10, -20), "yanak pistonu x2 [REZERV]": (0, -10, 55),
             "ses: 2x INMP441 + kablo": (0, 14, -44), "sahte detay (kabuga entegre, CAD'de)": (0, 0, 0)}
    import check_boyun as CB
    for ad, g in P.SATIN_KUTLE.items():
        if g > 0 and ("REZERV" not in ad or ("yanak" in ad and "P2_dis" not in BLD.PARCALAR)):
            top.append(dict(ad=ad, kutle=g, butce=g, kaynak="tahmin/datasheet (PLAN 5.1)" + (f" {CP}" if "REZERV" in ad else ""), konum=konum[ad]))
    for k in CB.bas_boyun_kalemleri():           # CP3b-2: REZERV satirlari yerine gercek kalemler
        top.append(dict(ad=k["ad"], kutle=k["kutle"], butce=k["kutle"], kaynak=k["kaynak"], konum=tuple(k["konum"])))
    s = kontrol_kutle_butce(top, P.HEDEF_KUTLE, tolerans=0.15, am_sinir=(5.0, None, None), parca_bulgu=False)
    for k in kal:
        s.notlar.append(f"   parca {k['ad']}: {k['kutle']:.1f} g")
    s.olculmedi.append("N3 hac (pitch ile doner, roll ile donmez; ~6 g, pivotta) bas butcesine girmedi; P2 yanak pistonu kurulana kadar PLAN tahmini")
    return s, kal


SATIN_KONUM = {"SG90 x5": (0, 10, 40), "cene MG996R + C1": (25, 44, -30), "PCA#2": (0, 44, -68), "vida+somun": (0, 20, 10),
               "kablo+LED": (0, 30, 10), "rotil kafa ucu x2 [REZERV]": (0, -6, -26), "yay kafa ucu [REZERV]": (0, -2, -64),
               "SCM piston yarisi x2 [REZERV]": (0, -10, -20), "yanak pistonu x2 [REZERV]": (0, -10, 55),
               "ses: 2x INMP441 + kablo": (0, 14, -44), "sahte detay (kabuga entegre, CAD'de)": (0, 0, 0)}


# ================================================================== 3. carpisma
def carpisma():
    out = []
    gr = gruplar_bas()
    # goz x kapak supurmesi (teller dahil)
    pozlar = {}
    yaws = (-P.GOZ_YAW, 0, P.GOZ_YAW)
    pits = (-P.GOZ_PITCH, 0, P.GOZ_PITCH)
    usts = (0, P.UST_STROK / 2, P.UST_STROK)
    alts = (0, P.ALT_STROK / 2, P.ALT_STROK)
    if HIZLI:
        yaws, pits = (-P.GOZ_YAW, P.GOZ_YAW), (-P.GOZ_PITCH, P.GOZ_PITCH)
    cozulmeyen = []
    for gy, gp, u, al in itertools.product(yaws, pits, usts, alts):
        p = dict(K.NOTR, goz_yaw=gy, goz_pitch=gp, ust_L=u, ust_R=u, alt=al)
        poz, aci = poz_bas(p)
        bos = [a for a, v in aci.items() if v is None]
        if bos:
            cozulmeyen.append((gy, gp, u, al, bos))
        pozlar[f"y{gy:+.0f}_p{gp:+.0f}_u{u:.0f}_a{al:.0f}"] = poz
    s = kontrol_cakisma(pozlar, muaf=MUAF_BAS, min_bosluk=P.POZ_MIN_BOSLUK, gruplar=gr, ad="cakisma_goz_kapak_supurme", sadece_capraz=False)
    for c in cozulmeyen:
        s.bulgu(f"baglanti cozulemedi (tel boyu sabit): poz {c[:4]} servo {c[4]}")
    s.olculmedi.append("goz yaw/pitch ile kapaklarin ayri ayri (ustL != ustR) kombinasyonu olculmedi (ikisi ayni aci)")
    s.olculmedi.append("Z-bukumlu tel ucu geometrisi (bukum, tel deligi icindeki 0.15 bosluk) modellenmedi: tel duz silindir O1")
    out.append(s)
    # cene supurmesi
    pozlar = {}
    for ph in np.arange(0, P.CENE_ACI + 0.01, 2.5):
        p = dict(K.NOTR, cene=float(ph))
        poz, aci = poz_bas(p)
        if aci["cene_krank"] is None:
            out.append(Sonuc("cene_rod", False, [f"cene {ph}: krank cozulmedi"]))
        pozlar[f"cene{ph:.1f}_krank{(aci['cene_krank'] or 0):.1f}"] = poz
    s = kontrol_cakisma(pozlar, muaf=MUAF_BAS, min_bosluk=P.POZ_MIN_BOSLUK, gruplar=gr, ad="cakisma_cene_supurme")
    s.olculmedi.append(f"cene x boyun kolonu / gogus (egme-cene kilidi, min {P.CENE_BOYUN_PAY} mm) - boyun ve egme {CP}: olculmedi")
    s.olculmedi.append(f"yanak pistonu P2 (cene <-> yuz) {CP}: cene supurmesine girmedi")
    out.append(s)
    # govde statik + bas notr <-> govde
    poz = {"notr": {**{a: m for a, m in GOV.items()}, **{a: m for a, m in BAS.items() if GRUP[a] in ("bas", "cene")}}}
    g = {a: ("sabit" if a in GOV else "bas") for a in poz["notr"]}
    s = kontrol_cakisma(poz, min_bosluk=P.POZ_MIN_BOSLUK, gruplar=g, ad="cakisma_govde_statik",
                        muaf={("lazy_susan_*", "G1"): "alt halka guverteye vidali (temas tasarim geregi)",
                              ("lazy_susan_alt", "lazy_susan_ust"): "rulman halkalari (satin alinan tek parca)",
                              ("mg996r_yaw", "lazy_susan_*"): "servo mili rulman ic deliginde, Y1 kaplin " + CP})
    s.olculmedi.append(f"bas pozlari (yaw +-70, pitch -25..+20, roll +-15) x govde/koprucuk {CP}: yalniz notr olculdu")
    out.append(s)
    # REZERV yer tutucular x CP3b-1 parcalari (bilgi)
    poz = {"notr": {**{a: m for a, (m, gg) in REZ.items()}, **{a: m for a, m in BAS.items() if GRUP[a] in ("bas", "cene")},
                    **{a: m for a, m in GOV.items()}}}
    g = {a: ("rezerv_" + a if a in REZ else "x") for a in poz["notr"]}
    r = kontrol_cakisma(poz, min_bosluk=0.0, gruplar=g, ad="rezerv_yer_tutucu_cakisma",
                        muaf={("N1_yaw_tablasi", "lazy_susan_ust"): "rulman ust halkasi N1'e vidali", ("Y1_kaplin", "mg996r_yaw"): "kaplin mile",
                              ("N3_U_hac", "N2_boyun_kolonu"): "catal pimi", ("N5_pushrod_*", "N4_krank_*"): "rotil", ("N5_pushrod_*", "B1"): "rotil kulagi",
                              ("N4_krank_*", "egme_mg996r_*"): "servo mili", ("yay", "B1"): "yay kancasi", ("egme_mg996r_*", "N1_yaw_tablasi"): "kulak",
                              ("N2_boyun_kolonu", "N1_yaw_tablasi"): "flans", ("Y1_kaplin", "N1_yaw_tablasi"): "Oldham yarigi",
                              ("P1_SCM_*", "*"): "konum " + CP, ("P2_yanak_*", "*"): "konum " + CP, ("Y1_kaplin", "lazy_susan_*"): "ic delik"})
    out.append(sonuc_bilgiye(r, f"REZERV yer tutucu (yalniz P2 yanak pistonu) kaba silindir: carpismalar yalniz bilgi"))
    return out


# ================================================================== 4. montaj-sokme
def sokme():
    out = []
    p, _ = poz_bas(K.NOTR)
    parca = {a: v for a, v in p.items() if not a.startswith("tel_")}
    for a, v in list(parca.items()):
        if isinstance(v, tuple):
            parca[a] = geo.transform(geo.to_manifold(v[0]), v[1])
    D = (0, -1, 0); U = (0, 1, 0)
    b5 = ["B5a", "B5b_L", "B5b_R", "B5c_L", "B5c_R", "B5g_L", "B5g_R", "B5h", "B5d_L", "B5d_R", "B5e_L", "B5e_R", "B5i"]
    sira = [("B1", None)] + [(f"sg90_{a}", D) for a in P.SG] + \
        [("mg996r_cene", (-1, 0, 0)), ("pca2", (0, 0, 1)),
         (["kopuk_L", "inmp441_L", "B6L"], (-1, 0, 0)), (["kopuk_R", "inmp441_R", "B6R"], (1, 0, 0)),
         ("kamera_rezerv", (0, 0, -1)), ("B2", U), (b5, D)] + \
        [([f"sgkol_{a}", f"B5f_{a}"], D) for a in P.SG] + \
        [("B4", U), (["mgkol_cene", "C1"], (-1, 0, 0)), ([a for a in ("rotil_krank", "rotil_cene", "cene_rod") if a in parca], (-1, 0, 0)),
         ("B3R", (1, 0, 0)), ("B3L", (-1, 0, 0))]
    s = kontrol_montaj_sokme(sira, parca, ad="montaj_sokme_bas")
    s.olculmedi.append("teller (O1 Z-bukum) takma yolu elle; montaj_sokme'ye girmedi")
    s.olculmedi.append(f"bas <-> boyun (N3 hac, adim 10-12) {CP}")
    out.append(s)
    gp = {a: geo.to_manifold(m) for a, m in GOV.items()}
    X = (-1, 0, 0)
    sira = [("G4R", None), ("G4L", X), ("G1", D), ("mg996r_yaw", D), ("lazy_susan_alt", D), ("lazy_susan_ust", D),
            ("hoparlor", X), ("kart_uno", X), ("kart_pca1", X), ("kart_esp32", X), ("kart_max98357", X), ("G2L", X), ("G2R", (1, 0, 0))]
    s = kontrol_montaj_sokme(sira, gp, ad="montaj_sokme_govde")
    s.olculmedi.append(f"N1/Y1/boyun alt montaji lazy susan ustune (adim 5, 7, 8) {CP}")
    out.append(s)
    return out


# ================================================================== 5. tolerans
def tolerans():
    E = np.array(P.GOZ[1])
    # Z1: kure <-> B2 goz cukuru kenari (dudak ic yuzu) radyal, modelden
    B2m = BASILI["B2"]
    eye = geo.transform(geo.to_manifold(BASILI["B5b_R"]), np.eye(4))
    z1 = float(eye.min_gap(B2m, 10.0))
    lid = BASILI["B5e_R"]
    z2 = float(geo.to_manifold(BASILI["B5d_R"]).min_gap(geo.to_manifold(BASILI["B5g_R"]), 5.0))
    zin = {
        "Z1 goz merkezleme (kure <-> B2 cukur, model)": {"halkalar": [("model bosluk", z1, 0, +1), ("B2-B1 vida", 0, 0.15, -1), ("B5-B1 M2", 0, 0.15, -1),
                                                                  ("kure pimi O1 tel", 0, 0.15, -1), ("kure O", 0, 0.10, -1),
                                                                  ("baski konum x3", 0, 0.30, -1)], "esik": 0.4},
        "Z2 kapak <-> halka (radyal, es eksen, model)": {"halkalar": [("model bosluk", z2, 0, +1), ("halka r", 0, 0.10, -1), ("kapak ic r", 0, 0.10, -1),
                                                                     ("halka M3 pimi", 0, 0.15, -1), ("kapak M3 pimi", 0, 0.15, -1),
                                                                     ("eksen kacikligi x2", 0, 0.20, -1)], "esik": 0.3},
        "Z2b goz <-> halka (radyal)": {"halkalar": [("nominal", P.HALKA_RI - P.GOZ_R, 0, +1), ("kure O", 0, 0.10, -1), ("halka ic r", 0, 0.10, -1),
                                                    ("O1 tel pim delik", 0, 0.15, -1), ("baski", 0, 0.10, -1)], "esik": 0.1},
        "Z6 cene kapali dis boslugu": {"halkalar": [("nominal", 2.25, 0, +1), ("kondil M4 radyal 0.15 x kol 60/1", 0, 0.15 * 75 / 60, -1),
                                                   ("B2-B1 vida", 0, 0.15, -1), ("dis baski", 0, 0.2, -1)], "esik": 0.4},
    }
    s = kontrol_tolerans(zin, olculmeyen=[f"Z3/Z3b diferansiyel pushrod, Z4/Z4b yaw tablasi, Z5 SCM strok {CP}"])
    s.notlar.append(f"model: kure<->B2 {z1:.2f} mm, ust kapak<->halka {z2:.2f} mm")
    return s


# ================================================================== 6. giris yolu
def giris():
    al = []
    p, _ = poz_bas(K.NOTR)
    parca = {a: (geo.transform(geo.to_manifold(v[0]), v[1]) if isinstance(v, tuple) else v) for a, v in p.items() if not a.startswith("tel_")}
    hepsi = list(parca)
    # B3 yan vidalari (X), dis yuzden
    for s in (-1, 1):
        for nm, d in P.B3_DIREK.items():
            zc = sum(d["z"]) / 2
            bas = (s * 63.0, P.B3_VIDA_Y, zc)
            al.append(dict(ad=f"B3_{nm}_{'L' if s > 0 else 'R'}", vida="M3x14",
                           geo=alet_silindiri(bas, (-s, 0, 0), 6.0, 60), mevcut=[a for a in hepsi if a not in ("B3L", "B3R")]))
        b = P.B3_ARKA
        al.append(dict(ad=f"B3_arka_{'L' if s > 0 else 'R'}", vida="M3x14", geo=alet_silindiri((s * 20, b["vida_y"], -72), (0, 0, 1), 6.0, 60),
                       mevcut=[a for a in hepsi if a not in ("B3L", "B3R")]))
        # B2 kulak vidalari alttan (B4 takilmadan once)
        for dx in P.B2_KULAK["delik_x"]:
            al.append(dict(ad=f"B2_kulak_{s * dx:+.0f}", vida="M3x14", geo=alet_silindiri((s * dx, P.B2_TAB_Y[0], P.B2_KULAK["delik_z"]), (0, 1, 0), 6.0, 90),
                           mevcut=[a for a in hepsi if a not in ("B4", "B3L", "B3R", "C1", "mgkol_cene", "rotil_krank", "rotil_cene", "cene_rod")]))
        # kondil M4 (disaridan, X)
        al.append(dict(ad=f"kondil_{'L' if s > 0 else 'R'}", vida="M4x10", geo=alet_silindiri((s * (P.CENE_TAB_X[1] + 3.0), P.KONDIL[1], P.KONDIL[2]), (-s, 0, 0), 7.0, 60),
                       mevcut=[a for a in hepsi if a not in ("B3L", "B3R", "C1", "mgkol_cene", "rotil_krank", "rotil_cene", "cene_rod")]))
    # SG90 M2 (ustten), B5 takilmadan
    from sablonlar.sg90 import sg90_kulak_x
    for ad, sv in P.SG.items():
        x, z = sv["mil"][0], sv["mil"][1] + sg90_kulak_x()[1]
        al.append(dict(ad=f"sg90_{ad}_M2", vida="M2x8", geo=alet_silindiri((x, sv["ped"] + 2.5 + 1.6, z), (0, -1, 0), 4.0, 60),
                       mevcut=["B1"] + [f"sg90_{a}" for a in P.SG]))
    # B5 ayak M2 (ustten, B5 yerinde)
    b5 = [a for a in hepsi if a.startswith("B5") and not a.startswith("B5f")]
    for x, z in B.B5_AYAK_VIDA:
        al.append(dict(ad=f"B5_ayak_{x:+.0f}_{z:.0f}", vida="M2x8", geo=alet_silindiri((x, P.B1_Y[1] + 3.0 + 1.6, z), (0, -1, 0), 4.0, 60),
                       mevcut=["B1", "B2"] + [f"sg90_{a}" for a in P.SG] + b5))
    # cene servosu M4 (disaridan +X'ten, krank yok)
    mt = B.mg_T(); xc = (P.MG["L"] - 2 * P.MG["N"]) / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            q = mt[:3, :3] @ np.array([xc + sx * P.MG["KULAK_DX"], sy * P.MG["KULAK_DY"], 0]) + mt[:3, 3]
            al.append(dict(ad=f"cene_servo_M4_{sx}{sy}", vida="M4x14", geo=alet_silindiri((P.CENE_SERVO["mil_x"] + P.MG["KULAK_Z0"] + P.MG["KULAK_T"] + 3.0, q[1], q[2]), (-1, 0, 0), 7.0, 50),
                           mevcut=["B1", "mg996r_cene"] + [f"sg90_{a}" for a in P.SG]))
    s = kontrol_giris_yolu(al, parca, muaf={("B3_*", "B3*"): "vida kabuk deliginden gecer (kabugun kendisi)"})
    s.olculmedi.append("PCA#2 M3 (arkadan), mikrofon M2, lazy susan / G1-G4 / G2-G1 vidalari alet koridoru olculmedi")
    s.olculmedi.append(f"N3 hac M4 pimleri, rotil kulaklari, yay kancasi alet yolu {CP}")
    return s


# ================================================================== 7. kablo
def kablo():
    pozlar = {}
    for yw, pt, rl in itertools.product((-70, 0, 70), (-25, 0, 20), (-15, 0, 15)):
        p = dict(K.NOTR, bas_yaw=yw, bas_pitch=pt, bas_roll=rl)
        pozlar[f"yaw{yw}_p{pt}_r{rl}"] = {"bas": Tr(0, 0, 0) @ K.bas_T(p) if False else Ry(yw) @ Rx(-pt) @ Rz(rl), "yaw": Ry(yw), "sabit": np.eye(4)}
    kab = [dict(ad="boyun 8 iletken (5V, GND, SDA, SCL, I2S SCK/WS/SD, 3V3)", boy=P.KABLO_8["boy"], servis=P.KABLO_8["servis"],
                noktalar=[("bas", (0, 44, -66)), ("bas", (0, 16, -50)), ("bas", (0, -4, -24)), ("yaw", (0, -60, -24)),
                          ("yaw", (0, -118, -12)), ("sabit", (-18, -134, 10)), ("sabit", (-8, -222, -2))])]
    s = kontrol_kablo(kab, pozlar)
    s.olculmedi.append(f"kablo yolu boyun icinde REZERV noktalarla (N2 kolon arkasi) - gercek gecis {CP}; 2 egme servo kablosu {CP}")
    return s


# ================================================================== 8. vida
def vidalar():
    v = [dict(ad="SG90 kulak x5", tip="M2", L=8.0, sikisan=2.5 + 1.2), dict(ad="B5 ayak x4", tip="M2", L=8.0, sikisan=3.0 + 3.0 - 1.8),
         dict(ad="mikrofon kabi x4", tip="M2", L=8.0, sikisan=2.0 + P.MIK["kopuk"] + 2.0),
         dict(ad="kamera rezerv x4", tip="M2", L=8.0, sikisan=2.0 + 1.6),
         dict(ad="goz dis pim x4 (M3x10)", tip="M3", L=10.0, sikisan=5.0 - 2.6),
         dict(ad="B3 yan x4", tip="M3", L=14.0, sikisan=4.5 + 0.4 + 1.5), dict(ad="B3 arka x2", tip="M3", L=14.0, sikisan=3.0 + 0.4 + 1.5),
         dict(ad="B2 kulak x4", tip="M3", L=14.0, sikisan=3.6 + 0.4 + 5.0 - 1.4), dict(ad="PCA#2 x4", tip="M3", L=14.0, sikisan=1.6 + 4.4 + 3.0 - 2.6),
         dict(ad="rotil cene x2", tip="M3", L=14.0, sikisan=6.0 + 0.4 + 4.0), dict(ad="kondil M4 x2", tip="M4", L=10.0, sikisan=4.0 + 0.4 + 5.0 - 3.4),
         dict(ad="cene servo kulak x4", tip="M4", L=14.0, sikisan=2.5 + 4.0), dict(ad="yaw servo kulak x4 (G1)", tip="M4", L=14.0, sikisan=2.5 + 4.0),
         dict(ad="G2-G1 x6", tip="M3", L=14.0, sikisan=5.0 + 0.4 + 3.0), dict(ad="G1-G4 x4", tip="M3", L=14.0, sikisan=6.5 + 4.0 - 2.6),
         dict(ad="G4L-G4R x4", tip="M3", L=14.0, sikisan=3.0 + 3.0 - 2.6), dict(ad="lazy susan alt x4", tip="M3", L=14.0, sikisan=2.0 + 5.0)]
    s = kontrol_vida_envanter(v, {"M2": (8.0,), "M3": (8.0, 10.0, 14.0), "M4": (8.0, 10.0)}, satin={"M3": (20.0, 25.0), "M4": (14.0, 20.0, 40.0)})
    s.olculmedi.append("ic M3 dişli cubuk (goz ic pimi, 38.6 mm, 1 m cubuktan kesilir) ve rotil rodu vida listesinde degil; BOM'da")
    return s


def plan_sapma():
    dec = open(os.path.join(HERE, "DECISIONS.md"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "DECISIONS.md")) else ""
    kal = [dict(anahtar="ust kapak stroku", plan="75", model=str(P.UST_STROK)),
           dict(anahtar="kapak malzemesi", plan="PETG 0.8", model="PLA 1.2"),
           dict(anahtar="goz yaw pimi", plan="M3 vida-pim", model="O1 tel pim"),
           dict(anahtar="ust kapak pivotu", plan="iki yan", model="tek yan (dis)"),
           dict(anahtar="B2 vidalari", plan="onden 4x M3", model="alttan 4x M3"),
           dict(anahtar="kubbe sagital", plan="bindirme + 6x M3 her yari", model="bindirme dili vidasiz + 3x M3 B1'e"),
           dict(anahtar="mikrofon yeri", plan="kabuk deligi 12 mm", model="sakak penceresinde ayri kap"),
           dict(anahtar="cene servosu yonu", plan="konsept mil Y", model="mil X (+X yan duvar)"),
           dict(anahtar="montaj sirasi", plan="B4 adim 9, B2 adim 14", model="B2 B4'ten once (tezgahta)"),
           dict(anahtar="lazy susan", plan="100-120", model="100 OD [TAHMIN]"),
           dict(anahtar="pitch pimi", plan="1x M4x40", model="2x M4x14 saplama"),
           dict(anahtar="P1 SCM yeri", plan="(+-55, -10, -20)", model="mastoid alti (+-42, -4, -30) -> N1 arka kolu"),
           dict(anahtar="N5 kilif et", plan="0.8", model="1.2"),
           dict(anahtar="P2 yanak pistonu", plan="B2 <-> B4 basili", model="kurulmadi (B2 kilitli)")]
    return kontrol_plan_sapmasi(kal, dec)


def main():
    t0 = time.time()
    sonuc = []
    sonuc += parca_kontrolleri(); print("parca", round(time.time() - t0), flush=True)
    km, kal = kutle(); sonuc.append(km); print("kutle", round(time.time() - t0), flush=True)
    sonuc += carpisma(); print("carpisma", round(time.time() - t0), flush=True)
    sonuc += sokme(); print("sokme", round(time.time() - t0), flush=True)
    sonuc.append(tolerans()); sonuc.append(giris()); sonuc.append(kablo()); sonuc.append(vidalar()); sonuc.append(plan_sapma())
    import check_boyun as CB
    sonuc += CB.kontroller(); print("boyun", round(time.time() - t0), flush=True)
    if "P2_dis" not in BLD.PARCALAR:
        ert = Sonuc("ertelenen_P2")
        ert.olculmedi.append(f"{CP}: P2 yanak pistonlari yer tutucu (satin.rezerv); strok/carpisma olculmedi")
        sonuc.append(ert)
    metin = rapor_yaz(sonuc, os.path.join(P.OUT, "check_report.txt"), baslik="Project Bust CP3b-1 + CP3b-2 (boyun)")
    print(metin[:3000])
    print("sure", round(time.time() - t0))


if __name__ == "__main__":
    main()
