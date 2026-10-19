# 10 — Kart ölçüleri, pin dizilimleri, kablo (Project Bust)

Envanter okundu: `Rynnat/agentic-mechanism-design@plan-v2:envanter.md` → ESP32 = **"YD-ESP32 geliştirme kartı (muhtemelen ESP32-S3, iki USB-C)"**; PCA9685 ×2 (kondansatör takılı, yeşil vidalı giriş, birinde A0 → 0x41). Kartın kendisi ölçülmedi → ESP32 **DOĞRULANMADI**.
Birim mm. Orijin: PCB sol-alt köşe, bileşen yüzü +Z, uzun kenar +X. **[T]** = tahmin/doğrulanmadı. Makinece okunur kopya: `cad_y/kartlar.json`.

## Başlık standardı (tüm kartlar)
Düz erkek başlık: aralık 2.54, plastik 2.5 yüksek, pin 0.64 kare, PCB üstü pin 6.0 (toplam 8.5), altta 3.0 (lehim tarafı). Açılı: plastik 2.5×2.5 PCB kenarında, pin yatay 6.0 dışarı, altta 3.0. Dişi dupont takılınca: başlık 8.5 + gövde 14 → PCB'den ~**22.5** yükseklik (açılıda kenardan ~20 dışarı, yükseklik ~2.5).

## 1. PCA9685 — Adafruit 815 (Eagle `Adafruit PCA9685 rev C.brd`'den çıkarıldı)
- PCB **62.23 × 25.40 × 1.6**, köşe R 3.175. Ürün sayfası: 62.5×25.4×3 [1].
- Delik Ø**2.5** ×4: (3.175, 3.175) (3.175, 22.225) (59.055, 3.175) (59.055, 22.225) → aralık **55.88 × 19.05** [2].
- Yan başlıklar 1×6, kısa kenarlarda, x=1.905 ve x=60.325, y 6.477…19.177: GND, OE, SCL, SDA, VCC, V+ (sıra yönü [T]; sağdaki zincirleme için) [1][2].
- Servo 3×4 bloklar ×4, alt uzun kenar boyunca, merkez x = 10.795 / 23.495 / 38.735 / 51.435; satırlar y 1.397 / 3.937 / 6.477 = GND (kenar) / V+ / PWM [sıra T] [2].
- Terminal 1×2, 3.5 mm adım, üst uzun kenar ortası (31.115, 21.59); gövde ~7.0×7.6×10 h [T].
- Kondansatör C2 pedi (11.811, 21.209), Adafruit'te boş; envanterdeki kartta takılı elektrolitik ~Ø8×12 [T] → en yüksek sabit bileşen ~12–13. Servo fişleri takılı: **22.5**.
- Klon (yaygın): aynı dış ölçü ve delik düzeni (Adafruit kopyası) [T].

## 2. MAX98357A — Adafruit 3006 (Eagle `Adafruit MAX98357 Breakout.brd`)
- PCB **17.78 × 19.05 × 1.6**, köşe R 2.54; ürün sayfası 19.4×17.8×3.0, 1.2 g [3][4].
- Delik Ø**2.5** ×2, üst kenarda: (2.54, 16.51), (15.24, 16.51) → aralık 12.70 [4].
- Başlık 1×7 alt kenar, merkez (8.89, 2.54), x 1.27…16.51: **LRC, BCLK, DIN, GAIN, SD, GND, Vin** [3][4].
- Hoparlör terminali 1×2 3.5 mm, (8.89, 15.494), iki delik arasında; 2024-06'dan beri lehimli gelir [3]; ~10 h [T] → en yüksek bileşen.
- Klon (mor "MAX98357 I2S 3W"): ~18×18 [T], delik çoğunda yok [T], aynı 7 pin sırası, hoparlör 2 ped veya 2 pin.

## 3. INMP441 breakout (yaygın yuvarlak; DOĞRULANMADI, kumpasla ölç)
- PCB Ø**~14** (ilanlar 14–15) [T][5][6], kare varyant 14×14 [6]; kalınlık 1.0–1.6 [T].
- MEMS 4.72 × 3.76 × 1.0, **alt portlu** [5].
- Port: PCB merkezinde, MEMS'in altında PCB'den geçen delik Ø~0.8 [T]; ses **MEMS'in karşı (bileşensiz) yüzünden** girer → başlık plastiğini MEMS yüzüne koy, port yüzü düz kalsın, köpüğe bu yüz bakar.
- Başlık 6 pin, 2 sütun × 3: SCK, WS, L/R | SD, VDD, GND; sütun aralığı ~10.16 [T] [5]. Montaj deliği yok.

