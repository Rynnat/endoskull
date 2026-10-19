# 06: Bütçe, güç, elektronik

Tarih: 2026-10-16. Aşama 0. Tavan ~2000 ₺ (KARARLAR.md). Önce envanter kullanılır.
Envanter: `Rynnat/agentic-mechanism-design` reposunun `plan-v2` dalındaki `envanter.md` dosyası okundu (güncelleme 2026-10-06).

## 1. Envanterden kullanılacaklar (0 ₺)
- 6× MG996R, ~6× SG90 (boşta), 2× PCA9685 (birinin A0 pedi lehimlenerek 0x41), 2× 5 V 5 A adaptör (MRW-2505), 4× 1000 µF, 2× dişi DC jak
- Uno klon (boşta), Nano + shield, ESP32
- LED seti (kırmızı göz), kırmızı-siyah kablo makarası (kesit **bilinmiyor**)
- Vidalar: M2×8 (30), M3×8/14 (30'ar), M3×10 (6), M3×15 havşa (20), M4×8 (30), M4×10 (çok). Somunlar var.
- Eye v5 parçaları **kilitli**, kullanılmaz.

**Envanterde olmayanlar:** filament (cins ve miktarı listede yok, kullanıcı söylemeli), rulman, yay, ball link, M3 için 14 mm'den uzun vida, servo uzatma kablosu.

## 2. Alınacaklar: TR fiyatları
| Kalem | Adet | Birim | Toplam | Kaynak |
|---|---|---|---|---|
| Lazy susan / döner tabla rulmanı 100–150 mm (yaw) | 1 | 150–300 | 150–300 | **tahmin**. Yurt dışında 100 mm £3.85 + KDV ([Flints](https://flints.co.uk/product/All/CAS100LS)), ~5–50 € ([eBay](https://www.ebay.de/itm/133058843509)) |
| 608ZZ rulman (eğme mafsalı, çene menteşesi) | 4–6 | 15–30 | 60–180 | **tahmin** |
| Çekme yayı seti (denge yayı, çene kapatma) | 1 | 100–200 | 100–200 | **tahmin** |
| M3 rot ucu / ball link + dişli çubuk | 6–8 | — | 200–400 | **tahmin** |
| Uzun vida seti (M3×20/25/30, M4×16/20) | 1 | — | 150–250 | **tahmin** |
| Servo uzatma kablosu 30 cm | 6 | 10–25 | 60–150 | **tahmin** |
| **Donanım ara toplamı** | | | **~720–1480 (orta ~1050)** | |
| MG90S (isteğe bağlı) | 5–6 | **116.24** | 581–697 | [direnc.net](https://www.direnc.net/mg90s-servo-motor) (fiyat çekildi) |
| DS3218 20 kg (isteğe bağlı) | 1–2 | 600–1000 | 600–2000 | **tahmin**. Yurt dışında $15–25 ([rcdrone TR](https://rcdrone.top/tr/products/dsservo-ds3218-dijital-servo), [thinkrobotics](https://thinkrobotics.com/products/ds3218-servo)). Tork beyanı 19 kg·cm @5 V, bir kullanıcı "12–15" ölçmüş ([desertcart](https://www.desertcart.ma/products/42716427)) |
| PLA (düz renk) | 1.5–2.5 kg | ~580/kg | 870–1450 | [akakce](https://www.akakce.com/filament/1-kg-filament,33.html) |
| Silk PLA (gümüş tonlu) | 1 kg | 981–1097 | ~1000 | [idefix Kingroon](https://www.idefix.com/kingroon-cift-renk-altin-gumus-pla-silk-filament-175-mm-1000gr-p-26437925) |
| Astar + gümüş sprey | 2–3 | — | 300–500 | **tahmin** |
| Rub 'n Buff | 1 | — | 400–700 | **tahmin** |

Filament tahmini: kafa ve boyun 0.8–1.0 kg. Göğüs ve omuz **kapalı kabuk** olursa 1.0–1.5 kg, **T-800 kaburga iskeleti** (açık) olursa ~0.5–0.7 kg. Hepsi **tahmin**. Açık iskelet hem filamenti hem baskı süresini azaltır.

## 3. Seçenekler (2000 ₺ içinde)
| | Mimari | Servolar | Alım | Filament dahil? |
|---|---|---|---|---|
| **S1: Envanter maksimum** | N2 boyun (3× MG996R) + J3 çene (MG996R) + E3 göz (5× SG90) | 4 MG996R + 5 SG90, hepsi envanterden. 2 MG996R + 1 SG90 yedek | ~1050 ₺ donanım | + düz PLA 1.5 kg (iskelet göğüs) 870 + kuru fırça boya ~150 = **~2070 ₺**, sınırda. Filament elde varsa **~1050** |
| **S2: Metal dişli gözler** | S1, ama gözde 5× MG90S | 4 MG996R + 5 MG90S, SG90'lar yedek | ~1050 + 581 = **~1630 ₺** | filament hariç sığar, dahil olursa aşar (~2650) |
| **S3: Seri boyun (N1)** | N1 (4× MG996R) + J3 + E2 (4× SG90) | 5 MG996R + 4 SG90 | ~1050 ₺ | S1 ile aynı. Kafada/boyunda daha çok servo ağırlığı taşınır |
| S4: Güçlü boyun (bütçe **dışı**) | N1 + 2× DS3218 pitch | — | ~2250–3050 ₺ | aşar |

## 4. Güç dağılımı
| Hat | Yük | Tipik | Kötü durum | Not |
|---|---|---|---|---|
| Adaptör A → PCA9685 #1 (0x40) | 3–4 MG996R (boyun + çene) | 3–4 × 0.5–0.9 A = **1.5–3.6 A** | 4 × 2.5 A kilitlenme = **10 A** > 5 A | Kilitlenme aynı anda pek olmaz. Ama başlangıç akım sıçramaları çakışabilir. Yazılımda hareket başlangıçlarını 20–50 ms kaydırmak ve rayda 2× 1000 µF önerilir |
| Adaptör B → PCA9685 #2 (0x41) | 5 SG90 / MG90S (göz + kapak) | <1 A | 5 × ~0.65 A ≈ 3.3 A **(SG90 kilitlenme akımı belirsiz)** | rahat |
- MG996R akımları: [makerstore](https://www.makerstore.com.au/?p=3302). Prensip 8: servolar harici beslenir, GND ortak olur, USB'den servo beslenmez.
- **Boyundan geçen kablo:** PCA #2 kafada olursa boyundan yalnız 4 iletken geçer (5 V, GND, SDA, SCL). Akım ≤3.3 A, 0.5 mm² kablo, 1 m gidiş-dönüş ≈ 0.034 Ω, düşüm ≈ 0.1 V. Kafada değilse 5 servo × 3 tel = 15 tel + çene kabloları geçer, demet çapı ~8 mm **(tahmin)**. ±70° yaw için servis halkası gerekir. 30–50 cm I2C 100 kHz'de genelde sorun çıkarmaz **(belirsiz)**.
- **Kontrol:** PC (webcam + MediaPipe, Eye v5 / Tracking Arm altyapısı) → seri port → Uno klon → I2C → 2× PCA9685. ESP32 Wi-Fi ile kablosuz da olur, ama 3.3 V lojik; PCA9685 3.3 V ile çalışır **(datasheet, doğrulanmadı)**.
