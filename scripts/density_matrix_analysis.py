#!/usr/bin/env python3
"""Density matrix analysis: what distinguishes ALL THREE seeds?

Instead of predicting from structure, examine the AMPLITUDE-LEVEL
difference. Compute the detector-conditioned reduced density matrix:
  ρ_det(y1,y2) = Σ_env ψ*(y1,env) ψ(y2,env)  [two-register, detector-only]

Decoherence = suppression of off-diagonal elements.
The purity Tr(ρ²) measures how mixed the detector-conditioned state is.
  Purity = 1 → pure (no decoherence)
  Purity < 1 → mixed (decoherence)

Compare purity of ALL THREE seeds vs non-seeds.

PStack experiment: density-matrix-analysis
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.two_register_decoherence import compute_field


def propagate_two_register_full(positions, adj, field, src, det, k, mass_set,
                                blocked=None):
    """Return full (det_node, env) → amplitude state, not traced."""
    n = len(positions)
    blocked = blocked or set()

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

    state = {}
    for s in src:
        state[(s, -1)] = 1.0/len(src) + 0.0j

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

    # Extract detector entries
    det_state = {(d, env): amp for (d, env), amp in state.items() if d in det}
    return det_state


def build_post_barrier_setup(positions, adj, env_depth_layers=1, mass_y_half=3.0):
    """Build the standard source/slit/mass/detector geometry for a graph.

    `env_depth_layers` controls how many post-barrier layers carry the
    environment-coupling mass nodes. This lets size sweeps keep the environment
    region fixed or scale it with graph depth.
    """
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det = set(by_layer[layers[-1]])
    det_list = list(det)
    if not det:
        return None

    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)

    bl_idx = len(layers) // 3
    bl = layers[bl_idx]
    bi = by_layer[bl]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    si = set(sa + sb)
    blocked = set(bi) - si

    start = bl_idx + 1
    stop = min(len(layers), start + max(1, env_depth_layers))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(
            i for i in by_layer[layer]
            if abs(positions[i][1] - cy) <= mass_y_half
        )
    if len(mass_nodes) < 2:
        return None
    mass_set = set(mass_nodes)

    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    full_mass = mass_set | set(grav_mass)
    field = compute_field(positions, adj, list(full_mass))

    return {
        "n": n,
        "by_layer": by_layer,
        "layers": layers,
        "src": src,
        "det": det,
        "det_list": det_list,
        "cy": cy,
        "blocked": blocked,
        "mass_set": mass_set,
        "grav_mass": grav_mass,
        "field": field,
        "env_depth_layers": max(1, env_depth_layers),
    }


def compute_detector_metrics(det_state, det_nodes):
    """Return detector-conditioned purity metrics plus detector hit fraction."""
    envs = set(env for (d, env) in det_state.keys())

    rho = {}
    for d1 in det_nodes:
        for d2 in det_nodes:
            val = 0.0 + 0.0j
            for env in envs:
                a1 = det_state.get((d1, env), 0.0 + 0.0j)
                a2 = det_state.get((d2, env), 0.0 + 0.0j)
                val += a1.conjugate() * a2
            rho[(d1, d2)] = val

    trace = sum(rho.get((d, d), 0.0) for d in det_nodes).real
    if trace <= 1e-30:
        return math.nan, math.nan, math.nan, 0.0

    for key in rho:
        rho[key] /= trace

    purity = sum(abs(v) ** 2 for v in rho.values()).real
    diag_total = sum(abs(rho.get((d, d), 0.0)) ** 2 for d in det_nodes).real
    offdiag_total = purity - diag_total
    return purity, diag_total, offdiag_total, trace


def compute_purity(det_state, det_nodes):
    """Compute detector-conditioned purity Tr(ρ²).

    ρ(d1, d2) = Σ_env ψ*(d1,env) ψ(d2,env)
    Tr(ρ²) = Σ_{d1,d2} |ρ(d1,d2)|²
    """
    purity, diag_total, offdiag_total, _ = compute_detector_metrics(det_state, det_nodes)
    return purity, diag_total, offdiag_total


def main():
    n_layers = 15
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 20
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("DENSITY MATRIX ANALYSIS")
    print("  detector-state purity Tr(rho_det^2): 1=pure, <1=mixed")
    print("=" * 70)
    print()

    data = []

    for seed in range(n_seeds):
        positions, adj, _ = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=npl,
            y_range=y_range, connect_radius=radius,
            rng_seed=seed*11+7,
        )
        setup = build_post_barrier_setup(positions, adj, env_depth_layers=1)
        if setup is None:
            continue

        n = setup["n"]
        src = setup["src"]
        det = setup["det"]
        det_list = setup["det_list"]
        cy = setup["cy"]
        blocked = setup["blocked"]
        mass_set = setup["mass_set"]
        grav_mass = setup["grav_mass"]
        field = setup["field"]

        # k-averaged purity
        purities = []
        det_probs = []
        for k in k_band:
            det_state = propagate_two_register_full(
                positions, adj, field, src, det, k, mass_set, blocked)
            purity, diag, offdiag, det_prob = compute_detector_metrics(det_state, det_list)
            purities.append(purity)
            det_probs.append(det_prob)

        avg_purity = sum(purities)/len(purities)
        avg_det_prob = sum(det_probs)/len(det_probs)

        # Check ALL THREE (gravity + interference + decoherence)
        from scripts.two_register_decoherence import (
            pathsum_two_register, pathsum_coherent, visibility, centroid_y,
        )
        free_f = [0.0]*n

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

        vc = visibility(dict(avg_coh), positions, det_list)
        v2 = visibility(dict(avg_2reg), positions, det_list)
        vd = vc - v2
        has_all3 = attracts and v2 > 0.05 and vd > 0.02

        data.append({
            'seed': seed, 'det_purity': avg_purity, 'det_prob': avg_det_prob, 'all3': has_all3,
            'V_drop': vd, 'grav': avg_grav,
        })

    # Results
    print(f"  {'seed':>4s}  {'det_pur':>8s}  {'det_P':>8s}  {'V_drop':>8s}  {'grav':>7s}  {'all3':>4s}")
    print(f"  {'-' * 47}")
    for d in data:
        print(f"  {d['seed']:4d}  {d['det_purity']:8.4f}  {d['det_prob']:8.4f}  {d['V_drop']:+8.4f}  "
              f"{d['grav']:+7.2f}  {'Y' if d['all3'] else 'n':>4s}")

    # Compare purity
    a3 = [d for d in data if d['all3']]
    non = [d for d in data if not d['all3']]

    print()
    if a3:
        print(f"  ALL THREE detector-state purity: {sum(d['det_purity'] for d in a3)/len(a3):.4f}")
    if non:
        print(f"  Non-ALL3 detector-state purity:  {sum(d['det_purity'] for d in non)/len(non):.4f}")

    # Correlation
    purities = [d['det_purity'] for d in data]
    labels = [1 if d['all3'] else 0 for d in data]
    n_tot = len(data)
    mx = sum(purities)/n_tot
    my = sum(labels)/n_tot
    cov = sum((p-mx)*(l-my) for p, l in zip(purities, labels))/n_tot
    sx = (sum((p-mx)**2 for p in purities)/n_tot)**0.5
    sy = (sum((l-my)**2 for l in labels)/n_tot)**0.5
    corr = cov/(sx*sy) if sx > 0 and sy > 0 else 0

    print(f"  Corr(detector-state purity, all3): {corr:+.4f}")
    print()
    print("det_P = detector hit probability before conditioning")
    print("Lower detector-state purity = more detector-side decoherence")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
