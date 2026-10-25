# CP3a kuponları — durum (2026-10-17)

Durum: kuponlar hazır, `out/check_report.txt` → SONUC: TEMIZ. Sıradaki adım kullanıcıda: bas, `OLCUM_FORMU.md`'yi doldur. Asıl büst CAD'i (PLAN §9) kupon sonuçlarından sonra başlar.

Üret / kontrol (kuponlar/ içinde, `PYTHONUTF8=1 C:\Users\LENOVO\Projeler\epic-project\.venv-cad\Scripts\python.exe -B`):
`build.py [--only a,b]` → `out/stl/*.stl` + `out/tabla/tabla_1.stl`, `tabla_2.stl`, `yerlesim.txt` · `check.py` (~3 dk) · `render.py` → `out/render/*.png`.
Dilimleme: `C:\Users\LENOVO\Projeler\_arsiv\qr-stand\araclar\dilimle.py`. tabla_1 birleşik STL: 12 sa 33 dk / 105 g. tabla_2 birleşik STL'de Orca CLI hata verdi ("found error"); aynı 20 parça ayrı nesne olarak verilince tek tablada dilimlendi: 9 sa 52 dk / 71 g. Bu yüzden tabla_2'yi Orca'ya ayrı STL'lerle yükle ya da `yerlesim.txt`'yi kullan.

Açık kalanlar (görsel tur sınırı 2 doldu, düzeltilmedi):
- Hafif K1 tutucu (2. görsel turdan SONRA değişti) render edildi (`out/render/K1_*.png`) ama görsel olarak yeniden incelenmedi. Yalnız check'lerle doğrulandı: tek gövde, ada, sarkma, çakışma, sökme.
- Yazıların okunurluğu (0.6 kabartma, 2.5–5 mm) baskıda görülecek. K1 kadranındaki ince çizgiler (2°'de bir, r 29–36) kalabalık olabilir.
- Satın alınan parça ölçüleri [TAHMIN] (MG996R, kit kolları, rotil). Formun 0. adımında ölçülecek. Fark çıkarsa `params.py` + `build.py --only <parça>`.
- K4 tel yolu modellenmedi. Telin krank, disk ve direkle çarpışmadığı gözle kontrol edilecek.
- M2 somun envanterde teyitsiz (K1/K2/K4'te 6 adet gerekiyor).
