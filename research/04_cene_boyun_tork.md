# 04: Çene ve boyun: kütle, mimari, tork bütçesi

Tarih: 2026-10-16. Aşama 0. Karar yok.
Servo değerleri: **sürekli kullanılabilir tork** MG996R ≈ 3.5 kg·cm, SG90 ≈ 1.2 kg·cm (ajan tanımı). Hedef pay ≥ 1.5.
MG996R **ölçülmemiş**: `bilesenler.json` içinde yok, yalnız SG90 ve M3/M4 var. Datasheet değerleri: 9.4 kg·cm @4.8 V, 11 @6 V, kilitlenme akımı 2.5 A @6 V, çalışma akımı 0.5–0.9 A ([makerstore](https://www.makerstore.com.au/?p=3302)). Bir kullanıcının 4 cm kol üstünde ağırlıkla yaptığı testte maksimum ~10 kg·cm @6.6 V çıkmış ve boşluğu (free play) yüksek bulunmuş ([desertcart yorum](https://www.desertcart.ni/products/71405317)). **Plan aşamasında kumpasla ölçüm ve tork kuponu gerekiyor.**

## 1. Baş kütlesi tahmini
İnsan başı P50 manken değeri 4.9 kg ([Ball 2012, 3dbody](https://proc.3dbody.tech/papers/A2012/a12101_07ball.pdf)). Basılı endoskeleton kafası bunun çok altında kalır:

| Kalem | g (tahmin) |
|---|---|
| Kafatası kubbesi + yüz + çene (PLA, 2.5 mm duvar, %20–30 dolgu) | 400–600 |
| Göz modülü (5× SG90 ≈ 45 g + mekanizma) | 80–100 |
| Çene servosu kafadaysa (MG996R 55 g) | 0–55 |
| Vida, somun, kablo, LED, (kafada PCA9685) | 60–100 |
| **Toplam** | **~0.55–0.85 kg** |

Tasarım değeri **m = 1.0 kg**, kötü durum **1.5 kg** (kalın duvar, boya, ileride eklenecekler). Hepsi **(tahmin)**. CAD kütlesi çıkınca güncellenmeli.

## 2. Hedef açı aralıkları
İnsan ortalaması: fleksiyon ~56.5°, ekstansiyon ~69.5°, rotasyon ~72–74°/taraf, yana eğilme ~43° ([NeckCare tablosu](https://help.neckcare.com/range-of-motion-test)). Literatürde dağılım geniş ([boneandspine](https://boneandspine.com/range-motion-cervical-spine/)). Etkileşim büstü için öneri aralık **(tasarım tahmini)**: yaw ±60–70°, pitch ±25–30°, roll ±15–20°.

## 3. Boyun mimarileri

| | Yapı | MG996R | Artı | Eksi | Benzeri |
|---|---|---|---|---|---|
| **N1** seri | yaw (altta, lazy susan) → pitch (2× paralel) → roll (1×) | 4 | kontrol basit, eksenler bağımsız | kafada/boyunda 3 servo taşınır, uzun zincir boşluk biriktirir | InMoov ([hardware map](https://inmoov.fr/default-hardware-map/)), [Salvius](https://salvius.org/spec/v01/neck/) |
| **N2** yaw + diferansiyel eğme | yaw (lazy susan) + 2 pushrod'lu servo, üstte U-mafsal ya da küresel mafsal. Aynı yöne itiş = pitch, ters yöne = roll | 3 | iki servo pitch yükünü paylaşır. **Pushrod'lar T-800 "hidrolik"i gibi görünür.** Servolar gövdede, kafada değil | pitch ve roll bağlı (IK gerekir), roll kullanılınca pitch aralığı daralır | Disney patenti: 1 doğrudan yaw + 2 dolaylı eğme + küresel mafsal ([US5289273](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5289273)); RobotShop Gen7: 2 lineer + 1 döner, 3 kg, ~$1695 ([RobotShop](https://www.robotshop.com/products/animatronic-robotic-neck-mechanism-gen7-w-3-dofs)); 1 servo + 2 lineer ([US11440198](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11440198)) |
| **N3** 2 eksen | yaw + pitch (2× paralel), roll yok | 3 | en az risk | kafayı yana eğme (insanın "merak" hareketi) yok | Salvius |

Ortak kural: **servo yük taşımaz.** Yaw'da kafa ağırlığını lazy susan ya da büyük rulman taşır (Salvius da büyük lazy susan öneriyor). Eğme mafsalını iki taraflı yatak ya da küresel mafsal taşır, servo yalnız tork verir. Kablo: dönüş ±70° ile sınırlı olduğu için slip ring gerekmez, servis halkası (gevşek kablo payı) yeter. Salvius'un slip ring önerisi sürekli dönüş için.

## 4. Pitch tork hesabı (kritik eksen)
Formül: τ = m·g·L·sin(θ+φ) + I·α. Burada L, ağırlık merkezinin (AM) pivota uzaklığı; φ = atan(x/z), x = AM'nin öne kayması, z = AM'nin pivot üstündeki yüksekliği.
I = I_AM + m·L², I_AM ≈ 0.2·m·(0.10² + 0.115²) = 0.0046 kg·m² (elipsoid, m = 1 kg).
Profil: 30° hareket 0.5 s'de, üçgen hız profili → α = 4·0.524/0.25 = 8.4 rad/s². Kötü durum açısı θ = 30° öne.

| Pivot yeri (x, z) **(tahmin)** | L | statik (1 kg) | dinamik | **toplam 1 kg** | toplam 1.5 kg |
|---|---|---|---|---|---|
| **P1** boyun dibi, insan C7 benzeri (20, 150 mm) | 151 mm | 9.2 kg·cm | 2.4 | **11.6** | 17.4 |
| **P2** kafatası tabanı, C0–C1 benzeri (25, 70 mm) | 74 mm | 5.7 | 0.9 | **6.6** | 9.9 |
| **P3** AM'ye yakın, gimbal (10, 20 mm) | 22 mm | 1.9 | 0.4 | **2.3** | 3.5 |

Örnek P2 statik: 1.0 kg × 7.43 cm × sin(30° + 19.7°) = 5.67 kg·cm.

**Kapasite seçenekleri ve pay (1 kg / 1.5 kg):**

| Sürüş | Kapasite | P1 | P2 | P3 |
|---|---|---|---|---|
| C1: 1× MG996R doğrudan | 3.5 | 0.30 / 0.20 | 0.53 / 0.35 | **1.52** / 1.01 |
| C2: 2× MG996R paralel, 1:1 | 7.0 | 0.60 / 0.40 | 1.06 / 0.71 | **3.0 / 2.0** |
| C3: 2× MG996R, 2:1 kol (pushrod) | 14.0 | 1.21 / 0.80 | **2.12** / 1.41 | 6.1 / 4.0 |
| C2 + denge yayı (statik yükün ~%50'sini karşılar, **tahmin**) | 7.0 | — | **1.9** / 1.25 | — |

Sonuçlar:
- **Tek MG996R'yi doğrudan pitch'e bağlamak yalnız P3'te ve 1 kg'da çalışır.** İnsan gibi kafatası tabanında (P2) pivotlanan bir başta en az C3 ya da C2 + yay gerekir.
- 2:1 kol hızı yarıya indirir: MG996R yüksüz 0.17 s/60° (@4.8 V, datasheet) = 353°/s → başta ~176°/s yüksüz, yük altında daha az. 30°/0.5 s profili ortalama 60°/s ister, **yeterli.** Hızlı bakış dönüşlerinde (100–300°/s tepe, **belirsiz**) sınırda kalır. İnsansı yöntem: büyük bakış dönüşünde göz önce gider, baş sonra gelir (05). Yani başın hızlı olması şart değil.
- 2:1 geometri: kafada pushrod bağlantısı d = 40 mm, servo kolu r = 20 mm. Baş 25° dönünce strok 16.9 mm, servo ±58°. **Uygun.**
- **Denge yayı önerilir** (zorunlu değil). Güç kesildiğinde başın düşmesini önler, servo ısınmasını azaltır, 1.5 kg senaryosunda payı kurtarır.

## 5. Roll (N1/N2)
P2 pivotu, yana kaçıklık 0, 20° eğim: 1 kg × 7.0 cm × sin 20° = 2.4 kg·cm. Dinamik ~0.5 eklenince **~2.9 kg·cm**.
- N1 tek MG996R 1:1: pay 1.2 ✗
- N1 tek MG996R 2:1: pay 2.4 ✓
- N2 diferansiyel 2:1: kapasite ~14 → pay 4.8 ✓

## 6. Yaw
Ağırlığı rulman taşır, servo yalnız atalet ve sürtünmeyi yener.
I_yaw ≈ 0.2·1·(0.10² + 0.078²) + eğme servoları (2 × 55 g, r = 40 mm) ≈ 0.0036 kg·m².
- 60°/0.5 s → α = 16.8 rad/s² → 0.06 N·m = **0.62 kg·cm**
- 60°/0.3 s → α = 46.5 rad/s² → **1.7 kg·cm**
- Sürtünme ve kablo burulması: +0.2–0.5 **(tahmin)**

Toplam 0.8–2.2 kg·cm → tek MG996R ile **pay 1.6–4.4.** Salvius yaw için 25–35 kg·cm öneriyor ([Salvius](https://salvius.org/spec/v01/neck/)), ama o tasarım daha ağır. Rulman yoksa servo mili radyal yük taşır ve bu kural ihlali olur.

## 7. Çene
Basılı T-800 çenesi 80–120 g **(tahmin)**, AM menteşeden 50–60 mm uzakta.
- Statik: 0.12 × 6 = 0.72 kg·cm
- Dinamik (konuşma hızı, 20° açılma 0.1 s'de): I = 0.12·0.055² = 3.6e-4 kg·m², α = 140 rad/s² → 0.51 kg·cm
- **Toplam ≈ 1.2 kg·cm**

| Seçenek | Kapasite | Pay | Not |
|---|---|---|---|
| J1: SG90 | 1.2 | 0.98 ✗ | kapatma yayıyla ~1.5 olabilir, sınırda |
| J2: MG90S | 2.0 datasheet, sürekli ~0.75 **(MG996R oranıyla tahmin)** | ✗ / belirsiz | |
| J3: MG996R, boyun tepesinde ya da kafatası tabanında, pushrod = "yanak pistonu" | 3.5 | **2.9** ✓ | envanterden, T-800 görüntüsüne uyar |

InMoov çene için büyük bir servo (HK15298) kullanıyor ([inmoov neck & jaw](https://inmoov.fr/neck-and-jaw/)). Bir kurucu çene hareketinin 0–20° olduğunu söylüyor, ama kendisi de emin değil ([inmoov.fr/?p=406](https://inmoov.fr/?p=406)).

## 8. MG996R dağılımı (envanterde 6 adet)
- N1 + J3: 5 kullanılır, 1 yedek
- N2 + J3: 4 kullanılır, 2 yedek
- N3 + J3: 4 kullanılır, 2 yedek
