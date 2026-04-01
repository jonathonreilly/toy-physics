#!/usr/bin/env python3
"""Directional record decoherence: env tracks angle of transit through mass.

Previous env architectures tracked WHICH mass node was visited (node
labels, edge hashes). These fail because both slits reach the same
nodes on dense graphs.

New idea: track the DIRECTION of transit through mass. Different slits
approach mass from different angles. The record captures this angle,
making env states more slit-discriminating.

Implementation: at each mass edge, the env accumulates a directional
hash based on the edge's angle bin (not the node identity). The env
state is a tuple of recent angle-bin transitions.

This combines the directional measure insight (angle is the key
discriminator) with the record/environment architecture.

Uses the promoted angle² β=0.8 propagator.

PStack experiment: directional-record-decoherence
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import build_post_barrier_setup, compute_detector_metrics

BETA = 0.8
N_ANGLE_BINS = 4  # coarse directional sectors


def angle_bin(dy, dx, n_bins=N_ANGLE_BINS):
    """Bin the edge angle into n_bins sectors."""
    theta = math.atan2(dy, max(dx, 1e-10))
    # Map [-π, π] to [0, n_bins)
    return int(((theta + math.pi) / (2 * math.pi)) * n_bins) % n_bins


def propagate_directional_record(positions, adj, field, src, det, k,
                                  mass_set, blocked=None, max_records=2):
    """Angle-weighted propagator with directional env records.

    At mass edges, the env records the angle bin of the edge.
    The env state is a tuple of the last max_records angle bins.
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

    state = {}
    for s in src:
        state[(s, ())] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {rec: amp for (node, rec), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for rec, amp in entries.items():
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                dx = x2-x1
                dy = y2-y1
                L = math.sqrt(dx*dx+dy*dy)
                if L < 1e-10:
                    continue
                lf = 0.5*(field[i]+field[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret

                # Angle weight (directional measure)
                theta = math.atan2(abs(dy), max(dx, 1e-10))
                weight = math.exp(-BETA*theta*theta)
                ea = cmath.exp(1j*k*act) * weight / (L**1.0)

                # Directional record at mass edges
                if i in mass_set or j in mass_set:
                    ab = angle_bin(dy, dx)
                    new_rec = (rec + (ab,))[-max_records:]
                else:
                    new_rec = rec

                key = (j, new_rec)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    det_state = {(d, rec): amp for (d, rec), amp in state.items() if d in det}
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("DIRECTIONAL RECORD DECOHERENCE")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Env: last {2} angle-bin transitions at mass edges")
    print(f"  {N_ANGLE_BINS} angle sectors")
    print("=" * 70)
    print()

    # Compare: node-label env vs directional-record env
    print("DECOHERENCE SCALING: node-label vs directional record")
    print()
    print(f"  {'N':>4s}  {'pur_node':>8s}  {'pur_dir':>8s}  {'n_node':>6s}  {'n_dir':>6s}")
    print(f"  {'-' * 38}")

    for nl in [8, 12, 18, 25]:
        pn_list, pd_list = [], []
        max_node_envs, max_dir_envs = 0, 0

        for seed in range(4):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_set = set(setup["mass_set"]) - setup["blocked"]

            for k in k_band:
                # Node-label env with angle weight
                n = len(positions)
                blocked = setup["blocked"]
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

                state_n = {}
                for s in setup["src"]:
                    state_n[(s, -1)] = 1.0/len(setup["src"]) + 0.0j
                processed = set()
                for i in order:
                    if i in processed: continue
                    processed.add(i)
                    entries = {env: amp for (node, env), amp in list(state_n.items())
                               if node == i and abs(amp) > 1e-30}
                    if not entries or i in blocked: continue
                    for env, amp in entries.items():
                        new_env = i if i in mass_set else env
                        for j in adj.get(i, []):
                            if j in blocked: continue
                            x1,y1 = positions[i]; x2,y2 = positions[j]
                            dx=x2-x1; dy=y2-y1
                            L = math.sqrt(dx*dx+dy*dy)
                            if L < 1e-10: continue
                            lf = 0.5*(setup["field"][i]+setup["field"][j])
                            dl=L*(1+lf); ret=math.sqrt(max(dl*dl-L*L,0)); act=dl-ret
                            theta = math.atan2(abs(dy), max(dx, 1e-10))
                            w = math.exp(-BETA*theta*theta)
                            ea = cmath.exp(1j*k*act)*w/(L**1.0)
                            key = (j, new_env)
                            if key not in state_n: state_n[key] = 0.0+0.0j
                            state_n[key] += amp*ea

                ds_n = {(d, env): amp for (d, env), amp in state_n.items() if d in setup["det"]}
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)
                max_node_envs = max(max_node_envs, len(set(env for (d, env) in ds_n.keys())))

                # Directional record env
                ds_d = propagate_directional_record(
                    positions, adj, setup["field"], setup["src"], setup["det"], k,
                    mass_set, setup["blocked"])
                pd, _, _, _ = compute_detector_metrics(ds_d, setup["det_list"])
                if not math.isnan(pd):
                    pd_list.append(pd)
                max_dir_envs = max(max_dir_envs, len(set(rec for (d, rec) in ds_d.keys())))

        if pn_list and pd_list:
            print(f"  {nl:4d}  {sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(pd_list)/len(pd_list):8.4f}  "
                  f"{max_node_envs:6d}  {max_dir_envs:6d}")

    print()
    print("If pur_dir < pur_node: directional records are more slit-discriminating")
    print("If pur_dir stable with N: directional records fix scaling")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
