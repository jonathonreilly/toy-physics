#!/usr/bin/env python3
"""Born rule check on stochastic collapse + |y|-removal.

The other thread found Born=2.3e-5 on 2D collapse. Verify on 3D
chokepoint DAGs with and without |y|-removal.

Collapse is stochastic — the Sorkin test needs averaging over
realizations. For each realization r:
  P_X^r = sum_det |ψ_X^r(d)|^2
Then average I_3 over realizations:
  <I_3> = <P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C>
  |<I_3>| / <P_ABC>

If Born holds for the averaged probabilities, |<I_3>|/<P_ABC> ~ 0.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
CONNECT_RADIUS = 4.0
XYZ_RANGE = 12.0
NPL = 50
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 16
P_COLLAPSE = 0.2
N_REAL = 100  # More realizations for accurate Born test


def generate_3d_dag_chokepoint(n_layers, npl, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for _ in range(npl):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                if layer_indices:
                    prev = layer_indices[-1]
                    for prev_idx in prev:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px)**2 + (y - py)**2 + (z - pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), barrier_layer


def apply_y_removal(positions, adj, barrier_layer, y_thresh, protected):
    removed = set()
    for idx, (x, y, z) in enumerate(positions):
        if x <= barrier_layer or idx in protected:
            continue
        if abs(y) < y_thresh:
            removed.add(idx)
    new_adj = {}
    for i, nbs in adj.items():
        if i in removed: continue
        new_nbs = [j for j in nbs if j not in removed]
        if new_nbs: new_adj[i] = new_nbs
    return new_adj, removed


def propagate_3d_collapse(positions, adj, field, src, k, blocked, mass_set,
                           p_collapse, rng_obj):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if abs(amps[i]) < 1e-30 or i in blocked:
                continue
            if i in mass_set and p_collapse > 0 and rng_obj.random() < p_collapse:
                theta_rand = rng_obj.uniform(0, 2 * math.pi)
                amps[i] *= cmath.exp(1j * theta_rand)
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1, z1 = positions[i]
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
                L = math.sqrt(dx*dx + dy*dy + dz*dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl*dl - L*L, 0))
                act = dl - ret
                theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                ea = cmath.exp(1j * k * act) * w / L
                amps[j] += amps[i] * ea
    return amps


def propagate_3d(positions, adj, field, src, k, blocked):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if abs(amps[i]) < 1e-30 or i in blocked:
                continue
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1, z1 = positions[i]
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
                L = math.sqrt(dx*dx + dy*dy + dz*dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl*dl - L*L, 0))
                act = dl - ret
                theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                ea = cmath.exp(1j * k * act) * w / L
                amps[j] += amps[i] * ea
    return amps


def mc_sorkin_test(positions, adj, src, k, barrier_nodes, slit_a, slit_b, slit_c,
                    det_list, mass_set, p_collapse, n_real, field):
    """Monte Carlo Sorkin test averaged over collapse realizations."""
    all_slits = set(slit_a + slit_b + slit_c)
    other_barrier = set(barrier_nodes) - all_slits

    combos = {
        'abc': set(slit_a + slit_b + slit_c),
        'ab': set(slit_a + slit_b),
        'ac': set(slit_a + slit_c),
        'bc': set(slit_b + slit_c),
        'a': set(slit_a),
        'b': set(slit_b),
        'c': set(slit_c),
    }

    # Accumulate probabilities over realizations
    avg_P = {key: [0.0] * len(det_list) for key in combos}

    for r in range(n_real):
        for key, open_set in combos.items():
            bl = other_barrier | (all_slits - open_set)
            if p_collapse > 0:
                rng_obj = random.Random(r * 7000 + hash(key) % 10000)
                a = propagate_3d_collapse(positions, adj, field, src, k, bl,
                                          mass_set, p_collapse, rng_obj)
            else:
                a = propagate_3d(positions, adj, field, src, k, bl)
            for di, d in enumerate(det_list):
                avg_P[key][di] += abs(a[d]) ** 2

    # Average
    for key in avg_P:
        for di in range(len(det_list)):
            avg_P[key][di] /= n_real

    # Compute I3
    I3 = 0.0
    P_abc = 0.0
    for di in range(len(det_list)):
        i3_d = (avg_P['abc'][di] - avg_P['ab'][di] - avg_P['ac'][di] - avg_P['bc'][di]
                + avg_P['a'][di] + avg_P['b'][di] + avg_P['c'][di])
        I3 += abs(i3_d)
        P_abc += avg_P['abc'][di]

    return I3 / P_abc if P_abc > 1e-30 else math.nan


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 90)
    print("BORN RULE CHECK: COLLAPSE + |y|-REMOVAL ON 3D CHOKEPOINT DAGs")
    print(f"  NPL={NPL}, p={P_COLLAPSE}, {N_REAL} realizations, {N_SEEDS} seeds")
    print("=" * 90)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("linear", False, 0.0),
        ("linear+|y|", True, 0.0),
        ("collapse", False, P_COLLAPSE),
        ("col+|y|", True, P_COLLAPSE),
    ]

    for nl in [15, 25]:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'mode':>12s}  {'|I3|/P':>12s}  {'max':>10s}  {'ok':>3s}  {'time':>5s}  {'verdict':>8s}")
        print(f"  {'-' * 60}")

        for label, use_yrem, p_col in configs:
            t0 = time.time()
            i3p_all = []

            for seed in seeds:
                pos, adj, bl = generate_3d_dag_chokepoint(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(pos):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7:
                    continue
                src = by_layer[layers[0]]
                det_list = list(by_layer[layers[-1]])
                if not det_list:
                    continue
                cy = sum(pos[i][1] for i in range(n)) / n
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]

                upper = sorted([i for i in bi if pos[i][1] > cy + 2], key=lambda i: pos[i][1])
                lower = sorted([i for i in bi if pos[i][1] < cy - 2], key=lambda i: -pos[i][1])
                middle = sorted([i for i in bi if abs(pos[i][1] - cy) <= 2],
                                key=lambda i: abs(pos[i][1] - cy))
                if not upper or not lower or not middle:
                    continue

                slit_a = [upper[0]]
                slit_b = [lower[0]]
                slit_c = [middle[0]]

                grav_layer = layers[2 * len(layers) // 3]
                mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
                mass_set = set(mass_nodes) if mass_nodes else set()

                protected = set(src) | set(det_list) | set(slit_a + slit_b + slit_c)
                if use_yrem:
                    adj_use, _ = apply_y_removal(pos, adj, bl, 2.0, protected)
                else:
                    adj_use = adj

                field = [0.0] * n  # flat field for Born test

                for k in K_BAND:
                    val = mc_sorkin_test(pos, adj_use, src, k, bi, slit_a, slit_b, slit_c,
                                         det_list, mass_set, p_col,
                                         N_REAL if p_col > 0 else 1, field)
                    if not math.isnan(val):
                        i3p_all.append(val)

            dt = time.time() - t0
            if i3p_all:
                mi, sei = _mean_se(i3p_all)
                mx = max(i3p_all)
                if mx < 1e-10:
                    verdict = "PERFECT"
                elif mx < 0.001:
                    verdict = "PASS"
                elif mx < 0.01:
                    verdict = "~PASS"
                elif mx < 0.1:
                    verdict = "MARGINAL"
                else:
                    verdict = "FAIL"
                print(f"  {label:>12s}  {mi:12.2e}±{sei:.1e}  {mx:10.2e}  "
                      f"{len(i3p_all):3d}  {dt:4.0f}s  {verdict:>8s}")
            else:
                print(f"  {label:>12s}  NO DATA  {dt:4.0f}s")

        print()

    print("Born compliance thresholds:")
    print("  < 1e-10: machine precision (PERFECT)")
    print("  < 0.001: clean (PASS)")
    print("  < 0.01:  practically clean (~PASS)")
    print("  < 0.1:   marginal")
    print("  >= 0.1:  violated (FAIL)")


if __name__ == "__main__":
    main()
