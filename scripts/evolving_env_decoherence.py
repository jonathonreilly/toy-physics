#!/usr/bin/env python3
"""Discretized evolving phase-bin environment.

The scaling problem: passive env labels (node-label, cumulative) become
shared as graphs grow. Here we test a discretized evolving phase register
that updates at every edge and is re-binned after each step.

Between mass nodes, the env state picks up phase from the local graph
structure. Different paths between mass nodes → different env phases →
env states become more orthogonal on larger graphs.

Implementation: env is an underlying phase variable represented by a
discrete phase bin.
At each edge, env_phase += edge_action * coupling_strength.
At mass nodes, the env is "measured" (binned into discrete labels).
Between mass nodes, the env evolves freely before being re-quantized.

The partial trace bins by the final env phase.

PStack experiment: evolving-env-decoherence
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


def propagate_evolving_env(positions, adj, field, src, det, k, mass_set,
                           blocked=None, env_coupling=0.5, n_bins=12):
    """Two-register with discretized evolving environment phase.

    The env accumulates phase at EVERY edge (not just mass edges).
    At mass edges, the coupling is stronger (env_coupling).
    At non-mass edges, the coupling is weaker (env_coupling * 0.1).
    The env phase is binned at the detector for the partial trace.
    """
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

    # State: (node, env_phase_bin) → amplitude
    state = {}
    for s in src:
        state[(s, 0)] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {env_bin: amp for (node, env_bin), amp in list(state.items())
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

                # Env phase evolution: stronger at mass, weaker elsewhere
                if i in mass_set or j in mass_set:
                    env_delta = act * env_coupling
                else:
                    env_delta = act * env_coupling * 0.1

                # Convert continuous env phase to bin
                new_phase = (env_bin * 2 * math.pi / n_bins) + env_delta
                new_bin = int((new_phase % (2 * math.pi)) * n_bins / (2 * math.pi))

                key = (j, new_bin)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    det_state = {(d, env): amp for (d, env), amp in state.items() if d in det}
    return det_state


def main():
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 8
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("DISCRETIZED EVOLVING ENVIRONMENT: purity vs graph size")
    print("  12-bin phase register accumulates phase at every edge")
    print("  env depth scales ~ n_layers/6 to avoid simple env-region dilution")
    print("=" * 70)
    print()

    for coupling in [0.1, 0.5, 1.0]:
        print(f"  env_coupling = {coupling}:")
        print(f"    {'n_layers':>8s}  {'depth':>5s}  {'pur_node':>8s}  {'hit_node':>8s}  {'pur_evol':>8s}  {'hit_evol':>8s}  {'n_valid':>7s}")
        print(f"    {'-' * 69}")

        for n_layers in [6, 8, 10, 12, 15, 20, 25]:
            pur_node_list = []
            hit_node_list = []
            pur_evol_list = []
            hit_evol_list = []
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

                from scripts.density_matrix_analysis import propagate_two_register_full
                node_purs = []
                node_hits = []
                evol_purs = []
                evol_hits = []

                for k_val in k_band:
                    ds_node = propagate_two_register_full(
                        positions, adj, setup["field"], setup["src"], setup["det"], k_val,
                        setup["mass_set"], setup["blocked"])
                    p_node, _, _, hit_node = compute_detector_metrics(ds_node, setup["det_list"])
                    node_purs.append(p_node)
                    node_hits.append(hit_node)

                    ds_evol = propagate_evolving_env(
                        positions, adj, setup["field"], setup["src"], setup["det"], k_val,
                        setup["mass_set"], setup["blocked"], coupling, n_bins=12)
                    p_evol, _, _, hit_evol = compute_detector_metrics(ds_evol, setup["det_list"])
                    evol_purs.append(p_evol)
                    evol_hits.append(hit_evol)

                pur_node_list.append(sum(node_purs)/len(node_purs))
                hit_node_list.append(sum(node_hits)/len(node_hits))
                pur_evol_list.append(sum(evol_purs)/len(evol_purs))
                hit_evol_list.append(sum(evol_hits)/len(evol_hits))

            if pur_node_list:
                mn = sum(pur_node_list)/len(pur_node_list)
                hn = sum(hit_node_list)/len(hit_node_list)
                me = sum(pur_evol_list)/len(pur_evol_list)
                he = sum(hit_evol_list)/len(hit_evol_list)
                print(f"    {n_layers:8d}  {scaled_depth:5d}  {mn:8.4f}  {hn:8.4f}  {me:8.4f}  {he:8.4f}  {len(pur_node_list):7d}")

        # Check trend
        print()

    print("pur_* = detector-state purity conditioned on detector hits")
    print("hit_* = detector hit probability before conditioning")
    print("If pur_evol DECREASES with n_layers: this discretized evolving env fixes scaling")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
