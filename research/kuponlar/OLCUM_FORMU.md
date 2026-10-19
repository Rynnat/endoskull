# Project Bust — Ölçüm formu (CP3a kuponları, PLAN §8)

Aletler: mutfak tartısı (~1 g), kumpas, cetvel, telefon slow-mo (240 fps), 5 V 5 A adaptör + PCA9685 (servo gücü adaptörden, GND ortak), multimetre SONRA (isteğe bağlı akım).
Her tabloyu doldur, en alttaki "Sonuç → plan kararı" satırını işaretle. Sonuçlar gelince CAD adım 0 (`params.py`) bunlarla başlar.

## Baskı
| Tabla | Kuponlar | Süre / filament (Orca CLI, Epic POC, PLA) |
|---|---|---|
| `out/tabla/tabla_1.stl` | K1, K2 MG kolları + M3 eklem, K3 | 12 sa 33 dk, 105 g |
| `out/tabla/tabla_2.stl` | K2 SG kolları, K4, K5, K7 | 9 sa 52 dk, 71 g |

Kupon başına: K1 6 sa 48 dk / 56 g · K2 3 sa 09 dk / 26 g · K3 3 sa 08 dk / 27 g · K4 2 sa 51 dk / 24 g · K5 4 sa 59 dk / 30 g · K7 1 sa 13 dk / 10 g.
Acil olanlar K1 ve K2 (tork ve pay kararları bunlara bağlı). Bunları önce basabilirsin: tek tek STL'ler `out/stl/` klasöründe.
- Destek yok. Tabla 2'de: uzun K5 tüpleri ve dil üstünde duran 2 kardan tüpü için Orca'da **brim 5 mm** aç.
- Her parçanın üstünde pay ya da varyant yazısı var (K5 kardan tüplerinin dilinde oyma "D" / "I").

## 0. Önce kumpasla ölç (modeldeki [TAHMIN] değerler)
| Ölçü | Modeldeki | Ölçülen |
|---|---|---|
| MG996R gövde en × boy (kulaksız) | 19.7 × 40.7 | |
| MG996R kulak delikleri: boy yönünde aralık / en yönünde aralık / çap | 49 / 10 / Ø4.5 | |
| MG996R mil ucu → kulak alt yüzü | 17.2 | |
| MG996R disk kol: çap / kalınlık / vida deliği yarıçapı | Ø21 / 2.0 / 7.5 | |
| SG90 tek kol: kalınlık / boy / göbek çapı / delik yarıçapı | 1.5 / 16 / Ø7.2 / 10 | |
| M3 rotil: göz kalınlığı / göz çapı / bilye merkezi → gövde ucu | 6 / Ø10 / 17 | |
| Kit kol delikleri M2 vidayı geçiriyor mu? (geçmiyorsa 2.0 mm matkapla aç) | — | |

K1 penceresi 19.9 × 41.1. Servo bundan büyük çıkarsa pencereyi eğe ile genişlet ve ölçtüğün değeri yaz.

## K1 — MG996R sürekli tork ve boşluk (2 servo: A, B)
Kurulum: Tutucuyu masa kenarına koy. Ön yüz masa kenarıyla aynı hizada olsun, ağırlıklar masanın dışına sarksın. Tabanı işkenceyle sık ya da üstüne ~2 L su koy. Servoyu arkadan pencereye sok, 4× M3×14 + somunla bağla. Disk kolu kolun cebine oturt, 2× M2×8 + somunla bağla, merkez vidasını tak. Servoya 1500 µs ver ve kolu yatay getir (kuyruk ucu kadranda "0").
Kolun kendi momenti ≈ 0.06 kg·cm. Kolu tartıp yaz: ___ g × 4.7 cm.

**Tork:** İpi + poşeti + suyu birlikte tart; bu toplam m. 100 mm deliğinden as, 60 s bekle. Bitince kol ile 110 çıkıntısı arasındaki boşluğu kumpasla ölç. Yüklü ve yüksüz ölçüm arasındaki fark ≤ 3.8 mm ise 2° koşulu tutar. Servo da elle tutulabilecek sıcaklıkta kalmalı. Ağırlığı 50 g adımlarla artır. 100 mm'de 1 kg'ı geçme, ağır yükleri 40 ya da 60 mm deliğine as.
Tork (kg·cm) = m (kg) × d (cm) + kolun kendi momenti.
| Servo | d (cm) | m (g) | 60 s sonra sarkma (mm) | sıcaklık (elle tutulur? E/H) | geçti? |
|---|---|---|---|---|---|
| A | | | | | |
| A | | | | | |
| B | | | | | |
| B | | | | | |
**Sürekli tork** = geçen en büyük değer: A ___ · B ___ kg·cm → küçük olan geçerli.

