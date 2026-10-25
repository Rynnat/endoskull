"""Project Bust CP3a - olcum kuponlari (PLAN.md §8: K1, K2, K3, K4, K5, K7). Asil bust CAD'i DEGIL.

Calistir (kuponlar/ icinde):
  PYTHONUTF8=1 C:\\Users\\LENOVO\\Projeler\\epic-project\\.venv-cad\\Scripts\\python.exe -B build.py            # hepsi + tabla
  ... build.py --only K4_disk,K4_krank        # yalniz bu parcalar (tabla yeniden birlestirilir)
  ... build.py --liste                        # parca adlari
Cikti: out/stl/<parca>.stl (BASKI YONUNDE, z=0 tabla), out/tabla/tabla_<n>.stl + yerlesim.txt.
Her parca: ayri fonksiyon, ayri STL, pay/varyant adi KABARTMA yazi (istisnalar DECISIONS.md).
Sablonlar (agent-flow/sablonlar): sg90_cebi, servo_kolu.*_cebi / modelleri, baglanti.somun_tuzagi / vida_pim_eklemi /
pahli_delik. Project Angela dosyalari KULLANILMADI.
"""
from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from params import *  # noqa: E402,F401
import params as P  # noqa: E402

import cadquery as cq  # noqa: E402
import numpy as np  # noqa: E402

from sablonlar.sg90 import sg90_cebi, sg90_kulak_x  # noqa: E402
from sablonlar.servo_kolu import sg90_tek_kol_cebi, mg996r_disk_kol_cebi  # noqa: E402
from sablonlar.baglanti import somun_tuzagi, vida_pim_eklemi, pahli_delik  # noqa: E402

# =====================================================================================================================
# yardimcilar
# =====================================================================================================================


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def silindir(r, z0, z1, x=0.0, y=0.0):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(r).extrude(z1 - z0)


def silindir_eksen(r, p0, p1):
    """p0 -> p1 dogrultusunda silindir."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    s = cq.Solid.makeCylinder(r, L, cq.Vector(*p0), cq.Vector(*(d / L)))
    return cq.Workplane("XY").add(s)


def yazi_ust(metin, boy, x, y, z, h=ETIKET_H, aci=0.0):
    """Ust yuzde KABARTMA yazi: z'den +Z'ye h (z yuzeyin kendisi; 0.01 bindirme -> tek govde)."""
    a = math.radians(aci)
    pl = cq.Plane(origin=(x, y, z - 0.01), xDir=(math.cos(a), math.sin(a), 0), normal=(0, 0, 1))
    return cq.Workplane(pl).text(metin, boy, h + 0.01, combine=False, halign="center", valign="center", kind="bold")


def yazi_on(metin, boy, x, z, y_yuz, h=ETIKET_H, oyma=False):
    """-Y'ye bakan dikey yuzde (y = y_yuz) yazi; okunus onden (-Y'den) bakinca dogru. oyma=True -> kesici."""
    if oyma:
        pl = cq.Plane(origin=(x, y_yuz + h, z), xDir=(1, 0, 0), normal=(0, -1, 0))
        return cq.Workplane(pl).text(metin, boy, h + 0.05, combine=False, halign="center", valign="center", kind="bold")
    pl = cq.Plane(origin=(x, y_yuz + 0.01, z), xDir=(1, 0, 0), normal=(0, -1, 0))
    return cq.Workplane(pl).text(metin, boy, h + 0.01, combine=False, halign="center", valign="center", kind="bold")


def cizgi_xz(r0, r1, aci_deg, merkez_x, merkez_z, y_yuz, en=0.6, derin=ETIKET_OYMA):
    """-Y yuzunde (y_yuz) radyal oyma cizgi kesicisi (XZ duzleminde, aci x ekseninden +z'ye)."""
    a = math.radians(aci_deg)
    L = r1 - r0
    rm = (r0 + r1) / 2
    b = cq.Workplane("XY").box(L, derin * 2, en).rotate((0, 0, 0), (0, 1, 0), -aci_deg)
    return b.translate((merkez_x + rm * math.cos(a), y_yuz, merkez_z + rm * math.sin(a)))


def cizgi_xy(r0, r1, aci_deg, z_ust, en=0.6, derin=ETIKET_OYMA):
    """Ust yuzde (z_ust) radyal oyma cizgi kesicisi (XY)."""
    a = math.radians(aci_deg)
    rm = (r0 + r1) / 2
    b = cq.Workplane("XY").box(r1 - r0, en, derin * 2).rotate((0, 0, 0), (0, 0, 1), aci_deg)
    return b.translate((rm * math.cos(a), rm * math.sin(a), z_ust))


def stadyum_y(x, z, cap, yarik, y0, y1):
    """Y boyunca delen, Z yonunde uzun delik (dikey duvarda yatay eksenli)."""
    r = cap / 2
    c1 = silindir_eksen(r, (x, y0, z - yarik), (x, y1, z - yarik))
    c2 = silindir_eksen(r, (x, y0, z + yarik), (x, y1, z + yarik))
    return c1.union(c2).union(kutu(x - r, x + r, y0, y1, z - yarik, z + yarik))


def m2_somun_kanalli(x, y, z0, kanal, aci=0.0):
    """M2 somun cebi (AF 4.0 + 0.3, t 1.6 + 0.2) + yandan surme kanali (baglanti.somun_tuzagi deseninin M2 kopyasi:
    sablonda M2 somun yok -> [TASLAK], kupon icinde)."""
    af2 = SOMUN_M2[0] + T.SOMUN_AGIZ_PAY
    t2 = SOMUN_M2[1] + T.SOMUN_DERIN_PAY
    kk = af2 / math.cos(math.radians(30))
    c = cq.Workplane("XY").workplane(offset=z0).polygon(6, kk).extrude(t2)
    c = c.union(cq.Workplane("XY").workplane(offset=z0).center(kanal / 2, 0).rect(kanal, af2).extrude(t2))
    return c.rotate((0, 0, 0), (0, 0, 1), aci).translate((x, y, 0))


def kol_govdesi(boy, w, hub_r, t, kuyruk=0.0):
    """+X kol (t kalin): gobek dairesi + w genis cubuk + yuvarlak uc; kuyruk > 0 ise -X'te sivri gosterge."""
    g = cq.Workplane("XY").circle(hub_r).extrude(t)
    g = g.union(cq.Workplane("XY").center(boy / 2, 0).rect(boy, w).extrude(t))
    g = g.union(cq.Workplane("XY").center(boy, 0).circle(w / 2).extrude(t))
    if kuyruk:
        g = g.union(cq.Workplane("XY").polyline([(0, w / 2), (-kuyruk, 0), (0, -w / 2)]).close().extrude(t))
    return g


def ters_cep(kesici, t):
    """Montaj cercevesinde (z=0 kola degen yuz, cep +Z) verilen cebi BASKI cercevesine cevir: cep ust yuzden acilir."""
    return kesici.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, t))


