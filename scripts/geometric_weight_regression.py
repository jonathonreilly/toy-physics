#!/usr/bin/env python3
"""Canonical regression for the geometric weight propagator.

Propagator: exp(ikS) × exp(-β×dy²) / L^p
β=0.5, field-independent local transverse-step penalty on edge y-displacement.

Important interpretation notes:
- this is a paraxial / directional path-measure correction on embedded edges
- it is not a shortest-path-distance penalty
- it is not a curvature penalty
- β is embedding-scale dependent here because the weight uses raw dy

Tests:
1. Born rule (3-slit I₃ on fixed DAG)
2. Interference visibility (2-slit V)
3. k=0→0 (gravity = pure phase)
4. Gravity scaling (R_grav vs N on random DAGs)
5. Decoherence scaling (detector-state purity vs N with a capped distributed-record model)

PStack experiment: geometric-weight-regression
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
from itertools import combinations
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
)
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import (
    build_post_barrier_setup, compute_detector_metrics,
)
from scripts.two_register_decoherence import compute_field


BETA = 0.5


def propagate_geo(positions, adj, field, src, det, k, blocked=None):
    """Corrected propagator with geometric weight exp(-β×dy²).

    The added weight suppresses edges with larger transverse displacement per
    step. This is a local paraxial/directional bias in the path measure, not a
    shortest-path or curvature functional.
    """
    n = len(positions) if isinstance(positions, list) else len(positions)
    blocked = blocked or set()

    # Build order
    if isinstance(positions, list):
        # DAG mode (int indices)
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
                dy = y2 - y1
                ea = cmath.exp(1j*k*act) * math.exp(-BETA*dy*dy) / (L**1.0)
                amps[j] += amps[i]*ea

        probs = {d: abs(amps[d])**2 for d in det}
    else:
        # Grid mode (tuple keys)
        nodes = positions
        post = RulePostulates(phase_per_action=k, attenuation_power=1.0,
                              attenuation_mode="geometry")
        rule = derive_local_rule(persistent_nodes=frozenset(), postulates=post)
        arrival = infer_arrival_times_from_source(nodes, list(src)[0] if isinstance(src, set) else src, rule)
        dag_local = build_causal_dag(nodes, arrival)
        order = sorted(arrival, key=arrival.get)
        s = list(src)[0] if isinstance(src, set) else src
        amps = {s: 1.0+0.0j}
        node_field = field if isinstance(field, dict) else {n: 0.0 for n in nodes}

        for node in order:
            if node not in amps or node in blocked:
                continue
            a = amps[node]
            for nb in dag_local.get(node, []):
                if nb in blocked:
                    continue
                L = math.dist(node, nb)
                lf = 0.5*(node_field.get(node, 0)+node_field.get(nb, 0))
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                dy = nb[1]-node[1]
                ea = cmath.exp(1j*k*act) * math.exp(-BETA*dy*dy) / (L**1.0)
                if nb not in amps:
                    amps[nb] = 0.0+0.0j
                amps[nb] += a*ea

        probs = {d: abs(amps.get(d, 0.0))**2 for d in det}

    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def visibility(probs, positions, det_list):
    py = defaultdict(float)
    for d in det_list:
        y = positions[d][1] if isinstance(positions, list) else d[1]
        py[y] += probs.get(d, 0)
    ys = sorted(py.keys())
    if len(ys) < 3:
        return 0.0
    vals = [py[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals)-1) if vals[i]>vals[i-1] and vals[i]>vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals)-1) if vals[i]<vals[i-1] and vals[i]<vals[i+1]]
    if peaks and troughs:
        return (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
    return 0.0


def centroid_y(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    if isinstance(positions, list):
        return sum(positions[d][1]*p for d, p in probs.items()) / total
    else:
        return sum(d[1]*p for d, p in probs.items()) / total


def main():
    print("=" * 70)
    print(f"GEOMETRIC WEIGHT CANONICAL REGRESSION (β={BETA})")
    print("=" * 70)
    print()
    print("Interpretation: local paraxial / directional path-measure correction")
    print("Scale note: β is tied to the embedding scale because the weight uses raw dy")
    print()

    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            failed += 1
            print(f"  [FAIL] {name}")
        if detail:
            print(f"         {detail}")

    # ================================================================
    # TEST 1: Born rule (3-slit I₃)
    # ================================================================
    print("TEST 1: Born rule")
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

    def screen_3slit(open_labels):
        open_nodes = set()
        for l in open_labels:
            open_nodes |= slits[l]
        bl = barrier - open_nodes
        order = sorted(arrival, key=arrival.get)
        amps = {source: 1.0+0.0j}
        for node in order:
            if node not in amps or node in bl: continue
            a = amps[node]
            for nb in dag.get(node, []):
                if nb in bl: continue
                L = math.dist(node, nb)
                lf = 0.5*(field_grid.get(node,0)+field_grid.get(nb,0))
                dl = L*(1+lf); ret = math.sqrt(max(dl*dl-L*L, 0)); act = dl-ret
                dy = nb[1]-node[1]
                ea = cmath.exp(1j*2.0*act) * math.exp(-BETA*dy*dy) / (L**1.0)
                if nb not in amps: amps[nb] = 0.0+0.0j
                amps[nb] += a*ea
        return {y: abs(amps.get((det_x, y), 0.0))**2 for y in screen_ys}

    p = {}
    for r in range(4):
        for combo in combinations('ABC', r):
            key = ''.join(combo) if combo else ''
            p[key] = screen_3slit(combo)

    max_i3 = max(abs(p['ABC'].get(y,0)-p['AB'].get(y,0)-p['AC'].get(y,0)-p['BC'].get(y,0)
        +p['A'].get(y,0)+p['B'].get(y,0)+p['C'].get(y,0)-p[''].get(y,0)) for y in screen_ys)
    max_p = max(max(p['ABC'].values()), 1e-30)
    check("Born rule I₃", max_i3/max_p < 1e-8, f"|I₃|/P = {max_i3/max_p:.2e}")

    # ================================================================
    # TEST 2: Interference visibility
    # ================================================================
    print()
    print("TEST 2: Interference")
    slit_2 = {-4, 4}
    slit_2_nodes = set()
    for sy in slit_2:
        for y in range(sy-1, sy+2):
            slit_2_nodes.add((barrier_x, y))
    blocked_2 = barrier - slit_2_nodes

    best_v = 0
    for k in [1.0, 2.0, 3.0, 4.0]:
        order = sorted(arrival, key=arrival.get)
        amps = {source: 1.0+0.0j}
        for node in order:
            if node not in amps or node in blocked_2: continue
            a = amps[node]
            for nb in dag.get(node, []):
                if nb in blocked_2: continue
                L = math.dist(node, nb)
                act = L  # free field
                dy = nb[1]-node[1]
                ea = cmath.exp(1j*k*act) * math.exp(-BETA*dy*dy) / (L**1.0)
                if nb not in amps: amps[nb] = 0.0+0.0j
                amps[nb] += a*ea
        probs = {y: abs(amps.get((det_x, y), 0.0))**2 for y in screen_ys}
        total = sum(probs.values())
        if total > 0: probs = {y: p/total for y, p in probs.items()}
        vals = [probs.get(y,0) for y in sorted(screen_ys)]
        peaks = [vals[i] for i in range(1,len(vals)-1) if vals[i]>vals[i-1] and vals[i]>vals[i+1]]
        troughs = [vals[i] for i in range(1,len(vals)-1) if vals[i]<vals[i-1] and vals[i]<vals[i+1]]
        V = (max(peaks)-min(troughs))/(max(peaks)+min(troughs)) if peaks and troughs else 0
        best_v = max(best_v, V)
    check("Interference V > 0.5", best_v > 0.5, f"V = {best_v:.4f}")

    # ================================================================
    # TEST 3: k=0→0
    # ================================================================
    print()
    print("TEST 3: k=0→0")
    mass_mn = frozenset((25, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_mn, postulates=post)
    mass_field = derive_node_field(nodes, mass_rule)

    det_nodes = [(det_x, y) for y in screen_ys]
    fp0 = propagate_geo(nodes, dag, field_grid, {source}, set(det_nodes), 0.0)
    mp0 = propagate_geo(nodes, dag, mass_field, {source}, set(det_nodes), 0.0)
    shift0 = centroid_y(mp0, nodes) - centroid_y(fp0, nodes)
    check("k=0 → zero gravity", abs(shift0) < 0.01, f"shift = {shift0:.6f}")

    # ================================================================
    # TEST 4: Gravity scaling on DAGs
    # ================================================================
    print()
    print("TEST 4: Gravity scaling")
    k_band = [3.0, 5.0, 7.0]
    grav_results = {}

    for nl in [8, 12, 18, 25]:
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
                fp = propagate_geo(positions, adj, free_f, setup["src"], setup["det"], k)
                mp = propagate_geo(positions, adj, field_g, setup["src"], setup["det"], k)
                shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))

            fp0 = propagate_geo(positions, adj, free_f, setup["src"], setup["det"], 5.0)
            total = sum(fp0.values())
            w = max((sum(positions[d][1]**2*p for d, p in fp0.items())/total -
                    (sum(positions[d][1]*p for d, p in fp0.items())/total)**2)**0.5, 0.1) if total > 0 else 1.0
            rs.append(sum(shifts)/len(shifts)/w)

        if rs:
            grav_results[nl] = sum(rs)/len(rs)
            print(f"  N={nl}: R_grav = {grav_results[nl]:+.3f}")

    r12 = grav_results.get(12, 0)
    r25 = grav_results.get(25, 0)
    check("Gravity scaling (R@25 >= R@12)", r25 >= r12 - 0.05,
          f"R@12={r12:+.3f}, R@25={r25:+.3f}")

    # ================================================================
    # TEST 5: Decoherence scaling (purity with distributed records)
    # ================================================================
    print()
    print("TEST 5: Decoherence scaling (capped distributed-record model)")

    pur_results = {}
    for nl in [8, 12, 18]:
        purs = []
        for seed in range(3):
            positions, adj, _ = generate_causal_dag(n_layers=nl, nodes_per_layer=25,
                y_range=12.0, connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj, env_depth_layers=max(1, round(nl/6)))
            if setup is None: continue
            n = len(positions)
            mass_set = set(setup["mass_set"]) - setup["blocked"]

            pk = []
            for k in k_band:
                # Distributed records with geometric weight.
                # This only tests the current capped edge-record architecture.
                blocked = setup["blocked"]
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
                for s in setup["src"]:
                    state[(s, ())] = 1.0/len(setup["src"]) + 0.0j
                processed = set()
                for i in order:
                    if i in processed: continue
                    processed.add(i)
                    entries = {rec: amp for (node, rec), amp in list(state.items())
                               if node == i and abs(amp) > 1e-30}
                    if not entries or i in blocked: continue
                    for rec, amp in entries.items():
                        for j in adj.get(i, []):
                            if j in blocked: continue
                            x1, y1 = positions[i]; x2, y2 = positions[j]
                            L = math.sqrt((x2-x1)**2+(y2-y1)**2)
                            if L < 1e-10: continue
                            lf = 0.5*(setup["field"][i]+setup["field"][j])
                            dl = L*(1+lf); ret = math.sqrt(max(dl*dl-L*L, 0)); act = dl-ret
                            dy = y2-y1
                            ea = cmath.exp(1j*k*act) * math.exp(-BETA*dy*dy) / (L**1.0)
                            if i in mass_set or j in mass_set:
                                new_rec = (rec + ((i,j),))[-2:]
                            else:
                                new_rec = rec
                            key = (j, new_rec)
                            if key not in state: state[key] = 0.0+0.0j
                            state[key] += amp*ea

                ds = {(d, rec): amp for (d, rec), amp in state.items() if d in setup["det"]}
                p, _, _, _ = compute_detector_metrics(ds, setup["det_list"])
                if not math.isnan(p): pk.append(p)

            if pk: purs.append(sum(pk)/len(pk))

        if purs:
            pur_results[nl] = sum(purs)/len(purs)
            print(f"  N={nl}: detector-state purity = {pur_results[nl]:.4f}")

    p12 = pur_results.get(12, 1.0)
    p18 = pur_results.get(18, 1.0)
    check("Decoherence scaling in capped record model (pur@18 <= pur@12)", p18 <= p12 + 0.02,
          f"pur@12={p12:.4f}, pur@18={p18:.4f}")

    # ================================================================
    # SUMMARY
    # ================================================================
    print()
    print("=" * 70)
    print(f"REGRESSION: {passed}/{passed+failed} passed, {failed}/{passed+failed} failed")
    print("=" * 70)
    print()
    if failed == 0:
        print("VERDICT: PROVISIONAL — all constraints satisfied")
    else:
        print(f"VERDICT: {failed} failure(s) — investigate before promoting")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
