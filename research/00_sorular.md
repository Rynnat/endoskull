# Project Bust — tasarımdan önce sorular (00)

Tarih: 2026-10-16. Bu bir ön keşif notu: karar yok, tasarım yok. Cevaplar Agent Flow v2'ye (araştırmacı → planlayıcı → cad → denetçi → doğrulayıcı) girdi olacak.

## 1. InMoov "bust" kısa özet
1. **Kapsam:** InMoov'un kendi sayfaları resmî bir "bust" tanımı vermiyor. Toplulukta "bust", bacaksız üst gövde anlamında kullanılıyor: baş + boyun + gövde + omuzlar (genelde kollar ve eller de dahil). Basında da robot "baş, gövde, kollar, eller var; bacak yok" diye anlatılıyor ([Make](https://makezine.com/2015/06/19/in-our-image/), [Register](https://www.theregister.com/2013/01/30/3d_printed_robot/)). Kolsuz versiyon "head + torso" ya da "head + shoulders" diye ayrıca belirtilmeli. **Bunu soru olarak sordum (S1).**
2. **Servolar (resmî varsayılan donanım haritası):** baş için 7 servo: boyun eğme 2× HK15298B (master/slave), baş dönüşü + baş eğme 2× HS-805BB, çene 1× HK15298B, göz X/Y 2× küçük servo. Gövde (topStom/midStom) için 4× HS-805BB sınıfı. Omuz/kol için 8× HS-805BB. Yani baş + gövde + omuz ≈ **19 servo**; ellerle birlikte 31 ([inmoov.fr hardware map](https://inmoov.fr/default-hardware-map/)). HS-805BB büyük bir servo (66×30×57 mm, ~20+ kg·cm).
3. **Ölçek:** 1:1 yetişkin insan boyu. Boyun/çene parçalarının sayısı 19 ([neck & jaw](https://inmoov.fr/build-yours/neck-and-jaw/)), tek omuzun yaklaşık 15 parça tipi var ([shoulder & torso](https://inmoov.fr/shoulder-and-torso/)). Tüm büst için **yüzlerce parça** ve **~300–600 saat baskı** gerekir (tahmin; resmî rakam bulunamadı). Baskı ayarı: %30 dolgu, 2.5 mm duvar, kalibratör parçası.
4. **Görünüm:** beyaz plastik, heykelsi ama mekanik bir robot. Gözlerde kamera, yüz sabit (kaş/dudak yok), sadece çene hareket ediyor. Blender'da yapılmış, yani **STEP dosyası yok**, sadece STL var; parametrik düzenleme zor.
5. **Lisans:** **CC BY-NC** ([inmoov.fr/?p=12](https://inmoov.fr/?p=12)). Ticari olmayan kullanım ve türev iş serbest, ama atıf zorunlu. Satış, para karşılığı stant ya da ticari demo yasak. Bizim CAD hattımız (CadQuery + kontroller) InMoov STL'lerini ölçemez ve doğrulayamaz → S3.

## 2. Yeniden kullanılabilecekler
- **Angela v2 baş + boyun** (`modules/project-angela/v2`): 961 g baş, 3 eksenli "top boyun" (DS3218 ile yaw→roll→pitch), çene (DS3218), göz + kapak + kaş + dudak (Bowden ile 8× MG90S). Kontrolleri temiz (297 poz), `model.html` hazır. **Büstün başı doğrudan bu olabilir.** Ama henüz basılmadı; yazılım kilidi ve Bowden kalibrasyonu doğrulanmadı.
- **Eye v5** (donanımda çalışan tek modül): 3× SG90 + Uno, yüz takibi (`control/face_follow_v2.py`), kalibrasyon paneli. **Fiziksel olarak kilitli.** Söküp kullanmak ancak kullanıcı izin verirse mümkün; yazılımı kopyalanabilir.
- **Tracking Arm sim** (`modules/tracking-arm/v1/sim`): webcam → MediaPipe → eklem açıları → three.js. Büstün omuz/baş taklidi için hazır bir altyapı.
- **Agent Flow altyapısı:** `agent-flow/checks` (çakışma, havada, montaj, tabla, vida/BOM–envanter) ve `sablonlar` (sg90_cebi, somun_tuzagi, …), Angela/Limb `viewer` + `test_harness`.
- **Envanterde serbest olanlar** (`envanter.md`, plan-v2 dalı): **6× MG996R** (~9.4 kg·cm), **~6× SG90**, **2× PCA9685**, **2× 5 V 5 A adaptör**, Arduino Uno klon + Nano, ESP32, 4× 1000 µF, PIR, 3× HC-SR04. Vidalar: M2×8, M3×8/10/14/15 (havşa), M4×8/10, somunlar. **DS3218 ve MG90S yok**, yani Angela v2 başı için ≈ 5000 ₺ servo/parça alımı gerekir (Angela BOM tahmini).

## 3. Kullanıcıya sorular (önem sırasına göre)

**S1. Kapsam: büst neyi içerecek?** *Neden:* servo sayısını, parça sayısını ve taşıyıcı yapıyı birlikte belirler.
- a) Baş + boyun (Angela v2'nin üstüne gövdesiz bir kaide): ~0 yeni tasarım, ~5000 ₺, ~80–120 saat baskı (tahmin).
- b) **Baş + boyun + göğüs/omuz kabuğu (sabit, hareketsiz)**: +1 gövde kabuğu, +~1–1.5 kg filament, +60–100 saat (tahmin), ek servo yok.
- c) b + gövde dönüşü/eğilmesi (1–2 servo): göğüs kabuğuyla başı taşıyan yeni bir gövde ekseni gerekir, +1500–3000 ₺ (tahmin).
- d) c + kollar (InMoov tam büst): +8 büyük servo, +~5000–10000 ₺, aylarca sürer (tahmin).
- *Varsayılan:* **b**.

**S2. Ölçek.** *Neden:* tablaya sığan parça boyutunu, bölme sayısını ve servo sınıfını belirler.
- a) **1:1 insan** (Angela ile uyumlu): omuz genişliği ~400–450 mm, yani göğüs kabuğu tabla için 4–6 parçaya bölünür. Boyun servoları DS3218 sınıfı.
- b) ~%75: göğüs 2–4 parça; baş Angela'dan küçük olacağı için yüz mekanizmaları sığmaz, baş yeniden tasarlanır.
- c) ~%50 masaüstü: MG996R/SG90 ile yapılır, ucuz; ama yüz ifadesi neredeyse imkânsız.
- *Varsayılan:* **a** (Angela başını korumak için).

