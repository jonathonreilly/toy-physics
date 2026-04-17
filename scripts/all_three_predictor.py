#!/usr/bin/env python3
"""What structural observable predicts ALL THREE seeds?

Under the optimal between-slit geometry (mass_offset=1, fine env),
30% of seeds show gravity + interference + decoherence simultaneously.
What distinguishes those seeds from the rest?

Candidate predictors (measured per seed before running the path-sum):
1. mass_path_fraction: fraction of slit→det paths passing through mass
2. slit_mass_distance: mean graph distance from slit nodes to mass nodes
3. mass_y_asymmetry: how asymmetrically mass is positioned relative to slits
4. slit_path_divergence: how different are paths from slit-A vs slit-B
5. mass_degree: mean out-degree of mass nodes
6. mass_field_gradient: field gradient at mass region
7. slit_to_det_path_count: number of distinct paths from slits to detector

This pass also tests a sharper hypothesis: perhaps decoherence depends on
which mass node each slit's paths exit from last, rather than on coarse
reachability alone.

PStack experiment: all-three-predictor
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.two_register_decoherence import (
    compute_field, pathsum_two_register, pathsum_coherent,
    visibility, centroid_y,
)


def bfs_reachable(adj, start_nodes, target_nodes, blocked=None):
    """Count how many target nodes are reachable from start nodes."""
    blocked = blocked or set()
    visited = set()
    queue = deque(s for s in start_nodes if s not in blocked)
    visited.update(queue)
    while queue:
        node = queue.popleft()
        for nb in adj.get(node, []):
            if nb not in visited and nb not in blocked:
                visited.add(nb)
                queue.append(nb)
    return len(visited & set(target_nodes))


def graph_distance(adj, src_nodes, target_nodes, blocked=None):
    """Mean shortest path length from src to target."""
    blocked = blocked or set()
    distances = []
    for s in src_nodes:
        dist = {s: 0}
        queue = deque([s])
        while queue:
            node = queue.popleft()
            for nb in adj.get(node, []):
                if nb not in dist and nb not in blocked:
                    dist[nb] = dist[node] + 1
                    queue.append(nb)
        for t in target_nodes:
            if t in dist:
                distances.append(dist[t])
    return sum(distances)/len(distances) if distances else 999


def topological_order(adj, n):
    """Return a topological order for the DAG."""
    in_deg = [0] * n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    queue = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in adj.get(node, []):
            in_deg[nb] -= 1
            if in_deg[nb] == 0:
                queue.append(nb)
    return order


def reverse_adjacency(adj):
    """Build reverse adjacency for dynamic path counting."""
    rev = defaultdict(list)
    for i, nbs in adj.items():
        for j in nbs:
            rev[j].append(i)
    return rev


def path_counts_from_sources(rev_adj, order, sources, blocked=None):
    """Count distinct paths from a source set to every node."""
    blocked = blocked or set()
    source_set = set(sources)
    counts = defaultdict(int)
    for s in source_set:
        if s not in blocked:
            counts[s] += 1
    for node in order:
        if node in blocked or node in source_set:
            continue
        total = 0
        for parent in rev_adj.get(node, []):
            if parent not in blocked:
                total += counts[parent]
        if total:
            counts[node] = total
    return counts


def path_counts_to_targets(adj, order, targets, blocked=None):
    """Count distinct paths from every node to a target set."""
    blocked = blocked or set()
    target_set = set(targets)
    counts = defaultdict(int)
    for t in target_set:
        if t not in blocked:
            counts[t] = 1
    for node in reversed(order):
        if node in blocked or node in target_set:
            continue
        total = 0
        for nb in adj.get(node, []):
            if nb not in blocked:
                total += counts[nb]
        if total:
            counts[node] = total
    return counts


def last_mass_distribution(adj, rev_adj, order, slit_nodes, det_nodes, mass_set, blocked=None):
    """Distribution over the last mass node reached by slit->detector paths."""
    blocked = blocked or set()
    to_mass = path_counts_from_sources(rev_adj, order, slit_nodes, blocked)

    weights = {}
    for mass_node in mass_set:
        if mass_node in blocked:
            continue
        blocked_after = set(blocked) | (set(mass_set) - {mass_node})
        to_det = path_counts_to_targets(adj, order, det_nodes, blocked_after)
        weight = to_mass[mass_node] * to_det[mass_node]
        if weight:
            weights[mass_node] = weight

    total = sum(weights.values())
    if total == 0:
        return {}
    return {node: weight / total for node, weight in weights.items()}


def distribution_overlap(dist_a, dist_b):
    """Overlap between two discrete distributions."""
    keys = set(dist_a) | set(dist_b)
    return sum(min(dist_a.get(k, 0.0), dist_b.get(k, 0.0)) for k in keys)


def independent_same_prob(dist_a, dist_b):
    """Probability two independently sampled paths share the same last mass node."""
    keys = set(dist_a) | set(dist_b)
    return sum(dist_a.get(k, 0.0) * dist_b.get(k, 0.0) for k in keys)


def mean_y(dist, positions):
    """Mean y-value of a node distribution."""
    total = sum(dist.values())
    if total == 0:
        return 0.0
    return sum(positions[node][1] * weight for node, weight in dist.items()) / total


def main():
    n_layers = 15
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 30
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("STRUCTURAL PREDICTOR FOR ALL THREE SEEDS")
    print(f"  Between-slit geometry, mass_offset=1, fine env")
    print(f"  {n_seeds} seeds, corrected propagator")
    print("=" * 70)
    print()

    data = []

    for seed in range(n_seeds):
        positions, adj, _ = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=npl,
            y_range=y_range, connect_radius=radius,
            rng_seed=seed*11+7,
        )
        n = len(positions)
        order = topological_order(adj, n)
        rev_adj = reverse_adjacency(adj)
        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 7:
            continue

        src = by_layer[layers[0]]
        det = set(by_layer[layers[-1]])
        if not det:
            continue

        all_ys = [y for _, y in positions]
        cy = sum(all_ys)/len(all_ys)

        bl_idx = len(layers) // 3
        bl = layers[bl_idx]
        bi = by_layer[bl]
        sa = [i for i in bi if positions[i][1] > cy + 3][:3]
        sb = [i for i in bi if positions[i][1] < cy - 3][:3]
        if not sa or not sb:
            continue
        si = set(sa + sb)
        blocked = set(bi) - si

        # Mass: post-barrier layer, between slits
        post_bl = layers[bl_idx + 1]
        pb_nodes = by_layer[post_bl]
        mass_nodes = [i for i in pb_nodes if abs(positions[i][1] - cy) <= 3]
        if len(mass_nodes) < 2:
            continue
        mass_set = set(mass_nodes)

        # Gravity mass downstream
        grav_layer = layers[2 * len(layers) // 3]
        grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
        full_mass = mass_set | set(grav_mass)
        field = compute_field(positions, adj, list(full_mass))
        free_f = [0.0]*n

        # --- Structural observables (computed BEFORE path-sum) ---

        # 1. Slit-A to mass graph distance
        dist_a_mass = graph_distance(adj, sa, list(mass_set))
        dist_b_mass = graph_distance(adj, sb, list(mass_set))
        slit_mass_asymmetry = abs(dist_a_mass - dist_b_mass)

        # 2. Mass out-degree
        mass_degrees = [len(adj.get(m, [])) for m in mass_nodes]
        mean_mass_deg = sum(mass_degrees)/len(mass_degrees) if mass_degrees else 0

        # 3. Mass y-spread
        mass_ys = [positions[m][1] for m in mass_nodes]
        mass_y_spread = max(mass_ys) - min(mass_ys) if mass_ys else 0

        # 4. Number of mass nodes
        n_mass = len(mass_nodes)

        # 5. Field gradient at mass region
        field_above = [field[m] for m in mass_nodes if positions[m][1] > cy]
        field_below = [field[m] for m in mass_nodes if positions[m][1] <= cy]
        field_grad = 0
        if field_above and field_below:
            field_grad = sum(field_above)/len(field_above) - sum(field_below)/len(field_below)

        # 6. Slit path divergence: how many post-barrier nodes are reachable from A but not B?
        reach_a = set()
        queue = deque(sa)
        reach_a.update(queue)
        while queue:
            node = queue.popleft()
            for nb in adj.get(node, []):
                if nb not in reach_a and nb not in blocked:
                    reach_a.add(nb)
                    queue.append(nb)

        reach_b = set()
        queue = deque(sb)
        reach_b.update(queue)
        while queue:
            node = queue.popleft()
            for nb in adj.get(node, []):
                if nb not in reach_b and nb not in blocked:
                    reach_b.add(nb)
                    queue.append(nb)

        mass_a_only = len(mass_set & reach_a - reach_b)
        mass_b_only = len(mass_set & reach_b - reach_a)
        mass_exclusive = mass_a_only + mass_b_only
        mass_exclusive_frac = mass_exclusive / n_mass if n_mass > 0 else 0

        # 7. Last-mass-node divergence: do slit-A and slit-B exit the mass region
        # through different final mass nodes?
        last_a = last_mass_distribution(adj, rev_adj, order, sa, det, mass_set, blocked)
        last_b = last_mass_distribution(adj, rev_adj, order, sb, det, mass_set, blocked)
        last_mass_overlap = distribution_overlap(last_a, last_b)
        last_mass_same_prob = independent_same_prob(last_a, last_b)
        last_mass_divergence = 1.0 - last_mass_same_prob
        last_mass_mean_y_gap = abs(mean_y(last_a, positions) - mean_y(last_b, positions))

        # --- Run path-sum ---
        grav_shifts = []
        for k in k_band:
            fp = pathsum_coherent(positions, adj, free_f, src, det, k)
            mp = pathsum_two_register(positions, adj, field, src, det, k,
                                     mass_set, env_mode="fine")
            grav_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))
        avg_grav = sum(grav_shifts)/len(grav_shifts)
        attracts = False
        if grav_mass:
            grav_cy = sum(positions[i][1] for i in grav_mass)/len(grav_mass)
            attracts = (grav_cy - cy > 0 and avg_grav > 0.05)

        avg_coh = defaultdict(float)
        avg_2reg = defaultdict(float)
        for k in k_band:
            pc = pathsum_coherent(positions, adj, field, src, det, k, blocked)
            p2 = pathsum_two_register(positions, adj, field, src, det, k,
                                       mass_set, blocked, env_mode="fine")
            for d in det:
                avg_coh[d] += pc.get(d, 0)
                avg_2reg[d] += p2.get(d, 0)

        for avg in [avg_coh, avg_2reg]:
            t = sum(avg.values())
            if t > 0:
                for d in avg:
                    avg[d] /= t

        vc = visibility(dict(avg_coh), positions, list(det))
        v2 = visibility(dict(avg_2reg), positions, list(det))
        vd = vc - v2

        has_all3 = attracts and v2 > 0.05 and vd > 0.02

        data.append({
            'seed': seed,
            'all3': has_all3,
            'grav': avg_grav,
            'V_drop': vd,
            'dist_a_mass': dist_a_mass,
            'dist_b_mass': dist_b_mass,
            'slit_mass_asym': slit_mass_asymmetry,
            'mean_mass_deg': mean_mass_deg,
            'mass_y_spread': mass_y_spread,
            'n_mass': n_mass,
            'field_grad': field_grad,
            'mass_exclusive_frac': mass_exclusive_frac,
            'last_mass_overlap': last_mass_overlap,
            'last_mass_same_prob': last_mass_same_prob,
            'last_mass_divergence': last_mass_divergence,
            'last_mass_mean_y_gap': last_mass_mean_y_gap,
        })

    # --- Correlation analysis ---
    all3_seeds = [d for d in data if d['all3']]
    non_seeds = [d for d in data if not d['all3']]

    print(f"  ALL THREE: {len(all3_seeds)}/{len(data)} seeds")
    print()

    predictors = ['slit_mass_asym', 'last_mass_divergence', 'last_mass_mean_y_gap',
                  'last_mass_overlap', 'last_mass_same_prob', 'mean_mass_deg',
                  'mass_y_spread', 'n_mass', 'field_grad', 'mass_exclusive_frac',
                  'dist_a_mass', 'dist_b_mass']

    print(f"  {'predictor':>22s}  {'all3_mean':>10s}  {'other_mean':>10s}  {'ratio':>8s}  {'corr':>8s}")
    print(f"  {'-' * 64}")

    for pred in predictors:
        a3_vals = [d[pred] for d in all3_seeds]
        oth_vals = [d[pred] for d in non_seeds]
        a3_mean = sum(a3_vals)/len(a3_vals) if a3_vals else 0
        oth_mean = sum(oth_vals)/len(oth_vals) if oth_vals else 0
        ratio = a3_mean/oth_mean if oth_mean != 0 else 0

        # Point-biserial correlation
        all_vals = [d[pred] for d in data]
        all_labels = [1 if d['all3'] else 0 for d in data]
        n_tot = len(data)
        mx = sum(all_vals)/n_tot
        my = sum(all_labels)/n_tot
        cov = sum((v-mx)*(l-my) for v, l in zip(all_vals, all_labels))/n_tot
        sx = (sum((v-mx)**2 for v in all_vals)/n_tot)**0.5
        sy = (sum((l-my)**2 for l in all_labels)/n_tot)**0.5
        corr = cov/(sx*sy) if sx > 0 and sy > 0 else 0

        print(f"  {pred:>22s}  {a3_mean:10.3f}  {oth_mean:10.3f}  {ratio:8.2f}  {corr:+8.4f}")

    print()
    print("Best predictor = highest |corr|")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
