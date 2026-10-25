# ORBITA TURU (2026-10-17, 5. oturum): DURDU (token 120k), 2 yeni SORUN acik

**Yaklasim:** eski huni + kas tupu + alin rafi + frontal zigoma tupu + burun kutusu KALDIRILDI. Ust yuz tek surekli kabuk (`_yuz_kabugu`, 6 satir serit 1.6: alin alti, kas, glabella, burun koku, elmacik, ice cokuk sakak duvari) + kas dolgusu (5 mm). Goz cukurlari loft ile OYULDU (`_orbita_halkalari`: yuzde genis, 5 mm iceride yuvarlanan kenar, 12 mm geride genisleyen, z 66'ya inen 1.6 duvar). Mekanizmayla cakisan her sey `zarf_b2.py` yasak zarfiyla kesilir (81 poz + cene + montaj-sokme supurmeleri + P2, ayrinti DECISIONS).
**Check:** SORUN (23) -> **SORUN (25)**. Goz/kapak 81 poz + cene supurmesi B2 icin 0 bulgu. YENI 2: (1) Z1 tolerans kure<->B2 nominal 1.02 (en kotu 0.17 < 0.4): duzeltme = yuz kabugundan goz merkezli r 13.6 kure cikar (goz her pozda ayni kure). (2) et_yapisal B2 %14.6 (zarf kesiminin egik bicak kenarlari + 1 mm supurme basamaklari): duzeltme onerisi = zarfi daha seyrek/duzgun (hull'lu) supurme ya da kesik kenarlara 1.6 kalinlastirma; olcmeden muaf YAZILMADI.
**Kutle:** B2 35.0 -> 39.35 cm3 (bas ~ 447 + 5.4 g, sinir 500). Tabla: B2 139 x 88 x 77 (220 icinde, bolme yok). Baski yonu ayni (yuz yukari), cukur ici/kas alti agac destek (P.DESTEKLI B2 notu gecerli).
**Gorseller:** `ref/orbita_tur{1,2,3}_{on,3q,yuz}.png` (tur3 = son form; son build'de yalniz derin duvar z 66'da kesildi + zarf 26 yon buyutuldu, gorunus ayni).
**Kalan zayiflik:** cukur TAVANI yok: B5 modulu +Y ile sokuldugu icin goz ustunde B2 malzemesi olamaz; tavan ancak B3'e (once sokulen) eklenirse olur. Ust kenar ince levha kenari gibi; cukur ust-ici zarf kesim basamaklari (cizgili) ve mekanizma gorunuyor. Sakak duvari duz. Kubbe (B3) alt kenari "kask siperi" gibi duruyor (bu turun kapsami disi).
**Hiz:** zarf_b2.py 8 dk; B2 build 15 dk (26 yonlu buyutme cache'lendi, sonraki build hizli); check 22 dk.

# ESTETIK TUR 2 (2026-10-17, 4. oturum): BITTI, mekanizmaya dokunulmadi

**Check:** SORUN (23) -> **SORUN (23)** (yeni bulgu yok). Goz/kapak (81 poz) ve cene supurmesi 0 bulgu. Var olan iki sokme bulgusu hafifledi: B5 grubu x B2 9.0 -> 0.9 mm3; B2 x kamera_rezerv ilk temas 2 -> 5 mm (kalan temas kamera cercevesinin alt penceresi, eski). Bas 446.3 -> 447.0 g / 500.
**Degisen parcalar:** B2 (orbita hunisi, kas cikintisi, alin rafi, burun kemigi, armut kenari + kamera perdesi, ust disler), B4 (yalniz alt disler). lib.py'ye `dis`, `dis_olcu` eklendi. Ayrinti DECISIONS "ESTETIK TUR 2".
**Bulunan hata:** eski `_armut()` poligonu CW oldugu icin armut kenari hic olusmuyordu (duzeltildi). Bu sinif icin genel kontrol (bos CrossSection / beklenen alt govde hacmi 0) YAZILMADI: acik is.
**Gorseller:** `ref/cad_estetik2_on.png`, `_3q.png`, `_yuz.png` (3 bakma turu kullanildi).
**Kalan estetik zayifliklar:** orbita hala belirgin bir cerceve cizgisi gibi okunabiliyor: sakak (yanal duvar) bos, yanal kenar arkasinda kafatasi yuzeyi yok; kas cikintisi iki goz arasinda hala neredeyse duz bir bant; huni ici aydinlik (mekanizma, pivot silindirleri goruluyor, "derin golge" yok, goz parlamasi LED/malzeme isi). Armut perdesi duz plaka gibi duruyor. Sakak duvari icin B5a yan ucu (x 55.7), kapak servolari ve B6 olculup yer acilmali. G1 sternum (madde 4) yapilmadi.

# ESTETIK TUR (2026-10-17, 3. oturum): BITTI, mekanizmaya dokunulmadi

**Check:** SORUN (33) -> **SORUN (23)**. Yeni bulgu yok; goz/kapak (81 poz) ve cene supurmesi 0 bulgu. Kapananlar: G1 x G2L/R, G2 x G4, G2 x lazy susan alt/ust (statik + montaj_sokme_govde G2 adimlari). Bas kutlesi 437.9 -> 446.3 g / 500.
**Degisen parcalar:** B2, B4, G2L, G2R, G1 (yalniz G2 omurga vidasi y -152.5 -> -154.2, somun tuzagi onunla tasindi). Digerleri yeniden uretilmedi.
**Gorseller:** `ref/cad_estetik_3q.png`, `_on.png`, `_yan.png`, `_yuz3q.png` (3 bakma turu kullanildi).
**Kalan estetik zayifliklar:** dis sirasi hala buyuk kutular (konseptle ayni); burun deliginde kamera cercevesinin kare kenari gorunuyor; maksilla plakasinda hull seridi kaynakli hafif fasetler; kas kemeri hala duz tup (sakak cukuru yalniz kemer + dis kenar ile okunuyor); humerus basi kucuk top + kok, konseptteki deltoid kubbesi yok; G1 sternum/manubrium hala kutu (G1'e estetik dokunulmadi).
**Acik hatalar listesi (asagida) gecerli; 1. ve 2. maddelerin G2 kismi kapandi, G1 x hoparlor/kartlar/mg996r_yaw ve montaj hoparlor/mg996r_yaw duruyor.**

# CP3b-1 durum (2026-10-17, 2. oturum): DEVAM EDİYOR, token bütçesi (~180k) doldu

**Durum:** tam tarama (`check.py`, --hizli değil) **SONUC: SORUN (33)**. model.html, Orca dilimleme ve render YAPILMADI (kural: kontroller temiz olmadan görüntüleyici yok; bütçe de bitti).

## Bu oturumda kapananlar (ayrıntı: DECISIONS "CP3b-1 devam")
- Alt kapak bağlantısı: göz ekseninin altına tel kolu eklendi (`ALT_KOL`), servo plakanın altında (ped 7.7), kol r 10. 0..40° kapak tüm pozlarda çözülüyor (servo 0..−44°).
- Göz/kapak süpürmesi (81 poz) ve çene süpürmesi: **0 bulgu** (B1×B3 arka dil, B5e×B1, B5f×direk, yaw kolu×pitch servo, yaw kolu×üst kapak, tel×tel hepsi kapandı).
- B2 tek gövde, havada_ada (destek listesi `params.DESTEKLI`), sg90_yaw/alt sökme, G4L×G4R dil/boss.
- PLAN SAPMASI kamera 32→24 DECISIONS'a yazıldı.

## Açık hatalar (sıradaki oturum, bu sırayla)
1. **cakisma_govde_statik**: G1 × G2L/G2R (1.5 cm³), G1 × hoparlör (0.7 cm³), G1 × kart_uno/pca1/esp32, G1 × mg996r_yaw, G2 × G4 (1.1 cm³), G2 × lazy_susan alt/üst (1.6–1.9 cm³). G2 alt ucu y −248.9, kaide üstü −240'ın altında. `govde.py` G1/G2 yerleşimi yeniden çözülmeli: G2 kaburgaları lazy susan'ın (y −132..−124, Ø100) ve G4'ün dışında kalmalı, G1 kart/hoparlör cepleri satın alınan modellere +0.4.
2. **montaj_sokme_govde**: G2L/R × G4 (1 madde ile aynı), hoparlör × G1 (−X'ten girmiyor), mg996r_yaw × G1.
3. **montaj_sokme_bas**: B2 × kamera_rezerv (B2 +Y'de 2 mm'de kesişiyor; kamera kartı B2'den sonra takılmalı ya da çerçeve açıklığı), B5 grubu × B2 (−Y'de B5d_L × B2 9 mm³), mg996r_cene × B1 (−X 9 mm'de 19.8 mm³), rotil_cene × B4.
4. **giris_yolu**: çene servosu M4 (+X'ten alet) B1 ile 98–144 mm³. Kulak vidaları için duvarda alet kanalı ya da vidaları ters (somun dışta).
5. **tolerans Z2** (üst kapak ↔ halka, en kötü −0.28 < 0.3): UST_RI 15.0 → 15.4 ya da HALKA_GOBEK x bandı 0.4 → 0.8.
6. **et_kabuk_1.2** (B3L/R %2.8–3.3, B5d %3.5–4.7) ve **et_yapisal_1.6** (B1 %8.5, B5a, B5g, G1): kaba ışın örnekleme. En ince noktalar kenar/kaburga uçlarında. Gerçek ince duvarlar ayıklanacak (örn. B1 0.04 @ x 40.9 = B2 kulağı somun kanalı, B5g 0.26 = pres tel deliği kenarı).
7. **B1 kütlesi 54.6 g > 45** (dilimleyici yaklaşımı): plaka 25.7 g, alt kulaklar 16.5 g, çene servo duvarı 6.3 g, PCA plakası 6.8 g. Seçenek: PCA'yı B1 arka direklerine taşıyıp dik plakayı kaldırmak; çene duvarını kafes yapmak.
8. Sonra: tam check TEMİZ → Orca dilimleme (`C:\Users\LENOVO\Projeler\_arsiv\qr-stand\araclar\dilimle.py`, parça başına) → `viewer.py` → `out/model.html` → headless Edge render (en çok 2 tur).

## Hat
`params.py` → `lib.py` → `bas.py` / `yuz_kubbe.py` / `govde.py` / `satin.py` → `kin.py` → `build.py [--only a,b]` → `check.py [--hizli]`. Tanı: `diag.py <parca>`, `carp_diag.py goz_yaw=.. alt=..`, `_tmp/ix.py A B` (iki parçanın kesişim bileşenleri), `_tmp/m.py` (B1 kütlesi), `_tmp/m2.py` (B1 kütle dökümü), `_tmp/pl.py` (B1 plaka kesiti PNG).
Kütle: baş toplamı check_report kutle_butce'de (B1 54.6 g; baş 437.9 g / 500).

## Kullanıcı işi / ölçülemeyen
- Kit SG90 kolu, basılı kolun r + 2 mm ötesinden kesilecek (r < 14 kollar: alt r 10, pitch 12, üst kapaklar 9).
- Kamera rezervi 24×24, 32×32 OV5640 sığmıyor. Kart seçilince bakılacak.
- Mikrofon titreşim izolasyonu, kâğıt değerleri, ağaç destek izleri: baskıda görülecek.
