#!/usr/bin/env python3
"""Dense central-band pocket scaling test: N=60..100.

Main found a Born-clean pocket at npl=60, y_cut=2.0, connect_radius=3.0
with LN+|y|+collapse giving purity=0.55 at N=60, Born=0.000.

Critical question: does this scale to N=80-100? If the pocket holds,
this is the project's best combined architecture.

Self-contained (no imports from main scripts).
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8
LAM = 10.0
# Dense pocket parameters from main
NPL = 60
CONNECT_RADIUS = 3.0
XYZ_RANGE = 12.0
Y_CUT = 2.0
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 8  # Fewer seeds since MC is expensive
N_REAL = 50
P_COLLAPSE = 0.2
N_LAYERS_LIST = [40, 60, 80, 100]


def generate_3d_dag_chokepoint(n_layers, npl, xyz_range, connect_radius, rng_seed):
    """Chokepoint DAG: layer-1 connectivity only (no skip-layer edges)."""
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
                    for prev_idx in layer_indices[-1]:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
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


def propagate_3d(positions, adj, field, src, k, blocked, use_ln=False,
                  p_collapse=0.0, mass_set=None, rng_obj=None):
    n = len(positions)
    mass_set = mass_set or set()
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if i in blocked:
                continue
            ai = amps[i]
            if ai == 0j:
                continue
            if p_collapse > 0 and i in mass_set and rng_obj and rng_obj.random() < p_collapse:
                ai *= cmath.exp(1j * rng_obj.uniform(0, 2*math.pi))
                amps[i] = ai
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1, z1 = positions[i]
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2-x1, y2-y1, z2-z1
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
                amps[j] += ai * ea
        if use_ln and li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i])**2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm
    return amps


def compute_field_3d(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix-mx)**2 + (iy-my)**2 + (iz-mz)**2) + 0.1
            field[i] += 0.1 / r
    return field


def get_graph_info(positions, adj, n_layers):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None
    # Three slits for Born test
    upper = sorted([i for i in bi if positions[i][1] > cy + 2], key=lambda i: positions[i][1])
    lower = sorted([i for i in bi if positions[i][1] < cy - 2], key=lambda i: -positions[i][1])
    middle = sorted([i for i in bi if abs(positions[i][1] - cy) <= 2],
                    key=lambda i: abs(positions[i][1] - cy))
    return {
        "src": src, "det": det_list, "sa": sa, "sb": sb,
        "blocked": blocked, "mass": mass_nodes, "mass_set": set(mass_nodes),
        "by_layer": by_layer, "layers": layers,
        "slit3": (upper[:1], lower[:1], middle[:1]) if upper and lower and middle else None,
        "bi": bi,
    }


def mc_born_test(positions, adj, info, k, use_ln, p_collapse, n_real, field):
    """Monte Carlo Sorkin test."""
    s3 = info["slit3"]
    if not s3 or not s3[0] or not s3[1] or not s3[2]:
        return math.nan
    slit_a, slit_b, slit_c = s3
    all_slits = set(slit_a + slit_b + slit_c)
    other_barrier = set(info["bi"]) - all_slits
    det_list = info["det"]
    combos = {
        'abc': set(slit_a + slit_b + slit_c),
        'ab': set(slit_a + slit_b), 'ac': set(slit_a + slit_c),
        'bc': set(slit_b + slit_c),
        'a': set(slit_a), 'b': set(slit_b), 'c': set(slit_c),
    }
    avg_P = {key: [0.0]*len(det_list) for key in combos}
    for r in range(max(1, n_real)):
        for key, open_set in combos.items():
            bl = other_barrier | (all_slits - open_set)
            rng_obj = random.Random(r*7000 + hash(key)%10000) if p_collapse > 0 else None
            a = propagate_3d(positions, adj, field, info["src"], k, bl,
                            use_ln=use_ln, p_collapse=p_collapse,
                            mass_set=info["mass_set"], rng_obj=rng_obj)
            for di, d in enumerate(det_list):
                avg_P[key][di] += abs(a[d])**2
    for key in avg_P:
        for di in range(len(det_list)):
            avg_P[key][di] /= max(1, n_real)
    I3 = 0.0; P_abc = 0.0
    for di in range(len(det_list)):
        i3d = (avg_P['abc'][di] - avg_P['ab'][di] - avg_P['ac'][di] - avg_P['bc'][di]
               + avg_P['a'][di] + avg_P['b'][di] + avg_P['c'][di])
        I3 += abs(i3d); P_abc += avg_P['abc'][di]
    return I3/P_abc if P_abc > 1e-30 else math.nan


def mc_purity_gravity(positions, adj, info, k_band, use_ln, p_collapse, n_real, field_m, field_f):
    """MC purity + gravity."""
    det_list = info["det"]
    rho = defaultdict(complex)
    n_rho = 0; grav_all = []
    for r in range(max(1, n_real)):
        for k in k_band:
            rng_a = random.Random(r*1000+7) if p_collapse > 0 else None
            rng_b = random.Random(r*1000+13) if p_collapse > 0 else None
            aa = propagate_3d(positions, adj, field_m, info["src"], k,
                             info["blocked"] | set(info["sb"]),
                             use_ln=use_ln, p_collapse=p_collapse,
                             mass_set=info["mass_set"], rng_obj=rng_a)
            ab = propagate_3d(positions, adj, field_m, info["src"], k,
                             info["blocked"] | set(info["sa"]),
                             use_ln=use_ln, p_collapse=p_collapse,
                             mass_set=info["mass_set"], rng_obj=rng_b)
            psi = [aa[d]+ab[d] for d in det_list]
            nsq = sum(abs(p)**2 for p in psi)
            if nsq < 1e-30: continue
            for i2, d1 in enumerate(det_list):
                for j2, d2 in enumerate(det_list):
                    rho[(d1,d2)] += psi[i2]*psi[j2].conjugate()
            n_rho += 1
            # Gravity
            rng_g = random.Random(r*1000+19) if p_collapse > 0 else None
            rng_g2 = random.Random(r*1000+19) if p_collapse > 0 else None
            am = propagate_3d(positions, adj, field_m, info["src"], k, info["blocked"],
                             use_ln=use_ln, p_collapse=p_collapse,
                             mass_set=info["mass_set"], rng_obj=rng_g)
            af = propagate_3d(positions, adj, field_f, info["src"], k, info["blocked"],
                             use_ln=use_ln, p_collapse=p_collapse,
                             mass_set=info["mass_set"], rng_obj=rng_g2)
            pm = sum(abs(am[d])**2 for d in det_list)
            pf = sum(abs(af[d])**2 for d in det_list)
            if pm > 1e-30 and pf > 1e-30:
                ym = sum(abs(am[d])**2*positions[d][1] for d in det_list)/pm
                yf = sum(abs(af[d])**2*positions[d][1] for d in det_list)/pf
                grav_all.append(ym-yf)
    if n_rho == 0: return None
    for key in rho: rho[key] /= n_rho
    tr = sum(rho[(d,d)] for d in det_list).real
    if tr < 1e-30: return None
    for key in rho: rho[key] /= tr
    pur = sum(abs(v)**2 for v in rho.values()).real
    grav = sum(grav_all)/len(grav_all) if grav_all else 0
    return {"pur": pur, "gravity": grav}


def _mean_se(vals):
    if not vals: return 0.0, 0.0
    m = sum(vals)/len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v-m)**2 for v in vals)/(len(vals)-1)
    return m, math.sqrt(var/len(vals))


def main():
    print("=" * 105)
    print("DENSE CENTRAL-BAND POCKET SCALING")
    print(f"  npl={NPL}, connect_radius={CONNECT_RADIUS}, y_cut={Y_CUT}")
    print(f"  p_collapse={P_COLLAPSE}, {N_REAL} MC realizations, {N_SEEDS} seeds")
    print("=" * 105)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("linear", False, 0.0),
        ("LN", True, 0.0),
        ("LN+|y|", True, True),
        ("LN+|y|+col", True, True),  # with collapse
    ]

    print(f"  {'N':>4s}  {'mode':>14s}  {'pur':>10s}  {'gravity':>12s}  {'Born':>10s}  "
          f"{'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 68}")

    for nl in N_LAYERS_LIST:
        for label, use_ln, use_yrem_or_col in configs:
            use_yrem = use_yrem_or_col if label != "LN" else False
            use_col = label.endswith("+col")
            p_col = P_COLLAPSE if use_col else 0.0

            t0 = time.time()
            pur_all, grav_all, born_all = [], [], []

            for seed in seeds:
                pos, adj, bl = generate_3d_dag_chokepoint(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                info = get_graph_info(pos, adj, nl)
                if not info:
                    continue

                protected = set(info["src"]) | set(info["det"]) | set(info["sa"] + info["sb"])
                if use_yrem:
                    adj, _ = apply_y_removal(pos, adj, bl, Y_CUT, protected)

                field_m = compute_field_3d(pos, info["mass"])
                field_f = [0.0] * len(pos)

                n_mc = N_REAL if use_col else 1
                r = mc_purity_gravity(pos, adj, info, K_BAND, use_ln, p_col, n_mc, field_m, field_f)
                if r:
                    pur_all.append(r["pur"])
                    grav_all.append(r["gravity"])

                # Born (on first k only, fewer MC)
                if info["slit3"] and info["slit3"][0] and info["slit3"][1] and info["slit3"][2]:
                    b = mc_born_test(pos, adj, info, K_BAND[0], use_ln, p_col,
                                    min(20, n_mc), field_f)
                    if not math.isnan(b):
                        born_all.append(b)

            dt = time.time() - t0
            if pur_all:
                mp, sep = _mean_se(pur_all)
                mg, seg = _mean_se(grav_all)
                mb, seb = _mean_se(born_all)
                n_ok = len(pur_all)
                print(f"  {nl:4d}  {label:>14s}  {mp:7.4f}±{sep:.3f}  {mg:+8.4f}±{seg:.3f}  "
                      f"{mb:8.2e}±{seb:.1e}  {n_ok:3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>14s}  FAIL  {dt:4.0f}s")

        print()


if __name__ == "__main__":
    main()
