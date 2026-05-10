#!/usr/bin/env python3
"""Weak-field recovery sweep for the minimal source-driven field architecture."""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


TARGET_MAXES = [0.001, 0.002, 0.005, 0.010, 0.020, 0.040, 0.080]


def main() -> None:
    lat = m.Lattice3D.build(m.NL_PHYS, m.PW, m.H)
    zero = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 84)
    print("SOURCE-DRIVEN FIELD RECOVERY SWEEP")
    print("  weak-field calibration sweep on the exact 3D lattice")
    print("=" * 84)
    print(f"telegraph parameters: c={m.C_FIELD:.2f}, damp={m.DAMP:.2f}")
    print(f"source strengths: {m.SOURCE_STRENGTHS}")
    print()

    print(f"{'target max':>10s} {'toward':>8s} {'F~M':>8s} {'largest delta':>14s}")
    print("-" * 48)

    rows = []  # (tmax, toward, alpha)
    for tmax in TARGET_MAXES:
        ref_raw = m._source_driven_field_layers_raw(lat, max(m.SOURCE_STRENGTHS), m.SOURCE_Z)
        ref_max = m._field_abs_max(ref_raw)
        gain = tmax / ref_max if ref_max > 1e-30 else 1.0

        vals = []
        for s in m.SOURCE_STRENGTHS:
            dyn = m._scale_field_layers(m._source_driven_field_layers_raw(lat, s, m.SOURCE_Z), gain)
            amps = lat.propagate(dyn, m.K)
            vals.append(m._centroid_z(amps, lat) - z_free)

        alpha = m._fit_power(list(m.SOURCE_STRENGTHS), vals)
        toward = sum(v > 0 for v in vals)
        largest = max(vals) if vals else float("nan")
        alpha_str = f"{alpha:.3f}" if alpha is not None else "nan"
        print(f"{tmax:10.3f} {toward:>5d}/4 {alpha_str:>8s} {largest:+14.6e}")
        rows.append((tmax, toward, alpha))

    print()
    print("SAFE READ")
    print("  the minimal source-driven field has a real weak-field recovery pocket")
    print("  when the calibrated dynamic field stays small")
    print("  as the field calibration grows, the mass exponent drifts away from 1")
    print("  so the architecture is not dead, but it is calibration-sensitive")

    # Hard-bar assertions on the load-bearing observables.
    # Per docs/SOURCE_DRIVEN_FIELD_RECOVERY_SWEEP_NOTE.md "Hard-bar runner assertions" table.
    print()
    print("HARD-BAR ASSERTIONS")
    n_pass = 0
    n_fail = 0
    expected_per_row = len(m.SOURCE_STRENGTHS)

    # Bar 1: TOWARD sign on every target-max row.
    n_full_toward = sum(1 for _, t, _ in rows if t == expected_per_row)
    if n_full_toward == len(rows):
        print(f"  PASS: TOWARD sign full on every row ({n_full_toward}/{len(rows)})")
        n_pass += 1
    else:
        print(f"  FAIL: TOWARD sign full only on {n_full_toward}/{len(rows)} rows")
        n_fail += 1

    # Bar 2: weak-field linear recovery at small targets.
    weak_alphas = [a for tmax, _, a in rows if tmax <= 0.005 and a is not None]
    if weak_alphas and all(a >= 0.95 for a in weak_alphas):
        print(f"  PASS: weak-field F~M >= 0.95 at target<=0.005 (alphas={[round(a,3) for a in weak_alphas]})")
        n_pass += 1
    else:
        print(f"  FAIL: weak-field F~M >= 0.95 at target<=0.005 not satisfied (alphas={weak_alphas})")
        n_fail += 1

    # Bar 3: strong-calibration drift at target = 0.080.
    strong = [a for tmax, _, a in rows if abs(tmax - 0.080) < 1e-9]
    if strong and strong[0] is not None and strong[0] < 0.80:
        print(f"  PASS: strong-calibration drift F~M={strong[0]:.3f} < 0.80 at target=0.080")
        n_pass += 1
    else:
        sa = strong[0] if strong else None
        print(f"  FAIL: strong-calibration drift F~M={sa} not < 0.80 at target=0.080")
        n_fail += 1

    # Bar 4: monotonic drift of F~M with target (non-increasing).
    alphas_in_target_order = [a for _, _, a in rows if a is not None]
    monotone = all(alphas_in_target_order[i] >= alphas_in_target_order[i + 1] - 1e-9
                   for i in range(len(alphas_in_target_order) - 1))
    if monotone and len(alphas_in_target_order) == len(rows):
        print(f"  PASS: F~M is non-increasing with target ({len(alphas_in_target_order)} rows)")
        n_pass += 1
    else:
        print(f"  FAIL: F~M not non-increasing with target (alphas={alphas_in_target_order})")
        n_fail += 1

    # Bar 5: per-row F~M sanity (all in (0, 1.05)).
    if all(a is not None and 0.0 < a < 1.05 for _, _, a in rows):
        print(f"  PASS: every row F~M in (0, 1.05)")
        n_pass += 1
    else:
        bad = [(t, a) for t, _, a in rows if not (a is not None and 0.0 < a < 1.05)]
        print(f"  FAIL: per-row F~M sanity (offenders={bad})")
        n_fail += 1

    print(f"  === TOTAL: PASS={n_pass}, FAIL={n_fail} ===")
    if n_fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
