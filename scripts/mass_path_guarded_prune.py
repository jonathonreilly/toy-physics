#!/usr/bin/env python3
"""Mass-path-guarded pruning: preserve mass-to-detector amplitude flow.

The gravity sign flip on pruned graphs happens because pruning severs
paths connecting the mass region to detectors. A guard that monitors
the mass-coupled amplitude at detectors (not just total detector reach)
should prevent the flip.

Guard: after each pruning iteration, propagate WITH mass field and check
that the gravity signal hasn't flipped. If it has, undo that iteration.

This is narrower than the total-detector-reach guard (which was too
conservative and blocked all pruning). It only intervenes when gravity
specifically degrades.

PStack experiment: mass-path-guarded-prune
"""

from __future__ import annotations

import cmath
import math
import random
from collections import defaultdict, deque

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_YBINS = 8
LAM = 10.0


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


def gravity_signal(positions, adj, mass_nodes, src, det_list):
    """Quick gravity check: mean shift across k-band."""
    field = compute_field(positions, adj, mass_nodes)
    free_f = [0.0] * len(positions)
    shifts = []
    for k in K_BAND:
        am = propagate(positions, adj, field, src, k)
        af = propagate(positions, adj, free_f, src, k)
        shifts.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
    return sum(shifts)/len(shifts) if shifts else 0.0


def mass_path_guarded_prune(positions, adj, layer_indices, mass_nodes,
                             quantile=0.10, max_iter=3):
    """Prune with gravity-preservation guard.

    After each pruning iteration, check if gravity signal stays positive.
    If it flips, undo that iteration and stop.
    """
    n = len(positions); n_layers = len(layer_indices); bl_idx = n_layers//3
    all_ys = [positions[i][1] for i in range(n)]; cy = sum(all_ys)/len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
    if not slit_a or not slit_b: return adj, 0
    base_blocked = set(barrier) - set(slit_a+slit_b)
    blocked_a = base_blocked | set(slit_b); det_set = set(layer_indices[-1])
    field_zero = [0.0]*n
    current_adj = dict(adj); total_removed = 0
    src = layer_indices[0]; det_list = list(layer_indices[-1])

    # Baseline gravity
    base_grav = gravity_signal(positions, current_adj, mass_nodes, src, det_list)

    for iteration in range(max_iter):
        amps_a = propagate(positions, current_adj, field_zero, src, 5.0, blocked_a)
        amps_b = propagate(positions, current_adj, field_zero, src, 5.0, base_blocked|set(slit_a))
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

        # Tentative prune
        tentative_adj = {}
        for i, nbs in current_adj.items():
            if i in remove_set: continue
            filtered = [j for j in nbs if j not in remove_set]
            if filtered: tentative_adj[i] = filtered

        # Check gravity signal
        new_grav = gravity_signal(positions, tentative_adj, mass_nodes, src, det_list)

        if new_grav < 0 and base_grav > 0:
            # Gravity flipped — undo and stop
            break

        total_removed += len(remove_set)
        current_adj = tentative_adj

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


