#!/usr/bin/env python3
"""Continuum limit of kubo_true across Fam1, Fam2, Fam3.

Lane α+ extension: the single-family continuum-limit test showed
kubo_true converges to +5.986 on Fam1 with 0.2% drift at H=0.25.
This lane repeats the same refinement sweep on Fam2 and Fam3 to
test whether the converged continuum coefficient is **family-portable**.

If all three families give the same continuum value (or close),
we have a geometry-invariant Kubo coefficient that's a candidate
for a "true" continuum-limit observable. If they differ, the
continuum limit is family-specific and we have three distinct
physical predictions.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kubo_continuum_limit import (
    grow, true_kubo_at_H, finite_diff_dM,
    T_PHYS, PW_PHYS, K_PER_H, S_PHYS, MASS_Z_PHYS, SRC_LAYER_FRAC,
)

FAMILIES = [
    ("Fam1", 0.20, 0.70),
    ("Fam2", 0.05, 0.30),
    ("Fam3", 0.50, 0.90),
]

REFINEMENTS = [(0.5, "coarse"), (0.35, "medium"), (0.25, "fine")]


def measure(H_val, fam_drift, fam_restore):
    NL = max(3, round(T_PHYS / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    x_src = round(NL * SRC_LAYER_FRAC) * H_val
    z_src = MASS_Z_PHYS

    pos, adj, nmap = grow(0, fam_drift, fam_restore, NL, PW, 3, H_val)
    kubo, cz_free, T0 = true_kubo_at_H(pos, adj, NL, PW, H_val, k_phase, x_src, z_src)
    cz_0 = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, 0.0)
    cz_s = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, S_PHYS)
    dM_fd = (cz_s - cz_0) / S_PHYS
    return {
        "H": H_val, "NL": NL, "n_nodes": len(pos),
        "kubo_true": kubo, "dM_fd": dM_fd, "cz_free": cz_free,
    }


def main():
    print("=" * 100)
    print("KUBO CONTINUUM LIMIT — FAMILY PORTABILITY (Fam1, Fam2, Fam3)")
    print(f"Physical: T={T_PHYS}, PW={PW_PHYS}, k*H={K_PER_H}, "
          f"S={S_PHYS}, z_src={MASS_Z_PHYS}")
    print("=" * 100)

    results = {}
    for fam_name, drift, restore in FAMILIES:
        print(f"\n--- {fam_name} (drift={drift}, restore={restore}) ---")
        fam_runs = []
        for H_val, label in REFINEMENTS:
            r = measure(H_val, drift, restore)
            fam_runs.append((label, r))
            print(f"  [{label}] H={H_val}, NL={r['NL']}, n={r['n_nodes']}")
            print(f"    kubo_true = {r['kubo_true']:+.6f}, "
                  f"dM_fd = {r['dM_fd']:+.6f}, "
                  f"cz_free = {r['cz_free']:+.6f}")
        results[fam_name] = fam_runs

    print("\n" + "=" * 100)
    print("REFINEMENT TABLE — kubo_true per family")
    print("=" * 100)
    header = f"{'H':>6s}"
    for fam_name, _, _ in FAMILIES:
        header += f" {fam_name + '_kubo':>14s}"
    print(header)
    for i, (H_val, label) in enumerate(REFINEMENTS):
        row = f"{H_val:6.3f}"
        for fam_name, _, _ in FAMILIES:
            v = results[fam_name][i][1]["kubo_true"]
            row += f" {v:+14.6f}"
        print(row)

    print("\n" + "=" * 100)
    print("PER-FAMILY CONVERGENCE")
    print("=" * 100)
    for fam_name, _, _ in FAMILIES:
        runs = results[fam_name]
        print(f"\n{fam_name}:")
        for i in range(len(runs) - 1):
            v1 = runs[i][1]["kubo_true"]
            v2 = runs[i + 1][1]["kubo_true"]
            d = v2 - v1
            rel = d / v1 if abs(v1) > 1e-12 else 0.0
            print(f"  {runs[i][0]:>8s} ({v1:+.4f}) → {runs[i+1][0]:>8s} "
                  f"({v2:+.4f})  Δ = {d:+.4f} ({rel:+.1%})")

    # Compare last-refinement values across families
    print("\n" + "=" * 100)
    print("FAMILY PORTABILITY (at finest H)")
    print("=" * 100)
    final_vals = []
    for fam_name, _, _ in FAMILIES:
        v = results[fam_name][-1][1]["kubo_true"]
        final_vals.append((fam_name, v))
        print(f"  {fam_name}: kubo_true = {v:+.4f}")
    mean_v = sum(v for _, v in final_vals) / len(final_vals)
    dev = [abs(v - mean_v) for _, v in final_vals]
    max_dev = max(dev)
    rel_dev = max_dev / abs(mean_v) if abs(mean_v) > 1e-12 else 0.0
    print(f"\n  Mean: {mean_v:+.4f}")
    print(f"  Max deviation from mean: {max_dev:.4f} ({rel_dev:.1%})")

    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    # Last-step convergence for each family
    last_drifts = []
    for fam_name, _, _ in FAMILIES:
        runs = results[fam_name]
        v_prev = runs[-2][1]["kubo_true"]
        v_last = runs[-1][1]["kubo_true"]
        drift = abs(v_last - v_prev) / abs(v_prev) if abs(v_prev) > 1e-12 else 0.0
        last_drifts.append((fam_name, drift))
        print(f"  {fam_name}: last-step drift = {drift:.1%}")

    all_converged = all(d < 0.05 for _, d in last_drifts)
    family_portable = rel_dev < 0.10

    if all_converged and family_portable:
        print(f"\n  STRONG POSITIVE — all three families converge at the last")
        print(f"  refinement step (all drifts < 5%) AND the converged values")
        print(f"  agree within 10% ({rel_dev:.1%} max deviation from mean).")
        print(f"  The continuum-limit Kubo coefficient is family-portable.")
    elif all_converged:
        print(f"\n  PARTIAL POSITIVE — all three families converge individually")
        print(f"  but the converged values differ by {rel_dev:.1%} > 10%.")
        print(f"  Each family has its own continuum-limit coefficient; they")
        print(f"  don't agree across families.")
    elif family_portable:
        print(f"\n  PARTIAL — family values agree at the last refinement but")
        print(f"  not all families are individually converged. More refinements")
        print(f"  needed.")
    else:
        print(f"\n  NEGATIVE — families neither individually converged nor")
        print(f"  family-portable at the last refinement.")


if __name__ == "__main__":
    main()
