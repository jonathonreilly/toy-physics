#!/usr/bin/env python3
"""Coupled birth/death emergence: constant node count, migrating gap.

Soft pruning is asymptotically closed (backlog update). The next
serious variant: coupled birth/death where removed nodes are
REPLACED at high-D positions, keeping total node count constant.

Rule per iteration:
  1. Propagate from each slit, compute D(i) at post-barrier nodes
  2. Remove bottom quantile of D (death)
  3. For each removed node: spawn a new node at the same x-layer,
     with y drawn from the distribution of surviving high-D nodes
     and z drawn uniformly
  4. Connect the new node to neighbors within connect_radius
  5. Repeat

Physics: "events without which-path information are replaced by
events at positions where which-path information is high."

Key advantage: total node count stays constant → connectivity
doesn't degrade → should survive at larger N than pruning-only.

PStack experiment: birth-death-emergence
"""

from __future__ import annotations
import cmath, math, random
from collections import defaultdict, deque

BETA = 0.8; N_YBINS = 8; LAM = 10.0; K_BAND = (3.0, 5.0, 7.0)


def gen_3d(n_layers=20, npl=30, yz_range=10.0, r=3.5, rng_seed=42):
    rng = random.Random(rng_seed)
    positions = []; adj = defaultdict(list); layers = []
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


def birth_death_step(positions, adj, layer_indices, quantile=0.10,
                     connect_radius=3.5, rng=None):
    """One birth/death step: remove low-D, spawn at high-D positions."""
    if rng is None:
        rng = random.Random(42)

    n = len(positions)
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3

    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys) / len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
    if not slit_a or not slit_b:
        return positions, adj, layer_indices, 0

    base_blocked = set(barrier) - set(slit_a + slit_b)
    blocked_a = base_blocked | set(slit_b)
    det_set = set(layer_indices[-1])
    field = [0.0] * n

    amps_a = propagate(positions, adj, field, layer_indices[0], 5.0, blocked_a)
    amps_b = propagate(positions, adj, field, layer_indices[0], 5.0,
                       base_blocked | set(slit_a))

    # Compute D at each post-barrier node, grouped by layer
    layer_node_d = defaultdict(list)  # layer_idx -> [(node_id, D)]
    for li in range(bl_idx + 1, n_layers - 1):
        for i in layer_indices[li]:
            if i in det_set:
                continue
            pa = abs(amps_a[i])**2
            pb = abs(amps_b[i])**2
            total = pa + pb
            D = abs(pa - pb) / total if total > 1e-30 else 0.0
            layer_node_d[li].append((i, D))

    # Per-layer birth/death
    new_positions = list(positions)
    new_adj = dict(adj)
    new_layer_indices = [list(l) for l in layer_indices]
    total_births = 0

    for li, node_d_list in layer_node_d.items():
        if not node_d_list:
            continue

        node_d_list.sort(key=lambda x: x[1])
        n_remove = max(1, int(len(node_d_list) * quantile))

        # Death: remove lowest-D nodes
        remove_set = set(idx for idx, _ in node_d_list[:n_remove])

        # High-D survivors: use their y-distribution as birth template
        survivors = [(idx, D) for idx, D in node_d_list if idx not in remove_set and D > 0]
        if not survivors:
            continue

        # Remove dead nodes from adj
        for i in remove_set:
            if i in new_adj:
                del new_adj[i]
        for i in new_adj:
            new_adj[i] = [j for j in new_adj[i] if j not in remove_set]
        for i in remove_set:
            if i in new_layer_indices[li]:
                new_layer_indices[li].remove(i)

        # Birth: spawn new nodes at high-D y-positions
        survivor_ys = [new_positions[idx][1] for idx, _ in survivors]
        x_layer = float(li)

        for _ in range(n_remove):
            # Draw y from survivor distribution (pick random survivor's y + small noise)
            template_y = rng.choice(survivor_ys) + rng.gauss(0, 0.5)
            new_z = rng.uniform(-10.0, 10.0)

            new_idx = len(new_positions)
            new_positions.append((x_layer, template_y, new_z))
            new_layer_indices[li].append(new_idx)

            # Connect to neighbors in previous and same layer
            for target_li in range(max(0, li-1), min(n_layers, li+2)):
                for pi in new_layer_indices[target_li]:
                    if pi == new_idx:
                        continue
                    d = math.sqrt(sum((a-b)**2 for a, b in
                                      zip(new_positions[new_idx], new_positions[pi])))
                    if d <= connect_radius:
                        # Forward edges only (pi → new if pi.x < new.x, or new → pi if pi.x > new.x)
                        if new_positions[pi][0] < x_layer:
                            if pi not in new_adj:
                                new_adj[pi] = []
                            new_adj[pi].append(new_idx)
                        elif new_positions[pi][0] > x_layer:
                            if new_idx not in new_adj:
                                new_adj[new_idx] = []
                            new_adj[new_idx].append(pi)

            total_births += 1

    return new_positions, new_adj, new_layer_indices, total_births


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes if m < len(positions)]
    if not ys: return 0.0
    y_min, y_max = min(ys)-0.01, max(ys)+0.01; bw = (y_max-y_min)/N_YBINS
    ba = [0j]*N_YBINS; bb = [0j]*N_YBINS
    for m in mid_nodes:
        if m >= len(positions): continue
        b = max(0, min(N_YBINS-1, int((positions[m][1]-y_min)/bw)))
        ba[b] += amps_a[m] if m < len(amps_a) else 0j
        bb[b] += amps_b[m] if m < len(amps_b) else 0j
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    d = sum(abs(a)**2 for a in ba) + sum(abs(b)**2 for b in bb)
    return S/d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            a1 = amps_a[d1] if d1 < len(amps_a) else 0j
            a2 = amps_a[d2] if d2 < len(amps_a) else 0j
            b1 = amps_b[d1] if d1 < len(amps_b) else 0j
            b2 = amps_b[d2] if d2 < len(amps_b) else 0j
            rho[(d1,d2)] = a1*a2.conjugate() + b1*b2.conjugate() + D*a1*b2.conjugate() + D*b1*a2.conjugate()
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
    blocked_a = blocked|set(slit_b); blocked_b = blocked|set(slit_a)
    bath_mass = []
    for li in range(bl_idx+1, min(n_layers, bl_idx+3)):
        for i in layer_indices[li]:
            if i < n and abs(positions[i][1]-cy) <= 3: bath_mass.append(i)
    grav_idx = 2*n_layers//3
    grav_mass = [i for i in layer_indices[grav_idx] if i < n and positions[i][1] > cy+1]
    all_mass = list(set(bath_mass)|set(grav_mass))
    field = compute_field(positions, adj, all_mass) if all_mass else [0.0]*n
    mid_nodes = [i for li in range(bl_idx+1, n_layers-1) for i in layer_indices[li]
                 if i not in blocked and i not in set(det_list) and i < n]
    if len(mid_nodes) < 4: return math.nan
    pur_list = []
    for k in K_BAND:
        aa = propagate(positions, adj, field, src, k, blocked_a)
        ab = propagate(positions, adj, field, src, k, blocked_b)
        Sn = cl_contrast(aa, ab, mid_nodes, positions)
        D = math.exp(-LAM**2*Sn); pur = cl_purity(aa, ab, D, det_list)
        if not math.isnan(pur): pur_list.append(pur)
    return sum(pur_list)/len(pur_list) if pur_list else math.nan


