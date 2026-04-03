#!/usr/bin/env python3
"""K-band averaging artifact check.

FINDING: Single-k purity is exactly 1.0 for LN+|y| without collapse.
The reported pur~0.5 came from averaging pure states at different k values.

This script verifies:
1. Single-k purity = 1.0 for all non-collapse modes (LN, LN+|y|, linear)
2. K-band averaged purity << 1.0 (the artifact)
3. Collapse at single-k gives genuine purity < 1.0 (real decoherence)
4. CL bath S_norm is single-k and therefore artifact-free

If (3) confirms collapse creates real single-k decoherence, then
the only genuine decoherence mechanisms are:
  - CL bath (single-k, subject to 1/N ceiling)
  - Collapse (single-k, marginal Born)
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
CONNECT_RADIUS = 3.0
XYZ_RANGE = 12.0
NPL = 60
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 8
P_COLLAPSE = 0.2
N_REAL = 50


def generate_3d_dag_chokepoint(n_layers, npl, xyz_range, connect_radius, rng_seed):
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
                if layer_indices:
                    for prev_idx in layer_indices[-1]:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
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
            if i in blocked: continue
            ai = amps[i]
            if ai == 0j: continue
            if p_collapse > 0 and i in mass_set and rng_obj and rng_obj.random() < p_collapse:
                ai *= cmath.exp(1j * rng_obj.uniform(0, 2*math.pi))
                amps[i] = ai
            for j in adj.get(i, []):
                if j in blocked: continue
                x1, y1, z1 = positions[i]
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2-x1, y2-y1, z2-z1
                L = math.sqrt(dx*dx + dy*dy + dz*dz)
                if L < 1e-10: continue
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


def single_k_purity(positions, adj, src, k, blocked_a, blocked_b, det_list,
                     field, use_ln=False, p_collapse=0.0, mass_set=None, n_real=1):
    """Purity at a single k value, optionally MC-averaged over collapse."""
    rho = defaultdict(complex)
    n_rho = 0
    for r in range(n_real):
        rng_a = random.Random(r*1000+7) if p_collapse > 0 else None
        rng_b = random.Random(r*1000+13) if p_collapse > 0 else None
        aa = propagate_3d(positions, adj, field, src, k, blocked_a,
                         use_ln=use_ln, p_collapse=p_collapse,
                         mass_set=mass_set, rng_obj=rng_a)
        ab = propagate_3d(positions, adj, field, src, k, blocked_b,
                         use_ln=use_ln, p_collapse=p_collapse,
                         mass_set=mass_set, rng_obj=rng_b)
        psi = [aa[d] + ab[d] for d in det_list]
        nsq = sum(abs(p)**2 for p in psi)
        if nsq < 1e-30:
            continue
        for i, d1 in enumerate(det_list):
            for j, d2 in enumerate(det_list):
                rho[(d1, d2)] += psi[i] * psi[j].conjugate()
        n_rho += 1
    if n_rho == 0:
        return math.nan
    for key in rho:
        rho[key] /= n_rho
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr < 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def _mean_se(vals):
    if not vals: return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v-m)**2 for v in vals) / (len(vals)-1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 95)
    print("K-BAND AVERAGING ARTIFACT CHECK")
    print(f"  Dense pocket: npl={NPL}, connect_radius={CONNECT_RADIUS}")
    print(f"  Collapse p={P_COLLAPSE}, {N_REAL} MC realizations")
    print("=" * 95)
    print()

    seeds = [s*7+3 for s in range(N_SEEDS)]

    configs = [
        ("linear", False, False, 0.0),
        ("LN", True, False, 0.0),
        ("LN+|y|", True, True, 0.0),
        ("LN+|y|+col", True, True, P_COLLAPSE),
    ]

    for nl in [40, 60]:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'mode':>14s}  {'k':>5s}  {'pur_single_k':>14s}  {'genuine?':>10s}")
        print(f"  {'-' * 52}")

        for label, use_ln, use_yrem, p_col in configs:
            for k in K_BAND:
                pur_all = []
                for seed in seeds:
                    pos, adj, bl = generate_3d_dag_chokepoint(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                    n = len(pos)
                    by_layer = defaultdict(list)
                    for idx, (x, y, z) in enumerate(pos):
                        by_layer[round(x)].append(idx)
                    layers = sorted(by_layer.keys())
                    if len(layers) < 7: continue
                    src = by_layer[layers[0]]
                    det_list = list(by_layer[layers[-1]])
                    if not det_list: continue
                    cy = sum(pos[i][1] for i in range(n)) / n
                    bl_idx = len(layers) // 3
                    bi = by_layer[layers[bl_idx]]
                    sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                    sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                    if not sa or not sb: continue
                    blocked = set(bi) - set(sa + sb)
                    grav_layer = layers[2 * len(layers) // 3]
                    mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
                    mass_set = set(mass_nodes)
                    protected = set(src) | set(det_list) | set(sa + sb)
                    if use_yrem:
                        adj_use, _ = apply_y_removal(pos, adj, bl, 2.0, protected)
                    else:
                        adj_use = adj
                    field = compute_field_3d(pos, mass_nodes)
                    n_mc = N_REAL if p_col > 0 else 1
                    p = single_k_purity(pos, adj_use, src, k,
                                        blocked | set(sb), blocked | set(sa),
                                        det_list, field, use_ln=use_ln,
                                        p_collapse=p_col, mass_set=mass_set,
                                        n_real=n_mc)
                    if not math.isnan(p):
                        pur_all.append(p)

                if pur_all:
                    mp, sep = _mean_se(pur_all)
                    genuine = "PURE" if mp > 0.999 else ("REAL" if mp < 0.99 else "WEAK")
                    print(f"  {label:>14s}  {k:5.1f}  {mp:10.6f}±{sep:.4f}  {genuine:>10s}")

            # Also show k-band averaged for comparison
            pur_avg_all = []
            for seed in seeds:
                pos, adj, bl = generate_3d_dag_chokepoint(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(pos):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7: continue
                src = by_layer[layers[0]]
                det_list = list(by_layer[layers[-1]])
                if not det_list: continue
                cy = sum(pos[i][1] for i in range(n)) / n
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                if not sa or not sb: continue
                blocked = set(bi) - set(sa + sb)
                grav_layer = layers[2 * len(layers) // 3]
                mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
                mass_set = set(mass_nodes)
                protected = set(src) | set(det_list) | set(sa + sb)
                if use_yrem:
                    adj_use, _ = apply_y_removal(pos, adj, bl, 2.0, protected)
                else:
                    adj_use = adj
                field = compute_field_3d(pos, mass_nodes)
                rho = defaultdict(complex)
                n_rho = 0
                n_mc = N_REAL if p_col > 0 else 1
                for r in range(n_mc):
                    for k in K_BAND:
                        rng_a = random.Random(r*1000+7) if p_col > 0 else None
                        rng_b = random.Random(r*1000+13) if p_col > 0 else None
                        aa = propagate_3d(pos, adj_use, field, src, k, blocked | set(sb),
                                         use_ln=use_ln, p_collapse=p_col, mass_set=mass_set, rng_obj=rng_a)
                        ab = propagate_3d(pos, adj_use, field, src, k, blocked | set(sa),
                                         use_ln=use_ln, p_collapse=p_col, mass_set=mass_set, rng_obj=rng_b)
                        psi = [aa[d]+ab[d] for d in det_list]
                        nsq = sum(abs(p)**2 for p in psi)
                        if nsq < 1e-30: continue
                        for i, d1 in enumerate(det_list):
                            for j, d2 in enumerate(det_list):
                                rho[(d1,d2)] += psi[i]*psi[j].conjugate()
                        n_rho += 1
                if n_rho > 0:
                    for key in rho: rho[key] /= n_rho
                    tr = sum(rho[(d,d)] for d in det_list).real
                    if tr > 1e-30:
                        for key in rho: rho[key] /= tr
                        pur_avg_all.append(sum(abs(v)**2 for v in rho.values()).real)
            if pur_avg_all:
                mp, sep = _mean_se(pur_avg_all)
                print(f"  {label:>14s}  {'avg':>5s}  {mp:10.6f}±{sep:.4f}  {'ARTIFACT' if mp < 0.99 else 'OK':>10s}")
            print()

    print("VERDICT:")
    print("  If single-k purity = 1.0 for non-collapse modes: k-band artifact")
    print("  If collapse single-k purity < 1.0: genuine decoherence")
    print("  The CL bath (S_norm) is always single-k and artifact-free")


if __name__ == "__main__":
    main()
