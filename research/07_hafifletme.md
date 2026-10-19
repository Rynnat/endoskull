# 07: Hareketli kütleyi en aza indirme (CP1.5)

Tarih: 2026-10-16 · Aşama 0 ek turu · Araştırmacı ajan · Karar yok, seçenek ve tek öneri var.
Envanter okundu: `Rynnat/agentic-mechanism-design@plan-v2/envanter.md` (MG996R 55 g, SG90 ~6 boşta, PCA9685 ×2).
Ölçülmüş değer: `cq-ders/bilesenler.json` dosyasında yalnız SG90 ölçüleri ve M3/M4 var, **kütle ölçümü yok**. MG996R hiç ölçülmedi.
Project Angela dosyalarına bakılmadı (KARARLAR.md). Web araması 15/15 kullanıldı.
Hesap betiği: `kutle.py` (bu klasörde).

## 0. Project Eye dersi (elde ölçülmüş tek veri)
Eye v5'in pitch ekseninde 2026-10-01'de CAD hesabı yapıldı (memory `epic-project.md`). Dönen kütle **~225 g**, ağırlık merkezi eksenin **~23 mm gerisinde**, statik tork **~0.5 kg·cm**. SG90 sürekli 1.2 kg·cm kabul edilirse kağıt üstünde pay **~2.3** çıkıyor. Buna rağmen servo aşağı bakarken zorlandı ve "çok az hareket etti". O sırada güç de sorunluydu (USB 5 V, brown-out).
**Sonuç:** kağıt üstündeki 1.5 payı bu ekipte yetmedi. Bu notta pitch için hedef **≥3 (nominal)** öneriliyor. MG996R ölçülene kadar bu bir tasarım tamponu.

