# Project Bust: kâğıt üstü ölçüm + sapma payı (2026-10-17)

Kullanıcı kararı: kuponlar basılmadan CAD sürsün; değerler kâğıt üstü tahmin + sapma bandı, tasarım **bandın kötü ucuna** göre yapılır, kalan belirsizlik **ayarlanabilir özelliklerle** (çift delik, sıra delik, firmware sınırı) emilir. Kuponlar sonra yalnız ayarı seçer, yeniden baskı gerekmez.

Kaynak notu: MG996R satıcı datasheet'leri birbirini tutmuyor (4.8 V'ta 9.4–13 kg·cm stall, 6 V'ta 11–15). Klon servoların sürekli (ısınmadan tutabildiği) torku tipik olarak stall'ın ~%25–40'ı kabul edildi [mühendislik tahmini, ölçülmedi].

| # | Büyüklük | Kâğıt nominal | Sapma bandı | **Tasarım değeri** | CAD bunu nasıl emer | Kupon sonra neyi seçer |
|---|---|---|---|---|---|---|
| 1 | MG996R sürekli tork @5 V | 3.0 kg·cm | 2.0 – 4.0 | **2.5** (kötü uç 2.0'da da pay ≥ 1.2 olmalı) | pitch payı 2.5'le hesaplanır; yay ön gerilmesi **sıra delikle** %60–%95 denge arası ayarlanır; firmware'de yatırma sınırı parametre (±15 / ±10) | K1 → yay deliği + yatırma sınırı |
| 2 | MG996R çıkış boşluğu | 1.0° | 0.5 – 2.0° | **1.5°** | N4 krankında **iki rod deliği**: r = 22.8 (1:1) ve r = 15.2 (1.5:1); rod boyu ikisinde de aynı kalacak geometri | K1 → hangi delik |
| 3 | Basılı kol cebi payı (MG / SG) | 0.2 mm | 0.1 – 0.3 | **0.2** | krank küçük ve ucuz → 0.1 / 0.2 / 0.3 üç varyant STL üretilir | K2 → hangi STL basılır |
| 4 | M3 vida-pim delik çapı | 3.3 | 3.3 – 3.4 | **3.3** (sıkıysa matkapla 3.4) | — | K2 |
| 5 | M3 rotil boşluğu (metal) | 0.08 mm/uç | 0.03 – 0.15 | **0.15** | kafa kulağı d = 35 (plandaki yedek) varsayılan | K3 |
| 6 | SG90 hız @5 V | 0.11 s/60° | 0.10 – 0.15 | **0.15 s/60°** | kapak stroku ≤ 60°, 1.5× bağlantı → servo 40° → ~100 ms; bağlantıda **ikinci delik** 1.8× (daha hızlı, daha az tork) | K4 |
| 7 | Teleskop piston boşluğu (PLA) | 0.5 mm | 0.4 – 0.6 | **0.5** | piston boruları ucuz → 0.4/0.5/0.6 STL hazır | K5 |
| 8 | Kabuk birim kütlesi (1.2 mm + 1.6×5 kaburga, PLA 1.24 g/cm³) | 0.19 g/cm² | ±%15 | **0.22 g/cm²** | kütle bütçesi kötü uçla: baş ≤ 500 g bu değerle sağlanmalı | K7 |
| 9 | Yay sabiti k (alınacak yay) | belirsiz | ×0.5 – ×2 | **ayarlanabilir** | yay kancası **5 delik sırası** + makara opsiyonu; gerekli kuvvet tablosu CAD raporunda | K6 |
| 10 | Lazy susan sürtünme torku | 0.35 kg·cm | 0.2 – 0.5 | **0.5** | yaw payı 0.5 ile hesaplanır; delik çemberi için **oval delikler** (±3 mm) | K8 |
| 11 | MG996R gövde ölçüleri | 40.7 × 19.7 | ±0.3 | cep +0.3 | cepler şablondan, servo itme payı | form 0. adım |

## Kötü uç kontrolü (planın sayılarından ölçekleme)
Plan: en kötü pozda pitch payı 3.7 (yaylı, 3.5 kg·cm varsayımı), yaysız 1.9.
- Tork 2.5 ile: yaylı **2.6**, yaysız **1.4** → yay şart; hedef ≥ 1.5 yaylı sağlanıyor.
- Tork 2.0 ile: yaylı **2.1**, yaysız 1.1 → yatırma ±10'a düşürülürse en kötü poz hafifler (firmware parametresi).
- Kural: CAD raporu pitch payını **2.0 / 2.5 / 3.5** kg·cm üç satırla verir.
