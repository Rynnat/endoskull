"""Project Bust CP3a - olcum kuponlari parametreleri (PLAN.md §8). Tek kaynak: tum sayilar burada.

Etiketler: [OLCUM] kumpasla olculmus | [KAYNAK] datasheet/sablon | [TAHMIN] olculmeli (OLCUM_FORMU.md 0. adim) |
           [SPEC] PLAN/KARARLAR | [SECIM] tasarim secimi.
Toleranslar agent-flow/sablonlar/toleranslar.py'den gelir (DOGRULANDI olanlar); burada yalniz kupona ozel sayilar var.
Project Angela dosyalari KULLANILMADI (KARARLAR.md KESIN KURAL).
"""
import os
import sys

AGENT_FLOW = r"C:\Users\LENOVO\Projeler\epic-project\agent-flow"
if AGENT_FLOW not in sys.path:
    sys.path.insert(0, AGENT_FLOW)

from sablonlar import toleranslar as T  # noqa: E402
from sablonlar.servo_kolu import MG_KOL, SG_KOL  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
STL = os.path.join(OUT, "stl")
TABLA = os.path.join(OUT, "tabla")
RENDER = os.path.join(OUT, "render")

# ---------------- genel ----------------
ETIKET_H = 0.6            # [SECIM] kabartma yazi yuksekligi (3 katman @0.2)
ETIKET_OYMA = 0.4         # [SECIM] oyma derinligi (yalniz kardan dili ve kadran cizgileri)
M3 = T.M3_SERBEST         # 3.3 [DOGRULANDI]
M4 = T.M4_SERBEST
M2 = T.M2_SERBEST         # 2.3 [TASLAK]
YATAY = T.YATAY_DELIK_EK  # +0.2 [TASLAK]
SOMUN_M2 = (4.0, 1.6)     # [KAYNAK ISO 4032] AF, kalinlik - M2 somun envanterde TEYITSIZ (PLAN §12-4)
PLA_YOGUNLUK = 1.24       # g/cm3 [KAYNAK 07 §]
TABLA_XY = 220.0          # Ender 3 Neo [SPEC]
TABLA_KENAR = 5.0         # [SECIM] tabla kenar payi
TABLA_ARALIK = 4.0        # [SECIM] parcalar arasi

# ---------------- MG996R (satin alinan, envanter) ----------------
# Servo-yerel "mil ucu" cercevesi (servo_kolu.MG_KOL ile ayni): mil +Z, z=0 mil ucu; govde boyu +X (mile UZAK uc +X).
MG = dict(L=40.7, W=19.7,            # [TAHMIN datasheet -> OLCUM_FORMU 0. adim]
          N=10.2,                    # mil ekseni -> mile yakin govde ucu [TAHMIN]
          Z_ALT=-42.9,               # govde alti (mil ucuna gore) [TAHMIN]
          Z_UST=-7.0,                # kasa ustu [TAHMIN]
          BOSS_R=6.75, Z_BOSS=-4.0, SPL_R=2.95,
          KULAK_BOY=54.0, KULAK_Z0=-17.2, KULAK_T=2.5,   # kulak alt yuzu mil ucundan 17.2 asagida [TAHMIN]
          KULAK_DX=24.5, KULAK_DY=5.0, KULAK_DELIK=4.5)   # delik: govde merkezinden boy +-24.5, en +-5 [TAHMIN]
MG_PENCERE_PAY = (0.2, 0.4)   # (en, boy) [SECIM] sg90 cebiyle ayni mantik (en +0.2, boy +0.4)

# ---------------- K1 MG996R tork + bosluk tutucusu ----------------
K1 = dict(DUVAR_T=4.0,        # [SECIM] kulaklar arka yuze oturur; M3x10/14 sigar (4+2.5+2.4+0.5 = 9.4)
          MIL_Z=70.0,         # [SECIM] mil ekseni yuksekligi (tabladan)
          TABAN_T=4.0, TABAN_Y=40.0, RAY_Y=14.0,   # servo plakasi altinda taban (isgence/agirlik), kiris altinda ray
          X0=-45.0, PLAKA_X1=25.0, X1=120.0, DUVAR_Z=92.0,
          HAFIF=(-40.0, -16.0, 9.0, 44.0),          # servo plakasinda hafifletme penceresi (x0 x1 z0 z1)
          KIRIS_Z=(33.0, 56.0), DIREK_X=(110.0, 116.0), ARA_DIREK_X=(50.0, 72.0, 92.0),
          GUSSET_X=(-43.0, 23.0, 113.0), GUSSET_T=4.0, GUSSET_Y=30.0, GUSSET_Z=50.0,
          YARIK=1.5,          # kulak deligi uzun delik +-1.5 (kulak araligi [TAHMIN] -> 46..52 kabul)
          CIKINTI_X=(50.0, 110.0),  # olcu cikintilari (kumpasla bosluk) - K2 MG kolu 50, K1 kolu 110
          CIKINTI_BOSLUK=8.0,  # kol alt kenari -> cikinti ustu (2 deg sarkma 110'da 3.8 mm; 8 mm = 4 deg durdurucu)
          CIKINTI_Y=-19.0, CIKINTI_W=6.0,
          KADRAN_R=(29.0, 33.0, 36.0),   # kisa / uzun cizgi ic-dis yaricap, uzun cizgi
          KADRAN_ACI=30, KADRAN_ADIM=2)
