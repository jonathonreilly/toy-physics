#!/usr/bin/env python3
"""Hierarchical alpha study: is alpha=0.96 stable, and does it converge?

The overnight batch showed hierarchical leak=0.05 gives alpha=0.96 in 3D,
matching the best modular result. This follow-up asks:

  1. Is alpha stable across leak values?
  2. Does alpha converge with density (like modular alpha~0.58)?
  3. How does hierarchical compare to modular at matched parameters?

If hierarchical alpha converges near 1.0: channel separation WITHOUT
hard gap is sufficient for Newtonian mass scaling.

PStack experiment: hierarchical-alpha-study
"""

from __future__ import annotations
import math, cmath, random, statistics
from collections import defaultdict, deque

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)


def gen_3d_hierarchical(n_layers=15, npl=30, yz_range=10.0, r=3.5,
                         rng_seed=42, leak=0.05):
    rng = random.Random(rng_seed)
    positions = []; adj = defaultdict(list); layers = []
    bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0)); nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if layer > bl and round(positions[pi][0]) > bl:
                            same = positions[idx][1]*positions[pi][1] > 0
                            threshold = r if same else r*leak
                        else:
                            threshold = r
                        if d <= threshold:
                            adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def gen_3d_modular(n_layers=15, npl=30, yz_range=10.0, r=3.5,
                    rng_seed=42, gap=5.0, xlink=0.02):
    rng = random.Random(rng_seed)
    positions = []; adj = defaultdict(list); layers = []
    bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0)); nodes.append(len(positions)-1)
        else:
            for ni in range(npl):
                z = rng.uniform(-yz_range, yz_range)
                if gap > 0 and layer > bl:
                    y = rng.uniform(gap/2, yz_range) if ni < npl//2 else rng.uniform(-yz_range, -gap/2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if gap > 0 and layer > bl and round(positions[pi][0]) > bl:
                            same = positions[idx][1]*positions[pi][1] > 0
                            if same and d <= r: adj[pi].append(idx)
                            elif not same and d <= 2*r and rng.random() < xlink: adj[pi].append(idx)
                        elif d <= r:
                            adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def compute_field(positions, adj, mass_ids, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs: undirected[i].add(j); undirected[j].add(i)
    ms = set(mass_ids)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0]*n
        for i in range(n):
            if i in ms: nf[i] = 1.0
            elif undirected.get(i): nf[i] = sum(field[j] for j in undirected[i])/len(undirected[i])
        field = nf
    return field


def propagate(positions, adj, field, src, k):
    n = len(positions)
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
        if abs(amps[i]) < 1e-30: continue
        pi = positions[i]
        for j in adj.get(i, []):
            pj = positions[j]; dx = pj[0]-pi[0]
            L = math.sqrt(sum((a-b)**2 for a, b in zip(pi, pj)))
            if L < 1e-10: continue
            theta = math.acos(min(max(dx/L,-1),1))
            w = math.exp(-BETA*theta*theta)
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf); ret = math.sqrt(max(dl*dl-L*L,0)); act = dl-ret
            amps[j] += amps[i] * cmath.exp(1j*k*act) * w / L
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d])**2; total += p; wy += p*positions[d][1]
    return wy/total if total > 1e-30 else 0.0


