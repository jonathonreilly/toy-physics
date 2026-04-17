#!/usr/bin/env python3
"""Find structural predictor for decoherence susceptibility.

Phase noise decoheres on irregular graphs but not lattices. What graph
property predicts how much V drops? Candidates:

1. path_length_std (current coarse predictor)
2. edge_length_variance (how varied are edge lengths)
3. degree_variance (how varied are node degrees)
4. spectral_gap (algebraic connectivity of the Laplacian)
5. slit_path_divergence (how different are paths from slit A vs B)
6. mass_path_overlap (fraction of slit→det paths passing through mass)
7. graph_diameter / shortest_path_ratio

Measure V_ensemble at η=0.7 on 30 different DAG configs.
Correlate V_drop with each structural measure.

PStack experiment: decoherence-structural-predictor
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


def pathsum_noisy(positions, adj, field, src, det, k, eta, rng,
                  barrier_idx=None, slit_idx=None):
    n = len(positions)
    blocked = set()
    if barrier_idx is not None and slit_idx is not None:
        blocked = set(barrier_idx) - set(slit_idx)

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
        if i in blocked or abs(amps[i]) < 1e-30:
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
            noise = eta*rng.gauss(0, 1) if eta > 0 else 0
            ea = cmath.exp(1j*(k*act+noise))/(L**1.0)
            amps[j] += amps[i]*ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def visibility(probs, positions, det):
    py = defaultdict(float)
    for d in det:
        py[positions[d][1]] += probs.get(d, 0)
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


def compute_structural_measures(positions, adj, src, det, slit_a, slit_b,
                                mass_idx, barrier_idx, slit_idx):
    """Compute candidate structural predictors."""
    n = len(positions)

    # 1. Edge length stats
    edge_lengths = []
    for i, nbs in adj.items():
        for j in nbs:
            L = math.sqrt((positions[i][0]-positions[j][0])**2 +
                          (positions[i][1]-positions[j][1])**2)
            edge_lengths.append(L)

    mean_el = sum(edge_lengths)/len(edge_lengths) if edge_lengths else 0
    var_el = sum((l-mean_el)**2 for l in edge_lengths)/len(edge_lengths) if edge_lengths else 0

    # 2. Degree stats
    out_degrees = [len(adj.get(i, [])) for i in range(n)]
    mean_deg = sum(out_degrees)/len(out_degrees) if out_degrees else 0
    var_deg = sum((d-mean_deg)**2 for d in out_degrees)/len(out_degrees) if out_degrees else 0

    # 3. Shortest path lengths from each slit to detectors
    def bfs_lengths(start_nodes, end_nodes):
        lengths = []
        for s in start_nodes:
            dist = {s: 0}
            queue = deque([s])
            while queue:
                node = queue.popleft()
                for nb in adj.get(node, []):
                    if nb not in dist:
                        dist[nb] = dist[node] + 1
                        queue.append(nb)
            for e in end_nodes:
                if e in dist:
                    lengths.append(dist[e])
        return lengths

    blocked_set = set(barrier_idx) - set(slit_idx) if barrier_idx and slit_idx else set()

    # Build filtered adj (remove blocked)
    filt_adj = {}
    for i, nbs in adj.items():
        if i in blocked_set:
            continue
        filt_adj[i] = [j for j in nbs if j not in blocked_set]

    def bfs_filt(start_nodes, end_nodes):
        lengths = []
        for s in start_nodes:
            dist = {s: 0}
            queue = deque([s])
            while queue:
                node = queue.popleft()
                for nb in filt_adj.get(node, []):
                    if nb not in dist:
                        dist[nb] = dist[node] + 1
                        queue.append(nb)
            for e in end_nodes:
                if e in dist:
                    lengths.append(dist[e])
        return lengths

    paths_a = bfs_filt(slit_a, det)
    paths_b = bfs_filt(slit_b, det)

    mean_a = sum(paths_a)/len(paths_a) if paths_a else 0
    mean_b = sum(paths_b)/len(paths_b) if paths_b else 0
    slit_divergence = abs(mean_a - mean_b)

    # Combined path length stats (all slit→det paths)
    all_paths = paths_a + paths_b
    mean_pl = sum(all_paths)/len(all_paths) if all_paths else 0
    std_pl = (sum((p-mean_pl)**2 for p in all_paths)/len(all_paths))**0.5 if all_paths else 0

    # 4. Mass overlap: how many slit→det paths go near mass?
    mass_set = set(mass_idx)
    mass_ys = [positions[m][1] for m in mass_idx]
    mass_y_range = (min(mass_ys), max(mass_ys)) if mass_ys else (0, 0)
    mass_xs = [positions[m][0] for m in mass_idx]
    mass_x_range = (min(mass_xs), max(mass_xs)) if mass_xs else (0, 0)

    # Count edges in mass region
    edges_near_mass = 0
    total_edges = 0
    for i, nbs in adj.items():
        for j in nbs:
            total_edges += 1
            y_avg = (positions[i][1] + positions[j][1]) / 2
            x_avg = (positions[i][0] + positions[j][0]) / 2
            if (mass_y_range[0]-2 <= y_avg <= mass_y_range[1]+2 and
                mass_x_range[0]-2 <= x_avg <= mass_x_range[1]+2):
                edges_near_mass += 1

    mass_overlap = edges_near_mass / total_edges if total_edges > 0 else 0

    # 5. CV of edge lengths (coefficient of variation)
    cv_el = (var_el**0.5) / mean_el if mean_el > 0 else 0

    return {
        'edge_len_var': var_el,
        'edge_len_cv': cv_el,
        'degree_var': var_deg,
        'path_len_std': std_pl,
        'slit_divergence': slit_divergence,
        'mass_overlap': mass_overlap,
        'mean_degree': mean_deg,
    }


def main():
    N_env = 30
    eta = 0.7
    k = 5.0

    configs = []
    # Vary y_range, radius, nodes_per_layer
    for yr in [5, 10, 15, 20]:
        for r in [2.0, 3.0, 4.0]:
            for npl in [15, 25]:
                configs.append((12, npl, yr, r))

    print("=" * 70)
    print("STRUCTURAL PREDICTOR FOR DECOHERENCE SUSCEPTIBILITY")
    print(f"  η={eta}, k={k}, {N_env} env states")
    print(f"  {len(configs)} graph configurations")
    print("=" * 70)
    print()

    data = []

    for n_layers, npl, yr, radius in configs:
        v_drops = []
        measures_list = []

        for seed in range(3):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=float(yr), connect_radius=radius,
                rng_seed=seed*11+7,
            )
            n = len(positions)
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 6:
                continue

            src = by_layer[layers[0]]
            det = by_layer[layers[-1]]
            if not det:
                continue

            mid = len(layers)//2
            all_ys = [y for _, y in positions]
            cy = sum(all_ys)/len(all_ys)

            mass_layers = [layers[mid-1], layers[mid], layers[mid+1]]
            mass_idx = [i for i in sum((by_layer[l] for l in mass_layers), [])
                        if positions[i][1] > cy+1]
            if len(mass_idx) < 3:
                continue

            free_f = [0.0]*n

            if mid < 3:
                continue
            bl = layers[mid-3]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy+2][:3]
            sb = [i for i in bi if positions[i][1] < cy-2][:3]
            if not sa or not sb:
                continue
            si = sa + sb

            measures = compute_structural_measures(
                positions, adj, src, det, sa, sb, mass_idx, bi, si)
            measures_list.append(measures)

            # Baseline V
            pb = pathsum_noisy(positions, adj, free_f, src, det, k, 0.0,
                               random.Random(0), bi, si)
            vb = visibility(pb, positions, det)

            # Noisy ensemble V
            avg_p = {d: 0.0 for d in det}
            for env_i in range(N_env):
                rng = random.Random(env_i*31+seed*7)
                pn = pathsum_noisy(positions, adj, free_f, src, det, k, eta,
                                    rng, bi, si)
                for d in det:
                    avg_p[d] += pn.get(d, 0)
            t = sum(avg_p.values())
            if t > 0:
                avg_p = {d: p/t for d, p in avg_p.items()}
            vn = visibility(avg_p, positions, det)

            v_drops.append(vb - vn)

        if v_drops and measures_list:
            mean_vd = sum(v_drops)/len(v_drops)
            mean_measures = {}
            for key in measures_list[0]:
                mean_measures[key] = sum(m[key] for m in measures_list)/len(measures_list)
            mean_measures['v_drop'] = mean_vd
            data.append(mean_measures)

    # ================================================================
    # Correlation analysis
    # ================================================================
    print(f"Collected {len(data)} data points")
    print()

    predictors = ['edge_len_var', 'edge_len_cv', 'degree_var', 'path_len_std',
                  'slit_divergence', 'mass_overlap', 'mean_degree']

    v_drops = [d['v_drop'] for d in data]

    print(f"  {'predictor':>20s}  {'corr':>8s}  {'R²':>8s}  {'range':>12s}")
    print(f"  {'-' * 52}")

    for pred in predictors:
        xs = [d[pred] for d in data]
        ys = v_drops
        n = len(data)
        mx = sum(xs)/n
        my = sum(ys)/n
        cov = sum((x-mx)*(y-my) for x, y in zip(xs, ys))/n
        sx = (sum((x-mx)**2 for x in xs)/n)**0.5
        sy = (sum((y-my)**2 for y in ys)/n)**0.5
        corr = cov/(sx*sy) if sx > 0 and sy > 0 else 0
        r2 = corr**2
        x_range = f"[{min(xs):.3f}, {max(xs):.3f}]"
        print(f"  {pred:>20s}  {corr:+8.4f}  {r2:8.4f}  {x_range:>12s}")

    print()
    print("Best predictor = highest |corr| or R²")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
