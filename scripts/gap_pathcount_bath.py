#!/usr/bin/env python3
"""Path-count bath: CL-like decoherence using path-count distinguishability.

INSIGHT: The CL bath uses S_norm (y-bin amplitude distinguishability),
which CLT kills at large N. But path-count asymmetry DOESN'T CLT-converge
(Exp 9). What if we couple the bath to path-count structure instead?

For each environment node m, define:
  D_path(m) = |n_A(m) - n_B(m)| / (n_A(m) + n_B(m))
where n_A, n_B are path counts from each slit.

Then the bath coupling becomes:
  S_path = Σ_m D_path(m)² × |amp(m)|²  (weighted by amplitude at m)
  D_cl = exp(-λ² × S_path / norm)

This is a CL-like bath that measures which-path info via TOPOLOGICAL
(path-count) structure rather than GEOMETRIC (y-bin) structure.

If S_path doesn't decay as 1/N, the decoherence won't have a 1/N ceiling.

Single-k measurement throughout — no k-band averaging.
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
LAM = 10.0
CONNECT_RADIUS = 4.0
XYZ_RANGE = 12.0
NPL = 50
K_SINGLE = 5.0  # Single k — no band averaging
N_SEEDS = 16
N_LAYERS_LIST = [12, 25, 40, 60, 80]


def _topo_order(adj, n):
    in_deg = [0] * n
    for nbs in adj.values():
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
    return order


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
            layer_nodes.append(len(positions)-1)
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
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3


def compute_path_count(adj, start_nodes, n, order):
    counts = [0] * n
    for s in start_nodes:
        counts[s] = 1
    for i in order:
        if counts[i] == 0: continue
        for j in adj.get(i, []):
            counts[j] += counts[i]
    return counts


def propagate_3d(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked: continue
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
            amps[j] += amps[i] * ea
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


def cl_purity_single_k(amps_a, amps_b, D, det_list):
    """Single-k CL purity (not k-averaged)."""
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
                + D * amps_a[d1].conjugate() * amps_b[d2]
                + D * amps_b[d1].conjugate() * amps_a[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def _mean_se(vals):
    if not vals: return 0.0, 0.0
    m = sum(vals)/len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v-m)**2 for v in vals)/(len(vals)-1)
    return m, math.sqrt(var/len(vals))


def main():
    print("=" * 100)
    print("PATH-COUNT BATH: TOPOLOGICAL CL-LIKE DECOHERENCE")
    print(f"  Single k={K_SINGLE}, NPL={NPL}, lambda={LAM}, {N_SEEDS} seeds")
    print(f"  Compare: y-bin bath (standard) vs path-count bath (new)")
    print("=" * 100)
    print()

    seeds = [s*7+3 for s in range(N_SEEDS)]

    print(f"  {'N':>4s}  {'bath':>12s}  {'pur_cl':>10s}  {'S/S_path':>10s}  "
          f"{'gravity':>10s}  {'ok':>3s}")
    print(f"  {'-' * 60}")

    for nl in N_LAYERS_LIST:
        for bath_type in ["y-bin", "path-count", "path+|y|"]:
            pur_all, s_all, grav_all = [], [], []

            for seed in seeds:
                pos, adj, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
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
                if not mass_nodes: continue

                # Apply |y|-removal for path+|y| bath
                adj_use = adj
                if bath_type == "path+|y|":
                    protected = set(src) | set(det_list) | set(sa + sb)
                    removed = set()
                    for idx, (x, y, z) in enumerate(pos):
                        if x <= bl or idx in protected: continue
                        if abs(y) < 2.0: removed.add(idx)
                    new_adj = {}
                    for i, nbs in adj.items():
                        if i in removed: continue
                        new_nbs = [j for j in nbs if j not in removed]
                        if new_nbs: new_adj[i] = new_nbs
                    adj_use = new_adj

                # Environment nodes
                env_depth = max(1, round(nl / 6))
                start = bl_idx + 1
                stop = min(len(layers) - 1, start + env_depth)
                mid = []
                for layer in layers[start:stop]:
                    mid.extend(by_layer[layer])

                field_m = compute_field_3d(pos, mass_nodes)
                field_f = [0.0] * n

                # Single-slit propagations
                aa = propagate_3d(pos, adj_use, field_m, src, K_SINGLE, blocked | set(sb))
                ab = propagate_3d(pos, adj_use, field_m, src, K_SINGLE, blocked | set(sa))

                if bath_type == "y-bin" or bath_type == "path+|y|":
                    # Standard y-bin bath
                    N_YBINS = 8
                    bw = 24.0 / N_YBINS
                    ba = [0j] * N_YBINS
                    bb = [0j] * N_YBINS
                    for m in mid:
                        y = pos[m][1]
                        b = int((y + 12.0) / bw)
                        b = max(0, min(N_YBINS - 1, b))
                        ba[b] += aa[m]
                        bb[b] += ab[m]
                    S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
                    NA = sum(abs(a)**2 for a in ba)
                    NB = sum(abs(b)**2 for b in bb)
                    Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0

                elif bath_type == "path-count":
                    # Path-count bath
                    order = _topo_order(adj_use, n)
                    adj_a_only = {}
                    blocked_a = blocked | set(sb)
                    for i, nbs in adj_use.items():
                        if i not in blocked_a:
                            adj_a_only[i] = [j for j in nbs if j not in blocked_a]
                    adj_b_only = {}
                    blocked_b = blocked | set(sa)
                    for i, nbs in adj_use.items():
                        if i not in blocked_b:
                            adj_b_only[i] = [j for j in nbs if j not in blocked_b]
                    pc_a = compute_path_count(adj_a_only, sa, n, order)
                    pc_b = compute_path_count(adj_b_only, sb, n, order)

                    # S_path = Σ_m D_path(m)² × (|aa(m)|² + |ab(m)|²)
                    S_num = 0.0
                    S_den = 0.0
                    for m in mid:
                        total_paths = pc_a[m] + pc_b[m]
                        if total_paths > 0:
                            d_path = abs(pc_a[m] - pc_b[m]) / total_paths
                        else:
                            d_path = 0.0
                        amp_weight = abs(aa[m])**2 + abs(ab[m])**2
                        S_num += d_path**2 * amp_weight
                        S_den += amp_weight
                    Sn = S_num / S_den if S_den > 0 else 0.0

                D_cl = math.exp(-LAM**2 * Sn)
                pc = cl_purity_single_k(aa, ab, D_cl, det_list)
                if not math.isnan(pc):
                    pur_all.append(pc)
                    s_all.append(Sn)

                # Gravity
                am = propagate_3d(pos, adj_use, field_m, src, K_SINGLE, blocked)
                af = propagate_3d(pos, adj_use, field_f, src, K_SINGLE, blocked)
                pm = sum(abs(am[d])**2 for d in det_list)
                pf = sum(abs(af[d])**2 for d in det_list)
                if pm > 1e-30 and pf > 1e-30:
                    ym = sum(abs(am[d])**2*pos[d][1] for d in det_list)/pm
                    yf = sum(abs(af[d])**2*pos[d][1] for d in det_list)/pf
                    grav_all.append(ym - yf)

            if pur_all:
                mpc, sepc = _mean_se(pur_all)
                ms, _ = _mean_se(s_all)
                mg, seg = _mean_se(grav_all)
                print(f"  {nl:4d}  {bath_type:>12s}  {mpc:7.4f}±{sepc:.3f}  {ms:10.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {len(pur_all):3d}")

        print()

    print("KEY:")
    print("  y-bin: standard CL bath (S_norm from y-bins)")
    print("  path-count: new bath (S from path-count asymmetry)")
    print("  path+|y|: y-bin bath on |y|-pruned graph")
    print()
    print("  If path-count S doesn't decay: ceiling broken by topological bath")
    print("  Single-k throughout — no k-band artifact possible")


if __name__ == "__main__":
    main()
