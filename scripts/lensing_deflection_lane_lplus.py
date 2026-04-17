#!/usr/bin/env python3
"""Lane L+ analysis: combine H=0.5/0.35 from the original sweep with
H=0.25 fine asymptotic data from per-process runs.

The original Lane L sweep at 6 b-values × 2 H values gave a clean
moderate-positive slope ≈ −1.03 (R²=0.94) on b ∈ {2..6} at H=0.35.

Lane L+ added H=0.25 at the asymptotic subset b ∈ {3, 4, 5, 6}, run
one process per b to avoid OOM. This script combines all data and
refits the slopes at every refinement to test continuum stability.

The headline finding: refinement STEEPENS the slope from −1.03 (H=0.35,
b ∈ {2..6}) to roughly −1.43 to −1.52 (H=0.25, b ∈ {3..6}). The R²
improves from 0.94 to 0.998 — the fine data is a much cleaner power
law, just with a different exponent than Newton/Einstein 1/b lensing.
"""

from __future__ import annotations

import math


# All measured points (from the merged log + the per-b fine runs).
# Each entry: H -> b -> {dM, kubo}
DATA = {
    0.5: {
        1.0: {"dM": -0.014349, "kubo": -0.7476},
        2.0: {"dM": +0.019068, "kubo": +4.6543},
        3.0: {"dM": +0.034642, "kubo": +7.0619},
        4.0: {"dM": +0.026148, "kubo": +5.6136},
        5.0: {"dM": +0.013483, "kubo": +3.6639},
        6.0: {"dM": +0.012404, "kubo": +3.0176},
    },
    0.35: {
        1.0: {"dM": -0.013448, "kubo": -2.2912},
        2.0: {"dM": +0.028442, "kubo": +6.9576},
        3.0: {"dM": +0.024169, "kubo": +5.9728},
        4.0: {"dM": +0.012387, "kubo": +3.3393},
        5.0: {"dM": +0.012620, "kubo": +3.0606},
        6.0: {"dM": +0.009623, "kubo": +2.3599},
    },
    0.25: {
        # b=1.0 from the partial run before OOM:
        1.0: {"dM": -0.001112, "kubo": +0.7761},
        # b=3,4,5,6 from per-process fine runs:
        3.0: {"dM": +0.025555, "kubo": +5.986043},
        4.0: {"dM": +0.015455, "kubo": +3.819639},
        5.0: {"dM": +0.011405, "kubo": +2.826383},
        6.0: {"dM": +0.008900, "kubo": +2.211718},
    },
}


def slope(xs, ys):
    n = len(xs)
    lx = [math.log(x) for x in xs]
    ly = [math.log(abs(y)) for y in ys]
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    syy = sum((y - my) ** 2 for y in ly)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    s = sxy / sxx
    r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 1.0
    return s, r2


