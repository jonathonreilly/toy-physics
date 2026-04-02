#!/usr/bin/env python3
"""Dense+prune gravity repair: does q=0.05 preserve gravity at N=80?

The same-graph joint showed gravity flips sign at N=80 with q=0.10.
Try gentler pruning (q=0.05) that removes fewer nodes.

PStack experiment: dense-prune-gravity-repair
"""

from __future__ import annotations

import cmath
import math
import os
import random
import statistics
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
LAM = 10.0
N_YBINS = 8


def gen_dense_3d(n_layers=80, npl=60, yz_range=12.0, r=2.7, rng_seed=42):
    rng = random.Random(rng_seed)
    positions = []; adj = defaultdict(list); layers = []
    for layer in range(n_layers):
        x = float(layer); nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0)); nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range); z = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r: adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def compute_field(positions, adj, mass_ids, iterations=50):
    n = len(positions); undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs: undirected[i].add(j); undirected[j].add(i)
    ms = set(mass_ids); field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0]*n
        for i in range(n):
            if i in ms: nf[i] = 1.0
            elif undirected.get(i): nf[i] = sum(field[j] for j in undirected[i])/len(undirected[i])
        field = nf
    return field


def propagate(positions, adj, field, src, k, blocked=None):
    n = len(positions); blocked = blocked or set()
    in_deg = [0]*n
    for nbs in adj.values():
        for j in nbs: in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0); order = []
    while q:
        i = q.popleft(); order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0: q.append(j)
    amps = [0j]*n
    for s in src: amps[s] = 1.0/len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked: continue
        pi = positions[i]
        for j in adj.get(i, []):
            if j in blocked: continue
            pj = positions[j]; dx = pj[0]-pi[0]
            L = math.sqrt(sum((a-b)**2 for a, b in zip(pi, pj)))
            if L < 1e-10: continue
            theta = math.acos(min(max(dx/L,-1),1)); w = math.exp(-BETA*theta*theta)
            lf = 0.5*(field[i]+field[j]); dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L,0)); act = dl-ret
            amps[j] += amps[i]*cmath.exp(1j*k*act)*w/L
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list: p = abs(amps[d])**2; total += p; wy += p*positions[d][1]
    return wy/total if total > 1e-30 else 0.0


