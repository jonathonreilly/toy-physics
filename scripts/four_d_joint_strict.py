#!/usr/bin/env python3
"""Strict 4D same-graph unification test on the retained modular lanes.

Goal
----
Use the same 4D modular DAG instances, where possible, to test whether the
retained higher-dimensional lane simultaneously supports:

  1. Gravity: positive deflection toward mass
  2. Decoherence: actual CL-bath purity `pur_cl`
  3. Interference: newer binned true-visibility metric
  4. Born rule: a true chokepoint companion graph with linearity + I_3

This is intentionally the stricter version of the 4D story:
  - no old exact-y visibility proxy
  - no old purity-floor-only pass criterion
  - no propagator tweaks

The modular lanes tested here are the retained dense 4D families:
  gap=3 and gap=5.

Interpretation discipline
-------------------------
The strict visibility metric is the hardest filter. If gravity, purity, and
Born rule pass but visibility stays weak, the safe claim is still a partial
coexistence result, not full strict unification.
"""

from __future__ import annotations

import math
import os
import random
import statistics
import sys
import time
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.four_d_born_rule_chokepoint import (  # type: ignore
    generate_4d_chokepoint_dag,
    linearity_check,
    sorkin_test_4d,
)
from scripts.four_d_decoherence_large_n import (  # type: ignore
    N_YBINS,
    cl_purity,
    compute_field_4d,
    generate_4d_modular_dag,
    propagate_4d,
)
from scripts.four_d_true_visibility_binned import (  # type: ignore
    build_setup,
    true_visibility_binned,
)

BETA = 0.8
LAM = 10.0
K_BAND = (3.0, 5.0, 7.0)
TARGET_VALID = 4
MAX_ATTEMPTS = 24
NODES_PER_LAYER = 40
SPATIAL_RANGE = 5.0
CONNECT_RADIUS = 6.0
N_LAYERS_LIST = (20, 40, 60, 80)
GAPS = (3.0, 5.0)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _t_stat(values: list[float]) -> float:
    if not values:
        return math.nan
    se = _se(values)
    if not math.isfinite(se) or se <= 1e-30:
        return math.nan
    return _mean(values) / se


def _gravity_seed_delta(positions, adj, setup) -> float | None:
    src = setup["src"]
    det_list = setup["det_list"]
    field = setup["field"]
    blocked = setup["blocked"]

    deltas = []
    field_flat = [0.0] * len(positions)
    for k in K_BAND:
        amps_mass = propagate_4d(positions, adj, field, src, k, blocked)
        amps_flat = propagate_4d(positions, adj, field_flat, src, k, blocked)

        prob_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        prob_flat = sum(abs(amps_flat[d]) ** 2 for d in det_list)
        if prob_mass <= 1e-30 or prob_flat <= 1e-30:
            continue

        y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / prob_mass
        y_flat = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / prob_flat
        deltas.append(y_mass - y_flat)

    if not deltas:
        return None
    return _mean(deltas)


def _decoherence_seed_metrics(positions, adj, setup) -> tuple[float, float, float] | None:
    src = setup["src"]
    det_list = setup["det_list"]
    field = setup["field"]
    blocked = setup["blocked"]
    slit_a = setup["slit_a"]
    slit_b = setup["slit_b"]
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    bl_idx = len(layers) // 3

    mid_nodes = [
        i
        for layer in layers[bl_idx + 1 : -1]
        for i in by_layer[layer]
        if i not in blocked and i not in set(det_list)
    ]
    if len(mid_nodes) < 4:
        return None

    pur_vals = []
    min_vals = []
    sn_vals = []

    for k in K_BAND:
        amps_a = propagate_4d(positions, adj, field, src, k, blocked | set(slit_b))
        amps_b = propagate_4d(positions, adj, field, src, k, blocked | set(slit_a))

        ba = [0j] * N_YBINS
        bb = [0j] * N_YBINS
        y_min = min(positions[i][1] for i in mid_nodes) - 1e-3
        y_max = max(positions[i][1] for i in mid_nodes) + 1e-3
        if y_max <= y_min:
            continue
        bw = (y_max - y_min) / N_YBINS
        for m in mid_nodes:
            y = positions[m][1]
            b = int((y - y_min) / bw)
            b = max(0, min(N_YBINS - 1, b))
            ba[b] += amps_a[m]
            bb[b] += amps_b[m]

        denom = sum(abs(a) ** 2 for a in ba) + sum(abs(b) ** 2 for b in bb)
        if denom <= 1e-30:
            continue
        sn = sum(abs(a - b) ** 2 for a, b in zip(ba, bb)) / denom
        D = math.exp(-(LAM ** 2) * sn)
        pur = cl_purity(amps_a, amps_b, D, det_list)
        pur_min = cl_purity(amps_a, amps_b, 0.0, det_list)
        if math.isnan(pur) or math.isnan(pur_min):
            continue
        pur_vals.append(pur)
        min_vals.append(pur_min)
        sn_vals.append(sn)

    if not pur_vals:
        return None

    return _mean(pur_vals), _mean(min_vals), _mean(sn_vals)


