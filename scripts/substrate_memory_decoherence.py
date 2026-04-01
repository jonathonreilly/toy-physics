#!/usr/bin/env python3
"""True substrate memory: records modify the graph for later propagation.

When amplitude first arrives at mass node m, it splits:
  cos(α): no record (env unchanged, propagation unchanged)
  sin(α): record created (env marks m, subsequent edges at m get phase kick)

The key difference: in the "record=1" branch, ALL subsequent amplitude
arriving at m gets an extra phase factor exp(i×φ_kick). This makes the
propagation history-dependent — later paths through m see different
physics depending on whether earlier paths created a record.

This breaks the symmetry between early and late paths, and between
paths that create records at different nodes. On larger graphs with
more mass nodes, more record sites → more history-dependent divergence.

The trace over record configurations gives decoherence.

Uses the promoted angle² β=0.8 propagator.

PStack experiment: substrate-memory-decoherence
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
ALPHA = math.pi / 4    # splitting angle
PHI_KICK = math.pi / 3  # phase kick from existing record


def propagate_substrate_memory(positions, adj, field, src, det, k,
                               mass_set, alpha, phi_kick, blocked=None):
    """Propagator with true substrate memory at mass nodes.

    State: (node, recorded_frozenset) → amplitude
    recorded_frozenset = set of mass nodes where a record exists.

    At mass node j (destination):
      If j NOT in recorded set:
        SPLIT: cos(α) × amp (no record) + sin(α) × amp (create record at j)

    At any node i that IS in recorded set (source):
      Apply phase kick exp(i×φ_kick) to ALL outgoing edges from i.
      This makes later propagation FROM recorded nodes history-dependent.

    On forward DAGs, nodes are never revisited. The kick fires on edges
    LEAVING recorded nodes, which happens when later-layer paths pass
    through a node that was recorded by earlier-layer paths in a
    different env branch.
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

    cos_a = math.cos(alpha)
    sin_a = math.sin(alpha)
    kick = cmath.exp(1j * phi_kick)

    # Diagnostic counters
    kick_count = [0]
    total_mass_trans = [0]

    state = {}
    for s in src:
        state[(s, frozenset())] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {rec: amp for (node, rec), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for recorded, amp in entries.items():
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

                # History-dependent kick: if SOURCE node i is recorded,
                # apply phase kick to this outgoing edge
                if i in recorded:
                    ea = ea * kick
                    kick_count[0] += 1
                total_mass_trans[0] += 1 if (i in mass_set or j in mass_set) else 0

                if j in mass_set and alpha > 0 and j not in recorded:
                    # Unrecorded mass destination: SPLIT
                    # Branch 0: no record, env unchanged
                    key_0 = (j, recorded)
                    if key_0 not in state:
                        state[key_0] = 0.0+0.0j
                    state[key_0] += amp * ea * cos_a

                    # Branch 1: create record at j
                    rec_1 = recorded | frozenset([j])
                    key_1 = (j, rec_1)
                    if key_1 not in state:
                        state[key_1] = 0.0+0.0j
                    state[key_1] += amp * ea * sin_a
                else:
                    key = (j, recorded)
                    if key not in state:
                        state[key] = 0.0+0.0j
                    state[key] += amp * ea

    det_state = {(d, rec): amp for (d, rec), amp in state.items() if d in det}
    return det_state, kick_count[0], total_mass_trans[0]


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("SUBSTRATE MEMORY DECOHERENCE")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Split: cos({ALPHA:.2f})/sin({ALPHA:.2f}) at unrecorded mass")
    print(f"  Kick: exp(i×{PHI_KICK:.2f}) at recorded mass")
    print("=" * 70)
    print()

    print(f"  {'N':>4s}  {'n_mass':>6s}  {'n_env':>6s}  {'kicks':>6s}  "
          f"{'pur_sub':>8s}  {'pur_node':>8s}  {'sub_off':>8s}")
    print(f"  {'-' * 56}")

    for nl in [8, 12, 18]:
        ps_list, pn_list, p0_list = [], [], []
        n_mass_count = 0
        max_envs = 0
        total_kicks = 0

        for seed in range(3):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_set = set(setup["mass_set"]) - setup["blocked"]
            n_mass_count = len(mass_set)
            if n_mass_count > 12:
                mass_set = set(sorted(mass_set)[:12])

            for k in k_band:
                # Substrate memory
                ds_s, n_kicks, n_mass_trans = propagate_substrate_memory(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, ALPHA, PHI_KICK, setup["blocked"])
                ps, _, _, _ = compute_detector_metrics(ds_s, setup["det_list"])
                if not math.isnan(ps):
                    ps_list.append(ps)
                envs = set(rec for (d, rec) in ds_s.keys())
                max_envs = max(max_envs, len(envs))
                total_kicks += n_kicks

                # Node-label (comparison — use SAME capped mass_set)
                from scripts.density_matrix_analysis import propagate_two_register_full
                ds_n = propagate_two_register_full(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, setup["blocked"])
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)

                # Off baseline (α=0)
                ds_0, _, _ = propagate_substrate_memory(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, 0.0, 0.0, setup["blocked"])
                p0, _, _, _ = compute_detector_metrics(ds_0, setup["det_list"])
                if not math.isnan(p0):
                    p0_list.append(p0)

        if ps_list:
            print(f"  {nl:4d}  {n_mass_count:6d}  {max_envs:6d}  {total_kicks:6d}  "
                  f"{sum(ps_list)/len(ps_list):8.4f}  "
                  f"{sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(p0_list)/len(p0_list):8.4f}")

    print()
    print("pur_sub = substrate memory (this test)")
    print("pur_node = node-label env (comparison)")
    print("sub_off = α=0 (should be ~1.0, unitary baseline)")
    print()
    print("PASS: pur_sub does not rise with N")
    print("FAIL: pur_sub rises with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
