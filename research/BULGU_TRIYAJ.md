# Project Bust — check bulgu triyajı (SORUN 29, check_report 2026-10-17 20:09)

Salt okuma: hiçbir betik çalıştırılmadı. Kaynak: `cad/out/check_report.txt`, `cad/STATE.md` (Açık hatalar 1–7), `cad/STATE_CP3b2.md` §5, `cad/DECISIONS.md`, `cad/check.py`, `cad/govde.py`, `cad/params.py`.
"doğrulanmadı" = koordinat/geometri tek tek ölçülmedi, sınıf rapordaki koordinat + kod okumasından çıkarım.

Sınıf kısaltmaları: **G** = GERÇEK, **Y** = ÖLÇÜM YANILGISI, **K** = KABUL EDİLEBİLİR, **D** = DEVAM EDEN İŞLE ETKİLENİR.

## Tablo

| # | bölüm | parça | ne | sınıf | önerilen düzeltme | zorluk |
|---|---|---|---|---|---|---|
| 1 | et_kabuk_1.2 | B3L | %2.8 < 1.15; en ince 0.01 @ (158.2,48.5,22.9), 0.06 @ (32.0,**0.0**,69.8) | **D** (estetik ajanı: B3 alt kenar + şakak duvarı + orbita tavanı) + kısmen Y (y=0.0 sınır kutusu kenarı = kabuk kesim kenarı) | Estetik turu bitince yeniden ölç. Kalırsa `yuz_kubbe.py`/B3 kabuk kesim kenarlarına 1.2 dik pah yerine düz kesim; kaburga uçlarını kabukla birleştir | S (ölçüm) / M |
| 2 | et_kabuk_1.2 | B3R | %3.3; 0.00 @ (100.0,65.7,1.9), 0.05 @ (72.8,46.9,7.1) | **D** (aynı) + kısmen Y (z≈1.9 = tabla/alt kenar bölgesi) | #1 ile aynı | S/M |
| 3 | et_kabuk_1.2 | B5d_L | %3.5; 0.01 @ (4.2,5.3,12.0), 0.01 @ (**28.2**,10.2,12.9) | **Y** (x=28.2 = bbox genişliği 28.2 → kapak kabuğunun serbest kesim kenarı; havada_ada'da da 0.05 mm² tesselasyon kenarı görülüyor) — tek gerçek ince duvar doğrulanmadı | Ölçüm düzeltmesi (aşağıda M1). Kapak kenarına 0.6 mm × 1.2 dudak (rim) verilirse bulgu da kenar da sağlamlaşır: `bas.py` kapak kabuğu fonksiyonu | S |
| 4 | et_kabuk_1.2 | B5d_R | %4.7; 0.03 @ (**0.0**,11.0,12.8), 0.11 @ (0.0,5.0,12.0) | **Y** (üç en ince nokta da x=0.0 = kesim kenarı) | #3 ile aynı | S |
| 5 | et_yapisal_1.6 | B1 | %8.2; 0.08 @ (85.6,68.7,50.5), 0.09 @ (83.5,111.9,45.7) | **G + Y karışık** — STATE: bir kısmı somun kanalı/kulak kenarı (Y), ama %8.2 kenar etkisiyle açıklanamayacak kadar büyük; B1 ayrıca kütle bütçesini aşıyor (55.7 g > 40×1.15) | B1 kütle düzeltmesiyle birlikte ele al (STATE #7: PCA dik plakasını kaldır, çene servo duvarını kafes yap) → sonra yeniden ölç; kalan ince yerleri `diag.py B1` ile ayıkla. **Not:** boyun ajanı B1'e bağlı P1 üst ucu/dil bölgesini etkileyebilir — doğrulanmadı | M |
| 6 | et_yapisal_1.6 | B2 | %14.0; 0.01 @ (86.9,76.5,61.0) | **G** (DECISIONS 116 / STATE: `zarf_b2.py` yasak zarf kesiminin eğik bıçak kenarları + 1 mm süpürme basamakları — gerçekten keskin/ince kenar üretir, baskıda kırılır) | `zarf_b2.py`: süpürme zarfını hull'lu/seyrek yap (basamak yok) veya kesik kenarlara 1.6 kalınlaştırma bandı (zarf − offset) | M/L |
| 7 | et_yapisal_1.6 | B5a | %1.9; en ince 1.05 @ (45.1,1.4,27.6) | **K/Y** — eşiğin hemen üstü (%1.9 vs %1); min 1.05 (0.0x değil); noktalar y≈0–1.5 = plaka ön kenarı/pahı. Doğrulanmadı | Ölçüm düzeltmesi M1 sonrası büyük olasılıkla kapanır; kapanmazsa plaka kenarındaki pahı kaldır (`bas.py` B5a) | S |
| 8 | et_yapisal_1.6 | B5g_L | %5.1; 0.26 @ (15.0,**0.0**,16.2) | **Y** (STATE: 0.26 = pres tel deliği kenarı; y=0.0 sınır) + kozmetik halka eti 1.6 ile eşik aynı → 1.02'ler halka duvarı | Halka duvarını 1.6 → 2.0 (`params.py` halka et parametresi, adı doğrulanmadı) **veya** B5g'yi et_kabuk sınıfına al (halka yapısal yük taşımıyor mu? karar kullanıcıda) | S |
| 9 | et_yapisal_1.6 | B5g_R | %5.5; 0.27 @ (15.0,0.0,16.2), 0.39 @ (27.2,13.0,15.0) | **Y** (aynı) | #8 ile aynı | S |
| 10 | et_yapisal_1.6 | G1 | %4.1; 0.08 @ (54.5,11.2,91.6), 0.40 @ (29.4,13.4,98.0) | **G olası** — z 91–98 bölgesi G1 üst kısmı (manubrium/hoparlör plakası `kutu(..,41,45.01)` gibi 4 mm levhalar + delikli ızgara Ø2.2 / 3.4 adım → delikler arası et ~1.2) doğrulanmadı. Not: G1 yerleşimi #11–15 ile zaten yeniden çözülecek | Hoparlör ızgarası adımını 3.4 → 4.0 (`govde.py` `np.arange(-15,15.1,3.4)`) ya da delik r 1.1 → 0.9; ızgara kalınlığı ≥ 2 | S |
| 11 | cakisma_govde_statik | G1 × hoparlör | 699 mm³ | **G** | `govde.py`: hoparlör cebi yalnız z 40..45.6 silindir; hoparlör `params.HOPARLOR` boy 20 → gövdesi boyun yuvası güvertesi (`kutu(-20,20,gy0,gy1,30,51)`) / manubrium kutusuna giriyor (doğrulanmadı hangisi). Cebi tüm boy + 0.4 için kes (`silindir(..z 45-boy-0.4 .. 45.6, d/2+0.4)`) | S |
| 12 | cakisma_govde_statik | G1 × kart_esp32 | 51.2 mm³ | **G** | `govde.py` kart tablası bağlantı kirişleri (`kutu(-4,4,y±3, SPINE z..47)`) kart zarfından geçiyor olabilir; kirişleri kart dış sınırına taşı veya `P.KARTLAR` c'lerini kaydır, cep +0.4 | S |
| 13 | cakisma_govde_statik | G1 × kart_pca1 | 8.96 mm³ | **G** | #12 ile aynı (8.96 = muhtemelen tek ayak/kiriş köşesi) | S |
| 14 | cakisma_govde_statik | G1 × kart_uno | 17.9 mm³ | **G** | #12 ile aynı | S |
| 15 | cakisma_govde_statik | G1 × mg996r_yaw | 56.3 mm³ | **G** | `govde.py` yaw servo taşıyıcı (`ky-4..ky` plakası + yan duvarlar x ±20..±24) servo gövdesi/kulak + 0.4 ile kesişiyor; taşıyıcıdan servo zarfı (`satin.py` MG996R + 0.4) çıkarılmalı. Boyun ajanı Y1/N1'i değiştiriyor ama G1'e dokunup dokunmadığı doğrulanmadı | S |
| 16 | montaj_sokme_bas | rotil_krank+rotil_cene+cene_rod | adım 21, −X'te 1 mm'de rotil_cene × B4 36.4 mm³ | **Y olası** — rotil gözü B4 kulağına M3 ile bağlanır (çarpışmada muaf çift); doğrusal −X yolu cıvata eksenine paralel değil, takılı kesişim 0.0 → göz kulağın üstüne eksen boyunca geçirilir. Doğrulanmadı | `check.py` montaj sırasında adım 21 yönünü M3 eksenine (kulak deliği ekseni) çevir; ya da grubu ikiye böl: rod+krank rotili önce, B4 rotili cıvatayla sonra | S |
| 17 | montaj_sokme_bas | B5 grubu | adım 13, −Y 10 mm'de B5a × B1 16 mm³ | **G** (önceki tur B5d_L × B2 idi; şimdi B1 ile — gerçek geometri) | B1'de B5a'nın giriş yolundaki çıkıntıyı (B5 ayak/servo pedi yakını) 10 mm geri çek ya da B5 grubu yönünü (0,−1,0) yerine B5 ayak vidası eksenine göre seç. Yer doğrulanmadı: `_tmp/ix.py B5a B1` ile bul | M |
| 18 | montaj_sokme_bas | B2 | adım 12, +Y 5 mm'de B2 × kamera_rezerv 6.9 mm³ | **G** (sıra hatası) | Montaj sırasında kamera kartını B2'den SONRA (B2 içinden) tak — `check.py` montaj_sokme_bas sıra listesi; ya da B2 kamera çerçeve açıklığını +1 mm | S |
| 19 | montaj_sokme_bas | mg996r_cene | adım 7, −X 9 mm'de × B1 19.8 mm³ | **G** | B1 çene servo duvarında servonun −X giriş yoluna pencere/yarık; **#20–21 ile aynı duvar** — duvarı kafes yapmak (STATE #7) üçünü + B1 kütlesini birlikte çözer | M |
| 20 | giris_yolu | cene_servo_M4_1-1 | alet B1 ile 143.9 mm³ | **G** | B1 çene servo duvarında +X'ten Ø6 alet kanalı ya da vidaları ters (somun dışta). #19 ile birlikte | M |
| 21 | giris_yolu | cene_servo_M4_11 | alet B1 ile 98.1 mm³ | **G** | #20 ile aynı | (#20) |
| 22 | montaj_sokme_govde | hoparlör | adım 7, takılı kesişim 699.3 → 759.5 | **G, #11'in yan etkisi** (takılı halde zaten kesişiyor) | #11 kapanınca kapanır; sonra −X yolu ayrıca doğrulanmalı | (#11) |
| 23 | montaj_sokme_govde | mg996r_yaw | adım 4, takılı 56.3 → 61.8 | **G, #15'in yan etkisi** | #15 ile kapanır | (#15) |
| 24 | tolerans | Z1 göz merkezleme | en kötü 0.174 < 0.4 (nominal 1.024, toplam sapma 0.85) | **G** | Nominal ≥ 1.25 olmalı (sapma 0.85 sabitse). STATE önerisi: B2 yüz kabuğundan göz merkezli küre (r = GOZ_R + 1.25, STATE'teki r 13.6 tutarını yeniden hesapla) çıkar → nominal tanımlı olur. B2 hiçbir paralel ajanın kapsamında değil | S/M |
| 25 | tolerans | Z2 kapak ↔ halka | en kötü −0.28 < 0.3 (nominal 0.42, sapma 0.70) | **G** | Nominal ≥ 1.0 gerekli → +0.58. **STATE'teki "UST_RI 15.0 → 15.4" YETMEZ** (−0.28+0.4 = 0.12 < 0.3). `params.py` UST_RI 15.0 → 15.6 (kapak–halka model boşluğu `check.py` z2 = B5d_R↔B5g_R min_gap 1:1 artıyorsa — doğrulanmadı) ya da RSS (0.324) kullanmaya karar ver → nominal ≥ 0.63 yeter | S |
| 26 | montaj_sokme_boyun | P1R_orta_alt | adım 14, 4 mm'de × N1 1.3 mm³ | **D** (boyun ajanı: P1 alt uçları kolon tabanına, N1 küçülüyor) | Boyun turu sonrası yeniden ölç | — |
| 27 | montaj_sokme_boyun | P1L_orta_alt | adım 13, aynı | **D** (aynı) | aynı | — |
| 28 | montaj_sokme_boyun | P1R_orta_ust | adım 12, 24 mm'de × B1 0.7 mm³ (eşik 0.5) | **D** (P1 geometrisi değişiyor) + sınırda (0.7 vs 0.5 — 1 mm adımda sıyırma) | Kalırsa B1 dil/kulak kenarına 0.5 pah ya da takma yönünü tek pim eksenine çevir | S |
| 29 | montaj_sokme_boyun | P1L_orta_ust | adım 11, aynı | **D** (aynı) | aynı | S |

## Sınıf sayıları (29)
- **GERÇEK: 16** — #6, #10 (olası), #11–15, #17–25 (#22, #23 yan etki)
- **ÖLÇÜM YANILGISI: 5** — #3, #4, #8, #9, #16 (olası)
- **KABUL EDİLEBİLİR / sınırda: 1** — #7
- **DEVAM EDEN İŞLE ETKİLENİR: 6** — #1, #2 (estetik), #26–29 (boyun)
- **Karışık G+Y: 1** — #5 (B1)

## Tek değişiklikle birlikte kapananlar
1. **G1 cep/taşıyıcı düzeltmesi (`govde.py`)** → #11, #12, #13, #14, #15, #22, #23 (7 bulgu). #10 da aynı dosyada, aynı turda.
2. **B1 çene servo duvarı → kafes + −X giriş penceresi + Ø6 alet kanalı (`bas.py` B1)** → #19, #20, #21 + B1 kütle aşımı + muhtemelen #5'in bir kısmı.
3. **Kapak kabuğu kenar dudağı / ölçüm düzeltmesi M1** → #3, #4, #7 (+ B3'te kenar kaynaklı kısım).
4. **Boyun turu bitişi** → #26–29 (yeniden ölçüm).
5. **Estetik turu bitişi** → #1, #2 (yeniden ölçüm).

## Önerilen temizlik turu sırası
(Paralel ajanlar bitmeden B3, N*, P1 ve boyunla ilişkili B1 dillerine dokunma.)
1. **G1 (`govde.py`)** — #11–15, #22–23, #10. Paralel ajanlarla çakışmıyor (G1'e dokunup dokunmadıkları doğrulanmadı; boyun ajanına "G1'i değiştiriyor musun?" diye sor). En çok bulgu kapatır.
2. **Tolerans (`params.py` + B2)** — #25 (UST_RI 15.6) ve #24 (B2 göz küresi kesimi). Küçük, bağımsız.
3. **Montaj sırası (`check.py` montaj listesi)** — #18 (kamera B2'den sonra), #16 (rotil yönü). Geometri değişmez.
4. **B1 çene bölgesi** — #19–21 + kütle. Boyun ajanı bitince (B1 dilleri/P1 üst ucu sabitlendikten sonra).
5. **#17 B5a × B1** — `_tmp/ix.py B5a B1` ile yeri bul, sonra düzelt.
6. **Ölçüm düzeltmesi M1/M2** (aşağıda) → yeniden check → kalan et bulguları (#5, #6, #8–9) tek tek.
7. Paralel turlar bitince tam check; #1–2, #26–29 yeniden sınıfla.

## check.py ölçüm düzeltme önerileri
- **M1 (et, kenar yanılgısı):** `kontrol_et(..., n=1500)` (`checks` modülü, `check.py` satır 122–123). Ray örneklemesi yüzey noktasından içe normal boyunca atış yapıyor; serbest kenar/pah yakınındaki noktalar 0.0x veriyor (B5d x=0/28.2, B5g y=0, B3 y=0). Öneri: (a) örnek noktayı, yüzey normali komşu yüzlerle > 60° açı yapan kenarlardan ≥ 1× eşik mesafesi uzaktaysa say; (b) tek nokta yerine noktanın 0.5 mm çevresindeki 3–5 atışın medyanı; (c) raporda "en ince"leri kenar/iç ayırarak yaz. Bu, “%1 alan” eşiğini değiştirmeden yanlış pozitifleri ayıklar.
- **M2 (et, sınıf):** B5g (halka, kozmetik/hafif yük) ve B5a yapısal listede; `check.py` 122–123'teki `kab`/`yap` listelerinde hangi parçanın hangi eşikte ölçüleceği DECISIONS'a gerekçeyle yazılmalı (muaf yazmadan sınıf değiştirmek).
- **M3 (montaj, yön):** pimli/cıvatalı grupta (#16) takma yönü, çiftin bağlantı ekseninden (kulak deliği ekseni) türetilsin; şu an sabit eksen vektörü.
- **M4 (montaj, eşik):** 0.5 mm³ eşik + 1 mm adım, 0.7 mm³ sıyırmaları (#28–29) bulgu sayıyor; ya 0.25 mm adım + 1.0 mm³ ya da "ardışık 2 adımda artan kesişim" kuralı. (Gerçek sıyırmayı gizlememesi için eşik değil adım küçültülmeli.)
- **M5 (çakışma → montaj tekrarı):** takılı halde kesişen çift (#22, #23: takılı 699/56 mm³) montaj bölümünde ayrı bulgu olarak tekrar sayılıyor; montaj_sokme raporunda "takılı kesişim > 0 → çakışma bulgusuna bağlı" diye bağlanıp sayaçtan düşülebilir.
