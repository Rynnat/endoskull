# Project Bust — kullanıcı kararları (2026-10-16)

Bu dosya tüm ajanlar için bağlayıcıdır.

## KESİN KURAL
**Project Angela (v1, v2, v3 ve tüm dosyaları) bu operasyonun hiçbir aşamasında kullanılmaz.**
`modules/project-angela/`, Angela raporları ve research_notes'taki Angela notları okunmaz, kopyalanmaz, kaynak alınmaz.
Baş sıfırdan tasarlanır. (`00_sorular.md` dosyasında Angela önerileri geçiyor; o kısımlar GEÇERSİZ.)

## Kararlar
| Konu | Karar |
|---|---|
| Kapsam | Klasik büst kesimi: hareketli baş + boyun + **sabit** omuz eğimi ve göğüs kafesinin ÜST kısmı (köprücük, manubrium, 1.–2. kaburga) + kaide. Gövde dönüşü yok, kol yok, alt kaburgalar yok |
| Ölçek | 1:1 insan boyu (göğüs tablaya göre parçalara bölünür) |
| Hedef | Sim (model.html) + baskı paketi: temiz kontroller, STL, BOM, montaj. Fiziksel baskı sonra |
| Bütçe | Satın alma tavanı **~2000 ₺**; envanterdekiler (MG996R ×6, SG90 ~6, PCA9685 ×2, 5 V 5 A ×2...) öncelikli |
| Estetik | **Robotik, Terminatör endoskeleton havası** (metalik iskelet hissi). AMA hareket gerçekçi ve insansı: göz kapağı, göz sakkadı, göz kırpma, çene, boyun — insan hareket kalitesi öncelikli |
| Kontrol (sim) | Webcam yüz takibi: baş ve gözler kullanıcıyı izler (Eye v5 / Tracking Arm altyapısı) |
| Görsel referans | InMoov (yalnız görsel ilham; STL kullanılmaz, lisans CC BY-NC) |
| Zaman | Acele yok |
| Süreç | **Checkpoint'li.** Her aşama sonunda dur: ne yapıldı, ne kadar token harcandı, sıradaki aşamanın tahmini maliyeti, karmaşıklık seçenekleri. Kullanıcı onaylamadan sonraki aşamaya geçme |

## Yazıcı / prensipler
Ender 3 Neo (~220 mm tabla, tek renk), M3/M4 vida+somun. Prensipler: `~/.claude/projects/C--Users-LENOVO/memory/epic-tasarim-prensipleri.md`.

