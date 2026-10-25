"""Project Bust CP3b-1 - torktan bagimsiz parcalar. TEK KAYNAK: tum olculer burada (mm).

Etiketler: [OLCUM] olculmus | [KAYNAK] datasheet/sablon/PLAN | [TAHMIN] olculmeli | [SPEC] PLAN/KARARLAR | [SECIM] tasarim
           [KONSEPT] modules/project-bust/v6/model.html (cm -> mm) | [REZERV] CP3b-2 (boyun/egme/yay/piston) yer tutucusu.
Koordinat (PLAN): +Y yukari, +Z ileri (yuz), +X bustun solu. Orijin = bas pivotu (U-mafsal merkezi), notr pozda.
Bas parcalari bas cercevesinde (notrde dunya ile ayni). Gogus/kaide: konsept dunya (cm) * 10 - (0, 130, -5).
Project Angela dosyalari KULLANILMADI (KARARLAR KESIN KURAL).
"""
import math
import os
import sys

AGENT_FLOW = r"C:\Users\LENOVO\Projeler\epic-project\agent-flow"
if AGENT_FLOW not in sys.path:
    sys.path.insert(0, AGENT_FLOW)
from sablonlar import toleranslar as T  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
STL = os.path.join(OUT, "stl")
RENDER = os.path.join(OUT, "render")

PLA = 1.24                 # g/cm3 [KAYNAK]
TABLA_XY = 220.0           # Ender 3 Neo [SPEC]
KABUK_G_CM2 = 0.22         # [KAGIT_OLCUM 8] kabuk birim kutlesi tasarim (kotu uc), nominal 0.19
DUVAR_E = 1.0              # [TAHMIN] dilimleyici: cevre+ust/alt etkin kalinlik (kutle yaklasimi; Orca ile karsilastirilir)
DOLGU = 0.15               # [SECIM] dolgu orani (Epic POC)
M2, M3, M4 = T.M2_SERBEST, T.M3_SERBEST, T.M4_SERBEST
YATAY = T.YATAY_DELIK_EK
EKS = T.EKSENEL_BOSLUK     # 0.4 [DOGRULANDI]
SOMUN_M2 = (4.0, 1.6)      # [KAYNAK ISO 4032]
KABUK = 1.2                # [SPEC 07 §4] kubbe kabuk
KABURGA_T, KABURGA_H = 1.6, 5.0   # [SPEC]
TEL_D, TEL_DELIK = 1.0, 1.3       # O1 celik tel [SPEC], delik [TAHMIN PLAN I20]

# ------------------------------------------------------------------ kafatasi formu [KONSEPT CR, skullWarp]
SKULL_C = (0.0, 60.0, 4.0)
SKULL_R = (72.0, 74.0, 94.0)
KUBBE_Y_ALT = 46.0         # [SECIM] yan alt kenar (sakak penceresi altinda acik: cene krank/kondil/mikrofon gorunur)
KUBBE_Y_ON = 54.5          # [SECIM] on (z > KUBBE_Z_ON) alt kenar: ust kapak supurmesi (y <= 47.8) + 2 mm
KUBBE_Z_ON = 30.0
KUBBE_ARKA_Z, KUBBE_ARKA_Y = -58.0, 10.0   # [SECIM] arka (oksiput) z < -58'de kabuk y 10'a iner
KUBBE_KABURGA_Y = (75.0, 105.0)            # [SECIM] yatay kaburgalar
KUBBE_KABURGA_Z = (-60.0, -20.0, 20.0, 55.0)   # [SECIM] dikey (koronal) kaburgalar
SAG_FLANS = 3.0            # [SECIM] sagital flans kalinligi (her yarida), x 0..3

