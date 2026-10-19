# Project Bust v13 — CAD SIM + Etkileşim
v12 (gerçek CAD parçaları, CAD kinematiğinden eklem tabloları, v6 hareket motoru, çene-eğme kilidi) + **davranış katmanı**.

## Etkileşim paneli
- **Etkileşim**: aç/kapa (açınca kamera moduna geçer). **Konuşma**: TTS aç/kapa. **Sesli komut**: tr-TR konuşma tanıma (tarayıcı desteklemiyorsa pasif).
- Yüz: ilk görünce "Bir insan görüyorum." / 2+ kişi "İki kişi görüyorum."; 4 sn kaybolunca "Nereye gittin?"; yüz kutusu büyükse "Biraz geri çekil."; 8 sn+ bakınca göz kırpma + baş yatırma; 30 sn kimse yoksa boşta (etrafa bakınma).
- Nesne: MediaPipe ObjectDetector (efficientdet_lite0, COCO), ~2.5 Hz, güven ≥ 0.5, Türkçe etiket; aynı nesneyi 45 sn görmeden tekrar söylemez.
- Komutlar: "merhaba" (selam + baş sallama), "adın ne", "ne görüyorsun", "sus"/"sessiz", "konuş".
- Konuşma kuyruğu (üst üste binmez), çene mevcut TTS senkronuyla. Jestler yalnız ofset verir; eklem sınırları ve çene-eğme kilidi aynen uygulanır.

## Test
`model.html?test` → durum makinesi sahte algılama girdisiyle sınanır; sonuç sayfa başlığında (BEHTEST PASS n/n) ve panelin altında.

Üretim: research_notes/Project Bust/cad/sim_export.py (şablon sim_sablon.html v13 katmanını içerir).
