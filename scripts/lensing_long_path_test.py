#!/usr/bin/env python3
"""Long-path lensing test — falsifiable check of the finite-path explanation.

Lane L++ direct test of the prediction in
[`LENSING_FINITE_PATH_EXPLANATION_NOTE.md`](../docs/LENSING_FINITE_PATH_EXPLANATION_NOTE.md).

The analytical finite-path integral predicts:

    α(b, L) = s · L / (b · √((L/2)² + b²))

At T_phys = 15 (L_eff = 10), the predicted slope on b ∈ {3..6} is
−1.42, which matched the H=0.25 measurement at 1.5%.

The same formula predicts that at **T_phys = 45 (L_eff = 30)**, the
slope should drop to **−1.08** — much closer to the canonical 1/b
lensing law. This is a clean falsifiable test:

  1. Increase T_phys from 15 to 45 (NL grows proportionally)
  2. Re-run the lensing sweep on b ∈ {3..6}
  3. Compare measured slope to the analytical prediction −1.08
  4. If they match within noise, the finite-path explanation is
     confirmed and we have demonstrated the regime transition

This script is self-contained: it does NOT use the module-level
T_PHYS constant from kubo_continuum_limit, so the existing Lane L
artifact chain is undisturbed.

Cost: NL grows from 30 (H=0.5) → 90 at the long path. Each beam
propagation is 3× more expensive than Lane L. Single b at a time
to manage memory.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kubo_continuum_limit import (
    grow, finite_diff_dM, true_kubo_at_H,
    PW_PHYS, K_PER_H, S_PHYS, SRC_LAYER_FRAC,
)

# Long-path setup
T_PHYS_LONG = 45.0  # 3× the original T_phys = 15
T_PHYS_SHORT = 7.5  # 0.5× the original T_phys (test the opposite direction)
LONG_HS = [0.5]     # H=0.5 only at first; add H=0.35 if memory allows
B_VALUES = [3.0, 4.0, 5.0, 6.0]


def alpha_finite_path(b, L_eff, s=1.0):
    """Analytical finite-path-length deflection (for prediction comparison)."""
    return s * L_eff / (b * math.sqrt((L_eff / 2) ** 2 + b ** 2))


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


def measure_at(H_val, b_phys, T_phys):
    """Single measurement at (H, b) with arbitrary T_phys."""
    NL = max(3, round(T_phys / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    x_src = round(NL * SRC_LAYER_FRAC) * H_val
    z_src = b_phys

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    cz_0 = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, 0.0)
    cz_s = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, S_PHYS)
    dM = cz_s - cz_0
    kubo, _, _ = true_kubo_at_H(pos, adj, NL, PW, H_val, k_phase, x_src, z_src)
    return {
        "H": H_val, "NL": NL, "n_nodes": len(pos), "b": b_phys,
        "dM": dM, "kubo_true": kubo,
    }


def main():
    L_eff_long = (1.0 - SRC_LAYER_FRAC) * T_PHYS_LONG  # = (2/3) * T_phys

    print("=" * 80)
    print(f"LANE L++ LONG-PATH LENSING TEST")
    print("=" * 80)
    print(f"  T_phys = {T_PHYS_LONG}  (3× original Lane L T_phys=15)")
    print(f"  L_eff = (2/3)·T_phys = {L_eff_long}")
    print(f"  B values: {B_VALUES}")
    print(f"  Refinements: {LONG_HS}")
    print()
    print(f"  PREDICTION: slope on b ∈ {{3..6}} should be ≈ "
          f"{slope_loglog(B_VALUES, [alpha_finite_path(b, L_eff_long) for b in B_VALUES])[0]:.3f}")
    print(f"             (vs T_phys=15 prediction of -1.42, measured -1.43)")
    print()

    results = {}
    for H in LONG_HS:
        print(f"--- H = {H}, T_phys = {T_PHYS_LONG} (long path) ---", flush=True)
        results[H] = {}
        for b in B_VALUES:
            r = measure_at(H, b, T_PHYS_LONG)
            results[H][b] = r
            print(f"  b={b:.1f}  NL={r['NL']:3d}  n={r['n_nodes']:6d}  "
                  f"dM={r['dM']:+.6f}  kubo_true={r['kubo_true']:+.4f}",
                  flush=True)

    # Also run the SHORT path (toward 1/b² regime) — at all three refinements
    # since the lattice is SMALLER at short T_phys (NL is smaller)
    short_results = {}
    L_eff_short = (1.0 - SRC_LAYER_FRAC) * T_PHYS_SHORT
    pred_short = slope_loglog(B_VALUES, [alpha_finite_path(b, L_eff_short) for b in B_VALUES])[0]
    print()
    print("=" * 80)
    print(f"--- T_phys = {T_PHYS_SHORT} (short path), H ∈ {{0.5, 0.35, 0.25}} ---")
    print(f"  PREDICTION: slope on b ∈ {{3..6}} should be ≈ {pred_short:+.3f}")
    print(f"             (steeper than the L=10 measurement of -1.43)")
    print("=" * 80)
    for H in [0.5, 0.35, 0.25]:
        print(f"\n  H = {H}")
        short_results[H] = {}
        for b in B_VALUES:
            r = measure_at(H, b, T_PHYS_SHORT)
            short_results[H][b] = r
            print(f"    b={b:.1f}  NL={r['NL']:3d}  n={r['n_nodes']:6d}  "
                  f"dM={r['dM']:+.6f}  kubo_true={r['kubo_true']:+.4f}",
                  flush=True)

    # Slope comparison
    print()
    print("=" * 80)
    print(f"SLOPE FITS at T_phys = {T_PHYS_LONG} (L_eff = {L_eff_long}) — long path")
    print("=" * 80)

    # Analytical prediction
    a_alphas = [alpha_finite_path(b, L_eff_long) for b in B_VALUES]
    sa, ra = slope_loglog(B_VALUES, a_alphas)
    print(f"  analytical (no fit):    slope = {sa:+.4f}  R² = {ra:.4f}")

    # Measurements
    for H in LONG_HS:
        kubos = [results[H][b]["kubo_true"] for b in B_VALUES]
        dMs = [results[H][b]["dM"] for b in B_VALUES]
        s_k, r_k = slope_loglog(B_VALUES, kubos)
        s_d, r_d = slope_loglog(B_VALUES, dMs)
        print(f"  H={H} kubo_true:        slope = {s_k:+.4f}  R² = {r_k:.4f}  "
              f"|Δ from analytic| = {abs(s_k - sa):.4f}")
        print(f"  H={H} dM:               slope = {s_d:+.4f}  R² = {r_d:.4f}  "
              f"|Δ from analytic| = {abs(s_d - sa):.4f}")

    # Short-path slope fits at all three refinements
    print()
    print("=" * 80)
    print(f"SLOPE FITS at T_phys = {T_PHYS_SHORT} (L_eff = {L_eff_short}) — short path")
    print("=" * 80)
    a_alphas_s = [alpha_finite_path(b, L_eff_short) for b in B_VALUES]
    sas, ras = slope_loglog(B_VALUES, a_alphas_s)
    print(f"  analytical (no fit):    slope = {sas:+.4f}  R² = {ras:.4f}")
    for H in [0.5, 0.35, 0.25]:
        if H not in short_results:
            continue
        kubos_s = [short_results[H][b]["kubo_true"] for b in B_VALUES]
        dMs_s = [short_results[H][b]["dM"] for b in B_VALUES]
        s_ks, r_ks = slope_loglog(B_VALUES, kubos_s)
        s_ds, r_ds = slope_loglog(B_VALUES, dMs_s)
        print(f"  H={H} kubo_true:        slope = {s_ks:+.4f}  R² = {r_ks:.4f}  "
              f"|Δ from analytic| = {abs(s_ks - sas):.4f}")
        print(f"  H={H} dM:               slope = {s_ds:+.4f}  R² = {r_ds:.4f}  "
              f"|Δ from analytic| = {abs(s_ds - sas):.4f}")

    # Compare across T_phys values
    print()
    print("=" * 80)
    print("REGIME TRANSITION TEST")
    print("=" * 80)
    print()
    print("Predicted slope on b ∈ {3..6} as a function of T_phys (analytical):")
    print(f"  {'T_phys':>8s}  {'L_eff':>8s}  {'predicted slope':>17s}")
    for tp in [7.5, 15.0, 30.0, 45.0, 60.0, 90.0, 150.0]:
        leff = (2.0 / 3.0) * tp
        ys = [alpha_finite_path(b, leff) for b in B_VALUES]
        s, _ = slope_loglog(B_VALUES, ys)
        marker = " ← we measured this" if abs(tp - 15.0) < 0.1 else (
            " ← we ARE measuring this" if abs(tp - T_PHYS_LONG) < 0.1 else "")
        print(f"  {tp:8.1f}  {leff:8.1f}  {s:17.4f}{marker}")

    # Verdict
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    H = LONG_HS[0]
    kubos = [results[H][b]["kubo_true"] for b in B_VALUES]
    s_k, r_k = slope_loglog(B_VALUES, kubos)
    diff = abs(s_k - sa)
    print(f"  Predicted slope (analytical, L_eff={L_eff_long}):  {sa:+.4f}")
    print(f"  Measured slope (H={H} kubo_true):                  {s_k:+.4f}")
    print(f"  |measured - analytical|:                           {diff:.4f}")
    print()
    if diff < 0.10:
        print("  STRONG MATCH — the slope follows the analytical regime-transition")
        print("  prediction. The finite-path explanation is CONFIRMED.")
        print()
        print("  This demonstrates the program reproduces standard Fermat-principle")
        print("  gravitational deflection through a 2D 1/r field, with the slope")
        print("  exponent determined by L_eff/b (transition-regime physics).")
        print()
        print(f"  At L_eff = {L_eff_long}, slope = {s_k:+.3f} is significantly closer")
        print(f"  to the canonical 1/b lensing law (slope = −1) than the L_eff = 10")
        print(f"  measurement of −1.43.")
    elif diff < 0.20:
        print("  MODERATE MATCH — direction is right but quantitative agreement")
        print("  is not as tight as Lane L+ at L_eff=10. Possible reasons:")
        print("  - H=0.5 has known coarse-lattice bias (Lane L+ saw 0.14 deviation")
        print("    at H=0.5 vs 0.015 at H=0.25)")
        print("  - May need finer H to confirm the analytical match")
    else:
        print("  POOR MATCH — measured slope deviates significantly from prediction.")
        print("  Either the explanation needs refinement or the long-path setup")
        print("  has its own confounders.")


if __name__ == "__main__":
    main()