# =====================================================================================================================
# satin alinan parca modelleri (carpisma icin; STL'e girmez)
# =====================================================================================================================


def mg996r_model():
    """MG996R, mil-ucu cercevesi (servo_kolu ile ayni): mil +Z, z=0 mil ucu, govde +X. Olculer [TAHMIN] params.MG."""
    m = MG
    x0, x1 = -m["N"], m["L"] - m["N"]
    xc = (x0 + x1) / 2
    g = kutu(x0, x1, -m["W"] / 2, m["W"] / 2, m["Z_ALT"], m["Z_UST"])
    k = kutu(xc - m["KULAK_BOY"] / 2, xc + m["KULAK_BOY"] / 2, -m["W"] / 2, m["W"] / 2, m["KULAK_Z0"], m["KULAK_Z0"] + m["KULAK_T"])
    for sx in (-1, 1):
        for sy in (-1, 1):
            k = k.cut(silindir(m["KULAK_DELIK"] / 2, m["KULAK_Z0"] - 1, m["KULAK_Z0"] + 5, xc + sx * m["KULAK_DX"], sy * m["KULAK_DY"]))
    g = g.union(k)
    g = g.union(silindir(m["BOSS_R"], m["Z_UST"] - 0.01, m["Z_BOSS"]))
    g = g.union(silindir(m["SPL_R"], m["Z_BOSS"] - 0.01, 0.0))
    return g


def mg996r_kulak_x():
    xc = (MG["L"] - 2 * MG["N"]) / 2
    return xc - MG["KULAK_DX"], xc + MG["KULAK_DX"]


def rotil_model():
    """M3 goz tipi rotil [TAHMIN]: goz (dikey eksen) merkezi orijinde, govde +X. Bilye merkezi z = 0."""
    r = ROTIL
    g = silindir(r["GOZ_D"] / 2, -r["GOZ_T"] / 2, r["GOZ_T"] / 2)
    g = g.union(silindir_eksen(r["GOVDE_D"] / 2, (r["GOZ_D"] / 2 - 1.0, 0, 0), (r["GOZ_D"] / 2 + r["GOVDE_L"], 0, 0)))
    return g.cut(silindir(1.5, -5, 5))


# =====================================================================================================================
# K1 - MG996R tork + bosluk tutucusu
# =====================================================================================================================


def k1_servo_cerceve():
    """Servo mil-ucu cercevesi -> dunya (K1 tutucu baski = montaj cercevesi). S_x -> -Z, S_y -> +X, S_z -> -Y."""
    y_uc = K1["DUVAR_T"] - (-(MG["KULAK_Z0"] + MG["KULAK_T"]))   # kulak ust yuzu arka duvar yuzunde
    M = np.eye(4)
    M[:3, 0] = (0, 0, -1)
    M[:3, 1] = (1, 0, 0)
    M[:3, 2] = (0, -1, 0)
    M[:3, 3] = (0, y_uc, K1["MIL_Z"])
    return M


