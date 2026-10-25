# Project Bust — yeni oturum devam noktası (2026-10-17 19:40)

Kullanıcı yeni oturumda **"epic project bust"** derse: bu dosyayı oku, sonra kaldığın yerden devam et (aşağıdaki "SIRADAKİ").

## Bağlayıcılar (önce oku)
- `KARARLAR.md` (KESİN KURAL: Project Angela hiç kullanılmaz), `PLAN.md` (§13 ses/mik/kamera eki), `KAGIT_OLCUM.md` (tasarım = sapma bandının kötü ucu), `LOOP_LOG.md` (tüm aşamalar + token), `SIPARIS.md`.
- CAD: `cad/STATE.md` (baş/gövde), `cad/STATE_CP3b2.md` (boyun), `cad/DECISIONS.md`. Python: `PYTHONUTF8=1 C:\Users\LENOVO\Projeler\epic-project\.venv-cad\Scripts\python.exe -B` (cad/ içinde).
- Kullanıcı tercihleri: ürettiğini HEMEN aç (`Start-Process` / `start ""`; Artifact open tek başına açılmıyor), ara hali sakla-ma; checkpoint'te token raporu; kısa cevap.

## Durum
| Ne | Durum | Nerede |
|---|---|---|
| Ölçüm kuponları K1–K7 | 28 STL + G-code + Arduino k1_tork.ino + k1_hesap.py; kullanıcı henüz basmadı | `kuponlar/` |
| Baş + gövde CAD (CP3b-1 + 2 estetik tur + orbita sıfırdan) | oyulmuş göz çukurları, tek tek dişler, anatomik mandibula, yassı kaburga; baş ~452 g / 500 | `cad/` |
| Boyun CAD (CP3b-2) | N1–N5, Y1, P1 gerçek parça; **tork payı en kötü 3.05–4.07 (hedef 1.5) — Eye sorunu yok**; öne eğilme −25° (çene açık −11.9°, kilit tablosu var); P2 yanak pistonu hâlâ yer tutucu | `cad/boyun.py`, `out/check_report_boyun.txt` |
| Kontroller | ana check **SORUN 33** (gövde statik: hoparlör/kartlar/yaw servo × G1; montaj_sökme; çene servo M4 alet yolu; Z1 göz–B2 0.17<0.4; ince et; yay ayar sırası) | `cad/out/check_report.txt` |
| **CAD SIM** | gerçek parçalar + CAD kinematik tabloları + v6 motoru (fare/otonom/kamera yüz/mik/TTS) + çene–eğme kilidi | panel **v12** (`modules/project-bust/v12/model.html`), artifact https://claude.ai/artifact/4j1DAnhDx2UasaewDd5862 ; üretim `cad/sim_export.py` (~2 dk) |
| Önizleme görüntüleyici | `cad/onizleme.py` → artifact https://claude.ai/artifact/EH1cyFaimpsP6W7GTrPrvN (dosya `modules/project-bust/v9/artifact.html`) | |

Panel: v1–v5 konsept, v6 konsept+sensörler, v7–v11 CAD önizleme ara halleri, v12 CAD sim. Yeni sürüm klasörüne `tools/` kopyala.

