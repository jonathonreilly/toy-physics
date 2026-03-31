#!/usr/bin/env python3
"""Exit-point divergence: the real predictor for two-register decoherence.

The fine env labels paths by their LAST mass node. Decoherence requires
slit-A paths to exit the mass region through different nodes than slit-B.

Measure: propagate amplitude from each slit separately through the mass,
record the exit-point distribution (amplitude-weighted last mass node).
If the distributions are different → slit-selective env → decoherence.

The divergence between exit-point distributions should predict D.

PStack experiment: exit-point-divergence
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


def exit_distribution(positions, adj, field, start_nodes, mass_set, k, blocked):
    """Propagate from start_nodes, record amplitude-weighted last-mass-node distribution."""
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

    # Track (node, last_mass_node) → amplitude
    state = {}
    for s in start_nodes:
        state[(s, -1)] = 1.0/len(start_nodes) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {env: amp for (node, env), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for env, amp in entries.items():
            new_env = i if i in mass_set else env
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
                key = (j, new_env)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    # Collect exit distribution: for each env label, sum |amp|² at all nodes
    exit_dist = defaultdict(float)
    for (node, env), amp in state.items():
        if env >= 0:  # has visited at least one mass node
            exit_dist[env] += abs(amp)**2

    total = sum(exit_dist.values())
    if total > 0:
        exit_dist = {k: v/total for k, v in exit_dist.items()}
    return dict(exit_dist)


def js_divergence(p, q):
    """Jensen-Shannon divergence between two distributions (dicts)."""
    all_keys = set(p.keys()) | set(q.keys())
    m = {k: 0.5*(p.get(k, 0) + q.get(k, 0)) for k in all_keys}
    div = 0
    for k in all_keys:
        pk = p.get(k, 0)
        qk = q.get(k, 0)
        mk = m[k]
        if pk > 0 and mk > 0:
            div += 0.5 * pk * math.log(pk/mk)
        if qk > 0 and mk > 0:
            div += 0.5 * qk * math.log(qk/mk)
    return div


def main():
    n_layers = 15
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 30
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("EXIT-POINT DIVERGENCE AS DECOHERENCE PREDICTOR")
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

        bl_idx = len(layers)//3
        bl = layers[bl_idx]
        bi = by_layer[bl]
        sa = [i for i in bi if positions[i][1] > cy+3][:3]
        sb = [i for i in bi if positions[i][1] < cy-3][:3]
        if not sa or not sb:
            continue
        si = set(sa+sb)
        blocked = set(bi) - si

        post_bl = layers[bl_idx+1]
        mass_nodes = [i for i in by_layer[post_bl] if abs(positions[i][1]-cy) <= 3]
        if len(mass_nodes) < 2:
            continue
        mass_set = set(mass_nodes)

        grav_layer = layers[2*len(layers)//3]
        grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy+1]
        full_mass = mass_set | set(grav_mass)
        field = compute_field(positions, adj, list(full_mass))
        free_f = [0.0]*n

        # Exit-point distributions for each slit (k-averaged)
        exit_a_total = defaultdict(float)
        exit_b_total = defaultdict(float)
        for k in k_band:
            ea = exit_distribution(positions, adj, field, sa, mass_set, k, blocked)
            eb = exit_distribution(positions, adj, field, sb, mass_set, k, blocked)
            for m, p in ea.items():
                exit_a_total[m] += p
            for m, p in eb.items():
                exit_b_total[m] += p

        # Normalize
        ta = sum(exit_a_total.values())
        tb = sum(exit_b_total.values())
        if ta > 0:
            exit_a_total = {k: v/ta for k, v in exit_a_total.items()}
        if tb > 0:
            exit_b_total = {k: v/tb for k, v in exit_b_total.items()}

        jsd = js_divergence(dict(exit_a_total), dict(exit_b_total))

        # How many unique exit points per slit?
        n_exit_a = len([v for v in exit_a_total.values() if v > 0.01])
        n_exit_b = len([v for v in exit_b_total.values() if v > 0.01])

        # Overlap: how much do the distributions overlap?
        all_keys = set(exit_a_total.keys()) | set(exit_b_total.keys())
        overlap = sum(min(exit_a_total.get(k, 0), exit_b_total.get(k, 0)) for k in all_keys)

        # Run path-sum for ALL THREE check
        grav_shifts = []
        for k in k_band:
            fp = pathsum_coherent(positions, adj, free_f, src, det, k)
            mp = pathsum_two_register(positions, adj, field, src, det, k,
                                     mass_set, env_mode="fine")
            grav_shifts.append(centroid_y(mp, positions)-centroid_y(fp, positions))
        avg_grav = sum(grav_shifts)/len(grav_shifts)
        attracts = False
        if grav_mass:
            gc = sum(positions[i][1] for i in grav_mass)/len(grav_mass)
            attracts = (gc-cy > 0 and avg_grav > 0.05)

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

        has_decoh = vd > 0.02
        has_all3 = attracts and v2 > 0.05 and vd > 0.02

        data.append({
            'seed': seed, 'jsd': jsd, 'overlap': overlap,
            'n_exit_a': n_exit_a, 'n_exit_b': n_exit_b,
            'V_drop': vd, 'has_decoh': has_decoh, 'has_all3': has_all3,
        })

    # Correlation
    print(f"  Seeds: {len(data)}, ALL THREE: {sum(1 for d in data if d['has_all3'])}")
    print()

    for pred in ['jsd', 'overlap', 'n_exit_a', 'n_exit_b']:
        vals = [d[pred] for d in data]
        vdrops = [d['V_drop'] for d in data]
        labels = [1 if d['has_decoh'] else 0 for d in data]
        n_tot = len(data)

        # Corr with V_drop
        mx = sum(vals)/n_tot
        my = sum(vdrops)/n_tot
        cov = sum((v-mx)*(l-my) for v, l in zip(vals, vdrops))/n_tot
        sx = (sum((v-mx)**2 for v in vals)/n_tot)**0.5
        sy = (sum((l-my)**2 for l in vdrops)/n_tot)**0.5
        corr_vd = cov/(sx*sy) if sx > 0 and sy > 0 else 0

        # Corr with has_decoh
        my2 = sum(labels)/n_tot
        cov2 = sum((v-mx)*(l-my2) for v, l in zip(vals, labels))/n_tot
        sy2 = (sum((l-my2)**2 for l in labels)/n_tot)**0.5
        corr_d = cov2/(sx*sy2) if sx > 0 and sy2 > 0 else 0

        print(f"  {pred:>12s}: corr(V_drop)={corr_vd:+.4f}, corr(decoh)={corr_d:+.4f}")

    # Show per-seed
    print()
    print(f"  {'seed':>4s}  {'JSD':>8s}  {'overlap':>8s}  {'V_drop':>8s}  {'decoh':>5s}  {'all3':>4s}")
    print(f"  {'-' * 40}")
    for d in sorted(data, key=lambda x: -x['jsd'])[:15]:
        print(f"  {d['seed']:4d}  {d['jsd']:8.4f}  {d['overlap']:8.3f}  "
              f"{d['V_drop']:+8.3f}  {'Y' if d['has_decoh'] else 'n':>5s}  "
              f"{'Y' if d['has_all3'] else 'n':>4s}")

    print()
    print("JSD = Jensen-Shannon divergence between exit-point distributions")
    print("High JSD = slits exit through different mass nodes = more decoherence")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