def K1_tutucu():
    """Hafif K1: servo plakasi (pencere + kulak yariklari + kadran) + sagda kiris (olcu cikintilari) + uc direk + taban/ray."""
    k = K1
    zs, t = k["MIL_Z"], k["DUVAR_T"]
    x0, px1, x1 = k["X0"], k["PLAKA_X1"], k["X1"]
    g = kutu(x0, px1, 0, k["TABAN_Y"], 0, k["TABAN_T"])                     # taban (servo plakasi arkasi)
    g = g.union(kutu(px1 - 0.01, x1, 0, k["RAY_Y"], 0, k["TABAN_T"]))       # ray (kiris alti)
    g = g.union(kutu(x0, px1, 0, t, 0, k["DUVAR_Z"]))                        # servo plakasi
    kz0, kz1 = k["KIRIS_Z"]
    g = g.union(kutu(px1 - 0.01, k["DIREK_X"][1], 0, t, kz0, kz1))           # kiris
    g = g.union(kutu(k["DIREK_X"][0], k["DIREK_X"][1], 0, t, 0, kz1))        # uc direk
    for ax in k["ARA_DIREK_X"]:   # kiris alti kopru <= 22 mm (sarkma check: 85 mm kopru yakaladi)
        g = g.union(kutu(ax - 2, ax + 2, 0, t, k["TABAN_T"] - 0.01, kz0 + 0.01))
    hx0, hx1, hz0, hz1 = k["HAFIF"]
    g = g.cut(kutu(hx0, hx1, -1, t + 1, hz0, hz1))
    for gx in k["GUSSET_X"]:
        tri = (cq.Workplane("YZ", origin=(gx - k["GUSSET_T"] / 2, 0, 0))
               .polyline([(t - 0.01, k["TABAN_T"] - 0.01), (t + k["GUSSET_Y"], k["TABAN_T"] - 0.01), (t - 0.01, k["GUSSET_Z"])])
               .close().extrude(k["GUSSET_T"]))
        if gx > px1:   # kiris direginin arkasi: ray dar, ucgen kucuk
            tri = (cq.Workplane("YZ", origin=(gx - k["GUSSET_T"] / 2, 0, 0))
                   .polyline([(t - 0.01, k["TABAN_T"] - 0.01), (k["RAY_Y"], k["TABAN_T"] - 0.01), (t - 0.01, kz1 - 6)])
                   .close().extrude(k["GUSSET_T"]))
        g = g.union(tri)
    # olcu cikintilari: kol alt kenarinin CIKINTI_BOSLUK altinda, 45 deg alt pah (desteksiz)
    z_ust = zs - K1_KOL["W"] / 2 - k["CIKINTI_BOSLUK"]
    yc = k["CIKINTI_Y"]
    for cx in k["CIKINTI_X"]:
        cik = (cq.Workplane("YZ", origin=(cx - k["CIKINTI_W"] / 2, 0, 0))
               .polyline([(0.01, z_ust), (yc, z_ust), (yc, z_ust - 3), (0.01, z_ust - 3 + yc)]).close()
               .extrude(k["CIKINTI_W"]))
        g = g.union(cik)
        g = g.union(yazi_on(f"{cx:g}", 4.5, cx - 11, (kz0 + kz1) / 2, 0.0))
    # servo penceresi (mil ust ucta: yakin uc yukari)
    pw, pl = MG_PENCERE_PAY
    g = g.cut(kutu(-(MG["W"] + pw) / 2, (MG["W"] + pw) / 2, -1, t + 1, zs - (MG["L"] - MG["N"]) - pl / 2, zs + MG["N"] + pl / 2))
    # kulak uzun delikleri (M3, yatay eksen -> +0.2)
    for kx in mg996r_kulak_x():
        for ky in (-MG["KULAK_DY"], MG["KULAK_DY"]):
            g = g.cut(stadyum_y(ky, zs - kx, M3 + YATAY, k["YARIK"], -1, t + 1))
    # kadran: kuyruk gostergesi icin (kol ucu +theta yukari -> kuyruk 180+theta, asagi)
    r0, r1, r2 = k["KADRAN_R"]
    for a in range(-k["KADRAN_ACI"], k["KADRAN_ACI"] + 1, k["KADRAN_ADIM"]):
        uzun = a % 10 == 0
        g = g.cut(cizgi_xz(r0, r2 if uzun else r1, 180 + a, 0.0, zs, 0.0))
    for a in (-20, -10, 0, 10, 20):
        aa = math.radians(180 + a)
        g = g.union(yazi_on(f"{a:+d}" if a else "0", 3.5, 41.0 * math.cos(aa), zs + 41.0 * math.sin(aa), 0.0))
    g = g.union(yazi_on("K1 MG996R", 4.0, 76.0, (kz0 + kz1) / 2, 0.0))
    g = g.union(yazi_ust("K1", 6, -10.0, 28.0, k["TABAN_T"]))
    return g


def mg_kol(boy, w, hub_r, t, pay, delikler, kuyruk=0.0, etiketler=(), erisim=K1_KOL["ERISIM_D"]):
    """MG996R disk kol cepli kaldirac, BASKI cercevesinde (cep ust yuzde). Mil merkezi orijinde, kol +X."""
    g = kol_govdesi(boy, w, hub_r, t, kuyruk)
    g = g.cut(ters_cep(mg996r_disk_kol_cebi(pay=pay), t))
    g = g.cut(silindir(erisim / 2, -1, t + 1))
    for s in (-1, 1):
        g = g.cut(pahli_delik(M2, t).translate((0, s * MG_KOL["HOLE_R"], 0)))
    for d in delikler:
        g = g.cut(pahli_delik(K1_KOL["ASKI_D"], t).translate((d, 0, 0)))
    for metin, boy_, x in etiketler:
        g = g.union(yazi_ust(metin, boy_, x, 0, t))
    return g


def K1_kol():
    k = K1_KOL
    # etiketler cebin (r 10.7) DISINDA: "20" cep ile 20 deligi arasinda, digerleri deliklerin 10 mm gerisinde
    et = [(f"{d:g}", 4.0, 15.0 if d == 20 else d - 10) for d in k["DELIKLER"]] + [(f"p{k['CEP_PAY']:.1f}", 4.0, 108.0)]
    return mg_kol(k["BOY"], k["W"], k["HUB_R"], k["T"], k["CEP_PAY"], k["DELIKLER"], kuyruk=k["KUYRUK"], etiketler=et)


def k1_kol_cerceve(phi=0.0, t=K1_KOL["T"]):
    """Kol BASKI cercevesi -> servo mil-ucu cercevesi (disk alti z = Y0). phi: kol ucu yukari (+)."""
    return Tz(MG_KOL["Y0"]) @ Rz(90 + phi) @ baski_to_montaj(t)