**S3. InMoov STL'lerini kullanalım mı, sıfırdan mı tasarlayalım?** *Neden:* lisansı ve kontrol hattının çalışıp çalışmayacağını belirler.
- a) InMoov STL'leri doğrudan (CC BY-NC, atıf + ticari değil): CAD'i hızlı biter, ama check.py bu ağları ölçemez. HS-805BB gerekir (~600–900 ₺/adet, tahmin). Görünüm %100 InMoov olur.
- b) **Sadece görsel referans; CadQuery'de sıfırdan tasarım** (InMoov oranları ve hatları): bütün kontroller çalışır, envanterdeki servolar kullanılır, lisans sorunu yok.
- c) Karma: InMoov göğüs/omuz kabuk formu Blender'da yeniden çizilir, mekanik bizim. Lisans açısından türev iş sayılır, atıf gerekir.
- *Varsayılan:* **b**.

**S4. Hareket listesi / servo bütçesi.** *Neden:* iç hacmi ve güç bütçesini belirler (PCA9685 başına 16 kanal, 5 A adaptör).
- a) Minimal: göz (2) + kapak (1) + çene (1) + boyun 2 eksen = 5 servo.
- b) Angela v2'nin tamamı: göz, kapak, kaş, dudak, yanak, çene, boyun 3 eksen ≈ 19 servo (15 MG90S + 4 DS3218).
- c) b + gövde dönüşü (1) + omuz silkme L/R (2) ≈ 22 servo. 2 PCA9685 yeter, ama 5 A'lik adaptörler sınırda (tahmin).
- *Varsayılan:* **b + yalnız gövde dönüşü** (20 servo).