def _visibility_seed_metric(positions, adj) -> tuple[float, float, float] | None:
    setup = build_setup(positions, adj)
    if setup is None:
        return None
    result = true_visibility_binned(positions, adj, setup)
    if result is None:
        return None
    return result


def _born_companion_metrics(n_layers: int, seed: int) -> tuple[float, float] | None:
    positions, adj, layer_indices = generate_4d_chokepoint_dag(
        n_layers=n_layers,
        nodes_per_layer=NODES_PER_LAYER,
        rng_seed=seed * 13 + 5,
    )

    lin_errs = []
    for k in K_BAND:
        rel = linearity_check(positions, adj, layer_indices, k)
        if rel is not None:
            lin_errs.append(rel)

    i3_ratios = []
    for k in (3.0, 5.0):
        result = sorkin_test_4d(positions, adj, layer_indices, k)
        if result is None:
            continue
        i3, p = result
        if p > 1e-30:
            i3_ratios.append(abs(i3) / p)

    if not lin_errs or not i3_ratios:
        return None
    return max(lin_errs), max(i3_ratios)


def _fmt_verdict(flag: bool, weak: bool = False) -> str:
    if flag:
        return "PASS"
    return "WEAK" if weak else "FAIL"


def run_gap(
    gap: float, born_cache: dict[tuple[int, int], tuple[float, float] | None]
) -> list[dict[str, float | int | str]]:
    print(f"[4D modular gap={gap}] same-graph gravity + decoherence + binned visibility")
    print(
        f"  {'N':>4s}  {'grav_d':>8s}  {'grav_t':>6s}  {'pur_cl':>8s}  {'pur_min':>8s}  "
        f"{'V_gain':>8s}  {'born_err':>9s}  {'born_I3/P':>10s}  {'n_ok':>4s}  verdict"
    )
    print(f"  {'-' * 88}")

    rows: list[dict[str, float | int | str]] = []
    for nl in N_LAYERS_LIST:
        grav_vals: list[float] = []
        pur_vals: list[float] = []
        min_vals: list[float] = []
        vis_vals: list[float] = []
        born_i3_vals: list[float] = []
        born_lin_vals: list[float] = []
        n_ok = 0
        attempts = 0

        t0 = time.time()
        while attempts < MAX_ATTEMPTS and n_ok < TARGET_VALID:
            seed = attempts
            attempts += 1
            positions, adj, _ = generate_4d_modular_dag(
                n_layers=nl,
                nodes_per_layer=NODES_PER_LAYER,
                spatial_range=SPATIAL_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed * 13 + 5,
                gap=gap,
            )

            setup = build_setup(positions, adj)
            if setup is None:
                continue

            grav_delta = _gravity_seed_delta(positions, adj, setup)
            decoh = _decoherence_seed_metrics(positions, adj, setup)
            vis = _visibility_seed_metric(positions, adj)
            born = born_cache.get((nl, seed))
            if born is None:
                born = _born_companion_metrics(nl, seed)
                born_cache[(nl, seed)] = born

            if grav_delta is None or decoh is None or vis is None or born is None:
                continue

            pur_cl, pur_min, _sn = decoh
            v_coh, v_single, v_gain = vis
            born_lin, born_i3 = born

            grav_vals.append(grav_delta)
            pur_vals.append(pur_cl)
            min_vals.append(pur_min)
            vis_vals.append(v_gain)
            born_lin_vals.append(born_lin)
            born_i3_vals.append(born_i3)
            n_ok += 1

        dt = time.time() - t0
        if not n_ok:
            print(f"  {nl:4d}  FAIL")
            continue

        grav_mean = _mean(grav_vals)
        grav_se = _se(grav_vals)
        grav_t = _t_stat(grav_vals)
        pur_cl = _mean(pur_vals)
        pur_min = _mean(min_vals)
        vis_gain = _mean(vis_vals)
        born_i3 = _mean(born_i3_vals)
        born_lin = _mean(born_lin_vals)
        born_i3_max = max(born_i3_vals)
        born_lin_max = max(born_lin_vals)

        grav_pass = math.isfinite(grav_t) and grav_t > 2.0 and grav_mean > 0
        decoh_pass = pur_cl < 0.96
        vis_pass = vis_gain > 0.02
        born_pass = born_lin_max < 1e-10 and born_i3_max < 1e-10

        if grav_pass and decoh_pass and vis_pass and born_pass:
            verdict = "ALL FOUR"
        elif grav_pass and decoh_pass and born_pass:
            verdict = "3/4 (vis weak)"
        elif grav_pass and decoh_pass:
            verdict = "2/4+"
        else:
            verdict = "PARTIAL"

        print(
            f"  {nl:4d}  {grav_mean:+8.3f}  {grav_t:6.2f}  {pur_cl:8.3f}  {pur_min:8.3f}  "
            f"{vis_gain:+8.3f}  {born_lin:9.1e}  {born_i3:10.2e}  {n_ok:4d}  {verdict}"
        )
        rows.append(
            {
                "gap": gap,
                "N": nl,
                "grav_d": grav_mean,
                "grav_t": grav_t,
                "pur_cl": pur_cl,
                "pur_min": pur_min,
                "vis_gain": vis_gain,
                "born_err": born_lin,
                "born_i3": born_i3,
                "n_ok": n_ok,
                "verdict": verdict,
            }
        )

    print()
    print(
        "Interpretation: the strict joint lane is the retained modular family with the\n"
        "same graph used for gravity, actual CL purity, and binned visibility.\n"
        "Born-rule tests use a matched chokepoint companion graph with the same\n"
        "seed and layer schedule, because the barrier has to be a true chokepoint."
    )
    print()
    return rows