**Boşluk:** Kol yatayken servo güç altında beklesin. Kol ucunu ~200 g ile yukarı it, 110 çıkıntısına olan boşluğu ölç. Sonra aşağı it, yine ölç. 200 g kuvvetin ne kadar olduğunu tartıya bastırarak öğren. δ = fark (mm), boşluk ≈ δ × 0.52°.
| Servo | yukarı (mm) | aşağı (mm) | δ | boşluk (°) |
|---|---|---|---|---|
| A | | | | |
| B | | | | |
Not: Bu boşluğa kol cebinin payı da dahil (pay 0.2). K2'deki MG ölçümü cebin payını ayrıca verir.
Kol aşağı en çok −4°'ye iner, sonra çıkıntıya oturur. Bu bilerek konmuş bir durdurucu: kol çıkıntıya değdiyse o deneme GEÇMEDİ sayılır.

**Sonuç → plan kararı:** sürekli tork ≥ 3.5 → plan aynen · 2.5–3.5 → pitch en kötü payı yeniden hesaplanır (yay %85) · < 2.5 → C2 iptal + yatırma ±10° · boşluk > 1.5° → B yedeği (1.5:1, yatırma ±10°).

## K2 — Basılı kol cebi payı (0.1 / 0.2 / 0.3) ve dönen M3 eklem
MG kolları K1 tutucusunda (ölçüm çıkıntısı 50), SG kolları K4 tabanında (ölçüm direği 50) denenir. Kit kolu cebe oturt, M2×8 + somunla bağla. Servo 1500 µs'de güç altında beklesin. Kolun 50 mm noktasını ileri geri it, çıkıntıya ya da direğe olan boşluk farkını (δ) ölç.
| Kol | cebe girdi mi (sıkı / iyi / bol) | δ @50 mm (mm) | MG: 400 g @50 (2 kg·cm) 60 s, kalem izi kaydı mı? |
|---|---|---|---|
| MG 0.1 | | | |
| MG 0.2 | | | |
| MG 0.3 | | | |
| SG 0.1 | | | — |
| SG 0.2 | | | — |
| SG 0.3 | | | — |
SG90'da 2 kg·cm testi yok, çünkü SG90 kapasitesinin üstünde. SG cebinin tork altında kaymadığını K4 dolaylı gösterir.
**Sonuç:** Elle oturan **en küçük** pay ve δ < 0.3 mm → `toleranslar.py`'ye DOĞRULANDI olarak yazılır. MG için ___, SG için ___.

**Dönen M3 eklem:** Sabit bloğa alttan M3 somun göm. M3×10'u dönen koldan geçir. Sık, sonra ¼ tur geri al (kafa altında ~0.4 mm kalsın). Mümkünse vida sabitleyici kullan.
| Delik | elle serbest dönüyor mu | 30 mm çizgisinde yanal oynama (mm) |
|---|---|---|
| 3.3 | | |
| 3.4 | | |
**Sonuç:** Takılmadan dönen en az oynamalı delik → Z2/Z3 zincir halkası ve göz/kapak pimi.