# =====================================================================================================================
# K2 - kol cebi paylari + donen M3 eklem
# =====================================================================================================================


def _k2_mg(pay):
    k = K2_MG
    return mg_kol(k["UC"], k["W"], k["HUB_R"], k["T"], pay, (K2_KOL_BOY,),
                  etiketler=[(f"MG {pay:.1f}", 4.5, 33.0)])


def sg_kol(pay, uc, w, hub_r, t, ek_delikler=(), tel=None, etiketler=()):
    """SG90 tek kol cepli kaldirac, BASKI cercevesinde. Mil merkezi orijinde, kit kolu +X."""
    g = kol_govdesi(uc, w, hub_r, t)
    if tel:   # -X tarafinda tel deligi kolu (krank)
        g = g.union(cq.Workplane("XY").center(-tel / 2, 0).rect(tel, w).extrude(t))
        g = g.union(silindir(w / 2, 0, t, -tel))
        g = g.cut(pahli_delik(K4["TEL_DELIK"], t).translate((-tel, 0, 0)))
    g = g.cut(ters_cep(sg90_tek_kol_cebi(pay=pay), t))
    g = g.cut(silindir(K2_SG["ERISIM_D"] / 2, -1, t + 1))
    g = g.cut(pahli_delik(M2, t).translate((SG_KOL["HOLE_R"], 0, 0)))
    for d in ek_delikler:
        g = g.cut(pahli_delik(K1_KOL["ASKI_D"], t).translate((d, 0, 0)))
    for metin, boy_, x in etiketler:
        g = g.union(yazi_ust(metin, boy_, x, 0, t))
    return g


def _k2_sg(pay):
    k = K2_SG
    return sg_kol(pay, k["UC"], k["W"], k["HUB_R"], k["T"], (K2_KOL_BOY,), etiketler=[(f"SG {pay:.1f}", 4.0, 33.0)])


def K2_pim_sabit():
    x, y, z = K2_PIM["SABIT"]
    vp = vida_pim_eklemi("M3", sabit_t=z, donen_t=K2_PIM["DONEN"][2])
    g = kutu(-x / 2, x / 2, -y / 2, y / 2, 0, z).cut(vp["sabit"])
    # etiket -Y yan yuzde (ust yuzu donen kol supurur)
    g = g.union(yazi_on("K2 M3", 3.0, 0, z / 2, -y / 2))
    return g


def _k2_pim_donen(cap):
    x, y, z = K2_PIM["DONEN"]
    g = kutu(-6, x - 6, -y / 2, y / 2, 0, z).cut(pahli_delik(cap, z))
    g = g.union(yazi_ust(f"{cap:.1f}", 4.5, 15.0, 0, z))
    g = g.union(kutu(K2_PIM["OLCU_R"] - 0.4, K2_PIM["OLCU_R"] + 0.4, -y / 2, y / 2, z - 0.01, z + ETIKET_H))   # olcu cizgisi
    return g


# =====================================================================================================================
# K3 - M3 rotil / pushrod boslugu
# =====================================================================================================================


def _alttan_somun_direk(x, y, z_ust, somun_ust):
    """Alttan sokulan M3 somun (derin altigen cep, tavani somun_ust) + 3.3 delik z_ust'e kadar."""
    t2 = T.SOMUN["M3"][1] + T.SOMUN_DERIN_PAY
    return somun_tuzagi("M3", ek_derinlik=somun_ust - t2, z0=-0.01).union(silindir(M3 / 2, -1, z_ust + 1)).translate((x, y, 0))


def K3_taban():
    k = K3
    x0, x1, y0, y1, t = k["TABAN"]
    g = kutu(x0, x1, y0, y1, 0, t)
    dx, dy = k["DIREK"]
    g = g.union(kutu(-dx / 2, dx / 2, -dy / 2, dy / 2, 0, k["DIREK_UST"]))
    g = g.cut(_alttan_somun_direk(0, 0, k["DIREK_UST"], k["SOMUN_UST"]))
    # kizak kanali
    w = k["KIZAK"][1] / 2 + k["KANAL_BOSLUK"]
    kx0, kx1 = k["KANAL_X"]
    for s in (-1, 1):
        g = g.union(kutu(kx0, kx1, min(s * w, s * (w + k["KANAL_DUVAR"])), max(s * w, s * (w + k["KANAL_DUVAR"])), t - 0.01, k["KANAL_Z"]))
    g = g.union(kutu(kx1 - 3, kx1, -(w + k["KANAL_DUVAR"]), w + k["KANAL_DUVAR"], t - 0.01, k["DIREK_UST"]))
    # aci plakasi (XZ), cizgiler bilye merkezinden
    py0, pt, plx, pz = k["ACI_PLAKA"]
    g = g.union(kutu(-dx / 2, plx, py0, py0 + pt, t - 0.01, pz))
    zb = k["DIREK_UST"] + ROTIL["GOZ_T"] / 2
    for a in k["ACILAR"]:
        uzun = a % 15 == 0
        g = g.cut(cizgi_xz(12.0, 47.0 if uzun else 40.0, a, 0.0, zb, py0))
    for a in (0, 15, 30, 45):     # etiket cizgi ucunun (r 47) otesinde: oyma ustune binmesin (havada ada)
        aa = math.radians(a)
        g = g.union(yazi_on(f"{a}", 3.0, 51.5 * math.cos(aa), zb + 51.5 * math.sin(aa), py0))
    g = g.union(yazi_ust("K3 rotil", 5, 40.0, 0.0, t))
    g = g.union(yazi_ust("90", 4, 105.0, 0.0, t))
    return g