def same_graph_joint(nl, quantile, guarded, n_seeds=16):
    grav_base = []; grav_prune = []; pur_base = []; pur_prune = []
    for seed in range(n_seeds):
        positions, adj_orig, layers = gen_dense_3d(n_layers=nl, rng_seed=seed*13+5)
        n = len(positions); n_act = len(layers); bl_idx = n_act//3
        src = layers[0]; det_list = list(layers[-1])
        if not det_list or n_act < 7: continue
        all_ys = [positions[i][1] for i in range(n)]; cy = sum(all_ys)/len(all_ys)
        grav_idx = 2*n_act//3
        mass = sorted([i for i in layers[grav_idx] if positions[i][1] > cy+2],
                       key=lambda i: abs(positions[i][1]-(cy+3)))[:8]
        if len(mass) < 8: continue

        gb = gravity_signal(positions, adj_orig, mass, src, det_list)
        grav_base.append(gb)

        if guarded:
            adj_p, _ = mass_path_guarded_prune(positions, adj_orig, layers, mass,
                                                quantile=quantile, max_iter=3)
        else:
            # Plain adaptive
            adj_p = dict(adj_orig)
            barrier = layers[bl_idx]
            slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
            slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
            if slit_a and slit_b:
                base_blocked = set(barrier) - set(slit_a+slit_b)
                blocked_a = base_blocked | set(slit_b); det_set = set(layers[-1])
                field_zero = [0.0]*n
                for _ in range(3):
                    amps_a = propagate(positions, adj_p, field_zero, src, 5.0, blocked_a)
                    amps_b = propagate(positions, adj_p, field_zero, src, 5.0, base_blocked|set(slit_a))
                    node_d = []
                    for li in range(bl_idx+1, n_act-1):
                        for i in layers[li]:
                            if i in det_set: continue
                            pa, pb = abs(amps_a[i])**2, abs(amps_b[i])**2
                            total = pa+pb; D = abs(pa-pb)/total if total > 1e-30 else 0.0
                            node_d.append((i, D))
                    if not node_d: break
                    node_d.sort(key=lambda x: x[1])
                    n_remove = max(1, int(len(node_d)*quantile))
                    remove_set = set(idx for idx, _ in node_d[:n_remove])
                    new_adj = {}
                    for i, nbs in adj_p.items():
                        if i in remove_set: continue
                        filtered = [j for j in nbs if j not in remove_set]
                        if filtered: new_adj[i] = filtered
                    adj_p = new_adj

        gp = gravity_signal(positions, adj_p, mass, src, det_list)
        grav_prune.append(gp)

        # Decoherence
        barrier = layers[bl_idx]
        slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
        slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
        if not slit_a or not slit_b: continue
        blocked = set(barrier) - set(slit_a+slit_b)
        blocked_a = blocked|set(slit_b); blocked_b = blocked|set(slit_a)
        bath_mass = []
        for li in range(bl_idx+1, min(n_act, bl_idx+3)):
            for i in layers[li]:
                if abs(positions[i][1]-cy) <= 3: bath_mass.append(i)
        grav_mass_d = [i for i in layers[grav_idx] if positions[i][1] > cy+1]
        all_mass = list(set(bath_mass)|set(grav_mass_d))

        for adj_test, pur_list in [(adj_orig, pur_base), (adj_p, pur_prune)]:
            field_d = compute_field(positions, adj_test, all_mass) if all_mass else [0.0]*n
            mid_nodes = [i for li in range(bl_idx+1, n_act-1) for i in layers[li]
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
        "grav_flip_count": sum(1 for gb, gp in zip(grav_base, grav_prune) if gb > 0 and gp < 0),
        "n": min(len(grav_base), len(pur_base)),
    }


def main():
    print("=" * 70)
    print("MASS-PATH-GUARDED PRUNING: prevent gravity sign flip")
    print("  Guard: if pruning iteration flips gravity, undo and stop")
    print("=" * 70)
    print()

    for nl in [80, 100]:
        print(f"  N={nl}")
        print(f"  {'mode':>25s}  {'grav_b':>7s}  {'grav_p':>7s}  "
              f"{'pur_b':>6s}  {'pur_p':>6s}  {'flips':>5s}  {'n':>3s}")
        print(f"  {'-'*60}")
        for label, guarded in [("Plain adaptive q=0.10", False),
                                ("Mass-path guarded q=0.10", True)]:
            r = same_graph_joint(nl, 0.10, guarded, n_seeds=16)
            print(f"  {label:>25s}  {r['grav_base']:+7.3f}  {r['grav_prune']:+7.3f}  "
                  f"{r['pur_base']:6.4f}  {r['pur_prune']:6.4f}  "
                  f"{r['grav_flip_count']:5d}  {r['n']:3d}")
        print()

    print("=" * 70)
    print("KEY: does the guard reduce flip count while preserving decoherence?")
    print("=" * 70)


if __name__ == "__main__":
    main()
