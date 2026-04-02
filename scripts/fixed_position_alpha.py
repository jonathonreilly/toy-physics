#!/usr/bin/env python3
"""Fixed-position mass scaling: clean alpha measurement across families.

The hierarchical alpha=0.71 was flagged as mass-position confounded.
This script uses FIXED position (cy+3) for all mass counts, varying
only count while keeping the spatial center constant.

This is the same methodology that caught the pruning alpha confound
(PR #23) — the clean approach.

PStack experiment: fixed-position-alpha
"""

from __future__ import annotations
import cmath, math, random
from collections import defaultdict, deque

BETA = 0.8; K_BAND = (3.0, 5.0, 7.0)


def gen_3d(n_layers=15, npl=30, yz_range=10.0, r=3.5, rng_seed=42,
           gap=0.0, leak=0.0, xlink=0.02):
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
                elif leak > 0 and layer > bl:
                    y = rng.uniform(-yz_range, yz_range)
                else: y = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if gap > 0 and layer > bl and round(positions[pi][0]) > bl:
                            same = positions[idx][1]*positions[pi][1] > 0
                            if same and d <= r: adj[pi].append(idx)
                            elif not same and d <= 2*r and rng.random() < xlink: adj[pi].append(idx)
                        elif leak > 0 and layer > bl and round(positions[pi][0]) > bl:
                            same = positions[idx][1]*positions[pi][1] > 0
                            threshold = r if same else r*leak
                            if d <= threshold: adj[pi].append(idx)
                        elif d <= r: adj[pi].append(idx)
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
            theta = math.acos(min(max(dx/L,-1),1)); w = math.exp(-BETA*theta*theta)
            lf = 0.5*(field[i]+field[j]); dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L,0)); act = dl-ret
            amps[j] += amps[i]*cmath.exp(1j*k*act)*w/L
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list: p = abs(amps[d])**2; total += p; wy += p*positions[d][1]
    return wy/total if total > 1e-30 else 0.0


def measure_alpha_fixed_position(gen_fn, n_seeds=24, target_y_offset=3.0, **gen_kwargs):
    """Fixed-position mass scaling: all mass counts centered at cy+target_y_offset."""
    mass_counts = [2, 4, 6, 8, 12, 16]
    results = []

    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layers = gen_fn(rng_seed=seed*17+3, **gen_kwargs)
            src = layers[0]; det_list = list(layers[-1])
            if not det_list: continue
            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys)/len(all_ys)
            mid = len(layers)//2

            # FIXED POSITION: sort by distance to cy+target_y_offset, take closest target_n
            target_y = cy + target_y_offset
            cands = sorted([i for i in layers[mid] if positions[i][1] > cy+1],
                           key=lambda i: abs(positions[i][1] - target_y))
            mn = cands[:target_n]
            if len(mn) < target_n: continue

            field = compute_field(positions, adj, mn)
            free_f = [0.0]*len(positions)
            shifts = []
            for k in K_BAND:
                am = propagate(positions, adj, field, src, k)
                af = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
            if shifts: per_seed.append(sum(shifts)/len(shifts))

        if per_seed:
            avg = sum(per_seed)/len(per_seed)
            se = (sum((s-avg)**2 for s in per_seed)/len(per_seed))**0.5/len(per_seed)**0.5
            t = avg/se if se > 1e-10 else 0
            results.append((target_n, avg, se, t))

    # Fit alpha
    pos_results = [(n, s) for n, s, _, _ in results if s > 0]
    alpha = None
    if len(pos_results) >= 3:
        log_n = [math.log(n) for n, _ in pos_results]
        log_s = [math.log(s) for _, s in pos_results]
        np_ = len(log_n); sx, sy = sum(log_n), sum(log_s)
        sxy = sum(x*y for x, y in zip(log_n, log_s)); sxx = sum(x*x for x in log_n)
        denom = np_*sxx - sx*sx
        if abs(denom) > 1e-10: alpha = (np_*sxy - sx*sy)/denom

    return alpha, results


def main():
    n_seeds = 24
    print("=" * 70)
    print("FIXED-POSITION MASS SCALING (24 seeds)")
    print("  All mass counts at cy+3.0, sorted by distance to target")
    print("  This is the clean methodology from PR #23")
    print("=" * 70)
    print()

    families = [
        ("Uniform", {}),
        ("Modular gap=3", {"gap": 3.0}),
        ("Modular gap=5", {"gap": 5.0}),
        ("Hierarchical leak=0.05", {"leak": 0.05}),
        ("Hierarchical leak=0.10", {"leak": 0.10}),
    ]

    print(f"  {'family':>25s}  {'alpha':>7s}  (fixed-position clean)")
    print(f"  {'-'*38}")

    for name, kwargs in families:
        alpha, results = measure_alpha_fixed_position(gen_3d, n_seeds=n_seeds, **kwargs)
        if alpha is not None:
            print(f"  {name:>25s}  {alpha:7.3f}")
        else:
            print(f"  {name:>25s}  FAIL")

    print()
    print("  Detail by mass count:")
    print()

    for name, kwargs in families:
        alpha, results = measure_alpha_fixed_position(gen_3d, n_seeds=n_seeds, **kwargs)
        print(f"  [{name}] alpha={'%.3f'%alpha if alpha else 'FAIL'}")
        print(f"  {'n':>4s}  {'shift':>8s}  {'SE':>6s}  {'t':>5s}")
        print(f"  {'-'*26}")
        for n, s, se, t in results:
            print(f"  {n:4d}  {s:+8.4f}  {se:6.4f}  {t:+5.2f}")
        print()

    print("=" * 70)
    print("Compare: earlier confounded values → fixed-position values")
    print("  Uniform:     0.57 → ?")
    print("  Modular g=5: 0.94 → ?")
    print("  Hierarchical: 0.71 → ?")
    print("=" * 70)


if __name__ == "__main__":
    main()