def K3_kizak():
    x, y, z = K3["KIZAK"]
    g = kutu(-x / 2, x / 2, -y / 2, y / 2, 0, z)
    g = g.cut(_alttan_somun_direk(0, 0, z, z - (K3["DIREK_UST"] - K3["SOMUN_UST"])))
    g = g.union(yazi_ust("K3", 3.5, -x / 2 + 2.6, 0, z, aci=90))
    return g


def k3_bilye_z():
    return K3["DIREK_UST"] + ROTIL["GOZ_T"] / 2


# =====================================================================================================================
# K4 - SG90 kapak hizi (1.5x baglanti + acili disk)
# =====================================================================================================================


def k4_pivot():
    """Disk pivotu P: orta konumda krank pimi C=(-R1,0), disk pimi D=(-R1,-L), D-P = (-R2, 0)."""
    k = K4
    return (-k["R1"] + k["R2"], -k["L_BAG"])


def k4_disk_aci(theta_deg):
    """Krank acisi theta (servo, CCW +) -> disk pimi acisi beta (derece, P etrafinda). Orta: theta 0 -> beta 180."""
    k = K4
    px, py = k4_pivot()
    t = math.radians(180 + theta_deg)
    cx, cy = k["R1"] * math.cos(t), k["R1"] * math.sin(t)
    vx, vy = cx - px, cy - py
    d = math.hypot(vx, vy)
    c = (d * d + k["R2"] ** 2 - k["L_BAG"] ** 2) / (2 * k["R2"] * d)
    c = max(-1.0, min(1.0, c))
    av = math.atan2(vy, vx)
    adaylar = [av + math.acos(c), av - math.acos(c)]
    ref = math.radians(180 + 1.5 * theta_deg)
    b = min(adaylar, key=lambda x: abs(math.atan2(math.sin(x - ref), math.cos(x - ref))))
    return math.degrees(b) % 360


def K4_taban():
    k = K4
    x0, x1, y0, y1, t = k["TABAN"]
    bx0, bx1, by0, by1 = k["BLOK"]
    g = kutu(x0, bx1, y0, y1, 0, t)                                    # T taban: servo + disk alani
    g = g.union(kutu(bx1 - 0.01, x1, -22.0, 0.0, 0, t))                # kol: K2 olcu diregine
    g = g.union(kutu(bx0, bx1, by0, by1, 0, T.SG90_KULAK_Z))
    g = g.cut(sg90_cebi(kulak_delikleri=None, alt_acik=1.0))
    kx = sg90_kulak_x()[1]
    g = g.cut(silindir(M2 / 2, T.SG90_KULAK_Z - 8, T.SG90_KULAK_Z + 1, kx, 0))
    g = g.cut(m2_somun_kanalli(kx, 0, T.SG90_KULAK_Z - 3.3 - (SOMUN_M2[1] + T.SOMUN_DERIN_PAY), kanal=bx1 - kx + 1.0))
    # disk pivot diregi + yandan somun kanali (somun_tuzagi kanal [TASLAK] -> bu kupon onu da dener)
    px, py = k4_pivot()
    g = g.union(silindir(k["DIREK_D"] / 2, 0, k["DIREK_UST"], px, py))
    z_somun = k["DIREK_UST"] - 5.0 - (T.SOMUN["M3"][1] + T.SOMUN_DERIN_PAY)
    g = g.cut(somun_tuzagi("M3", z0=z_somun, kanal=k["DIREK_D"] / 2 + 1.5).translate((px, py, 0)))
    g = g.cut(silindir(M3 / 2, k["DIREK_UST"] - 14.0, k["DIREK_UST"] + 1, px, py))
    # gosterge diregi (disk kenarina sivri uc, -Y tarafinda)
    gy = py - k["GOSTERGE_R"]
    z_top = k["DISK_ALT"] + k["DISK_T"]
    gos = kutu(px - 3, px + 3, gy - 4, gy + 1.0, 0, z_top)
    gos = gos.union(cq.Workplane("XY").polyline([(px - 3, gy + 1.0), (px + 3, gy + 1.0), (px, gy + 2.2)]).close().extrude(z_top))
    g = g.union(gos)
    # K2 SG kolu oynama diregi (yuz y = OLCU_DIREK[1], kolun 50 mm noktasinda)
    ox, oy = k["OLCU_DIREK"]
    g = g.union(kutu(ox - 3, ox + 3, oy - 7, oy, 0, 34.0))
    g = g.union(yazi_ust("K4 SG90 1.5x", 4.5, -3.0, -15.0, t))
    g = g.union(yazi_ust("50", 4, 40.0, -6.0, t))
    return g


def K4_krank():
    k = K4
    return sg_kol(0.2, 24.0, k["KRANK_W"] + 3.0, 7.5, k["KRANK_T"], tel=k["R1"], etiketler=[("K4", 3.5, 18.5)])


def K4_disk():
    k = K4
    r, t = k["DISK_R"], k["DISK_T"]
    g = silindir(r, 0, t)
    g = g.cut(pahli_delik(M3, t))
    g = g.cut(pahli_delik(k["TEL_DELIK"], t).translate((-k["R2"], 0, 0)))
    for a in range(0, 360, 5):
        uzun = a % 15 == 0
        g = g.cut(cizgi_xy(14.0 if uzun else 16.0, r - 0.6, a - 90, t))
    for a in range(0, 360, 30):
        aa = math.radians(a - 90)
        g = g.union(yazi_ust(f"{a}", 2.5, 11.0 * math.cos(aa), 11.0 * math.sin(aa), t, aci=a))
    return g