# ------------------------------------------------------------------ goz modulu (B5)  [KONSEPT EYE]
GOZ = ((-32.5, 30.0, 77.0), (32.5, 30.0, 77.0))
GOZ_R = 12.0               # [TAHMIN PLAN Z1] O24
IRIS_R, IRIS_T, IRIS_CEP = 5.8, 1.6, 1.0     # [SECIM] ayri renk (prensip 6)
HALKA_RI, HALKA_RO, HALKA_T = 12.6, 14.2, 3.0  # gimbal halkasi (pitch), goz-halka 0.6
HALKA_GOBEK = (12.6, 14.6, 3.5)               # x bandi (goz merkezinden) + gobek yaricapi
UST_RI, UST_RO = 15.0, 16.2                   # ust kapak kabugu (PLA 1.2, PETG YOK)
ALT_RI, ALT_RO = 16.7, 17.9   # ust kapaktan 0.5 radyal (kure tessellation 0.03)
KAPAK_X = 12.0
UST_BANT = (15.02, 16.2)      # yan plaka x bandi (halka gobegi 14.6 + 0.4 eksenel; 0.02 sayisal pay)
ALT_BANT = (16.62, 17.8)             # [SECIM] kapak kabugu |x| <= 12 (yanlarda kol bantlari icin bos)
KAPAK_GOBEK_R = 4.0
UST_ACI = (-5.0, 55.0)     # [SECIM] ust kapak KAPALI acisal araligi (theta = atan2(dy, dz), goz cerceve)
UST_STROK = 60.0           # [KAGIT_OLCUM 6] SG90 kotu uc 0.15 s/60 -> strok <= 60 (PLAN R4 75 idi)
ALT_ACI_ACIK = (-90.0, -45.0)   # alt kapak ACIK araligi; kapanma = +ALT_STROK (yukari)
ALT_STROK = 40.0           # [SPEC] <= 40
CERCEVE_X = (18.22, 21.22)   # dis plaka bandi (goz merkezinden)
GOZ_ESIK = 0.4
PIM_M3_BOY = 8.0           # dis pim M3x8 (uc halka gobeginde, goze 1.2)
ORTA_BLOK = dict(x=14.25, y=(24.0, 36.0), z=(71.0, 81.0))
ORTA_SAP = dict(x=(6.0, 10.0), z_on=(76.0, 80.0), y_alt=(2.0, 6.0), dus_x=(32.0, 36.0), dus_z=(55.0, 59.0))
PITCH_BAR = dict(r=19.0, th=133.0, kal=2.0)    # halkalari birlestiren rijit cubuk (ic gobek bandi), O4
ALT_BAR = dict(r=19.0, th_acik=-160.0, kal=2.0)  # alt kapaklari birlestiren cubuk (alt kapak ic kol bandi)
ALT_KOL = dict(r=11.0, th_acik=-118.0, x=-13.2, w=2.0, ru=2.6)   # alt cubuk uzerinde tel kolu: goz ekseninin altinda, hareket ~+Z (SG90 kolu XZ duzleminde)
YAW_KOL = (0.0, 6.0, -18.0)                    # goz uzerinde yaw kolu tel deligi (goz yerel)
UST_KOL = dict(r=6.0, r2=5.0, th_acik=120.0)  # ust kapak kolu: servo kolu r 9 -> 1.5x (r 6.0) + 1.8x (r 5.0) iki delik [KAGIT_OLCUM 6, K4]
GOZ_YAW, GOZ_PITCH = 32.0, 24.0                # [SPEC]

# SG90 x5 (I16): mil (x, z), kulak alt yuzu y (ped), kol yonu (xz birim), kol r. Govde: mile yakin uc ARKADA.
SG = {
    "yaw":   dict(mil=(0.0, 37.0), ped=15.0, yon=(0.0, 1.0), r=21.0),
    "pitch": dict(mil=(20.5, 30.0), ped=24.0, yon=(-1.0, 0.0), r=12.0),
    "alt":   dict(mil=(-22.34, 33.0), ped=7.7, yon=(0.914, -0.407), r=10.0),   # CP3b-1 devam: kol -24 deg (strok ortasi +X)
    "ustL":  dict(mil=(-37.0, 14.0), ped=18.0, yon=(-1.0, 0.0), r=9.0),
    "ustR":  dict(mil=(37.0, 14.0), ped=18.0, yon=(1.0, 0.0), r=9.0),
}
SG_KOL_T = 3.0             # basili kol kalinligi (kit kolu cebinde, K2)
SG_KOL_PAY = 0.2           # [TASLAK -> K2]
KIT_KOL_UC = 2.0           # kit kolu basili kol deliginin r + 2.0 mm otesinde KESILIR (r < 14 kollar) [SECIM]

# ------------------------------------------------------------------ B1 sasi
B1_Y = (15.0, 18.0)        # taban plakasi (U-mafsal hac supurmesi y <= 14.2 [REZERV hesap])
B1_DIS = [(-44, -42), (44, -42), (44, 3), (56.6, 3), (56.6, 34), (54, 34), (54, 59),
          (-54, 59), (-54, 34), (-56.6, 34), (-56.6, 3), (-44, 3)]
