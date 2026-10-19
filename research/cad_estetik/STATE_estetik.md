# STATE_estetik (cad_estetik/, paralel estetik ajani) - 2026-10-17

## TUR 1 (orbita_tavan / kubbe_kenar / sakak) - BITTI, kullanici+koordinator: tavan ve sakak zayif, kubbe_kenar iyi
Anahtarlar `params.ESTETIK` (+ gecici ortam override `ESTETIK="sakak=0,..."`). Hepsi False -> eski kod yolu birebir:
B2 39.35, B3L 46.864, B3R 45.774 cm3 (degismemis kodun bugunku ciktisi; cache'teki eski B3 46.724/45.587 bayatti).

| anahtar | parca / fonksiyon | hacim etkisi | gorsel |
|---|---|---|---|
| orbita_tavan | B3: `_orbita_tavan`, `_kubbe_on_z`, `_B3` (tavan + B3R'de dil boslugu) | +4.1 cm3 (~+5 g) | ref/estetik_orbita_tavan_{once,sonra}.png |
| kubbe_kenar | B3: `_y_kenar`, `_bolge_egri`, `_kenar_bandi`, `_bolge`, `_kubbe_ham` | -4.85 cm3 (~-6 g) | ref/estetik_kubbe_kenar_{once,sonra}.png |
| sakak | B2: `_yuz_satirlar`, `_yuz_kabugu`, `_kas_dolgu` (+ params.EST_SAKAK) | +2.1 cm3 (~+2.6 g) | ref/estetik_sakak_{once,sonra}.png |
| hepsi | | B2 41.43, B3L 46.39, B3R 45.52 (net +1.4 cm3) | ref/estetik_hepsi.png |

**Check (tam, hepsi acik, 40 dk):** SORUN 121. Yeni bulgularin TAMAMI tek neden: B3L x B3R 6.3 mm3 (tavanin kabuga gomulu ucu B3L bindirme diline giriyordu; her pozda tekrarlandi: goz/kapak 81 + cene 9 + statik 1). Duzeltildi (B3R tavanindan dil bandi + 0.4 cikarildi, B3L x B3R = 0.0 mm3); tam check tur 2 sonunda yeniden kosulacak. B3 sokme yollari serbest (B3L 76 mm, B3R 70 mm). Diger bulgular onceki listeyle ayni (kapsam disi).
Raporlar: out/check_report.txt (tur 1), onceki: _tmp/check_report_oncesi_estetik3.txt.

## TUR 2 (T-800 referansi, ref_t800/ORANLAR.md) - BITTI
Anahtarlar (params.ESTETIK): `orbita_tavan False` (siperlik; kod duruyor), `kubbe_kenar True`, `sakak True`, **`kas_kemeri True`**, **`sakak_pencere True`**.
Hepsi False -> B2 39.35 / B3L 46.864 / B3R 45.774 cm3 = eski (tekrar dogrulandi).

| anahtar | ne degisti | dosya / fonksiyon | hacim (yalniz bu anahtar) |
|---|---|---|---|
| kas_kemeri | Kas bandi B3'te: alt yuz y 48.6 (+2.5 orbita kemeri, goz pitch bolgesinde |x|<=48.5 ya y 52.4 ya z >= 81), on = min(104, kubbe+5.5) -> yanda kubbeye doner; yan uclar dolu kapak. Kubbe onu z'de %11'e kadar gerdirildi -> alin basamaksiz. **B2 y <= 47'ye kirpilir** (B2 de yeniden uretilmeli). | yuz_kubbe: `kafatasi` (gerdirme sarmali), `_gerdir_np/_gerdir`, `_kas_kemeri`, `_B3`, `_kubbe_ham` (detaylar gerdirilir), `B2` (kirpma) | B3 +4.3/+4.2 cm3, B2 ~-5.4 cm3 |
| sakak_pencere | Yan duvarda kapali oval pencere (z -48..36, y 50..90) + 1.6 x 8 mm ice donen dudak; alt bant y 46..50 kalir | yuz_kubbe: `_oval_x`, `_B3` | B3 -2.0 cm3 her yari |

**Kutle (check kutle_butce, hepsi acik):** bas TOPLAM 465.9 g / 500 (tur oncesi 468.2). B3L/R 52.7 g (kabuk alani), B2 42.2 g.
**Karsilastirma gorselleri (sol ref, sag bizim):** ref/kars_{yan,on,on34}_{1,2,3,son}.png (son = final). Iterasyon: 1 = duz alin plakasi + yay kenarli pencere, 2 = gerdirilmis kubbe + kas, 3 = kas kubbe egrisini izler + kapali oval pencere.
**Kalan farklar (referansa gore):** kas bandi duz yatay (ref'te her gozun ustunde kemer + ortada dikey oluk); goz cukurlari hala "gozluk" gibi (B2/B5, kapsam disi); pencere altinda (y < 46) kapali sakak kemigi yok ve kubbe arka-alt kenari goz hizasina inmiyor (C1 krank x 61.4..65.4 ve B1 arka direk kabuk icinde kaliyor -> mekanizma degismeden yapilamaz); panel cizgileri islenmedi.
**Check (tur 2 son, tam, 28 dk):** SONUC SORUN (30) (tur oncesi 33). B3 kaynakli bulgu YOK: goz/kapak 81 poz + cene supurmesi 0 bulgu (ilk tam taramada kas alti x B5g/B5h pitch +-24 108 bulgu cikti -> pitch bolgesinde kas alti y 52.4 / z >= 81 ile kapandi), B3L x B3R 0, B2 x B3 0, B3 sokme yollari serbest. Kalan 30 bulgu eski listeyle ayni (kapsam disi). et_kabuk B3 %2.5-2.9 (oncesi %2.8-3.3, kaba isin).  onizleme: out/onizleme.html (hepsi acik).

## Birlestirme (cad/'a tasima)
- cad/params.py ve cad/yuz_kubbe.py su an _tmp/est_base ile AYNI -> yamalar temiz uygulanir: `_tmp/estetik_params.patch` (yalniz dosya sonuna ESTETIK blogu ekler), `_tmp/estetik_yuz_kubbe.patch` (yalniz yuz_kubbe.py). Baska dosya degismedi (bas.py, zarf_b2, build, check dokunulmadi).
- Birlestirmeden sonra cad/'da: `build.py --only B2,B3L,B3R` (zarf_b2 yeniden gerekmez: B2 yalniz kirpildi/sakak satirlari zarfla kesiliyor), sonra tam check.
- Anahtar atmak: params.ESTETIK'te False. kas_kemeri False iken B2 kirpilmaz (eski kas satirlari doner).