## K3 — M3 rotil / pushrod boşluğu (2 adet metal M3 rotil + 90 mm M3 çubuk)
Rotil A direğe, rotil B kızağa gelir, her biri M3×14 ile ve somun alttan gömülü. Merkezden merkeze 90 mm olacak şekilde çubuğun iki ucuna rotil vida, kontra somunla kilitle.
**Eksenel boşluk:** Kızağı ~0.5 kg ile uca doğru it, sonra geri çek (0.5 kg'ı tartıya bastırarak öğren). Her iki durumda uç duvar ile kızak yüzü arasını kumpasın derinlik çubuğuyla ölç.
| itilmiş (mm) | çekilmiş (mm) | δ toplam | uç başına δ/2 |
|---|---|---|---|
| | | | |
**Açı sınırı:** B ucunu sök. Çubuğu A bilyesi etrafında yukarı kaldır, takıldığı açıyı plakadaki çizgilerden oku (çizgiler 5°'de bir).
| sınır açı (°) | |
|---|---|
**Sonuç → plan kararı:** uç başına > 0.15 mm → kafa kolu d = 35 mm (pushrod kulakları dışa). Açı sınırı → `strok.py` rotil açısı (şu an ±25° [T]).

## K4 — SG90 kapak hızı (1.5× bağlantı, açılı disk)
Kurulum: SG90'ı cebe oturt, uzak kulağa M2×8 vida tak, somunu yan kanaldan sür. Kranka SG90 kitinin tek kolunu oturt (pay 0.2). Diski pivota M3×14 ile tak; somunu direğin yan kanalından sür, sonra ¼ tur geri al. Krank ve disk tel deliklerini Ø1 tel ya da açılmış ataşla Z-büküp bağla (orta konumda tel boyu 40 mm). Servo 50° adım atınca disk ~79° döner (CAD: 1.57×).
Çekim: Telefon diskin üstünde, 240 fps. Servoya 50° adım komutu ver (~530 µs fark; diskteki çizgiden gerçek açıyı oku). Her yönde 5 tekrar al. Süre, hareketin başladığı kareden diskin durduğu kareye kadar: kare sayısı / 240 s.
| Yön | tekrar 1..5 (ms) | ortalama (ms) | diskte gerçek strok (°) |
|---|---|---|---|
| kapanma | | | |
| açılma | | | |
Not: Diskin ataleti gerçek kapağa yakın (disk 2.4 g, r 20; kapak ~3 g, r 14), bu yüzden sonuç biraz kötümser çıkar.
**Sonuç → plan kararı:** kapanma > 100 ms → kapak stroku 60°'ye iner ya da göz servoları MG90S olur (S2, +581 ₺).

## K5 — Teleskopik piston (PLA, radyal boşluk 0.4 / 0.5 / 0.6) ve kardan
Kayma kuvveti: Dış tüpü flanşı altta olacak şekilde tartının üstüne dik koy, darayı al. İç tüpü (flanşı üstte) yavaşça ve sabit hızla sonuna kadar it, en büyük okumayı yaz. Sonra dış tüpü 10° kamaya koy (flanş dudağa dayansın) ve aynı ölçümü yap. N = g / 102.
| Boşluk | düz: en büyük (g) | 10°: en büyük (g) | takılma / tutuk-kaygan (stick-slip) var mı | sallantı (iyi / bol) |
|---|---|---|---|---|
| 0.4 | | | | |
| 0.5 | | | | |
| 0.6 | | | | |
**Kardan örneği (0.5):** Her uçta 2 pim var, toplam 4× M3×14. Somunlar çatalın dışında kalsın; vidayı sıkma, kontra somun ya da nyloc kullan. Bağlantıyı iki eksende ±25° oynat ve iç tüpü kardanla birlikte sür.
| eklem iki eksende serbest mi | ±25°'de takılma | teleskop kardanla akıyor mu |
|---|---|---|
| | | |
**Sonuç → plan kararı:** takılmayan en küçük boşluk → P1/P2 borusu. 10°'de > 0.5 N (51 g) ya da stick-slip görülürse → alüminyum iç boru (Ø6×1, ~100 ₺). Kardan çalışırsa I27/I28 = M3 vida-pimli kardan.

## K7 — İnce kabuk paneli (60×60, 1.2 mm + 1.6×5 kaburga + M3 somun bossu)
| Ölçü | Değer |
|---|---|
| kütle (g), Orca tahmini 9.9 g | |
| g/cm² = kütle / 36 | |
| elle eğince (kabuk / kaburga yönü): esnek / sert / çatladı | |
| M3×8 kabuk tarafından, somun bossta: sıkınca somun döndü mü / boss çatladı mı | |
| kabuk yüzeyi düzgün mü (delik, çarpılma) | |
**Sonuç → plan kararı:** g/cm² → kütle bütçesinde (§5.1) kabukların gerçek gramı. Somun dönmez ve boss sağlam kalırsa boss ≥ 5 mm DOĞRULANDI. Çatlarsa boss Ø12 / 6 mm yapılır.

## Kupon için gereken parçalar
Envanterden: M3×14 ×11 (K1 4, K3 2, K4 1, K5 kardan 4) · M3×10 ×1 (K2) · M3×8 ×1 (K7) · M3 somun ×12 · M2×8 ×6 · servolar: MG996R ×2, SG90 ×1.
Satın: M3 rotil ×2 (PLAN'daki 8'in içinden) · M3 dişli çubuk (90 mm parça) · M2 somun ×6+ (envanterde yoksa) · Ø1 çelik tel (ya da ataş) · isteğe bağlı M3 nyloc ×4 (kardan).

## Hazır dosyalar (2026-10-17)
- G-code (Ender 3 Neo, Epic POC, PLA): `out/gcode/K1_tork.gcode` (6 sa 48 dk, 56 g) · `out/gcode/K2_K7.gcode` (K2 MG+SG kolları + M3 eklem + K7 panel; 4 sa 18 dk, 36 g). SD karta kopyala.
- Servo sürme: `firmware/k1_tork/k1_tork.ino` (Uno + Servo.h, sinyal D9; PCA gerekmez). Servo gücü 5 V 5 A adaptörden, GND ortak. Seri 115200: sayı = µs, +/- adım, c = 1500, d = bırak.
- Hesap: `k1_hesap.py` içindeki OLCUM / BOSLUK listelerini doldur → `python k1_hesap.py` sürekli torku ve plan kararını yazar.
