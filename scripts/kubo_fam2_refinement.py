#!/usr/bin/env python3
"""Fam2 single-family refinement of kubo_true.

Lane α++ follow-on. The family-portability lane
([`KUBO_CONTINUUM_LIMIT_FAMILIES_NOTE.md`](../docs/KUBO_CONTINUUM_LIMIT_FAMILIES_NOTE.md))
showed:

- Fam1 converges to +5.986 with 0.2% drift at H=0.25 (clean)
- Fam3 converges to +5.955 with 6.4% drift at H=0.25 (Fam1/Fam3
  agree to 0.5%)
- **Fam2 is the outlier**: 6.66 → 6.32 → **7.09** at H=0.25,
  non-monotone trajectory, 12.2% last-step drift. Clearly NOT
  converged.

The question: is Fam2 converging to ~5.97 (like Fam1/Fam3) but
just needs finer H, or is it converging to a different value?

This lane runs Fam2 ONLY at an additional refinement point
H = 0.20 (between the existing H = 0.25 and the memory-feasible
limit). Single family, single new H point — cheapest possible
probe of whether Fam2 settles.

Cost: one grow() + one parallel perturbation propagator at
H=0.20. Grown-DAG at H=0.20 has ~259k nodes (up from 141k at
H=0.25). Bigger but still feasible on the current hardware.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kubo_continuum_limit import (
    grow, true_kubo_at_H, finite_diff_dM,
    T_PHYS, PW_PHYS, K_PER_H, S_PHYS, MASS_Z_PHYS, SRC_LAYER_FRAC,
)

FAM2_DRIFT = 0.05
FAM2_RESTORE = 0.30


def measure(H_val):
    NL = max(3, round(T_PHYS / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    x_src = round(NL * SRC_LAYER_FRAC) * H_val
    z_src = MASS_Z_PHYS

    pos, adj, nmap = grow(0, FAM2_DRIFT, FAM2_RESTORE, NL, PW, 3, H_val)
    kubo, cz_free, T0 = true_kubo_at_H(pos, adj, NL, PW, H_val, k_phase, x_src, z_src)
    return {
        "H": H_val, "NL": NL, "n_nodes": len(pos),
        "kubo_true": kubo, "cz_free": cz_free,
    }


def main():
    print("=" * 100)
    print("LANE α++: Fam2 single-family refinement")
    print(f"Fam2 (drift={FAM2_DRIFT}, restore={FAM2_RESTORE})")
    print(f"Physical: T={T_PHYS}, PW={PW_PHYS}, k*H={K_PER_H}, "
          f"S={S_PHYS}, z_src={MASS_Z_PHYS}")
    print("Refinement: H ∈ {0.5, 0.35, 0.25, 0.20} — one new point at 0.20")
    print("=" * 100)

    # Known values from KUBO_CONTINUUM_LIMIT_FAMILIES_NOTE.md
    known = {
        0.5: +6.6588,
        0.35: +6.3168,
        0.25: +7.0883,
    }
    print("\nKnown Fam2 values from the family-portability lane:")
    for H, v in sorted(known.items(), reverse=True):
        print(f"  H={H:.3f}  kubo_true = {v:+.4f}")

    print("\nNew refinement point:")
    r = measure(0.20)
    print(f"  H={r['H']:.3f}  NL={r['NL']}  n_nodes={r['n_nodes']}  "
          f"kubo_true = {r['kubo_true']:+.4f}")
    new_val = r["kubo_true"]

    # Full series
    all_pts = sorted(list(known.items()) + [(0.20, new_val)], reverse=True)
    print("\n" + "=" * 100)
    print("FULL FAM2 SERIES")
    print("=" * 100)
    print(f"  {'H':>6s}  {'kubo_true':>12s}")
    for H, v in all_pts:
        print(f"  {H:6.3f}  {v:+12.4f}")

    # Step-by-step drifts
    print("\nStep-by-step drifts (coarser → finer):")
    for i in range(len(all_pts) - 1):
        H1, v1 = all_pts[i]
        H2, v2 = all_pts[i + 1]
        d = v2 - v1
        rel = d / v1 if abs(v1) > 1e-12 else 0.0
        print(f"  H={H1:.3f} ({v1:+.4f}) → H={H2:.3f} ({v2:+.4f})  "
              f"Δ = {d:+.4f} ({rel:+.1%})")

    # Verdict
    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    # Compare new H=0.20 to Fam1/Fam3 converged values ~5.97
    target_F1F3 = 5.97
    dev_from_F1F3 = abs(new_val - target_F1F3)
    rel_dev = dev_from_F1F3 / target_F1F3
    print(f"  Fam2 at H=0.20: {new_val:+.4f}")
    print(f"  Fam1/Fam3 converged value (H=0.25): ~+5.97")
    print(f"  Fam2 deviation from Fam1/Fam3 target: {dev_from_F1F3:.4f} "
          f"({rel_dev:.1%})")

    # Last-step drift
    last_drift_rel = abs(new_val - known[0.25]) / abs(known[0.25])
    print(f"  Last-step drift (H=0.25 → H=0.20): {last_drift_rel:.1%}")

    print()
    if rel_dev < 0.05 and last_drift_rel < 0.05:
        print("  STRONG — Fam2 at H=0.20 agrees with Fam1/Fam3 converged value")
        print("  to within 5%, AND Fam2's last-step drift is < 5%. Fam2 was just")
        print("  slow to converge; the family-portable continuum value is ~5.97.")
    elif rel_dev < 0.05:
        print("  GOOD — Fam2 at H=0.20 agrees with Fam1/Fam3 within 5%, but")
        print("  the last-step drift is still large. Family portability is")
        print("  supported but Fam2 still has residual lattice artifacts.")
    elif last_drift_rel < 0.05:
        print("  STABILIZED BUT DIFFERENT — Fam2 has converged (last-step < 5%)")
        print("  but to a value different from Fam1/Fam3. The continuum limit is")
        print("  family-specific, not portable.")
    else:
        print("  STILL BOUNCING — Fam2 last-step drift is still > 5%. Either")
        print("  the continuum limit is at much finer H, or Fam2 has a genuine")
        print("  convergence pathology at this combination of physical parameters.")


if __name__ == "__main__":
    main()
