#!/usr/bin/env python3
"""D1: Multi-local tensor environment for decoherence scaling.

Instead of one global env label (last mass node), divide the mass
region into M spatial cells. Each cell has its own local env register.
The full env state is the tuple (env_cell_1, env_cell_2, ..., env_cell_M).

Paths through different cell configurations get different env tuples.
The env dimension grows as d^M (exponential in M), matching path
multiplicity growth.

Implementation: mass region is divided into y-bins. Each y-bin is an
independent env cell. At each cell, the env register records which
mass node was last visited in THAT cell. The full env is the tuple
of per-cell labels.

Pass criterion: purity should NOT increase from N=12 to N=25.

PStack experiment: d1-multilocal-tensor-env
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


def propagate_multilocal_env(positions, adj, field, src, det, k, mass_set,
                              blocked=None, n_cells=3, mass_y_range=None):
    """Two-register with multi-local tensor environment.

    The mass region is divided into n_cells y-bins. Each cell has its own
    env register. The full env state is a tuple of per-cell labels.
    """
    n = len(positions)
    blocked = blocked or set()

    # Determine mass y-range for cell binning
    if mass_y_range is None:
        mass_ys = [positions[m][1] for m in mass_set]
        if not mass_ys:
            mass_y_range = (-6, 6)
        else:
            mass_y_range = (min(mass_ys) - 0.5, max(mass_ys) + 0.5)

    y_min, y_max = mass_y_range
    cell_width = (y_max - y_min) / n_cells if n_cells > 0 else 1

    def get_cell(y):
        return min(int((y - y_min) / cell_width), n_cells - 1)

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

    # State: (node, env_tuple) → amplitude
    # env_tuple = (cell_0_label, cell_1_label, ..., cell_M-1_label)
    init_env = tuple([-1] * n_cells)
    state = {}
    for s in src:
        state[(s, init_env)] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)

        entries = {env: amp for (node, env), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for env_tuple, amp in entries.items():
            # If this is a mass node, update the corresponding cell's env
            if i in mass_set:
                cell_idx = get_cell(positions[i][1])
                cell_idx = max(0, min(cell_idx, n_cells - 1))
                new_env = list(env_tuple)
                new_env[cell_idx] = i  # record this mass node in its cell
                new_env = tuple(new_env)
            else:
                new_env = env_tuple

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

                key = (j, new_env)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    # Partial trace: P(det) = Σ_env |ψ(det,env)|²
    det_state = {(d, env): amp for (d, env), amp in state.items() if d in det}
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("D1: MULTI-LOCAL TENSOR ENVIRONMENT")
    print("  Mass region divided into cells, each with own env register")
    print("=" * 70)
    print()

    # Pass: purity at N=25 <= purity at N=12
    for n_cells in [2, 3, 4, 6]:
        print(f"  n_cells = {n_cells}:")
        print(f"    {'N_layers':>8s}  {'pur_fine':>8s}  {'pur_tensor':>10s}  {'n_envs':>6s}")
        print(f"    {'-' * 38}")

        for nl in [8, 10, 12, 15, 20, 25]:
            pur_fine, pur_tensor = [], []

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

                pf_k, pt_k = [], []
                n_env_states = 0
                for k in k_band:
                    # Fine env (baseline)
                    from scripts.density_matrix_analysis import propagate_two_register_full
                    ds_f = propagate_two_register_full(
                        positions, adj, setup["field"], setup["src"], setup["det"], k,
                        setup["mass_set"], setup["blocked"])
                    pf, _, _, _ = compute_detector_metrics(ds_f, setup["det_list"])
                    if not math.isnan(pf):
                        pf_k.append(pf)

                    # Multi-local tensor env
                    ds_t = propagate_multilocal_env(
                        positions, adj, setup["field"], setup["src"], setup["det"], k,
                        setup["mass_set"], setup["blocked"], n_cells)
                    pt, _, _, _ = compute_detector_metrics(ds_t, setup["det_list"])
                    if not math.isnan(pt):
                        pt_k.append(pt)

                    # Count unique env states
                    envs = set(env for (d, env) in ds_t.keys())
                    n_env_states = max(n_env_states, len(envs))

                if pf_k:
                    pur_fine.append(sum(pf_k)/len(pf_k))
                if pt_k:
                    pur_tensor.append(sum(pt_k)/len(pt_k))

            if pur_fine and pur_tensor:
                print(f"    {nl:8d}  {sum(pur_fine)/len(pur_fine):8.4f}  "
                      f"{sum(pur_tensor)/len(pur_tensor):10.4f}  {n_env_states:6d}")

        print()

    # Pass/fail summary
    print("PASS: pur_tensor at N=25 <= pur_tensor at N=12")
    print("FAIL: pur_tensor increases with N (like fine env)")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