def gap_metric(positions, layer_indices):
    n_layers = len(layer_indices); bl_idx = n_layers//3; det_set = set(layer_indices[-1])
    ys = []
    for li in range(bl_idx+1, n_layers-1):
        for i in layer_indices[li]:
            if i not in det_set and i < len(positions): ys.append(positions[i][1])
    if len(ys) < 10: return 0.0
    ys.sort()
    return max(ys[i]-ys[i-1] for i in range(1, len(ys)))


def main():
    n_seeds = 16
    print("=" * 74)
    print("COUPLED BIRTH/DEATH EMERGENCE")
    print("  Death: remove low-D nodes")
    print("  Birth: spawn at high-D y-positions")
    print("  Node count stays constant → connectivity preserved")
    print("=" * 74)
    print()

    n_layers_list = [30, 40, 50, 60, 80]
    n_iter = 3

    for label, use_bd in [("Uniform baseline", False),
                           ("Birth/death q=0.10, 3 iter", True)]:
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_cl':>8s}  {'gap':>6s}  {'births':>8s}  {'n':>3s}")
        print(f"  {'-'*36}")

        for nl in n_layers_list:
            purs = []; gaps = []; total_births = []
            for seed in range(n_seeds):
                rng = random.Random(seed*31+7)
                positions, adj, layers = gen_3d(n_layers=nl, rng_seed=seed*13+5)

                if use_bd:
                    births = 0
                    for _ in range(n_iter):
                        positions, adj, layers, b = birth_death_step(
                            positions, adj, layers, quantile=0.10,
                            connect_radius=3.5, rng=rng)
                        births += b
                    total_births.append(births)
                else:
                    total_births.append(0)

                pur = measure_decoherence(positions, adj, layers)
                if not math.isnan(pur):
                    purs.append(pur)
                    gaps.append(gap_metric(positions, layers))

            if purs:
                mp = sum(purs)/len(purs)
                mg = sum(gaps)/len(gaps) if gaps else 0
                mb = sum(total_births)/len(total_births)
                print(f"  {nl:4d}  {mp:8.4f}  {mg:6.2f}  {mb:8.1f}  {len(purs):3d}")
            else: print(f"  {nl:4d}  FAIL")

        print()

    # Paired comparison
    print("PAIRED COMPARISON at N=60 (16 seeds)")
    print(f"  {'rule':>25s}  {'pur_cl':>8s}")
    print(f"  {'-'*36}")

    for label, use_bd in [("Uniform", False), ("Birth/death", True)]:
        purs = []
        for seed in range(n_seeds):
            rng = random.Random(seed*31+7)
            positions, adj, layers = gen_3d(n_layers=60, rng_seed=seed*13+5)
            if use_bd:
                for _ in range(3):
                    positions, adj, layers, _ = birth_death_step(
                        positions, adj, layers, quantile=0.10,
                        connect_radius=3.5, rng=rng)
            pur = measure_decoherence(positions, adj, layers)
            if not math.isnan(pur): purs.append(pur)
        if purs:
            print(f"  {label:>25s}  {sum(purs)/len(purs):8.4f}")

    print()
    print("=" * 74)
    print("KEY: does birth/death survive better than pruning-only at N=80?")
    print("  Pruning-only: delta=-0.017 at N=80, dies at N=100")
    print("  Birth/death should maintain connectivity → better at large N")
    print("=" * 74)


if __name__ == "__main__":
    main()
