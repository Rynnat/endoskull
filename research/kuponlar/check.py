"""Project Bust CP3a kuponlari - kontrol raporu -> out/check_report.txt (1. satir SONUC, sonra KAPSAM).

  PYTHONUTF8=1 python -B check.py
Kontroller agent-flow/checks'ten: tek_govde, havada_ada, sarkma, tabla (parca + tabla yerlesimi), cakisma (kupon
montajlari, poz taramasi), montaj_sokme (K1, K4), vida_envanter. Yeni genel check YAZILMADI (kupon isi; DECISIONS).
"""
from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

import build as B  # noqa: E402
import montaj as M  # noqa: E402
from params import *  # noqa: E402,F401,F403

from checks import rapor_yaz, geo  # noqa: E402
from checks.core import Sonuc  # noqa: E402
from checks.havada import kontrol_tek_govde, kontrol_ada  # noqa: E402
from checks.sarkma import kontrol_sarkma  # noqa: E402
from checks.tabla import kontrol_tabla  # noqa: E402
from checks.cakisma import kontrol_cakisma  # noqa: E402
from checks.montaj_sokme import kontrol_montaj_sokme  # noqa: E402
from checks.vida_envanter import kontrol_vida_envanter  # noqa: E402


def pozlar_ad(on, d):
    return {f"{on}{k}": v for k, v in d.items()}


def durdurucu(cx):
    """Kol alt kenari cikintinin dis ust kosesine degdigi aci (derece, negatif = kol ucu asagi)."""
    w = K1_KOL["W"] / 2
    px, pz = cx + K1["CIKINTI_W"] / 2, -(w + K1["CIKINTI_BOSLUK"])
    return math.degrees(math.atan2(pz, px) + math.asin(w / math.hypot(px, pz)))


def cakisma_hepsi():
    sonuc = []
    # K1: kol acisi; asagi yonde cikinti 110 TASARIM GEREGI DURDURUCU (-4.2 deg). Kol ucu yukari serbest.
    dur_k1 = durdurucu(K1["CIKINTI_X"][1])
    poz = {f"K1_phi{p:+.1f}": M.k1(p) for p in (dur_k1 + 0.5, 0.0, 10.0, 20.0, 30.0)}
    dur_k2 = durdurucu(K1["CIKINTI_X"][0])
    for pay in K2_PAYLAR:
        for p in (dur_k2 + 0.5, 0.0, 15.0):
            poz[f"K2mg{pay:.1f}_phi{p:+.1f}"] = M.k1(p, f"K2_mg_p{pay:.1f}")
    s = kontrol_cakisma(poz, min_bosluk=0.3, gruplar=M.K1_GRUP, ad="cakisma_K1_K2mg",
                        muaf={("mg996r", "mg_korna"): "kit korna servo miline gecer (satin alinan cift, spline tasarim geregi)"})
    s.olculmedi.append("kol asagi yonde durdurucu (cikinti) acisinin 0.5 deg ustunden asagisi olculmedi: temas KASITLI (sarkma siniri)")
    s.notlar.append(f"K1 kolu asagi durdurucu: cikinti 110 -> {dur_k1:.1f} deg; K2 MG kolu cikinti 50 -> {dur_k2:.1f} deg (kasitli)")
    sonuc.append(s)
    # K4: servo -25..+25 (strok 50) ; disk aci + oran
    thetas = list(range(-25, 26, 5))
    poz = {f"K4_th{t:+d}": M.k4(t) for t in thetas}
    for pay in K2_PAYLAR:
        for t in (-5, 0, 5):
            poz[f"K2sg{pay:.1f}_th{t:+d}"] = M.k4(t, f"K2_sg_p{pay:.1f}")
    s = kontrol_cakisma(poz, min_bosluk=0.3, gruplar=M.K4_GRUP, ad="cakisma_K4_K2sg",
                        muaf={("sg90", "sg_korna"): "kit korna servo miline gecer (satin alinan cift)"})
    b = [B.k4_disk_aci(t) for t in thetas]
    s.notlar.append(f"K4 disk acisi (servo -25..+25): {b[0]:.1f} .. {b[-1]:.1f} deg -> kapak stroku {b[-1] - b[0]:.1f} deg "
                    f"(oran {(b[-1] - b[0]) / 50:.2f}); orta oran {(B.k4_disk_aci(1) - B.k4_disk_aci(-1)) / 2:.2f}")
    s.olculmedi.append("K4 tel (Z-bukum O1) modellenmedi: tel yolu x krank/disk/direk carpismasi olculmedi (gozle, OLCUM_FORMU K4)")
    s.olculmedi.append("K2 SG kolu K4'te yalniz servo -5/0/+5 deg'de olculdu (olcu diregi +-9 deg'de kola deger, kasitli)")
    sonuc.append(s)
    # K3: nominal, kizak +-2, egim (B sokulu) 15/30/45
    # kizak kanal tabaninda KAYAR (temas tasarim geregi): yan bosluk olculsun diye kizak 0.35 kaldirilarak olculur
    poz = {"K3_nom": M.k3(kaldir=0.35), "K3_kizak-2": M.k3(kizak_dx=-2, kaldir=0.35), "K3_kizak+2": M.k3(kizak_dx=2, kaldir=0.35)}
    for e in (15, 30, 45):
        poz[f"K3_egim{e}"] = M.k3(egim=e)
    s = kontrol_cakisma(poz, min_bosluk=0.3, gruplar=M.K3_GRUP, ad="cakisma_K3",
                        muaf={("rotil_A", "rod"): "rod rotile vidalanir (satin alinan cift)",
                              ("rotil_B", "rod"): "rod rotile vidalanir (satin alinan cift)",
                              ("rotil_A", "K3_taban"): "rotil gozu direk ustune M3 ile sikilir (temas tasarim geregi)",
                              ("rotil_B", "K3_kizak"): "rotil gozu kizak ustune M3 ile sikilir (temas tasarim geregi)"})
    s.olculmedi.append("kizak x kanal TABANI temasi (kayma yuzeyi) olculmedi: kizak 0.35 kaldirilarak yalniz yan bosluk (0.4) olculdu")
    s.olculmedi.append("rotil modeli [TAHMIN] (goz O10x6, govde O5.5x12): gercek rotil olculunce yeniden olculmeli")
    sonuc.append(s)
    # K5 kardan: alt eklem, a x b = +-25
    poz = {}
    for tup in ("K5_kardan_dis", "K5_kardan_ic"):
        for a in (-25, 0, 25):
            for bb in (-25, 0, 25):
                poz[f"{tup[-3:]}_a{a:+d}_b{bb:+d}"] = M.k5_kardan(a, bb, tup)
    s = kontrol_cakisma(poz, min_bosluk=0.3, gruplar=M.K5_GRUP, ad="cakisma_K5_kardan")
    s.olculmedi.append("ust kardan eklemi (ic tup ucu) alt eklemle ayni geometri -> ayri olculmedi; M3 vida-pim govdesi modellenmedi")
    sonuc.append(s)
    # K5 teleskop ciftleri: ic tup 3 konumda
    poz = {}
    for c in K5["BOSLUKLAR"]:
        for ck in (0.5, 35.0, 65.0):
            poz[f"K5_{c:.1f}_c{ck:g}"] = M.k5_cift(c, ck)
    s = kontrol_cakisma(poz, min_bosluk=0.3, ad="cakisma_K5_teleskop")
    s.olculmedi.append("teleskop radyal boslugu 0.3 esiginin ustunde (0.4/0.5/0.6) -> min bosluk yalniz nominal eksenli olculdu; "
                       "10 deg eksen kacikligi fiziksel test (kama)")
    sonuc.append(s)
    # K2 donen pim
    poz = {}
    for cap in K2_PIM["DELIKLER"]:
        for a in (0, 90, 180):
            poz[f"K2pim{cap:.1f}_{a}"] = M.k2_pim(a, cap)
    sonuc.append(kontrol_cakisma(poz, min_bosluk=0.3, ad="cakisma_K2_pim"))
    return sonuc