## 4. ESP32
**YD-ESP32-S3 (envanter adayı) — DOĞRULANMADI**: PCB **57.15 × 27.94** [7] veya **63.5 × 28** (ilan) [8]; sıra aralığı **25.4** (Espressif footprint'indeki 22.86 bu karta uymaz) [8][9]; 2×22 pin, 2.54. Pin 1–44 sırası [7]: GND, GND, IO19, IO20, IO21, IO47, IO48, IO45, IO0, IO35–IO42, IO2, IO1, IO44, IO43, GND, GND, 5V, IO14, IO13, IO12, IO11, IO10, IO9, IO46, IO3, IO8, IO18, IO17, IO16, IO15, IO7, IO6, IO5, IO4, RST, 3V3, 3V3 (hangi sıranın sol olduğu kaynakta yok). 2× USB-C kısa kenarda (gövde ~8.94×7.3×3.2), modül 3.1 h, BOOT/RST butonları, WS2812 (IO48); montaj deliği yok [T]. N16R8'de IO35–37 PSRAM'a ayrılı → kullanma.
Yedek varyantlar: DevKitC V4 38 pin **54.4 × 27.9** [T], 2×19, sıra 25.4; DOIT V1 30 pin **51.5 × 28.4** [T], 2×15, sıra 25.4; ikisi micro-USB.

## 5. Hoparlör 40 mm 3 W 4 Ω (SİPARİŞ "metal kasa 2'li" — ilan 503 verdi, okunamadı)
Ø**40**, derinlik ~**20** [T] (Pimoroni 4 Ω 3 W benzeri 40×40×20, M2.5 delik 32.5 aralık — kare çerçeveli, farklı form) [10]; mıknatıs Ø~27 [T]; yuvarlak metal çerçevede kulak yok [T] → kenardan kelepçe/halka; uçlar arka çerçeve kenarında 2 lehim tabı, kablo radyal çıkar [T]. Gelince ölç.

## 6. OV5640 (rezerv, XICOOLEE) — DOĞRULANMADI
XICOOLEE ilanı/çizimi bulunamadı. Yaygın DVP kartlar **35.7 × 23.9** (SparkFun / Waveshare A-B-C) [11][12]; PLAN yuvası 32×32, params 24×24 [T]. ESP32-S3 uyumlu FPC versiyon: sensör modülü ~8.5×8.5, 24 pin 0.5 mm FPC [T]. Sipariş sırasında ilan ölçüsünü al.

## 7. 5 V DC jak (envanter tipi bilinmiyor)
Panel DC-022: M8×0.75 diş, panel deliği Ø8.0, gövde ~17 boy, somun 10 AA [T]. PCB DC-005: 14.0 × 9.0 × 11.0, 3 pin [T]. Fiş 5.5×2.1.

## 8. Netlist (GPIO önerisi [T] — PLAN §13'te pin numarası yok)
| Sinyal | ESP32-S3 | Hedef |
|---|---|---|
| I2S0 SCK | IO4 | INMP_L.SCK + INMP_R.SCK |
| I2S0 WS | IO5 | iki mic WS |
| I2S0 SD | IO6 | iki mic SD (ortak hat) |
| L/R | — | sol mic → GND, sağ → 3V3 |
| VDD / GND | 3V3 / GND | iki mic |
| I2S1 BCLK / LRC / DIN | IO15 / IO16 / IO7 | MAX.BCLK / LRC / DIN |
| Vin / GND | 5V / GND | MAX |
| GAIN | boş | 9 dB (GND'ye 12 dB, Vin'e 6 dB) [3] |
| SD | boş | Adafruit'te Vin'e çekili → (L+R)/2 |
| MAX +/- | — | hoparlör (köprü çıkış, GND'ye bağlama) |
| I2C SDA/SCL | Uno A4/A5 (veya ESP IO8/IO9) | PCA1 → zincir → PCA2 |
| PCA VCC | MCU lojik (Uno 5 V / ESP 3V3) | — |
| PCA V+ | terminal | her PCA ayrı 5 V 5 A adaptör; GND'ler ortak |

Servo kablo: kahverengi GND, kırmızı V+, turuncu PWM (MG996R ve SG90). I2S kablo ≤40 cm (params KABLO_8 = 420 + 60 servis).

## 9. Kablo / konnektör ölçüleri
Dupont dişi 1 pin 2.54×2.54×14; servo 3p fiş ~7.6×2.6×14; JST-PH 2p ~6.0×4.5×6.0; JST-XH 2p ~7.4×5.75×7.0 [T]. Tel dış çap: 26 AWG ~1.0, 24 AWG ~1.2, 22 AWG ~1.6; servo şerit 3 damar ~3.3×1.1. Önerilen: dupont 24–26 AWG, servo 22 AWG, hoparlör 22 AWG.
Bükülme yarıçapı: sabit 5×OD, hareketli (boyun geçişi) 10×OD → 22 AWG 8 / 16; servo şerit (düz eksende) 5.5 / 11.

## 10. cad/satin.py + params.py kaba ölçülerle karşılaştırma
| Parça | params | Gerçek | Fark |
|---|---|---|---|
| esp32 | 55 × 28 × 1.6 | 57.15–63.5 × 28 | **+2…+8.5 boy**, + USB-C uçta; başlık altı 3, üstü 8.5 |
| max98357 | 18 × 18 | 17.78 × 19.05 | +1.05 W; terminal 10 h + başlık/dupont 22.5 yok |
| pca / pca1 | 62.5 × 25.4, delik 56 × 19 | 62.23 × 25.4, 55.88 × 19.05 | ≤0.3 (iyi); servo fişleriyle **22.5** h + kondansatör yok |
| inmp441 | 14 × 14 × 1.6 kutu | Ø14 yuvarlak | arkada başlık+dupont 22.5 yok |
| kamera | 24 × 24 | 35.7 × 23.9 (aday), plan 32 × 32 | +11.7 boy (aday) |
| hoparlör | Ø40 × 20 | Ø40 × ~20 [T] | uyumlu, ilanla doğrula |

## Plan için riskler
- **Kablo (kritik):** her düz başlık+dupont PCB'den 22.5 çıkıyor; kulak mikrofonu arkasında (MIK boy 10) ve kart tablasında bu hacim yok. Açılı başlıkta yükseklik ~2.5'e iner ama kenardan ~20 dışarı taşar.
- **Tolerans:** ESP32 boyu 6.35 mm belirsiz → yuvayı 64'e göre aç ya da kart gelince ölç; USB-C ucunda +10 fiş erişimi.
- **Montaj erişimi:** ESP32'de delik yok → kenar kızağı/klips; MAX 2× M2.5 (12.7 aralık); PCA 4× M2.5 (55.88×19.05).
- **Tork / tabla:** bu not için etkisiz (pasif kartlar).
- Doğrulanacaklar: YD-ESP32 boyu ve pin tarafı, INMP441 çapı/sütun aralığı/port yüzü, hoparlör derinliği/mıknatıs, DC jak tipi.

## Kaynaklar
1. https://www.adafruit.com/product/815
2. https://github.com/adafruit/Adafruit-16-Channel-PWM-Servo-Driver-PCB (Adafruit PCA9685 rev C.brd)
3. https://www.adafruit.com/product/3006
4. https://github.com/adafruit/Adafruit-MAX98357-I2S-Amp-Breakout (Adafruit MAX98357 Breakout.brd)
5. https://components101.com/modules/inmp441-mems-omnidirectional-microphone
6. https://manuals.plus/asin/B081JN1CW5
7. https://www.espboards.dev/esp32/yd-esp32-s3/
8. https://www.cadcrowd.com/job/8402-esp32-s3-mic-carrier-board
9. https://forum.kicad.info/t/pin-distance-in-esp32-s3-devkitc-1/71001
10. https://shop.pimoroni.com/products/mini-speaker-4-3w-with-jst-ph-connector
11. https://www.sparkfun.com/ov5640-camera-board-5-megapixel-2592x1944-fisheye-lens.html
12. https://www.waveshare.com/ov5640-camera-board-a.htm
