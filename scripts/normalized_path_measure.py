#!/usr/bin/env python3
"""Normalized path measure: scale-free continuation quality weight.

Replace raw exp(-β×dy²) with exp(-β×(dy/L)²) — penalize slope squared.
This is scale-free: the penalty depends on the direction of the edge,
not its length. On edges of any length, the weight is the same for
the same angle.

Variants:
  A: slope² = (dy/L)²      — penalizes off-axis displacement
  B: turning = 1 - dx/L    — penalizes deviation from forward direction
  C: angle² = atan2(dy,dx)² — penalizes angle directly

All are field-independent, scale-free, and penalize transverse motion.

PStack experiment: normalized-path-measure
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
from itertools import combinations
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import build_post_barrier_setup, compute_detector_metrics
from scripts.two_register_decoherence import compute_field, centroid_y, visibility
from toy_event_physics import (
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
)


def edge_weight(dy, dx, L, beta, mode="slope"):
    """Compute the path-measure weight for an edge."""
    if mode == "slope":
        slope = dy / L if L > 0 else 0
        return math.exp(-beta * slope * slope)
    elif mode == "turning":
        forward = dx / L if L > 0 else 1
        return math.exp(-beta * (1 - forward))
    elif mode == "angle":
        angle = math.atan2(abs(dy), max(dx, 1e-10))
        return math.exp(-beta * angle * angle)
    elif mode == "raw_dy":
        return math.exp(-beta * dy * dy)
    return 1.0


def propagate_weighted(positions, adj, field, src, det, k, beta, mode,
                       blocked=None, normalize=True):
    """Corrected propagator with normalized path-measure weight."""
    n = len(positions) if isinstance(positions, list) else len(positions)
    blocked = blocked or set()

    if isinstance(positions, list):
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
                dx = x2 - x1
                dy = y2 - y1
                L = math.sqrt(dx*dx + dy*dy)
                if L < 1e-10:
                    continue
                lf = 0.5*(field[i]+field[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                w = edge_weight(dy, dx, L, beta, mode)
                ea = cmath.exp(1j*k*act) * w / (L**1.0)
                amps[j] += amps[i]*ea

        probs = {d: abs(amps[d])**2 for d in det}
    else:
        # Grid mode
        post = RulePostulates(phase_per_action=k, attenuation_power=1.0,
                              attenuation_mode="geometry")
        rule = derive_local_rule(persistent_nodes=frozenset(), postulates=post)
        s = list(src)[0] if isinstance(src, (set, list)) else src
        arrival = infer_arrival_times_from_source(positions, s, rule)
        dag = build_causal_dag(positions, arrival)
        order = sorted(arrival, key=arrival.get)
        node_field = field if isinstance(field, dict) else {n: 0.0 for n in positions}

        amps = {s: 1.0+0.0j}
        for node in order:
            if node not in amps or node in blocked:
                continue
            a = amps[node]
            for nb in dag.get(node, []):
                if nb in blocked:
                    continue
                dx = nb[0]-node[0]
                dy = nb[1]-node[1]
                L = math.sqrt(dx*dx+dy*dy)
                if L < 1e-10:
                    continue
                lf = 0.5*(node_field.get(node, 0)+node_field.get(nb, 0))
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                w = edge_weight(dy, dx, L, beta, mode)
                ea = cmath.exp(1j*k*act) * w / (L**1.0)
                if nb not in amps:
                    amps[nb] = 0.0+0.0j
                amps[nb] += a*ea

        probs = {d: abs(amps.get(d, 0.0))**2 for d in det}

    total = sum(probs.values())
    if normalize and total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def run_regression(beta, mode):
    """Run canonical regression for one (beta, mode) pair."""
    k_band = [3.0, 5.0, 7.0]
    results = {}

    # Born rule
    width, height = 50, 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height+1))
    barrier_x, det_x = 20, 40

    post = RulePostulates(phase_per_action=2.0, attenuation_power=1.0, attenuation_mode="geometry")
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=post)
    field_grid = derive_node_field(nodes, rule)
    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)

    barrier = set((barrier_x, y) for y in range(-height, height+1))
    slit_centers = [-5, 0, 5]
    slits = {}
    for i, sc in enumerate(slit_centers):
        slits[chr(ord('A')+i)] = {(barrier_x, y) for y in range(sc-1, sc+2)}

    def screen_3(open_labels):
        open_nodes = set()
        for l in open_labels:
            open_nodes |= slits[l]
        bl = barrier - open_nodes
        return propagate_weighted(nodes, dag, field_grid, {source}, set((det_x, y) for y in screen_ys),
                                  2.0, beta, mode, bl, normalize=False)

    p = {}
    for r in range(4):
        for combo in combinations('ABC', r):
            key = ''.join(combo) if combo else ''
            p[key] = screen_3(combo)

    max_i3 = max(abs(p['ABC'].get(y,0)-p['AB'].get(y,0)-p['AC'].get(y,0)-p['BC'].get(y,0)
        +p['A'].get(y,0)+p['B'].get(y,0)+p['C'].get(y,0)-p[''].get(y,0))
        for y in set((det_x, y) for y in screen_ys))
    max_p = max(max(p['ABC'].values()), 1e-30)
    results['born'] = max_i3/max_p

    # k=0
    mass_mn = frozenset((25, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_mn, postulates=post)
    mass_field = derive_node_field(nodes, mass_rule)
    det_nodes = set((det_x, y) for y in screen_ys)
    fp0 = propagate_weighted(nodes, dag, field_grid, {source}, det_nodes, 0.0, beta, mode)
    mp0 = propagate_weighted(nodes, dag, mass_field, {source}, det_nodes, 0.0, beta, mode)
    fcy = sum(d[1]*p for d, p in fp0.items()) / max(sum(fp0.values()), 1e-30)
    mcy = sum(d[1]*p for d, p in mp0.items()) / max(sum(mp0.values()), 1e-30)
    results['k0'] = abs(mcy - fcy)

    # Gravity scaling
    grav = {}
    for nl in [12, 25]:
        rs = []
        for seed in range(4):
            positions, adj, _ = generate_causal_dag(n_layers=nl, nodes_per_layer=25,
                y_range=12.0, connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj, env_depth_layers=max(1, round(nl/6)))
            if setup is None: continue
            n = len(positions)
            free_f = [0.0]*n
            mid = setup["layers"][len(setup["layers"])//2]
            gm = [i for i in setup["by_layer"][mid] if positions[i][1] > setup["cy"]+2]
            if len(gm) < 2: continue
            field_g = compute_field(positions, adj, gm)
            shifts = []
            for k in k_band:
                fp = propagate_weighted(positions, adj, free_f, setup["src"], setup["det"], k, beta, mode)
                mp = propagate_weighted(positions, adj, field_g, setup["src"], setup["det"], k, beta, mode)
                shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))
            fp0 = propagate_weighted(positions, adj, free_f, setup["src"], setup["det"], 5.0, beta, mode)
            t = sum(fp0.values())
            w = max((sum(positions[d][1]**2*p for d, p in fp0.items())/t-(sum(positions[d][1]*p for d, p in fp0.items())/t)**2)**0.5, 0.1) if t > 0 else 1.0
            rs.append(sum(shifts)/len(shifts)/w)
        grav[nl] = sum(rs)/len(rs) if rs else 0
    results['r12'] = grav.get(12, 0)
    results['r25'] = grav.get(25, 0)

    # Interference
    slit_2_nodes = set()
    for sy in [-4, 4]:
        for y in range(sy-1, sy+2):
            slit_2_nodes.add((barrier_x, y))
    blocked_2 = barrier - slit_2_nodes
    best_v = 0
    for k in [2.0, 4.0]:
        pc = propagate_weighted(nodes, dag, field_grid, {source}, det_nodes, k, beta, mode, blocked_2)
        vals = [pc.get(y, 0) for y in sorted(det_nodes)]
        peaks = [vals[i] for i in range(1, len(vals)-1) if vals[i]>vals[i-1] and vals[i]>vals[i+1]]
        troughs = [vals[i] for i in range(1, len(vals)-1) if vals[i]<vals[i-1] and vals[i]<vals[i+1]]
        V = (max(peaks)-min(troughs))/(max(peaks)+min(troughs)) if peaks and troughs else 0
        best_v = max(best_v, V)
    results['V'] = best_v

    return results


def main():
    print("=" * 70)
    print("NORMALIZED PATH MEASURE: scale-free variants")
    print("=" * 70)
    print()

    variants = [
        ("raw_dy", 0.5, "exp(-0.5×dy²) [baseline]"),
        ("slope", 0.5, "exp(-0.5×(dy/L)²)"),
        ("slope", 1.0, "exp(-1.0×(dy/L)²)"),
        ("slope", 2.0, "exp(-2.0×(dy/L)²)"),
        ("turning", 1.0, "exp(-1.0×(1-dx/L))"),
        ("turning", 2.0, "exp(-2.0×(1-dx/L))"),
        ("angle", 1.0, "exp(-1.0×θ²)"),
        ("angle", 2.0, "exp(-2.0×θ²)"),
    ]

    print(f"  {'variant':>25s}  {'Born':>10s}  {'V':>6s}  {'k0':>8s}  {'R@12':>6s}  {'R@25':>6s}  {'pass':>4s}")
    print(f"  {'-' * 68}")

    for mode, beta, label in variants:
        r = run_regression(beta, mode)
        born_ok = r['born'] < 1e-8
        v_ok = r['V'] > 0.5
        k0_ok = r['k0'] < 0.01
        grav_ok = r['r25'] >= r['r12'] - 0.05
        all_ok = born_ok and v_ok and k0_ok and grav_ok
        n_pass = sum([born_ok, v_ok, k0_ok, grav_ok])

        print(f"  {label:>25s}  {r['born']:10.2e}  {r['V']:6.3f}  {r['k0']:8.5f}  "
              f"{r['r12']:+6.3f}  {r['r25']:+6.3f}  {n_pass}/4")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