## 1. Kafa kütle bütçesi (S1)
Koordinat: orijin P2 pivotu (kafatası tabanı), x ileri, z yukarı, mm. Hepsi **(tahmin)**, CAD kütlesi gelince güncellenir.
Kaynaklı birim değerler:
- SG90 9 g ([datasheet](https://www.brain.rcast.u-tokyo.ac.jp/aad/wp-content/uploads/2024/12/SG90_a.pdf))
- MG996R 55 g (envanter; [Kiwi](https://www.kiwi-electronics.com/en/mg996r-180-digital-metal-gear-servo-11kg-cm-55g-3020))
- PCA9685 5.5–12 g ([grobotronics](https://grobotronics.com/16-channel-12-bit-pwm-servo-driver-pca9685.html?sl=en), [direnc.net](https://www.direnc.net/pca9685-16-kanal-12-bit-pwmservo-i2c-surucu-modul-en))
- PLA 1.24 g/cm³
- Çelik vida ve somun (hesap, ρ = 7.85): M3×14 + somun 1.5 g, M3×8 + somun 1.2 g, M2×8 + somun 0.46 g

| Kalem | BAZ: S1 naif (2.5 mm duvar, %20–30 dolgu) | L1: ince kabuk + kaburga | Konum (x, z): BAZ → L2 |
|---|---|---|---|
| Kafatası kubbesi + arka | 280 | 120 | (−5, 95) |
| Yüz (kaş, elmacık, üst diş) | 150 | 80 | (65, 55) |
| Çene (mandibula) | 90 | 45 | (50, −20) |
| Sahte detay (cıvata başı, oluk, piston kılıfı) | — | 15 | (30, 60) |
| Boyun üst plakası / U-mafsalın kafa yarısı | 40 | 30 | (0, 5) |
| Göz, basılı (2 küre, 3 kapak, çerçeve, link) | 55 | 40 | (70, 70) |
| 5× SG90 | 45 | 45 | (40, 70) → **(15, 15)** |
| Çene MG996R + kol | 60 | 60 | (20, 25) → **(−10, 0)** |
| PCA9685 #2 | 10 | 10 | (0, 60) → **(−45, 35)** |
| Vida + somun | 50 (~35 takım) | 25 (~18 takım + M2) | dağınık |
| Kablo + LED | 25 | 15 | dağınık |
| Ball-link / pushrod uçları | 5 | 5 | (40, 0) |
| **Toplam** | **~810 g** | **~490 g** | |

Kabuk sağlaması: 200 × 155 × 230 mm elipsoidin yüzey alanı ~1190 cm². 1.2 mm PLA ile tamamı kapalı olsa 177 g, 2.5 mm ile 369 g. Alt taraf, göz çukurları ve yan pencereler açık kalırsa (~%70 alan) 1.2 mm kabuk ~125 g olur. Kaburga ~25 g, dolu detay bölgeleri (dişler, elmacık) ~50 g eklenince **~200 g** çıkıyor ve L1 satırıyla tutuyor.

**Hedef önerisi: hareketli kafa ≤ 500 g**, kötü durum (+%30) 650 g. Kütlenin %40'ı yalnız kabuk et kalınlığından gidiyor. Servo yerini değiştirmek tork kazandırır ama gram kazandırmaz.

## 2. Pitch torku, senaryolar (θ = ±30°, α = 8.4 rad/s², P2)
τ = g·Σmᵢ(xᵢcosθ + zᵢsinθ) + I·α. I hesabına parçaların kendi jirasyon yarıçapı da katıldı.

| Senaryo | Kütle | AM (x, z) | Statik +30° | Dinamik | **Toplam** | Pay C1 (1× 3.5) | Pay C2 (2× 1:1, 7) | Pay C3 (2× 2:1, 14) | C3, +%30 kütle |
|---|---|---|---|---|---|---|---|---|---|
| BAZ (S1 naif) | 810 g | (26, 57) | 4.15 | 0.54 | **4.69** | 0.75 | 1.49 | 2.99 | 2.30 |
| L1 ince kabuk | 490 g | (29, 53) | 2.51 | 0.29 | **2.80** | 1.25 | 2.50 | 4.99 | 3.84 |
| **L2** = L1 + servolar ve PCA pivotun yanına/arkasına | 493 g | (22, 44) | 2.03 | 0.26 | **2.29** | 1.53 | **3.05** | **6.11** | 4.70 |
| L3 = L2 + çene servosu gövdede (Bowden) | 441 g | (26, 50) | 2.09 | 0.26 | **2.35** | 1.49 | 2.98 | 5.96 | 4.59 |
| **L4** = L2 + denge yayı (statiğin ~%70'i, tahmin) | 493 g | — | ~0.6 | 0.26 | **~0.87** | ~4.0 | **~8** | ~16 | ~12 |

−30° (geriye) yönünde bütün senaryolarda toplam ≤ 1.0 kg·cm, kritik değil.
(04'teki 6.6 kg·cm değeri 1 kg ve L = 74 mm varsayımıyla hesaplanmıştı. Burada parça parça dağılımla L ≈ 63 mm çıktı.)

**Her hamlenin tek başına etkisi** (L1'den başlayarak, +30° toplam torka):

| Hamle | Δτ | Gram değişimi |
|---|---|---|
| Kabuk 2.5 mm → 1.2 mm + kaburga (BAZ → L1) | **−1.89 kg·cm (−%40)** | −320 g |
| 5× SG90 göz arkasından kafatası tabanına | −0.24 | 0 (+3 g çubuk) |
| Çene MG996R, TMJ yanından pivotun arkasına/yanına | −0.24 | 0 |
| Çene MG996R gövdeye + Bowden | −0.18 | −52 g |
| PCA arkaya (oksipitale) | −0.05 | 0 |
| Denge yayı | **~−1.4** | +5–10 g |

**Önemli bulgu:** çene servosunu kafadan tamamen çıkarmak (−0.18), onu pivotun hemen arkasına koymaktan (−0.24) **daha az** kazandırıyor. Pivotun gerisindeki 55 g "bedava karşı ağırlık" işi görüyor. Bowden'ın sürtünme ve boşluk bedeli de buna ekleniyor.

## 3. Servoyu kafadan çıkarma: seçenekler

| | Ne | Tork kazancı | Dezavantaj (rakamla) |
|---|---|---|---|
| **S-a** göz servoları kafatası tabanında | 5 SG90 göz arkasından (40, 70) konumundan (15, 15) konumuna. Çubuklar 60–100 mm, Ø1 mm çelik tel | −0.24 kg·cm | Ø1 mm çelikte Euler burkulma 60 mm'de 27 N, 100 mm'de 9.7 N. Yük ≤ 2 N, yani pay 5–13 (hesap). Uzun çubuk ve ek ball-link boşluk ekler: link başına ~0.3 mm. 10 mm kolda ~±1.7° ek bakış hatası (tahmin). Taban, boyun mafsalıyla aynı hacmi paylaşır: **çakışma riski yüksek**, check.py baştan kurulmalı |
| **S-b** çene servosu pivotun arkasında/yanında, kafada | MG996R U-mafsal çatalının yanında (−10, 0). Çeneye bağlantı pushrod ("yanak pistonu") | −0.24 kg·cm | Çubuk ~60–70 mm olur, pistona bağlamak T-800 görüntüsüne zaten uyuyor. Roll ekseninde yanal kaçıklık 55 g × 30 mm ≈ 0.17 kg·cm. Roll payı 4.8 olduğu için önemsiz |
| **S-c** çene servosu gövdede + Bowden / push-pull kablo | Kafadan −52 g | −0.18 kg·cm | Bowden verimi en iyi ~%79 (475 mm, egzoiskelet; [ABB 2022](https://doaj.org/article/c34d28cbdf104532b834f4c7da5a131e)). Kapasite 3.5 → 2.76, çene payı 2.9 → **2.3**. Sürtünme kılıfın toplam bükülme açısıyla artar ([arXiv 2406.18412](https://arxiv.org/pdf/2406.18412), [arXiv 2512.24657](https://arxiv.org/pdf/2512.24657)). Boşluk/histerezis ve kablo uzaması zamanla kalibrasyon ister ([PMC9611146](https://pmc.ncbi.nlm.nih.gov/articles/PMC9611146)). Kablo, düz pushrod'dan her zaman daha sürtünmeli ([locostbuilders](https://www.locostbuilders.co.uk/viewthread.php?tid=215032), [stunthanger](https://stunthanger.com/smf/open-forum/pull-pull-control-surfaces)). Boyun 3 eksende eğildikçe kılıf yolu değişir ve çene ~0.5–1° oynar (tahmin). Artı: çeneyi yerçekimi açar, kablo yalnız kapatmak için çeker. 20° düşüş ~78 ms sürer, 100 ms hedefinin altında (hesap) |
| S-d PCA9685'i gövdeye almak | −10 g | −0.03 | Boyundan 4 yerine 15+ tel geçer. **Değmez** |

Disney ve KIST yaklaşımı aynı: ağır parçalar (servo, yay) tabanda, kafaya tel ya da çubukla ulaşılır ([US5289273](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5289273), [KIST statik dengeleyici](https://pubs.kist.re.kr/handle/201004/127140)). N2 zaten boyun servolarını gövdeye koyuyor. Kafada kalan 5 SG90 ve çene servosu, toplam kütlenin yalnız ~%21'i.

## 4. Hafif ama yoğun görünen yapı

| Teknik | Rakam | Kaynak / hesap |
|---|---|---|
| Kabuk 1.2 mm (0.4 nozul, 3 çevre) + kaburga 1.6 × 5 mm, 20 mm aralıkla | Aynı genişlikte 2.5 mm düz plakaya göre **kütle %64, eğilme rijitliği 3.0×** (kaburga yönünde). Eşdeğer düz kalınlık 3.6 mm, kütlesi onun %45'i | hesap |
| FDM alt sınırları | Destekli duvar en az 0.8 mm ([Oakland FDM kılavuzu](https://www.secs.oakland.edu/~latcha/ME4999/fdm_design_guidelines_2017-1.pdf)). Duvar en az 4 × katman yüksekliği, yani 0.2 mm katmanda 0.8 mm ([Stratasys Direct](https://info.stratasysdirect.com/rs/626-SBR-192/images/FDM_Design_Guide_Stratasys_Direct.pdf)). Kaburga en az 1.5 mm ([Xometry](https://xometry.com/blog/fdm-mini-guide), [Stanford Lab64](https://lab64.stanford.edu/hiddenoutdated-items/fdm-rules-of-thumb)). İnce duvarda çarpılmaya karşı kaburga önerilir (Stratasys) | kaynaklı |
| Önerilen et | Yük taşıyan kabuk **1.2 mm** · kaburga **1.6 mm** (4 hat) · yük taşımayan kapak ve süs **0.8 mm** · vida çevresi kalın (boss) ≥ 4 çevre | tasarım önerisi |
| Çevre > dolgu | Aynı gramda çevre sayısını artırmak dolguyu artırmaktan daha çok dayanım verir. 4 çevre ve %50 dolgunun üstünde kazanç ihmal edilebilir ([forum.v1e, CNC Kitchen'a atıf](https://forum.v1e.com/t/perimeter-settings/9562), [stacksheriff](https://stacksheriff.com/glossary/infill/), **ikinci el**) | Kalın detay bloklarında (elmacık, diş) gyroid %10–15 + 3 çevre |
| Sahte cıvata başı (basılı, Ø6 × 2.5) | ~0.08 g. Gerçek M3 takımı 1.2–1.5 g, yani **~15–20× hafif**. 50 adet basılı baş = 4 g | hesap |
| Sahte piston kılıfı (Ø10 × 60, 0.8 mm boru) | 1.9 g. Dolu basılsa 5.8 g. Gerçek pushrod'u kılıf içinden geçirmek ikisini birleştirir | hesap |
| Oluk, kenar ve panel çizgileri | Gram eklemez, hatta kütle çıkarır. "Yoğunluk" geometriyle verilir. Prensip 6 (ayrı basılan renk/detay) ile uyumlu | — |
| Açık kafes kafatası | T-800 endoskeleton zaten iskelet. Şakak ve kafatası arkası pencere olabilir, içteki servo görünür. 1:1 animatronik kafatası modellerinde oyuk bölgeler kullanılıyor ([Cults3D](https://cults3d.com/:3363296)). 1:1 T-800 kafatası ince katmanda "yüzlerce saat" sürüyor ([RPF](https://www.therpf.com/forums/threads/3d-printing-a-1-1-terminator-t-800-endoskeleton.297143/page-2)). İnce kabuk süreyi de kısaltır | kaynaklı |
| PETG | Yoğunluk 1.27, PLA'dan ~%2 ağır, daha esnek. İnce kapaklarda kırılmaya karşı iyi, kabukta PLA daha rijit | genel bilgi |

Basılabilirlik riski: 1.2 mm kabukta vida bağlantısı doğrudan yapılmaz. Somun cebi için yerel kalınlaştırma gerekir (≥ 5 mm; M3 somun 2.4 + 0.2 + taban). Somun cebi başına ~0.5 g ek (tahmin). Kubbe tabla için 3 parçaya bölünürse (01 risk tablosu) ek yerinde bindirme kaburgası kullanılmalı.

## 5. AM'yi pivota yaklaştırma: pivot, karşı ağırlık, yay
- **Pivot konumu:** 04'teki P3 (AM'de gimbal) tork olarak en iyisi, ama baş "top gibi" döner. L2'de AM (22, 44) mm. P2'yi 10 mm öne ve 10 mm yukarı almak L'yi ~49'dan ~37 mm'ye indirir, statik torku yaklaşık −%25 düşürür (tahmin). Görünüm hâlâ "kafatası tabanından eğilme" olur. Ara bir seçenek (P2').
- **Ölü karşı ağırlık:** nötrde m·x = 0.493 × 2.19 = 1.08 kg·cm. Bunu 50 mm geride bir ağırlıkla sıfırlamak **216 g** ölü kütle demek: kütle +%44, atalet ve yaw yükü artar. Kullanıcının prensibine aykırı, **önerilmez.**
- **Fonksiyonel karşı ağırlık:** çene servosu (55 g) ve PCA (10 g) zaten pivotun arkasına konur (L2). Bedava.
- **Yay (L4):** pivotun 40 mm arkasından gövdeye inen çekme yayı. Nötr torku sıfırlamak için ön yük F₀ = 1.08 / 4 = 0.27 kgf = **2.65 N**. +30°'de yay ~21 mm uzar ve ~2.0 kg·cm vermesi gerekir → F = 4.9 N → **k ≈ 0.11 N/mm**, ön yük 2.65 N. −30°'de kuvvet 0.4 N'a düşer ve yay gergin kalır. Bu yay tüm aralıkta statiği büyük ölçüde dengeler (kol açısının değişimi yüzünden ~%70 kabul edildi, tahmin).
  - İdeal çözüm "sıfır boylu yay": tel + makara ile kurulur, yay tabanda durur ([KIST yüz robotu boynu](https://pubs.kist.re.kr/handle/201004/127140), [Deepak & Ananthasuresh](https://eprints.iisc.ac.in/45507), patent [US8789440](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8789440)).
  - Kütle değişince denge bozulur ([Machines 2021](https://shura.shu.ac.uk/28896/1/machines-09-00145.pdf)). Bu yüzden yay bağlantı noktası ayarlanabilir olmalı (2–3 delik).
  - Ön gerilmeli yay ve motoru eksenden uzaklaştırmak ucuz RC servoyu yeterli kılmış ([PSU humanoid boyun](https://pure.psu.edu/en/publications/realizing-a-humanoid-neck-with-serial-chain-four-bar-mechanism/)). Salvius pitch için karşı ağırlık ya da yay öneriyor ([Salvius](https://salvius.org/spec/v01/neck/)).
  - Yay **satın alma kalemi**: küçük çekme yayı seti, ~50–150 ₺ (belirsiz). Envanterde yay yok.
- **Sönüm:** ağır kafa RC servoda salınım/overshoot yapıyor. Hafif sürtünme pedi (köpük) çözüm olarak kullanılmış ([Synthiam](https://synthiam.com/Community/Questions/Servo-Dampening-9571)). Yay ve hafif kafa bu ihtiyacı azaltır.

## 6. Benzer projelerden dersler

| Proje | Kafa kütlesi | Ders |
|---|---|---|
| EZ-InMoov kafası (ticari kit) | **1250 g**, boyun 2× 19 kg·cm "HDD" servo | [STEMfinity](https://stemfinity.com/collections/all/products/ez-inmoov-robot-head). Bizim BAZ'dan 1.5× ağır, servosu bizim 2:1 MG996R'ın ~2.7× torkunda. InMoov ölçeğinde kafa = büyük servo |
| Salvius | örnek 2.5 kg, 5 cm kol | Formül: kütle × kol × 1.5 → 18.75 kg·cm, öneri 25–35 ([Salvius](https://salvius.org/spec/v01/neck/)) |
| Synthiam topluluğu, ağır kafalar | — | Plastik dişli servo ağır kafada titreşiyor → metal dişli. Overshoot → köpükle sürtünme ([Synthiam dampening](https://synthiam.com/Community/Questions/Servo-Dampening-9571), [Wall-e örneği](https://synthiam.com/Robot/Cyberdude-s-Wall-e-368), hangi başlıkta olduğu belirsiz) |
| Stan Winston forumu, animatronik ejderha | — | Mafsallar kablo tahrikli ve **yayla dengelenmiş**, yalnız dönüş servoda ([forum](https://forums.stanwinstonschool.com/discussion/comment/12475), belirsiz) |
| Will Cogley kafa iskeleti | rakam yok | Basılı iç iskelet + çok sayıda küçük servo ([Arduino blog](https://blog.arduino.cc/?p=40566)). Ağız 2× MG996R ([Hackster](https://www.hackster.io/news/will-cogley-s-animatronic-mouth-responds-to-his-typing-2e4d892f453c)), ama sabit tabanda |
| Berkeley ME102B gözü | göz için 170 g PLA alınmış (bitmiş kütle değil) | [PDF](https://edg.berkeley.edu/wp-content/uploads/2020/12/2020Fall_ME102B_gerhardtkatelyn.pdf) |
| Project Eye v5 (kendi) | pitch'te 225 g, AM 23 mm geride | Kağıtta pay 2.3, pratikte yetmedi (§0) |

Benzer kafalar için gram düzeyinde yayımlanmış kütle **bulunamadı** (InMoov açık kaynak, Poppy, Cogley). Tek sayı EZ-InMoov'un 1250 g'ı.

## 7. Seçenek paketleri

| Paket | İçerik | Kafa | +30° tork | Pitch payı | Ek maliyet | Risk |
|---|---|---|---|---|---|---|
| H0 | S1 olduğu gibi | ~810 g | 4.69 | C3: 2.99 | 0 | Eye dersi: +%30 kütlede 2.3 |
| H1 | İnce kabuk + kaburga + sahte detay | ~490 g | 2.80 | C3: 4.99 | 0 | ince et baskı kalitesi |
| **H2** | H1 + S-a + S-b (servolar pivot yanına, PCA arkaya) + yay | ~495 g | ~0.9 | C3: ~16 · **C2 (1:1): ~8** | yay ~50–150 ₺ | taban hacmi kalabalık |
| H3 | H2 + çene gövdede (Bowden) | ~445 g | ~0.9 | ≈ H2 | Bowden kılıf ~100–200 ₺ (belirsiz) | çene payı 2.3, kalibrasyon kayması |

"Köşe kesme" fırsatı: H2'de **2:1 yerine 1:1 sürüş (C2)** pay ~3 verir, yaysız bile ≥3. Baş hızı 2 katına çıkar (~350°/s yüksüzde), 2:1 kol için gereken hacim de kalkar. Ama 1:1'de MG996R boşluğu başa küçülmeden geçer. 2:1, ölçülmemiş servo için daha güvenli tampon.

## 8. Tek öneri
**H2:**
- Kabuk 1.2 mm + 1.6 mm kaburga. Yük taşımayan süsler 0.8 mm, basılı sahte cıvata başları. Hedef **≤ 500 g**.
- Çene MG996R kafada kalır ama pivotun arkasına/yanına alınır, pushrod "yanak pistonu" kılıfının içinden geçer.
- 5 SG90 kafatası tabanına toplanır, Ø1 mm çelik çubuklarla sürülür.
- PCA oksipitale konur.
- Pivot arkasında ayarlanabilir çekme yayı (k ≈ 0.1 N/mm, ön yük ≈ 2.7 N).
- Boyunda 2:1 korunur. MG996R tork kuponu ölçülünce 1:1'e inmek düşünülebilir.
- Bowden (H3) önerilmez: pivot arkasındaki servo daha fazla kazandırıyor (−0.24'e karşı −0.18 kg·cm) ve sürtünme getirmiyor.

## 9. Plan için riskler (rakamla)
| Risk | Bu projede | Rakam | Kritiklik |
|---|---|---|---|
| **Tork** | pitch | H0'da pay 2.99, +%30 kütlede 2.30. Eye dersine göre sınırda. H2'de ~16. **MG996R sürekli torku ölçülmedi** (3.5 varsayım). Yay olmazsa H1/H2 payı 5–6 | **1.** CAD kütlesi her revizyonda yeniden hesaplanmalı (kütle bütçesi tablosu check'e eklenmeli) |
| **Montaj erişimi** | kafatası tabanı: U-mafsal + 5 SG90 + çene servosu + yay bağlantısı aynı ~60 mm hacimde | Pitch ±30°, roll ±20° süpürme hacmiyle çakışma. SG90 kulak vidaları (M2) tornavidayla alttan erişilebilmeli | **2.** check_montaj baştan |
| **Tolerans zinciri** | uzun göz çubukları | Link başına +2 ball-link ~0.3 mm, 10 mm kolda ±1.7° ek bakış hatası (tahmin). Toplam bakış hatası 01'deki ±2–3°'den ±3–4°'e çıkabilir | 3. Kol yarıçapını büyütmek (15 mm) hatayı ~⅔'e indirir |
| Tabla | ince kabuk | Kubbe 3 parça. Ek yerinde bindirme kaburgası ≥ 1.6 mm. 1.2 mm duvarda vida yok, somun cebi bossu ≥ 5 mm | orta |
| Kablo | 5 SG90 kablosu tabandan kısa yol | Göz servoları tabana gelince SG90 kabloları ~10 cm kısalır, kafada ~5 g azalır. Boyundan 4 iletken geçmeye devam eder | düşük |
| Baskı dayanımı | 1.2 mm kabuk | Darbeye zayıf (tahmin). Taşıma ya da düşmede kubbe kırılabilir. Kenarlar kaburgayla çerçevelenmeli | düşük–orta |
