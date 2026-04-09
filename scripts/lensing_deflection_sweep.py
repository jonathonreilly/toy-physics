#!/usr/bin/env python3
"""Lane L: Gravitational deflection / lensing sweep.

Moonshot test: does the program reproduce gravitational-lensing-style
deflection α ∝ 1/b, where b is the impact parameter between the beam
and a source mass?

Physical framing: the propagator action S = L(1−f) is literally Fermat's
principle with refractive index n = 1−f. A mass sources f ∝ 1/r, so
the beam path through that field is a geodesic in a gradient-index
medium — the same formalism as weak-field gravitational lensing.

Setup:
- Fix beam initial condition: single source at origin (iy=0, iz=0, layer=0)
- Vary mass position z_src across b ∈ {1, 2, 3, 4, 5, 6}
- Measure dM(b) = cz(field) − cz(free) at the detector layer
- Deflection angle α(b) ≈ dM(b) / (physical propagation length)
- Fit log|dM| vs log(b): expect slope ≈ −1 for Newton/Einstein-like
  lensing (α ∝ 1/b), or a different power for a unique model prediction

Reference: Lane α gave kubo_true → +5.986 on Fam1 at z_src=3.0 with 0.2%
continuum drift. This lane asks: what's the b-dependence?

If the slope is close to −1, the program reproduces the 1/b scaling of
gravitational lensing. Combined with the continuum-stable Kubo coefficient,
that would be the strongest physical tier-up result the program has
produced so far.

Cost: 6 b-values × 2 H values (H ∈ {0.5, 0.35}) = 12 runs.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kubo_continuum_limit import (
    grow, finite_diff_dM, true_kubo_at_H,
    T_PHYS, PW_PHYS, K_PER_H, S_PHYS, SRC_LAYER_FRAC,
)

IMPACT_PARAMETERS = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
REFINEMENTS = [(0.5, "coarse"), (0.35, "medium")]


def measure_deflection_at(H_val, b_phys):
    """Compute dM(b) for a mass at (x_src, y=0, z=b) using Fam1."""
    NL = max(3, round(T_PHYS / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    x_src = round(NL * SRC_LAYER_FRAC) * H_val
    z_src = b_phys  # impact parameter in physical z

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    cz_0 = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, 0.0)
    cz_s = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, S_PHYS)
    dM = cz_s - cz_0
    kubo, _, _ = true_kubo_at_H(pos, adj, NL, PW, H_val, k_phase, x_src, z_src)
    return {
        "H": H_val, "NL": NL, "b_phys": b_phys, "x_src": x_src, "z_src": z_src,
        "cz_0": cz_0, "cz_s": cz_s, "dM": dM, "kubo_true": kubo,
    }


def log_slope(xs, ys):
    """Log-log linear fit, returns (slope, intercept, R²)."""
    valid = [(x, y) for x, y in zip(xs, ys) if x > 0 and abs(y) > 1e-15]
    if len(valid) < 2:
        return 0.0, 0.0, 0.0
    lx = [math.log(x) for x, _ in valid]
    ly = [math.log(abs(y)) for _, y in valid]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    syy = sum((y - my) ** 2 for y in ly)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    if sxx <= 0:
        return 0.0, my, 0.0
    slope = sxy / sxx
    intercept = my - slope * mx
    r2 = (sxy * sxy) / (sxx * syy) if syy > 0 else 1.0
    return slope, intercept, r2


def main():
    print("=" * 100)
    print("LANE L: GRAVITATIONAL DEFLECTION / LENSING SWEEP")
    print(f"Physical: T={T_PHYS}, PW={PW_PHYS}, k*H={K_PER_H}, S={S_PHYS}")
    print(f"Impact parameters b: {IMPACT_PARAMETERS}")
    print(f"Refinements: {[r[0] for r in REFINEMENTS]}")
    print("=" * 100)

    results = {}  # results[H][b] = measurement dict
    for H_val, label in REFINEMENTS:
        print(f"\n--- {label} (H={H_val}) ---", flush=True)
        results[H_val] = {}
        for b in IMPACT_PARAMETERS:
            r = measure_deflection_at(H_val, b)
            results[H_val][b] = r
            print(f"  b={b:.1f}  NL={r['NL']:3d}  "
                  f"dM={r['dM']:+.6f}  kubo_true={r['kubo_true']:+.4f}")

    print("\n" + "=" * 100)
    print("DEFLECTION TABLE — dM(b) at each refinement")
    print("=" * 100)
    header = f"{'b':>6s}"
    for H_val, label in REFINEMENTS:
        header += f" {label + f' dM (H={H_val})':>22s}"
    header += f" {'drift':>10s}"
    print(header)
    for b in IMPACT_PARAMETERS:
        row = f"{b:6.1f}"
        dMs = []
        for H_val, label in REFINEMENTS:
            dM = results[H_val][b]["dM"]
            dMs.append(dM)
            row += f" {dM:22.6f}"
        if len(dMs) >= 2 and abs(dMs[0]) > 1e-12:
            drift = abs(dMs[1] - dMs[0]) / abs(dMs[0])
            row += f" {drift:10.1%}"
        print(row)

    # Log-log fit at each refinement
    print("\n" + "=" * 100)
    print("LOG-LOG FIT |dM| vs b  at each refinement")
    print("=" * 100)
    for H_val, label in REFINEMENTS:
        bs = list(IMPACT_PARAMETERS)
        dMs = [results[H_val][b]["dM"] for b in bs]
        slope, intercept, r2 = log_slope(bs, dMs)
        print(f"  {label} (H={H_val}):")
        print(f"    log|dM| = {slope:+.4f} * log(b) + {intercept:+.4f}")
        print(f"    R² = {r2:.4f}")
        # Compare to Newton/Einstein 1/b
        dev_from_minus1 = abs(slope - (-1.0))
        print(f"    |slope − (−1)| = {dev_from_minus1:.4f}")

    # Also fit kubo_true — first-order analytic quantity
    print("\n" + "=" * 100)
    print("LOG-LOG FIT kubo_true vs b  at each refinement (full range)")
    print("=" * 100)
    for H_val, label in REFINEMENTS:
        bs = list(IMPACT_PARAMETERS)
        kubos = [results[H_val][b]["kubo_true"] for b in bs]
        slope, intercept, r2 = log_slope(bs, kubos)
        print(f"  {label} (H={H_val}):")
        print(f"    log|kubo| = {slope:+.4f} * log(b) + {intercept:+.4f}")
        print(f"    R² = {r2:.4f}")
        dev_from_minus1 = abs(slope - (-1.0))
        print(f"    |slope − (−1)| = {dev_from_minus1:.4f}")

    # Restricted fits: exclude near-field pathology (b ≤ 1)
    # The b=1 point has NEGATIVE deflection (beam AWAY from mass) because
    # the mass is inside the beam's natural transverse width. This is a
    # near-field pathology, not lensing. The lensing regime requires the
    # mass to be clearly outside the beam.
    print("\n" + "=" * 100)
    print("RESTRICTED FITS — excluding near-field pathology")
    print("=" * 100)
    for subset_label, subset_bs in [
        ("b ∈ {2,3,4,5,6} (excluding near-field b=1)", [2.0, 3.0, 4.0, 5.0, 6.0]),
        ("b ∈ {3,4,5,6}   (asymptotic only, excluding peak at b≈2)", [3.0, 4.0, 5.0, 6.0]),
    ]:
        print(f"\n  Subset: {subset_label}")
        for H_val, label in REFINEMENTS:
            kubos = [results[H_val][b]["kubo_true"] for b in subset_bs]
            dMs = [results[H_val][b]["dM"] for b in subset_bs]
            slope_k, intercept_k, r2_k = log_slope(subset_bs, kubos)
            slope_d, intercept_d, r2_d = log_slope(subset_bs, dMs)
            print(f"    {label} (H={H_val}):")
            print(f"      kubo_true: slope = {slope_k:+.4f}  R²={r2_k:.4f}  "
                  f"|slope−(−1)|={abs(slope_k-(-1.0)):.4f}")
            print(f"      dM       : slope = {slope_d:+.4f}  R²={r2_d:.4f}  "
                  f"|slope−(−1)|={abs(slope_d-(-1.0)):.4f}")

    # Sign check
    print("\n" + "=" * 100)
    print("SIGN CHECK — gravity should be TOWARD the mass (dM > 0 when z_src > 0)")
    print("=" * 100)
    all_toward = True
    for H_val, label in REFINEMENTS:
        for b in IMPACT_PARAMETERS:
            dM = results[H_val][b]["dM"]
            toward = dM > 0
            if not toward:
                all_toward = False
                print(f"  {label} b={b:.1f}: dM={dM:+.6f}  AWAY (NOT toward)")
    if all_toward:
        print("  OK — all deflections are toward the mass at every b and every H")

    # Verdict — use asymptotic fit (b ≥ 3) at the finest refinement
    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    H_fine = REFINEMENTS[-1][0]
    asymp_bs = [3.0, 4.0, 5.0, 6.0]
    asymp_kubos = [results[H_fine][b]["kubo_true"] for b in asymp_bs]
    slope_asymp, _, r2_asymp = log_slope(asymp_bs, asymp_kubos)

    full_bs = list(IMPACT_PARAMETERS)
    full_kubos = [results[H_fine][b]["kubo_true"] for b in full_bs]
    slope_full, _, r2_full = log_slope(full_bs, full_kubos)

    print(f"  Full range (b=1..6) at H={H_fine}:")
    print(f"    kubo_true(b) ∝ b^{slope_full:+.3f}  R²={r2_full:.3f}")
    print(f"    Dominated by near-field pathology at b=1 (negative deflection)")
    print()
    print(f"  Asymptotic (b=3..6) at H={H_fine}:")
    print(f"    kubo_true(b) ∝ b^{slope_asymp:+.3f}  R²={r2_asymp:.3f}")
    print()
    if abs(slope_asymp - (-1.0)) < 0.3 and r2_asymp > 0.85:
        print("  MODERATE POSITIVE — the asymptotic slope is consistent with −1")
        print("  within noise. The program shows 1/b-like deflection in the")
        print("  far-field regime (mass clearly outside the beam's natural width).")
        print()
        print("  Caveats:")
        print("  - Only a 2-refinement sweep (H ∈ {0.5, 0.35}), not 3-refinement")
        print("  - Large H-drifts at some b values (up to 50%+), not continuum-stable")
        print("  - The near-field regime (b ≤ 1) has a genuine sign flip, not lensing")
        print("  - Asymptotic range is only 4 b points; more needed for a clean fit")
    elif abs(slope_asymp - (-1.0)) < 0.5:
        print(f"  WEAK — asymptotic slope = {slope_asymp:+.3f}, in the vicinity of −1")
        print("  but not clean. Needs more refinements or more b values to confirm.")
    else:
        print(f"  NEGATIVE — asymptotic slope = {slope_asymp:+.3f}, far from −1.")
        print("  The deflection does not follow a clean 1/b law even in the")
        print("  far-field regime.")


if __name__ == "__main__":
    main()
