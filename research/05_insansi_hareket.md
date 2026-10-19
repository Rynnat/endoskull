# 05: İnsansı hareket: sim ve firmware için sayılar

Tarih: 2026-10-16. Aşama 0. Sayılar insan ölçümü. Servo sınırları 03 ve 04'te.

## 1. Sakkad (ana dizi)
| Değişken | Değer | Kaynak |
|---|---|---|
| Süre | **D = 2.2·A + 21 ms** (A derece). Başka fit: 37 + 2.7·A | [arXiv 1906.07183](https://arxiv.org/pdf/1906.07183), [PMC7166123](https://pmc.ncbi.nlm.nih.gov/articles/PMC7166123) |
| Tepe hız | **V = 500·(1 − e^(−A/14)) °/s**. 10° → ~255°/s. Başka kaynak: 10° → 300°/s, 30° → 500°/s, ~60°'de doyum | [arXiv 1906.07183](https://arxiv.org/pdf/1906.07183), [USPTO 11507184](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11507184) |
| Ölçülmüş örnek | 10° sakkad: tepe 362–377°/s, süre 42–43 ms | [PMC3491344 T3](https://pmc.ncbi.nlm.nih.gov/articles/PMC3491344/table/T3) |
| Not | Sabitler denekten ve yöntemden yönteme değişiyor | [PMC2637438](https://pmc.ncbi.nlm.nih.gov/articles/PMC2637438), [Radboud ders notu](https://perception-and-action-37169a.pages.science.ru.nl/content/12_the_saccadic_system_pulsestep.html) |

Örnek: 5° → 32 ms · 10° → 43 ms · 20° → 65 ms · 30° → 87 ms.
Sim: profil olarak minimum-jerk ya da asimetrik çan eğrisi kullanılabilir **(tasarım önerisi)**. Firmware'de 50 Hz servo güncellemesi 20 ms adım demek. 10° sakkad 2–3 karede biter, yani hedef açıyı **tek adımda** vermek, ara adımlarla yumuşatmaktan daha gerçekçi görünür.

## 2. Fiksasyon arası mikro hareketler
| | Değer | Kaynak |
|---|---|---|
| Mikrosakkad | 0.02–1°, 1–2/s (koşula göre ort. 0.4–0.5°, 1.6–4.3/s) | [JEMR 2241](https://bop.unibe.ch/JEMR/article/download/2241/3437/8465), [Mergenthaler tezi](https://publishup.uni-potsdam.de/files/2805/mergenthaler_diss.pdf) |
| Drift | ort. 0.04–0.13°, her drift bir mikrosakkadla biter | aynı |
| Tremor | ~84 Hz, foto-reseptör genliğinde | aynı |
| Fiksasyon süresi | **bulunamadı** (genelde ~200–300 ms denir, **belirsiz**) | — |

Fiziksel sınır: SG90 + PCA9685'te adım ~0.45°, ölü bant ~1° **(belirsiz)**. Mikrosakkad ve drift fizikte **görünmez**, simde birebir uygulanabilir. Fizik için yaklaşık yol: 1–3 s'de bir 1–2°'lik "bakış kayması" **(tasarım tahmini, insan değeri değil)**.

## 3. Göz kırpma
| | Değer | Kaynak |
|---|---|---|
| Toplam süre | 100–400 ms (BioNumbers), 100–150 ms (UCL) | [Wikipedia: Blinking](https://en.wikipedia.org/wiki/Blinking), [lens.com](https://www.lens.com/questions-answered/what-is-the-average-time-it-takes-to-blink/) |
| Kapanma | **75–100 ms** (başka kaynakta 50–130). Açılmadan ~2 kat hızlı | [somatechnology](https://www.somatechnology.com/blog/thursday-thoughts/fast-average-blink), [Frontiers 2023](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2023.1242654/pdf) |
| Açılma | **150–300 ms** (zayıf kaynak) | [somatechnology](https://www.somatechnology.com/blog/thursday-thoughts/fast-average-blink) |
| Kapak tepe hızı | 16–19 cm/s | aynı |
| Sıklık | kadın 19/dk, erkek 11/dk. Kontrol grubu 20 ± 2.1/dk | [air.unimi](https://air.unimi.it/handle/2434/40476), [UNESP](https://acervodigital.unesp.br/handle/11449/1426) |
| Kedi verisi | kapanma, açılmadan ~10 kat hızlı (insana aktarılamaz) | [WUSTL](https://profiles.wustl.edu/en/publications/kinematics-of-spontaneous-reflex-and-conditioned-eyelid-movements/) |

Firmware önerisi **(tasarım)**: kırpmalar arası süre 2–6 s rastgele (ort. ~4 s ≈ 15/dk). Kapanma ~80 ms, kapalı bekleme 0–30 ms, açılma ~200 ms. Büyük sakkadla birlikte kırpma olasılığı artırılabilir (**belirsiz**, kaynak bulunamadı).

## 4. Göz–baş koordinasyonu ve VOR
| | Değer | Kaynak |
|---|---|---|
| Başın katkısı | < ~25° bakış kaymasında baş katkısı yok ya da az. Üstünde **doğrusal artar** | [Freedman & Sparks / Pitt PDF](https://sites.pitt.edu/~neg8/rajimages/pdf/2001-3295.pdf), [Springer BF00229630](https://link.springer.com/doi/10.1007/BF00229630) |
| Göz sınırı | Merkezden başlayan yatay kaymada göz nadiren 35°'yi geçer | aynı |
| Zamanlama | Görsel hedefte **göz önce, baş 20–40 ms sonra** başlar (primat). İşitsel hedefte baş önce | [PMC1890377](https://pmc.ncbi.nlm.nih.gov/articles/PMC1890377), [PMC3191847](https://pmc.ncbi.nlm.nih.gov/articles/PMC3191847) |
| VOR | Bakış kayması sırasında VOR bastırılır. Baş gelmeye devam ederken göz ters döner, bakış hedefte sabit kalır | [Cecala SFN 2005](https://www.urmc.rochester.edu/MediaLibraries/URMCMedia/labs/freeman-lab/documents/Cecala-SFN-2005.pdf), [NASA NTRS](https://ntrs.nasa.gov/api/citations/20060023313/downloads/20060023313.pdf) |
| Başlangıç pozisyonu | Göz hedef yönüne kaymış başlarsa baş katkısı artar | [PMC1890377](https://pmc.ncbi.nlm.nih.gov/articles/PMC1890377) |

Firmware/sim algoritması **(tasarım önerisi, kaynaklı kurallardan türetildi)**:
1. Hedef bakış açısı G (webcam yüzünden) gelir. Göz hemen sakkad yapar: e = clamp(G − h, ±e_max). e_max fizikte ~±25–30°.
2. |G − h| > ~20–25° ise baş 20–40 ms sonra G'ye doğru yavaş bir profille (04: ~60–120°/s) hareket etmeye başlar.
3. Her döngüde **VOR**: e = G − h. Baş döndükçe göz geri döner, bakış sabit kalır. Sonuçta göz merkeze, baş hedefe oturur.
4. Küçük takip hareketlerinde (< ~10°) yalnız göz döner, baş kıpırdamaz.
5. Üst kapak ofseti göz pitch'ini izler (03).
Not: Göz servosu ~50 Hz çalışıyor, baş servosu yavaş. VOR'un fizikte titremesiz görünmesi için iki eksenin aynı kontrol döngüsünde yazılması gerekir. **Risk:** iki ayrı PCA9685 kartı varsa ikisini de aynı I2C turunda güncellemek gerekir.

## 5. Çene
Konuşmada çene açıklığı ~0–20° **(belirsiz)**, hece hızında (~4–6 Hz, **belirsiz**) titreşir. Ses zarfından (RMS) türetilen açı simde yeterli. Bu sayılar için kaynak aranmadı (arama bütçesi bitti).

## 6. Baş "nefes" ve canlılık
Boşta 0.1–0.3 Hz'de ±1–2° yavaş roll/pitch salınımı **(tasarım tahmini, kaynak yok)**. MG996R'nin ölü bandı (~1–2°, **belirsiz**) nedeniyle fizikte "takılarak" görünebilir. Simde serbest, fizikte kuponla denenmeli.
