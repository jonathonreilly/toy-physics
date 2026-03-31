#!/usr/bin/env python3
"""Fixed-bin cumulative phase environment.

The discrete node-label env weakens with graph size because both slits
reach all mass nodes. Here we test a genuinely fixed-bin cumulative phase
register rather than an ever-growing label.

Each path accumulates action_at_mass = Σ S(edge) for edges at mass nodes.
Paths from different slits accumulate different total action (different
routes through mass) → different binned env labels → decoherence.

This is still a discretized detector-conditioned purity test, but now the
environment state space remains fixed at `n_bins`.

PStack experiment: cumulative-phase-env
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
    compute_detector_metrics,
    build_post_barrier_setup,
)


def propagate_cumulative_env(positions, adj, field, src, det, k, mass_set,
                             blocked=None, n_bins=8):
    """Two-register with fixed-bin cumulative phase at mass interactions."""
    n = len(positions)
    blocked = blocked or set()

    in_deg = [0]*n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    # State: (node, env_bin) → amplitude with env_bin in [0, n_bins).
    state = {}
    for s in src:
        state[(s, 0)] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {env: amp for (node, env), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for env_bin, amp in entries.items():
            for j in adj.get(i, []):
                if j in blocked:
                    continue
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

                # Fixed-bin cumulative env: update the phase register modulo 2π
                if i in mass_set or j in mass_set:
                    current_phase = env_bin * 2 * math.pi / n_bins
                    new_phase = current_phase + act
                    new_bin = int((new_phase % (2 * math.pi)) * n_bins / (2 * math.pi))
                else:
                    new_bin = env_bin

                key = (j, new_bin)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    # Partial trace
    det_state = {(d, env): amp for (d, env), amp in state.items() if d in det}
    return det_state


def main():
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 8
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("FIXED-BIN CUMULATIVE PHASE ENVIRONMENT: purity vs graph size")
    print("  compares node-label vs fixed-bin cumulative env with scaled env depth")
    print("=" * 70)
    print()

    print(
        f"  {'n_layers':>8s}  {'depth':>5s}  "
        f"{'pur_node':>8s}  {'hit_node':>8s}  {'pur_cum':>8s}  {'hit_cum':>8s}  {'n_valid':>7s}"
    )
    print(f"  {'-' * 68}")

    for n_layers in [6, 8, 10, 12, 15, 18, 20, 25]:
        pur_node_list = []
        hit_node_list = []
        pur_cum_list = []
        hit_cum_list = []
        scaled_depth = max(1, round(n_layers / 6))

        for seed in range(n_seeds):
            positions, adj, _ = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius,
                rng_seed=seed*11+7,
            )
            setup = build_post_barrier_setup(positions, adj, env_depth_layers=scaled_depth)
            if setup is None:
                continue

            # Node-label env (original)
            from scripts.density_matrix_analysis import propagate_two_register_full
            node_purs = []
            node_hits = []
            cum_purs = []
            cum_hits = []

            for k in k_band:
                # Node-label
                ds_node = propagate_two_register_full(
                    positions, adj, setup["field"], setup["src"], setup["det"], k,
                    setup["mass_set"], setup["blocked"])
                p_node, _, _, hit_node = compute_detector_metrics(ds_node, setup["det_list"])
                node_purs.append(p_node)
                node_hits.append(hit_node)

                # Cumulative
                ds_cum = propagate_cumulative_env(
                    positions, adj, setup["field"], setup["src"], setup["det"], k,
                    setup["mass_set"], setup["blocked"], n_bins=8)
                p_cum, _, _, hit_cum = compute_detector_metrics(ds_cum, setup["det_list"])
                cum_purs.append(p_cum)
                cum_hits.append(hit_cum)

            pur_node_list.append(sum(node_purs)/len(node_purs))
            hit_node_list.append(sum(node_hits)/len(node_hits))
            pur_cum_list.append(sum(cum_purs)/len(cum_purs))
            hit_cum_list.append(sum(cum_hits)/len(cum_hits))

        if pur_node_list:
            mn = sum(pur_node_list)/len(pur_node_list)
            hn = sum(hit_node_list)/len(hit_node_list)
            mc = sum(pur_cum_list)/len(pur_cum_list)
            hc = sum(hit_cum_list)/len(hit_cum_list)
            print(f"  {n_layers:8d}  {scaled_depth:5d}  {mn:8.4f}  {hn:8.4f}  {mc:8.4f}  {hc:8.4f}  {len(pur_node_list):7d}")

    print()
    print("pur_* = detector-state purity conditioned on detector hits")
    print("hit_* = detector hit probability before conditioning")
    print("env depth scales ~ n_layers/6 to avoid simple env-region dilution")
    print()
    print("If pur_cum decreases with n_layers: fixed-bin cumulative env fixes scaling")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