def main() -> None:
    print("=" * 88)
    print("4D STRICT SAME-GRAPH UNIFICATION TEST")
    print("  Retained lanes: modular gap=3 and gap=5")
    print("  Metrics: gravity, actual pur_cl, binned visibility, chokepoint Born rule")
    print("  Graph family: dense 4D modular DAGs")
    print("=" * 88)
    print()

    born_cache: dict[tuple[int, int], tuple[float, float] | None] = {}
    all_rows: list[dict[str, float | int | str]] = []
    for gap in GAPS:
        all_rows.extend(run_gap(gap, born_cache))

    best_all_four = next((r for r in all_rows if r["verdict"] == "ALL FOUR"), None)
    best_partial = next((r for r in all_rows if r["verdict"] in {"ALL FOUR", "3/4 (vis weak)", "PARTIAL"}), None)

    print("=" * 88)
    print("OVERALL STRONGEST SAFE CLAIM")
    if best_all_four is not None:
        print(
            f"  gap={best_all_four['gap']:.1f}, N={best_all_four['N']}: "
            f"gravity {best_all_four['grav_d']:+.3f} (t={best_all_four['grav_t']:.2f}), "
            f"pur_cl={best_all_four['pur_cl']:.3f}, V_gain={best_all_four['vis_gain']:+.3f}, "
            f"Born companion machine-precision clean"
        )
        print("  Safe headline: 4-way coexistence exists on the retained 4D modular lane,")
        print("  but only at the best retained gap/N point; other rows remain partial.")
    elif best_partial is not None:
        print(
            f"  gap={best_partial['gap']:.1f}, N={best_partial['N']}: "
            f"gravity {best_partial['grav_d']:+.3f} (t={best_partial['grav_t']:.2f}), "
            f"pur_cl={best_partial['pur_cl']:.3f}, V_gain={best_partial['vis_gain']:+.3f}"
        )
        print("  Safe headline: partial coexistence only; strict visibility remains weak.")
    else:
        print("  No valid same-graph strict row survived the hard metric.")

    print("=" * 88)
    print("SAFE CLAIM GUIDE")
    print("  - If gravity + pur_cl + Born pass but visibility is weak, keep the claim")
    print("    at 'partial coexistence on the same 4D modular graphs'.")
    print("  - If visibility passes too, that is the strongest 4D coexistence claim.")
    print("  - Do not promote any row that relies on the old exact-y visibility proxy.")
    print("=" * 88)


if __name__ == "__main__":
    main()