B1_ARKA_YAN = (24.0, 51.0, -58.0, -42.0)   # arka direk tabani (her iki yan, ayna)
B1_ARKA = (-24.0, 24.0, -59.0, -42.0)   # arka dil (x0 x1 z0 z1)
ASKI = dict(x=(51.6, 56.6), z=(2.0, 18.0), y=(-4.0, B1_Y[1]))   # kondil askisi (sabit, M4 somun ic yuzde)
KONDIL = (0.0, 3.0, 10.0)  # [KONSEPT jawG] cene ekseni X
CENE_TAB_X = (57.0, 61.0)  # donen (vida_pim M4: sabit 5 + 0.4 + donen 4)
PCA_DIK = dict(z=(-59.0, -56.0), x=24.0, y=(B1_Y[0], 60.0))     # PCA#2 dik plaka
PCA = dict(w=62.5, h=25.4, t=1.6, delik=(56.0, 19.0), z=-65.0, yc=44.0, ayak=6.0)   # [KAYNAK Adafruit PCA9685]
B2_KULAK = dict(x=(38.0, 52.0), y=(4.0, B1_Y[0]), z=(47.0, 55.0), delik_x=(41.5, 48.5), delik_z=51.0, somun_y=9.0)
B2_TAB_Y = (0.0, 3.6)        # B2 tablari kulaklarin ALTINDA, vida alttan (+Y) - PLAN SAPMASI (DECISIONS)
B3_DIREK = {"on": dict(x=(48.6, 54.0), z=(18.0, 24.0)), "arka": dict(x=(42.0, 48.0), z=(-58.0, -52.0))}
B3_DIREK_UST = 46.0
B3_VIDA_Y = 43.0           # yatay M3 (X ekseni) yandan, sakak penceresinden
B3_ARKA = dict(x=(14.0, 22.0), y=(16.0, 21.0), z=(-60.0, -56.0), vida_y=18.5)
MIK_KOL = dict(z=(-48.0, -40.0), x=(44.0, 50.0))
# REZERV CP3b-2 (basit kulak; olcu PLAN §3/R1)
RZ_ROLL = dict(z=(11.4, 16.4), x=8.0, y=(-8.0, B1_Y[0]))   # N3 hac roll pimi (Z) kafa kulaklari
RZ_ROTIL = dict(x=(27.5, 32.5), z=(-30.0, -22.0), y=(-10.0, B1_Y[0]), dy=-6.0)
RZ_YAY = dict(x=4.0, z=(-56.0, -52.0), y=(-6.0, B1_Y[0]))

# ------------------------------------------------------------------ cene servosu (MG996R, I21) + C1 + rod
MG = dict(L=40.7, W=19.7, N=10.2, Z_ALT=-42.9, Z_UST=-7.0, BOSS_R=6.75, Z_BOSS=-4.0, SPL_R=2.95,
          KULAK_BOY=54.0, KULAK_Z0=-17.2, KULAK_T=2.5, KULAK_DX=24.5, KULAK_DY=5.0, KULAK_DELIK=4.5)   # [TAHMIN K1]
CENE_SERVO = dict(mil_x=48.0, y=36.0, z=-20.0)   # mil +X, govde -Z'ye uzanir
CENE_DUVAR_T = 4.0
MG_CEP_PAY = 0.3           # [KAGIT_OLCUM 11] govde +0.3 (en/boy)
MG_KOL_DISK = dict(Y0=0.6, T=2.0, R=10.5)        # servo_kolu.MG_KOL
C1 = dict(r=20.0, t=6.0, w=12.0, psi0=70.0)      # krank r 20 [SPEC], notr: asagidan 70 deg ileri (rod ~dikey, olu noktadan uzak)
CENE_KOL = (-12.0, -16.0)    # B4 uzerinde rotil pimi (kondile gore dy, dz) r ~20 [SPEC]
ROTIL = dict(GOZ_D=10.0, GOZ_T=6.0, GOVDE_D=5.5, GOVDE_L=12.0)   # [TAHMIN K3]
ROTIL_X = 58.0
CENE_LEVER_X = (61.4, 65.4)
CENE_ACI = 20.0            # [SPEC] 0..20

