# CP3a kuponları — kararlar (2026-10-17)

Project Angela dosyaları okunmadı/kullanılmadı. Kaynak: PLAN §3/§6/§8, KARARLAR.md, agent-flow/sablonlar + checks.

## PLAN SAPMALARI
- PLAN SAPMASI: "tek tabla ~2–3 saat [T]" yerine **2 tabla**, toplam ~22 sa 25 dk / ~176 g (Orca CLI, Epic POC). Neden: K1 servo tutucusu (100 mm kol + ağırlık + 2 ölçü çıkıntısı) ve 3+3 kol varyantı tek tablaya sığmıyor (bbox alanı 57 800 mm², tabla 44 100 mm²). Kesitleri 4–6 mm olan parçalar 3 duvar + 4 kat üst/alt ile neredeyse dolu basılıyor; profil hızları düşük (25/40 mm/s).
- PLAN SAPMASI (kullanıcı kararı, KARARLAR 2026-10-17): K5 PETG 0.3/0.4/0.5 değil, **PLA 0.4/0.5/0.6**. Küresel soket (bilye-yuva) yerine **M3 vida-pimli kardan**. K3'te basılı küresel mafsal YOK, yalnız metal M3 rotil.
- PLAN SAPMASI: K2 "2 kg·cm'de kayma yok" testi yalnız MG996R'da yapılıyor. SG90'ın kapasitesi ~1.2–1.8 kg·cm, ayrıca K4'te mili dikey duruyor; SG cebinin tork altında kayması K4'te dolaylı görülür.

## Tasarım seçimleri
- K1 kol cebi payı 0.2 (servo_kolu varsayılanı [TASLAK]). K1 boşluk ölçümü cep payını da içeriyor; ayrımı K2 MG verir (form notu).
- K1 ölçü çıkıntıları kolun 8 mm altında duruyor, yani **kasıtlı aşağı durdurucu**: K1 kolu −4.0°, K2 MG kolu −8.5°. 2° sarkma ölçülebiliyor (110 mm'de 3.8 mm), kol düşerse çıkıntıya oturuyor.
- K1 ilk sürümü 153 cm³ (dolu duvar) idi → 54 cm³ hafif sürüm: servo plakası + kiriş + direkler. Kiriş altındaki 85 mm köprüyü `sarkma.kontrol_sarkma` yakaladı (z 33.1, 300 mm²). Ara direklerle köprü ≤ 22 mm'ye indi, check TEMİZ.
- K1 kulak delikleri ±1.5 mm uzun delik: kulak aralığı [TAHMIN] 49, kabul aralığı 46–52 mm. M3 vida MG996R'ın ~Ø4.5 kulak deliğinden geçer.
- K4 bağlantısı: R1 12 / R2 8 / tel 40. Ortada oran 1.50, servo 50° → disk 78.7° (ortalama 1.57). Kapak stroku 75° hedefine uygun.
- K4 M2 somun kanalı (SG90 kulağı) ve M3 somun yan kanalı (disk pimi): sablonlar'da M2 somun yok, kanal da [TASLAK]. Kural gereği şablona eklenmedi, kupon içinde `m2_somun_kanalli()` olarak duruyor. Kupon M3 kanalını da deniyor.
- K5 kardan: dili kalın, çatallı **çift çatal** orta parça; eksenler arası 14.6 mm kaçık (vida pimleri kesişemez). Dil omzu loft yerine 45° koni: loft K5_kardan_ic'te kapalı olmayan mesh ve ±25°'de orta parçaya 18.5 mm³ çakışma üretti.
- Etiket istisnaları (kabartma yerine **oyma**): kardan tüp dili (kabartma 0.4 çatal boşluğunu yerdi), K1 kadran ve K3/K4 açı çizgileri (okuma çizgisi). K2 sabit blok etiketi yan yüzde (üst yüzü dönen kol süpürüyor).
- K7 kaburga yüksekliği 5 mm, kabuk iç yüzünden ölçüldü (toplam 6.2). 07 §4 "1.6×5" ifadesinin yorumu bu. Boss Ø10, kabuktan 5 mm yüksek.
- K5 tüp eti 0.8 (PLAN §2.1) ve K7 kabuk 1.2 bilerek MIN_ET 1.6'nın altında. `kontrol_et` çalıştırılmadı, gerekçesi raporda OLCULMEDI.

## Yeni check / şablon
- Yeni genel check yazılmadı, sablonlar'a dokunulmadı (checks/ ve sablonlar/ değişmedi, regresyon gerekmedi). Görev kupon; yakalanan hatalar mevcut check'lerle bulundu: sarkma (K1 kiriş), havada_ada (K1 kol ve K3 etiketleri cep/oyma üstünde), cakisma (K2 pim etiketi, K5 loft).
