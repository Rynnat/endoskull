"""Project Bust CP3b-2 - boyun / egme / yay / piston olculeri. TEK KAYNAK (CP3b-2), birim mm.

Etiketler (params.py ile ayni): [KAYNAK] PLAN/sablon/datasheet | [TAHMIN] olculmeli | [SPEC] PLAN/KARARLAR | [SECIM] tasarim
          [KAGIT] KAGIT_OLCUM.md tasarim degeri (bandin kotu ucu) | [HESAP] _tmp/cp2/*.py betigiyle secildi.
Koordinat: params.py ile ayni (+Y yukari, +Z ileri, +X sol; orijin = U-mafsal merkezi = bas pivotu).
Yaw grubu (N1, N2, egme servolari, kranklar, yay diregi, P1 alt ucu) "yaw cercevesinde" (bas_yaw = 0'da dunya ile ayni).
Project Angela dosyalari KULLANILMADI.
"""
import params as P

# ------------------------------------------------------------------ U-mafsal (N2 catal - N3 hac - B1 roll kulaklari)
HAC = dict(x=14.0, y=10.0, z=11.0)              # N3 yari olculeri; B1 roll kulaklari z +-11.4 [P.RZ_ROLL], catal x +-14.4 [SECIM]
CATAL = dict(x=(14.4, 19.4), z=8.0, y_alt=-26.0, kopru=4.0, ust_r=8.0)   # N2 catal kollari, kopru y -26..-22
HAC_PIM_DERIN = 9.0                              # catal disindan hac icine M4x14 kendinden kilavuzlu (sabit = hac, 3.3 delik) [PLAN I13]
ROLL_PIM = dict(L=40.0, d=4.0)                   # M4x40 Z ekseni, B1 kulaklari + hac, nyloc [PLAN I14, satin]

# ------------------------------------------------------------------ N1 yaw tablasi
N1_Y = (-124.0, -118.0)                          # lazy susan ust halkasi ustu -124 [P.LS]; kalinlik 6 [SECIM]
N1_R = 52.0
N1_CEP = dict(r=18.0, derin=2.0)                 # alttan Y1 cebi
N1_LS_DELIK = [(44.0, 0.0), (0.0, 44.0), (-44.0, 0.0), (0.0, -44.0)]   # I8, oval +-3 teget [KAGIT 10]; K8 ile kesinlesir
N1_KABLO = dict(c=(-20.1, 11.2), r=5.5)          # 8 iletken + 2 egme servo kablosu -> G1 guverte deligi (-18, 10) [SECIM]
OLDHAM = dict(r=11.0, pim_d=4.0, yarik_w=4.4, yarik_L=7.0)   # Y1 pimleri N1 radyal yariklarinda (I7, +-1.5 radyal)

# ------------------------------------------------------------------ Y1 yaw kaplini
Y1 = dict(r=16.0, t=5.0, pim_h=3.0)              # alt yuz = servo mil ucu + MG_KOL Y0 (0.6); ust -122.4

# ------------------------------------------------------------------ N2 boyun kolonu
N2_FLANS = dict(r=25.0, t=4.0, vida_r=20.0)      # I12 4x M3, O40 daire [PLAN]
N2_KOLON = dict(x=11.0, z=(-15.0, 6.0), r_kose=5.0)   # kolon kesiti (yuvarlatilmis dikdortgen)
N2_OMUR = [(-100.0, 17.0), (-82.0, 16.5), (-64.0, 16.0), (-46.0, 15.0)]   # (y, yari en) omur gorunumlu halkalar [SECIM]
N2_OMUR_T = 4.0
N2_KABLO_KANCA = dict(c=(-13.0, -60.0, -12.0))   # kablo kancasi (kolon sol arka) [SECIM]

# ------------------------------------------------------------------ egme servolari (MG996R x2) + N4 krank + pushrod
EGME = dict(x_uc=34.1, y=-92.0, z=-45.0)         # mil ucu (sol +X tarafinda, mil -X'e bakar); govde +Z'ye (one) uzanir [SECIM]
KRANK = dict(r1=22.8, r2=15.2, t=6.0, hub_r=12.5, kol_w=11.0, uc_r=5.5)   # [KAGIT 2] iki delik: 1:1 ve 1.5:1
KRANK_PAYLAR = (0.1, 0.2, 0.3)                   # [KAGIT 3] disk kol cebi varyantlari; varsayilan 0.2
ROTIL_X = 24.1                                   # rotil gozu merkezi |x| (kafa kulagi ic yuzu 27.5 - 0.4 - 3) [SECIM]
ROTIL_KAFA = (-6.0, -26.0)                       # (y, z) [P.RZ_ROTIL dy, z merkezi]
BRAKET = dict(x=(51.3, 55.3), y=(-118.0, -78.0), z=(-64.0, -4.0))   # dik servo braketi (kulaklar ic yuzunde) [SECIM]
N5 = dict(r=5.5, et=1.2, boy=46.0)               # pushrod kilifi (kozmetik "hidrolik"), rod ortasinda [SECIM; PLAN 0.8 -> 1.2 PLA]
EGME_KAPASITE = (2.0, 2.5, 3.5)                  # [KAGIT 1] surekli tork satirlari kg*cm; tasarim 2.5
KRANK_MAKS = 60.0                                # [SPEC PLAN B] krank <= 60 deg zarfi
ROTIL_ACI_MAKS = 25.0                            # [TAHMIN K3] M3 rotil acisal siniri

