# CP3b-2 durum: BITTI (P2 haric), 2026-10-17

B2/B3/yuz_kubbe.py'ye DOKUNULMADI (paralel goz cukuru ajani). bas.py degismedi (B1 boyun.B1_boyun ile sarildi).

## Dosyalar
- `params_boyun.py` (TEK KAYNAK), `boyun.py` (parcalar + kinematik + `poz(p)`), `check_boyun.py` (CP3b-2 kontrolleri; check.py main bunu cagirir; tek basina `check_boyun.py [--hizli]` -> out/check_report_boyun.txt).
- build.py: N1, N2, N3, N4_L/R, N5, Y1, P1_orta, P1_dis, P1_ic; B1 = boyun.B1_boyun. `--varyant` -> out/stl_varyant (N4 pay 0.1/0.3, P1_ic bosluk 0.4/0.6).
- check.py: kutle yalniz bas gruplari (N parcalari HARIC), REZERV satin satirlari -> gercek kalemler (rotil 2x 9 g, yay yarisi 3, roll pimi 6, P1 ust yarisi 2x); et kontrolunden P1 tup / N5 cikarildi (OLCULMEDI); ertelenen blok -> check_boyun.kontroller(); plan_sapma 4 yeni satir.
- satin.rezerv(): yalniz P2. onizleme.py: boyun pozlu.
- agent-flow/checks: strok.py, diferansiyel_tork.py, poz_kilit.py [TASLAK] + test_bust_cp3b2_ekleri.py (BASARILI). test_regresyon BASARILI.
- Gorseller: ref/boyun_adim1_yan.png, boyun_adim1_arka3q.png (ara), boyun_adim2_arka.png, boyun_adim2_yan.png, boyun_adim2_on3q.png (2 gorsel tur kullanildi).

## Sonuclar (CP3b-2 kontrolleri)
- Tork (en kotu servo payi, pitch -25..+20 x roll +-15, dinamik 30 deg/0.5 s + surtunme 0.15):
  yayli nominal 2.0/2.5/3.5 -> 4.07 / 5.09 / 7.12; yayli +%30 -> 3.05 / 3.82 / 5.34; yaysiz -> 3.30 / 4.13 / 5.78.
  Bas 469 g, AM (3.8, 28.8, 8.8): plan tahmininden (one 19.8) cok geride -> yercekimi torku kucuk (0.94 kg*cm @ -25), bas +17 deg'de dengede.
- Yay: oran 0.77 (sapma 0.033 kg*cm), 5 delik 0.56..0.97 (KAGIT %60-95 kapsar). Yay boyu 55..113, kuvvet 0.6..1.8 N, k 0.020 N/mm, L0 <= 50.
- Strok: krank r 22.8 en cok 50.5 deg (<= 60); rotil ust 16.6 / alt 1.6 deg; P1 pim1-pim1 86.2..120.7 (izin 85.7..129.5); kardan pim1 +-18.7 (K5 +-25).
  1.5:1 deligi firmware zarfi (izinli roll): -25: +-2, -20: +-7.5, -15: +-13, >= -10: +-15.
- poz_kilit tam izgara (yaw 5 x roll 3 x cene 3 x pitch 10 + ikiye bolme = 610 poz): yaw'dan bagimsiz. Kilit tablosu (pitch alt siniri):
  roll 0: cene 0 -> -25 (kilit yok), cene 10 -> -19.1 (B4 x N1), cene 20 -> -11.9 (B4 x N2)
  roll +-15: cene 0 -> -21.9, cene 10 -> -11.6, cene 20 -> -1.9 (B4 x N2, 5 mm kurali)
  Ust sinir her yerde +20. **One egilme (cene kapali) 25 deg** (spec siniri; KARARLAR >= 21 saglandi).
- Kablo: 8 iletken yol 272..323 + servis 60 = 383 / 420; egme servo kablolari 247 / 600. Devrilme: en kotu 87 mm, 29.8 deg.
- montaj_sokme_boyun_tezgah GECTI; montaj_sokme_boyun: 4 bulgu kaldi - P1 kardan ortasi dile DOGRUSAL takilamiyor (orta yerel Y boyunca 4-24 mm'de 0.7-1.3 mm3 gecici surtunme; asagi/yukari ve +-Z yollari da 0.6-3 mm3). Fiziksel montajda egerek takilir (K5 kuponu boyle takildi); duzeltme: dil ucuna pah ya da yanak araligi 4.8 -> 5.2 (K5 varyanti).
- Kutle: bas 468.8 g / 500 (pay 31 g).

## Acik isler (sonraki)
1. **P2 yanak pistonlari kurulmadi** (PLAN SAPMASI, DECISIONS): B2 serbest kalinca plan yerinden (B2 kulagi -> B4), iki uc X ekseni mentese (duzlemsel; kardan gerekmez). Kutle PLAN tahmini 6 g.
2. Roll 15 + cene acik pozlarda one egilme cok kisitli (-1.9): firmware tablosu yeterli; istenirse N2 catal kollarini (x 14.4..19.4) daraltmak icin N3'u kucultmek.
3. N1 97 cm3 (yaw grubu, bas butcesi disi) - hafifletme yapilmadi.
4. Lazy susan delik deseni / ust halka somun erisimi K8'e bagli (OLCULMEDI).
5. CP3b-1'den kalan (bu ajanin kapsami degil): G1 x hoparlor/kartlar/yaw servo, Z1/Z2 tolerans, cene servo M4 alet yolu, B2 x kamera, et bulgulari (B1, B2, B5g, G1).

## Satin alma farki (PLAN 11'e gore)
- M4x40: 4 yerine 1 (roll pimi). M4x14: +2 (pitch saplamalari). M4 nyloc: +3. M3x14 + nyloc: P1 kardan 8 pim. MG996R egme kulak: 8x M4x14 (PLAN M4x20 yerine yeterli: kulak 2.5 + braket 4 + somun 3.2).
- Yay: k ~0.02 N/mm, serbest boy <= 50, uzama >= 63 mm (K6). Rotil 4 (boyun) + 2 (cene).
