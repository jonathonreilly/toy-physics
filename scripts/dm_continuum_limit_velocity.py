#!/usr/bin/env python3
"""Continuum limit of dM (retarded wave field deflection) at multiple v/c.

Lane δ. The wave-retardation continuum lane
(`wave_retardation_continuum_limit.py`) established that `dM` — the
beam centroid deflection through the retarded wave-equation field
driven by a moving source — is the one continuum-stable dynamical
quantity. At v/c = 0.30 on Fam1, dM drifts only 14% monotonically
across the refinement {0.5, 0.35, 0.25}.

That was a single velocity. This lane sweeps v/c and measures dM
alone (NO comparators: no dI, dIeq, or dN) across the same
refinement. The question:

  Does dM(v/c, H) converge to a stable function dM(v/c) in the H→0
  limit, across multiple velocities?

If yes, we have a **direct continuum prediction** for the retarded
gravitational deflection as a function of source velocity — without
any reference to an instantaneous-Newton comparator. This bypasses
the comparator question that blocks the wave-retardation lab card.

If no, we learn that dM's apparent stability at v/c = 0.30 was
velocity-specific and the retarded field has lattice artifacts at
other velocities too.

Safety: this lane does NOT touch cached-slice comparators, does NOT
reason from the old broken dN numbers, does NOT collide with Codex's
matrix-free exact-comparator work.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Reuse the lattice-spacing-parametric wave-equation machinery from
# the companion continuum-limit lane. We only import helpers, NOT
# the cached-slice or imposed-Newton comparators.
from wave_retardation_continuum_limit import (
    grow, solve_wave, prop_beam, cz,
    PW_PHYS, K_PER_H, S_PHYS, BETA,
    T_PHYS_LAYERS, IZ_START_PHYS, IZ_END_PHYS,
    SRC_LAYER_FRAC,
)


def measure_dM_at(H_val, v_target):
    """Measure dM at a given (H, v/c target) without any comparator.

    Physical parameters: T_phys, PW_phys, k*H held approximately constant.
    Source trajectory: iz_start at IZ_START_PHYS/H, moves linearly in z
    with velocity v_target (cells/layer) for n_active layers.

    The source trajectory is set by the TARGET velocity, not the
    physical displacement — iz_end follows from v_target.
    """
    NL = max(3, round(T_PHYS_LAYERS / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    src_layer = max(1, int(SRC_LAYER_FRAC * NL))
    n_active = NL - src_layer
    if n_active < 2:
        return None

    # Source starts at IZ_START_PHYS in physical coordinates and moves
    # at v_target cells per layer (lattice-unit velocity).
    iz_start = round(IZ_START_PHYS / H_val)
    # v_target is negative (source moves toward z=0); iz_end follows.
    iz_end_realized = iz_start + round(v_target * n_active)
    # realized v_per_layer from rounded endpoints
    v_per_layer = (iz_end_realized - iz_start) / n_active

    iz_of_t = lambda t, sl=src_layer, vpl=v_per_layer, izs=iz_start: \
        izs + int(round(vpl * (t - sl)))

    # M only — no comparators
    h_M = solve_wave(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    free = prop_beam(pos, adj, nmap, None, k_phase, NL, PW, H_val)
    z_free = cz(free, pos, NL, PW, H_val)
    cz_M = cz(prop_beam(pos, adj, nmap, h_M, k_phase, NL, PW, H_val),
              pos, NL, PW, H_val)
    dM = cz_M - z_free

    return {
        "H": H_val, "NL": NL, "src_layer": src_layer,
        "n_active": n_active, "iz_start": iz_start,
        "iz_end_realized": iz_end_realized,
        "v_target": v_target, "v_realized": v_per_layer,
        "n_nodes": len(pos), "dM": dM,
    }


def main():
    print("=" * 100)
    print("LANE δ: dM continuum limit across multiple v/c")
    print("No comparators (no dI, dIeq, or dN) — only the retarded wave field")
    print("=" * 100)
    print(f"Physical: T={T_PHYS_LAYERS}, PW={PW_PHYS}, k*H={K_PER_H}, S={S_PHYS}")
    print(f"Source trajectory: iz_start from IZ_START_PHYS={IZ_START_PHYS},")
    print(f"                   iz_end follows from velocity target")
    print()

    # Velocity targets (cells per layer, negative = source moves toward z=0)
    # Lane δ+: extended to 3 refinements including H=0.25 at the three existing
    # velocities. Cost: 3 velocities × 3 refinements = 9 wave solves. The H=0.25
    # finest step dominates cost.
    velocity_targets = [-0.15, -0.25, -0.35]
    refinements = [(0.5, "coarse"), (0.35, "medium"), (0.25, "fine")]

    # results[v_target] = list of runs (one per refinement)
    results = {}

    for v_target in velocity_targets:
        print(f"\n--- v_target = {v_target:+.3f} ---", flush=True)
        runs = []
        for H_val, label in refinements:
            r = measure_dM_at(H_val, v_target)
            if r is None:
                print(f"  [{label}] H={H_val}: SKIPPED (n_active < 2)")
                continue
            runs.append((label, r))
            print(f"  [{label}] H={H_val:.3f} NL={r['NL']:3d} "
                  f"iz: {r['iz_start']:+d}→{r['iz_end_realized']:+d} "
                  f"v_real={r['v_realized']:+.4f} "
                  f"dM={r['dM']:+.6f}")
        results[v_target] = runs

    # Refinement table
    print("\n" + "=" * 100)
    print("REFINEMENT TABLE — dM(v, H)")
    print("=" * 100)
    header = f"{'v_target':>10s}"
    for H_val, label in refinements:
        header += f" {label + f' (H={H_val})':>18s}"
    header += f" {'|Δlast|/|med|':>15s}"
    print(header)
    for v_target in velocity_targets:
        runs = results[v_target]
        row = f"{v_target:+10.3f}"
        dM_vals = []
        for H_val, label in refinements:
            found = next((r for l, r in runs if l == label), None)
            if found is None:
                row += f" {'—':>18s}"
                dM_vals.append(None)
            else:
                row += f" {found['dM']:+18.6f}"
                dM_vals.append(found["dM"])
        # Compute last-step drift between the two FINAL refinements (whatever
        # they are — handles 2 or 3 refinement schedules).
        if len(dM_vals) >= 2 and dM_vals[-2] is not None and dM_vals[-1] is not None \
                and abs(dM_vals[-2]) > 1e-12:
            last_drift = abs(dM_vals[-1] - dM_vals[-2]) / abs(dM_vals[-2])
            row += f" {last_drift:15.1%}"
        print(row)

    # Per-velocity convergence verdict
    print("\n" + "=" * 100)
    print("PER-VELOCITY CONVERGENCE (last-step drift)")
    print("=" * 100)
    converged = []
    not_converged = []
    for v_target in velocity_targets:
        runs = results[v_target]
        if len(runs) < 2:
            print(f"  v={v_target:+.3f}: insufficient data")
            continue
        dM_med = runs[-2][1]["dM"]
        dM_fine = runs[-1][1]["dM"]
        if abs(dM_med) > 1e-12:
            drift = abs(dM_fine - dM_med) / abs(dM_med)
        else:
            drift = 0.0
        status = "CONVERGED" if drift < 0.05 else \
                 "MARGINAL" if drift < 0.15 else \
                 "NOT CONVERGED"
        print(f"  v={v_target:+.3f}: Δ = {dM_fine - dM_med:+.6f} "
              f"({drift:.1%})  {status}")
        if drift < 0.05:
            converged.append((v_target, dM_fine))
        else:
            not_converged.append((v_target, dM_fine, drift))

    # Functional form on converged subset
    if converged:
        print("\n" + "=" * 100)
        print("FUNCTIONAL FORM dM(v/c) ON CONVERGED VELOCITIES (at finest H)")
        print("=" * 100)
        for v, dM_v in converged:
            print(f"  v={v:+.3f}:  dM = {dM_v:+.6f}")

        # Simple trend check: is dM monotone in v?
        sorted_conv = sorted(converged, key=lambda x: x[0])
        dM_series = [d for _, d in sorted_conv]
        is_monotone_inc = all(dM_series[i] <= dM_series[i + 1]
                              for i in range(len(dM_series) - 1))
        is_monotone_dec = all(dM_series[i] >= dM_series[i + 1]
                              for i in range(len(dM_series) - 1))
        print()
        if is_monotone_inc:
            print("  dM is MONOTONE INCREASING in v_target (toward zero)")
        elif is_monotone_dec:
            print("  dM is MONOTONE DECREASING in v_target (toward zero)")
        else:
            print("  dM is NON-MONOTONE in v_target across converged points")

    # Verdict
    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    n_conv = len(converged)
    n_total = len(velocity_targets)
    print(f"  Converged velocities: {n_conv}/{n_total}")
    if n_conv >= 3 and converged:
        sorted_conv = sorted(converged, key=lambda x: x[0])
        dM_series = [d for _, d in sorted_conv]
        is_monotone = (all(dM_series[i] <= dM_series[i + 1]
                           for i in range(len(dM_series) - 1))
                       or all(dM_series[i] >= dM_series[i + 1]
                              for i in range(len(dM_series) - 1)))
        if is_monotone:
            print("  STRONG POSITIVE — dM(v/c) has a clean continuum form on")
            print(f"  at least {n_conv} velocities AND is monotone in v. This is a")
            print("  direct continuum prediction for the retarded gravitational")
            print("  deflection, independent of any c=∞ comparator.")
        else:
            print("  PARTIAL POSITIVE — dM converges at multiple velocities but")
            print("  the v-dependence is non-monotone.")
    elif n_conv >= 1:
        print(f"  PARTIAL — dM converges at {n_conv} velocities, not enough for")
        print("  a functional-form claim.")
    else:
        print("  NEGATIVE — no velocity converged at the 5% threshold.")
    if not_converged:
        print(f"\n  {len(not_converged)} velocities NOT converged:")
        for v, dM_v, drift in not_converged:
            print(f"    v={v:+.3f}: dM={dM_v:+.6f} last-step drift {drift:.1%}")


if __name__ == "__main__":
    main()