# ------------------------------------------------------------------ yay (H2, %75 denge) [HESAP _tmp/cp2/tasar.py]
YAY_KAFA = (8.0, -2.0, -54.0)                    # B1 yay kulagi (x 6..10; eski x 0 kulagi roll pimi sokme yolunu kapatiyordu)
YAY_ANKRAJ = (8.0, -45.0, -118.0)                # N1 arka diregi, nominal delik [HESAP _tmp/cp2/yay2.py: gercek AM (3.7, 28.8, 8.8) ile %75'e en yakin]
YAY_DELIKLER = (-18.0, -9.0, 0.0, 9.0, 18.0)      # 5 delik yay hatti boyunca (+ = kafadan uzak, on gerilme artar) [KAGIT 9]
YAY_DIREK = dict(x=(14.0, 18.0), pay=5.0)        # direk yay ekseninin yaninda (S-kanca), deliklerin +-pay mm cevresi
YAY_K = 0.020                                    # N/mm [HESAP, tasarim; K6 olcer]
YAY_LE = 22.8                                    # etkin sifir boy L0 - F0/k (mm) [HESAP]
YAY_L0 = 50.0                                    # serbest boy ust siniri (ornek: F0 = k (L0 - LE) = 0.54 N on gerilme) [TAHMIN K6]
YAY_HEDEF = 0.75                                 # [SPEC KARARLAR H2]
YAY_AYAR = (0.60, 0.95)                          # [KAGIT 1]

# ------------------------------------------------------------------ P1 SCM pistonlari (kozmetik, teleskop + M3 vida-pimli kardan)
P1_UST = (42.0, -4.0, -30.0)                     # mastoid alti, B1 dili pim merkezi (sol; sag ayna) [HESAP _tmp/cp2/scm.py]
P1_ALT = (56.0, -110.0, -98.0)                   # N1 dili pim merkezi (yaw cercevesi)
KARDAN = dict(gap=4.8, ct=2.4, cw=9.0, pin2=4.5, b0=10.3, b1=13.3, pin1=19.1)   # K5 kuponu (kuponlar/build.py K5_kardan_orta)
DIL = dict(w=8.0, t=4.0, h=10.0, pah=2.0, delik=5.0)   # K5 DIL
TUP = dict(od=10.0, et=0.8, bosluk=0.5, varyant=(0.4, 0.5, 0.6))   # [KARARLAR: PLA, 0.5; 0.4/0.6 varyant]
KARDAN_MAKS = 25.0                               # [K5 kuponu: iki eksende +-25]
STROK_PAY = 3.0                                  # [SPEC PLAN 2.1] her uçta >= 3 mm
P1_ODAK = (-2.5, 0.0)                            # kardan notr yonu bu pozda (pitch, roll): eklem acilari aralik ortasinda [SECIM]

# ------------------------------------------------------------------ P2 yanak pistonlari (duzlemsel: iki uc M3 mentese, X ekseni)
# P2 yanak pistonlari: CP3b-2 ikinci yarisinda (STATE_CP3b2.md) - satin.rezerv() yer tutucusu henuz duruyor

# ------------------------------------------------------------------ poz izgarasi / kilit [SPEC PLAN §7]
POZ_YAW = (-70.0, -35.0, 0.0, 35.0, 70.0)
POZ_PITCH = tuple(float(a) for a in range(-25, 21, 5))
POZ_ROLL = (-15.0, 0.0, 15.0)
POZ_CENE = (0.0, 10.0, 20.0)
CENE_BOYUN_PAY = P.CENE_BOYUN_PAY                # 5 mm [SPEC KARARLAR]
ONE_EGILME_HEDEF = 21.0                          # [KARARLAR C] cene kapali >= 21 deg

# ------------------------------------------------------------------ tork girdileri [PLAN 5.2 / KAGIT]
DINAMIK = dict(aci=30.0, sure=0.5)               # 30 deg / 0.5 s [PLAN 5.2]
SURTUNME_PITCH = 0.15                            # kg*cm (SCM 0.12 + rotil) [PLAN 5.2, TAHMIN K5]
KUTLE_ARTI = 1.30                                # +%30 kotu durum [PLAN 5.2]
