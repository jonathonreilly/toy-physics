#!/usr/bin/env python3
"""Deep overnight batch: push emergence frontiers.

A. N=100 emergence: does the adaptive quantile improvement survive?
B. Cross-family emergence: does pruning help on hierarchical DAGs?
C. 4D emergence: does pruning help in the strongest decoherence dimension?
D. Gravity survival: does pruning preserve the gravity signal?

PStack experiment: overnight-deep-batch
"""

from __future__ import annotations
import cmath, math, random
from collections import defaultdict, deque

BETA = 0.8; N_YBINS = 8; LAM = 10.0; K_BAND = (3.0, 5.0, 7.0)


def gen_3d(n_layers=20, npl=30, yz_range=10.0, r=3.5, rng_seed=42,
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
                        elif leak > 0 and layer > bl and round(positions[pi][0]) > bl:
                            same = positions[idx][1]*positions[pi][1] > 0
                            threshold = r if same else r*leak
                            if d <= threshold: adj[pi].append(idx)
                        elif d <= r: adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def gen_4d(n_layers=15, npl=25, sr=8.0, r=4.5, rng_seed=42, gap=5.0, xlink=0.02):
    rng = random.Random(rng_seed)
    positions = []; adj = defaultdict(list); layers = []
    bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0, 0.0)); nodes.append(len(positions)-1)
        else:
            for ni in range(npl):
                z = rng.uniform(-sr, sr); w = rng.uniform(-sr, sr)
                if gap > 0 and layer > bl:
                    y = rng.uniform(gap/2, sr) if ni < npl//2 else rng.uniform(-sr, -gap/2)
                else: y = rng.uniform(-sr, sr)
                idx = len(positions); positions.append((x, y, z, w)); nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if gap > 0 and layer > bl and round(positions[pi][0]) > bl:
                            same = positions[idx][1]*positions[pi][1] > 0
                            if same and d <= r: adj[pi].append(idx)
                            elif not same and d <= 2*r and rng.random() < xlink: adj[pi].append(idx)
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


def adaptive_prune(positions, adj, layer_indices, quantile=0.10, max_iter=3):
    n = len(positions); n_layers = len(layer_indices); bl_idx = n_layers//3
    all_ys = [positions[i][1] for i in range(n)]; cy = sum(all_ys)/len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
    if not slit_a or not slit_b: return adj, 0
    base_blocked = set(barrier) - set(slit_a+slit_b)
    blocked_a = base_blocked | set(slit_b)
    det_set = set(layer_indices[-1]); field = [0.0]*n
    current_adj = dict(adj); total_removed = 0
    for _ in range(max_iter):
        amps_a = propagate(positions, current_adj, field, layer_indices[0], 5.0, blocked_a)
        amps_b = propagate(positions, current_adj, field, layer_indices[0], 5.0,
                           base_blocked | set(slit_a))
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


def measure_decoherence(positions, adj, layer_indices):
    n = len(positions); n_layers = len(layer_indices); bl_idx = n_layers//3
    src = layer_indices[0]; det_list = list(layer_indices[-1])
    if not det_list or n_layers < 7: return math.nan
    all_ys = [positions[i][1] for i in range(n)]; cy = sum(all_ys)/len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
    if not slit_a or not slit_b: return math.nan
    blocked = set(barrier) - set(slit_a+slit_b)
    blocked_a = blocked | set(slit_b); blocked_b = blocked | set(slit_a)
    bath_mass = []
    for li in range(bl_idx+1, min(n_layers, bl_idx+3)):
        for i in layer_indices[li]:
            if abs(positions[i][1]-cy) <= 3: bath_mass.append(i)
    grav_idx = 2*n_layers//3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1]
    all_mass = list(set(bath_mass)|set(grav_mass))
    field = compute_field(positions, adj, all_mass) if all_mass else [0.0]*n
    mid_nodes = [i for li in range(bl_idx+1, n_layers-1) for i in layer_indices[li]
                 if i not in blocked and i not in set(det_list)]
    if len(mid_nodes) < 4: return math.nan
    pur_list = []
    for k in K_BAND:
        aa = propagate(positions, adj, field, src, k, blocked_a)
        ab = propagate(positions, adj, field, src, k, blocked_b)
        Sn = cl_contrast(aa, ab, mid_nodes, positions)
        D = math.exp(-LAM**2*Sn); pur = cl_purity(aa, ab, D, det_list)
        if not math.isnan(pur): pur_list.append(pur)
    return sum(pur_list)/len(pur_list) if pur_list else math.nan


