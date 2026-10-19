# Project Bust: Aşama 0 araştırma özeti

Tarih: 2026-10-16 · Agent Flow v2 aşama 0 · Araştırmacı ajan
Envanter okundu: `Rynnat/agentic-mechanism-design@plan-v2/envanter.md` (güncelleme 2026-10-06). Ölçülmüş değerler `cq-ders/bilesenler.json`, `agent-flow/sablonlar/toleranslar.py` ve `epic-tasarim-prensipleri.md` dosyalarından alındı. **MG996R için ölçülmüş değer yok.**
KARARLAR.md'ye uyuldu: Project Angela'nın hiçbir dosyası okunmadı. `00_sorular.md` dosyasından yalnız InMoov özeti ve envanter bilgisi alındı.
Arama bütçesi: 20/20 web araması ve 5 sayfa çekme kullanıldı. Kaynakların çoğu forum ya da ilan; bilimsel sayılar makalelerden.

Detay dosyaları:
- `02_gorsel_dil.md`: T-800, InMoov, metalik görünüm
- `03_goz_mekanizmasi.md`: göz mekanizması
- `04_cene_boyun_tork.md`: kütle, boyun mimarisi, tork hesapları
- `05_insansi_hareket.md`: sakkad, kırpma, VOR sayıları
- `06_butce_guc.md`: TR fiyatları, seçenekler, güç dağılımı

## 1. En önemli bulgular
1. **Pitch ekseni bu projenin darboğazı.** Kafa kütlesi 1.0 kg kabul edildi, tahmin aralığı 0.55–0.85 kg. Pivot insandaki gibi kafatası tabanındaysa 30° öne eğik + dinamik yük **6.6 kg·cm** tutuyor. Tek MG996R doğrudan bağlanırsa (sürekli 3.5) **pay 0.53 ✗.** İki MG996R 2:1 pushrod'la **2.12 ✓**. Kafa 1.5 kg olursa 1.41, yani denge yayı gerekir. Yaw rulman üstündeyse 0.8–2.2 kg·cm, tek MG996R ile pay 1.6–4.4.
2. **T-800 estetiği mekanizmayla aynı yöne çalışıyor.** Boyundaki pushrod'lar "hidrolik silindir", çene pushrod'u "yanak pistonu" olarak giydirilebilir. Göğüs açık kaburga iskeleti olursa filament de baskı süresi de yaklaşık yarıya iner (tahmin). Tek çelişki: **T-800'ün göz kapağı yok.** Kapak robotik bir "deklanşör" plakası olarak tasarlanabilir.
3. **Göz için tork sorun değil; hız ve çözünürlük sorun.** SG90 10°'lik sakkadı ~40–60 ms'de yapar (tahmin), insan 43 ms. Kırpmada kapanma 75–100 ms gerekiyor; SG90 60°'yi 100 ms'de dönüyor, sınırda. 1.5× kol oranı ~67 ms verir. Mikrosakkadlar (0.02–1°) ~1° ölü bant yüzünden fizikte görünmez, yalnız simde yapılabilir.
4. **Gerçekçilik için firmware sayıları:**
   - Sakkad süresi D = 2.2·A + 21 ms, tepe hızı V = 500·(1 − e^(−A/14)) °/s.
   - Kırpma: kapanma ~80 ms, açılma ~200 ms, dakikada 11–20.
   - Bakış < ~25° ise yalnız göz döner; daha büyükse baş katılır ve gözden 20–40 ms sonra başlar. VOR kuralı: e = G − h (göz açısı = hedef bakış − baş açısı).
5. **Envanterle yapılabilir.**
   - Servolar: 4 MG996R + 5 SG90 envanterden; 2 MG996R + 1 SG90 yedek kalıyor.
   - Donanım alımı ~1050 ₺ (rulman, yay, ball link, uzun vida, kablo; çoğu tahmin).
   - Belirsizlik filamentte: envanterde filament yok ve 1.5–2.5 kg gerekiyor (~870–1450 ₺). Filament bütçeye dahilse toplam ~2000 ₺ sınırına dayanıyor.

