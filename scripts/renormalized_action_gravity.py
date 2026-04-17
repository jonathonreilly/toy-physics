#!/usr/bin/env python3
"""G1: Path-multiplicity-renormalized action.

Current: amplitude = exp(i*k*S) / L^p — all paths contribute equally.
Fix: S_eff = S / n_paths^α where n_paths = number of paths through edge.

High-multiplicity edges (common on large graphs) get their action
divided down. This should prevent the total phase deficit from
saturating, because the many near-equivalent paths that cause
saturation each contribute proportionally less.

Test on the scaling testbench: does R_grav stay nonzero at large N?

PStack experiment: renormalized-action-gravity
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.two_register_decoherence import compute_field, centroid_y


def count_paths_per_edge(adj, src, det, n):
    """Count paths through each edge: n_paths(i→j) = paths_from_src(i) × paths_to_det(j)."""
    # Forward: count paths from sources
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

    src_set = set(src)
    fwd = [0]*n
    for s in src_set:
        fwd[s] = 1
    for i in order:
        if i in src_set:
            continue
        for j in adj.get(i, []):
            pass  # forward pass below
    # Recompute properly
    fwd = [0]*n
    for s in src:
        fwd[s] = 1
    for i in order:
        for j in adj.get(i, []):
            fwd[j] += fwd[i]

    # Backward: count paths to detectors
    det_set = set(det)
    bwd = [0]*n
    for d in det_set:
        bwd[d] = 1
    for i in reversed(order):
        for j in adj.get(i, []):
            bwd[i] += bwd[j]

    # Edge path count = fwd[i] * bwd[j]
    edge_paths = {}
    for i, nbs in adj.items():
        for j in nbs:
            edge_paths[(i, j)] = max(fwd[i] * bwd[j], 1)

    return edge_paths


def propagate_renormalized(positions, adj, field, src, det, k, alpha,
                           edge_paths=None):
    """Corrected propagator with path-multiplicity-renormalized action.

    S_eff = S / n_paths(edge)^alpha
    alpha=0: standard (no renormalization)
    alpha>0: high-multiplicity edges contribute less action
    """
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

    amps = [0.0+0.0j]*n
    for s in src:
        amps[s] = 1.0/len(src)
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2-x1)**2+(y2-y1)**2)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret

            # Renormalize action by path multiplicity
            np = edge_paths.get((i, j), 1) if edge_paths else 1
            act_eff = act / (np ** alpha) if alpha > 0 and np > 0 else act

            ea = cmath.exp(1j*k*act_eff)/(L**1.0)
            amps[j] += amps[i]*ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("G1: PATH-MULTIPLICITY-RENORMALIZED ACTION")
    print("  S_eff = S / n_paths^α")
    print("=" * 70)
    print()

    # Test: does R_grav stay nonzero at large N?
    for alpha in [0.0, 0.1, 0.25, 0.5, 1.0]:
        print(f"  α = {alpha}:")
        print(f"    {'N_layers':>8s}  {'R_grav':>8s}  {'k0_shift':>8s}")
        print(f"    {'-' * 28}")

        for nl in [8, 12, 15, 20, 25]:
            gravs = []
            k0_shifts = []
            for seed in range(5):
                positions, adj, _ = generate_causal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed*11+7)
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
                mid = len(layers)//2
                grav_mass = [i for i in by_layer[layers[mid]]
                            if positions[i][1] > cy+2]
                if len(grav_mass) < 2:
                    continue

                free_f = [0.0]*n
                field = compute_field(positions, adj, grav_mass)
                edge_paths = count_paths_per_edge(adj, src, det, n)

                shifts = []
                for k in k_band:
                    fp = propagate_renormalized(positions, adj, free_f, src, det, k, alpha, edge_paths)
                    mp = propagate_renormalized(positions, adj, field, src, det, k, alpha, edge_paths)
                    fy = centroid_y(fp, positions)
                    my = centroid_y(mp, positions)
                    shifts.append(my - fy)

                avg = sum(shifts)/len(shifts)
                # Beam width
                fp0 = propagate_renormalized(positions, adj, free_f, src, det, 5.0, alpha, edge_paths)
                total = sum(fp0.values())
                if total > 0:
                    mean = sum(positions[d][1]*p for d, p in fp0.items())/total
                    var = sum(positions[d][1]**2*p for d, p in fp0.items())/total - mean**2
                    width = max(var**0.5, 0.1)
                else:
                    width = 1.0
                gravs.append(avg/width)

                # k=0 check
                fp0 = propagate_renormalized(positions, adj, free_f, src, det, 0.0, alpha, edge_paths)
                mp0 = propagate_renormalized(positions, adj, field, src, det, 0.0, alpha, edge_paths)
                k0_shifts.append(centroid_y(mp0, positions) - centroid_y(fp0, positions))

            if gravs:
                k0 = sum(abs(s) for s in k0_shifts)/len(k0_shifts) if k0_shifts else 0
                print(f"    {nl:8d}  {sum(gravs)/len(gravs):+8.3f}  {k0:8.5f}")

        print()

    print("If R_grav stays stable at large N for some α > 0: renormalization helps")
    print("If k0_shift > 0: renormalization breaks k=0→0 constraint")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