def main():
    print("=" * 100)
    print("LANE L+ — combined analysis with H=0.25 fine refinement")
    print("=" * 100)

    # Per-b drift
    print("\nPER-b DRIFT across refinements (kubo_true)")
    print(f"{'b':>4s}  {'H=0.5':>12s}  {'H=0.35':>12s}  {'H=0.25':>12s}  "
          f"{'Δ(0.5→0.35)':>12s}  {'Δ(0.35→0.25)':>14s}")
    for b in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]:
        row = f"{b:4.1f}"
        v05 = DATA[0.5].get(b, {}).get("kubo")
        v035 = DATA[0.35].get(b, {}).get("kubo")
        v025 = DATA[0.25].get(b, {}).get("kubo")
        for v in (v05, v035, v025):
            row += f"  {v:+12.4f}" if v is not None else f"  {'—':>12s}"
        if v05 and v035:
            d1 = abs(v035 - v05) / abs(v05)
            row += f"  {d1:12.1%}"
        else:
            row += f"  {'—':>12s}"
        if v035 and v025:
            d2 = abs(v025 - v035) / abs(v035)
            row += f"  {d2:14.1%}"
        else:
            row += f"  {'—':>14s}"
        print(row)

    # Slope fits at every refinement, two subsets
    print("\nSLOPE FITS — log|kubo_true| vs log(b)")
    print("=" * 100)
    for subset_label, subset_bs in [
        ("b ∈ {2,3,4,5,6}", [2.0, 3.0, 4.0, 5.0, 6.0]),
        ("b ∈ {3,4,5,6}",   [3.0, 4.0, 5.0, 6.0]),
    ]:
        print(f"\n  Subset: {subset_label}")
        print(f"    {'H':>6s}  {'slope':>10s}  {'R²':>8s}  {'|s−(−1)|':>10s}")
        for H in [0.5, 0.35, 0.25]:
            kubos = []
            ok = True
            for b in subset_bs:
                k = DATA[H].get(b, {}).get("kubo")
                if k is None:
                    ok = False
                    break
                kubos.append(k)
            if not ok:
                print(f"    {H:6.3f}   missing data")
                continue
            s, r2 = slope(subset_bs, kubos)
            print(f"    {H:6.3f}  {s:+10.4f}  {r2:8.4f}  {abs(s + 1.0):10.4f}")

    # Same for dM
    print("\nSLOPE FITS — log|dM| vs log(b)")
    print("=" * 100)
    for subset_label, subset_bs in [
        ("b ∈ {2,3,4,5,6}", [2.0, 3.0, 4.0, 5.0, 6.0]),
        ("b ∈ {3,4,5,6}",   [3.0, 4.0, 5.0, 6.0]),
    ]:
        print(f"\n  Subset: {subset_label}")
        print(f"    {'H':>6s}  {'slope':>10s}  {'R²':>8s}  {'|s−(−1)|':>10s}")
        for H in [0.5, 0.35, 0.25]:
            dMs = []
            ok = True
            for b in subset_bs:
                d = DATA[H].get(b, {}).get("dM")
                if d is None:
                    ok = False
                    break
                dMs.append(d)
            if not ok:
                print(f"    {H:6.3f}   missing data")
                continue
            s, r2 = slope(subset_bs, dMs)
            print(f"    {H:6.3f}  {s:+10.4f}  {r2:8.4f}  {abs(s + 1.0):10.4f}")

    # Verdict
    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    s_med_kubo, r_med_kubo = slope([2.0, 3.0, 4.0, 5.0, 6.0],
        [DATA[0.35][b]["kubo"] for b in [2.0, 3.0, 4.0, 5.0, 6.0]])
    s_fin_kubo, r_fin_kubo = slope([3.0, 4.0, 5.0, 6.0],
        [DATA[0.25][b]["kubo"] for b in [3.0, 4.0, 5.0, 6.0]])
    print(f"  Lane L (medium, b ∈ {{2..6}}, kubo): slope = {s_med_kubo:+.4f}, "
          f"R² = {r_med_kubo:.4f}")
    print(f"  Lane L+ (fine, b ∈ {{3..6}}, kubo): slope = {s_fin_kubo:+.4f}, "
          f"R² = {r_fin_kubo:.4f}")
    print()
    print("  R² IMPROVES dramatically with refinement (0.94 → 0.998)")
    print("  The fine data is a much cleaner power law than the medium data.")
    print()
    print(f"  But the SLOPE STEEPENS from {s_med_kubo:+.3f} to {s_fin_kubo:+.3f}.")
    print(f"  Refinement is NOT stabilizing the slope at −1; it is moving it toward")
    print(f"  a steeper exponent (~−1.43 to −1.52).")
    print()
    print("  This DOWNGRADES the Lane L 'matches 1/b lensing' claim.")
    print("  The asymptotic power law on b ∈ {3..6} at H=0.25 is closer to")
    print("  −1.43, NOT −1. This is either:")
    print("    (a) a unique prediction of the lattice model (steeper than 1/b)")
    print("    (b) a transition regime that asymptotes to 1/b at b ≫ 6")
    print("        (untestable here: PW=6 limits the b range)")
    print("    (c) a boundary effect — b=6 is at the lattice edge")
    print()
    print("  The R²=0.998 at H=0.25 says it IS a clean power law.")
    print("  Just not the −1 power expected from Newton/Einstein lensing.")


if __name__ == "__main__":
    main()