# ------------------------------------------------------------------ mikrofon (INMP441) + kamera rezervi
MIK = dict(c=(57.0, 14.0, -44.0), od=24.0, boy=10.0, kart=(14.0, 14.0, 1.6), kopuk=1.5)   # kart [TAHMIN]
KAMERA = dict(c=(0.0, -0.5, 84.6), w=24.0, t=1.6, lens=(8.0, 4.0), delik=20.0)   # OV5640 [TAHMIN 13]

# ------------------------------------------------------------------ gogus / kaide (dunya)
KAIDE = dict(a=170.0, b=90.0, y=(-254.0, -240.0), zc=-1.0, duvar=2.4, ust=2.0)
LS = dict(od=100.0, id=56.0, h=8.0, delik_r=44.0, y_alt=-132.0, oval=3.0)   # lazy susan [TAHMIN K8], delikler oval +-3 [KAGIT_OLCUM 10]
GUVERTE = dict(r=50.0, y=(-137.0, -132.0))
YAW_SERVO = dict(mil_y=-128.0)          # MG996R mil +Y, eksen (0, 0) [REZERV mekanik Y1 CP3b-2]
HOPARLOR = dict(c=(0.0, -160.0, 45.0), d=40.0, boy=20.0)   # 4 cm 3 W [TAHMIN §13]
KART_TABLA = dict(z=(-10.0, -7.0), x=44.0, y=(-238.0, -174.0))
KARTLAR = {   # (w, h, t) [TAHMIN]; konum: kart merkezi (x, y), yuz (+1 on / -1 arka)
    "uno": dict(boy=(68.6, 53.4, 1.6), c=(0.0, -206.0), yuz=-1, ayak=6.0),
    "pca1": dict(boy=(62.5, 25.4, 1.6), c=(0.0, -192.0), yuz=1, ayak=5.0),
    "esp32": dict(boy=(55.0, 28.0, 1.6), c=(-8.0, -222.0), yuz=1, ayak=5.0),
    "max98357": dict(boy=(18.0, 18.0, 1.6), c=(33.0, -222.0), yuz=1, ayak=5.0),
}
KABLO_8 = dict(boy=420.0, servis=60.0)   # [SPEC §13] 8 iletken, I2S <= 40 cm (+servis)

# ------------------------------------------------------------------ destek karari [SECIM] (DECISIONS 'Destek listesi')
DESTEKLI = {
    "B1": "alt yuze sarkan kulaklar (aski, B2 kulagi, REZERV kulaklar), tabla yuzunde degil",
    "B2": "kas kemeri / burun koprusu / dis sirasi yuzden sarkar; organik form, yon degisimi adayi yok",
    "B3L": "kabuk ici kaburga uclari", "B3R": "kabuk ici kaburga uclari",
    "B4": "cene kolu ucu", "B5a": "goz pivot diskleri plakadan sarkar",
    "B5d_L": "kapak kabugu tesselasyon kenari (0.05 mm2)", "B5d_R": "kapak kabugu tesselasyon kenari (0.05 mm2)",
    "B5g_L": "pitch kulagi halka duzleminin ustunde", "B5g_R": "pitch kulagi halka duzleminin ustunde",
    "G1": "omur / kart tablasi cikintilari", "G2L": "kaburga uclari", "G2R": "kaburga uclari",
}

# ------------------------------------------------------------------ pozlar / esikler
POZ_MIN_BOSLUK = 0.4
CENE_BOYUN_PAY = 5.0       # [SPEC KARARLAR] - CP3b-2'de olculur
HEDEF_KUTLE = 500.0
KUTLE_BUTCE = {"B3L": 55, "B3R": 55, "B2": 75, "B4": 45, "B1": 40, "B5": 40}   # [SPEC PLAN 5.1] (g)
SATIN_KUTLE = {   # bas uzerindeki satin alinan / ertelenen (g) [KAYNAK PLAN 5.1]
    "SG90 x5": 45.0, "cene MG996R + C1": 60.0, "PCA#2": 10.0, "vida+somun": 22.0, "kablo+LED": 15.0,
    "rotil kafa ucu x2 [REZERV]": 6.0, "yay kafa ucu [REZERV]": 3.0, "SCM piston yarisi x2 [REZERV]": 8.0,
    "yanak pistonu x2 [REZERV]": 6.0, "ses: 2x INMP441 + kablo": 5.0, "sahte detay (kabuga entegre, CAD'de)": 0.0,
}
