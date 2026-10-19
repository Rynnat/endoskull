# Project Bust: PLAN (Agent Flow v2, aşama 1, G1 kapısı)

Tarih: 2026-10-17 · Planlayıcı · Kod/CAD yok.
Kaynaklar: KARARLAR.md, 01–07, kutle.py, konsept `modules/project-bust/v5/model.html` (DONDURULMUŞ), AKIS.md, `agent-flow/sablonlar`, `agent-flow/checks`, prensipler.
Project Angela dosyalarına bakılmadı.
Etiketler: **[T]** tahmin · **[H]** hesap (betik: konsept koordinatları + kütle tablosu) · **[K]** kaynak/datasheet · **[Ö]** ölçülmüş. **[Ö] olan tek değerler:** SG90 gövdesi ve cep payları, M3/M4 delik ve somun payları (sablonlar/toleranslar.py).
Koordinat (konseptle aynı, birim mm): +Y yukarı, +Z ileri (yüzün baktığı yön), +X büstün solu. Orijin: baş pivotu (U-mafsal merkezi), yaw tablası üst yüzünün **124 mm** üstü (PIVOT_Y = 12.4 cm).

> **ONAY BEKLİYOR (3 karar, §0).** Plan, kararlar için önerilen değerlerle yazıldı. Değişen kısımlar ayrıca işaretlendi.

---

## 0. Onay bekleyen kararlar

