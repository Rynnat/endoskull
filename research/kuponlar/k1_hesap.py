"""K1 olcumlerinden surekli tork + bosluk -> plan karari (OLCUM_FORMU.md K1 esikleri).

Kullanim: python k1_hesap.py   (degerleri asagidaki OLCUM listesine yaz)
Satir: (servo, d_cm, m_g, sarkma_mm, elle_tutulur)   sarkma = yuklu - yuksuz bosluk farki (mm)
"""
OLCUM = [
    # ("A", 10, 250, 1.2, True),
]
BOSLUK = {  # servo: (yukari_mm, asagi_mm)
    # "A": (0.0, 0.0),
}
KOL_G = 0.0           # tartilan kol kutlesi (g); 0 ise model degeri 0.06 kg.cm kullanilir
SARKMA_SINIR = 3.8    # mm @ 110 mm cikinti = 2 derece

kol = KOL_G / 1000 * 4.7 if KOL_G else 0.06
gecen = {}
for sv, d, m, sark, sicak in OLCUM:
    t = m / 1000 * d + kol
    ok = sark <= SARKMA_SINIR and sicak
    print(f"{sv}  d={d:>4} cm  m={m:>5} g  tork={t:5.2f} kg.cm  sarkma={sark:4.1f} mm  {'GECTI' if ok else 'kaldi'}")
    if ok:
        gecen[sv] = max(gecen.get(sv, 0), t)
if gecen:
    T = min(gecen.values())
    print(f"\nsurekli tork (kucuk servo): {T:.2f} kg.cm  {gecen}")
    print("karar:", "plan aynen" if T >= 3.5 else "pitch en kotu pay yeniden hesap (yay %85)" if T >= 2.5 else "C2 iptal + yatirma +-10")
for sv, (y, a) in BOSLUK.items():
    b = abs(y - a) * 0.52
    print(f"bosluk {sv}: {b:.2f} deg", "-> B yedegi (1.5:1, yatirma +-10)" if b > 1.5 else "-> 1:1 tamam")