def adaptive_prune(positions, adj, layer_indices, quantile=0.05, max_iter=3):
    n = len(positions); n_layers = len(layer_indices); bl_idx = n_layers//3
    all_ys = [positions[i][1] for i in range(n)]; cy = sum(all_ys)/len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
    if not slit_a or not slit_b: return adj, 0
    base_blocked = set(barrier) - set(slit_a+slit_b)
    blocked_a = base_blocked | set(slit_b); det_set = set(layer_indices[-1])
    field = [0.0]*n; current_adj = dict(adj); total_removed = 0
    for _ in range(max_iter):
        amps_a = propagate(positions, current_adj, field, layer_indices[0], 5.0, blocked_a)
        amps_b = propagate(positions, current_adj, field, layer_indices[0], 5.0, base_blocked|set(slit_a))
        node_d = []
        for li in range(bl_idx+1, n_layers-1):
            for i in layer_indices[li]:
                if i in det_set: continue
                pa, pb = abs(amps_a[i])**2, abs(amps_b[i])**2
                total = pa+pb; D = abs(pa-pb)/total if total > 1e-30 else 0.0
                node_d.append((i, D))
        if not node_d: break
        node_d.sort(key=lambda x: x[1])
        n_remove = max(1, int(len(node_d)*quantile))
        remove_set = set(idx for idx, _ in node_d[:n_remove])
        new_adj = {}
        for i, nbs in current_adj.items():
            if i in remove_set: continue
            filtered = [j for j in nbs if j not in remove_set]
            if filtered: new_adj[i] = filtered
        total_removed += len(remove_set); current_adj = new_adj
    return current_adj, total_removed


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys: return 0.0
    y_min, y_max = min(ys)-0.01, max(ys)+0.01; bw = (y_max-y_min)/N_YBINS
    ba = [0j]*N_YBINS; bb = [0j]*N_YBINS
    for m in mid_nodes:
        b = max(0, min(N_YBINS-1, int((positions[m][1]-y_min)/bw)))
        ba[b] += amps_a[m]; bb[b] += amps_b[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    d = sum(abs(a)**2 for a in ba) + sum(abs(b)**2 for b in bb)
    return S/d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1,d2)] = (amps_a[d1]*amps_a[d2].conjugate() + amps_b[d1]*amps_b[d2].conjugate() +
                            D*amps_a[d1]*amps_b[d2].conjugate() + D*amps_b[d1]*amps_a[d2].conjugate())
    tr = sum(rho[(d,d)] for d in det_list).real
    if tr <= 1e-30: return math.nan
    for key in rho: rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def same_graph_joint(nl, quantile, n_seeds=16):
    """Same-graph: gravity + decoherence before/after pruning."""
    grav_base = []; grav_prune = []
    pur_base = []; pur_prune = []

    for seed in range(n_seeds):
        positions, adj_orig, layers = gen_dense_3d(n_layers=nl, rng_seed=seed*13+5)
        n = len(positions); n_layers_actual = len(layers); bl_idx = n_layers_actual//3
        src = layers[0]; det_list = list(layers[-1])
        if not det_list or n_layers_actual < 7: continue
        all_ys = [positions[i][1] for i in range(n)]; cy = sum(all_ys)/len(all_ys)

        # Fixed mass
        grav_idx = 2*n_layers_actual//3
        mass_cands = sorted([i for i in layers[grav_idx] if positions[i][1] > cy+2],
                            key=lambda i: abs(positions[i][1]-(cy+3)))[:8]
        if len(mass_cands) < 8: continue

        # Gravity baseline
        field = compute_field(positions, adj_orig, mass_cands)
        free_f = [0.0]*n
        gd_base = []
        for k in K_BAND:
            am = propagate(positions, adj_orig, field, src, k)
            af = propagate(positions, adj_orig, free_f, src, k)
            gd_base.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
        grav_base.append(sum(gd_base)/len(gd_base))

        # Prune
        adj_pruned, _ = adaptive_prune(positions, adj_orig, layers, quantile=quantile, max_iter=3)

        # Gravity pruned (same mass nodes)
        field_p = compute_field(positions, adj_pruned, mass_cands)
        gd_prune = []
        for k in K_BAND:
            am = propagate(positions, adj_pruned, field_p, src, k)
            af = propagate(positions, adj_pruned, free_f, src, k)
            gd_prune.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
        grav_prune.append(sum(gd_prune)/len(gd_prune))

        # Decoherence baseline
        barrier = layers[bl_idx]
        slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
        slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
        if not slit_a or not slit_b: continue
        blocked = set(barrier) - set(slit_a+slit_b)
        blocked_a = blocked|set(slit_b); blocked_b = blocked|set(slit_a)
        bath_mass = []
        for li in range(bl_idx+1, min(n_layers_actual, bl_idx+3)):
            for i in layers[li]:
                if abs(positions[i][1]-cy) <= 3: bath_mass.append(i)
        grav_mass = [i for i in layers[grav_idx] if positions[i][1] > cy+1]
        all_mass = list(set(bath_mass)|set(grav_mass))

        for adj_test, pur_list in [(adj_orig, pur_base), (adj_pruned, pur_prune)]:
            field_d = compute_field(positions, adj_test, all_mass) if all_mass else [0.0]*n
            mid_nodes = [i for li in range(bl_idx+1, n_layers_actual-1) for i in layers[li]
                         if i not in blocked and i not in set(det_list)]
            if len(mid_nodes) < 4: continue
            kpurs = []
            for k in K_BAND:
                aa = propagate(positions, adj_test, field_d, src, k, blocked_a)
                ab = propagate(positions, adj_test, field_d, src, k, blocked_b)
                Sn = cl_contrast(aa, ab, mid_nodes, positions)
                D = math.exp(-LAM**2*Sn)
                pur = cl_purity(aa, ab, D, det_list)
                if not math.isnan(pur): kpurs.append(pur)
            if kpurs: pur_list.append(sum(kpurs)/len(kpurs))

    return {
        "grav_base": sum(grav_base)/len(grav_base) if grav_base else float('nan'),
        "grav_prune": sum(grav_prune)/len(grav_prune) if grav_prune else float('nan'),
        "pur_base": sum(pur_base)/len(pur_base) if pur_base else float('nan'),
        "pur_prune": sum(pur_prune)/len(pur_prune) if pur_prune else float('nan'),
        "n": min(len(grav_base), len(pur_base)),
    }


def main():
    print("=" * 70)
    print("DENSE+PRUNE GRAVITY REPAIR: q=0.05 vs q=0.10")
    print("  Same-graph joint at N=80,100")
    print("=" * 70)
    print()

    for q in [0.05, 0.10]:
        print(f"  [quantile={q}]")
        print(f"  {'N':>4s}  {'grav_base':>10s}  {'grav_prune':>11s}  "
              f"{'pur_base':>9s}  {'pur_prune':>10s}  {'n':>3s}")
        print(f"  {'-'*52}")
        for nl in [80, 100]:
            r = same_graph_joint(nl, q, n_seeds=16)
            print(f"  {nl:4d}  {r['grav_base']:+10.4f}  {r['grav_prune']:+11.4f}  "
                  f"{r['pur_base']:9.4f}  {r['pur_prune']:10.4f}  {r['n']:3d}")
        print()

    print("=" * 70)
    print("KEY: does q=0.05 preserve gravity while still improving decoherence?")
    print("=" * 70)


if __name__ == "__main__":
    main()