## 2. Benzer projeler
| Proje | Eksen | Boyut / kütle | Aktüatör | Redüksiyon / yatak | Maliyet | İşe yarayan / yaramayan |
|---|---|---|---|---|---|---|
| InMoov baş ([hardware map](https://inmoov.fr/default-hardware-map/), [neck&jaw](https://inmoov.fr/neck-and-jaw/)) | boyun eğme, dönüş, yana eğme, çene, göz X/Y | 1:1, "çok ağır" (rakam yok) ([?p=406](https://inmoov.fr/?p=406)) | 2× HK15298B eğme (master/slave), HS-805BB, çene HK15298 | dişli (MainGear → NeckHinge) | yüksek | ✓ çift servo eğme. ✗ büyük servo şart, kapak yok, STL yalnız Blender |
| Will Cogley göz 2017 ([Hackster](https://hackster.io/news/creep-your-friends-out-with-this-3d-printed-eye-dd42d3434d7c)) | göz X/Y + 2 kapak | tek göz | 4 mikro servo | doğrudan kol | düşük | ✓ pot ile varsayılan kapak açıklığı |
| Cogley EyeMech 1.0 / 3.1 ([1.0](https://willcogley.notion.site/EyeMech-1-0-fee129fa32a443749f88524f53702f5a), [3.1](https://willcogley.notion.site/EyeMech-3-1-1af24779b64d80b19edfdd795d4b90e5)) | çift göz X/Y + 4 kapak | 1:1'e yakın | 6× MG90S önerilir | ball link + pushrod | düşük | ✓ kompakt, tamamen basılı. SG90 "zayıf" bulunmuş |
| Nilheim gözü / Berkeley ME102B ([PDF](https://edg.berkeley.edu/wp-content/uploads/2020/12/2020Fall_ME102B_gerhardtkatelyn.pdf)) | X, Y, kapak | — | 6× SG90 | sert tel | düşük | ✓ SG90 ile çalışmış |
| Robowaifu 1:1 baş ([MMF](https://www.myminifactory.com/object/3d-print-robowaifu-animatronic-head-1-1-human-sized-166251)) | göz pitch/yaw/roll | 1:1 | 4× MG90S | göz modülü 4× M2×12 ile tabana | — | ✓ göz tek alt montaj olarak sökülüyor |
| Salvius boynu ([spec](https://salvius.org/spec/v01/neck/)) | yaw + pitch | insan boyu | yaw servosu 25–35 kg·cm | büyük lazy susan, slip ring | — | ✓ ağırlığı rulman taşıyor |
| RobotShop Gen7 ([ürün](https://www.robotshop.com/products/animatronic-robotic-neck-mechanism-gen7-w-3-dofs)) | 3 DOF | 3 kg | 2× Actuonix lineer + HS-755MG | paralel lineer | ~$1695 | ✓ paralel eğme. ✗ pahalı |
| Disney patenti US5289273 ([PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5289273)) | yaw + 2 eğme | — | 1 doğrudan + 2 dolaylı servo | küresel mafsal | — | ✓ N2 mimarisinin öncülü |
| Patent US11440198 ([PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11440198)) | pitch/roll/yaw | — | 1 servo + 2 lineer aktüatör | — | ucuz (iddia) | ✓ döner eklem sayısını azaltıyor |
| Blitzway T-800 1:1 kafatası ([BBTS](https://www.bigbadtoystore.com/product/terminator-real-series-t-800-endoskeleton-skull-1_1-scale-limited-edition-replica-159745)) | baş eklemli (pasif) | 50 cm | — | — | koleksiyon | görsel referans |
| Agora T-800 1:2 ([Agora](https://www.agoramodels.com/jp/terminator-t-800)) | eklemler + RC çene | 95 cm, 6 kg, 650+ parça | — | — | — | görsel referans |
| 1984 T-800 propu ([CGW](https://www.cgw.com/Publications/CGW/2008/Volume-31-Issue-5-May-2008-/Man-vs-Machine.aspx)) | hidrolik | 1:1 | hidrolik piston | — | — | ✗ plastik üstü metalik kaplama soyuldu |

## 3. Mekanik iyi uygulamalar (bu projeye özel)
- **Servo yük taşımaz.** Yaw'da lazy susan, eğme mafsalında iki taraflı 608 ya da küresel mafsal, gözde iki taraflı pim.
- **Denge yayı** pitch statik yükünü karşılar; güç kesilince başın düşmesini önler.
- **Ağır servolar gövdede durur.** N2'de eğme servoları göğüste olur, kafada yalnız göz servoları (5× 9 g) kalır.
- **Basılı servo kolu ve spline:** `servo_kolu.mg996r_disk_kol_cebi()` ve `sg90_tek_kol_cebi()` **[TASLAK]**. Önce pay kuponu basılmalı.
- SG90 kulağında **M2** kullanılır (sablonlar/README), somunlu bağlantı tercih edilir (prensip 2).
- Göz modülü tek alt montaj olur ve birkaç vidayla takılır.

## 4. Kullanıcıya açık kararlar
| # | Karar | Seçenekler | Öneri |
|---|---|---|---|
| K1 | Boyun mimarisi | N1 seri yaw→pitch→roll (4 MG996R) · **N2** yaw + diferansiyel eğme (3) · N3 yaw + pitch (3) | **N2**: pitch yükü iki servoya bölünür, roll gelir, pushrod T-800 görüntüsü verir |
| K2 | Pitch pivotu ve sürüş | P2 kafatası tabanı + 2:1 (pay 2.12) · P3 AM'de + 1:1 (pay 3.0, ama "top gibi" döner) · P2 + 1:1 + yay (~1.9) | **P2 + 2:1 + denge yayı** (1.5 kg'da bile ≥1.5) |
| K3 | Göz/kapak servo sayısı | E1 3 · E2 4 · **E3 5** · E4 6 | **E3**: wink ve kısma var, 1 SG90 yedek kalır |
| K4 | Göz servosu tipi | SG90 (envanter) · MG90S (+581 ₺) | **SG90 ile başla**, boşluk kuponu kötü çıkarsa MG90S |
| K5 | Çene | J1 SG90 (pay 0.98 ✗) · **J3** MG996R + "yanak pistonu" pushrod (2.9) | **J3** |
| K6 | Kapak dili | metal "deklanşör" plaka · diyafram (iris) · insan formu | **Deklanşör plaka** |
| K7 | Metalik görünüm | M1 silk · M2 astar + sprey · M3 + Rub 'n Buff · M4 mat siyah + kuru fırça · M5 parça ayırma (silk kafa + gri göğüs) | **M5** (işlemsiz, prensip 6). Para yetmezse M4 |
| K8 | Göğüs formu | kapalı kabuk (1.0–1.5 kg) · **açık kaburga iskeleti** (0.5–0.7 kg) | **Açık iskelet** |
| K9 | Filament 2000 ₺'ye dahil mi, elde ne var? | — | kullanıcı bilgisi gerekiyor |
| K10 | PCA9685 #2 nerede | kafada (boyundan 4 tel geçer) · gövdede (15+ tel geçer) | **Kafada** |
| K11 | Bütçe paketi | **S1** envanter maksimum (~1050 ₺ + filament) · S2 MG90S gözler (~1630) · S3 seri boyun · S4 DS3218 (bütçe dışı) | **S1** |

## 5. Tek öneri
**S1:** N2 boyun (lazy susan yaw + 2× MG996R 2:1 pushrod diferansiyel eğme + denge yayı), J3 çene (MG996R, yanak pistonu), E3 göz (5× SG90, deklanşör kapaklar), açık kaburga göğüs, M5 görünüm, PCA #2 kafada. Plan aşamasında **önce üç kupon** basılmalı: MG996R tork/boşluk ölçümü, MG996R disk kol cebi, pushrod ball-link boşluğu.

## 6. Plan için riskler (rakamla)
| Risk | Bu projede | Rakam | Kritiklik |
|---|---|---|---|
| **Tork** | pitch ekseni | P2 + tek MG996R: pay 0.53. Önerilen düzen 1 kg'da 2.12, 1.5 kg'da 1.41. MG996R sürekli torku **ölçülmedi** (3.5 varsayım) | **1. sırada** |
| **Kablo** | ±70° yaw'dan geçiş | PCA kafada: 4 iletken, ≤3.3 A, 0.5 mm² ile ~0.1 V düşüm. Kafada değilse 15+ tel, ~8 mm demet. Servis halkası gerekir, uzatma kabloları alınacak | 2. sırada |
| **Tolerans zinciri** | göz bağlantıları ve kapak boşluğu | SG90 dişli boşluğu ~1–2° (**belirsiz**) + 2 ball-link + 2 pim (her biri 0.3 mm delik payı) → bakış hatası ±2–3° (**tahmin**). 1 m'de ~35–50 mm kayma. Kapak-göz radyal boşluğu ≥1 mm olmalı (küre ±0.2 + pim 0.3 + kapak ±0.2 + EKSENEL_BOSLUK 0.4). Boyunda 2:1 kol, MG996R boşluğunu başta yarıya indirir | 3. sırada |
| **Tabla** | 220×220×250 | Kafatası 200×155×230: XY'ye ancak sığar → en az 3 parça (kubbe / yüz / çene). Göğüs ~400 mm → en az 4 parça + omuz kapakları. Z 250 sorun değil | orta |
| **Montaj erişimi** | kafa içi göz servoları, yaw rulmanı vidaları | Göz modülü tek blok olmalı (4 vida). Kafatası kubbesi sökülebilir olmalı. Lazy susan vidalarına göğüs açıklığından tornavida koridoru gerekir. check_montaj baştan kurulmalı | orta |
| Vida envanteri | M3 yalnız 8/10/14 mm, havşa 15 mm. M4 havşa 2 adet | sıkışan kalınlık M3×14 ile ≤11 mm. Kafatası ek yerleri bu sınıra göre tasarlanmalı ya da uzun vida alınmalı (~200 ₺) | düşük |
| Güç | adaptör A, 3–4 MG996R | tipik 1.5–3.6 A, kötü durum 10 A > 5 A. Başlangıçlar kaydırılmalı + 1000 µF | düşük–orta |

## CP1.5 eki: hareketli kütle (2026-10-16)
Detay: `07_hafifletme.md`. Hesaplar tahmin, P2 pivotu, +30° öne eğim.
- **Kütle bütçesi:** S1 naif hali (2.5 mm duvar) **~810 g**. 1.2 mm kabuk + 1.6 mm kaburga ile **~490 g**. Gram kazancının neredeyse tamamı kabuktan geliyor (−320 g, tork −%40). **Hedef ≤ 500 g.**
- **Servo yerleri:** göz SG90'larını kafatası tabanına almak −0.24 kg·cm, çene MG996R'ını pivotun arkasına almak −0.24 kg·cm kazandırıyor. Çeneyi gövdeye alıp Bowden'la sürmek **daha az** kazandırıyor (−0.18), sürtünme getiriyor (verim ≤ ~%79) ve çene payını 2.3'e düşürüyor. **Bowden önerilmez.**
- **Yay:** pivot arkasında k ≈ 0.11 N/mm, ön yük ≈ 2.7 N. Statiğin ~%70'ini karşılar. Ölü karşı ağırlık için 216 g gerekirdi, önerilmez.
- **Yeni paylar (2× MG996R 2:1):** naif 2.99 → ince kabuk 4.99 → ince kabuk + servo yerleşimi 6.11 → + yay ~16. Yaylı düzende 1:1 sürüş bile ~8 pay verir (köşe kesme seçeneği).
- **Eye dersi:** Eye'da kağıt üstünde 2.3 pay pratikte yetmedi. Pitch için hedef **≥ 3 nominal**.
- **Öneri: H2:** ince kabuk + sahte detay, servolar pivotun yanında/arkasında, PCA oksipitalde, ayarlanabilir yay, 2:1 korunur. Yeni satın alma: yay seti ~50–150 ₺ (belirsiz).
