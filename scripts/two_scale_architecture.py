#!/usr/bin/env python3
"""Two-scale architecture: G2 macro + micro env within bins.

Macro layer (G2): coarse-grained propagation between y-bins.
  → Prevents gravity saturation (tested, passes scaling).

Micro layer: within each y-bin, amplitude carries a local env register
  that records which mass node was visited in that bin.
  → Provides slit-selective recording within the coarse bundle.

The key insight: G2 reduces the effective path count between bins
(fixing gravity), while the per-bin env records maintain fine-grained
slit discrimination within each bin (potentially fixing decoherence).

Pass criteria:
  Gravity: R_grav at N=25 >= R_grav at N=12 (same as G2)
  Decoherence: purity at N=25 <= purity at N=12

PStack experiment: two-scale-architecture
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import (
    build_post_barrier_setup, compute_detector_metrics,
)
from scripts.two_register_decoherence import compute_field, centroid_y


def propagate_two_scale(positions, adj, field, src, det, k, mass_set,
                        blocked=None, n_ybins=8):
    """Two-scale propagator: G2 coarse-grained + per-bin env.

    State: (layer_idx, y_bin, per_bin_env) → amplitude
    per_bin_env is a tuple: for each y-bin, the last mass node visited
    while amplitude was in that bin (or -1 if none).

    Macro: amplitude moves between y-bins (G2 averaging).
    Micro: within each bin, env records mass interactions.
    """
    n = len(positions)
    blocked = blocked or set()

    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    all_ys = [y for _, y in positions]
    y_min, y_max = min(all_ys), max(all_ys)
    y_range = y_max - y_min + 1e-10
    bin_width = y_range / n_ybins

    def y_bin(y):
        return min(int((y - y_min) / bin_width), n_ybins - 1)

    # State: {(layer, ybin, env_tuple): amplitude}
    # env_tuple[b] = last mass node visited while in bin b (-1 if none)
    init_env = tuple([-1] * n_ybins)
    state = defaultdict(complex)
    for s in src:
        yb = y_bin(positions[s][1])
        state[(0, yb, init_env)] += 1.0 / len(src)

    for li in range(len(layers) - 1):
        curr_layer = layers[li]
        next_layer = layers[li + 1]
        curr_nodes = by_layer[curr_layer]
        next_nodes = set(by_layer[next_layer])

        curr_bins = defaultdict(list)
        for i in curr_nodes:
            if i not in blocked:
                curr_bins[y_bin(positions[i][1])].append(i)

        new_state = defaultdict(complex)

        for cb, cb_nodes in curr_bins.items():
            # Collect all env states at this bin
            env_amps = defaultdict(complex)
            for (l, b, env), amp in state.items():
                if l == li and b == cb and abs(amp) > 1e-30:
                    env_amps[env] += amp

            if not env_amps:
                continue

            # Find edges from this bin to next layer, grouped by dest bin
            dest_edges = defaultdict(list)
            for i in cb_nodes:
                for j in adj.get(i, []):
                    if j not in next_nodes or j in blocked:
                        continue
                    nb = y_bin(positions[j][1])
                    x1, y1 = positions[i]
                    x2, y2 = positions[j]
                    L = math.sqrt((x2-x1)**2+(y2-y1)**2)
                    if L < 1e-10:
                        continue
                    lf = 0.5*(field[i]+field[j])
                    dl = L*(1+lf)
                    ret = math.sqrt(max(dl*dl-L*L, 0))
                    act = dl-ret
                    ea = cmath.exp(1j*k*act)/(L**1.0)
                    is_mass = j in mass_set
                    dest_edges[nb].append((ea, j, is_mass))

            for env_tuple, amp in env_amps.items():
                for nb, edges in dest_edges.items():
                    # Macro: average edge amplitude within bundle (G2)
                    avg_ea = sum(ea for ea, _, _ in edges) / len(edges)

                    # Micro: update per-bin env with ALL mass nodes in dest bin
                    mass_in_dest = sorted(set(j for _, j, is_m in edges if is_m))
                    if mass_in_dest:
                        new_env = list(env_tuple)
                        # Use sorted tuple of mass nodes as env for this bin
                        new_env[nb] = tuple(mass_in_dest) if len(mass_in_dest) > 1 else mass_in_dest[0]
                        new_env = tuple(new_env)
                    else:
                        new_env = env_tuple

                    new_state[(li+1, nb, new_env)] += amp * avg_ea

        state.update(new_state)

    # Collect at detector: distribute bin amplitude evenly among
    # detector nodes in that bin (avoid occupancy-count distortion)
    det_layer_idx = len(layers) - 1

    det_by_bin = defaultdict(list)
    for d in det:
        det_by_bin[y_bin(positions[d][1])].append(d)

    det_state = {}
    for (l, b, env), amp in state.items():
        if l == det_layer_idx and b in det_by_bin:
            d_nodes = det_by_bin[b]
            # Distribute amplitude evenly (preserves total probability)
            amp_per_node = amp / len(d_nodes)
            for d in d_nodes:
                key = (d, env)
                if key not in det_state:
                    det_state[key] = 0.0+0.0j
                det_state[key] += amp_per_node

    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]
    tested_bins = []
    passing_bins = []

    print("=" * 70)
    print("TWO-SCALE ARCHITECTURE: G2 macro + per-bin micro env")
    print("  Pass: gravity stable AND purity not increasing with N")
    print("=" * 70)
    print()

    for n_bins in [6, 8]:
        print(f"  n_ybins = {n_bins}:")
        print(f"    {'N':>4s}  {'R_std':>7s}  {'R_g2':>7s}  {'R_2s':>7s}  "
              f"{'pur_fine':>8s}  {'pur_2s':>8s}  {'n_env':>5s}")
        print(f"    {'-' * 52}")
        rows = {}

        for nl in [8, 12, 15, 20, 25]:
            rg_std, rg_g2, rg_2s = [], [], []
            pf_list, p2s_list = [], []
            max_envs = 0

            for seed in range(5):
                positions, adj, _ = generate_causal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed*11+7)
                n = len(positions)
                scaled_depth = max(1, round(nl/6))
                setup = build_post_barrier_setup(positions, adj,
                                                  env_depth_layers=scaled_depth)
                if setup is None:
                    continue

                free_f = [0.0]*n
                mid_layer = setup["layers"][len(setup["layers"])//2]
                grav_mass = [i for i in setup["by_layer"][mid_layer]
                            if positions[i][1] > setup["cy"]+2]
                if len(grav_mass) < 2:
                    continue
                field_g = compute_field(positions, adj, grav_mass)

                # Standard gravity
                from scripts.two_register_decoherence import pathsum_coherent
                std_shifts = []
                for k in k_band:
                    fp = pathsum_coherent(positions, adj, free_f, setup["src"], setup["det"], k)
                    mp = pathsum_coherent(positions, adj, field_g, setup["src"], setup["det"], k)
                    std_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))

                # G2 gravity (from g2 script)
                from scripts.g2_coarse_grained_propagator import propagate_coarse_grained
                g2_shifts = []
                for k in k_band:
                    fp = propagate_coarse_grained(positions, adj, free_f, setup["src"], setup["det"], k, n_bins)
                    mp = propagate_coarse_grained(positions, adj, field_g, setup["src"], setup["det"], k, n_bins)
                    g2_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))

                # Two-scale gravity + decoherence
                ts_shifts = []
                for k in k_band:
                    fp = propagate_two_scale(positions, adj, free_f, setup["src"], setup["det"], k,
                                           set(), set(), n_bins)
                    mp = propagate_two_scale(positions, adj, setup["field"], setup["src"], setup["det"], k,
                                           setup["mass_set"], setup["blocked"], n_bins)
                    # Centroid from partial-traced probs
                    fp_probs = defaultdict(float)
                    for (d, env), amp in fp.items():
                        fp_probs[d] += abs(amp)**2
                    mp_probs = defaultdict(float)
                    for (d, env), amp in mp.items():
                        mp_probs[d] += abs(amp)**2
                    tf = sum(fp_probs.values())
                    tm = sum(mp_probs.values())
                    if tf > 0:
                        fp_probs = {d: p/tf for d, p in fp_probs.items()}
                    if tm > 0:
                        mp_probs = {d: p/tm for d, p in mp_probs.items()}
                    fy = sum(positions[d][1]*p for d, p in fp_probs.items())
                    my = sum(positions[d][1]*p for d, p in mp_probs.items())
                    ts_shifts.append(my - fy)

                # Beam width
                fp0 = pathsum_coherent(positions, adj, free_f, setup["src"], setup["det"], 5.0)
                total = sum(fp0.values())
                width = 1.0
                if total > 0:
                    mean = sum(positions[d][1]*p for d, p in fp0.items())/total
                    var = sum(positions[d][1]**2*p for d, p in fp0.items())/total - mean**2
                    width = max(var**0.5, 0.1)

                rg_std.append(sum(std_shifts)/len(std_shifts)/width)
                rg_g2.append(sum(g2_shifts)/len(g2_shifts)/width)
                rg_2s.append(sum(ts_shifts)/len(ts_shifts)/width)

                # Two-scale purity
                pf_k, p2s_k = [], []
                for k in k_band:
                    from scripts.density_matrix_analysis import propagate_two_register_full
                    ds_f = propagate_two_register_full(
                        positions, adj, setup["field"], setup["src"], setup["det"], k,
                        setup["mass_set"], setup["blocked"])
                    pf, _, _, _ = compute_detector_metrics(ds_f, setup["det_list"])
                    if not math.isnan(pf):
                        pf_k.append(pf)

                    ds_2s = propagate_two_scale(
                        positions, adj, setup["field"], setup["src"], setup["det"], k,
                        setup["mass_set"], setup["blocked"], n_bins)
                    p2s, _, _, _ = compute_detector_metrics(ds_2s, setup["det_list"])
                    if not math.isnan(p2s):
                        p2s_k.append(p2s)

                    envs = set(env for (d, env) in ds_2s.keys())
                    max_envs = max(max_envs, len(envs))

                if pf_k:
                    pf_list.append(sum(pf_k)/len(pf_k))
                if p2s_k:
                    p2s_list.append(sum(p2s_k)/len(p2s_k))

            if rg_std:
                avg_rg_std = sum(rg_std) / len(rg_std)
                avg_rg_g2 = sum(rg_g2) / len(rg_g2)
                avg_rg_2s = sum(rg_2s) / len(rg_2s)
                avg_pf = sum(pf_list) / len(pf_list)
                avg_p2s = sum(p2s_list) / len(p2s_list)
                rows[nl] = {
                    "rg_std": avg_rg_std,
                    "rg_g2": avg_rg_g2,
                    "rg_2s": avg_rg_2s,
                    "pur_fine": avg_pf,
                    "pur_2s": avg_p2s,
                }
                print(f"    {nl:4d}  {avg_rg_std:+7.3f}  "
                      f"{avg_rg_g2:+7.3f}  "
                      f"{avg_rg_2s:+7.3f}  "
                      f"{avg_pf:8.4f}  "
                      f"{avg_p2s:8.4f}  "
                      f"{max_envs:5d}")

        print()
        tested_bins.append(n_bins)
        if 12 in rows and 25 in rows:
            grav_pass = rows[25]["rg_2s"] >= rows[12]["rg_2s"]
            deco_pass = rows[25]["pur_2s"] <= rows[12]["pur_2s"]
            if grav_pass and deco_pass:
                passing_bins.append(n_bins)
                print(
                    "    verdict: PASS — gravity stays stable and purity does not rise"
                )
            else:
                print(
                    "    verdict: FAIL — "
                    f"R_2s(12)={rows[12]['rg_2s']:+.3f}, "
                    f"R_2s(25)={rows[25]['rg_2s']:+.3f}; "
                    f"pur_2s(12)={rows[12]['pur_2s']:.4f}, "
                    f"pur_2s(25)={rows[25]['pur_2s']:.4f}"
                )
            print()

    if passing_bins:
        print(
            "PASS: found a two-scale configuration with stable gravity and "
            "non-rising purity"
        )
    elif tested_bins:
        print(
            "FAIL: no tested two-scale configuration keeps gravity stable and "
            "purity non-increasing"
        )
    else:
        print("FAIL: no complete two-scale benchmark rows were produced")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
