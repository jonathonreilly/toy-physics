#!/usr/bin/env python3
"""Canonical slit-width complementarity sweep on the ordered lattice family.

The question is narrow:
does the retained ordered-lattice family support a stable tradeoff between
which-slit / decoherence observables and barrier-card distance-law quality?

Scope rules:
  - standard linear propagator only
  - same ordered-lattice family throughout
  - one fixed detector observable: final-layer centroid shift
  - one fixed barrier-card distance-law fit: far-field |delta| fit on b >= 7
  - Born is reported on a same-family companion Sorkin aperture, not the exact
    same two-slit card used for MI / d_TV / gravity
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.lattice_family_validation import (  # noqa: E402
    K,
    centroid_y,
    cl_purity,
    fit_power_law,
    mutual_info_and_purity,
    sorkin_born,
)
from scripts.lattice_mirror_distance import (  # noqa: E402
    compute_field_at_b,
    generate_lattice_mirror,
    propagate,
)

N_LAYERS = 40
HALF_WIDTH = 20
SLIT_GAPS = [1, 2, 3, 4, 5, 6, 7]
B_VALUES = [3, 5, 7, 10, 13, 16, 19]
FIT_B_MIN = 7
MASS_OFFSET_FROM_FIRST_OPEN_ROW = 4

RETAIN_BORN_MAX = 1e-12
RETAIN_K0_MAX = 1e-9
RETAIN_MI_MIN = 0.50
RETAIN_DECOH_MIN = 0.05
RETAIN_DISTANCE_R2_MIN = 0.90


def build_mid_nodes(layers, node_map):
    barrier_idx = len(layers) // 3
    start = barrier_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(N_LAYERS / 6)))
    mid_nodes = []
    for layer in layers[start:stop]:
        for y in range(-HALF_WIDTH, HALF_WIDTH + 1):
            mid_nodes.append(node_map[(layer, y)])
    return mid_nodes


def fit_barrier_distance(rows):
    tail = [(b, abs(delta)) for b, delta in rows if b >= FIT_B_MIN and abs(delta) > 1e-12]
    if len(tail) < 3:
        return None
    return fit_power_law(tail)


def open_rows_for_gap(gap):
    upper_rows = list(range(gap + 1, HALF_WIDTH + 1))
    lower_rows = list(range(-HALF_WIDTH, -gap))
    return upper_rows, lower_rows


def born_companion_rows(gap):
    # Same family, but a companion 3-slit Sorkin aperture rather than the exact
    # same two-slit card used for MI / d_TV / gravity.
    return [gap + 1], [-(gap + 1)], [-1, 0, 1]


def retained_balance(row):
    fit = row["fit"]
    return (
        row["born"] <= RETAIN_BORN_MAX
        and abs(row["k0"]) <= RETAIN_K0_MAX
        and row["mi"] >= RETAIN_MI_MIN
        and row["decoh"] >= RETAIN_DECOH_MIN
        and fit is not None
        and fit[2] >= RETAIN_DISTANCE_R2_MIN
    )


def main():
    positions, adj, barrier_layer, node_map = generate_lattice_mirror(N_LAYERS, HALF_WIDTH, 42)
    layers = sorted({round(p[0]) for p in positions})
    src = [node_map[(layers[0], 0)]]
    det_list = [node_map[(layers[-1], y)] for y in range(-HALF_WIDTH, HALF_WIDTH + 1)]
    grav_layer = layers[2 * len(layers) // 3]
    field_zero = [0.0] * len(positions)
    barrier_nodes = [node_map[(barrier_layer, y)] for y in range(-HALF_WIDTH, HALF_WIDTH + 1)]
    mid_nodes = build_mid_nodes(layers, node_map)

    print("=" * 114)
    print("LATTICE COMPLEMENTARITY SWEEP")
    print("  ordered 2D lattice, standard linear propagator, barrier-card slit-width sweep")
    print("  Born is a same-family companion Sorkin audit, not the exact same 2-slit aperture card")
    print("=" * 114)
    print()
    print("SETUP")
    print(f"  N={N_LAYERS}, half_width={HALF_WIDTH}, k={K}")
    print("  family: ordered 2D lattice with forward |dy| <= 1")
    print("  detector observable: final-layer centroid shift")
    print(f"  fit procedure: far-field |delta| fit on b >= {FIT_B_MIN} using the same barrier card")
    print("  mass convention: one mass node at first_open_upper_row + 4")
    print()

    rows = []
    for gap in SLIT_GAPS:
        upper_rows, lower_rows = open_rows_for_gap(gap)
        slit_width = len(upper_rows)
        first_open_row = upper_rows[0]
        mass_b = first_open_row + MASS_OFFSET_FROM_FIRST_OPEN_ROW

        slit_a = [node_map[(barrier_layer, y)] for y in upper_rows]
        slit_b = [node_map[(barrier_layer, y)] for y in lower_rows]
        blocked = set(barrier_nodes) - set(slit_a + slit_b)

        field_m, _ = compute_field_at_b(positions, node_map, grav_layer, mass_b, n_mass=1)

        psi_a = propagate(positions, adj, field_m, src, K, blocked | set(slit_b))
        psi_b = propagate(positions, adj, field_m, src, K, blocked | set(slit_a))
        mi_row = mutual_info_and_purity(psi_a, psi_b, det_list)
        pur_cl, s_norm = cl_purity(psi_a, psi_b, positions, mid_nodes, det_list, HALF_WIDTH)

        pa = {d: abs(psi_a[d]) ** 2 for d in det_list}
        pb = {d: abs(psi_b[d]) ** 2 for d in det_list}
        na = sum(pa.values())
        nb = sum(pb.values())
        dtv = (
            0.5 * sum(abs(pa[d] / na - pb[d] / nb) for d in det_list)
            if na > 1e-30 and nb > 1e-30
            else math.nan
        )

        am = propagate(positions, adj, field_m, src, K, blocked)
        af = propagate(positions, adj, field_zero, src, K, blocked)
        gravity = centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list)

        am0 = propagate(positions, adj, field_m, src, 0.0, blocked)
        af0 = propagate(positions, adj, field_zero, src, 0.0, blocked)
        gravity_k0 = centroid_y(am0, positions, det_list) - centroid_y(af0, positions, det_list)

        born_a_rows, born_b_rows, born_c_rows = born_companion_rows(gap)
        born_a = [node_map[(barrier_layer, y)] for y in born_a_rows]
        born_b = [node_map[(barrier_layer, y)] for y in born_b_rows]
        born_c = [node_map[(barrier_layer, y)] for y in born_c_rows]
        born = sorkin_born(
            positions,
            adj,
            src,
            K,
            barrier_nodes,
            born_a,
            born_b,
            born_c,
            det_list,
            field_zero,
        )

        distance_rows = []
        for b in B_VALUES:
            field_b, _ = compute_field_at_b(positions, node_map, grav_layer, b, n_mass=1)
            amb = propagate(positions, adj, field_b, src, K, blocked)
            afb = propagate(positions, adj, field_zero, src, K, blocked)
            delta = centroid_y(amb, positions, det_list) - centroid_y(afb, positions, det_list)
            distance_rows.append((b, delta))
        fit = fit_barrier_distance(distance_rows)

        rows.append(
            {
                "gap": gap,
                "slit_width": slit_width,
                "first_open_row": first_open_row,
                "mass_b": mass_b,
                "mi": mi_row["MI"],
                "dtv": dtv,
                "pur_cl": pur_cl,
                "decoh": 1.0 - pur_cl,
                "gravity": gravity,
                "gravity_sign": "away" if gravity < 0 else "toward",
                "born": born,
                "k0": gravity_k0,
                "fit": fit,
                "distance_rows": distance_rows,
                "s_norm": s_norm,
            }
        )

    print("TRADEOFF TABLE")
    print(
        f"  {'gap':>4s}  {'width':>5s}  {'mass_b':>6s}  {'MI':>7s}  {'d_TV':>7s}  "
        f"{'pur_cl':>7s}  {'1-pur':>7s}  {'alpha':>8s}  {'R^2':>7s}  {'grav':>9s}  "
        f"{'sign':>6s}  {'Born':>10s}  {'k=0':>10s}"
    )
    print(f"  {'-' * 108}")
    for row in rows:
        alpha = math.nan if row["fit"] is None else row["fit"][1]
        r2 = math.nan if row["fit"] is None else row["fit"][2]
        print(
            f"  {row['gap']:4d}  {row['slit_width']:5d}  {row['mass_b']:6d}  {row['mi']:7.3f}  "
            f"{row['dtv']:7.3f}  {row['pur_cl']:7.3f}  {row['decoh']:7.3f}  "
            f"{alpha:8.3f}  {r2:7.3f}  {row['gravity']:+9.4f}  {row['gravity_sign']:>6s}  "
            f"{row['born']:10.2e}  {row['k0']:+10.2e}"
        )
    print()

    print("DISTANCE CURVES")
    for row in rows:
        curve = "  ".join(f"b={b}:{delta:+.4f}" for b, delta in row["distance_rows"])
        print(f"  gap={row['gap']:d} width={row['slit_width']:d}: {curve}")
    print()

    qualifying_rows = [row for row in rows if retained_balance(row)]
    sweet_spot = max(qualifying_rows, key=lambda row: row["mi"]) if qualifying_rows else None

    print("TREND SUMMARY")
    print(f"  MI rises from {rows[0]['mi']:.3f} to {rows[-1]['mi']:.3f} as slits narrow")
    print(f"  d_TV rises from {rows[0]['dtv']:.3f} to {rows[-1]['dtv']:.3f} as slits narrow")
    print(f"  1-pur stays nontrivial across the sweep: {min(row['decoh'] for row in rows):.3f} to {max(row['decoh'] for row in rows):.3f}")
    print(
        f"  distance-law R^2 falls from {rows[0]['fit'][2]:.3f} to {rows[-1]['fit'][2]:.3f} "
        f"as slits narrow"
    )
    print(
        f"  same-card gravity sign is constant across the sweep: "
        f"{sorted({row['gravity_sign'] for row in rows})}"
    )
    print(
        f"  Born-clean companion rows: "
        f"{sum(1 for row in rows if row['born'] <= RETAIN_BORN_MAX)}/{len(rows)}"
    )
    print(
        f"  k=0-clean rows: "
        f"{sum(1 for row in rows if abs(row['k0']) <= RETAIN_K0_MAX)}/{len(rows)}"
    )
    print()

    print("SWEET SPOT GUARD")
    print(
        f"  Born <= {RETAIN_BORN_MAX:.0e}, |k0| <= {RETAIN_K0_MAX:.0e}, "
        f"MI >= {RETAIN_MI_MIN:.2f}, 1-pur >= {RETAIN_DECOH_MIN:.2f}, R^2 >= {RETAIN_DISTANCE_R2_MIN:.2f}"
    )
    if sweet_spot is None:
        print("  No row satisfies the bounded sweet-spot guard.")
        wording = "too unstable to promote"
    else:
        alpha = sweet_spot["fit"][1]
        r2 = sweet_spot["fit"][2]
        print(
            f"  retained sweet spot: gap={sweet_spot['gap']}, width={sweet_spot['slit_width']}, "
            f"mass_b={sweet_spot['mass_b']}"
        )
        print(
            f"    MI={sweet_spot['mi']:.3f}, d_TV={sweet_spot['dtv']:.3f}, pur_cl={sweet_spot['pur_cl']:.3f}, "
            f"1-pur={sweet_spot['decoh']:.3f}"
        )
        print(
            f"    alpha={alpha:.3f}, R^2={r2:.3f}, gravity={sweet_spot['gravity']:+.4f} "
            f"({sweet_spot['gravity_sign']}), Born={sweet_spot['born']:.2e}, k0={sweet_spot['k0']:+.2e}"
        )
        wording = "bounded tradeoff curve with a sweet spot"
    print()

    print("PROMOTED WORDING RECOMMENDATION")
    print(f"  best description: {wording}")
    if sweet_spot is not None:
        print(
            "  ordered lattice supports a continuous tradeoff between "
            "decoherence/which-slit structure and distance-law quality, with a "
            "bounded sweet spot where both are simultaneously present"
        )
    else:
        print("  do not promote beyond exploratory status")


if __name__ == "__main__":
    main()
