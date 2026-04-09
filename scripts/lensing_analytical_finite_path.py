#!/usr/bin/env python3
"""Analytical finite-path-length deflection — explains the Lane L+ slope.

After Lane L+ downgraded the lensing measurement to 'clean power law
with exponent ≈ −1.43, NOT 1/b', the natural question was: why isn't
it 1/b?

The answer is that the model IS doing standard Fermat-principle
deflection through the imposed 2D 1/r field, but we are in the
finite-path-length transition regime where the asymptotic 1/b law
does NOT apply.

For a beam at z=0 passing a mass at z_src=b in the +x direction
through a field f = s/(r + ε) where r = sqrt(x² + z²) (2D distance,
y ignored), the deflection angle integrated over a path of length L
centered on the mass is:

    α(b, L) = -s · L / (b · sqrt((L/2)² + b²))

Three regimes:
  L ≫ b  →  α ≈ -2s/b              (canonical 1/b lensing)
  L ≪ b  →  α ≈ -s·L/b²            (steeper 1/b² falloff)
  L ≈ b  →  intermediate, slope ≈ -1.4 or so

Our setup has L_eff = (2/3) · T_phys = 10 (the source is active for
the second 2/3 of the propagation), and b ∈ {3, 4, 5, 6}, so
L_eff/b ∈ [1.67, 3.33] — squarely in the transition regime.

This script:
  1. Computes the analytical α(b, L) for various L values
  2. Compares to the Lane L / Lane L+ measurements
  3. Demonstrates the regime transition by varying L
  4. Predicts what happens as L → ∞ (canonical 1/b should emerge)
"""

from __future__ import annotations

import math


def alpha_finite_path(b, L, s=1.0):
    """Deflection angle through a 2D 1/r field on a finite path of length L."""
    return s * L / (b * math.sqrt((L / 2) ** 2 + b ** 2))


def slope_loglog(xs, ys):
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


# Lane L / Lane L+ measurements (kubo_true on Fam1)
MEASUREMENTS = {
    0.5: {
        2.0: +4.6543,
        3.0: +7.0619,
        4.0: +5.6136,
        5.0: +3.6639,
        6.0: +3.0176,
    },
    0.35: {
        2.0: +6.9576,
        3.0: +5.9728,
        4.0: +3.3393,
        5.0: +3.0606,
        6.0: +2.3599,
    },
    0.25: {
        3.0: +5.9860,
        4.0: +3.8196,
        5.0: +2.8264,
        6.0: +2.2117,
    },
}