K1_KOL = dict(T=6.0, W=12.0, HUB_R=14.0, BOY=114.0, KUYRUK=27.0,
              DELIKLER=(20.0, 40.0, 60.0, 80.0, 100.0), ASKI_D=4.0,   # ip/S kanca deligi
              ERISIM_D=7.0,     # kit merkez vidasi erisim deligi
              CEP_PAY=0.2)      # [TASLAK] servo_kolu varsayilani; K2 sonucu bunu degistirir (OLCUM_FORMU K1 notu)

# ---------------- K2 kol cebi + donen M3 eklem ----------------
K2_PAYLAR = (0.1, 0.2, 0.3)
K2_KOL_BOY = 50.0             # [SPEC] olcum noktasi / agirlik deligi kol merkezinden 50 mm
K2_MG = dict(T=6.0, W=12.0, HUB_R=14.0, UC=56.0)
K2_SG = dict(T=5.0, W=8.0, HUB_R=7.5, UC=55.0, ERISIM_D=6.0)
K2_PIM = dict(SABIT=(20.0, 20.0, 5.0), DONEN=(40.0, 12.0, 4.0), DELIKLER=(3.3, 3.4), OLCU_R=30.0)

# ---------------- K3 rotil / pushrod ----------------
# M3 metal rotil (satin alinacak). Model [TAHMIN]: goz tipi (bilye delikli), M3 disi govde.
ROTIL = dict(GOZ_D=10.0, GOZ_T=6.0, GOVDE_D=5.5, GOVDE_L=12.0, MERKEZ_GOVDE=6.0)
K3 = dict(TABAN=(-10.0, 126.0, -12.0, 13.0, 4.0),   # x0 x1 y0 y1 kalinlik
          DIREK=(14.0, 14.0), DIREK_UST=14.0,       # direk/kizak ustu z (rotil buraya oturur)
          SOMUN_UST=11.4,                            # alttan gomulu somun cebinin tavani z (M3x14 hesabi)
          ROD=90.0,                                  # [SPEC] rotil merkezleri arasi
          KANAL_X=(70.0, 126.0), KANAL_BOSLUK=0.4, KANAL_DUVAR=3.0, KANAL_Z=12.0,
          KIZAK=(20.0, 16.0, 10.0),
          ACI_PLAKA=(9.0, 2.4, 56.0, 58.0),          # y0, kalinlik, x boyu, ust z
          ACILAR=(0, 5, 10, 15, 20, 25, 30, 35, 40, 45))

# ---------------- K4 SG90 kapak hizi (1.5x baglanti) ----------------
K4 = dict(TABAN=(-30.0, 58.0, -68.0, 12.0, 2.5),     # x0 x1 y0 y1 t
          BLOK=(-15.0, 24.0, -10.0, 10.0),            # SG90 cebi blogu (ust z = kulak oturma 15.6)
          R1=12.0, R2=8.0,                            # krank / disk tel deligi yaricapi -> oran 1.5 [SPEC]
          L_BAG=40.0,                                 # baglanti (tel) boyu
          DISK_R=20.0, DISK_T=1.6, DISK_ALT=29.4,     # disk z 29.4..31.0 (krank ile ayni seviye)
          DIREK_D=10.0, DIREK_UST=29.0,
          TEL_DELIK=1.3,                              # [TAHMIN PLAN I20] O1 tel / atas
          KRANK_T=4.0, KRANK_W=7.0,
          SERVO_STROK=50.0,                           # [SPEC] servo 50 deg -> kapak ~75 deg
          GOSTERGE_R=23.0, OLCU_DIREK=(50.0, -12.0))  # K2 SG kolu oynama direği (yuz y = -12)

# ---------------- K5 teleskopik piston (PLA) ----------------
K5 = dict(DIS_OD=10.0, ET=0.8, BOY=70.0, KAPAK=1.2, BOSLUKLAR=(0.4, 0.5, 0.6),   # [SPEC KARARLAR: PLA, 0.4/0.5/0.6]
          FLANS=(-7.0, 19.0, -7.0, 7.0, 1.6), HAVA_D=2.0,
          KAMA_ACI=10.0, KAMA=(34.0, 34.0, 3.0),
          KARDAN_BOSLUK=0.5,                         # [SECIM] orta deger; secim K5 cifti sonucuna gore
          DIL=(8.0, 4.0, 10.0), DIL_PAH=2.0, DIL_DELIK_Z=5.0, OMUZ=3.5,
          CATAL_T=2.4, CATAL_W=9.0, EKSENEL=T.EKSENEL_BOSLUK,
          ANKRAJ=(24.0, 24.0, 4.0))

# ---------------- K7 ince kabuk paneli ----------------
K7 = dict(A=60.0, KABUK=1.2, KABURGA_T=1.6, KABURGA_H=5.0, KABURGA_ARALIK=20.0,   # [SPEC 07 §4]
          BOSS_D=10.0, BOSS_H=5.0)   # boss kabuk ic yuzunden 5 mm (toplam 6.2 >= 5 [SPEC 07: boss >= 5 mm])

# ---------------- vida envanteri (PLAN §11) ----------------
ENVANTER = {"M2": (8.0,), "M3": (8.0, 10.0, 14.0), "M4": (8.0, 10.0)}
SATIN = {"M3": (20.0, 25.0), "M4": (20.0, 40.0)}