**S5. Görünüm / estetik.**
- a) InMoov tarzı beyaz plastik robot (tek renk, en kolayı).
- b) **Angela gibi insansı yüz + robotik gövde** (ten rengi yüz, gövde gümüş/beyaz kabuk; Limb'deki siyah-gümüş-turuncu paleti olabilir).
- c) Tamamen insansı (gövdede de ten ve kıyafet formu): daha çok renk parçası çıkar.
- d) b + açık panel/şeffaf göğüs (mekanizma görünür): +tasarım yükü, ama demoda etkili.
- *Varsayılan:* **b**.

**S6. "Şaheser"in başarı ölçütü.**
- a) Yalnız simülasyon: tam kontrolü geçmiş `model.html` + render (~1–2 hafta ajan işi, 0 ₺).
- b) a + basılabilir paket (BOM, MONTAJ, tolerans kuponları).
- c) **b + fiziksel baskı ve montaj** (ayların işi, ~5000–8000 ₺; tahmin).
- d) Stant demosu (canlı yüz takibi): c + yazılım.
- *Varsayılan:* **b** (önce b, sonra c'ye karar ver).

**S7. Bütçe / satın alma tavanı.**
- a) 0 ₺: yalnız envanter (6× MG996R + SG90) → hareketler kısıtlı, yüz ifadesi yok.
- b) ~2000 ₺: boyun DS3218'leri + birkaç MG90S.
- c) ~5000 ₺: Angela v2 başının tamamı.
- d) ~8000 ₺+: c + gövde servoları ve filament.
- *Varsayılan:* **b ya da c'yi kullanıcı söylesin.** Yalnız sim seçilirse (S6a/b) para harcanmaz.

**S8. Kontrol ve etkileşim.**
- a) Önceden yazılmış ifade/poz dizileri (en basit).
- b) **Yüz takibi** (Eye v5 `face_follow_v2` yazılımı başa uyarlanır).
- c) b + ses: konuşurken çene senkronu, Angela AI/Spinal Cord bağlantısı.
- d) Tracking Arm gibi webcam ile birebir taklit: kullanıcının başını ve omuzlarını kopyalar.
- *Varsayılan:* **b**, c ve d sonraya.

**S9. Angela v2 başı olduğu gibi mi kullanılsın, büste özel yeniden mi tasarlansın?** *Neden:* boyun kaidesi (`base_tub` 150×150) gövdeye gömülmeli; Angela'nın yaka/boyun parçaları değişir.
- a) Angela v2 dondurulur, büst onun kaidesinin altına eklenir (en hızlı).
- b) **Angela v2 kopyalanıp "Bust v1" içinde boyun-gövde arayüzü yeniden yapılır.**
- c) Yeni bir baş tasarlanır (InMoov yüz hatlarıyla).
- *Varsayılan:* **b**.

**S10. Teslim zamanı.** a) 1 hafta (yalnız sim) b) **2–3 hafta (sim + baskı paketi)** c) stant tarihi (Lunar ~09-23/30 geçti, yeni tarih var mı?). *Varsayılan:* **b**.

## 4. Kullanıcıdan istenecek bilgi/ölçümler
- Eldeki 6 MG996R gerçekten boşta mı (başka projeye takılı değil mi)? SG90 sayısı kesin kaç?
- DS3218 / MG90S satın alınabilir mi, nereden ve hangi fiyata (Angela BOM'u ~5000 ₺ varsayıyor)?
- Filament: hangi renkler ve kaç kg var (ten, beyaz, gümüş, siyah)? PETG var mı?
- Yazıcı hâlâ Ender 3 Neo mu, yeni yazıcı (Centauri Carbon 2) alındı mı? Alındıysa tabla 256 mm ve çok renk baskı her şeyi değiştirir.
- Büstün duracağı yer ve en büyük boyutu (masa mı, stant mı; yükseklik sınırı).
- Eye v5 sökülmeden kalacak mı (varsayılan: evet, kilitli)?
- InMoov'dan beğenilen belirli görseller/parçalar (göğüs plakası, omuz formu, yüz) — ekran görüntüsü ya da link.