## Oturum kapanırken açık kalan
- Boyun ajanının son tam taraması (`check.py`, 18:45'ten beri, çok yavaş: B2 ~900k üçgen) muhtemelen yarım kaldı; ajanın final raporu GELMEDİ. Yeni oturumda: `cad/out/check_report.txt` ve `STATE_CP3b2.md` tarihlerine bak; tarama tamamlanmadıysa çalışan `check.py` süreçlerini durdur.

## SIRADAKİ (sırayla; her birinde token raporu, sonuçları hemen aç)
1. **Tarama hızı:** B2'nin kontrol kopyasını sadeleştir (ya da çarpışmada seyreltilmiş B2) → tam check'i tamamla (~10–20k).
2. **Kullanıcının son isteği — arkadaki kütle omurgaya:** iki eğme MG996R'ı dik/sırt sırta boyun kolonunun arkasına, etrafına omur görünümlü kasa (gövde + diken çıkıntıları); P1 piston alt uçları arka L-kulelerden kolon tabanına (öne-yana, SCM gibi); N1 tablası küçülsün. Sonra strok, diferansiyel tork, poz_kilit, kablo yeniden. ~120–200k. (Kullanıcı "bağlayamaz mıyız" dedi; öneri sunuldu, onay bekleniyor → önce sor/teyit et.)
3. 33 bulguyu kapatan temizlik turu (~100–150k) + P2 yanak pistonları.
4. Denetim (denetci-v2) → doğrulama (dogrulayici) → düzeltme (≤2 tur).
5. Final paket: sim v-son, STL'ler, BOM, montaj sırası, tabla/süre.
6. Estetik açıklar (sonra): orbita tavanı (B3'e eklenmeli = plan kararı), kubbe alt kenarı kask siperi gibi, şakak duvarı.

## Token
Toplam ~2.9M (döngü tavanı 1.5M ~0.4M aşıldı; kullanıcı açık komutlarla devam ettirdi). Yeni büyük aşamadan önce tavan sor.

## 2026-10-17 ~20:00 güncelleme
- B2 910k -> 50.7k üçgen (build.py: >100k üçgende simplify 0.02 mm + kırıntı atma; `build.py --sadelestir --only X`). Tam check yeniden başlatıldı (19:56).
- Madde 2 (omurga) ONAYLANDI, cad-tasarimci-v2 çalışıyor -> çıktı cad/STATE_omurga.md, referans rapor out/check_report_oncesi_omurga.txt. Oturum tavanı 500k.
- Paralel estetik ajanı (cad-tasarimci-v2) cad_estetik/ kopyasında: orbita_tavan / kubbe_kenar / sakak, params.ESTETIK anahtarlarıyla tek tek geri alınabilir; çıktı cad_estetik/STATE_estetik.md. Bitince beğenilen anahtarlar cad/'a birleştirilip tam check.
- 20:15: tam check SORUN 29 (33'ten; 4 plan_sapmasi etiket bulgusu kapandı, geometri aynı; sure 13.5 dk). Paralel 3 ajan: BULGU_TRIYAJ.md (29 bulgu ayıklama), 08_yanak_piston_omurga_ref.md (T-800 P2 + omurga ref), 09_satin_alma_risk.md (yay R6, lazy susan K8, rotil, MG996R R2).
- 20:30: omurga ajanı tasarımı hesapladı (STATE_omurga.md); kullanıcı P1 = (a) arka-yan kasaya, tavan 650k. Ajan CAD'e devam ediyor.
- 20:45: bitti -> 09_satin_alma_risk.md (MG996R 3.5 kg*cm hafif iyimser, 4 servo stall 10 A > 5 A hat, K1 öne), BULGU_TRIYAJ.md (16 gerçek; G1 tek turda 7 bulgu; Z2 UST_RI >= 15.6), 08_yanak_piston_omurga_ref.md (P2 öneri A, omurga O3; mm'ler [H]). Etkileşim ajanı -> modules/project-bust/v13 (+ cad/sim_sablon.html). Bütçe ~740k tahmini > 650k tavan, kullanıcıya soruldu.
- 20:50: v13 sim 'İnsan görüntüden çıktı' eklendi (18/18). Kullanıcı: boyun 'çok arkadan geliyor, insansı değil, Terminatör tarzı' -> boyun ajanına siluet turu: yay kalk (yaysız @2.2 kg*cm >= 1.5 ise), P1 SCM öne-aşağı N1 ön kenarına, O1 kasa yukarı/kafatası altına; metrik 'arka taşma' <= 0.
- 20:55: estetik turu ZAYIF bulundu (orbita_tavan = şapka siperi, sakak az fark; kubbe_kenar iyi). Referans ajanı -> ref_t800/ (görseller + KAYNAKLAR.md + ORANLAR.md). Sonra referansla yan yana karşılaştırmalı kafatası kaynaştırma turu.
- 21:05: ref_t800/ hazır (18 görsel, ORANLAR.md; telifli, yalnız iç referans). Boyun ajanına: boyun kafatası izdüşümünde, arka taşma <= -40 ideal. Estetik ajanına: referanslı kafatası kaynaştırma turu (kas_kemeri / sakak_pencere / kubbe_arka_inis anahtarları, yan yana kars_*.png).
- 21:12: panel v14 = sim_export (omurga2 ara hali, yay yok, B2 sade) + v13 etkileşim; 18/18. Kafatası estetiği henüz yok.
- 21:30: omurga2 BİTTİ (STATE_omurga.md): arka taşma +45 -> -2.1, yay kalktı (yaysız @2.2 +%30 pay 2.70), N1 30.8, öne eğilme -25 korundu, SORUN 36 (+7 küçük). Açık karar: P1 -> kozmetik örgülü hortum (taşma ~-40). Kafatası turu 3. iterasyon da zayıf -> öneri: sökülebilir YAN PLAKALAR (kubbe->kulak hizası, zigomatik + şakak penceresi) + kalın alın kemiği. Bekleyen sorular: yan plaka turu, P1 hortum, yüz ifadesi (FaceLandmarker).
- 22:25: estetik TUR 2 BİTTİ (cad_estetik/STATE_estetik.md): kubbe_kenar/sakak/kas_kemeri/sakak_pencere True, orbita_tavan False; SORUN 30, baş 465.9 g; B3 kaynaklı bulgu yok. Birleştirme: _tmp/estetik_*.patch -> cad/, sonra build --only B2,B3L,B3R + tam check. Kalan: kubbe arka-alt göz hizasına inemiyor (C1 krank x61-65, B1 arka direk) -> yan plaka turu mekanizma yer değişikliği ister. Kullanıcıya birleştirme sorulacak.
- 22:35: KARAR (kullanıcı): kafatası primitiflerle olmuyor -> YENİDEN TASARIM: dış kabuk hazır heykel T-800 modelinden (1:1 ölçek, içi boşalt 1.2 mm, B2/B3/B4'e böl, mekanizma içine sığdır; ters sıra: kabuk ana kısıt). Model avı ajanı -> ref_t800/MODEL_ADAYLARI.md; kullanıcı modeli seçecek, sonra indirme + plan. cad_estetik birleştirmesi askıda (yeni kabukla gereksiz olabilir).
- 22:55: MODEL İNDİRİLDİ: MakerWorld 1714306 (CAGLAYAN NARTA, ücretsiz, Standard Digital File = kişisel, YAYINLAMA) -> model_makerworld/raw (12 STL; Skull_hi_poly 140.7x212.5x161.3, yüz -Y, Z yukarı; mandibula+pistonlar ayrı). bak.py önizleme. Kullanıcı hesabı: MakerWorld onboarding dolduruldu (Experienced, ToS kullanıcı isteğiyle).
- YENİ DAL "y" = panelde YEŞİL v<N> (klasör modules/project-bust/y<N>); app.py v21 + ui/index.html (_versions [vy]\d+, y serisi v'den sonra; yedek $TEMP/app.py.bak). CAD çalışma klasörü cad_y/ (cad/ kopyası). y1 = model yerleşimi + çakışma haritası + ilk sim (cad-tasarimci-v2 çalışıyor -> cad_y/STATE_y1.md).
- 23:15: y1 BİTTİ (cad_y/STATE_y1.md, modules/project-bust/y1 18/18): ölçek 1.0 (göz arası 63.4 vs 65, %2.5), mandibula modelin pimine (pivot bizim çerçevede (0,-25,31), kondilden 28 aşağı 21 önde). Model kabuğu dolu/kalın: kafatası 1388 cm3 malzeme (~1.7 kg PLA) -> KÜTLE RİSKİ (baş sınırı 500 g, tork). Çakışma: B1 16.1 cm3 (±56.6), B5a 7.6, SG90 1-3.9, kamera maksillada, MG996R+C1 şakak penceresinden görünüyor. y2 önerisi: kabuğu boşalt (~3 mm) + kubbeyi y~60'tan kes (sökülebilir), çene pivotu modele + MG996R/C1 kubbe içine, göz modülü daralt (GOZ x ±31.7), B1 ±36, B2 kalkar. Kullanıcı onayı bekleniyor.
- 23:25: kullanıcı: hoparlör+mikrofon+kartlar CAD'e gerçek ölçülerle, lehimli başlık + gerçek kablo yolları; sonra çakışmaları çöz; MODÜLER yapı (göz modülü, çene modülü vb. ayrı parçalar). Aşama 1: kart ölçüleri ajanı -> 10_kart_olculeri.md + cad_y/kartlar.json. Aşama 2: planlayici ile modüler mimari planı (onaya). Aşama 3: cad-tasarimci-v2 -> y2.
- 23:40: PLAN_y2.md hazır (cad_y/): 9 modül (ÇEKİRDEK şasi + GÖZ/ÇENE/KULAK/KAFATASI; BOYUN/YAW/GÖĞÜS-ELEKTRONİK/GÖVDE), kabuk EDT boşaltma, kubbe y=60 kesim; kabuk 2.0 mm -> baş ~675 g, pay 1.90 (500 g spec değişir); yaw hız 60°/0.4 s sınırı; CAD G0-G11 ~445-485k; satın alma +~540 TL. 4 açık karar kullanıcıya soruldu.
- 23:48: KULLANICI ONAYI y2: kabuk 2.0 mm (~675 g, pay 1.90; 500 g spec -> ~700 g), PCA#2 kafada, P1 örgülü hortum, tabla 256. Fazlar: A = G0-G4 (kart kütüphanesi, kabuk boşaltma, kesimler, çekirdek K0, göz modülü) ÇALIŞIYOR; B = G5-G8 (çene, kulak, göğüs elektronik, kablolar); C = G9-G11 (check'ler, çakışma turu, sim y2). Her faz sonunda kullanıcıya rapor.
- 00:20 (10-18): Faz A G0 (kartlar.py, temiz) + G1 (EDT kabuk; dış alan 1314 cm2; t2.0 -> kafatası 318 g, mandibula 79 g, baş 704 g, pay 1.82) bitti. Ajan G2-G4 için devam ettirildi.

- 2026-10-18 y2 Faz A G0-G4 bitti (bas 723 g, pay 1.78). Acik: goz modulu K0'a oturmuyordu -> KULLANICI KARARI: goz K-yuz yan duvarlarina baglanacak; sim (yesil v2) bu duzeltmeden SONRA cikacak. Ajan a07e0ac duzeltiyor. Onizleme: cad_y/out/onizleme.html
- 2026-10-18 ara sim yesil v2 (modules/project-bust/y2): ara_sim_y2.py + modul_sim.py (scratchpad) ile; MODULLER paneli (9 modul ac/kapa, tek modul, patlat, modul renkleri). Goz yan duvar duzeltmesi gelince ayni betikle yenilenecek. BEHTEST 18/18.
- 2026-10-18 G4b bitti: goz K-yuz yan duvarina 4x M3 alttan; montaj sirasi K-yuz -> K0 -> GOZ (goz K-yuz sokmeden servis). Faz A TAMAM (~405k token). Sim y2 yenilendi (18/18). SIRADAKI: Faz B (G5-G8: cene, kulak, gogus elektronik, kablolar) - kullanici onayi ile.
- 2026-10-18 Faz B ajani baslatildi (G5 cene, G6 kulak, G7 gogus tepsi, G8 lehimli kablolar). SIRADA: vida/baglanti ajani (tum modulleri vidayla baglar; ic ya da dis ek parcalar, tercih ajanin) - Faz B bitince baslat. Sonra sim yenile (ara_sim_y2.py + modul_sim.py, scratchpad).
- 2026-10-18 Faz B bitti (~690k token): cene servosu agiz boslugunda (pay 2.1), sakak kapaklari + INMP, gogus 2 tepsi, 21 kablo + 2 hortum. Bas 793 g, pay 1.63. KARAR BEKLEYEN: K-G5 cene-boyun kilidi, K-G6 kapak dolgusu, K-G8 yaw kablo yolu, K-G8b uzatma kablolari. Vida/baglanti ajani (G9a) basladi. Sim y2 Faz B ile yenilendi (183 parca, 11 modul, 18/18).
- 2026-10-18 G9a vida/baglanti bitti (~470k): 22 gizli baglanti hatasi bulunup duzeltildi, 31 vida, BOM STATE_y2'de; bas 813 g pay 1.59. KARAR BEKLEYEN ek: K-G9a-1 MG996R 2 arka vida, K-G9a-2 P1 ust yuva K-yuz'de. Sim y2 yenilendi.
- 2026-10-18 KULLANICI: 'onerilerle devam et ve onerilerle devam etmeye devam et' (evden cikti). Tum bekleyen kararlarda onerilen secenek uygulaniyor. Faz C ajani basladi (kararlar + G9 tam kontrol + G10 sorun turlari + G11 kupon/baski listesi/BOM). Bitince: sim y2 yenile (scratchpad ara_sim_y2.py + modul_sim.py), test, ac.
- 2026-10-18 Faz C bitti (~600k): oneriler uygulandi (kilit tablosu, kapak %15, FFC saat yayi yaw ±70, uzatma BOM). SORUN 128 -> 108 benzersiz; bas 786 g pay 1.64; 6 kupon, baski listesi 56 kalem, BOM. Sim y2 yenilendi (208 parca, 18/18). SIRADAKI ONERI: (1) kesim payi 0.7 ile dar bosluk turu (~1 sa), (2) W2_cene x N2 ve W1_X1_g x G1 kablo kesisimleri, (3) kuponlari CC2'de bas + tezgah testleri, (4) parcalari olc (ESP32, INMP441, hoparlor, DC jack).
- 2026-10-19 G10 tur 4 bitti (~450k, ~4.5 sa): SORUN 108 -> 41 benzersiz, kesisim ve dar bosluk 0; kalanlar et/kabuk/kupon/hortum. Bas 785 g pay 1.64. Sim y2 yenilendi. CAD TURLARI DURDU. SIRADAKI: kuponlari CC2'de bas (out/stl_y2/kupon_*), kartlari kumpasla olc, sonra gercek olculerle tek son tur. Not: ajanlar mspaint'e bosluklu yolu tirnaksiz verince 'Untitled' bos Paint aciliyor.
- 2026-10-19 Terminator sesi: meSpeak.js (tr) + WebAudio zinciri (perde/bit/satur/ring/tarak/EQ/yanki/kompresor), 7 tur olcum dongusu (F0 ~94 Hz, sapma 0.5 yt, 3 hece/sn). Sim'de 'Ses: Terminator/Dogal' + kaydiricilar; ?sestest 7/7, ?test 18/18. Dosyalar cad_y/sim_y2/ses_sim.py + ses/. Kulakla degerlendirme BEKLIYOR.
- 2026-10-19 sim: boyundan gecen 4 kablo + 2 orgulu hortum artik pozla hareket ediyor (g8.kablo_pts/hortum_pts, yaw 5 x pitch 10 x roll 7 izgara, sim'de tup ara degeri; ara_sim_y2.py bolum 6 + modul_sim KAB). FFC saat yayi hala yaw 0'da statik. Testler 18/18, 7/7.
