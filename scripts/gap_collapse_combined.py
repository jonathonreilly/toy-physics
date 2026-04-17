#!/usr/bin/env python3
"""Stochastic collapse + |y|-removal on 3D DAGs.

The other thread found collapse gives (1-pur) ~ N^(+0.21) on 2D DAGs.
Test: does |y|-removal change this? Two hypotheses:

H1: Collapse is topology-independent (same exponent ± |y|)
    → |y| removal doesn't help because collapse depends on number
      of dephasing encounters, not slit-distinguishability

H2: |y|-removal HELPS collapse (higher decoherence)
    → Channel separation + collapse = stronger mixed state

Also: does gravity survive stochastic collapse? The collapse modifies
amplitudes at mass nodes — does this disrupt the phase valley?

Monte Carlo: 50 realizations per seed, average density matrix.
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
N_LAYERS_LIST = [25, 40, 60, 80]
P_COLLAPSE = 0.2
N_REALIZATIONS = 50


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


def propagate_3d_collapse(positions, adj, field, src, k, blocked, mass_set,
                           p_collapse, rng_obj):
    """3D propagator with stochastic dephasing at mass nodes."""
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

            # Stochastic dephasing at mass nodes
            if i in mass_set and p_collapse > 0 and rng_obj.random() < p_collapse:
                theta_rand = rng_obj.uniform(0, 2 * math.pi)
                amps[i] *= cmath.exp(1j * theta_rand)

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


def propagate_3d(positions, adj, field, src, k, blocked):
    """Standard 3D linear propagator."""
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


def compute_field_3d(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2 + (iz - mz) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def mc_purity_and_gravity(positions, adj, field_m, field_f, src, det_list,
                           blocked_a, blocked_b, blocked_both, mass_set,
                           k_band, p_collapse, n_real):
    """Monte Carlo purity + gravity via averaging over realizations."""
    # Collect rho entries over realizations
    rho_entries = defaultdict(complex)
    n_rho = 0
    grav_all = []

    for r in range(n_real):
        rng_obj = random.Random(r * 1000 + 7)

        for k in k_band:
            # Single-slit propagations for this realization
            aa = propagate_3d_collapse(positions, adj, field_m, src, k,
                                        blocked_a, mass_set, p_collapse, rng_obj)
            rng_obj2 = random.Random(r * 1000 + 13)
            ab = propagate_3d_collapse(positions, adj, field_m, src, k,
                                        blocked_b, mass_set, p_collapse, rng_obj2)

            # Combined state for this realization
            psi = [aa[d] + ab[d] for d in det_list]
            norm_sq = sum(abs(p) ** 2 for p in psi)
            if norm_sq < 1e-30:
                continue

            # Accumulate density matrix
            for i, d1 in enumerate(det_list):
                for j, d2 in enumerate(det_list):
                    rho_entries[(d1, d2)] += psi[i] * psi[j].conjugate()
            n_rho += 1

            # Gravity (with mass vs flat)
            rng_obj3 = random.Random(r * 1000 + 19)
            am = propagate_3d_collapse(positions, adj, field_m, src, k,
                                        blocked_both, mass_set, p_collapse, rng_obj3)
            rng_obj4 = random.Random(r * 1000 + 19)  # Same seed for flat
            af = propagate_3d_collapse(positions, adj, field_f, src, k,
                                        blocked_both, mass_set, p_collapse, rng_obj4)
            pm = sum(abs(am[d]) ** 2 for d in det_list)
            pf = sum(abs(af[d]) ** 2 for d in det_list)
            if pm > 1e-30 and pf > 1e-30:
                ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
                yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
                grav_all.append(ym - yf)

    if n_rho == 0:
        return None

    # Normalize and compute purity
    for key in rho_entries:
        rho_entries[key] /= n_rho
    tr = sum(rho_entries[(d, d)] for d in det_list).real
    if tr < 1e-30:
        return None
    for key in rho_entries:
        rho_entries[key] /= tr
    pur = sum(abs(v) ** 2 for v in rho_entries.values()).real
    grav = sum(grav_all) / len(grav_all) if grav_all else 0

    return {"pur": pur, "gravity": grav}


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 100)
    print("STOCHASTIC COLLAPSE + |y|-REMOVAL ON 3D DAGs")
    print(f"  NPL={NPL}, p_collapse={P_COLLAPSE}, {N_REALIZATIONS} realizations, {N_SEEDS} seeds")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("uniform", False, 0.0),
        ("uniform+col", False, P_COLLAPSE),
        ("|y|<2", True, 0.0),
        ("|y|<2+col", True, P_COLLAPSE),
    ]

    print(f"  {'N':>4s}  {'mode':>14s}  {'pur':>10s}  {'1-pur':>8s}  "
          f"{'gravity':>12s}  {'grav_t':>7s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 72}")

    for nl in N_LAYERS_LIST:
        for label, use_yrem, p_col in configs:
            t0 = time.time()
            pur_all, grav_all = [], []

            for seed in seeds:
                pos, adj, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
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
                sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                if not sa or not sb:
                    continue
                blocked = set(bi) - set(sa + sb)
                grav_layer = layers[2 * len(layers) // 3]
                mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
                if not mass_nodes:
                    continue
                mass_set = set(mass_nodes)

                protected = set(src) | set(det_list) | set(sa + sb)
                if use_yrem:
                    adj, _ = apply_y_removal(pos, adj, bl, 2.0, protected)

                field_m = compute_field_3d(pos, mass_nodes)
                field_f = [0.0] * n

                if p_col > 0:
                    r = mc_purity_and_gravity(
                        pos, adj, field_m, field_f, src, det_list,
                        blocked | set(sb), blocked | set(sa), blocked,
                        mass_set, K_BAND, p_col, N_REALIZATIONS)
                else:
                    # No collapse — standard CL-like purity from single propagation
                    gv, pv = [], []
                    for k in K_BAND:
                        am = propagate_3d(pos, adj, field_m, src, k, blocked)
                        af = propagate_3d(pos, adj, field_f, src, k, blocked)
                        pm = sum(abs(am[d]) ** 2 for d in det_list)
                        pf = sum(abs(af[d]) ** 2 for d in det_list)
                        if pm > 1e-30 and pf > 1e-30:
                            ym = sum(abs(am[d]) ** 2 * pos[d][1] for d in det_list) / pm
                            yf = sum(abs(af[d]) ** 2 * pos[d][1] for d in det_list) / pf
                            gv.append(ym - yf)
                        aa = propagate_3d(pos, adj, field_m, src, k, blocked | set(sb))
                        ab = propagate_3d(pos, adj, field_m, src, k, blocked | set(sa))
                        psi = [aa[d] + ab[d] for d in det_list]
                        nsq = sum(abs(p) ** 2 for p in psi)
                        if nsq < 1e-30:
                            continue
                        rho = {}
                        for i2, d1 in enumerate(det_list):
                            for j2, d2 in enumerate(det_list):
                                rho[(d1, d2)] = psi[i2] * psi[j2].conjugate()
                        tr = sum(rho[(d, d)] for d in det_list).real
                        if tr < 1e-30:
                            continue
                        for key in rho:
                            rho[key] /= tr
                        pu = sum(abs(v) ** 2 for v in rho.values()).real
                        pv.append(pu)
                    r = None
                    if gv and pv:
                        r = {"pur": sum(pv) / len(pv), "gravity": sum(gv) / len(gv)}

                if r:
                    pur_all.append(r["pur"])
                    grav_all.append(r["gravity"])

            dt = time.time() - t0
            if pur_all:
                mp, sep = _mean_se(pur_all)
                mg, seg = _mean_se(grav_all)
                gt = mg / seg if seg > 0 else 0
                omp = 1 - mp
                print(f"  {nl:4d}  {label:>14s}  {mp:7.4f}±{sep:.3f}  {omp:8.4f}  "
                      f"{mg:+8.4f}±{seg:.3f}  {gt:+6.2f}  {len(pur_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>14s}  FAIL  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  If collapse exponent is positive: decoherence grows with N")
    print("  If |y|+col > col alone: topology helps collapse")
    print("  Gravity grav_t > 2: phase valley survives collapse")


if __name__ == "__main__":
    main()
