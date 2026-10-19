# CP3b-1 kararları (2026-10-17)

Kaynaklar: PLAN.md (onaylı), KARARLAR.md, KAGIT_OLCUM.md (kupon yerine kâğıt değer, kötü uç), konsept v6 (model.html, yalnız koordinat/form). Project Angela dosyalarına bakılmadı.

## Genel yaklaşım
- Organik formlar (kafatası kabuğu, tüpler, kaburgalar) manifold3d ile kuruldu (konsept `skullWarp` aynen Python'a taşındı). Mekanik arayüzler (SG90 cebi, somun tuzağı, vida-pim, kol cepleri) agent-flow/sablonlar'dan CadQuery kesicisi olarak alındı. Alternatif: tamamen CadQuery. Organik yüzeyde loft/sweep hem yavaş hem kırılgan olurdu, o yüzden seçilmedi.
- Kabuk kütlesi KAGIT_OLCUM 8'deki kötü uç değeriyle hesaplandı: 0.22 g/cm² × dış alan. Diğer basılı parçalar için dilimleyici yaklaşımı kullanıldı (çevre 1.0 mm + %15 dolgu). Tartıyla doğrulanmadı.
- Üst kapak stroku ≤ 60° ve kapak kolunda 1.5× (r 8) ile 1.8× (r 6.67) iki delik: KAGIT_OLCUM 6.
- MG996R cebi +0.3, kol cebi 0.2, M3 vida-pim 3.3: KAGIT_OLCUM 3, 4, 11.

## PLAN SAPMASI: ust kapak stroku 75 -> 60
Neden: KAGIT_OLCUM 6'da SG90'ın kötü uç hızı 0.15 s/60°. 1.5× bağlantıyla 60° kapak için servo 40° döner, bu da ~100 ms eder. 75° ile 100 ms tutmuyordu. Alternatif 1.8× deliği daha hızlı ama torku daha düşük; ikisi de modelde.

## PLAN SAPMASI: kapak malzemesi PETG 0.8 -> PLA 1.2
Neden: KARARLAR'da "PETG YOK" var. PLA'da 0.8 mm kabuk 2 çevreye düşüyor ve kırılgan oluyor, o yüzden 1.2 mm (3 çevre) seçildi. Kapak başına ~1 g ek kütle çıktı.

## PLAN SAPMASI: goz yaw pimi M3 vida-pim -> O1 tel pim
Neden: göz yaw ekseni gimbal halkasının üst ve alt noktasında. Halka radyal 1.6 mm (r 12.6..14.2) ve üst kapağın iç yarıçapı 15.0, yani M3 kafası (1.9 mm) ya da somunu sığmıyor. Halka O1.0 deliğe pres O1 çelik tel (BOM'daki tel), göz O1.3 delikte dönüyor. Pitch ekseni M3 olarak kaldı (dışta M3x10 vida-pim, içte M3 dişli çubuk). Alternatif olarak halkanın dışına yoke konabilirdi, ama kapak süpürmesine giriyordu.

## PLAN SAPMASI: ust kapak pivotu iki yan -> tek yan (dis)
Neden: iç bantta (göz merkezinden 12.6–14.6 mm) halkayı pitch çubuğuna bağlayan kulak var. Bu kulak θ 109–157° aralığında süpürüyor; üst kapağın iç yan plakası açıkken aynı bölgeye giriyordu. Üst kapak yalnız dış yanda pivotlu. Kabuk 1.2 mm, kapak ~1 g; konsol açıklığı 24 mm. Alt kapak iki yanda pivotlu.

## PLAN SAPMASI: B2 vidalari onden 4x M3 -> alttan 4x M3
Neden: önden (−Z) girecek alet yolunu elmacık ve göz modülü kapatıyor. B1'in iki alt kulağına (x ±38..52) 2'şer M3 alttan (+Y) giriyor, somun yan kanallı. Bunun için montaj sırası değişti (aşağıya bakın).

## PLAN SAPMASI: montaj sirasi B2, B4'ten once
Neden: B2 vidaları alttan giriyor ve çene takılıyken alet yolu dar kalıyor. Baş tezgâh montajı: B1 → SG90×5 → çene MG996R → PCA#2 → mikrofonlar → kamera rezervi → **B2 (alttan, +Y)** → B5 göz modülü (−Y) → SG90 kolları → **B4 (alttan, +Y)** → C1 + rod → B3R (+X) → B3L (−X). Kontrol: montaj_sokme_bas.

## PLAN SAPMASI: kubbe sagital bindirme + 6x M3 her yari -> bindirme dili vidasiz + 3x M3 B1'e
Neden: sagital dikişteki iç vidalara iki yarı kapandıktan sonra erişilemiyor. B3L'de 6 mm × 1.6 mm bindirme dili var ve B3R'nin altına giriyor. Her yarı B1'e 3 vidayla bağlanıyor: 2 yandan (X ekseni, şakak penceresinden; vida başı dışta "cıvata" görünümü veriyor) ve 1 arkadan (Z). Toplam 6 vida, plandaki 12 yerine.

## PLAN SAPMASI: mikrofon yeri kabuk deligi 12 mm -> sakak penceresinde ayri kap
Neden: kubbenin yan alt kenarı y 46'da bitiyor. Bunun altı şakak penceresi; çene krankı, kondil ve rod görünür kalıyor (Terminatör iskelet görünümü). Kulak hizasındaki mikrofon bu açık bölgede, B6 kabının içinde duruyor. Kart köpük (EVA 1.5) içinde yüzüyor, kap B1 koluna köpük conta + 2× M2 ile bağlı. Dış yüzde O1.5 delikli ızgara var. Titreşim yolu: B1 → conta → kap → köpük → kart. Ölçülmedi.

## PLAN SAPMASI: cene servosu yonu konsept mil Y -> mil X
Neden: konseptte çene servosunun mili Y'deydi; krank XZ düzleminde dönüyor, kondil kolu ise YZ'de hareket ediyordu, ikisi uyuşmuyordu. Mil +X'e çevrildi: B1'in +X yan duvarına 4× M4 kulak (PLAN I21), krank r 20 (Ç1) YZ düzleminde, rod 2 rotil ile kondilin arkasındaki kola (r ~20) bağlı. Servo konumu PLAN'daki yer (pivotun arkası, z −10..−50, y 34..54). R1'i önlemek için konseptten ~10 mm yukarı alındı; rotil REZERV kulakları (x ±27.5..32.5, y < 15) servonun altında kaldı.

## PLAN SAPMASI: lazy susan 100-120 -> 100 OD [TAHMIN]
Neden: köprücük iç ucu (x ±18..70) güverte kenarına yaklaşıyor. Ø100 ile 2 mm pay kalıyor. Delikler oval (±3 mm, KAGIT 10). K8 ölçülünce güncellenir.

## Diğer tasarım seçimleri (sapma değil)
- SG90'ların mile yakın ucu (kablo) arkaya bakıyor. Kollar tel yönüne göre seçildi: yaw +Z r 18 (iki göz, iki tel tek delikte), pitch −X r 12 → pitch çubuğu, alt kapak +X r 12 → alt çubuk, üst kapaklar dışa r 12. Kol katmanları farklı yükseklikte (ped 12/18/24), böylece teller ve kollar birbirini kesmiyor.
- Göz modülü: kapak/halka/plaka x bantları (göz merkezinden): halka göbeği 12.6–14.6, üst kapak 15.0–16.2, alt kapak 16.6–17.8, çerçeve 18.2–21.2. Bantlar arasında 0.4 eksenel pay var. Kapak kabukları |x| ≤ 12'de, yani eksen etrafında süpürmede birbirine giremiyor.
- B3 kubbe alt kenarı: önde y 50 (üst kapak süpürmesi en çok y 47.8), yanlarda 46, arkada (z < −58) 10.
- REZERV (CP3b-2): B1'de roll pimi kulakları (Z, y 0), rotil kulakları (X, y −6), yay kancası (z −64) yalnız yer tutucu. U-haç süpürmesi y ≤ 14.2 hesabıyla B1 tabanı y 15..18'de.
- Kozmetik detay (cıvata başı, sırt, oluk) kabuğa entegre. Kütle bütçesinde ayrı satır yok, CAD hacminde var.

# CP3b-1 devam (2026-10-17, 2. oturum)

## PLAN SAPMASI: kamera rezervi 32x32 -> 24x24
Neden: göz çukuru kenarı ile maksilla arasında ~25 mm yer var, 32×32 OV5640 kartı sığmıyor. B2 kamera çerçevesi 24×24 kart için (M2 ×2, lens Ø8). Kart seçilince yeniden bakılacak (STATE: kullanıcı işi).

## Alt kapak bağlantısı yeniden düzenlendi (sapma değil: servo ve kapak plandaki gibi)
Sorun: tel noktası θ −160'taydı ve kapak kapanırken orada çoğunlukla −Y yönünde hareket ediyor. Dikey milli SG90 kolu ise XZ düzleminde dönüyor; 20°'nin üstünde tel boyu tutmadı.
Çözüm: alt çubuğa göz ekseninin altında bir tel kolu eklendi (`ALT_KOL`: r 11, θ −118 → −78, x −13.2, orta blok ile alt kapak iç bandı arasında). Bu nokta kapanırken ~+Z yönünde 7.5 mm ilerliyor. Servo plakanın altına alındı (ped 28.7 → 7.7, alçak ped kodu yaw ile aynı), kol r 14 → 10, nötrde −24°. Tel neredeyse yatay (y 23 → 20). Tel yaw tellerinin (y ≥ 27) altından geçiyor ve yaw kolunun |x| ≤ 12.1 süpürmesinin dışında kalıyor. Kapak 0..40° için servo 0..−44° dönüyor, doğrusal ve her pozda çözülüyor.
Alternatifler: (a) önceki aday, yani mil (−31.3, 40) ve r 16: sol üst kapak servosu ile çakışıyordu. (b) X milli yatay servo (paralel düzlemde 4-çubuk): yeni bir B1 braketi gerektiriyordu, seçilmedi.

## Süpürme çakışmaları için yerleşim kaydırmaları
- Üst kapak kapalı aralığının üst kenarı 60 → 55 (kabuk ve yan köprü). Yaw −32/pitch −24 pozunda göz yaw kolu, kapağın arka kenarına 2° giriyordu.
- Pitch servosu mil x 18 → 20.5 (pitch çubuğu tel kulağı x 8.5): yaw kolu, ±27° süpürmede pitch servo gövdesine giriyordu.
- Üst kapak servoları mil x ±38 → ±37: kolun ucu (r 9 + 2.6) B3 ön direğine 0.3 mm yaklaşıyordu.
- B1 ön kenarında |x| 14..16.6, z 54..60 bölgesine çentik açıldı: alt kapak iç kolu kapanırken plakanın ön kenarına iniyordu.
- B3 kenar kaburgasında B1'in arka plakası, arka dili ve arka direk tabanı için (+0.4) boşluk bırakıldı: B1 × B3 arka dil kesişimi 8 mm³'tü.
- Alçak pedli SG90 (yaw, alt) için plaka açıklığı yerel x −11.5 → −12.6: kablo çıkışı çıkıntısı yukarı sökmede plakaya takılıyordu.

## B2 tek gövde
Burun köprüsü, kaş kemerine ve armut kenarına 8 mm genişliğinde iki blokla bağlandı. Kamera çerçevesi zaten bağlıydı; ayrık gövde köprüydü.

## G4 bindirme dili
Boss, dilin üstünde (aynı Y bandında) yer alıyordu ve G4L × G4R kesişimi 1.5 cm³'tü. Boss dilin ALTINA taşındı (tek blok, iki vida, kendi yarısının z ±50 kaburgasına bağlı). Somun tuzağı boss tabanında. Orta bölgede (|x| < 12.4) kaburgalar dilin 0.4 altına kadar boşaltıldı. Dilin kökü kendi üst plakasına bağlandı.

## Destek listesi (havada ada kararı)
Aşağıdaki parçalar ağaç destekle basılacak, ada bulgusu not olarak raporlanıyor (`params.DESTEKLI`). Diğer bütün parçalar desteksiz ve adasız.
B1 (alt kulaklar), B2 (kemer/köprü/diş sırası), B3L/B3R (kaburga uçları), B4 (çene kolu ucu), B5a (pivot diskleri), B5d_L/R (0.05 mm² tesselasyon kenarı), B5g_L/R (pitch kulağı), G1 (omur/kart tablası çıkıntıları), G2L/G2R (kaburga uçları). Yön değişimi denenmedi: organik formlarda tek düz taban yok.

## B1 hafifletme (yarım)
Plakada açgözlü daire delik yerleşimi kullanıldı (delik + 2 mm et halkası, hiçbir özelliğe ve kenarın 2.5 mm içine girmiyor) ve PCA dik plakasına 40×22 pencere açıldı. Sonuç 58.4 → 54.6 g (dilimleyici yaklaşımı), hedef ≤ 45 g'a ulaşılamadı. Bu kütle modelinde ince levhanın kütlesi yüzey alanıyla orantılı. Kalan 25.7 g plakada; ön/yan bölgeler servo cepleri, kulaklar ve REZERV yük yolu (roll/rotil kulakları) ile dolu. Açık iş (STATE).

# ESTETIK TUR (2026-10-17, 3. oturum)

Amac: CAD v7, onayli konsept v6'dan uzaklasmisti (alt yuz kova, cene silindir, kaburga boru, omuz yarim kure). Mekanizma, servo/tel/eklem yerleri, arayuzler ve CP3b-2 rezervleri degismedi. Kontrol hatti ayni (check.py).
- **lib.serit / lib.yassi_tup:** kemik plakasi (2x2 nokta hucresinde kure zarfi) ve stadyum kesitli yassi kemik cubugu. Yalniz proje yerelinde, CadQuery kesicisi olmadigi icin sablonlar'a eklenmedi.
- **B2:** maksilla kovasi (silindir kabuk) kaldirildi. Yerine alveol kenarindan (R 39.5, disle hizali) goz cukuru tabanina, armut acikligina ve elmacige uzanan 2.8 mm kemik plakasi geldi: 5 satir, kopek disi cikintisi, kopek cukuru (ice 4.2) ve sahte civatalar. Elmacik elipsoidi yerine yassi zigoma govdesi + cikinti, kemer yassi kesitli (9 -> 6.5 x 4.4 -> 3.4). Glabella eklendi. Kamera cercevesi maksillaya iki blokla baglandi (tek govde). B2 tab baglanti cubugu yanak pistonu rezervinin (P2) disina alindi; eski B2 x P2 kesisimi 204 mm3 iken simdi 0. Plaka ust kenari B5e/B5a'nin altinda ve onunde (z >= 86.5) kaldi, boylece B5 yukari sokulebiliyor.
- **B4:** silindir cene ucu ve r 5 boru alt kenar kaldirildi. Yerine sunlar geldi: mandibula govde plakasi (dis kavsi -> ramus, 2.8), kalin alt kenar (r 4.2 -> 2.8), gonial aci cikintisi, ramus plakasi (x 59, t 3; sigmoid centik, koronoid), dis egik cizgi, alt alveol kenari, simfiz sirti, ucgen mental cikinti. Kondil dili, vida-pim, rotil kolu, disler ve diseti aynen kaldi (Z6 degismedi). Arka govde yolu P2 piston alt ucundan >= 1.4 mm uzakta.
- **G2:** boru halkalar yerine yassi kaburgalar geldi (8 x 4 -> 5 x 3; arka aci, kosto-kondral eklem, kikirdak). Kaburga baslari omurlar arasindaki bosluklarda (y -154 / -173 / -193.5), on uclar manubrium ve sternum tablarinda. Koprucuk hafif S, yassilasan kesitli. Yarim kure yerine yatay yassi akromiona donen spina, acik kabuk humerus basi, buyuk yumru ve kesik kol koku (alti civatali halka) kondu. Trapez plakasi ve kablo demeti guverte/lazy susan R 50'nin disinda (+ demet kelepcesi). Butun G2 y >= -220, yani G4 ustunde. Hacim 112.6 -> 48.4 cm3.
- **G2_VIDA omurga y -152.5 -> -154.2, tab yuksekligi 12 -> 8 (sapma degil, ic arayuz):** eski tab, G1 yaw servo tasiyicisinin arka duvarina (y >= -149.2) giriyordu. Yeni tab, tasiyici (-149.2) ile omur (-159) arasinda 0.8 / 1 mm pay birakiyor. G1 somun tuzagi ayni sabitten tasindi. Manubrium tabi z >= 45.4 (hoparlor plakasi), sternum tabi z <= 58.2 (G1 sirtlari).
- Tabla 220 icinde kaldi, yeni parca bolmesi yok.

# ESTETIK TUR 2 (2026-10-17, 4. oturum): "gozluk gibi" duzeltmesi, mekanizmaya dokunulmadi

Degisen parcalar yalniz **B2** ve **B4** (B4'te yalniz disler). Kontrol hatti ayni.
- **Orbita (B2 `_orbita`)**: yuvarlak tup dikdortgen cerceveler, aradaki "kopru" ve duz kas tupu kaldirildi. Yerine her goz icin `serit` ile 3 satirli huni (ic kenar -> icbukey orta satir -> dis kenar), kalinlik 2.2 (kenar yaricapi 1.1, tup degil). Ic kenar duzlemsel yaricap yanal 19.0 / ust 17.5 / burun 17.5 / alt 21.0, z = E_z + 10.5 - |cos u|; dis kenar ic kenardan yalniz 3..8 mm buyuk ama 4..10 mm onde (dik duvar, golgede). Ust kenar: dis kenar boyunca yassi kas cikintisi (6.5 x 4.2, one 1.6 tasar) glabellaya iner. Ic kenar burun kemigine (ust dar / alt genis hull, eski kutu yerine) kaynar; iki goz arasinda ayri cubuk yok. Dis kenar yassi zigoma cikintisi (x 55.5..57.5, onceki x 60..62.5 / z 72'den one alindi) elmacik govdesine iner, alt kenar maksilla ust kenarina oturur. Alin rafi (serit, y 51.5..53, |x| <= 44) kasin ustunden B3 on alt kenarinin (y 54.5) altina gecer (B3 olcumu cache'ten).
  Boyutlandirma: once ic kenar 18/17.5 yanal denendi -> alt kapak (B5e) kapali pozda yanal x 50.3, z 85'te 0.36 mm (< 0.4) -> yanal 19.0. Ilk denemede yanal dis kenar z 80 -> B2 x B5a yan ucu (x 55.7, z 80..81.5) 8 mm3 -> z 86 + orta satir yanalda geri itilmez. 16 uc poz (yaw +-32, pitch +-24, ust 0/60, alt 0/40) carp_diag ile 0 bulgu; tam tarama check.py'de.
- **Armut acikligi (bulunan hata)**: `_armut()` poligonu saat yonundeydi; manifold `CrossSection` bunu bos alan sayiyor, yani eski armut kenari HIC olusmuyordu (kamera cercevesinin kare kenarinin gorunme sebebi). Nokta sirasi ters cevrildi (CCW). Kenar mercegin onune alindi (z 90.6..94.5; arkada kalsaydi B2 +Y sokmede mercege 5 mm sonra degiyordu, ilk tam taramada goruldu); icinde ayni duzlemde 1.8 mm perde (1.2 iken et_yapisal B2 bulgusu verdi), mercege r 8 yuvarlak pencere (70 deg varsayilan gorus konisi mercek onunden 1.5 mm'de r 5.1, 24x24 rezerv aynen). Perde mercegin ONUNDE -> B2 +Y sokmede mercege degmez (mevcut B2 x kamera_rezerv 2 mm bulgusu cerceveden, degismedi).
  Hata sinifi ("CW poligon -> bos kesit, parca sessizce yok") icin genel kontrol eklenmedi (butce); STATE'te acik is.
- **Disler (lib.dis / dis_olcu)**: 14 kutu -> tek tek insan disi: orta 2 kesici (yassi, keski uc), yan kesici, kopek (sivri tek tepe, tam boy), 2 kucuk azi (iki tepecik), 2 azi (kare, dort tepecik). Her dis eski kutusunun ICINDE (ayni aci, ayni uc yuksekligi, genislik 5.0..6.4 -> aralarda >= 0.6 bosluk; kesici/azi uc 1.2..1.4 kisa, kopek dislerin uzun gorunmesi icin). Alt sira ayni fonksiyon, uc +Y; kutu zarfinin icinde kaldigi icin cene supurmesi ve kapanis hizasi degismedi.
- lib.dis/serit/yassi_tup manifold tabanli, sablonlar CadQuery tabanli -> sablonlar'a eklenmedi (estetik tur 1 ile ayni gerekce).
- Kutle: B2 40.7 -> 35.0 cm3, B4 40.2 -> 38.1 cm3 (bas hafifledi).

# CP3b-2 (2026-10-17, boyun mekanizmasi) - ara

Kaynaklar: PLAN §2 N1-N5/Y1/P1, §3, §5, §6, KARAR H2 + 1:1 (+ 1.5:1 ikinci delik), C (tek pivot), KAGIT_OLCUM tasarim degerleri. Angela'ya bakilmadi.
- **PLAN SAPMASI: pitch pimi 1x M4x40 -> 2x M4x14 saplama.** Neden: roll (Z) ve pitch (X) eksenleri U-mafsal merkezinde kesisiyor, iki tam boy pim ayni noktadan gecemez. Roll B1'deki hazir Z deligiyle M4x40 (nyloc); pitch iki yandan catal disindan hac icine 3.3 kendinden kilavuzlu (PLAN I13 "sabit 3.3 dis acar"). Alternatif (eksenleri 8 mm kaydirmak) kinematigi ve B1 rezervini degistirirdi.
- **Egme servolari mil iceri, govde one:** mil disari bakarsa iki govde ortada (x -23..13) cakisiyor. Mil iceri -> govde x 41..77. Govde arkaya uzansaydi P1'in gececegi arka bolgeyi kapatiyordu.
- **Krank delikleri:** r 22.8 ve 15.2, kafa rotili ikisinin orta noktasi (r 19) uzerinde -> iki delikte rod boyu ayni (KAGIT 2 "rod boyu ikisinde de ayni"). Kafa rotili kulagin IC yuzunde (x 24.1): dis yuzde (x 36) roll kolu buyuyor, -25/15'te krank 66 deg (> 60).
- **Yay ankraji pivotun dik altinda (0, -80, -62):** sifir boylu yay dengesine yakin; %75 orani -25..+20 boyunca 0.74-0.80 (tasar.py). Direk yay ekseninin yaninda (x 6..9), S-kanca: direk yay hattinda olsaydi alt deliklerde yay direge sürtünürdü.
- **PLAN SAPMASI: P1 SCM yeri plan (+-55, -10, -20) -> mastoid alti (+-42, -4, -30) -> N1 arka kolu (+-56, -110, -98).** Plan yeri (+-55, -10, -20) bas -25'te gonion'a (58, -54, -25) 4 mm yaklasiyor (piston r 5) ve K5 kardan yigini (2 x 22.6) ile 40 mm strokta bindirme 8 mm kaliyor. Arkaya egik uzun piston: strok 33.6, bindirme 31.3. Kardan pim ekseni ortalama yone dik X bileseni (K5 +-25 siniri pim1'de: +-18.7).
- **PLAN SAPMASI: N5 kilif et 0.8 -> 1.2.** Neden: PLA 0.8 iki cevre (KARARLAR PETG YOK; kapak karariyla ayni gerekce).
- **P2 henuz kurulmadi** (STATE_CP3b2 madde 5); satin.rezerv'de yer tutucu olarak duruyor.


## ORBITA TURU (2026-10-17): oyulmus goz cukuru (kullanici: "gozluk takiyor gibi")
- Kok neden: eklenen halka/huni, arkasinda ve yaninda yuzey yok. Cozum: ust yuz tek surekli kabuk (`_YUZ` satir tablosu, `serit` 1.6), cukurlar boolean ile oyulur (`_loft` bukey halka zarflari). Eski `_orb_ic`, `_orbita`, alin rafi, frontal zigoma `yassi_tup`, burun koprusu ust kutusu silindi. Kenar = oyugun kenari (ekli tup YOK; tur 1'de denenen supraorbital/yanal tup gozluk cercevesi gibi okundugu icin tur 2'de kaldirildi).
- Mekanizma sabit: yeni kabuk `zarf_b2.py` yasak zarfindan cikarilir. Zarf = 81 goz/kapak pozu + cene 0..CENE_ACI (5 deg adim) hareketli gruplar + montaj-sokme supurmeleri (B2 -Y cikar -> digerleri +Y 50 mm/1 mm adim; B3 +-X 40; B4/C1/rod -Y) + P2 rezervi; 6 eksen x 0.6 + yuz bolgesinde 26 yon x 0.45 buyutme. Sadece eksen buyutmesi kosegen yuzeylerde 0.35 kalip B2 x B5e 0.000 mm (411 bulgu) verdi -> 26 yon eklendi. Zarf kesiminden kopan adaciklar atilir (build ciktisinda listelenir, en buyugu ~180 mm3).
- Sonuc: cukur tavani B2'de olamaz (B5 +Y sokulur). Derin duvar z 66'da biter.
- Acik: Z1 (kure<->B2 1.02 nominal) ve et_yapisal B2 %14.6 -> STATE.

# CP3b-2 devam (2026-10-17)
- **Yay yeniden konumlandi (gercek AM ile):** CAD bas AM (3.7, 28.8, 8.8) planin (19.8 one) cok gerisinde; bas +17 deg'de kendiliginden dengede. Pivotun dik altindaki ankraj %75'i tutturamiyordu (oran -3..+7). En kucuk kareler taramasi (_tmp/cp2/yay2.py): kafa kulagi (8, -2, -54), ankraj (8, -45, -118), k 0.020 N/mm, etkin sifir boy 22.8 -> oran 0.77, en buyuk sapma 0.033 kg*cm. 5 delik yay hatti boyunca 9 mm arayla (on gerilme ayari): oran 0.57..0.96 (KAGIT %60-95 kapsar).
- **Yay kulagi x 0 -> x 8 (B1_boyun icinde eski kulak kesildi):** roll pimi M4x40 arkadan (+Z) takiliyor (onde sg90_yaw govdesi var); x 0 kulagi pim yolunu kapatiyordu (montaj_sokme ile bulundu).
- **Egme servo montaji:** servo ortadan asagi indirilip disari (+-X) kaydirilir (kulaklar braket ic yuzunde) - N2'den ONCE. Krank asagi + 8 mm yana. Rod grubu (iki rotil + rod + kilif) bastan ONCE kranka takilir, bas indirilince ust rotil vidalanir.
- **Braket arka kosegeni kaldirildi, braket z -64'e kadar:** P1 dis tupu pitch +13 / roll 15'te 0.11 mm yaklasiyordu (poz_kilit buldu).
- **PLAN SAPMASI: P2 yanak pistonu bu turda kurulmadi.** Neden: plan ust ucu B2'de; B2 paralel ajanin calisma alaninda (dokunma yasagi). B1'e baglanan duzlemsel varyant mandibula govdesinin (x 50-57, y -40..-60) icinden geciyor, disindan gecen varyant (x >= 60) icin B4'e yeni kulak + B2 elmacik olcusu gerekiyor. B2 serbest kalinca plan yerinden (B2 kulagi -> B4) mentese uclu (duzlemsel hareket, kardan gerekmez; strok ~10, bindirme yeterli - hesap STATE_CP3b2). Yer tutucu satin.rezerv'de, kutle PLAN tahmini (6 g).
- Yeni check'lerin kendi testi: `checks/test_bust_cp3b2_ekleri.py` (strok 65>60 ve cozumsuz poz yakalanir; diferansiyel J^-T dogrulanir ve pay 1.25 < 1.5 yakalanir; poz_kilit bilinen engelde alt siniri bulur ve hedef ihlalini yakalar).

# CP3b-2 plan sapmalari (baslik bicimi; gerekceler yukaridaki "CP3b-2" bolumlerinde)
## PLAN SAPMASI: pitch pimi 1x M4x40 -> 2x M4x14 saplama
Neden: roll (Z) ve pitch (X) eksenleri U-mafsal merkezinde kesisiyor; roll M4x40 B1 kulaklari + hactan geciyor, pitch iki yandan catal disindan hac icine 3.3 kendinden kilavuzlu (PLAN I13).
## PLAN SAPMASI: P1 SCM yeri (+-55, -10, -20) -> mastoid alti (+-42, -4, -30) -> N1 arka kolu
Neden: plan yeri bas -25'te gonion'a 4 mm (piston r 5) ve K5 kardan yigini ile bindirme 8 mm; yeni yerde strok 34.5, bindirme 31, kardan pim1 +-18.7.
## PLAN SAPMASI: N5 kilif et 0.8 -> 1.2
Neden: PETG yok; PLA 0.8 iki cevre (kapak karari ile ayni).
## PLAN SAPMASI: P2 yanak pistonu kurulmadi (B2 kilitli)
Neden: ust ucu B2'de; B2 paralel ajanin alani. B1'e baglanan varyant mandibula govdesinden geciyor. B2 serbest kalinca mentese uclu duzlemsel P2 (STATE_CP3b2 acik is 1).

# OMURGA REVIZYONU (2026-10-17) - tasarim karari, kod bekliyor (STATE_omurga.md)
- Egme servolari dik + sirt sirta (mil disari, mil ucu altta, 9 deg geri yatik), mil ekseni (y -92, z -45) ve rotil x 24.1 AYNI -> kinematik/tork degismez.
  Krankta iceri uzanan pim gobegi; rotil disarida (x 41.4) rotil ust 27.9 > 25 verdigi icin reddedildi (_tmp/omurga/rx.py).
- PLAN SAPMASI (oneri): krank r2 (1.5:1) deligi kalkar - r 15.2'de gobek servo govdesine girer; r1 ile en kotu pay 3.05 >= 1.5.
- PLAN SAPMASI (kullanici karari gerekli): P1 alt ucu one-yana tasinamaz. On alt uclar (z >= 30) bas -25'te B4'e -4.4..-4.9 mm giriyor,
  yan/on-yan (z -25..10) teleskop bindirmesi negatif (_tmp/omurga/scan2.py, scan3.py). Oneri: (60,-112,-90) kasa enine cikintisi.

# OMURGA1 + OMURGA2 uygulandi (2026-10-17, ayrinti STATE_omurga.md)
- Kullanici (a) karari: P1 alt ucu kasa enine kolunda. OMURGA2'de (70,-108,-86) (kafatasi arka cizgisi z -94.7 icinde).
- PLAN SAPMASI: yay (H2 %75) KALKTI. Kanit: yaysiz +%30 kutle @2.2 kg*cm en kotu pay 2.70 >= 1.5 (check_boyun tork).
- PLAN SAPMASI: egme mil ekseni (y -92, z -45) -> (y -88, z -40); y -80 krank x B4 kilidi (-22.5) verdi.
- P1 on/dik-asagi alt uc teleskopla uygulanamaz (on: one egilme +5/+12; dik asagi: bindirme 6 < 20) -> kozmetik hortum onerisi kullaniciya.
