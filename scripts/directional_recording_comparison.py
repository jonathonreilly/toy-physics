#!/usr/bin/env python3
"""Directional recording: lattice vs irregular DAG vs shuffled controls.

Per user request:
1. Keep 1/L^p fixed
2. Direction-dependent environment coupling at mass nodes
3. Each realization stays unitary; decoherence after ensemble average
4. Compare: lattice / irregular DAG / same graph with shuffled labels
5. Check Born rule at σ=0

PStack experiment: directional-recording-comparison
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from toy_event_physics import (
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
    local_edge_properties,
)


def compute_field_dag(positions, adj, mass_idx, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_idx)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0]*n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def signed_direction(pos_from, pos_to):
    """Return signed direction as (dx_sign, dy_sign) tuple — 9 possible values."""
    x1, y1 = pos_from
    x2, y2 = pos_to
    dx = x2 - x1
    dy = y2 - y1
    sx = 1 if dx > 0.01 else (-1 if dx < -0.01 else 0)
    sy = 1 if dy > 0.01 else (-1 if dy < -0.01 else 0)
    return (sx, sy)


def pathsum_dir_recording(positions_or_nodes, adj_or_dag, field,
                          src, det, k, mass_set, dir_phases,
                          blocked=None, is_dag=True, normalize=True):
    """Corrected propagator with direction-dependent recording.

    Works for both DAGs (indexed by int) and grids (indexed by tuple).
    dir_phases: {(node, signed_direction): phase}
    """
    blocked = blocked or set()

    if is_dag:
        n = len(positions_or_nodes)
        positions = positions_or_nodes
        adj = adj_or_dag

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
                ea = cmath.exp(1j*k*act)/(L**1.0)

                if j in mass_set:
                    sd = signed_direction(positions[i], positions[j])
                    extra = dir_phases.get((j, sd), 0.0)
                    ea *= cmath.exp(1j*extra)

                amps[j] += amps[i]*ea

        probs = {d: abs(amps[d])**2 for d in det}
    else:
        # Grid mode
        nodes = positions_or_nodes
        dag = adj_or_dag
        in_deg = defaultdict(int)
        all_nodes = set(nodes)
        for node in all_nodes:
            in_deg[node] = 0
        for node, nbs in dag.items():
            for nb in nbs:
                in_deg[nb] += 1
        q = deque(node for node in all_nodes if in_deg[node] == 0)
        order = []
        while q:
            node = q.popleft()
            order.append(node)
            for nb in dag.get(node, []):
                in_deg[nb] -= 1
                if in_deg[nb] == 0:
                    q.append(nb)

        amps = {}
        s = src[0] if isinstance(src, list) else src
        amps[s] = 1.0+0.0j

        for node in order:
            if node not in amps or node in blocked:
                continue
            a = amps[node]
            for nb in dag.get(node, []):
                if nb in blocked:
                    continue
                L = math.dist(node, nb)
                lf = 0.5*(field.get(node, 0.0)+field.get(nb, 0.0))
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                ea = cmath.exp(1j*k*act)/(L**1.0)

                if nb in mass_set:
                    sd = signed_direction(node, nb)
                    extra = dir_phases.get((nb, sd), 0.0)
                    ea *= cmath.exp(1j*extra)

                if nb not in amps:
                    amps[nb] = 0.0+0.0j
                amps[nb] += a*ea

        probs = {d: abs(amps.get(d, 0.0))**2 for d in det}

    total = sum(probs.values())
    if normalize and total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def visibility_from_probs(probs, get_y):
    """Compute V from prob dict using get_y function to extract y-coord."""
    py = defaultdict(float)
    for d, p in probs.items():
        py[get_y(d)] += p
    ys = sorted(py.keys())
    if len(ys) < 3:
        return 0.0
    vals = [py[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals)-1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals)-1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
    return 0.0


def gen_env(mass_idx, positions, sigma, rng):
    """Generate environment state with signed direction keys."""
    phases = {}
    directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
    for m in mass_idx:
        for d in directions:
            phases[(m, d)] = sigma * rng.gauss(0, 1)
    return phases


def gen_env_shuffled(mass_idx, positions, sigma, rng):
    """Shuffled control: same random phases but assigned to random (node, dir) pairs."""
    phases = gen_env(mass_idx, positions, sigma, rng)
    keys = list(phases.keys())
    values = list(phases.values())
    rng.shuffle(values)
    return dict(zip(keys, values))


def main():
    N_env = 30
    sigma = 0.5

    print("=" * 70)
    print("DIRECTIONAL RECORDING: Lattice vs DAG vs Shuffled")
    print(f"  σ={sigma}, {N_env} env states, 1/L^p propagator")
    print("=" * 70)
    print()

    # ================================================================
    # TEST A: Rectangular lattice
    # ================================================================
    print("TEST A: Rectangular lattice (50x31)")
    print()

    width = 50
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height+1))
    barrier_x = 20
    det_x = 40
    slit_ys = [-4, 4]

    barrier = set((barrier_x, y) for y in range(-height, height+1))
    slit_nodes = set()
    for sy in slit_ys:
        for y in range(sy-1, sy+2):
            slit_nodes.add((barrier_x, y))
    blocked = barrier - slit_nodes

    post = RulePostulates(phase_per_action=2.0, attenuation_power=1.0,
                          attenuation_mode="geometry")
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=post)
    free_field_grid = derive_node_field(nodes, rule)

    mass_mn = frozenset((25, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_mn, postulates=post)
    mass_field_grid = derive_node_field(nodes, mass_rule)
    mass_arrival = infer_arrival_times_from_source(nodes, source, mass_rule)
    mass_dag = build_causal_dag(nodes, mass_arrival)
    mass_set_grid = set(mass_mn)

    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)
    det_nodes = [(det_x, y) for y in screen_ys]

    # Baseline: mass present, no directional recording
    p_base = pathsum_dir_recording(
        nodes, mass_dag, mass_field_grid, [source], det_nodes, 2.0,
        mass_set_grid, {}, blocked, is_dag=False)
    v_base = visibility_from_probs(p_base, lambda d: d[1])

    # With recording
    avg_rec = {d: 0.0 for d in det_nodes}
    avg_shuf = {d: 0.0 for d in det_nodes}
    for env_i in range(N_env):
        rng = random.Random(env_i*31+7)
        dp = gen_env(list(mass_set_grid), None, sigma, rng)
        rng2 = random.Random(env_i*31+7)
        dp_s = gen_env_shuffled(list(mass_set_grid), None, sigma, rng2)

        pr = pathsum_dir_recording(
            nodes, mass_dag, mass_field_grid, [source], det_nodes, 2.0,
            mass_set_grid, dp, blocked, is_dag=False)
        ps = pathsum_dir_recording(
            nodes, mass_dag, mass_field_grid, [source], det_nodes, 2.0,
            mass_set_grid, dp_s, blocked, is_dag=False)

        for d in det_nodes:
            avg_rec[d] += pr.get(d, 0)
            avg_shuf[d] += ps.get(d, 0)

    for avg in [avg_rec, avg_shuf]:
        t = sum(avg.values())
        if t > 0:
            for d in avg:
                avg[d] /= t

    v_rec = visibility_from_probs(avg_rec, lambda d: d[1])
    v_shuf = visibility_from_probs(avg_shuf, lambda d: d[1])

    print(f"  V_baseline (mass, no recording): {v_base:.4f}")
    print(f"  V_recording (σ={sigma}):   {v_rec:.4f}  (drop: {v_base-v_rec:+.4f})")
    print(f"  V_shuffled (control):    {v_shuf:.4f}  (drop: {v_base-v_shuf:+.4f})")
    print()

    # ================================================================
    # TEST B: Irregular DAGs
    # ================================================================
    print("TEST B: Irregular DAGs (15 layers × 25 nodes, y_range=15)")
    print()

    n_seeds = 10
    v_bases = []
    v_recs = []
    v_shufs = []

    for seed in range(n_seeds):
        positions, adj_d, arrival_d = generate_causal_dag(
            n_layers=15, nodes_per_layer=25,
            y_range=15.0, connect_radius=3.0,
            rng_seed=seed*11+7,
        )
        n = len(positions)
        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 6:
            continue

        src = by_layer[layers[0]]
        det = by_layer[layers[-1]]
        if not det:
            continue

        mid = len(layers)//2
        all_ys = [y for _, y in positions]
        cy = sum(all_ys)/len(all_ys)

        mass_layers = [layers[mid-1], layers[mid], layers[mid+1]]
        mass_idx = [i for i in sum((by_layer[l] for l in mass_layers), [])
                    if positions[i][1] > cy+1]
        if len(mass_idx) < 3:
            continue
        mass_set = set(mass_idx)
        field = compute_field_dag(positions, adj_d, mass_idx)
        free_f = [0.0]*n

        if mid < 3:
            continue
        bl = layers[mid-3]
        bi = by_layer[bl]
        sa = [i for i in bi if positions[i][1] > cy+2][:3]
        sb = [i for i in bi if positions[i][1] < cy-2][:3]
        if not sa or not sb:
            continue
        si = sa + sb
        blocked_dag = set(bi) - set(si)

        # Baseline
        pb = pathsum_dir_recording(positions, adj_d, field, src, det, 5.0,
                                    mass_set, {}, blocked_dag)
        vb = visibility_from_probs(pb, lambda d: positions[d][1])
        v_bases.append(vb)

        # Recording + shuffled
        avg_r = {d: 0.0 for d in det}
        avg_s = {d: 0.0 for d in det}
        for env_i in range(N_env):
            rng = random.Random(env_i*31+seed*7)
            dp = gen_env(mass_idx, positions, sigma, rng)
            rng2 = random.Random(env_i*31+seed*7)
            dp_s = gen_env_shuffled(mass_idx, positions, sigma, rng2)

            pr = pathsum_dir_recording(positions, adj_d, field, src, det, 5.0,
                                        mass_set, dp, blocked_dag)
            ps = pathsum_dir_recording(positions, adj_d, field, src, det, 5.0,
                                        mass_set, dp_s, blocked_dag)
            for d in det:
                avg_r[d] += pr.get(d, 0)
                avg_s[d] += ps.get(d, 0)

        for avg in [avg_r, avg_s]:
            t = sum(avg.values())
            if t > 0:
                for d in avg:
                    avg[d] /= t

        vr = visibility_from_probs(avg_r, lambda d: positions[d][1])
        vs = visibility_from_probs(avg_s, lambda d: positions[d][1])
        v_recs.append(vr)
        v_shufs.append(vs)

    if v_bases:
        mb = sum(v_bases)/len(v_bases)
        mr = sum(v_recs)/len(v_recs)
        ms = sum(v_shufs)/len(v_shufs)
        print(f"  Mean V_baseline:   {mb:.4f}")
        print(f"  Mean V_recording:  {mr:.4f}  (drop: {mb-mr:+.4f})")
        print(f"  Mean V_shuffled:   {ms:.4f}  (drop: {mb-ms:+.4f})")
        print(f"  Recording > shuffled decoherence: {mb-mr > mb-ms}")
        print()
        print(f"  Per-seed V_drop (recording):")
        for i, (vb, vr) in enumerate(zip(v_bases, v_recs)):
            print(f"    seed {i}: V_base={vb:.3f}, V_rec={vr:.3f}, drop={vb-vr:+.3f}")
    print()

    # ================================================================
    # TEST C: Born rule at σ=0
    # ================================================================
    print("TEST C: Born rule (3-slit I₃) with directional recording at σ=0")
    print("  (should be zero — each realization is unitary)")
    print()

    slit_3 = [-5, 0, 5]
    barrier_3 = set((barrier_x, y) for y in range(-height, height+1))
    slits_3 = {}
    for i, sc in enumerate(slit_3):
        slits_3[chr(ord('A')+i)] = {(barrier_x, y) for y in range(sc-1, sc+2)}

    from itertools import combinations

    def screen_3slit(open_labels):
        open_nodes = set()
        for l in open_labels:
            open_nodes |= slits_3[l]
        bl = barrier_3 - open_nodes
        return pathsum_dir_recording(
            nodes, dag, free_field_grid, [source], det_nodes, 2.0,
            set(), {}, bl, is_dag=False, normalize=False)

    p = {}
    for r in range(4):
        for combo in combinations('ABC', r):
            key = ''.join(combo) if combo else ''
            p[key] = screen_3slit(combo)

    max_i3 = max(
        abs(p['ABC'].get(d, 0) - p['AB'].get(d, 0) - p['AC'].get(d, 0) - p['BC'].get(d, 0)
            + p['A'].get(d, 0) + p['B'].get(d, 0) + p['C'].get(d, 0) - p[''].get(d, 0))
        for d in det_nodes
    )
    max_p = max(max(p['ABC'].values()), 1e-30)
    ratio = max_i3 / max_p

    print(f"  |I₃|/P = {ratio:.2e}")
    print(f"  Born rule: {'PASS' if ratio < 1e-8 else 'FAIL'}")
    print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("Directional recording creates endogenous decoherence when:")
    print("  1. Mass is positioned in slit→detector path")
    print("  2. Different slits send amplitude from different angles")
    print("  3. Each angle gets a different environment-dependent phase")
    print()
    print("The shuffled control tells us whether the DIRECTIONAL structure")
    print("matters, or if any random phase perturbation would do.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
