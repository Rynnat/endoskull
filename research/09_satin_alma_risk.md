# 09 — Satın alma ve risk (R6 yay, lazy susan, M3 rotil, R2 MG996R)

Tarih: 2026-10-17. Bütçe tavanı ~2000 ₺ toplam. **Karar yok, seçenekler + tek öneri.**
Not: Envanter (plan-v2) ve cq-ders ölçümleri bu turda okunmadı (token bütçesi ~25k); ölçüm dosyalarında MG996R tork/boşluk verisi varsa bu notu ezer.
Arama aracı TR mağaza sayfalarını (Trendyol/Hepsiburada/robotistan/direnc) döndürmedi → **tüm TL fiyatları [T]**, sipariş öncesi elle kontrol şart.
Kur varsayımı [T]: 1 EUR ≈ 48 ₺, 1 USD ≈ 41 ₺ (2026-10).

---

## 1) R6 çekme yayı (k ≈ 0.020 N/mm, L0 ≤ 50, uzama ≥ 63, F 0.6–1.8 N)

İhtiyaç STATE_CP3b2'den: yay boyu 55..113 mm, F 0.6..1.8 N, k 0.020 → L0 = 50 ise **ön gerilme Fi ≈ 0.5 N**.

### Hesap (k = G d⁴ / (8 D³ n), D = ortalama çap, G yay çeliği 79 GPa, paslanmaz 304 ≈ 69 GPa)

| tel d | ort. D (dış) | n (k=0.020, çelik) | gövde boyu (n+1)d | L0 kancalı [T] | τ @1.8 N (Wahl dahil) | yorum |
|---|---|---|---|---|---|---|
| 0.25 | 3.0 (3.25) | 71 | 18 mm | ~25 | ~985 MPa | sınırda (kanca gerilmesi ~1.3×) ✗ |
| 0.30 | 3.0 (3.3) | 148 | 45 mm | ~52 | ~580 MPa | L0 sınırı aşıyor ✗ |
| **0.30** | **4.0 (4.3)** | **62** (304: 55) | **19 mm** | **~28** | **~750 MPa** | ✓ öneri; Sut ~2600 MPa, emniyet ~1.6 kancada |
| 0.40 | 5.0 (5.4) | 101 | 41 mm | ~50 | ~520 MPa | sınırda boy |
| **0.40** | **6.0 (6.4)** | **59** (304: 51) | **24 mm** | **~33** | **~430 MPa** | ✓ en dayanıklı; kanca Ø6 dar yerde sığmalı |

Ön gerilme 0.5 N: d0.3/D4 için τi ≈ 170 MPa (C = 13 için tercih edilen aralık ~50–120 MPa [T]) → hazır yayda Fi muhtemelen **daha düşük** çıkar; telafi = I15'teki 3 ayar deliği (±8 mm ≈ ±0.16 N). Uzama sınırı sorun değil: 63 mm / 62 sarım ≈ 1 mm/sarım, τ izin içinde.

### Tedarik seçenekleri

