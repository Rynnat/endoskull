# 03: Göz mekanizması (yaw/pitch + üst/alt kapak)

Tarih: 2026-10-16. Aşama 0. Karar yok.

## 1. Açık kaynak örnekler

| Proje | Servo | Eksenler | Not | Kaynak |
|---|---|---|---|---|
| Will Cogley göz (2017) | 4 | göz X/Y + 2 kapak | Joystick ile kontrol, buton kırpıyor, pot varsayılan kapak açıklığını belirliyor. Gövde, kapak ve taban basılı, cıvatalı | [Hackster](https://hackster.io/news/creep-your-friends-out-with-this-3d-printed-eye-dd42d3434d7c), [Arduino blog](https://blog.arduino.cc/2017/04/24/scare-your-friends-with-a-3d-printed-animatronic-eyeball/trackback), [All3DP](https://all3dp.com/make-your-own-spooky-animatronic-eye-in-1-day/) |
| Cogley EyeMech 1.0 | — | X/Y + kapak | Servo ball-link ve pushrod kullanıyor; öncekinden daha kompakt ve sağlam | [Notion](https://willcogley.notion.site/EyeMech-1-0-fee129fa32a443749f88524f53702f5a) |
| Cogley EyeMech 3.1 | **6 mikro servo** | çift göz X/Y + 4 kapak | Tamamı basılabilir. **MG90S öneriyor** (SG90 ile güç arasında orta yol). Sayfa içeriği fetch ile okunamadı | [Notion](https://willcogley.notion.site/EyeMech-3-1-1af24779b64d80b19edfdd795d4b90e5) |
| Nilheim gözü (Berkeley ME102B) | 6× SG90 | X ×2, Y ×2, kapak | Servo kolları sert telle bağlanmış | [Berkeley PDF](https://edg.berkeley.edu/wp-content/uploads/2020/12/2020Fall_ME102B_gerhardtkatelyn.pdf) |
| Robowaifu 1:1 baş (Nilheim gözü) | 4× MG90S | pitch/yaw/roll | Göz modülü tabana 4× M2×12 ile bağlanıyor | [MyMiniFactory](https://www.myminifactory.com/object/3d-print-robowaifu-animatronic-head-1-1-human-sized-166251) (sayfa 403 verdi, yalnız arama özeti) |
| MakerWorld 2 eksen + kapak | göz başına 3 (MG90S/SG90) | X/Y + kapak | Kollar takılmadan önce servolar 90°'ye alınıyor | [MakerWorld](https://makerworld.com/models/2827337), [circuitdigest](https://circuitdigest.com/microcontroller-projects/diy-3d-printed-animatronic-eye-with-arduino) |
| InMoov | 2 küçük servo | göz X/Y | Standart haritada kapak yok | [inmoov.fr](https://inmoov.fr/default-hardware-map/) |

Ortak desen: **iki göz tek bir yaw ve tek bir pitch servosuna çubukla bağlanıyor.** Kapaklar ayrı servolarla sürülüyor. Servolar gözün arkasında, kafatası boşluğunda duruyor. Bağlantı ball-link ya da bükülmüş tel.

## 2. Boyut bütçesi (1:1)
- Göz küresi Ø24 mm **(belirsiz, genel anatomi)**. Göz bebekleri arası ~63 mm **(belirsiz)**. Kafatası boyu ~200 mm ([NCSU](https://www.ergocenter.ncsu.edu/wp-content/uploads/sites/18/2017/09/Anthropometric-Summary-Data-Tables.pdf)).
- SG90 **ölçülmüş** gövde: 22.5 × 12.5 × 22.7 mm, kulaklar dahil 32.0 mm, kablo mile yakın uçtan çıkıyor (`cq-ders/bilesenler.json`, `agent-flow/sablonlar/toleranslar.py`). Cep boyu 22.9 ve eni 12.7 olarak doğrulandı.
- Uyarı (sablonlar/README, Spider v1): SG90'ın uzak kulak deliği gövde ucuna 2.65 mm. M3 başı gövdeye biniyor, bu yüzden **kulakta M2** kullanılmalı. Envanterde M2×8 30 adet var.
- 5 SG90'ı yan yana dizmek ~5 × 13 = 65 mm × 32 mm × 23 mm hacim ister. Göz arkasında ~70–90 mm derinlik var **(tahmin)**. Kafatası boşluğuna rahat sığar, T-800 açık kafatasında servoların görünmesi de estetiğe uygun.
- MG90S, SG90 ile aynı gövde ölçüsünde, metal dişli ve ~2 kg·cm ([direnc.net](https://www.direnc.net/mg90s-servo-motor)). Ölçülmedi.

## 3. Seçenekler

| | Servo | Hareketler | Envanter | Artı | Eksi |
|---|---|---|---|---|---|
| **E1** | 3 SG90 | yaw, pitch, üst kapaklar (bağlı) | ✓ (3 yedek) | basit, kalibrasyonu az | göz kırpma (wink) yok, alt kapak yok, kısma tek boyutlu |
| **E2** | 4 SG90 | E1 + alt kapaklar (bağlı) | ✓ | kısma (squint) ve "gülümseyen göz" var | wink yok |
| **E3** | 5 SG90 | yaw, pitch, üst kapak sol, üst kapak sağ, alt kapaklar (bağlı) | ✓ (1 yedek) | wink ve asimetrik ifade var | kalibrasyon 5 eksen |
| **E4** | 6 (Cogley 3.1 gibi) | 4 kapak ayrı | SG90 ~6'nın tamamı, yedek yok | en ifadeli | yedek yok. Cogley MG90S öneriyor (+~700 ₺) |

## 4. Tork ve hız (SG90 sürekli 1.2 kg·cm)
- Göz: basılı küre ~5–8 g **(tahmin)**. Yük sürtünme ağırlıklı, tahminen ≤0.2 kg·cm. **Pay ≥ 6.** Kapak (~3–5 g, r≈14 mm) için yerçekimi yükü ihmal edilebilir. **Pay ≥ 5 (tahmin).** Burada tork sorun değil; **hız ve boşluk (backlash)** sorun.
- Hız: SG90 yüksüz 0.1 s/60° @4.8 V (datasheet) = 600°/s. İnsan 10° sakkadı 43 ms sürer (05_insansi_hareket.md). Servo 10°'yi ~17 ms + 50 Hz güncelleme gecikmesi (≤20 ms) ile yapar, toplam ≈ 40–60 ms **(tahmin)**. **Yeterli.**
- Kırpma: kapanma 75–100 ms. Kapak 60° dönüyorsa SG90 1:1 bağlantıyla 100 ms'de kapatır, tam sınırda. Bağlantı 1.5× büyütme verirse (servo 40° → kapak 60°) süre ≈ 67 ms olur. Bu durumda tork yükü 1.5 katına çıkar, ama zaten ihmal edilebilir düzeyde.
- Çözünürlük: PCA9685 50 Hz'de 20000/4096 = 4.88 µs/adım. SG90 ~10–11 µs/° **(datasheet aralığı 500–2400 µs, belirsiz)** → ~0.45°/adım. Ölü bant ~10 µs **(belirsiz)** → **~1°**. Sonuç: mikrosakkadlar (0.02–1°) fiziksel olarak **taklit edilemez**, yalnız simde yapılabilir.

## 5. İyi uygulamalar
- Göz küresi iki taraflı pim ya da gimbal halkasına yataklanmalı. Servo mili yükü taşımamalı, yalnız çubuğu itmeli.
- Kapak gözle eş merkezli dönmeli (pivot göz merkezinde). Böylece kapak-göz boşluğu sabit kalır, sürtme olmaz.
- Üst kapak dikey bakışı takip eder (insanda kapak-göz eşleşmesi, **belirsiz, kaynak yok**). Ayrı servo gerekmez, firmware'de `kapak = açıklık + k·pitch` ile yapılır.
- Basılı servo kolu (memory: feedback-servo-horn-bas): `servo_kolu.sg90_tek_kol_cebi()` **[TASLAK]**, önce pay kuponu basılmalı.
- Kamera: göz içi kamera hareketli bir referans çerçevesi demektir, takip döngüsünü karmaşıklaştırır. Göğüste ya da alında sabit webcam basittir (Eye v5 düzeni). Sim kararı: webcam.
- Göz rengi: T-800 kırmızı mercek. Envanterdeki LED seti göz arkasına konabilir, iris ayrı parça olarak basılır (prensip 6).