def main():
    L_eff = 10.0  # (2/3) * T_phys = (2/3) * 15

    print("=" * 80)
    print("ANALYTICAL FINITE-PATH DEFLECTION through 2D 1/r field")
    print("=" * 80)
    print(f"alpha(b, L) = -s · L / (b · sqrt((L/2)² + b²))")
    print(f"Setup: L_eff = (2/3) · T_phys = (2/3) · 15 = {L_eff}")
    print(f"       b ∈ {{2..6}}, so L_eff/b ∈ [1.67, 5.0]")
    print()
    print("Three regimes:")
    print("  L ≫ b  →  α ≈ -2s/b           (canonical 1/b lensing)")
    print("  L ≪ b  →  α ≈ -s·L/b²         (steeper 1/b² falloff)")
    print("  L ≈ b  →  slope ≈ -1.4 (this is where we are)")
    print()

    # Analytical curve at L_eff = 10
    bs = [2.0, 3.0, 4.0, 5.0, 6.0]
    alphas = [alpha_finite_path(b, L_eff) for b in bs]

    print("=" * 80)
    print(f"ANALYTICAL CURVE at L = {L_eff}")
    print("=" * 80)
    print(f"{'b':>4s}  {'alpha(b)':>12s}  {'normalized to b=3':>20s}")
    a3 = alpha_finite_path(3.0, L_eff)
    for b in bs:
        a = alpha_finite_path(b, L_eff)
        print(f"{b:4.1f}  {a:12.6f}  {a/a3:20.4f}")

    # Slopes
    print()
    print("Analytical slopes (no fit, exact):")
    for label, subset in [
        ("b ∈ {2,3,4,5,6}", [2.0, 3.0, 4.0, 5.0, 6.0]),
        ("b ∈ {3,4,5,6}",   [3.0, 4.0, 5.0, 6.0]),
    ]:
        ys = [alpha_finite_path(b, L_eff) for b in subset]
        s, r2 = slope_loglog(subset, ys)
        print(f"  {label}: slope = {s:+.4f}  R² = {r2:.4f}")

    # Compare to measurements
    print()
    print("=" * 80)
    print("COMPARISON: analytical vs measured (normalized to b=3)")
    print("=" * 80)
    print(f"{'b':>4s}  {'analytic':>12s}  {'H=0.5':>12s}  {'H=0.35':>12s}  {'H=0.25':>12s}")
    a3 = alpha_finite_path(3.0, L_eff)
    for b in bs:
        a = alpha_finite_path(b, L_eff) / a3
        row = f"{b:4.1f}  {a:12.4f}"
        for H in [0.5, 0.35, 0.25]:
            v = MEASUREMENTS[H].get(b)
            if v is None:
                row += f"  {'—':>12s}"
            else:
                v3 = MEASUREMENTS[H].get(3.0, 1.0)
                row += f"  {v/v3:12.4f}"
        print(row)

    print()
    print("Slopes side-by-side on b ∈ {3,4,5,6}:")
    sub_bs = [3.0, 4.0, 5.0, 6.0]
    ana = [alpha_finite_path(b, L_eff) for b in sub_bs]
    sa, ra = slope_loglog(sub_bs, ana)
    print(f"  analytical (L=10):    slope = {sa:+.4f}  R² = {ra:.4f}")
    for H in [0.5, 0.35, 0.25]:
        ys = [MEASUREMENTS[H][b] for b in sub_bs]
        s, r2 = slope_loglog(sub_bs, ys)
        diff = abs(s - sa)
        print(f"  measured H={H}:        slope = {s:+.4f}  R² = {r2:.4f}  |Δ from analytic| = {diff:.4f}")

    # Regime test: vary L_eff and see slope change
    print()
    print("=" * 80)
    print("REGIME TEST: predicted slope on b ∈ {3..6} as L varies")
    print("=" * 80)
    print(f"{'L':>6s}  {'L/b̄':>6s}  {'slope':>10s}  {'regime':>30s}")
    bs_sub = [3.0, 4.0, 5.0, 6.0]
    b_mean = sum(bs_sub) / len(bs_sub)
    for L in [2.0, 5.0, 10.0, 15.0, 20.0, 30.0, 50.0, 100.0, 1000.0]:
        ys = [alpha_finite_path(b, L) for b in bs_sub]
        s, _ = slope_loglog(bs_sub, ys)
        ratio = L / b_mean
        if abs(s + 1.0) < 0.05:
            regime = "→ canonical 1/b"
        elif abs(s + 2.0) < 0.05:
            regime = "→ short-path 1/b²"
        elif s < -1.5:
            regime = "transition (closer to 1/b²)"
        else:
            regime = "transition (closer to 1/b)"
        print(f"{L:6.1f}  {ratio:6.2f}  {s:+10.4f}  {regime:>30s}")

    # Predictions for next test
    print()
    print("=" * 80)
    print("FALSIFIABLE PREDICTIONS")
    print("=" * 80)
    print()
    print("PREDICTION 1: at L_eff = 60 (T_phys = 90, NL=180 at H=0.5),")
    print(f"              the slope on b ∈ {{3..6}} should be ≈ "
          f"{slope_loglog([3,4,5,6], [alpha_finite_path(b, 60) for b in [3,4,5,6]])[0]:+.3f}")
    print(f"              (significantly closer to −1)")
    print()
    print("PREDICTION 2: at L_eff = 30 (T_phys = 45, NL=90 at H=0.5),")
    print(f"              the slope on b ∈ {{3..6}} should be ≈ "
          f"{slope_loglog([3,4,5,6], [alpha_finite_path(b, 30) for b in [3,4,5,6]])[0]:+.3f}")
    print()
    print("PREDICTION 3: at L_eff = 10 (current setup) but with b ∈ {1, 2, 3},")
    print(f"              the slope should be ≈ "
          f"{slope_loglog([1,2,3], [alpha_finite_path(b, 10) for b in [1,2,3]])[0]:+.3f}")
    print(f"              (closer to −1, but the b=1 point hits beam-near-field pathology)")
    print()
    print("PREDICTION 4: at L_eff = 10 (current setup) but with b ∈ {10, 15, 20},")
    print(f"              the slope should be ≈ "
          f"{slope_loglog([10,15,20], [alpha_finite_path(b, 10) for b in [10,15,20]])[0]:+.3f}")
    print(f"              (closer to −2, but blocked by PW limiting b)")
    print()
    print("Each of these is a falsifiable test of the analytical explanation.")
    print("If the program's measured slope matches the L-dependent prediction,")
    print("the 'transition regime' explanation is confirmed.")


if __name__ == "__main__":
    main()