| Seçenek | Fiyat [T] | Kaynak | Not |
|---|---|---|---|
| A. AliExpress/eBay "0.3 mm tel, OD 3–4 mm, boy 10–300 mm" çekme yayı (uzun alıp sarım sayarak kesmek, yeni kanca bükmek) | ~2–5 EUR/paket → **100–250 ₺**, 2–4 hafta | [eBay 0.3/0.4 mm, kanca 10–60](https://www.ebay.de/itm/166374657594), [eBay 0.3/0.4 OD 3–4, 10–300 mm](https://www.ebay.de/itm/226443522691), [304 paslanmaz 0.3/0.4](https://www.ebay.de/itm/226317767841) | **Öneri.** Uzun yay → istenen n'de kes; k ∝ 1/n olduğu için ayar kolay |
| B. Yerli yay üreticisine özel sipariş (d 0.3, OD 4.3, n 62, Fi 0.3–0.5 N) | 1 adet için min. sipariş/kalıp yok ama işçilik ~**300–600 ₺** [T] | [Yorulmaz Yay (0.15 mm'den çekme yayı)](https://yorulmaz-yay.idef.com.tr) | Tam istenen Fi ile gelir; telefonla teyit lazım |
| C. Hazır karışık yay seti (Trendyol/Hepsiburada "çekme yayı seti") | 150–300 ₺ [T] | link bulunamadı | Setlerde tipik d ≥ 0.5, k ≫ 0.1 N/mm → **büyük olasılıkla uymaz** |
| D. Kendi sarmak (0.3–0.4 mm piyano teli + Ø3.5/5.5 matkap ucu mandrel) | tel ~100 ₺ [T] | — | Yapılabilir; Fi kontrolsüz, k ±%20 |
| E. Lateks/elastik | ~50 ₺ | — | Sünme (creep) + ısı → %75 oran zamanla kayar ✗ |
| F. Sabit kuvvet yayı | 100–300 ₺ [T] | — | Kuvvet açıyla değişmeli (0.6→1.8 N); sabit kuvvet modele uymaz, ancak makara yarıçapı değişkense ✗ |
| G. Plan yedeği: misina + makara + kısa yay | ~0 | PLAN §5.2 | Mevcut yedek, geçerli |

---

## 2) Lazy susan 100–120 mm

| Bilgi | Değer | Kaynak |
|---|---|---|
| Piyasadaki en yaygın 100 mm tip | **kare** sac (çelik, galvaniz), 100 × 100, yükseklik ~8–10 mm, yük 130–135 kg | [Flints CAS100LS](https://flints.co.uk/product/All/CAS100LS), [LSB100 100×8 135 kg, orta delik Ø55](https://miniaturebearings.com.au/products/100x8x135-lazy-susan-bearingslazy-lsb100/data?view=data) |
| Yuvarlak alüminyum 100 mm | var, daha pahalı | [eBay 100 mm alüminyum](https://www.ebay.de/itm/401847894168), [30–120 mm seri](https://www.ebay.de/itm/133058843509) |
| Delik deseni (kare tip) | 4 delik alt sacda + 4 üst sacda, ~Ø4.2–4.5, köşegene yakın; **bir sacda erişim deliği** (karşı sacı vidalamak için) [T] | ölçülmemiş → K8 |
| Eksenel oynama / sürtünme | yayınlanmış veri yok; sac tiplerde bilye kafesi gevşek, ±0.2–0.4 mm [T] | — |
| Fiyat TR | 100 mm kare **60–150 ₺**, yuvarlak alü. 120 mm **200–400 ₺** [T] | link bulunamadı |

**K8'i basitleştirecek bilgi:** PLAN I4/I8 "4× M3, r 50, ±45°" varsayıyor; kare 100 mm tipte delikler köşegende r ≈ 55–62 olabilir [T] → N1 Ø124 sınırına yakın. Merkez Ø55 delik kablo/Y1 için yeterli. Öneri: **önce satın al, K8'de deliği ölç, sonra I4/I8 deseni.** Ø100 sac tipte eksenel oynama Z4b'yi (±0.6 mm göz hizası) büyütebilir; gerekirse iki halka arasında PTFE pul/ön yük.

---

## 3) M3 rotil ×8

| Seçenek | Fiyat | Kaynak | Not |
|---|---|---|---|
| Alüminyum M3 rod end, 1/10 RC (20'li) | ~14 EUR → **~680 ₺** + kargo | [eBay 20 adet alü M3](https://www.ebay.de/itm/254701177614) | top Ø~5.8–6, açı ±25–30° [T] |
| 8'li alü M3 | ~8–10 EUR [T] → ~400–500 ₺ | [eBay 8 adet](https://www.ebay.de/itm/356475102787) | |
| Plastik ball link (Secraft/Gator) 10'lu | 6.8 USD → **~280 ₺** + kargo | [Gator RC 10 pack](https://www.gator-rc.com/products/secraft-3mm-brass-ball-links-m3-10-pack-no-hardware) | pirinç top, açı ±30°+ ; boşluk düşük |
| TR RC mağazası (plastik ball link 10'lu) | 150–350 ₺ [T] | link bulunamadı | Kargo hızlı |
| Basılı küresel mafsal (Ø8 bilye + soket) | ~0 | PLAN pushrod | K5 ölçer |

±17–30° ihtiyacı: plastik RC ball linkler tipik ±30–35°, alü rod end'ler ±25° civarı [T] → **30° sınırı için plastik ball link tercih**, alü olanlarda strok.py ≤ ±25° kuralı sıkışabilir. K3 ölçecek.

---

## 4) R2 MG996R gerçek tork ve boşluk

| Kaynak | Değer |
|---|---|
| Datasheet / satıcılar | 9.4 kg·cm @4.8 V, 11 @6 V, stall ~2.5 A ([servodatabase](https://servodatabase.com/servo/towerpro/mg996r), [makerselectronics](https://makerselectronics.com/product/servo-motor-half-metal-gear-mg996r-towerpro-180-degree/)); bazıları 13–15 iddia ([probots](https://probots.co.in/mg996r-13kg-metal-gear-servo-180.html)) |
| Kullanıcı tezgâh testi (ağırlık + kol) | **~10 kg·cm @6.5 V** tepe; "önemli serbest oynama", tek pirinç burç, bilyesiz ([desertcart yorumları](https://www.desertcart.ni/products/71405317)) |
| Satıcı blogu (güvenilir değil) | hareket halinde ~6 kg·cm ([kpower](https://blog.kpower.com/servo/661.html)) |
| Klon kalite | "bilye yok, ana milde ciddi boşluk"; sahte < orijinal ([makerstore](https://www.makerstore.com.au/?p=101101)) |
| Boşluk (derece) | **yayınlanmış ölçüm bulunamadı.** Topluluk anlatımına göre klonlarda ±0.5–1.5° [T] → PLAN'ın ±0.75° varsayımı ortalama, kötü klon 2× olabilir |

**3.5 kg·cm muhafazakâr mı?** Kural: sürekli güvenli tork ≈ stall'un %20–30'u [T]. Orijinal (11) → 2.2–3.3; iyi klon (~8–10 @5 V) → 1.6–3.0. **3.5 kg·cm muhafazakâr DEĞİL, hafif iyimser.** Yine de pitch payları (8.3 / 3.7) 2.5 kg·cm'ye düşse bile 5.9 / 2.6 (> 1.5 ✓, < 3 hedefi ✗ en kötü pozda). Yaw 0.6–1.5 ihtiyaç → 2.5'te pay 1.7–4.2 ✓. Ayrıca 5 V 5 A hattında 4 servo aynı anda stall = 10 A → **akım asıl risk** (aşağıda). K1 kuponu belirleyici.

---

## Plan için riskler (rakamla)

| Risk | Kritik mi | Rakam |
|---|---|---|
| **Tork** | **evet** | Sürekli 3.5 [T] → gerçekçi 2.2–3.0. Pitch en kötü pay 3.7 → ~2.4–3.2; yaysız en kötü 1.9 → ~1.2–1.7 ✗. Yay kırılırsa/sünerse zarf kısıtı şart |
| **Güç** | **evet** | MG996R stall 2.5 A × 4 = 10 A > A hattı 5 A. Hızlı eş zamanlı hareket + çene konuşması (4–6 Hz) → gerilim düşmesi/reset. Soft-start / hareket sıralama |
| Tolerans zinciri | orta | Z3 ±1.8° (WC) ±0.9 (RSS); kötü klon boşluğu ±1.5° → WC ~±2.5°. Yay ön yükü yarıya indirir |
| Tabla | orta | lazy susan oynaması ±0.2 → ±0.4 mm [T] → göz hizasında ±0.6 → ±1.2 mm |
| Montaj erişimi | düşük-orta | kare lazy susan delik konumu r 55–62 [T]; erişim deliği ile adım 4 hizası K8 sonrası |
| Kablo | düşük | yaw ±70°, servis halkası; Ø55 merkez delik yeterli |

## Tahmini maliyet (satın alma farkı)

| Kalem | Düşük | Yüksek |
|---|---|---|
| R6 yay (A seçeneği; B olursa +300) | 100 | 250 (B: 600) |
| Lazy susan 100 kare / 120 yuvarlak | 60 | 400 |
| M3 rotil ×8 (plastik / alü) | 150 | 680 |
| **Toplam** | **~310 ₺** | **~1330 ₺** (B ile ~1680) |

PLAN §11'deki "+~200 ₺" farkının üzerine tahmini **+110 … +1130 ₺** eklenir; 2000 ₺ tavanının içinde kalır, ancak alü rotil + özel yay + yuvarlak alü. lazy susan birlikte seçilirse tavana yaklaşır.

**Tek öneri:** AliExpress'ten tek siparişte 0.3 mm uzun çekme yayı paketi + plastik M3 ball link 10'lu + TR'den 100 mm kare lazy susan (hızlı; K8 hemen) → ~350–500 ₺ [T]. Önce K1 (MG996R tork) kuponu, çünkü 3.5 kg·cm varsayımı en zayıf halka.