## CP1 sonrası kararlar (2026-10-16)
- Paket **S1**: boyun N2 (yaw + 2× MG996R diferansiyel eğme/yatırma, pushrod), çene J3 (MG996R), göz E3 (5× SG90: 2 göz + sağ/sol ayrı üst kapak), kapak = metal "deklanşör" plaka, PCA #2 kafada.
- Filament: elde var, maliyet/depo hesabına katma.
- **TASARIM PRENSİBİ (kullanıcı): minimalist ama yoğun/dolu görünen.** Project Eye'da aşırı taşınan yük yüzünden tork problemi yaşandı → **hareketli kütle birinci tasarım kriteri**. Kafada gereksiz gram yok; servoları mümkünse sabit gövdeye al, ince et + kaburga/kafes, yoğunluğu kütle değil görsel detay (kenar, oluk, cıvata başı, piston) versin. Bolca araştırma + gerektiğinde köşe kes.
- **Çene–boyun boşluğu (konsept sim'den, 2026-10-16):** alt çene boyundan geçemez. Eğme servoları boynun ARKASINDA ve yatık, çene servosu kafatası yanında (kondil arkası kaldıraç). Konseptte ölçülen: nötr ~26 mm; baş −25° + çene kapalı → serbest; çene 18° açık + baş aşağı → çene boyun kolonuna −9.5°'de ulaşıyor → firmware'de **eğme–çene kilidi** şart (min 5 mm pay). Plan ve CAD bu kontrolü check_montaj/çakışma taramasına (tüm poz kombinasyonları) almalı.
- **Ders (konsept, 2026-10-16):** kozmetik boyun pistonları ramusun önünden geçince başın öne eğilmesini ~5°'ye düşürdü (kilit). Ramusun ARKASINDAN geçirilince: nötr boşluk 28 mm, çene kapalı −21°, çene açık −8°. Kural: kozmetik parça da çakışma taramasına girer. İnsan gibi ~45° öne eğilme isteniyorsa tek pivot yetmez → boyun tabanında ikinci eğme (ek tork!) planda değerlendirilmeli.

## CP2 başlangıcı (2026-10-17)
- **Konsept v5'te donduruldu** (`modules/project-bust/v5/model.html` = `konsept.html`). Görsel referans bu; gerekirse CAD sonrası revizyon.
- Açık 3 soru (H2 kabul?, dişli 2:1 mi 1:1 mi?, ~21° öne eğilme yeter mi / boyun tabanına 2. eğme ekseni?) planlayıcı tarafından rakamla karşılaştırılıp PLAN.md'de "ONAY BEKLİYOR" olarak sunulacak; son karar kullanıcıda.
- Planın ilk adımı **ölçüm kuponları** (MG996R gerçek tork/boşluk, basılı servo kolu cebi, rotil boşluğu); kütle/tork sayıları tahmin değil ölçüme dayanacak (Eye dersi).
- Kullanıcı cevapları (2026-10-17): PETG YOK → kayan parçalar PLA (boşluk +0.1, kuru yağlayıcı) veya alüminyum iç boru. Tartı: mutfak tartısı (≈1 g çözünürlük). Büst yüksekliği: sonra dış kaide/yükselticiyle ayarlanır, tasarımı bağlamaz. M2 somun: stokta (varsayım, kontrol edilecek).
- C KARARI (kullanıcı, 2026-10-17): tek pivot, ~21° öne eğilme. 2. eksen için yalnız flanş rezervi. Piston uçları: bilye-yuva YOK → M3 vida-pimli kardan (yedek M3 rotil).
- Ses paketi (kullanıcı, 2026-10-17): göğüste ESP32 + MAX98357A + hoparlör, kulakta 2× INMP441 (ses yönü), çene lip-sync; burunda kamera **rezervi** (kart sonra). Bütçe tavanı aşılabilir ("TL çıksın problem değil") → ~2360 ₺. Ayrıntı: PLAN.md §13.
- Ses alımı güncel (kullanıcı, 2026-10-17): INMP441+MAX98357 seti 551 ₺ bulundu (setteki mikrofon adedi teyit edilecek; 2 gerekir, tekse +1 INMP441 ~199 ₺) + hoparlör ~371 ₺.
- A ve B ONAYLANDI (kullanıcı, 2026-10-17): H2 (yay %75 dengeye) + pitch 1:1. CP3a = yalnız ölçüm kuponları (PLAN §8), asıl CAD kupon sonuçlarından sonra.
- CP3b ikiye bölündü (kullanıcı, 2026-10-17): CP3b-1 = torktan bağımsız parçalar (kabuklar, çene, göz modülü, göğüs, kaide, ses yuvaları) şimdi; CP3b-2 = boyun/eğme/yay/pistonlar K1 sonucundan sonra. Çıktı research_notes/Project Bust/cad/.
- Kâğıt ölçüm (kullanıcı, 2026-10-17): kuponlar beklenmeden CAD sürer; değerler KAGIT_OLCUM.md (tasarım = bandın kötü ucu, belirsizlik ayarlanabilir özelliklerle: çift rod deliği, yay sıra deliği, varyant STL'ler, firmware sınırı). Kuponlar sonra yalnız ayar seçer.
- Döngü onayı (kullanıcı, 2026-10-17): 'hallet' → CP3b-1 → CP3b-2 → denetim/doğrulama/düzeltme → v8 paket, tavan ~1.5M; son simde mik + hoparlör + webcam takibi çalışır olacak. Günlük: LOOP_LOG.md.
