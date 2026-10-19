# Project Bust: sipariş listesi (2026-10-17)

Fiyatlar Amazon TR aramasından alındı, sayfalar doğrulanmadı. Almadan önce stok ve fiyatı ürün sayfasında kontrol et.
C2 (2. eğme ekseni) iptal edildi, kablo 8 damara çıktı (ses), filament hariç.

## A. Hemen al (kuponlar ve ses için)
| # | Kalem | Adet | ~₺ | Nereden / arama | Not |
|---|---|---|---|---|---|
| 1 | INMP441 + MAX98357 seti | 1 | 551 | kullanıcının bulduğu set | **Setteki mikrofon sayısını kontrol et**: 2 değilse 2. satırı al |
| 2 | INMP441 (tek) | 0–1 | 199 | [SANEC INMP441](https://www.amazon.com.tr/SANEC-INMP441-Y%C3%B6nl%C3%BC-Mikrofon-Mod%C3%BCl%C3%BC/dp/B0HHT6X24B) | yalnız sette 1 mikrofon varsa |
| 3 | Hoparlör 4 cm 3 W 4 Ω, 2'li | 1 | 371 | [metal kasa 2'li](https://www.amazon.com.tr/Hoparl%C3%B6r-M%C4%B1knat%C4%B1sl%C4%B1-Amplifikat%C3%B6r-Hoparl%C3%B6r%C3%BC-Kullan%C4%B1m%C4%B1/dp/B0DRW64JTD) | göğüs |
| 4 | M3 rotil, alüminyum | 8 (6'lı ×2) | ~300 | [Jenngaoo 6'lı](https://www.amazon.com.tr/ba%C4%9Flant%C4%B1-k%C3%BCresel-uzaktan-kumanda-uygundur/dp/B0D5DBB884) · alt.: [SPYMINNPOO 10'lu](https://www.amazon.com.tr/ba%C4%9Flant%C4%B1-al%C3%BCminyum-y%C3%BCkseltme-aksesuar%C4%B1-aksesuar/dp/B09W5XTFZT) | K3 bunları bekliyor. Plastik olan alınmasın (boşluk) |
| 5 | Lazy susan 5" (~120 mm) | 1 | ~250 | [Tembel Susan 5" 12 cm](https://www.amazon.com.tr/Halkalar%C4%B1-%C3%9812-100-P%C3%BCr%C3%BCzs%C3%BCz-Bilgisayar-Monit%C3%B6r%C3%BC/dp/B0CNQSBK7N) · alt.: [alüminyum 5"](https://www.amazon.com.tr/Tabanl%C4%B1-Al%C3%BCminyum-Ala%C5%9F%C4%B1ml%C4%B1-Rulman%C4%B1-B%C3%BCy%C3%BCleyici/dp/B0CQY7XFWN) | dış çapı ≤ 124 mm olmalı. K8 bunu bekliyor |
| 6 | Çekme yayı, yumuşak ve uzun, 2–3 farklı | 3–6 | ~100–150 | nalbur ya da Amazon "çekme yayı tel 0.6–0.8 mm, 50–80 mm" | K6'da ölçülecek. 1.5 mm telli yaylar fazla sert |

## B. CAD sonrası al (kupon sonuçlarına göre)
| # | Kalem | Adet | ~₺ | Not |
|---|---|---|---|---|
| 7 | M3 dişli çubuk 1 m | 1 | 40 | pushrod |
| 8 | Uzun vida: M4×40 ×4, M4×20 ×14, M3×20/25 ×10 | set | 200 | adetleri CAD vida_adet check'i kesinleştirir |
| 9 | M2 somun | 20 | 30 | **önce stoğa bak** |
| 10 | Servo uzatma kablosu 30 cm | 3 | 60 | |
| 11 | 8 damarlı ince esnek kablo 1 m + konnektör | 1 | ~120 | boyun (güç + I2C + I2S) |
| 12 | Ø1 çelik tel | 1 | 30 | göz |
| 13 | (koşullu) Al boru Ø6, 1 m | 1 | 100 | yalnız K5'te PLA piston takılırsa |
| 14 | (koşullu) MG90S ×5 | 5 | 581 | yalnız K4'te kapak > 100 ms çıkarsa |

**Toplam:** A ~1570–1820 ₺, B ~480 ₺ (koşullular hariç), hepsi ~2050–2300 ₺. Kullanıcı tavan aşımını onayladı.

## Envanter kontrolü (bedava, şimdi yap)
MG996R ×6 · SG90 ≥5 · PCA9685 ×2 · 5 V 5 A adaptör ×2 · Uno klon · **ESP32** · 1000 µF kondansatör · DC jak · M2×8 vida · **M2 somun?** · M3/M4 vida ve somun
