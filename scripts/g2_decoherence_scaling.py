#!/usr/bin/env python3
"""Does G2 (coarse-grained propagator) also fix decoherence scaling?

G2 passes gravity scaling by reducing effective path multiplicity.
Path multiplicity is also the root cause of decoherence failure.
If G2 reduces path multiplicity enough, the env labels should become
more slit-discriminating → purity should stop increasing with N.

Implementation: use coarse-grained propagator with two-register env.
The env labels paths by which y-bin they exit the mass region through.
With fewer effective paths (coarse bins), the labels should be more
slit-selective.

Pass criterion: purity should NOT increase from N=12 to N=25.

PStack experiment: g2-decoherence-scaling
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
from scripts.two_register_decoherence import compute_field


def propagate_g2_with_env(positions, adj, field, src, det, k, mass_set,
                          blocked=None, n_ybins=8):
    """G2 coarse-grained propagator with two-register env.

    Combines: y-bin coarse graining (G2) + fine env at mass nodes.
    Amplitude propagates between y-bins. At mass bins, env is updated.
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

    # State: (layer_idx, y_bin, env_label) → amplitude
    state = defaultdict(complex)
    for s in src:
        yb = y_bin(positions[s][1])
        state[(0, yb, -1)] += 1.0 / len(src)

    for li in range(len(layers) - 1):
        curr_layer = layers[li]
        next_layer = layers[li + 1]
        curr_nodes = by_layer[curr_layer]
        next_nodes = set(by_layer[next_layer])

        curr_bins = defaultdict(list)
        for i in curr_nodes:
            if i not in blocked:
                curr_bins[y_bin(positions[i][1])].append(i)

        next_bins = defaultdict(list)
        for j in by_layer[next_layer]:
            if j not in blocked:
                next_bins[y_bin(positions[j][1])].append(j)

        new_state = defaultdict(complex)

        for cb, cb_nodes in curr_bins.items():
            # Collect all env states at this bin
            env_amps = defaultdict(complex)
            for env_label in set(env for (l, b, env) in state if l == li and b == cb):
                amp = state.get((li, cb, env_label), 0.0)
                if abs(amp) > 1e-30:
                    env_amps[env_label] = amp

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
                    # Track whether destination is mass
                    is_mass_edge = j in mass_set
                    dest_edges[nb].append((ea, j, is_mass_edge))

            for env_label, amp in env_amps.items():
                for nb, edges in dest_edges.items():
                    # Average edge amplitude within bundle
                    avg_ea = sum(ea for ea, _, _ in edges) / len(edges)

                    # Update env: if any edge in bundle goes to mass node
                    any_mass = any(is_m for _, _, is_m in edges)
                    if any_mass:
                        # Use the most common mass node in the bundle as env
                        mass_nodes_in_bundle = [j for _, j, is_m in edges if is_m]
                        if mass_nodes_in_bundle:
                            new_env = mass_nodes_in_bundle[0]  # first mass node
                        else:
                            new_env = env_label
                    else:
                        new_env = env_label

                    new_state[(li+1, nb, new_env)] += amp * avg_ea

        state.update(new_state)

    # Collect at detector
    det_layer_idx = len(layers) - 1
    det_state = {}
    for d in det:
        yb = y_bin(positions[d][1])
        for (l, b, env), amp in state.items():
            if l == det_layer_idx and b == yb:
                key = (d, env)
                if key not in det_state:
                    det_state[key] = 0.0+0.0j
                det_state[key] += amp

    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("G2 + ENV: Does coarse-grained propagator fix decoherence scaling?")
    print("=" * 70)
    print()

    for n_bins in [6, 8, 12]:
        print(f"  n_ybins = {n_bins}:")
        print(f"    {'N_layers':>8s}  {'pur_fine':>8s}  {'pur_g2':>8s}  {'n_envs':>6s}")
        print(f"    {'-' * 36}")

        for nl in [8, 10, 12, 15, 20, 25]:
            pur_fine, pur_g2 = [], []
            max_envs = 0

            for seed in range(5):
                positions, adj, _ = generate_causal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed*11+7)
                scaled_depth = max(1, round(nl/6))
                setup = build_post_barrier_setup(positions, adj,
                                                  env_depth_layers=scaled_depth)
                if setup is None:
                    continue

                pf_k, pg_k = [], []
                for k in k_band:
                    # Fine env baseline
                    from scripts.density_matrix_analysis import propagate_two_register_full
                    ds_f = propagate_two_register_full(
                        positions, adj, setup["field"], setup["src"], setup["det"], k,
                        setup["mass_set"], setup["blocked"])
                    pf, _, _, _ = compute_detector_metrics(ds_f, setup["det_list"])
                    if not math.isnan(pf):
                        pf_k.append(pf)

                    # G2 + env
                    ds_g = propagate_g2_with_env(
                        positions, adj, setup["field"], setup["src"], setup["det"], k,
                        setup["mass_set"], setup["blocked"], n_bins)
                    pg, _, _, _ = compute_detector_metrics(ds_g, setup["det_list"])
                    if not math.isnan(pg):
                        pg_k.append(pg)

                    envs = set(env for (d, env) in ds_g.keys())
                    max_envs = max(max_envs, len(envs))

                if pf_k:
                    pur_fine.append(sum(pf_k)/len(pf_k))
                if pg_k:
                    pur_g2.append(sum(pg_k)/len(pg_k))

            if pur_fine and pur_g2:
                print(f"    {nl:8d}  {sum(pur_fine)/len(pur_fine):8.4f}  "
                      f"{sum(pur_g2)/len(pur_g2):8.4f}  {max_envs:6d}")

        print()

    print("PASS: pur_g2 at N=25 <= pur_g2 at N=12")
    print("FAIL: pur_g2 increases with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