### A) H2 kabul mü? (öneri: **EVET, bir değişiklikle**) · ONAYLANDI (2026-10-17)
| | H1 (ince kabuk, yay yok) | **H2 (ince kabuk + servolar pivot çevresinde + yay)** |
|---|---|---|
| Kafa kütlesi | ~495 g [H] | ~495 g [H] (yay +3 g) |
| Eğme ihtiyacı, −25° (aşağı), 1:1 | 1.9 kg·cm [H] | **0.76** kg·cm (yay statiğin %75'ini alır) [H] |
| Pitch payı, 1:1, saf eğme | 3.3 | **8.3** |
| Pitch payı, en kötü (−25° eğme + 15° yatırma, krank 49°) | **1.9 ✗** (<3) | **3.7 ✓** |
| Güç kesilince | baş düşer | baş yaklaşık dengede kalır |
| Boşluk (backlash) | baş boşlukta yüzer | **%75 yayda 0.3–0.4 kg·cm net öne tork kalır, boşluk hep aynı tarafa yaslanır** (§6 Z3) |
| Maliyet | 0 | yay ~150 ₺ |

**Değişiklik:** 07 dosyası SG90'ları kafatası tabanına (x 15, z 15) alıyordu. Konsept v5 bunları göz arkasında alçak konuma koyuyor (ileri 37, yukarı 15). Fark sadece 0.1 kg·cm [H], buna karşılık göz çubukları kısalıyor (tolerans zinciri T1 daha iyi) ve taban hacmi rahatlıyor. **Konsept konumu korunur.**
Yay %100 değil **%75** dengeye ayarlanır. Sebep: boşluğun yaslanacağı yön kalsın.

### B) Pitch sürüşü 2:1 mi 1:1 mi? (öneri: **1:1**) · ONAYLANDI (2026-10-17)
Konseptten [H]: kafadaki etkin kol eğmede **d = 22.8 mm**, yatırmada **27.9 mm**. Servo krank açısı ≈ oran × (eğme + 1.23 × yatırma).

| | 2:1 (krank r 11.4) | **1:1 (krank r 22.8)** |
|---|---|---|
| −25° saf eğmede krank açısı | 61° (ölü noktaya yakın, cos 0.49) | 26° (cos 0.90) |
| −25° eğme + 15° yatırma | **imkânsız**: strok 17.2 mm > r 11.4 | krank 49°, mümkün |
| Krank ≤ 60° için izinli zarf | eğme + 1.23·yatırma ≤ 30° → −25° eğmede yatırma ≤ 4° | eğme + 1.23·yatırma ≤ 60° → tüm hedef zarf (−25..+20 × ±15) |
| Yaysız saf eğme payı | 3.6 | 3.3 |
| H2 yaylı en kötü poz payı | (zarf dışı) | 3.7 |
| Baş tepe hızı (yüksüz, 4.8 V) | ~176°/s | ~353°/s [K] |
| Servo boşluğunun başa yansıması | ½ | 1:1, ama yay tek tarafa yaslar |
| Hacim | küçük krank | Ø46 krank süpürmesi, yaw tablasında yer var |

**Gerekçe:** konsept geometrisinde 2:1, yatırmayı neredeyse tamamen yasaklıyor. H2 yayıyla 1:1 pay hedefini (≥3) karşılıyor.
**Yedek plan:** K1 kuponunda MG996R boşluğu > 1.5° çıkarsa 1.5:1'e geçilir ve yatırma ±10° ile sınırlanır (o zaman krank 54°).

### C) ~21° öne eğilme yeter mi? (öneri: **C1 tek pivot + C2 için arayüz rezervi**) · ONAYLANDI (2026-10-17)
| | **C1 tek pivot** | C2 boyun tabanına 2. eğme ekseni (+20°) |
|---|---|---|
| Aşağı eğilme, çene kapalı / açık | −21° / −8° (eğme–çene kilidiyle) [konsept] | −41° / −28° |
| 2. eksen torku (taban, φ 20° + baş 21–25°) | — | **3.9–4.6 kg·cm** [H] |
| Sürüş | — | 5. MG996R, **2:1** + yay (%75) → pay ~3.8 (flex tek yönlü, 2:1 geometrisi sorunsuz). Yaysız 2:1 pay ~1.5 ✗, yaylı 1:1 pay 2.2 |
| MG996R yedeği | 2 | **1** |
| Yaw'da dönen ek kütle | 0 | +~120 g (servo 55 + braket 40 + 2× 608) [T] |
| Basılı parça | 13 ana | +3 (taban çatalı, kolon alt yarısı, krank) |
| Satın alma | — | +~200 ₺ (2× 608, yay, 2 rotil, vida) [T] |
| Yeni riskler | — | çene ↔ manubrium/köprücük çakışması, taban–baş IK bağlaşımı, pushrod'ların taban eğilmesinde hareket etmesi (eğme servoları flex çerçevesine taşınmalı) |

**Gerekçe:** büst masada duruyor, ziyaretçiler ayakta. Takip çoğunlukla **yukarı** bakmayı (+20°, kilitsiz) gerektiriyor. Aşağı bakış ihtiyacı küçük (göz pitch'i ±24° ekler). C2 hareketli kütleyi ve risk sayısını artırıyor.
**Rezerv:** N1–N2 arayüzü tek bir flanş (4× M3, Ø40 daire) olur. C2 istenirse araya flex modülü girer, başka parça değişmez.
**C2 seçilirse planda değişenler:** P-listesi +3 parça; arayüz +1 satır (flex ekseni, 2× 608 + M8 [T]); montajda adım 7a; tork tablosuna satır T-C2; kontrol matrisinde chin–göğüs taraması tüm φ × yaw × pitch kombinasyonlarına genişler; BOM +200 ₺.

---

## 1. Spec
| Eksen | Aralık | Sürüş | Not |
|---|---|---|---|
| Yaw (boyun dönüşü) | ±70° | 1× MG996R doğrudan + Oldham benzeri kaplin, yükü lazy susan taşır | servis halkası, slip ring yok |
| Pitch (baş eğme) | −25° (aşağı) .. +20° (yukarı) | 2× MG996R 1:1 pushrod (diferansiyel), U-mafsal, yay | **aşağı sınır = çene kilidi** (çene kapalıyken −21°, açıkken −8°) |
| Roll (yatırma) | ±15° | aynı 2 servo, ters yönde | krank ≤ 60° zarfı firmware'de |
| Çene | 0..20° açılma | 1× MG996R, pivotun arkasında (−32, +26), rod + rotil, kondilin arkasındaki kol r = 20 mm | konuşma 4–6 Hz [T] |
| Göz yaw / pitch | ±32° / ±24° | 2× SG90 (iki göz bağlı), çubuk | sakkad D = 2.2A + 21 ms [K] |
| Üst kapak sol / sağ | strok ≤ 75° (konseptteki 135° indirildi, §10 R4) | 2× SG90, 1.5× bağlantı | kapanma ≤ 100 ms |
| Alt kapaklar (bağlı) | ≤ 40° | 1× SG90 | |
| Hareketli baş kütlesi | **≤ 500 g** (bütçe 495 g, §5) | | kötü durum +%30 = 645 g |
| Ölçek | 1:1. Kafatası 144 (en) × 148 (yük.) × 188 (boy), omuz 408, kaide elips 340 × 180 | | konsept CR yarıçapları |
| Güç | 2× 5 V 5 A. A: MG996R ×4 (PCA#1, göğüste). B: SG90 ×5 (PCA#2, kafada, oksipital) | | boyundan 4 iletken geçer |

---

## 2. Parça listesi
Malzeme: PLA (yapısal), PETG (piston boruları, kapaklar). "Kabuk" = 1.2 mm duvar + 1.6 × 5 mm kaburga (07 §4). Kütleler **[T]**, CAD hacmi ve K7 kuponuyla güncellenir.

| ID | Parça | İşlev | Grup (hareket) | Şablon / yeni | Boyut (mm) [T] | Kütle (g) | Tabla 220 | Baskı yönü |
|---|---|---|---|---|---|---|---|---|
| **B1** | Kafatası şasisi | U-mafsal kafa kulakları (roll ekseni), 5× SG90 cebi, çene MG996R cebi, PCA#2 kulakları, yay kancası, 2 rotil kulağı | baş | YENİ + `sg90_cebi`, `somun_tuzagi`, `vida_pim_eklemi("M4")` | 130 × 110 × 45 | 40 | ✓ | taban plakası tablada |
| **B2** | Yüz önü | kaş, göz çukuru kenarı, elmacık, maksilla + üst dişler, yanak pistonu üst kulağı | baş | YENİ (kabuk) | 150 × 110 × 95 | 75 | ✓ | arka açık yüz tablada |
| **B3L/B3R** | Kubbe sol/sağ | sagital dikişten bölünmüş (konsepteki "sag" dikiş çizgisi ek yerini gizler), şakak yarıkları, sahte cıvata başları | baş | YENİ (kabuk) | 188 × 148 × 75 (her biri) | 55 + 55 | ✓ (188) | kesit yüzü tablada, tepede ağaç destek |
| **B4** | Alt çene | mandibula + alt dişler, kondil yatakları, kondil arkasındaki kol (20 mm) | çene | YENİ + `vida_pim_eklemi("M4")` | 135 × 90 × 75 | 45 | ✓ | diş sırası yukarı |
| **B5** | Göz modülü (alt montaj) | B5a çerçeve, B5b küre ×2 (Ø24 [T], içi boş), B5c iris/lens ×2 (kırmızı, ayrı renk, prensip 6), B5d üst kapak ×2 (0.8 mm PETG), B5e alt kapak çifti ×1, B5f basılı SG90 kolu ×5 | baş | YENİ + `sg90_tek_kol_cebi` [TASLAK→K2] | çerçeve 90 × 40 × 35 | 40 toplam | ✓ | çerçeve tabanı tablada |
| **N1** | Yaw üst tablası | lazy susan üst halkası, 2 eğme MG996R cebi, N2 flanşı (C2 rezervi), yay alt kancası, SCM alt mafsalları, kablo kancası | yaw | YENİ | Ø124 × 35 | 60 | ✓ | alt yüz tablada |
| **N2** | Boyun kolonu | C7–C1 omur görünümlü taşıyıcı + üstte pitch çatalı (X ekseni, M4 pim) | yaw | YENİ | 50 × 40 × 115 | 50 | ✓ | dik |
| **N3** | U-mafsal haçı | pitch (X) ve roll (Z) eksenleri, 2× M4 pim | haç | YENİ + `vida_pim_eklemi("M4")` | 28 × 28 × 22 | 10 | ✓ | yan |
| **N4** | Eğme krankları ×2 | MG996R disk kol cebi, r = 22.8 (1:1), M3 rotil deliği | eğme servoları | `mg996r_disk_kol_cebi` [TASLAK→K2] | 55 × 20 × 8 | 6 + 6 | ✓ | düz |
| **N5** | Pushrod kılıfı ×2 | gerçek M3 rod üstünde sabit "hidrolik" kılıf (Ø11, 0.8 mm), teleskopik değil | yaw–baş | YENİ | Ø11 × 60 | 2 + 2 | ✓ | dik |
| **P1** | SCM pistonu ×2 (kozmetik) | teleskopik dış + iç boru (PETG), uçlarda basılı küresel mafsal (§2.1) | yaw ↔ baş | YENİ | dış Ø10, iç Ø6.4 | 4 + 4 | ✓ | dik |
| **P2** | Yanak pistonu ×2 (kozmetik) | teleskopik, B2 ↔ B4, strok 8 mm [H] | baş ↔ çene | YENİ | Ø8 × 80 | 3 + 3 | ✓ | dik |
| **G1** | Göğüs merkezi | manubrium, sternum üstü, T1–T5, boyun yuvası, lazy susan alt halkası, yaw MG996R cebi, PCA#1 + Uno | sabit | YENİ | 170 × 120 × 130 | 120 | ✓ | taban tablada |
| **G2L/G2R** | Kaburga + köprücük + kürek + omuz başı | sol/sağ yarı (omuz başı birleşik, x 18→204) | sabit | YENİ | 186 × 120 × 120 | 90 + 90 | ✓ (186) | iç yüz tablada |
| **G4L/G4R** | Kaide yarıları | eliptik kaide 340 × 180 ikiye, DC jak, adaptör kablo çıkışı | sabit | YENİ | 170 × 180 × 30 | 150 + 150 | ✓ | düz |
| **Y1** | Yaw kaplini | MG996R disk kol cebi + 2 pim, N1'deki radyal yarıklara girer (Oldham benzeri, ≥ 0.7 mm radyal tolerans alır) | yaw | `mg996r_disk_kol_cebi` [TASLAK] | Ø40 × 10 | 6 | ✓ | düz |
| **Ç1** | Çene krankı | MG996R disk kol cebi, r 20 | çene servosu | aynı | 40 × 15 × 6 | 3 | ✓ | düz |

**Sayım:** 13 ana yapısal baskı (B1, B2, B3L, B3R, B4, N1, N2, N3, G1, G2L, G2R, G4L, G4R) + ~27 küçük parça (göz kiti 11, krank/kaplin 4, piston borusu 8, kılıf 2, mafsal başları).
**> 10 gerekçesi:** 1:1 ölçek ve 220 tabla (kafatası 188, omuz 408, kaide 340 bölünmek zorunda), prensip 6 (iris ayrı renk), kozmetik pistonlar kütle için ayrı ve ince basılıyor. Her ana parça zaten birden fazla işlevi birleştiriyor (B1 6 işlev, N1 6 işlev).

### 2.1 Kozmetik pistonlar (kullanıcı sorusu)
| Konu | Değer |
|---|---|
| Yapı | iki teleskopik boru: dış Ø10 / et 0.8, iç Ø ≈ 7.6 − 2 × boşluk, et 0.8, içi boş. PETG. Uçlarda basılı küresel mafsal (Ø8 bilye + 0.3 pay soket [T→K5]). Seçenek: M3 rotil (+3 g/uç, ₺). |
| Radyal boşluk | 0.3 / 0.4 / 0.5 mm → **K5 kuponu seçer** (0.3–0.4 hedef) |
| **Konseptteki SCM yeri** (baş ucu x 66, z −56, alt uç yaw 58, −16) | Tüm pozlarda boy 92.6 → 163.6 mm, **strok 71 mm** [H]. İki kademeli borunun bindirmesi 4 mm'ye düşer, **olmaz.** |
| **Önerilen yer** (baş ucu mastoid altı ≈ (±55, −10, −20), anatomik SCM yapışma yeri) | boy 95.3 → 135.3, **strok 40 mm** [H]. Borular 70 + 70, en uzun pozda bindirme 21 mm ✓. Konsept dersi (pistonlar ramusun ARKASINDAN geçmeli) korunur. CAD adım 7'de çakışma taramasıyla doğrulanır. |
| Yanak pistonu P2 | 82.5 → 90.5 mm (çene 0..20°), strok 8 mm [H], sorunsuz |
| Strok sınırı = **gizli kilit** | her uçta ≥ 3 mm pay. YENİ check `strok.py` tüm poz ızgarasında ölçer (§7) |
| Kütle | SCM 2 × 4 g (yarısı başa, bütçede 8 g), yanak 2 × 3 g (tamamı başta). PETG boru [H]: Ø10 × 0.8 × 70 → 2.0 g |
| Sürtünme | SCM 0.3 N/adet [T→K5] × kol ~20 mm → pitch'e 2 × 0.06 = **0.12 kg·cm**. Yanak 0.3 N × 40 mm → çeneye 2 × 0.12 = 0.24 kg·cm. Tork bütçesinde var (§5) |
| **Seçenek: iç boru alüminyum** | Ø6 × 1 Al boru, 70 mm = 3.2 g (PETG 1.0 g). **Başa binen +2.2 g/adet**, sürtünme μ PETG–Al ~0.2–0.3, PETG–PETG ~0.3–0.5 [T]. Gerçek metal parlaklığı verir. Maliyet ~100 ₺ (1 m) [T]. **Öneri:** PETG ile başla. K5'te kayma kuvveti > 0.5 N ya da yapışma-kayma (stick-slip) görülürse Al'ye geç. |

---

## 3. Arayüz tablosu
Paylar (prensip 1): M3 serbest 3.3, M4 4.3 [Ö]; somun cebi AF + 0.3 / t + 0.2 [Ö]; SG90 cebi 22.9 × 12.7 [Ö]; eksenel boşluk 0.4 [Ö, vida_pim_eklemi M4]. Diğerleri kuponla belirlenir.

| # | Çift | Bağlantı | Vida / eleman | Delik / pay | Dönen |
|---|---|---|---|---|---|
| I1 | G4L ↔ G4R | yan bindirme + yapıştırma + vida | 4× M3×14 + somun | 3.3 / somun tuzağı | — |
| I2 | G1 ↔ G4 | alttan vida | 4× M3×14 + somun | 3.3 | — |
| I3 | G2L/R ↔ G1 | dil-yuva + vida | 3× M3×14 her yan | 3.3 | — |
| I4 | lazy susan alt halkası ↔ G1 | vida | 4× M3×14 [T: halka deliği Ø4, K8] | 3.3 | — |
| I5 | yaw MG996R ↔ G1 | kulak vidası | 4× M4×20 [T: MG996R kulak deliği, K1'de ölçülür] | 4.3 | — |
| I6 | Y1 ↔ servo mili | disk kol cebi + merkez vida | MG996R merkez vidası | K2 payı | servo |
| I7 | Y1 ↔ N1 | 2 pim, N1'deki radyal yarıklarda (Oldham) | basılı pim Ø4 | yarık 4.4 genişlik, ±1 mm radyal | N1 |
| I8 | lazy susan üst halkası ↔ N1 | vida | 4× M3×14 | 3.3 | N1 |
| I9 | eğme MG996R ×2 ↔ N1 | kulak | 8× M4×20 | 4.3 | — |
| I10 | N4 ↔ servo | disk kol cebi + merkez vida | — | K2 | N4 |
| I11 | N4 ↔ pushrod ↔ B1 | M3 rotil ×2 / rod + M3 dişli çubuk (boy ayarlı + kontra somun) | 2× M3×14 + somun her uç | rotil boşluğu K3 | rotil |
| I12 | N2 ↔ N1 | flanş (C2 rezervi) | 4× M3×14, Ø40 daire | 3.3 | — |
| I13 | N2 ↔ N3 (pitch, X ekseni) | `vida_pim_eklemi("M4")` | 1× M4×40 + somun [satın alma] | sabit 3.3 diş açar / dönen 4.3, eksenel 0.4 | N3 |
| I14 | N3 ↔ B1 (roll, Z ekseni) | `vida_pim_eklemi("M4")` | 1× M4×40 + somun | aynı | B1 |
| I15 | yay ↔ B1 / N1 | kanca + 3 ayar deliği (±8 mm) | — | Ø2 tel kanca | — |
| I16 | SG90 ×5 ↔ B1 | `sg90_cebi` + uzak kulak | 5× M2×8 + M2 somun | M2 2.3 [TASLAK] | — |
| I17 | B5 ↔ B1 | göz modülü tek blok | 4× M2×8 (somunlu) | 2.3 | — |
| I18 | göz küresi ↔ B5a | iki taraflı pim (göz yaw: dikey, göz pitch: gimbal halkası) | M3 vida-pim | `vida_pim_eklemi("M3")` [TASLAK→K2] | küre |
| I19 | kapak ↔ B5a | **göz merkeziyle eş eksenli** pim | aynı M3 ekseni | aynı | kapak |
| I20 | SG90 kolu ↔ göz/kapak | Ø1 çelik tel Z-bükümü | — | tel deliği 1.3 [T] | — |
| I21 | çene MG996R ↔ B1 | kulak | 4× M4×14 | 4.3 | — |
| I22 | B4 ↔ B1 (kondil, X ekseni) | `vida_pim_eklemi("M4")` ×2 | 2× M4×20 | eksenel 0.4 | B4 |
| I23 | Ç1 ↔ rod ↔ B4 kolu | M3 rotil ×2 | 2× M3×14 | K3 | rotil |
| I24 | PCA#2 ↔ B1 | ara direk | 4× M3×8 + somun | 3.3 | — |
| I25 | B2 ↔ B1 | önden vida, şasi bossunda somun | 4× M3×14 | boss ≥ 5 mm | — |
| I26 | B3L/R ↔ B1 + B2 + birbiri | sagital bindirme kaburgası 1.6 mm + vida | 6× M3×10 her yarı | 3.3 | — |
| I27 | P1 ↔ B1 / N1 | basılı küresel mafsal (geçme + M3 tutucu) | 2× M3×10 | soket K5 | — |
| I28 | P2 ↔ B2 / B4 | aynı | 2× M3×10 | K5 | — |

---

## 4. Montaj sırası (sökme = tersi)
Yön = parçanın **hareket** vektörü (montaj_sokme parçalı yol olarak). Alet yönü = tornavidanın uçtan giriş yönü.

| Adım | Parça | Takma yolu | Alet (vida girişi) | Not |
|---|---|---|---|---|
| 1 | G4L + G4R | G4R sabit, G4L (−X) | alttan (+Y) | I1 |
| 2 | G1 | (0, −1, 0) | alttan (+Y), kaide altı açık | I2 |
| 3 | yaw MG996R | (0, −1, 0) cebe | üstten (−Y) | I5. Kablo G1 içinden PCA#1'e |
| 4 | lazy susan alt halkası | (0, −1, 0) | üstten (−Y), üst halkanın erişim deliğinden | I4. giris_yolu ölçecek |
| 5 | Y1 kaplin | (0, −1, 0) mile | üstten | servo 90° nötrde |
| 6 | G2L / G2R | (−1,0,0) / (+1,0,0) | yandan (∓X) ve alttan | I3 |
| 7 | **Boyun alt montajı (tezgâhta):** N2 → N1 (I12, alttan +Y; somunlar N2 flanşında), eğme MG996R ×2 → N1 (−Y), N4 ×2 nötrde | — | — | — |
| 7a | (yalnız C2) flex modülü N1 ile N2 arasına | (0, −1, 0) | yandan | C2 |
| 8 | Boyun alt montajı → lazy susan üst halkası | (0, −1, 0), Y1 pimleri N1 yarıklarına | üstten (−Y), 4 vida servo izdüşümü dışında (r 50, ±45°) | I8 |
| 9 | **Baş alt montajı (tezgâhta):** SG90 ×5 → B1 (−Y), B5 göz modülü (−Y, 4× M2 alttan), çene MG996R (−X), PCA#2 (−Y), B4 çene (−Y, kondil pimleri ±X'ten), Ç1 + rod | — | — | kubbe ve yüz takılmamış |
| 10 | N3 haç → N2 çatalı | (0, −1, 0) çatala, M4 pim (−X) | soldan (−X) | I13 |
| 11 | Baş (B1 alt montajı) → N3 | (0, −1, 0), M4 pim (−Z) | arkadan (−Z), kubbe yokken | I14 |
| 12 | Pushrod ×2 (I11), yay (I15), SCM pistonları P1 (I27) | aşağıdan yukarı | yandan (±X) | Rod boyu: baş 0°/0° iken servolar 90° |
| 13 | Kablo: 4 iletken + servis halkası | — | — | kablo check |
| 14 | B2 yüz | (0, 0, −1) şasiye | önden (−Z), göz çukurlarından | I25 |
| 15 | Yanak pistonları P2 | yandan | (±X) | I28 |
| 16 | B3L / B3R | (−1,0,0) / (+1,0,0) | yandan, şakak pencerelerinden | I26. Servis için ilk sökülen |

Kural: kubbe yarıları (16) ve yüz (14) sökülünce **tüm** servo vidalarına erişilebilmeli (giris_yolu check).

---

## 5. Kütle ve tork bütçesi

### 5.1 Hareketli baş kütle bütçesi (hedef ≤ 500 g)
Konum: pivota göre (ileri x, yukarı z), mm. Konum konseptten okundu.

| Kalem | Bütçe g | Kaynak | Konum (x, z) | Nasıl kesinleşir |
|---|---|---|---|---|
| B3L + B3R kubbe | 110 | [T] | (−5, 90) | CAD hacmi × K7 g/cm² |
| B2 yüz | 75 | [T] | (62, 20) | aynı |
| B4 çene | 45 | [T] | (45, −50) | aynı |
| Sahte detay (kabuğa entegre) | 10 | [T] | (30, 50) | aynı |
| B1 şasi | 40 | [T] | (22, −2) | aynı |
| B5 göz modülü (basılı) | 40 | [T] | (77, 30) | aynı |
| 5× SG90 | 45 | [K] 9 g | (37, 15) | **tartı** |
| Çene MG996R + Ç1 | 60 | [K] 55 g | (−32, 26) | **tartı** |
| PCA#2 | 10 | [K] | (−72, 52) | tartı |
| Vida + somun (~15 takım + M2) | 22 | [H] | dağınık | vida_adet listesi |
| Kablo + LED | 15 | [T] | (10, 30) | tartı |
| Rotil kafa ucu ×2 | 6 | [T] | (−26, −6) | tartı (K3) |
| Yay kafa ucu | 3 | [T] | (−64, −2) | — |
| SCM piston yarısı ×2 | 8 | [H] | (−20, −10) | K5 |
| Yanak pistonu ×2 | 6 | [H] | (55, −10) | K5 |
| **Toplam** | **495** | | **AM (19.8, 29.6)**, I = 0.00268 kg·m² [H] | YENİ `kutle_butce` check |

### 5.2 Tork bütçesi
Servo **sürekli** kapasitesi: MG996R 3.5, SG90 1.2 kg·cm. **İkisi de [T]**, K1 kuponu MG996R'ı ölçecek. Dinamik yük: 30°/0.5 s, α = 8.4 rad/s². Hedef pay ≥ 1.5, **pitch için ≥ 3**.

| Eksen | Dönen kütle / CG kolu | Gereken (kg·cm) | Kapasite | **Pay** | Durum |
|---|---|---|---|---|---|
| Pitch −25°, yay %75, saf eğme | 495 g, AM 36 mm | 0.38 statik + 0.23 dinamik + 0.15 sürtünme = **0.76** [H] | 2 × 3.5 × cos 26° = 6.3 | **8.3** | ✓ |
| Pitch, en kötü (−25° + 15° yatırma), yay %75 | aynı | en yüklü servoda 0.94 | 3.5 | **3.7** | ✓ |
| Pitch, yay yok/kırık, saf eğme | | 1.9 | 6.3 | 3.3 | ✓ |
| Pitch, yay yok, en kötü | | en yüklü servoda 1.80 | 3.5 | **1.9** | ✗ → firmware yay sensörsüz; yay çıkarsa zarf −25° eğmede yatırma ≤ 5° |
| Pitch, +%30 kütle, yay %75, en kötü | 645 g | 1.15 | 3.5 | 3.0 | sınırda ✓ |
| Roll ±15° | AM 29.6 mm yukarıda | 0.38 + 0.2 = 0.58 → servo başına 0.24 | 3.5 | > 10 | ✓ |
| Yaw, 60°/0.5 s … 60°/0.3 s | ~765 g lazy susan üstünde, I ≈ 0.0019–0.0025 [H] | 0.33–0.92 + sürtünme 0.2–0.5 [T, K8] + kablo 0.1 = 0.6–1.5 | 3.5 (doğrudan) | **2.3–5.8** | ✓. Servo radyal yük taşımaz (Y1 Oldham) |
| Çene 0..20°, 0.1 s | 45 g, kol 35–54 mm (baş −25°'de) | 0.24 statik + 0.32 dinamik + 0.24 yanak pistonu = 0.8 | 3.5, kol 1:1 (r 20) | **4.4** | ✓ |
| Göz yaw / pitch | küre ~5 g ×2 + çubuk | ≤ 0.2 [T] | 1.2 | ≥ 6 | ✓ (tork değil, hız ve boşluk kritik) |
| Üst kapak (1.5× bağlantı) | 3 g, r 14 | (0.02 + 0.1 sürtünme) × 1.5 = 0.18 [T] | 1.2 | 6.7 | ✓. Hız: 50°/600°/s = 83 ms + 20 ms kare → **~100 ms, sınırda (K4)** |
| T-C2 (yalnız C2) taban flex 20° + baş 21–25° | ~1 kg, AM ~80–90 mm önde | 4.6 (yaysız) / 1.6 (yay %75) | 3.5 × ~1 (1:1) | 0.8 ✗ / **2.2** (2:1'de 3.8) | C2 için 2:1 + yay şart (flex tek yönlü, 2:1 geometrisi sorunsuz) |

**Yay [H]:** konsept bağlantısı (baş −64, −2 ↔ yaw tablası −44, +9). Boy 92.5 mm (+20°) → 114.8 (0°) → 141 mm (−25°), yani **48.5 mm uzama aralığı**. %100 denge için k = 0.047 N/mm, F0 = 1.58 N (0°'de). %75 için k ≈ 0.035 N/mm, F0 ≈ 1.2 N.
Uzun ve yumuşak bir çekme yayı gerekiyor: serbest boy ~80 mm, ≥ 61 mm uzama [T]. **K6 ölçer.** Yay bulunamazsa misina + makara + kısa yay ("sıfır boylu yay", 07 §5) yedek plan.

---

## 6. Kritik tolerans zincirleri (tolerans.py girdisi)
Format: halka: nominal ± pay. En kötü = Σ|pay|, RSS = √Σpay².

| Zincir | Halkalar | Nominal | En kötü | RSS | Eşik |
|---|---|---|---|---|---|
| **Z1 göz merkezleme** (küre ↔ B2 göz çukuru kenarı, radyal) | B2–B1 vida (±0.15) · B5–B1 M2 (±0.15) · küre pimi (±0.15) · küre Ø (±0.10 radyal) · baskı konumu 3 parça (±0.10 ×3) | boşluk 1.5 | 1.5 − 0.85 = **0.65** | 1.5 − 0.32 = **1.18** | ≥ 0.4 ✓ |
| **Z2 kapak–göz** (radyal, eş eksen) | küre r (±0.10) · kapak iç r (±0.10) · küre pimi (±0.15) · kapak pimi (±0.15) · eksen kaçıklığı (±0.10 ×2) | 1.2 | 1.2 − 0.70 = **0.50** | 1.2 − 0.29 = **0.91** | ≥ 0.3 ✓. Pim [TASLAK M3]. K2'de dönen M3 eklemi ölçülür |
| **Z3 diferansiyel pushrod → baş açısı** | MG996R boşluğu ±0.75° → r 22.8'de ±0.30 [T, K1] · kol cebi ±0.3° → ±0.12 [T, K2] · rotil ×2 ±0.10 [T, K3] · U-mafsal M4 (0.15 radyal / 16 mm kol → ±0.11) · rod boyu (kalibrasyonla 0) | 0 | ±0.73 mm → **±1.8°** | ±0.37 → ±0.9° | ≤ ±1° hedef. **Yay ön yükü (%75) boşluğu tek tarafa yaslar → etkin yaklaşık yarısı [T].** K3 > 0.15/rotil çıkarsa kafa kolu d 22.8 → 35 mm (açı ×0.65) |
| Z3b sol/sağ rod uyumsuzluğu → roll hatası | rod boy farkı ±0.2 (kontra somun) · krank r farkı ±0.1 | 0 | ±0.3 / 27.9 → ±0.6° | ±0.4° | ≤ 1° ✓ |
| **Z4 yaw tablası** (servo mili ↔ lazy susan ekseni, radyal) | G1 servo cebi konumu (±0.10) · cep payı (±0.20) · spline eksen kaçıklığı (±0.10 [T]) · lazy susan merkezleme (±0.15) · N1 merkezleme (±0.15) | 0 | **±0.70** | ±0.33 | Y1 Oldham yarığı ≥ ±1.0 → servo yanal yük almaz ✓ |
| Z4b yaw tablası sallantısı | lazy susan eksenel oynaması ±0.2 [T, K8] / Ø100 → ±0.23° → göz hizasında (154 mm) ±0.6 mm | — | ±0.6 mm | — | bilgi |
| Z5 SCM strok | min/maks boy ± (küresel mafsal 0.3 ×2 + baskı 0.2) | strok 40, uç payı 3 | uç payı 3 − 0.8 = **2.2** | 3 − 0.47 = 2.5 | ≥ 1 ✓ |

---

## 7. Kontrol kapsam matrisi
Mevcut = `agent-flow/checks/` modülü. YENİ = CAD aşamasında `checks/`e eklenecek, KAPSAM bloklu.

| Risk | Check | Ne ölçer / parametre | Ölçülemeyen kısım → kim |
|---|---|---|---|
| **Çene–boyun + kozmetik parça çakışması, TÜM pozlar** | `cakisma.kontrol_cakisma(pozlar, gruplar, min_bosluk=5 mm)` + **YENİ `poz_kilit.py`** | ızgara: yaw {−70, −35, 0, 35, 70} × pitch −25..+20 / 5° (10) × roll {−15, 0, 15} × çene {0, 10, 20} × göz {merkez, 4 köşe} → **2250 poz**. Gruplar: sabit, yaw, haç, baş, çene, göz, kapak, pistonlar (iki uçlu, pozdan yeniden kurulur). Çıktı: izinli bölge tablosu (pitch_min(roll, çene)) → firmware kilit tablosu; konsept değerleriyle (−21/−8) karşılaştırılır | gerçek esneme → baskı sonrası kullanıcı |
| Kozmetik parça (SCM, yanak, kılıf, sahte cıvata) | aynı tarama, `muaf` YOK | konsept dersi: ramus önü 5°'ye kilitliyordu | — |
| Piston / pushrod strok sınırı (gizli kilit) | **YENİ `strok.py`** | her poz: iki uç mesafesi ∈ [Lmin + 3, Lmaks − 3]; rotil/küresel açı ≤ ±25° [T, K3]; krank açısı ≤ 60° | rotil açı sınırı → K3 |
| Pitch / roll / çene / yaw torku | `yercekimi_tork.kontrol_yercekimi_tork` (eksen başına, kütle tablosu CAD'den) + **YENİ `diferansiyel_tork.py`** (rod kuvveti Jacobian'ı → her servo, krank cos dahil, yay kuvveti modeli) | pay ≥ 3 pitch, ≥ 1.5 diğer; nominal ve +%30 | servo kapasitesi → **K1**; yay k → **K6**; sürtünme → K5/K8 |
| Kütle bütçesi | `yercekimi_tork.kutle_tablosu` + **YENİ `kutle_butce.py`** | parça başı bütçe (§5.1) ± %15, toplam ≤ 500 g, AM ≤ (25, 35) | dolgu/çevre gerçek gramı → K7 ve tartı |
| İnce et gereksiz kalın | `hafiflik.kontrol_hafiflik` | oran ≤ 1.15 | — |
| Et çok ince | `tabla.kontrol_et(min_et=1.2 kabuk / 1.6 yapısal)` | KABA ışın | baskı kalitesi → K7 |
| Tabla | `tabla.kontrol_tabla(xy=200)` | tüm STL | — |
| Havada vida/somun, ada | `havada.kontrol_tek_govde/ada/donanim_temas` | | — |
| Sarkma | `sarkma.kontrol_sarkma` | kubbe tepesi, kaş | destek gerektirenler raporda listelenir |
| Montaj sırası | `montaj_sokme.kontrol_montaj_sokme` (parçalı yol, §4) | 16 adım | — |
| Alet erişimi | `giris_yolu.kontrol_giris_yolu` | lazy susan vidaları (adım 4/8), M4 pimler (10/11), SG90 M2 vidaları, kubbe vidaları | — |
| Vida boyu / adet | `vida_envanter`, `vida_adet` | M3×14 sıkışan ≤ 11 mm; M4×40 satın alma | — |
| Kablo servis halkası | `kablo.kontrol_kablo` | yaw ±70 × pitch × roll → 4 iletken + 2 eğme servo kablosu | — |
| Tolerans Z1–Z5 | `tolerans.kontrol_tolerans` + `olc_serbest_oynama` (Z1, Z2 nominal modelden) | §6 | halka payları → K1–K3 |
| Devrilme | `devrilme.kontrol_devrilme` | kaide elipsi, baş tam öne + yaw 70° | — |
| BOM ↔ envanter | `bom_envanter`, `belge.kontrol_bom_belge_envanter` | MG996R 4/6, SG90 5/~6 | envanter adedi kullanıcı |
| Plan sapması | `plan_sapma.kontrol_plan_sapmasi` | DECISIONS etiketsiz sapma | — |
| Kapak hızı ≤ 100 ms | — | ölçülemez (CAD) | **K4** |
| Rotil / servo boşluğu | — | ölçülemez | **K1, K3** |
| Sakkad/VOR görünümü | — | sim (model.html) | kullanıcı göz testi |

---

## 8. Aşama 0: ölçüm kuponları (CAD'den önce, tek tabla ~2–3 saat [T])
| Kupon | Ne ölçer | Nasıl | Sonuç → plan kararı |
|---|---|---|---|
| **K1 MG996R tork + boşluk** | sürekli tork, boşluk, kulak deliği aralığı | basılı tutucu + 100 mm kol (20/40/60/80/100 mm delikler), su şişesi ağırlıklar + mutfak tartısı. 5.0 V adaptör A, PCA üzerinden. Kol yatayken 60 s tut: ≤ 2° sarkma ve gövde elle tutulabilir sıcaklıkta kalırsa "sürekli". **2 servo** test edilir. Boşluk: kol 90°'de tutulurken uca ±0.2 kg it-çek, uç kaymasını kumpas/cetvelle ölç → atan(δ/100) | ≥ 3.5 → plan aynen. 2.5–3.5 → pitch en kötü payı yeniden hesap (yay %85). < 2.5 → C2 iptal + yatırma ±10°. Boşluk > 1.5° → B yedeği (1.5:1, yatırma ±10°) |
| **K2 basılı kol cebi + dönen eklem** | `mg996r_disk_kol_cebi` ve `sg90_tek_kol_cebi` pay 0.1 / 0.2 / 0.3; `vida_pim_eklemi("M3")` | kit kolu cebe gömülür. Ölç: elle oturma, 50 mm uçta açısal boşluk (δ < 0.3 mm), 2 kg·cm'de kayma yok. M3 dönen eklem: 3.3 / 3.4 delik | pay seçimi → toleranslar.py (DOĞRULANDI). Z2 ve Z3 halkaları |
| **K3 rotil / pushrod boşluğu** | M3 rotil (satın) ve basılı küresel mafsal | 90 mm M3 rod + 2 uç, bir ucu sabit, ±0.5 kg it-çek, kumpasla toplam boşluk. Ayrıca rotilin açısal sınırı | > 0.15 mm/uç → kafa kolu d = 35 (pushrod kulakları dışa). Açı sınırı → strok.py |
| **K4 SG90 kapak hızı** | 60° / 50° süre, 1.5× bağlantıyla | telefon 240 fps slow-mo, açı çizgili disk | > 100 ms → kapak stroku 60°'ye iner ya da göz servosu MG90S (S2, +581 ₺) |
| **K5 teleskopik piston** | radyal boşluk 0.3 / 0.4 / 0.5 PETG; küresel soket 0.3 | kayma kuvveti (tartıyla it), 0° ve 10° eksen kaçıklığında; takılma var mı | boşluk seçimi; > 0.5 N ya da stick-slip → Al iç boru |
| **K6 yay** | k, ön gerilme, uzama sınırı | (satın alındıktan sonra) 50/100/200/300 g as, boy ölç | §5.2 ayar deliği; k uymazsa makara (sıfır boylu yay) |
| **K7 ince kabuk paneli** | 1.2 mm + 1.6 × 5 kaburga + M3 somun bossu, 60 × 60 | tart (g/cm²), elle eğ, somunu sık | kütle bütçesi g/cm² [Ö]; boss ≥ 5 mm doğrulama |
| **K8 lazy susan** | sürtünme torku, eksenel oynama, delik çapı/çemberi | (satın alındıktan sonra) kol + tartı; kumpas | yaw tork, Z4b, I4/I8 delik ölçüleri |

K1–K5 ve K7 tek tablada basılır. K6 ve K8 satın almadan sonra yapılır. Kuponlar sonuçlanmadan CAD adım 2 (tork) kesinleşmez.

---

## 9. CAD kurma sırası (cad-tasarimci-v2, parça parça)
| Adım | Parçalar | Ölçülecek (check) |
|---|---|---|
| 0 | `params.py`: kuponlardan gelen paylar, konsept koordinatları (pivot, göz, kondil, servo yerleri) | — |
| 1 | N2 + N3 + B1 iskeleti (yalnız eksenler, kulaklar) | cakisma: pitch × roll ızgarası (haç süpürmesi); tolerans Z3 U-mafsal halkası |
| 2 | N1 + eğme servoları + N4 + rod | **strok.py** (krank ≤ 60°), **diferansiyel_tork.py**, R1 (sol rod ucu ↔ çene servosu) ilk ölçüm |
| 3 | Yay + bağlantı delikleri | yercekimi_tork eğrisi (−25..+20), yaylı / yaysız |
| 4 | B5 göz modülü + 5 SG90 + teller | Z1/Z2, göz × kapak süpürme çakışması, giris_yolu (M2) |
| 5 | B4 + çene servosu + Ç1 + rod | çene süpürmesi, çene torku |
| 6 | B2, B3L/R kabukları | kutle_butce (≤ 500), hafiflik, kontrol_et, tabla, havada, sarkma; tüm iç poz çakışması |
| 7 | P1, P2 pistonlar, N5 kılıflar | strok.py; **poz_kilit.py tam ızgara** (2250 poz) → kilit tablosu |
| 8 | G1, G2L/R, G4L/R, Y1, lazy susan modeli | yaw uç pozlarında çene ↔ köprücük; montaj_sokme (16 adım); giris_yolu; kablo; devrilme; vida_envanter/adet |
| 9 | Tam rapor + BOM | bom_envanter, belge, plan_sapma; check_report KAPSAM ↔ §10 riskleri |

Her adımda yalnız değişen parça yeniden üretilir (`build.py --only`).

---

## 10. Riskler
| # | Risk | Rakam | Önlem / ölçen |
|---|---|---|---|
| **R1** | **Kafatası tabanı hacmi:** U-mafsal haçı (28 mm, ±25/±15 süpürme) + 2 rotil kulağı (±30, −6, −26) + çene MG996R (x 34..54, y 8..45, z −52..−12) + yay kancası (−64) + PCA + 5 SG90 aynı ~60 mm bölgede | konseptte sol rod kafa ucu (rotil Ø10 → x 25..35) ile çene servosu gövdesi (x ≥ 34) arasında **~0 mm** [H, konsept kutularından] | CAD adım 2'de ilk ölçüm. Çözüm: kulaklar x ±24'e ya da çene servosu +10 mm yukarı |
| R2 | MG996R gerçek torku ve boşluğu bilinmiyor (Eye dersi) | 3.5 [T]; yaysız en kötü pay 1.9 | K1 + yay; firmware zarfı |
| R3 | Kozmetik SCM stroku konseptte 71 mm | iki kademe sığmaz | mastoid yerleşimi → 40 mm; strok.py |
| R4 | Kapak stroku konseptte 135° → SG90 ile ~225 ms | hedef ≤ 100 ms | strok ≤ 75°, 1.5× bağlantı, K4 |
| R5 | 2:1 + yatırma geometrik olarak imkânsız | §0 B | 1:1 |
| R6 | Yay 48 mm uzama aralığı, yumuşak (0.035–0.047 N/mm) | piyasada bulmak [T] | K6, makara yedeği |
| R7 | Çene ↔ göğüs/köprücük, yaw ±70 × aşağı bakış | ölçülmedi (konsept yalnız boyunla ölçüyordu) | poz_kilit tam ızgara |
| R8 | 1.2 mm kabuk 188 mm yarılar, tepe sarkması, darbe | [T] | K7, sarkma check, kaburga çerçeve |
| R9 | Göz–baş VOR iki PCA'da aynı döngü | 50 Hz | firmware aynı I2C turunda yazar |

---

## 11. Satın alma (filament hariç; tavan ~2000 ₺)
**Envanterden (0 ₺):** MG996R ×4 (6'dan, 2 yedek), SG90 ×5 (~6'dan), PCA9685 ×2, 5 V 5 A ×2, 1000 µF ×2–4, DC jak, Uno klon, M2×8 (30), M3×8/10/14, M3×15 havşa, M4×8/10, somunlar, LED, kablo. **M2 somun envanterde teyitsiz** (açık soru).

| Kalem | Adet | ~₺ [T] | Not |
|---|---|---|---|
| Lazy susan 100–120 mm | 1 | 250 | yaw |
| M3 rotil (ball link) | 8 | 300 | 2 pushrod ×2 + çene ×2 + 4 yedek |
| M3 dişli çubuk 1 m | 1 | 40 | |
| Çekme yayı seti (yumuşak, uzun) | 1 | 150 | K6 |
| Uzun vida: M4×40 ×4, M4×20 ×14, M3×20/25 ×10 | set | 200 | U-mafsal ve servo kulakları |
| M2 somun | 20 | 30 | teyit edilirse çıkar |
| Servo uzatma 30 cm | 3 | 60 | eğme servoları → PCA#1 |
| 4 damarlı silikon kablo (≥ 0.5 mm², 1 m) + konnektör | 1 | 100 | boyun |
| Ø1 çelik tel (göz) | 1 | 30 | |
| **Ara toplam** | | **~1160** | |
| Seçenek: Al boru Ø6 × 1, 1 m (piston iç borusu) | 1 | 100 | K5'e bağlı |
| Seçenek C2: 2× 608ZZ + ek yay + 2 rotil + vida | — | 200 | karar C |
| Seçenek S2: MG90S ×5 | 5 | 581 [K] | K4 kötü çıkarsa |
| **En kötü toplam** | | **~2040** | S2 de alınırsa tavanı geçer; S2 ile C2 birlikte alınmaz |

---

## 12. Açık sorular
1. PETG filament elde var mı (pistonlar, kapaklar)?
2. Mutfak tartısı ve multimetre var mı (K1, K6, K8)?
3. Büst hangi yükseklikte duracak, ziyaretçinin göz hizasına göre kaç cm aşağıda (karar C'yi etkiler)?
4. M2 somun envanterde var mı?
5. Kozmetik piston uçları: basılı küresel mafsal (0 ₺) mı, M3 rotil (+~300 ₺) mı? K5 sonucuna mı bırakılsın?

## 13. Ek (kullanıcı, 2026-10-17): ses + kulak mikrofonları + burun kamera rezervi

| Konu | Karar |
|---|---|
| Beyin | Envanterdeki ESP32, **göğüste** (sabit kütle). I2S0 = 2× INMP441 stereo (L/R pini ile sol/sağ kanal, ortak SCK/WS), I2S1 = MAX98357A → 4 cm 3 W 4 Ω hoparlör (göğüs, ızgaralı). PC ↔ ESP32 USB seri (16 kHz stereo 16 bit = 64 kB/s → 921600 baud; yetmezse Wi-Fi UDP). |
| Mikrofonlar | Kafatası yanında **kulak hizası**, mastoid önü; ~12 mm iç-dış delik + toz kafesi. Kabuktan ayrı, lastik/köpük yuva (servo titreşimi mikrofona geçmesin). Aradaki mesafe ~140 mm → ses yönü (TDOA) çözünürlüğü yeterli. |
| Kablo | Boyundan geçen iletken **4 → 8**: +SCK, WS, SD, 3.3 V (GND ortak). I2S hatları GND ile bükülü, toplam ≤ 40 cm. Kablo check'i (yaw ±70 × pitch × roll) 8 iletkenle yapılır. |
| Kütle | Başa +~5 g (2 mikrofon + kablo). Kütle bütçesine "ses" satırı olarak eklenir; 495 g → ~500 g, hedef sınırında → kütle_butce check'i bunu ayrıca raporlar. |
| Davranış (yazılım, CAD değil) | Ses yönü → baş/göz yönelimi (saccade + VOR modeline girdi); TTS genliği → çene açıklığı (lip-sync); ses Terminatör tonunda işlenir. |
| Burun kamera rezervi | Burun boşluğunda ~32×32 mm kart yuvası (XICOOLEE OV5640 aday, 10 g) + kablo yolu; **kart şimdi yok**, kütle bütçesinde yalnız rezerv notu. Şimdilik kaidede mevcut webcam. |
| Satın alma (Amazon TR, arama fiyatları) | INMP441 5'li ~599 ₺, MAX98357A (SANEC) ~227 ₺, hoparlör 2'li ~371 ₺ → **~1200 ₺**. Güncel: INMP441+MAX98357 seti 551 ₺ (+ gerekirse 2. INMP441 ~199 ₺) + hoparlör ~371 ₺ → ~920–1120 ₺. Toplam satın alma ~2080–2280 ₺; kullanıcı tavan aşımını onayladı. |
