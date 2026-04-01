#!/usr/bin/env python3
"""Topology-changing record: the record modifies local graph structure.

Previous architectures modify phase or amplitude at recorded nodes.
This one modifies the GRAPH: when a record is created at mass node m,
edges from m are rewired in the recorded branch. This creates genuinely
different propagation paths in different env branches.

Architecture:
- At mass node m (first visit): split cos(α)/sin(α)
  - Branch 0: graph unchanged
  - Branch 1: edges from m are REDIRECTED (rotated to different neighbors)
- Later propagation in branch 1 follows different paths than branch 0
- The trace over branches gives decoherence from path divergence

The key: topology change creates STRUCTURAL differences between
branches, not just phase differences. Different paths → different
detector distributions → decoherence.

Uses the promoted angle² β=0.8 propagator.

PStack experiment: topology-changing-record
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
ALPHA = math.pi / 4


def build_rewired_adj(adj, mass_node, positions, n):
    """Create a modified adjacency where edges FROM mass_node are rotated.

    For each outgoing edge (mass_node → j), redirect to a nearby node
    that is NOT the original target. This creates a structurally different
    graph in the recorded branch.
    """
    new_adj = {}
    for i, nbs in adj.items():
        if i == mass_node:
            # Rotate outgoing edges: shift each target by +1 in the
            # sorted neighbor list (cyclic)
            sorted_nbs = sorted(nbs)
            if len(sorted_nbs) > 1:
                rotated = sorted_nbs[1:] + sorted_nbs[:1]
                new_adj[i] = rotated
            else:
                new_adj[i] = list(nbs)
        else:
            new_adj[i] = list(nbs)
    return new_adj


def propagate_topology_record(positions, adj, field, src, det, k,
                              mass_set, alpha, blocked=None):
    """Propagator with topology-changing records at mass nodes.

    State: (node, recorded_frozenset, adj_version) → amplitude
    But tracking per-branch adjacency is expensive. Instead:
    precompute the two adjacency versions (original + per-mass-node
    rewired) and propagate on both, splitting at mass nodes.

    Simplified: for each mass node, precompute the rewired adj.
    At each mass node, branch 1 uses the rewired edges from that node.
    We track which mass nodes have been recorded (rewired) and use
    the appropriate edges.
    """
    n = len(positions)
    blocked = blocked or set()
    cos_a = math.cos(alpha)
    sin_a = math.sin(alpha)

    # Precompute rewired edges for each mass node
    rewired_edges = {}
    for m in mass_set:
        original = adj.get(m, [])
        sorted_nbs = sorted(original)
        if len(sorted_nbs) > 1:
            rewired_edges[m] = sorted_nbs[1:] + sorted_nbs[:1]
        else:
            rewired_edges[m] = list(original)

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
            # Determine which edges to use from this node
            if i in recorded and i in mass_set:
                # This node was recorded: use rewired edges
                neighbors = rewired_edges.get(i, adj.get(i, []))
            else:
                neighbors = adj.get(i, [])

            for j in neighbors:
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

                if j in mass_set and j not in recorded and alpha > 0:
                    # Split at unrecorded mass destination
                    key_0 = (j, recorded)
                    if key_0 not in state:
                        state[key_0] = 0.0+0.0j
                    state[key_0] += amp * ea * cos_a

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
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("TOPOLOGY-CHANGING RECORD")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Split: cos({ALPHA:.2f})/sin({ALPHA:.2f})")
    print(f"  Record: rewire outgoing edges at recorded mass nodes")
    print("=" * 70)
    print()

    print(f"  {'N':>4s}  {'n_mass':>6s}  {'n_env':>6s}  "
          f"{'pur_topo':>8s}  {'pur_node':>8s}  {'topo_off':>8s}")
    print(f"  {'-' * 48}")

    for nl in [8, 12, 18]:
        pt_list, pn_list, p0_list = [], [], []
        n_mass_count = 0
        max_envs = 0

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
                ds_t = propagate_topology_record(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, ALPHA, setup["blocked"])
                pt, _, _, _ = compute_detector_metrics(ds_t, setup["det_list"])
                if not math.isnan(pt):
                    pt_list.append(pt)
                envs = set(rec for (d, rec) in ds_t.keys())
                max_envs = max(max_envs, len(envs))

                from scripts.density_matrix_analysis import propagate_two_register_full
                ds_n = propagate_two_register_full(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, setup["blocked"])
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)

                ds_0 = propagate_topology_record(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, 0.0, setup["blocked"])
                p0, _, _, _ = compute_detector_metrics(ds_0, setup["det_list"])
                if not math.isnan(p0):
                    p0_list.append(p0)

        if pt_list:
            print(f"  {nl:4d}  {n_mass_count:6d}  {max_envs:6d}  "
                  f"{sum(pt_list)/len(pt_list):8.4f}  "
                  f"{sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(p0_list)/len(p0_list):8.4f}")

    print()
    print("pur_topo = topology-changing record (this test)")
    print("pur_node = node-label env (matched mass set)")
    print("topo_off = α=0 (should be ~1.0)")
    print()
    print("PASS: pur_topo does not rise with N")
    print("FAIL: pur_topo rises with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
