#!/usr/bin/env python3
"""Analytical checks for the Lane L / L+ lensing slope.

Lane L+ measured a clean asymptotic power law on b ∈ {3,4,5,6}:
  kubo_true(b) ∝ b^-1.4335  with R² = 0.9984 at H=0.25.

An earlier explanation treated this as the finite-path integral for a
beam segment of length L=10 centered on the mass:

    α_centered(b, L) = L / (b * sqrt((L/2)^2 + b^2))

That surrogate reproduces the measured slope very well, but it is not
the literal harness geometry. In the actual sweep:

  - the mass is static at x_src ≈ T_phys / 3 ≈ 5
  - the beam propagates over the full interval x ∈ [0, (NL-1)H]
  - the imposed field uses the regularized denominator r + 0.1
  - the observable is detector centroid shift, not outgoing angle

This script compares several increasingly literal 1D reductions:
  1. centered-L=10 surrogate (the earlier explanation)
  2. actual full-path static-mass integral, no regularizer
  3. actual full-path static-mass integral, with +0.1 regularizer
  4. full-path + remaining-distance weighting as a crude detector-shift proxy

The question is not just "does some finite-path model fit?" but
"does the literal harness geometry reduce to that model?".
"""

from __future__ import annotations

import math


def alpha_centered_surrogate(b, L, s=1.0):
    """Centered finite-length surrogate used in the earlier explanation."""
    return s * L / (b * math.sqrt((L / 2) ** 2 + b ** 2))


def alpha_full_path_unreg(b, x_det, x_src, s=1.0):
    """Literal full-path angle integral for a static mass, no regularizer."""
    term_hi = (x_det - x_src) / math.sqrt((x_det - x_src) ** 2 + b ** 2)
    term_lo = x_src / math.sqrt(x_src ** 2 + b ** 2)
    return s * (term_hi + term_lo) / b


def alpha_full_path_reg(b, x_det, x_src, eps=0.1, n=200000):
    """Numerical full-path angle integral with the implemented r+eps denominator."""
    dx = x_det / n
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) * dx
        r = math.sqrt((x - x_src) ** 2 + b ** 2)
        acc += b / (((r + eps) ** 2) * r)
    return acc * dx


def shift_weighted_reg(b, x_det, x_src, eps=0.1, n=200000):
    """Crude detector-shift proxy: same full-path kernel with remaining-distance weight."""
    dx = x_det / n
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) * dx
        r = math.sqrt((x - x_src) ** 2 + b ** 2)
        acc += (x_det - x) * b / (((r + eps) ** 2) * r)
    return acc * dx


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
    L_sur = 10.0
    x_src = 5.0
    x_det = 14.75  # detector layer at x=(NL-1)H for H=0.25, NL=60

    print("=" * 80)
    print("LENSING ANALYTICAL CHECKS")
    print("=" * 80)
    print("Measured fine-lane target: kubo_true(b) on b ∈ {3,4,5,6} at H=0.25")
    print(f"Static harness geometry: x ∈ [0, {x_det}], x_src = {x_src}, regularizer = 0.1")
    print(f"Earlier surrogate: centered finite-path model with L = {L_sur}")
    print()
    print("Reference formulas:")
    print("  centered surrogate:   α(b,L) = L / (b * sqrt((L/2)^2 + b^2))")
    print("  full-path geometry:   α(b) ∝ ∫ grad_z[1/(r+0.1)] dx over the full beam path")
    print("  shift proxy:          same full-path kernel with remaining-distance weight")

    # Compare to measurements
    print()
    print("=" * 80)
    print("MODEL COMPARISON on b ∈ {3,4,5,6}")
    print("=" * 80)
    bs = [3.0, 4.0, 5.0, 6.0]
    models = {
        "measured H=0.25": {b: MEASUREMENTS[0.25][b] for b in bs},
        "centered L=10 surrogate": {b: alpha_centered_surrogate(b, L_sur) for b in bs},
        "actual full path (no reg)": {b: alpha_full_path_unreg(b, x_det, x_src) for b in bs},
        "actual full path (+0.1)": {b: alpha_full_path_reg(b, x_det, x_src) for b in bs},
        "shift-weighted full path": {b: shift_weighted_reg(b, x_det, x_src) for b in bs},
    }

    print(f"{'model':<28s} {'slope':>10s} {'R²':>8s} {'|Δ slope|':>10s}")
    s_meas, r_meas = slope_loglog(bs, [models['measured H=0.25'][b] for b in bs])
    for label, vals in models.items():
        s, r2 = slope_loglog(bs, [vals[b] for b in bs])
        ds = abs(s - s_meas)
        delta = "—" if label == "measured H=0.25" else f"{ds:.4f}"
        print(f"{label:<28s} {s:+10.4f} {r2:8.4f} {delta:>10s}")

    print()
    print("Normalized shapes relative to b=3:")
    print(f"{'b':>4s} {'measured':>10s} {'centered':>10s} {'full+reg':>10s} {'shift+reg':>10s}")
    m3 = models["measured H=0.25"][3.0]
    c3 = models["centered L=10 surrogate"][3.0]
    f3 = models["actual full path (+0.1)"][3.0]
    w3 = models["shift-weighted full path"][3.0]
    for b in bs:
        print(f"{b:4.1f} {models['measured H=0.25'][b]/m3:10.4f}"
              f" {models['centered L=10 surrogate'][b]/c3:10.4f}"
              f" {models['actual full path (+0.1)'][b]/f3:10.4f}"
              f" {models['shift-weighted full path'][b]/w3:10.4f}")

    print()
    print("=" * 80)
    print("READ")
    print("=" * 80)
    print("The centered L=10 surrogate reproduces the fine H=0.25 slope very well,")
    print("but it is not the literal sweep geometry. The actual static-mass full-path")
    print("reductions are meaningfully shallower (roughly -1.24 to -1.34).")
    print()
    print("So the finite-path idea is still useful, but the current 'exact analytical")
    print("explanation' is too strong. The missing ingredient is likely the actual")
    print("beam/path weighting of the detector-centroid observable, not just a plain")
    print("angle integral over a centered interaction segment.")


if __name__ == "__main__":
    main()
