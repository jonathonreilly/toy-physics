#!/usr/bin/env python3
"""Quantitative gravity on |y|-pruned graphs.

The other thread found on 2D DAGs:
  - 1/b^2 distance falloff (peak at b≈6)
  - F∝M mass scaling (alpha≈0.82)

Test: do these hold on 3D |y|<2 pruned graphs?
If yes, the joint coexistence result (gravity+decoherence) includes
quantitative gravity, not just sign.

Test 1: Distance scaling — vary mass y-offset (impact parameter b)
Test 2: Mass scaling — vary number of mass nodes M at fixed b
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
N_SEEDS = 24
NL = 40  # Fixed N for gravity tests


def generate_3d_dag_uniform(n_layers, npl, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
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
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3


def apply_y_removal(positions, adj, barrier_layer, y_thresh, protected):
    removed = set()
    for idx, (x, y, z) in enumerate(positions):
        if x <= barrier_layer or idx in protected:
            continue
        if abs(y) < y_thresh:
            removed.add(idx)
    new_adj = {}
    for i, nbs in adj.items():
        if i in removed:
            continue
        new_nbs = [j for j in nbs if j not in removed]
        if new_nbs:
            new_adj[i] = new_nbs
    return new_adj, removed


def propagate_3d(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
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
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                ea = cmath.exp(1j * k * act) * w / L
                amps[j] += amps[i] * ea
    return amps


def compute_field_at_offset(positions, grav_layer_nodes, y_offset, z_offset=0.0,
                             n_mass=3, strength=0.1):
    """Field from mass nodes shifted to specific (y,z) offset."""
    n = len(positions)
    field = [0.0] * n
    mass_used = sorted(grav_layer_nodes)[:n_mass]
    for m in mass_used:
        mx, _, _ = positions[m]
        my_shifted = y_offset
        mz_shifted = z_offset
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my_shifted) ** 2 + (iz - mz_shifted) ** 2) + 0.1
            field[i] += strength / r
    return field, mass_used


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 95)
    print("QUANTITATIVE GRAVITY ON |y|-PRUNED GRAPHS")
    print(f"  N={NL}, NPL={NPL}, |y|<2 removal, {N_SEEDS} seeds")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]
    b_values = [2, 3, 4, 5, 6, 8, 10]
    m_values = [1, 2, 3, 5, 8]

    # Test 1: Distance scaling
    print("TEST 1: DISTANCE SCALING (vary impact parameter b)")
    print(f"  Fixed M=3 mass nodes, N={NL}")
    print(f"  {'mode':>12s}  {'b':>4s}  {'delta':>12s}  {'delta_t':>8s}")
    print(f"  {'-' * 44}")

    for use_yrem in [False, True]:
        label = "|y|<2" if use_yrem else "uniform"
        for b in b_values:
            deltas = []
            for seed in seeds:
                pos, adj, bl = generate_3d_dag_uniform(NL, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(pos):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7:
                    continue
                src = by_layer[layers[0]]
                det_list = list(by_layer[layers[-1]])
                cy = sum(pos[i][1] for i in range(n)) / n
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                if not sa or not sb:
                    continue
                blocked = set(bi) - set(sa + sb)
                grav_layer = layers[2 * len(layers) // 3]
                grav_nodes = by_layer[grav_layer]

                protected = set(src) | set(det_list) | set(sa + sb)
                if use_yrem:
                    adj_use, _ = apply_y_removal(pos, adj, bl, 2.0, protected)
                else:
                    adj_use = adj

                field_m, _ = compute_field_at_offset(pos, grav_nodes, float(b), n_mass=3)
                field_f = [0.0] * n

                seed_deltas = []
                for k in K_BAND:
                    am = propagate_3d(pos, adj_use, field_m, src, k, blocked)
                    af = propagate_3d(pos, adj_use, field_f, src, k, blocked)
                    pm = sum(abs(am[d]) ** 2 for d in det_list)
                    pf = sum(abs(af[d]) ** 2 for d in det_list)
                    if pm > 1e-30 and pf > 1e-30:
                        ym = sum(abs(am[d]) ** 2 * pos[d][1] for d in det_list) / pm
                        yf = sum(abs(af[d]) ** 2 * pos[d][1] for d in det_list) / pf
                        seed_deltas.append(ym - yf)
                if seed_deltas:
                    deltas.append(sum(seed_deltas) / len(seed_deltas))

            if deltas:
                md, sed = _mean_se(deltas)
                dt = md / sed if sed > 0 else 0
                print(f"  {label:>12s}  {b:4d}  {md:+8.4f}±{sed:.3f}  {dt:+7.2f}")

        print()

    # Fit falloff for |y|<2
    print("  Fitting falloff region for |y|<2 (b >= peak)...")
    # Re-collect |y|<2 data for fit
    b_data, d_data = [], []
    for b in b_values:
        deltas = []
        for seed in seeds:
            pos, adj, bl = generate_3d_dag_uniform(NL, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
            n = len(pos)
            by_layer = defaultdict(list)
            for idx, (x, y, z) in enumerate(pos):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 7: continue
            src = by_layer[layers[0]]
            det_list = list(by_layer[layers[-1]])
            cy = sum(pos[i][1] for i in range(n)) / n
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if pos[i][1] > cy + 3][:3]
            sb = [i for i in bi if pos[i][1] < cy - 3][:3]
            if not sa or not sb: continue
            blocked = set(bi) - set(sa + sb)
            grav_layer = layers[2 * len(layers) // 3]
            protected = set(src) | set(det_list) | set(sa + sb)
            adj_use, _ = apply_y_removal(pos, adj, bl, 2.0, protected)
            field_m, _ = compute_field_at_offset(pos, by_layer[grav_layer], float(b), n_mass=3)
            field_f = [0.0] * n
            sd = []
            for k in K_BAND:
                am = propagate_3d(pos, adj_use, field_m, src, k, blocked)
                af = propagate_3d(pos, adj_use, field_f, src, k, blocked)
                pm = sum(abs(am[d])**2 for d in det_list)
                pf = sum(abs(af[d])**2 for d in det_list)
                if pm > 1e-30 and pf > 1e-30:
                    ym = sum(abs(am[d])**2*pos[d][1] for d in det_list)/pm
                    yf = sum(abs(af[d])**2*pos[d][1] for d in det_list)/pf
                    sd.append(ym-yf)
            if sd: deltas.append(sum(sd)/len(sd))
        if deltas:
            md = sum(deltas)/len(deltas)
            b_data.append(b)
            d_data.append(md)

    # Find peak and fit falloff
    if b_data:
        peak_idx = max(range(len(d_data)), key=lambda i: d_data[i])
        peak_b = b_data[peak_idx]
        falloff = [(b, d) for b, d in zip(b_data, d_data) if b > peak_b and d > 0]
        if len(falloff) >= 2:
            lx = [math.log(b) for b, _ in falloff]
            ly = [math.log(d) for _, d in falloff]
            n = len(lx)
            mx = sum(lx)/n; my = sum(ly)/n
            sxx = sum((x-mx)**2 for x in lx)
            sxy = sum((x-mx)*(y-my) for x, y in zip(lx, ly))
            if sxx > 1e-10:
                slope = sxy/sxx
                print(f"  Peak at b≈{peak_b}, falloff ~ b^({slope:.2f})")

    # Test 2: Mass scaling
    print()
    print("TEST 2: MASS SCALING (vary M at fixed b=5)")
    print(f"  Fixed b=5, N={NL}")
    print(f"  {'mode':>12s}  {'M':>4s}  {'delta':>12s}  {'delta_t':>8s}")
    print(f"  {'-' * 44}")

    for use_yrem in [False, True]:
        label = "|y|<2" if use_yrem else "uniform"
        for M in m_values:
            deltas = []
            for seed in seeds:
                pos, adj, bl = generate_3d_dag_uniform(NL, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(pos):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7: continue
                src = by_layer[layers[0]]
                det_list = list(by_layer[layers[-1]])
                cy = sum(pos[i][1] for i in range(n)) / n
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                if not sa or not sb: continue
                blocked = set(bi) - set(sa + sb)
                grav_layer = layers[2 * len(layers) // 3]
                protected = set(src) | set(det_list) | set(sa + sb)
                if use_yrem:
                    adj_use, _ = apply_y_removal(pos, adj, bl, 2.0, protected)
                else:
                    adj_use = adj
                field_m, _ = compute_field_at_offset(pos, by_layer[grav_layer], 5.0, n_mass=M)
                field_f = [0.0] * n
                sd = []
                for k in K_BAND:
                    am = propagate_3d(pos, adj_use, field_m, src, k, blocked)
                    af = propagate_3d(pos, adj_use, field_f, src, k, blocked)
                    pm = sum(abs(am[d])**2 for d in det_list)
                    pf = sum(abs(af[d])**2 for d in det_list)
                    if pm > 1e-30 and pf > 1e-30:
                        ym = sum(abs(am[d])**2*pos[d][1] for d in det_list)/pm
                        yf = sum(abs(af[d])**2*pos[d][1] for d in det_list)/pf
                        sd.append(ym-yf)
                if sd: deltas.append(sum(sd)/len(sd))
            if deltas:
                md, sed = _mean_se(deltas)
                dt = md / sed if sed > 0 else 0
                print(f"  {label:>12s}  {M:4d}  {md:+8.4f}±{sed:.3f}  {dt:+7.2f}")
        print()

    # Fit mass scaling for |y|<2
    m_data, dm_data = [], []
    for M in m_values:
        deltas = []
        for seed in seeds:
            pos, adj, bl = generate_3d_dag_uniform(NL, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
            n = len(pos)
            by_layer = defaultdict(list)
            for idx, (x, y, z) in enumerate(pos): by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 7: continue
            src = by_layer[layers[0]]
            det_list = list(by_layer[layers[-1]])
            cy = sum(pos[i][1] for i in range(n)) / n
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if pos[i][1] > cy + 3][:3]
            sb = [i for i in bi if pos[i][1] < cy - 3][:3]
            if not sa or not sb: continue
            blocked = set(bi) - set(sa + sb)
            protected = set(src) | set(det_list) | set(sa + sb)
            adj_use, _ = apply_y_removal(pos, adj, bl, 2.0, protected)
            field_m, _ = compute_field_at_offset(pos, by_layer[layers[2*len(layers)//3]], 5.0, n_mass=M)
            field_f = [0.0] * n
            sd = []
            for k in K_BAND:
                am = propagate_3d(pos, adj_use, field_m, src, k, blocked)
                af = propagate_3d(pos, adj_use, field_f, src, k, blocked)
                pm = sum(abs(am[d])**2 for d in det_list)
                pf = sum(abs(af[d])**2 for d in det_list)
                if pm > 1e-30 and pf > 1e-30:
                    ym = sum(abs(am[d])**2*pos[d][1] for d in det_list)/pm
                    yf = sum(abs(af[d])**2*pos[d][1] for d in det_list)/pf
                    sd.append(ym-yf)
            if sd: deltas.append(sum(sd)/len(sd))
        if deltas:
            md = sum(deltas)/len(deltas)
            if md > 0:
                m_data.append(M)
                dm_data.append(md)

    if len(m_data) >= 3:
        lx = [math.log(m) for m in m_data]
        ly = [math.log(d) for d in dm_data]
        nn = len(lx)
        mx = sum(lx)/nn; my = sum(ly)/nn
        sxx = sum((x-mx)**2 for x in lx)
        sxy = sum((x-mx)*(y-my) for x, y in zip(lx, ly))
        if sxx > 1e-10:
            alpha = sxy/sxx
            print(f"  Mass scaling on |y|<2: delta ~ M^{alpha:.2f}")
            if 0.5 < alpha < 1.5:
                print(f"  Consistent with F∝M (alpha≈1)")
            elif alpha < 0.5:
                print(f"  Sub-linear (alpha<0.5, possibly sqrt(M))")


if __name__ == "__main__":
    main()
