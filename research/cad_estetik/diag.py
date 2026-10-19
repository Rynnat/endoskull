"""Tani: parcadaki ayri govdeler (hacim, kutu)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
from checks import geo
for ad in sys.argv[1].split(","):
    M = build.yukle(ad)
    bs = sorted(M.decompose(), key=lambda m: -m.volume())
    print(ad, len(bs))
    for b in bs[:12]:
        lo, hi = geo.bbox(b)
        print(f"   {b.volume():9.1f}  {lo.round(1)} {hi.round(1)}")