def sokme():
    out = []
    p = M.k1(0)
    out.append(kontrol_montaj_sokme([("K1_tutucu", None), ("mg996r", (0, -1, 0)), (["mg_korna", "K1_kol"], (0, 1, 0))],
                                    p, ad="montaj_sokme_K1"))
    p = M.k4(0)
    out.append(kontrol_montaj_sokme([("K4_taban", None), ("sg90", (0, 0, -1)), (["sg_korna", "K4_krank"], (0, 0, -1)),
                                     ("K4_disk", (0, 0, -1))], p, ad="montaj_sokme_K4"))
    p = M.k3()
    out.append(kontrol_montaj_sokme([("K3_taban", None), ("K3_kizak", (0, 0, -1)), (["rotil_A", "rod", "rotil_B"], (0, 0, -1))],
                                    p, ad="montaj_sokme_K3"))
    return out


def vidalar():
    t2_m3 = T.SOMUN["M3"][1] + T.SOMUN_DERIN_PAY
    V = []
    V += [dict(ad=f"K1 kulak {i}", tip="M3", L=14.0, sikisan=K1["DUVAR_T"] + MG["KULAK_T"]) for i in range(4)]
    V += [dict(ad=f"K1 kol-korna {i}", tip="M2", L=8.0, sikisan=K1_KOL["T"] - (MG_KOL["T"] + K1_KOL["CEP_PAY"]) + MG_KOL["T"]) for i in range(2)]
    V += [dict(ad=f"K2 MG kol-korna {i}", tip="M2", L=8.0, sikisan=K2_MG["T"] - (MG_KOL["T"] + 0.1) + MG_KOL["T"]) for i in range(2)]
    V += [dict(ad="K2 SG kol-korna", tip="M2", L=8.0, sikisan=K2_SG["T"] - (SG_KOL["ARM_T"] + 0.1) + SG_KOL["ARM_T"])]
    V += [dict(ad="K2 donen pim", tip="M3", L=10.0,
               sikisan=K2_PIM["DONEN"][2] + T.EKSENEL_BOSLUK + (K2_PIM["SABIT"][2] - t2_m3))]
    V += [dict(ad=f"K3 rotil {n}", tip="M3", L=14.0, sikisan=ROTIL["GOZ_T"] + (K3["DIREK_UST"] - K3["SOMUN_UST"])) for n in "AB"]
    V += [dict(ad="K4 SG90 kulak", tip="M2", L=8.0, sikisan=T.SG90_KULAK_T + 3.3)]
    V += [dict(ad="K4 krank-korna", tip="M2", L=8.0, sikisan=K4["KRANK_T"] - (SG_KOL["ARM_T"] + 0.2) + SG_KOL["ARM_T"])]
    V += [dict(ad="K4 disk pimi", tip="M3", L=14.0, sikisan=K4["DISK_T"] + T.EKSENEL_BOSLUK + 5.0)]
    gap = K5["DIL"][1] + 2 * K5["EKSENEL"]
    V += [dict(ad=f"K5 kardan pim {i}", tip="M3", L=14.0, sikisan=gap + 2 * K5["CATAL_T"]) for i in range(4)]
    V += [dict(ad="K7 boss", tip="M3", L=8.0, sikisan=K7["KABUK"] + K7["BOSS_H"] - t2_m3)]
    s = kontrol_vida_envanter(V, ENVANTER, SATIN)
    s.olculmedi.append("M2 somun (K1/K2/K4 korna + K4 kulak: 6 adet ayni anda) envanterde TEYITSIZ (PLAN §12-4) -> satin listesinde 20 adet")
    s.olculmedi.append("kit merkez vidalari (MG996R / SG90 kornasi) somunsuz, listeye alinmadi")
    return s


