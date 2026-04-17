#!/usr/bin/env python3
"""Qubit-per-mass-node decoherence.

Each mass node is a qubit that starts in |0⟩. When amplitude crosses
an edge touching mass node m, qubit m flips: |0⟩→|1⟩ (or stays |1⟩).

The env state is a frozenset of flipped qubits. The env dimension
is 2^M where M = number of mass nodes. Different paths flip different
subsets → exponentially many env states → decoherence.

Key property: as M grows with graph size, the env dimension grows
exponentially, matching path multiplicity growth.

The partial trace at the detector:
  P(det) = Σ_{qubit_config} |ψ(det, config)|²

Uses the promoted angle² β=0.8 propagator.

PStack experiment: qubit-env-decoherence
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


def propagate_qubit_env(positions, adj, field, src, det, k,
                        mass_set, blocked=None):
    """Angle-weighted propagator with qubit-per-mass-node environment.

    State: (node, flipped_qubits_frozenset) → amplitude
    When amplitude crosses mass node m: m is added to the flipped set.
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

    # State: (node, frozenset_of_flipped_qubits) → amplitude
    state = {}
    for s in src:
        state[(s, frozenset())] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {qubits: amp for (node, qubits), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for qubits, amp in entries.items():
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
                theta = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA*theta*theta)
                ea = cmath.exp(1j*k*act) * w / (L**1.0)

                # Qubit flip: if destination is mass, add it to flipped set
                if j in mass_set:
                    new_qubits = qubits | frozenset([j])
                else:
                    new_qubits = qubits

                key = (j, new_qubits)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    det_state = {(d, qubits): amp for (d, qubits), amp in state.items()
                 if d in det}
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("QUBIT-PER-MASS-NODE DECOHERENCE")
    print(f"  Env = 2^M qubit configs, angle² β={BETA}")
    print("=" * 70)
    print()

    print(f"  {'N':>4s}  {'n_mass':>6s}  {'2^M':>8s}  {'n_env':>6s}  "
          f"{'purity':>8s}  {'pur_node':>8s}")
    print(f"  {'-' * 46}")

    for nl in [8, 10, 12, 15, 18]:
        purities_q, purities_n = [], []
        n_mass_count = 0
        max_envs = 0

        for seed in range(4):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_set = set(setup["mass_set"]) - setup["blocked"]
            n_mass_count = len(mass_set)

            # Cap mass size to prevent 2^M explosion
            if n_mass_count > 15:
                # Take only the first 15 mass nodes
                mass_set = set(sorted(mass_set)[:15])
                n_mass_count = 15

            for k in k_band:
                # Qubit env
                ds_q = propagate_qubit_env(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, setup["blocked"])
                pq, _, _, _ = compute_detector_metrics(ds_q, setup["det_list"])
                if not math.isnan(pq):
                    purities_q.append(pq)

                envs = set(qubits for (d, qubits) in ds_q.keys())
                max_envs = max(max_envs, len(envs))

                # Node-label env for comparison (inline)
                state_n = {}
                for s in setup["src"]:
                    state_n[(s, -1)] = 1.0/len(setup["src"]) + 0.0j
                processed = set()
                n = len(positions)
                in_deg = [0]*n
                for i, nbs in adj.items():
                    for j in nbs:
                        in_deg[j] += 1
                q_order = deque(i for i in range(n) if in_deg[i] == 0)
                order = []
                while q_order:
                    i = q_order.popleft()
                    order.append(i)
                    for j in adj.get(i, []):
                        in_deg[j] -= 1
                        if in_deg[j] == 0:
                            q_order.append(j)

                for i in order:
                    if i in processed: continue
                    processed.add(i)
                    entries = {env: amp for (node, env), amp in list(state_n.items())
                               if node == i and abs(amp) > 1e-30}
                    if not entries or i in setup["blocked"]: continue
                    for env, amp in entries.items():
                        new_env = i if i in mass_set else env
                        for j in adj.get(i, []):
                            if j in setup["blocked"]: continue
                            x1,y1 = positions[i]; x2,y2 = positions[j]
                            dx=x2-x1; dy=y2-y1
                            L = math.sqrt(dx*dx+dy*dy)
                            if L < 1e-10: continue
                            lf = 0.5*(setup["field"][i]+setup["field"][j])
                            dl=L*(1+lf); ret=math.sqrt(max(dl*dl-L*L,0)); act=dl-ret
                            theta_e = math.atan2(abs(dy), max(dx, 1e-10))
                            w = math.exp(-BETA*theta_e*theta_e)
                            ea = cmath.exp(1j*k*act)*w/(L**1.0)
                            key = (j, new_env)
                            if key not in state_n: state_n[key] = 0.0+0.0j
                            state_n[key] += amp*ea

                ds_n = {(d, env): amp for (d, env), amp in state_n.items()
                        if d in setup["det"]}
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    purities_n.append(pn)

        if purities_q:
            two_m = 2**min(n_mass_count, 15)
            print(f"  {nl:4d}  {n_mass_count:6d}  {two_m:8d}  {max_envs:6d}  "
                  f"{sum(purities_q)/len(purities_q):8.4f}  "
                  f"{sum(purities_n)/len(purities_n):8.4f}")

    print()
    print("purity = qubit env, pur_node = node-label env (comparison)")
    print("n_env = actual env states populated at detector")
    print()
    print("PASS: purity decreases or stays stable with N")
    print("FAIL: purity increases with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
