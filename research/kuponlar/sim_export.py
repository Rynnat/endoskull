"""Kupon montajlarini etkilesimli 3B sime aktarir -> out/kupon_sim.html (tek dosya, three.js).

Her kupon icin montaj.py pozlari N karede ornek alinir; parca geometrisi bir kez gomulur, karelerde yalniz 4x4 degisir.
  PYTHONUTF8=1 python -B sim_export.py
"""
import base64
import json
import os

import numpy as np

import montaj as M
import render as R
from params import OUT

N = 25


def sahneler():
    lin = lambda a, b: [a + (b - a) * i / (N - 1) for i in range(N)]
    dur = -4.0
    return [
        ("K1", "MG996R tork + boşluk", "kol açısı", lin(dur, 40), lambda p: M.k1(p), "°",
         "Kol yatayken ağırlığı 20/40/60/80/100 mm deliklere as, 60 s tut: ≤2° sarkma = sürekli tork. Alttaki çıkıntı kasıtlı durdurucu."),
        ("K2mg", "MG996R kol cebi (K1 tutucuda)", "kol açısı", lin(dur, 15), lambda p: M.k1(p, "K2_mg_p0.2"), "°",
         "0.1 / 0.2 / 0.3 mm cep payı; kit kolu cebe gömülür, 50 mm uçta boşluk ölçülür. Görünen: 0.2."),
        ("K4", "SG90 kapak hızı (1.5× bağlantı)", "servo açısı", lin(-25, 25), lambda t: M.k4(t), "°",
         "Servo 50° dönünce disk ~79° döner. Telefon 240 fps ile açı çizgilerinden kapanma süresi okunur (hedef ≤100 ms)."),
        ("K3", "Rotil / pushrod boşluğu", "eğim", lin(0, 45), lambda e: M.k3(egim=e) if e > 0.5 else M.k3(), "°",
         "0°: rod iki rotil arasında, kızak ±0.5 kg it-çek → toplam boşluk. Eğim: rotilin açı sınırı."),
        ("K5k", "Piston ucu: vida-pimli kardan", "salınım", lin(0, 360), lambda u: M.k5_kardan(25 * np.sin(np.radians(u)), 25 * np.cos(np.radians(u))), "°",
         "İki dik M3 pim; tüp kendi ekseninde de döner → bilye-yuvasız 3 serbestlik. ±25° her yön."),
        ("K5t", "Teleskop piston (PLA, 0.4 mm)", "çekme", lin(0.5, 65), lambda c: M.k5_cift(0.4, c), " mm",
         "0.4 / 0.5 / 0.6 mm radyal boşluk çiftleri; tartıyla itme kuvveti ölçülür, takılırsa Al iç boru."),
        ("K2pim", "M3 dönen eklem (3.3 / 3.4 delik)", "açı", lin(0, 360), lambda a: M.k2_pim(a), "°",
         "Vida pim olur; hangi delik çapının boşluksuz ama serbest döndüğü seçilir."),
    ]


def main():
    geos, gid = [], {}
    out = []
    for key, ad, slider, vals, f, unit, aciklama in sahneler():
        frames, names = [], []
        for v in vals:
            parts = f(v)
            fr = {}
            for nm, (g, Mx) in parts.items():
                v3, fc, _ = R.sahne({nm: g}, lambda _: (0, 0, 0))[0]
                gk = (nm, tuple(np.round(v3.min(0), 2)), tuple(np.round(v3.max(0), 2)))
                if gk not in gid:
                    gid[gk] = len(geos)
                    geos.append(dict(n=nm, c=list(R.renk(nm)),
                                     v=base64.b64encode(np.asarray(v3, np.float32).tobytes()).decode(),
                                     f=base64.b64encode(np.asarray(fc, np.uint32).tobytes()).decode()))
                if gk not in names:
                    names.append(gk)
                fr[gk] = np.round(np.asarray(Mx, float).T.reshape(-1), 4).tolist()   # three: sutun-oncelikli
            frames.append(fr)
        out.append(dict(k=key, ad=ad, s=slider, u=unit, a=aciklama, vals=[round(x, 2) for x in vals],
                        parts=[gid[n] for n in names], frames=[[fr.get(n) for n in names] for fr in frames]))
        print(key, len(names), "parca")
    data = json.dumps(dict(geos=geos, scenes=out), separators=(",", ":"))
    tpl = open(os.path.join(os.path.dirname(__file__), "sim_template.html"), encoding="utf-8").read()
    p = os.path.join(OUT, "kupon_sim.html")
    open(p, "w", encoding="utf-8").write(tpl.replace("/*DATA*/null", data))
    print(p, round(os.path.getsize(p) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