def k4_disk_cerceve(theta):
    px, py = k4_pivot()
    b = k4_disk_aci(theta)
    return Tx(px, py, K4["DISK_ALT"]) @ Rz(b - 180.0)


def k4_krank_cerceve(theta, t=K4["KRANK_T"]):
    return Rz(theta) @ Tz(SG_KOL["Z1"] - SG_KOL["ARM_T"]) @ baski_to_montaj(t)


# =====================================================================================================================
# K5 - teleskopik piston (PLA) + M3 vida-pimli kardan
# =====================================================================================================================


def _k5_tup(od, etiket):
    k = K5
    fx0, fx1, fy0, fy1, ft = k["FLANS"]
    g = kutu(fx0, fx1, fy0, fy1, 0, ft)
    g = g.union(silindir(od / 2, ft - 0.01, ft + k["BOY"]))
    g = g.cut(silindir(od / 2 - k["ET"], ft, ft + k["BOY"] + 1))
    g = g.cut(silindir(k["HAVA_D"] / 2, -1, ft + 1))
    g = g.union(yazi_ust(etiket, 4.0, (od / 2 + fx1) / 2 + 0.6, 0, ft, aci=90))
    return g


def k5_ic_od(c):
    return K5["DIS_OD"] - 2 * K5["ET"] - 2 * c


def K5_kama():
    k = K5
    L, W, h0 = k["KAMA"]
    h1 = h0 + L * math.tan(math.radians(k["KAMA_ACI"]))
    g = cq.Workplane("XZ").polyline([(0, 0), (L, 0), (L, h1), (0, h0)]).close().extrude(-W)
    g = g.union(cq.Workplane("XZ").polyline([(0, 0), (3, 0), (3, h0 + 4), (0, h0 + 4)]).close().extrude(-W))  # dudak
    g = g.union(yazi_on("K5 10", 4.5, L / 2 + 2, h1 / 2 - 0.3, 0.0))
    return g


def _dil(w, t, h, pah, delik_z, eksen):
    """Dikey dil (genislik w, kalinlik t, boy h), delik ekseni 'x' ya da 'y' (kalinlik yonu); genislik koseleri pahli."""
    if eksen == "y":     # kalinlik Y, genislik X -> pah XZ'de
        prof = [(-w / 2 + pah, 0), (w / 2 - pah, 0), (w / 2, pah), (w / 2, h), (-w / 2, h), (-w / 2, pah)]
        d = cq.Workplane("XZ").polyline(prof).close().extrude(t / 2, both=True)
        d = d.cut(silindir_eksen((M3 + YATAY) / 2, (0, -t, delik_z), (0, t, delik_z)))
    else:                # kalinlik X, genislik Y -> pah YZ'de (ustte)
        prof = [(-w / 2, 0), (w / 2, 0), (w / 2, h - pah), (w / 2 - pah, h), (-w / 2 + pah, h), (-w / 2, h - pah)]
        d = cq.Workplane("YZ").polyline(prof).close().extrude(t / 2, both=True)
        d = d.cut(silindir_eksen((M3 + YATAY) / 2, (-t, 0, delik_z), (t, 0, delik_z)))
    return d


def _k5_kardan_tup(od, harf):
    k = K5
    w, t, h = k["DIL"]
    g = _dil(w, t, h, k["DIL_PAH"], k["DIL_DELIK_Z"], "y")
    # omuz: dil ustunde r = t/2'den tup yaricapina 45 deg koni (desteksiz; ust catal yanaklarinin r 4.5 zarfinin disinda)
    oh = od / 2 - t / 2
    omuz = cq.Solid.makeCone(t / 2, od / 2, oh, cq.Vector(0, 0, h - 0.01), cq.Vector(0, 0, 1))
    g = g.union(cq.Workplane("XY").add(omuz))
    z0 = h + oh
    g = g.union(silindir(od / 2, z0 - 0.01, z0 + 1.5 + k["BOY"]))
    g = g.cut(silindir(od / 2 - k["ET"], z0 + 1.5, z0 + 1.5 + k["BOY"] + 1))
    # dil yuzune OYMA harf (kabartma catal boslugunu yerdi - DECISIONS)
    g = g.cut(yazi_on(harf, 2.4, 0, 8.6, -t / 2, h=0.3, oyma=True))
    return g


def k5_orta_olcu():
    k = K5
    gap = k["DIL"][1] + 2 * k["EKSENEL"]
    pin2 = 4.5
    blok0 = pin2 + 5.4 + 0.4 + 0.0
    blok1 = blok0 + 3.0
    pin1 = blok1 + 5.4 + 0.4
    return gap, pin2, blok0, blok1, pin1


