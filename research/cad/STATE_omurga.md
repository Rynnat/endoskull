# Omurga revizyonu - DURUM: OMURGA2 kuruldu (2026-10-17 ~21:05)

Angela'ya bakilmadi. Kafa (B*) ve cad_estetik/ dokunulmadi (B1'deki eski yay kulagi duruyor, artik bossta - kafa turu kaldirabilir).
Yedekler: `_tmp/omurga/*_once.py` (omurga oncesi), `*_omurga1.py` (tur 1). Betikler: `_tmp/omurga/` (rx, p1, scan2-7, render, yama*).

## Ne degisti
- **Tur 1 (omurga1):** egme MG996R'lar dik + sirt sirta (mil disari, mil ucu altta), O1L/O1R kasa yarilari (X-yukari basilir, kulaklar M4x14 +
  yan girisli somun, arka duvar + diken). Krankta iceri pim gobegi (rotil x 24.1 sabit), r2 deligi kalkti. N1 sade disk r 48.
- **Tur 2 (omurga2, kullanici: "cok arkadan geliyor"):**
  - **Yay + yay diregi + N1/kasa kancalari KALKTI** (`PB.YAY_VAR = False`). Yaysiz @2.2 kg*cm: nominal 3.44, kutle +%30 **2.70** (hedef 1.5).
  - Servo mil ekseni (y -92, z -45) -> **(y -88, z -40)**: kolona yaklasti + 4 mm yukari; 9 -> 6 deg yatik. Kasa 5 omur bolumu (4 oluk) + 5 diken.
    y -80 denendi: krank B4'e carpip one egilmeyi -22.5'e dusurdu -> geri alindi.
  - P1 alt ucu (60,-106,-95) -> **(70,-108,-86)** (kafatasi arka cizgisi icinde); enine kol y -122..-116 (dil 8 mm; kardan catali kol ustunde).
  - N5 kilif 46 -> 36 (rod 86 -> 82.5).
  - Kasa N1'e 2x M3x12 kendinden kilavuzlu (yari basina); N2 flansina yalniz oturur (omur halkasi dikey takmayi engelliyordu).

## Oncesi / sonrasi
| | omurga oncesi | omurga1 | omurga2 |
|---|---|---|---|
| arka tasma (kafatasi en geri z -94.7 - boyun en geri z; hedef <= 0, ideal <= -40) | **+45** (yay diregi z -140) | +45 | **-2.1** (P1 orta alt z -92.6) |
| tork payi yayli nominal / +%30 (2.0 kg*cm) | 4.07 / 3.05 | ayni | yay yok |
| yaysiz nominal / +%30 @2.2 kg*cm | 3.63* / - | - | **3.44 / 2.70** |
| one egilme (cene kapali, roll 0) | -25 | -25 | **-25** |
| kilit: cene 20 / roll 15 cene 0 / roll 15 cene 20 | -11.9 / -21.9 / -1.9 | ayni | ayni (hizli izgara) |
| N1 hacmi | 97 cm3 | 30.8 | 30.8 (+ O1L/R 35.3 + 35.4) |
| SORUN (tam check) | 29 | 34 | **36** |
*eski raporun 2.0 satirindan olceklendi.

## Kontrol (tam check.py, out/check_report_omurga2.txt): SONUC: SORUN (36); oncesi 29 (out/check_report_oncesi_omurga.txt)
KAPSAM: OLCULDU - tum check.py + check_boyun (poz_kilit tam izgara 610 poz, montaj_sokme_boyun(_tezgah), strok, tork, kablo, devrilme).
OLCULMEDI - muaf ciftler raporda (yeni: O1 x egme servo / N1 / N2 / O1L-O1R / P1 orta alt); kasa M3/M4 alet koridoru; kardan orta alt x O1 dili temasi.
Yeni 7 bulgu: havada_ada O1L/O1R (z 67, 2.6 mm2: P1 dili ucu, X-yukari baskida) 2; et < 1.6 N1 (on yarim ay kenari 0.02) + O1L/O1R (taban/somun yuvasi kenari) 3;
montaj_sokme_boyun +2 (P1 teleskop X yonunde takilirken dis tup x kardan orta alt 1.7 mm3 - eski P1 orta bulgularinin ayni sinifi).
montaj_sokme_boyun_tezgah GECTI. Kilit tablosu oncekiyle ayni (cene 10: -19.1 -> -19.4).

## P1 "on-yana / dik asagi" - UYGULANAMAZ (rakamla), karar kullanicida
Teleskop (bindirme >= 2xOD) + mandibula (B4 >= 5 mm) taramasi, pitch -25..+20 x roll 0/15 x cene 0/10/20:
| alt uc | teleskop | cene kapali one egilme |
|---|---|---|
| (50,-112,42) on-yan | OK | **+5** (hic egilemez) |
| (62,-112,42) on-yan | OK | **+12** |
| (60,-112,-60) dik asagi (tasma ~-35) | **bindirme 6 < 20** | - |
| (70,-108,-86) SECILEN | OK (pay 0.5 mm, tasarim) | -25 |
Secenekler: (1) secilen (kafatasi icinde, -2.1 mm; arkaya egik); (2) P1'i teleskop degil kozmetik orgulu hortum/esnek kilif yapmak
(kulak arkasindan dik asagi, z ~ -40..-55 -> tasma ~ -40, T-800 gibi) - hortum boy degisimini egilerek alir; mandibulaya dokunmaz. Oneri: (2), yeni tur.

## Acik / OLCULMEDI
- Gorsel: 2 tur kullanildi (ref/omurga_*.png tur 1; ref/omurga2_{yan,arka34,on34,karsilastirma}.png tur 2). Siluet: boyun kafatasi
  arka cizgisinin icinde ama referanstaki 40-50 mm ortme yok; P1 hala arkaya egik. 08_yanak_piston_omurga_ref O3'teki 2 kozmetik arka piston
  + orgulu hortum YAPILMADI (butce).
- Kardan orta alt x O1 dili poz_kilit'te muaf (temas); dil 8 mm ile eski bosluk (3.5) korunuyor varsayimi - montaj_sokme olcer.
- Kasa-N1 baglantisi kendinden kilavuzlu PLA (5.5 mm kor); stall'da gobek M3 egilmesi ~358 MPa (celik uygun).
- havada_ada O1 (tur 1'de 2 kucuk ada 1.65 mm2, P1 dili ucu) ve N1/O1 ince et noktalari: tur 1 raporunda; temizlik turuna.
- Satin alma: yay ve S-kanca CIKAR; + M3x35 + nyloc x2 (krank pimi), M3x12 x4 (kasa-N1), M3x16 + somun x2 (yari birlesim), M4 somun x8.
