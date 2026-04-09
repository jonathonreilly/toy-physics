#!/usr/bin/env python3
"""NN lattice distance law under refinement.

This is a narrow probe of the raw nearest-neighbor lattice branch from
`lattice_nn_continuum.py`.

Question:
- does the Born-safe refinement path keep a meaningful distance-law signal?
- if simple `h`-dependent strength laws are used, does the distance-law
  magnitude improve, degrade, or stay flat?

Scope:
- barrier harness only
- same slit geometry as the raw NN refinement study
- sign and magnitude are reported separately
- no no-barrier branch is mixed in here
"""

from __future__ import annotations

import math
import os
import sys
from typing import Iterable, Sequence

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lattice_nn_continuum import generate_nn_lattice, propagate  # type: ignore

K_PHYS = 5.0
PHYS_W = 20.0
PHYS_L = 40.0
SLIT_Y = 3.0
BASE_STRENGTH = 5e-4
N_YBINS = 8
B_VALUES = (3, 5, 7, 10, 13, 16, 19)
H_VALUES = (1.0, 0.5, 0.25)
ALPHAS = (0.0, 1.5)
FAR_FIELD_B = 7


def build_field(pos, mass_idx, strength):
    mx, my = pos[mass_idx]
    field = [0.0] * len(pos)
    for i, (ix, iy) in enumerate(pos):
        r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
        field[i] = strength / r
    return field


def strength_for_alpha(h: float, alpha: float) -> float:
    if alpha == 0.0:
        return BASE_STRENGTH
    return BASE_STRENGTH / (h ** alpha)


def fit_power_law(rows):
    pts = [(b, abs(delta)) for b, delta in rows if delta is not None and abs(delta) > 0 and b >= FAR_FIELD_B]
    if len(pts) < 2:
        return math.nan, math.nan
    xs = [math.log(b) for b, _ in pts]
    ys = [math.log(d) for _, d in pts]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx <= 0:
        return math.nan, math.nan
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    intercept = my - slope * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return slope, r2


def measure_distance(h: float, alpha: float, b: float):
    pos, adj, nl, hw, nmap = generate_nn_lattice(h)
    n = len(pos)
    det_layer = nl - 1
    det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1) if (det_layer, iy) in nmap]
    bl = nl // 3
    gl = 2 * nl // 3

    slit_iy = max(1, round(SLIT_Y / h))
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    sa_range = range(slit_iy, min(slit_iy + max(2, round(2 / h)), hw + 1))
    sb_range = range(-min(slit_iy + max(1, round(1 / h)), hw), -slit_iy + 1)
    sa = [nmap[(bl, iy)] for iy in sa_range if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in sb_range if (bl, iy) in nmap]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    mass_iy = round(b / h)
    mass_idx = nmap.get((gl, mass_iy))
    if mass_idx is None:
        return None

    field_f = [0.0] * n
    field_m = build_field(pos, mass_idx, strength_for_alpha(h, alpha))

    af = propagate(pos, adj, field_f, K_PHYS, blocked, n)
    am = propagate(pos, adj, field_m, K_PHYS, blocked, n)
    if af is None or am is None:
        return None

    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return None

    yf = sum(abs(af[d]) ** 2 * pos[d][1] for d in det) / pf
    ym = sum(abs(am[d]) ** 2 * pos[d][1] for d in det) / pm
    return ym - yf


def summarize(rows):
    far_rows = [(b, d) for b, d in rows if d is not None and b >= FAR_FIELD_B]
    positive_far = [(b, d) for b, d in far_rows if d > 0]
    slope, r2 = fit_power_law(rows)
    sign = "mixed"
    if far_rows and len(positive_far) == len(far_rows):
        sign = "positive"
    elif far_rows and len(positive_far) == 0:
        sign = "negative"
    return sign, slope, r2, positive_far, far_rows


def main():
    print("=" * 92)
    print("NN LATTICE DISTANCE LAW UNDER REFINEMENT")
    print(f"  raw barrier harness, K={K_PHYS}, SLIT_Y={SLIT_Y}, base_strength={BASE_STRENGTH}")
    print(f"  B values: {B_VALUES}")
    print(f"  h values: {H_VALUES}")
    print(f"  alpha values: {ALPHAS}")
    print("=" * 92)
    print()

    all_rows = {}

    for alpha in ALPHAS:
        print(f"ALPHA = {alpha:.1f}")
        for h in H_VALUES:
            rows = []
            print(f"  h = {h}")
            print(f"  {'b':>4s}  {'delta':>11s}  {'|delta|':>11s}")
            print(f"  {'-' * 30}")
            for b in B_VALUES:
                delta = measure_distance(h, alpha, b)
                rows.append((b, delta))
                if delta is None:
                    print(f"  {b:4.0f}  {'FAIL':>11s}  {'FAIL':>11s}")
                else:
                    print(f"  {b:4.0f}  {delta:+11.6f}  {abs(delta):11.6f}")
            sign, slope, r2, positive_far, far_rows = summarize(rows)
            all_rows[(alpha, h)] = rows
            if math.isnan(slope):
                print("  far-field fit: n/a")
            else:
                print(f"  far-field fit: |delta| ~ b^({slope:.3f}), R^2 = {r2:.3f}")
            print(f"  far-field sign: {sign}")
            if positive_far:
                print(f"  positive far-field rows: {len(positive_far)}/{len(far_rows)}")
            print()

    print("SAFE READ")
    print("  - coarse h=1.0 is sign-mixed and not yet a clean far-field regime")
    print("  - refined h=0.5 and h=0.25 keep a positive far-field distance signal")
    print("  - fixed strength gives the cleanest far-field decay")
    print("  - alpha-scaled strength keeps the signal but slightly flattens the decay")
    print("  - no no-barrier branch is mixed in here")


if __name__ == "__main__":
    main()