def K5_kardan_orta():
    k = K5
    gap, pin2, b0, b1, pin1 = k5_orta_olcu()
    ct, cw = k["CATAL_T"], k["CATAL_W"]
    i, o = gap / 2, gap / 2 + ct
    g = kutu(-o, o, -o, o, b0, b1)
    for s in (-1, 1):   # alt catal: yanaklar X'te, pim X boyunca
        g = g.union(kutu(min(s * i, s * o), max(s * i, s * o), -cw / 2, cw / 2, 0, b0 + 0.01))
        yan = kutu(-cw / 2, cw / 2, min(s * i, s * o), max(s * i, s * o), b1 - 0.01, pin1)   # ust catal: yanaklar Y'de
        yan = yan.union(silindir_eksen(cw / 2, (0, min(s * i, s * o), pin1), (0, max(s * i, s * o), pin1)))
        g = g.union(yan)
    g = g.cut(silindir_eksen((M3 + YATAY) / 2, (-o - 1, 0, pin2), (o + 1, 0, pin2)))
    g = g.cut(silindir_eksen((M3 + YATAY) / 2, (0, -o - 1, pin1), (0, o + 1, pin1)))
    return g


def k5_ankraj_pim_z():
    return K5["ANKRAJ"][2] + 8.0


def K5_kardan_ankraj():
    k = K5
    ax, ay, at = k["ANKRAJ"]
    w, t, _ = k["DIL"]
    g = kutu(-ax / 2, ax / 2, -ay / 2, ay / 2, 0, at)
    h = 13.0
    g = g.union(_dil(w, t, h, k["DIL_PAH"], 8.0, "x").translate((0, 0, at - 0.01)))
    for s in (-1, 1):
        g = g.cut(pahli_delik(M3, at).translate((s * 8.0, -8.0, 0)))
    g = g.union(yazi_ust("K5", 4, -7.5, 4.0, at, aci=90)).union(yazi_ust("0.5", 4, 7.5, 4.0, at, aci=90))
    return g


# =====================================================================================================================
# K7 - ince kabuk paneli
# =====================================================================================================================


def K7_panel():
    k = K7
    a, kb, rt, rh = k["A"] / 2, k["KABUK"], k["KABURGA_T"], k["KABURGA_H"]
    g = kutu(-a, a, -a, a, 0, kb)
    z1 = kb + rh
    g = g.union(kutu(-a, a, -a, a, kb - 0.01, z1).cut(kutu(-a + rt, a - rt, -a + rt, a - rt, 0, z1 + 1)))
    for c in (-k["KABURGA_ARALIK"] / 2, k["KABURGA_ARALIK"] / 2):
        g = g.union(kutu(c - rt / 2, c + rt / 2, -a, a, kb - 0.01, z1))
        g = g.union(kutu(-a, a, c - rt / 2, c + rt / 2, kb - 0.01, z1))
    g = g.union(silindir(k["BOSS_D"] / 2, kb - 0.01, kb + k["BOSS_H"]))
    t2 = T.SOMUN["M3"][1] + T.SOMUN_DERIN_PAY
    g = g.cut(somun_tuzagi("M3", z0=kb + k["BOSS_H"] - t2 + 0.01))
    g = g.cut(pahli_delik(M3, kb + k["BOSS_H"]))
    g = g.union(yazi_ust("K7", 5, -20, 20, kb)).union(yazi_ust("1.2", 5, 20, 20, kb))
    g = g.union(yazi_ust("1.6x5", 4, -20, -20, kb))
    return g


# =====================================================================================================================
# donusumler (montaj icin)
# =====================================================================================================================


def Rz(deg):
    a = math.radians(deg)
    M = np.eye(4)
    M[:2, :2] = [[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]]
    return M


def Rx(deg):
    a = math.radians(deg)
    M = np.eye(4)
    M[1:3, 1:3] = [[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]]
    return M


def Ry(deg):
    a = math.radians(deg)
    M = np.eye(4)
    M[0, 0], M[0, 2], M[2, 0], M[2, 2] = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    return M


def Tx(x, y, z):
    M = np.eye(4)
    M[:3, 3] = (x, y, z)
    return M


def Tz(z):
    return Tx(0, 0, z)


def baski_to_montaj(t):
    """Kol baski cercevesi (cep ustte, z 0..t) -> montaj cercevesi (cep yuzu z=0, govde +Z)."""
    return Rx(180) @ Tz(-t)


# =====================================================================================================================
# parca listesi
# =====================================================================================================================

PARCALAR = {
    "K1_tutucu": K1_tutucu,
    "K1_kol": K1_kol,
    **{f"K2_mg_p{p:.1f}": (lambda p=p: _k2_mg(p)) for p in K2_PAYLAR},
    **{f"K2_sg_p{p:.1f}": (lambda p=p: _k2_sg(p)) for p in K2_PAYLAR},
    "K2_pim_sabit": K2_pim_sabit,
    **{f"K2_pim_donen_{c:.1f}": (lambda c=c: _k2_pim_donen(c)) for c in K2_PIM["DELIKLER"]},
    "K3_taban": K3_taban,
    "K3_kizak": K3_kizak,
    "K4_taban": K4_taban,
    "K4_krank": K4_krank,
    "K4_disk": K4_disk,
    **{f"K5_dis_{c:.1f}": (lambda c=c: _k5_tup(K5["DIS_OD"], f"D{c:.1f}")) for c in K5["BOSLUKLAR"]},
    **{f"K5_ic_{c:.1f}": (lambda c=c: _k5_tup(k5_ic_od(c), f"I{c:.1f}")) for c in K5["BOSLUKLAR"]},
    "K5_kama": K5_kama,
    "K5_kardan_dis": lambda: _k5_kardan_tup(K5["DIS_OD"], "D"),
    "K5_kardan_ic": lambda: _k5_kardan_tup(k5_ic_od(K5["KARDAN_BOSLUK"]), "I"),
    "K5_kardan_orta": K5_kardan_orta,
    "K5_kardan_ankraj": K5_kardan_ankraj,
    "K7_panel": K7_panel,
}
ADET = {"K5_kardan_orta": 2, "K5_kardan_ankraj": 2}


