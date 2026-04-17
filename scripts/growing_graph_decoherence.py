#!/usr/bin/env python3
"""Decoherence from graph growth during propagation.

All static-graph env architectures have wrong scaling. Axiom 1 says
the graph GROWS. New nodes mid-propagation create paths that didn't
exist at the source → amplitude from different slits encounters
different graph structures → genuine new information.

Implementation: propagate in two phases.
Phase 1: propagate from source through slits to mid-graph (layers 0..M).
Phase 2: ADD new nodes/edges in layers M+1..N, then continue propagation.

The key: slit-A and slit-B amplitude arrive at the growth boundary at
different times/positions. New nodes connect preferentially to nearby
existing nodes → different slit amplitudes see different new structure.

Compare V with vs without mid-propagation growth.

PStack experiment: growing-graph-decoherence
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag


def compute_field(positions, adj, mass_idx, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_idx)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0]*n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def propagate_on_subgraph(positions, adj, field, start_amps, blocked, k):
    """Continue propagation from start_amps on the given graph."""
    n = len(positions)
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

    amps = dict(start_amps)
    for i in order:
        if i not in amps or abs(amps[i]) < 1e-30 or i in blocked:
            continue
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
            if j not in amps:
                amps[j] = 0.0+0.0j
            amps[j] += amps[i]*ea

    return amps


def visibility_from_amps(amps, det, positions):
    probs = {d: abs(amps.get(d, 0.0))**2 for d in det}
    total = sum(probs.values())
    if total == 0:
        return 0.0
    probs = {d: p/total for d, p in probs.items()}
    py = defaultdict(float)
    for d, p in probs.items():
        py[positions[d][1]] += p
    ys = sorted(py.keys())
    if len(ys) < 3:
        return 0.0
    vals = [py[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals)-1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals)-1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
    return 0.0


def main():
    n_seeds = 10
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("DECOHERENCE FROM GRAPH GROWTH DURING PROPAGATION")
    print("  Compare: static graph vs graph that grows mid-propagation")
    print("=" * 70)
    print()

    # For each seed: build graph with N layers. Propagate on full graph (static).
    # Then: propagate on first half, grow second half with different seed,
    # continue propagation. The growth creates different paths for each
    # "realization" → ensemble average should show decoherence.

    N_growth_realizations = 20

    for n_layers in [10, 15, 20]:
        print(f"  n_layers = {n_layers}:")
        print(f"    {'seed':>4s}  {'V_static':>8s}  {'V_grown':>8s}  {'V_drop':>8s}")
        print(f"    {'-' * 32}")

        v_drops = []

        for seed in range(n_seeds):
            # Build full static graph
            positions, adj, _ = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=20,
                y_range=10.0, connect_radius=3.0,
                rng_seed=seed*11+7,
            )
            n = len(positions)
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 5:
                continue

            src = by_layer[layers[0]]
            det = set(by_layer[layers[-1]])
            if not det:
                continue

            all_ys = [y for _, y in positions]
            cy = sum(all_ys)/len(all_ys)

            # Barrier in first third
            bl_idx = len(layers)//3
            bl = layers[bl_idx]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy+3][:3]
            sb = [i for i in bi if positions[i][1] < cy-3][:3]
            if not sa or not sb:
                continue
            si = set(sa+sb)
            blocked = set(bi) - si

            field = [0.0]*n  # free field for simplicity

            # Static: propagate on full graph, k-averaged V
            static_vs = []
            for k in k_band:
                start = {s: 1.0/len(src)+0.0j for s in src}
                amps = propagate_on_subgraph(positions, adj, field, start, blocked, k)
                static_vs.append(visibility_from_amps(amps, det, positions))
            v_static = sum(static_vs)/len(static_vs)

            # Growing: propagate through first half, then for each growth
            # realization, generate different second-half connections
            # and average the probabilities
            mid_layer_idx = len(layers)//2
            mid_layer = layers[mid_layer_idx]

            # Get nodes in first half and second half
            first_half_nodes = set()
            for l in layers[:mid_layer_idx+1]:
                first_half_nodes.update(by_layer[l])

            second_half_nodes = set()
            for l in layers[mid_layer_idx+1:]:
                second_half_nodes.update(by_layer[l])

            # First-half adj (only edges within first half)
            first_adj = {}
            for i, nbs in adj.items():
                if i in first_half_nodes:
                    first_adj[i] = [j for j in nbs if j in first_half_nodes]

            # Propagate through first half
            avg_grown_probs = {d: 0.0 for d in det}

            for growth_i in range(N_growth_realizations):
                # Re-wire second half edges randomly
                rng = random.Random(seed*1000 + growth_i*31 + 7)

                # Build new second-half edges: connect each second-half node
                # to nearby nodes in the previous layer with randomized threshold
                grown_adj = dict(first_adj)
                for l_idx in range(mid_layer_idx, len(layers)-1):
                    curr_layer = by_layer[layers[l_idx]]
                    next_layer = by_layer[layers[l_idx+1]]
                    for j in next_layer:
                        x2, y2 = positions[j]
                        for i in curr_layer:
                            x1, y1 = positions[i]
                            dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
                            # Randomize connection radius slightly
                            threshold = 3.0 * (0.7 + 0.6 * rng.random())
                            if dist <= threshold:
                                if i not in grown_adj:
                                    grown_adj[i] = []
                                grown_adj[i].append(j)

                for k in k_band:
                    start = {s: 1.0/len(src)+0.0j for s in src}
                    amps = propagate_on_subgraph(positions, grown_adj, field, start, blocked, k)
                    for d in det:
                        avg_grown_probs[d] += abs(amps.get(d, 0.0))**2

            # Normalize ensemble-averaged probs
            total = sum(avg_grown_probs.values())
            if total > 0:
                avg_grown_probs = {d: p/total for d, p in avg_grown_probs.items()}

            v_grown = visibility_from_amps(
                {d: math.sqrt(max(avg_grown_probs.get(d, 0), 0))+0.0j for d in det},
                det, positions)
            # Actually compute V from probabilities directly
            py = defaultdict(float)
            for d in det:
                py[positions[d][1]] += avg_grown_probs.get(d, 0)
            ys = sorted(py.keys())
            if len(ys) >= 3:
                vals = [py[y] for y in ys]
                peaks = [vals[i] for i in range(1, len(vals)-1)
                         if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
                troughs = [vals[i] for i in range(1, len(vals)-1)
                           if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
                if peaks and troughs:
                    v_grown = (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
                else:
                    v_grown = 0.0
            else:
                v_grown = 0.0

            v_drop = v_static - v_grown
            v_drops.append(v_drop)

            print(f"    {seed:4d}  {v_static:8.4f}  {v_grown:8.4f}  {v_drop:+8.4f}")

        if v_drops:
            mean_drop = sum(v_drops)/len(v_drops)
            n_decoh = sum(1 for d in v_drops if d > 0.02)
            print(f"    ---")
            print(f"    Mean V_drop: {mean_drop:+.4f}, D: {n_decoh}/{len(v_drops)}")
        print()

    print("If V_drop > 0 and increases with n_layers:")
    print("  → Graph growth provides correctly-scaling decoherence")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
