# Project Bust — döngü günlüğü

Başlangıç 2026-10-17. Kullanıcı: "hallet" — tavan **~1.5M token** (döngü içi), başlangıç toplamı ~1.13M.
Akış: CP3b-1 kontrol → v7 · CP3b-2 (boyun/eğme/yay/piston, KAGIT_OLCUM) · denetci-v2 → dogrulayici → düzeltme (≤2 tur) · paket + v8.
Ek gereksinim (kullanıcı): **son simde mikrofon, hoparlör (konuşma) ve webcam yüz takibi çalışır olacak.**
Dur koşulları: tavan · 2. turda kritik bulgu · plan değiştiren sonuç (baş > 500 g, öne eğilme < 21°, bütçe dışı parça).

| Zaman | Aşama | Sonuç | Token (tahmini) | Sıradaki |
|---|---|---|---|---|
| 10-17 | Döngü kuruldu; v6: hoparlör (TTS + çene senkronu) eklendi, headless test çene 0.22 rad | tamam | ~10k | CP3b-1 bitişi |
| 10-17 | Panel: Bust modülüne ⚙ araçları (📏 ölçüm kuponları, 📂 plan/kararlar) eklendi; v7/v8 klasörlerine tools/ kopyalanacak | tamam | ~5k | CP3b-1 bitişi |
| 10-17 | CP3b-1 tur 1: 31 STL, baş 441.5 g (≤500 ✓), check SORUN 268 (alt kapak bağlantısı çözülmüyor, kapak/göz kolu süpürme çakışmaları, gövde bindirme, B2 iki gövde, baskı adaları); B1 58 g > 40. model.html yok | 400k tavanında durdu | ~454k | CP3b-1 tur 2 (≤200k): düzeltme + dilim + model.html |
| 10-17 | **Bütçe uyarısı:** döngü içi ~470k harcandı, kalan ~1.03M. Kalan iş tahmini: CP3b-1 son 0.2M + CP3b-2 0.5–0.8M + denetim 0.4–0.6M = 1.1–1.6M → tavan muhtemelen denetimden önce dolar; dolarsa CP3b-2 sonunda durup kullanıcıya dönülecek | — | — | — |
| 10-17 | CP3b-1 tur 2: SORUN 268→33 (göz/kapak/çene süpürmesi 0; alt kapak çözüldü); baş 437.9 g; B1 54.6 g; gövde statik + montaj açık | bütçede durdu | ~167k | — |
| 10-17 | Önizleme (onizleme.py) → panel **v7** (kontroller temiz değil etiketli) | tamam | ~25k | **DURDU: görsel konseptten saptı (alt yüz kova/silindir, kaburgalar boru halka, omuz kubbe) → kullanıcı kararı** |
| 10-17 | Kullanıcı: estetik tur → ajan (≤250k): alt yüz/maksilla/elmacık/burun, mandibula (gonial açı, ramus), kaş/şakak geçişi, yassı kaburga, S köprücük, akromion; mekanizma sabit. Referans cad/ref/ | başladı | — | estetik sonucu → kullanıcıya göster |
| 10-17 | Estetik tur: B2 maksilla/elmacık/burun, B4 anatomik mandibula, G2 yassı kaburga/S köprücük/akromion; SORUN 33→23; baş 446.3 g → panel **v8** | tamam | ~187k | kullanıcı: CP3b-2 mi, 2. estetik mi |
| 10-17 | 2. estetik tur ARA HALİ kullanıcıya gösterildi → panel v9 (SORUN 24; dişler tek tek, orbita hâlâ çerçeve gibi) | ara | ~139k | ajan raporu |
| 10-17 | 2. estetik tur bitti: orbita huni + kaş rafı + burun kemiği, armut açıklığı düzeltildi, tek tek dişler; SORUN 23; baş 447.0 g; orbita hâlâ çerçeve gibi okunabiliyor (şakak duvarı yok) → v9 + artifact güncellendi | tamam | ~110k | kullanıcı kararı |
| 10-17 | Orbita sıfırdan (oyulmuş göz çukurları) ara hali → panel v10 + artifact v3; kullanıcı: 'CAD'e dahil et' → **CP3b-2 başladı** (boyun/eğme/yay/piston, ≤550k, 300k'da ara rapor). Döngü tavanı (1.5M) bununla ~0.3M aşılacak — kullanıcının açık komutu | başladı | — | ara rapor @300k |
| 10-17 | CP3b-2 ara rapor (~290k): N1–N5, Y1, P1 gerçek parça; krank 1:1 maks 51° ✓, 1.5:1'de −25°+roll ±10 çözülmüyor; rotil 16.6° ✓; yay denge 0.74–0.80; tork/poz_kilit henüz yok → panel v11 + artifact v4; ajan devam (≤250k) | ara | ~290k | final rapor |
| 10-17 | Orbita sıfırdan bitti: tek yüz kabuğu + boolean oyuk, mekanizma zarfı (zarf_b2.py); SORUN 25 (Z1 tolerans 0.17<0.4, B2 et %14.6 yeni); baş ~452 g; tavan yok (B5 yukarı sökülüyor), kubbe alt kenarı kask siperi | tamam | ~120k | v11 güncellendi |
| 10-17 | **Bust CAD SIM** (sim_export.py + sim_sablon.html): gerçek CAD parçaları, CAD kinematiğinden eklem tabloları, v6 hareket motoru (fare/otonom/kamera/mik/TTS), çene-eğme kilidi → panel **v12** + artifact 4j1DAnhDx2UasaewDd5862 | tamam | ~60k | boyun ajanı final |
| 10-17 19:40 | Oturum kapanıyor: DEVAM.md yazıldı; boyun ajanının son taraması yarım (B2 900k üçgen yavaşlatıyor); bekleyen istek: eğme servo kütlesi omurgaya | durdu | — | yeni oturum: 'epic project bust' |
