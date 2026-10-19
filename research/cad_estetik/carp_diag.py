"""Tani: verilen pozda kesisen ciftler + kesisim kutusu."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv += [] 
import check as C, kin as K
from checks import geo, core
import numpy as np
p = dict(K.NOTR, **{k: float(v) for k, v in (a.split("=") for a in sys.argv[1:] if "=" in a)})
poz, aci = C.poz_bas(p)
ms = core.muaf_sozluk(C.MUAF_BAS)
M = {n: geo.to_manifold(g) for n, g in poz.items()}
gr = C.gruplar_bas()
for a, b in itertools.combinations(sorted(M), 2):
    if core.muaf_mi(a, b, ms)[0]: continue
    if geo.bb_ayrik(geo.bbox(M[a]), geo.bbox(M[b]), 0.4): continue
    I = M[a] ^ M[b]
    v = I.volume()
    if v > 0.01:
        lo, hi = geo.bbox(I); print(f"KES {a} x {b}: {v:.2f} mm3  {lo.round(1)} {hi.round(1)}")
    elif gr.get(a) != gr.get(b):
        d = M[a].min_gap(M[b], 1.0)
        if d < 0.4: print(f"DAR {a} x {b}: {d:.2f}")
print(aci)
