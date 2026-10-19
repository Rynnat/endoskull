# Project Bust v6 — webcam yüz takibi + mikrofon (görsel v5'te donmuş)

- **Hoparlör:** "Söyle" kutusu → tarayıcı TTS (tr-TR, alçak/mekanik ton); konuşurken çene hece ritmiyle + kelime başlarında açılır; konuşurken mikrofon kendi sesine dönmez. Gerçekte ESP32 + MAX98357 + göğüs hoparlörü.
- **Kamera (yüz):** tarayıcıda MediaPipe yüz algılayıcı (tasks-vision 0.10.14, BlazeFace). Ayna görüntüsü: sen sağa geçince büst sağa bakar. Yüz kaybolunca 0.6 s sonra otonom bakışa döner. Görüş açısı varsayımı 70°×45°.
- **Mikrofon:** ses şiddeti → çene (lip-sync taklidi); ani ses → kırpma; stereo mikrofonda sağ/sol seviye farkı → o yöne dön (tam önden gelen sese dönmez). Mono mikrofonda yön yok.
- Gerçek büstte aynı mantık: kulaklarda 2× INMP441 (ESP32, göğüs), çene TTS çıkışına göre.
- Kamera/mikrofon yalnız düğmeye basınca açılır; sekme kapanınca kapanır (sunucu yok).
- Test: headless Edge + sahte medya; MediaPipe grafiği çalıştı, sahte yüz (x=0.2) → bakış +21°, baş +18.7°; sahte ses → çene 0.32 rad. Gerçek yüz/ses testi kullanıcıda.