def tabla_yerlesim_kontrol():
    s = Sonuc("tabla_yerlesim")
    for f in sorted(os.listdir(TABLA)):
        if not f.endswith(".stl"):
            continue
        m = geo.to_trimesh(os.path.join(TABLA, f))
        lo, hi = m.bounds
        if lo[0] < -1e-6 or lo[1] < -1e-6 or hi[0] > TABLA_XY + 1e-6 or hi[1] > TABLA_XY + 1e-6 or abs(lo[2]) > 1e-6:
            s.bulgu(f"{f}: {lo.round(1)} .. {hi.round(1)} tabla {TABLA_XY:g} disinda / z0 != 0")
        else:
            s.notlar.append(f"{f}: x {lo[0]:.1f}..{hi[0]:.1f}  y {lo[1]:.1f}..{hi[1]:.1f}  z {hi[2]:.1f}")
    s.olculdu.append(f"tabla STL'leri 0..{TABLA_XY:g} icinde, alt yuz z=0")
    return s


def tabla_ortusme():
    """Tabla yerlesiminde parcalar arasi bosluk >= 2 mm (her tabla bir 'poz')."""
    tablalar = B.tabla_yerlesim(geo.yukle_stl_klasoru(STL))
    poz = {f"tabla_{i + 1}": {f"{ad}#{k}": m for ad, k, m in tl} for i, tl in enumerate(tablalar)}
    s = kontrol_cakisma(poz, min_bosluk=2.0, ad="tabla_ortusme")
    s.olculmedi.append("slicer brim/etek alani ve Orca'nin kendi yerlestirmesi (--arrange) olculmedi")
    return s


def main():
    stl = geo.yukle_stl_klasoru(STL)
    sonuclar = [kontrol_tek_govde(stl), kontrol_ada(stl), kontrol_sarkma(stl), kontrol_tabla(stl, xy=200.0, z=240.0)]
    sonuclar += [tabla_yerlesim_kontrol(), tabla_ortusme()]
    sonuclar += cakisma_hepsi()
    sonuclar += sokme()
    sonuclar.append(vidalar())
    ek = Sonuc("kapsam_disi")
    ek.olculmedi += [
        "et kalinligi (tabla.kontrol_et): calistirilmadi - kuponlarda KASITLI ince et var (K5 tup 0.8 [SPEC 2.1], K7 kabuk 1.2 "
        "[SPEC 07 §4]) ve kabartma yazi cizgileri (<1 mm) KABA isin yontemini bogar; et degerleri params'ta acik",
        "tolerans zinciri: kuponlar zincir HALKALARINI olcmek icin (PLAN §6 Z2/Z3 girdisi); kupon icin zincir yok",
        "giris_yolu / kablo: kuponlarda alet koridoru elle (tum vidalar acik yuzden); servo kablosu serbest",
        "servo/korna/rotil olculeri [TAHMIN] (MG996R, kit kollar, rotil): OLCUM_FORMU 0. adim; farkliysa params + build --only",
        "yazi okunurlugu (0.6 kabartma, 2.5-5 mm) baskida; Orca dilim onizlemesinde gozle",
    ]
    sonuclar.append(ek)
    metin = rapor_yaz(sonuclar, os.path.join(OUT, "check_report.txt"),
                      baslik="Project Bust CP3a olcum kuponlari (K1 K2 K3 K4 K5 K7) - PLAN §8")
    print(metin[:6000])


if __name__ == "__main__":
    main()