def stl_yaz(ad, wp):
    os.makedirs(STL, exist_ok=True)
    yol = os.path.join(STL, f"{ad}.stl")
    cq.exporters.export(wp, yol, tolerance=0.02, angularTolerance=0.15)
    return yol


# =====================================================================================================================
# tabla yerlesimi (raf algoritmasi, 90 deg dondurme)
# =====================================================================================================================


TABLA_GRUP = (("K1", "K2_mg", "K2_pim", "K3"), ("K2_sg", "K4", "K5", "K7"))   # [SECIM] tabla 1 = MG996R/rotil, 2 = SG90/piston/kabuk


def tabla_yerlesim(mesler: dict):
    """Gruplara gore (TABLA_GRUP) ayri ayri yerlestir; bir grup sigmazsa ek tabla acilir."""
    out = []
    for grup in TABLA_GRUP:
        alt = {k: v for k, v in mesler.items() if k.startswith(grup)}
        if alt:
            out += _tabla_yerlesim(alt)
    return out


def _tabla_yerlesim(mesler: dict):
    """{ad: trimesh} -> [[(ad, kopya, trimesh_yerlestirilmis), ...], ...] tablalar. Kullanilabilir alan 220 - 2*kenar."""
    import trimesh
    U = TABLA_XY - 2 * TABLA_KENAR
    g = TABLA_ARALIK
    ogeler = []
    for ad, m in mesler.items():
        for i in range(ADET.get(ad, 1)):
            e = m.bounds[1] - m.bounds[0]
            dondur = e[0] < e[1] and e[1] <= U        # uzun kenar X'e
            ogeler.append((ad, i, m, dondur))

    def boyut(o):
        e = o[2].bounds[1] - o[2].bounds[0]
        return (e[1], e[0]) if o[3] else (e[0], e[1])

    ogeler.sort(key=lambda o: (-boyut(o)[1], -boyut(o)[0]))
    tablalar = []   # her tabla: raflar [(y0, h, x_dolu)]
    yer = []
    for o in ogeler:
        w, h = boyut(o)
        konuldu = False
        for ti, raflar in enumerate(tablalar):
            for r in raflar:
                if r[2] + w <= U + 1e-6 and h <= r[1] + 1e-6:
                    yer.append((ti, o, r[2], r[0])); r[2] += w + g; konuldu = True; break
            if konuldu:
                break
            y_ust = (raflar[-1][0] + raflar[-1][1] + g) if raflar else 0.0
            if y_ust + h <= U + 1e-6:
                raflar.append([y_ust, h, w + g]); yer.append((ti, o, 0.0, y_ust)); konuldu = True; break
        if not konuldu:
            tablalar.append([[0.0, h, w + g]]); yer.append((len(tablalar) - 1, o, 0.0, 0.0))
    sonuc = [[] for _ in tablalar]
    for ti, (ad, i, m, dondur), x, y in yer:
        mm = m.copy()
        if dondur:
            mm.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (0, 0, 1)))
        lo = mm.bounds[0]
        mm.apply_translation((TABLA_KENAR + x - lo[0], TABLA_KENAR + y - lo[1], -lo[2]))
        sonuc[ti].append((ad, i, mm))
    return sonuc


def tablalari_yaz():
    import trimesh
    from checks import geo
    mesler = geo.yukle_stl_klasoru(STL)
    tablalar = tabla_yerlesim(mesler)
    os.makedirs(TABLA, exist_ok=True)
    for f in os.listdir(TABLA):
        if f.startswith("tabla_") and f.endswith(".stl"):
            os.remove(os.path.join(TABLA, f))
    satirlar = []
    for ti, tl in enumerate(tablalar, 1):
        birlesik = trimesh.util.concatenate([m for _, _, m in tl])
        birlesik.export(os.path.join(TABLA, f"tabla_{ti}.stl"))
        lo, hi = birlesik.bounds
        satirlar.append(f"tabla_{ti}: {len(tl)} parca, kapsam {hi[0] - lo[0]:.1f} x {hi[1] - lo[1]:.1f} x {hi[2]:.1f} mm "
                        f"(tabla {TABLA_XY:g}, kenar {TABLA_KENAR:g})")
        for ad, i, m in tl:
            l2, h2 = m.bounds
            satirlar.append(f"   {ad}{'#' + str(i + 1) if ADET.get(ad, 1) > 1 else ''}: x {l2[0]:.1f}..{h2[0]:.1f}  y {l2[1]:.1f}..{h2[1]:.1f}  z {h2[2]:.1f}")
    with open(os.path.join(TABLA, "yerlesim.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(satirlar) + "\n")
    print("\n".join(satirlar))
    return tablalar


def main(argv):
    if "--liste" in argv:
        print("\n".join(PARCALAR)); return
    secili = list(PARCALAR)
    if "--only" in argv:
        secili = argv[argv.index("--only") + 1].split(",")
        bilinmeyen = [s for s in secili if s not in PARCALAR]
        if bilinmeyen:
            raise SystemExit(f"bilinmeyen parca: {bilinmeyen}")
    for ad in secili:
        wp = PARCALAR[ad]()
        v = wp.val()
        print(f"{ad}: gecerli={v.isValid()} hacim={v.Volume() / 1000:.2f} cm3 -> {os.path.basename(stl_yaz(ad, wp))}")
    if "--tablasiz" not in argv:
        tablalari_yaz()


if __name__ == "__main__":
    main(sys.argv[1:])
