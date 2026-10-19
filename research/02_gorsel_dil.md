# 02 — Görsel dil: T-800 endoskeleton + InMoov + tek renk metalik

Tarih: 2026-10-16 · Aşama 0 (araştırma) · Karar yok, seçenekler var.
Project Angela dosyaları kullanılmadı (KARARLAR.md).

## 1. T-800 endoskeleton: kaynaklı bilinenler

| Konu | Bulgu | Kaynak |
|---|---|---|
| 1:1 kafatası replika boyu | Blitzway "Real Series" 1:1 kafatası **~50 cm** (boyun + kaide dahil), başı hareketli, gözler LED | [BigBadToyStore](https://www.bigbadtoystore.com/product/terminator-real-series-t-800-endoskeleton-skull-1_1-scale-limited-edition-replica-159745) |
| Genisys 1:1 kafatası | ~15″ yükseklik × 10″ boy × 8.5″ en (≈ 38 × 25 × 22 cm, 2″ kaide dahil). Yani kaide hariç kafatası + boyun ≈ 33 cm | [Entertainment Earth](https://www.entertainmentearth.com/product/terminator-genisys-endoskeleton-skull-11-scale-prop-replica/tnclst5) |
| 1:2 tam figür | Agora Models: 95 cm, ~6 kg, 650+ parça, uzaktan kumandalı çene, ışıklar | [Agora](https://www.agoramodels.com/jp/terminator-t-800) |
| 1984 yapımı | İçinde hidrolik piston çubukları ve dişliler var; elle yontulmuş, **simetrik değil** (Rosengrant) | [CGW 2008](https://www.cgw.com/Publications/CGW/2008/Volume-31-Issue-5-May-2008-/Man-vs-Machine.aspx) |
| 1984 kaplama | Plastik parçalar elektrostatik metalik kaplamayla krom görünüme getirilmiş, çekimde kolayca soyulmuş, folyo ve boyayla yamanmış | [CGW 2008](https://www.cgw.com/Publications/CGW/2008/Volume-31-Issue-5-May-2008-/Man-vs-Machine.aspx) |
| Yanak pistonları, boyun montajı | Yalnız sonraki T2-3D ışıklı kafatası ilanında geçiyor. **1984 için doğrulanmadı.** | [Propstore](https://propstore.com/product/t2-3d-battle-across-time-1996/light-up-t-800-endoskeleton-skull/) |

### Tasarım öğeleri (gözleme dayalı, kaynaksız: **(belirsiz)**, kullanıcı referans görselle doğrulasın)
- **Kafatası:** derin göz çukurları, kırmızı göz merceği, belirgin elmacık kemiği, açıkta metal diş sırası, şakakta yatay "kas" plakaları.
- **Çene:** dişler açıkta. Çene menteşesinin önünde yanaklarda çene açan piston veya kablo görüntüsü var.
- **Boyun:** ortada omurga benzeri dikey bir kolon, etrafında 2–4 hidrolik silindir ve hortum/kablo demeti. Kalın tek bir boru değil, "açık" bir yapı.
- **Göğüs:** kaburga plakaları, ortada sternum, köprücük kemiği çubukları, omuzda deltoid kapakları.

**Tasarım fırsatı (öneri değil, gözlem):** Endoskeleton estetiğinde mekanizmanın **kendisi** görünür. Boyundaki pushrod'lar "hidrolik silindir" kılıfıyla giydirilirse hem gerçek iş görür hem T-800 görüntüsünü verir. Çene pushrod'u da "yanak pistonu" olabilir. Gizlemeye uğraşılmaz, yani gövde kabuğu tasarım yükü azalır.

**Çelişki:** T-800'ün **göz kapağı yoktur.** Kullanıcı ise kapak, kırpma ve kısma istiyor. Uzlaşma yolları:
- (a) Metal plaka "deklanşör" kapaklar: robotik ama insan gibi hareket ediyor.
- (b) Kamera diyaframı (iris) tipi kapak: daha robotik, kırpma okunur, ama mekanizması karmaşık.
- (c) İnsan formunda kapak, metalik kaplama.

## 2. İnsan ölçüleri (1:1 hedef zarfı)

| Ölçü | Değer | Kaynak |
|---|---|---|
| Baş boyu (glabella–opisthocranion), erkek P50 | ~7.9″ ≈ **200 mm** | [NCSU tabloları](https://www.ergocenter.ncsu.edu/wp-content/uploads/sites/18/2017/09/Anthropometric-Summary-Data-Tables.pdf) |
| Baş eni, erkek P50 | ~6.1″ ≈ **155 mm** | aynı |
| Baş çevresi / boyu (Çinli yetişkin ort.) | 555 mm / 184 mm | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7494015/table/T1) |
| Tepe–çene yüksekliği | ~230 mm **(belirsiz, kaynak bulunamadı)** | — |
| Göz bebekleri arası | ~63 mm **(belirsiz, genel bilgi)** | — |
| Göz küresi çapı | ~24 mm **(belirsiz, genel anatomi bilgisi)** | — |
| Omuz eni (biakromiyal) | ~400 mm **(belirsiz)** | — |

Tabla etkisi (Ender 3 Neo 220×220×250): kafatası 200×155×230 tek parça olarak XY'ye ancak sığar, %5 marjı yok. Prensip 5 ("~200 üstünü böl") gereği kafatası en az **kubbe / yüz / çene** olarak bölünür. 400 mm göğüs en az **4 parça** olur (sol/sağ × üst/alt), omuz kapakları ayrı basılır.

## 3. InMoov (yalnız görsel ilham, STL yok)
- Baş, boyun eğme, dönüş ve çene var. Gözler X/Y (küçük servo). Standart haritada kapak yok. Gövde beyaz, heykelsi ([inmoov.fr hardware map](https://inmoov.fr/default-hardware-map/), [neck & jaw](https://inmoov.fr/neck-and-jaw/)).
- Alınabilecek fikirler: göğüs plakasının bölünme hatları, boyun dişlisi ("MainGear → NeckHinge"), ağırlığı taşıyan büyük servolar. Topluluk yorumu: "baş çok ağır, büyük servo kullanmak kötü fikir değil" ([inmoov.fr/?p=406](https://inmoov.fr/?p=406)).
- Lisans CC BY-NC: form kopyalanmaz, yalnız oran ve fikir alınır.

## 4. Tek renk yazıcıda "metalik" görünüm

| Yol | Görünüm | İşçilik | Maliyet (TR) | Not |
|---|---|---|---|---|
| **M1** Gümüş silk PLA, işlemsiz | Fırçalanmış metal, ışıkta parlak; katman çizgileri görünür | yok | ~980–1100 ₺/kg (Kingroon silk, idefix) | Zımparalanmaz, boya tutmaz ([Bambu forum](https://forum.bambulab.com/t/bambu-pla-metal-alternatives/57800), [evetech](https://evezone.evetech.co.za/deep-dives/which-silk-or-metallic-filament-for-a-shiny-finish-without-painting)) |
| **M2** Gri/siyah PLA + astar + zımpara + gümüş sprey | Daha düzgün, krom değil "parlak" | yüksek (120→400–800 kum, astar–macun katları) | PLA ~580 ₺/kg + boya ~300–500 ₺ **(tahmin)** | Yüzey hazırlığı belirleyici ([Prusa forum](https://forum.prusa3d.com/forum/original-prusa-i3-mk2-s-others-archive/pla-possible-to-chrome), [Polyfab3D](https://www.polyfab3d.fr/ressources/?p=11914)) |
| **M3** M2 + Rub 'n Buff mumu | Demir/krom, "film propu" görünümü | en yüksek | +~400–700 ₺ **(tahmin)** | Astar şart ([RPF](https://www.therpf.com/forums/threads/easy-or-affordable-way-to-etch-pla-for-rub-n-buff.279795/post-4289902), [Core Electronics](https://core-electronics.com.au/videos/how-to-get-metallic-finishes-on-3d-prints)) |
| **M4** Mat siyah PLA + kuru fırça gümüş akrilik | "Yıpranmış savaş" endoskeleton; katman çizgisini gizler | orta | PLA + ~150 ₺ akrilik **(tahmin)** | Kaynak yok **(belirsiz)**, maket boyama pratiği |
| **M5** Parça ayırma: kafatası/boyun gümüş silk, göğüs koyu gri | İki ton metal, renk değişimi parça sınırında | yok | silk + düz PLA karışık | Prensip 6 ile uyumlu (renk = ayrı parça) |

Not: Film kaplaması da plastik üstüne metalikti ve soyuldu (CGW). Yani "plastik + kaplama" T-800 yöntemiyle aynı.