def measure_alpha(gen_fn, n_seeds=20, **kwargs):
    mass_counts = [1, 2, 4, 6, 8, 12, 16]
    results = []
    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layers = gen_fn(rng_seed=seed*17+3, **kwargs)
            src = layers[0]; det_list = list(layers[-1])
            if not det_list: continue
            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys)/len(all_ys)
            mid = len(layers)//2
            cands = sorted([i for i in layers[mid] if positions[i][1] > cy+1],
                           key=lambda i: -positions[i][1])
            mn = cands[:target_n]
            if not mn: continue
            field = compute_field(positions, adj, mn)
            free_f = [0.0]*len(positions)
            shifts = []
            for k in K_BAND:
                am = propagate(positions, adj, field, src, k)
                af = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
            if shifts: per_seed.append((len(mn), sum(shifts)/len(shifts)))
        if per_seed:
            actual_n = per_seed[0][0]
            vals = [v for _, v in per_seed]
            avg = sum(vals)/len(vals)
            if avg > 0: results.append((actual_n, avg))
    if len(results) >= 3:
        log_n = [math.log(n) for n, _ in results]
        log_s = [math.log(s) for _, s in results]
        np_ = len(log_n)
        sx, sy = sum(log_n), sum(log_s)
        sxy = sum(x*y for x, y in zip(log_n, log_s))
        sxx = sum(x*x for x in log_n)
        denom = np_*sxx - sx*sx
        if abs(denom) > 1e-10: return (np_*sxy - sx*sy)/denom
    return None


def main():
    print("=" * 70)
    print("HIERARCHICAL ALPHA STUDY")
    print("=" * 70)
    print()

    # Test 1: Leak sweep
    print("TEST 1: Alpha vs leak parameter (3D hierarchical, 20 seeds)")
    print(f"  {'leak':>6s}  {'alpha':>7s}")
    print(f"  {'-'*16}")
    for leak in [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.50, 1.00]:
        alpha = measure_alpha(gen_3d_hierarchical, n_seeds=20, leak=leak)
        print(f"  {leak:6.2f}  {alpha:7.3f}" if alpha else f"  {leak:6.2f}  FAIL")
    print()

    # Test 2: Density convergence
    print("TEST 2: Alpha vs density at leak=0.05 (convergence check)")
    print(f"  {'npl':>5s}  {'radius':>6s}  {'alpha':>7s}")
    print(f"  {'-'*22}")
    configs = [(15, 5.0), (25, 4.0), (40, 3.2), (60, 2.7), (80, 2.4)]
    alphas = []
    for npl, r in configs:
        alpha = measure_alpha(gen_3d_hierarchical, n_seeds=20, npl=npl, r=r, leak=0.05)
        if alpha is not None:
            alphas.append(alpha)
            print(f"  {npl:5d}  {r:6.1f}  {alpha:7.3f}")
        else:
            print(f"  {npl:5d}  {r:6.1f}  FAIL")

    if len(alphas) >= 3:
        last3 = alphas[-3:]
        spread = max(last3) - min(last3)
        mean_a = sum(last3)/3
        print(f"\n  Last 3: {', '.join(f'{a:.3f}' for a in last3)}")
        print(f"  Spread: {spread:.3f}, Mean: {mean_a:.3f}")
        if spread < 0.15:
            print(f"  → CONVERGING to alpha ≈ {mean_a:.2f}")
        else:
            print(f"  → NOT CONVERGED")
    print()

    # Test 3: Head-to-head with modular at matched density
    print("TEST 3: Hierarchical vs modular at matched density (npl=30, 20 seeds)")
    print(f"  {'family':>25s}  {'alpha':>7s}")
    print(f"  {'-'*35}")

    families = [
        ("Modular gap=3", gen_3d_modular, {"gap": 3.0}),
        ("Modular gap=5", gen_3d_modular, {"gap": 5.0}),
        ("Hierarchical leak=0.02", gen_3d_hierarchical, {"leak": 0.02}),
        ("Hierarchical leak=0.05", gen_3d_hierarchical, {"leak": 0.05}),
        ("Hierarchical leak=0.10", gen_3d_hierarchical, {"leak": 0.10}),
    ]
    for name, gen_fn, kwargs in families:
        alpha = measure_alpha(gen_fn, n_seeds=20, **kwargs)
        print(f"  {name:>25s}  {alpha:7.3f}" if alpha else f"  {name:>25s}  FAIL")

    print()
    print("=" * 70)
    print("KEY QUESTION: does hierarchical alpha converge near 1.0?")
    print("If yes: channel separation without hard gap gives F~M")
    print("=" * 70)


if __name__ == "__main__":
    main()