def measure_gravity(positions, adj, layer_indices, n_mass=8):
    n = len(positions); src = layer_indices[0]; det_list = list(layer_indices[-1])
    if not det_list: return 0.0
    all_ys = [positions[i][1] for i in range(n)]; cy = sum(all_ys)/len(all_ys)
    grav_idx = 2*len(layer_indices)//3
    mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1][:n_mass]
    if not mass: return 0.0
    field = compute_field(positions, adj, mass)
    free_f = [0.0]*n
    deltas = []
    for k in K_BAND:
        am = propagate(positions, adj, field, src, k)
        af = propagate(positions, adj, free_f, src, k)
        deltas.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
    return sum(deltas)/len(deltas) if deltas else 0.0


def run_emergence(gen_fn, label, n_layers_list, n_seeds=16, **gen_kwargs):
    print(f"  [{label}]")
    print(f"  {'N':>4s}  {'base':>8s}  {'pruned':>8s}  {'delta':>8s}  {'removed':>8s}  {'n':>3s}")
    print(f"  {'-'*46}")
    for nl in n_layers_list:
        base_purs = []; prune_purs = []; removals = []
        for seed in range(n_seeds):
            positions, adj, layers = gen_fn(n_layers=nl, rng_seed=seed*13+5, **gen_kwargs)
            pb = measure_decoherence(positions, adj, layers)
            adj_e, removed = adaptive_prune(positions, adj, layers, quantile=0.10, max_iter=3)
            pp = measure_decoherence(positions, adj_e, layers)
            if not math.isnan(pb) and not math.isnan(pp):
                base_purs.append(pb); prune_purs.append(pp); removals.append(removed)
        if base_purs:
            mb = sum(base_purs)/len(base_purs); mp = sum(prune_purs)/len(prune_purs)
            mr = sum(removals)/len(removals)
            print(f"  {nl:4d}  {mb:8.4f}  {mp:8.4f}  {mp-mb:+8.4f}  {mr:8.1f}  {len(base_purs):3d}")
        else: print(f"  {nl:4d}  FAIL")
    print()


def run_gravity_check(n_seeds=16):
    """Check if pruning preserves gravity signal."""
    print("  [Gravity survival under pruning (N=30)]")
    print(f"  {'config':>25s}  {'grav_d':>8s}  {'t':>5s}")
    print(f"  {'-'*42}")
    for label, use_prune in [("Uniform (no prune)", False), ("Uniform + prune q=0.10", True)]:
        grav_seeds = []
        for seed in range(n_seeds):
            positions, adj, layers = gen_3d(n_layers=30, rng_seed=seed*13+5)
            if use_prune:
                adj, _ = adaptive_prune(positions, adj, layers, quantile=0.10, max_iter=3)
            gd = measure_gravity(positions, adj, layers)
            grav_seeds.append(gd)
        avg = sum(grav_seeds)/len(grav_seeds)
        se = (sum((d-avg)**2 for d in grav_seeds)/len(grav_seeds))**0.5/len(grav_seeds)**0.5
        t = avg/se if se > 1e-10 else 0
        v = "GRAV" if avg > 0 and t > 2 else "weak"
        print(f"  {label:>25s}  {avg:+8.4f}  {t:+5.2f}  {v}")
    print()


def main():
    print("=" * 74)
    print("DEEP OVERNIGHT BATCH: Emergence frontiers")
    print("=" * 74)
    print()

    # A: Push to N=100
    print("EXPERIMENT A: Emergence at N=100 (3D uniform)")
    run_emergence(gen_3d, "3D Uniform", [30, 40, 60, 80, 100], n_seeds=16)

    # B: Cross-family emergence
    print("EXPERIMENT B: Cross-family emergence")
    run_emergence(gen_3d, "Hierarchical leak=0.05", [30, 40, 60, 80], n_seeds=16, leak=0.05)
    run_emergence(gen_3d, "Modular gap=3", [30, 40, 60, 80], n_seeds=16, gap=3.0)

    # C: 4D emergence
    print("EXPERIMENT C: 4D emergence (modular gap=5)")
    run_emergence(gen_4d, "4D Modular gap=5", [12, 15, 18, 20, 25], n_seeds=16, gap=5.0)

    # D: Gravity survival
    print("EXPERIMENT D: Does pruning preserve gravity?")
    run_gravity_check(n_seeds=16)

    print("=" * 74)
    print("DEEP OVERNIGHT BATCH COMPLETE")
    print("=" * 74)


if __name__ == "__main__":
    main()
