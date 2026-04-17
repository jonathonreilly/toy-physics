#!/usr/bin/env python3
"""Gap stability under perturbation: fill the gap with nodes at controlled
densities and measure where decoherence / gravity / interference break.

Gap-as-physics investigation, Experiment 1.

Independent variable: fill_fraction in {0.00, 0.05, 0.10, 0.25, 0.50, 1.00}
Dependent: pur_cl, gravity centroid shift, S_norm, visibility

Physics question: is there a sharp phase transition in decoherence as the
gap fills, or gradual degradation?
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
N_YBINS = 8
LAM = 10.0
GAP = 4.0
CONNECT_RADIUS = 4.0
XYZ_RANGE = 12.0
NPL = 30
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 16
N_LAYERS_LIST = [12, 25, 40]
FILL_FRACTIONS = [0.00, 0.05, 0.10, 0.25, 0.50, 1.00]


@dataclass(frozen=True)
class FillResult:
    n_layers: int
    fill_fraction: float
    seed: int
    pur_cl: float
    pur_coh: float
    s_norm: float
    gravity: float
    n_fill_nodes: int
    n_bridging_edges: int


# ---------- graph generation ----------

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


def generate_3d_dag_filled_gap(n_layers, nodes_per_layer, xyz_range, connect_radius,
                                rng_seed, gap, fill_fraction):
    """Generate 3D modular DAG then inject fill nodes into the gap region.

    fill_fraction=0.0 -> standard modular DAG
    fill_fraction=1.0 -> gap fully populated (approaches uniform)
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    n_fill_nodes = 0
    n_bridging_edges = 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            # Standard channel nodes
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-xyz_range, xyz_range)
                if layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, xyz_range)
                    else:
                        y = rng.uniform(-xyz_range, -gap / 2)
                else:
                    y = rng.uniform(-xyz_range, xyz_range)

                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)

                        if layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < 0.02:
                                    adj[prev_idx].append(idx)
                        else:
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)

            # Gap-fill nodes (only post-barrier)
            if layer > barrier_layer and fill_fraction > 0:
                n_fill_per_layer = max(1, int(fill_fraction * nodes_per_layer))
                for _ in range(n_fill_per_layer):
                    y = rng.uniform(-gap / 2, gap / 2)
                    z = rng.uniform(-xyz_range, xyz_range)
                    idx = len(positions)
                    positions.append((x, y, z))
                    layer_nodes.append(idx)
                    n_fill_nodes += 1

                    # Fill nodes connect to ALL neighbors within radius
                    # (no crosslink suppression — they bridge channels)
                    for prev_layer in layer_indices[max(0, layer - 2):]:
                        for prev_idx in prev_layer:
                            px, py, pz = positions[prev_idx]
                            dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)
                                # Count edges that bridge channels
                                if abs(positions[prev_idx][1]) > gap / 2:
                                    n_bridging_edges += 1

        layer_indices.append(layer_nodes)

    return positions, dict(adj), n_fill_nodes, n_bridging_edges


# ---------- physics ----------

def propagate_3d(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
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


def bin_amplitudes_3d(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity(amps_a, amps_b, D, det_list):
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
        return math.nan, math.nan
    for key in rho:
        rho[key] /= tr
    pur = sum(abs(v) ** 2 for v in rho.values()).real

    # coherent baseline (D=1)
    rho_c = {}
    for d1 in det_list:
        for d2 in det_list:
            rho_c[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
                + amps_a[d1].conjugate() * amps_b[d2]
                + amps_b[d1].conjugate() * amps_a[d2]
            )
    tr_c = sum(rho_c[(d, d)] for d in det_list).real
    if tr_c <= 1e-30:
        return math.nan, math.nan
    for key in rho_c:
        rho_c[key] /= tr_c
    pur_coh = sum(abs(v) ** 2 for v in rho_c.values()).real

    return pur, pur_coh


# ---------- measurement pipeline ----------

def measure_single(positions, adj, n_layers, k_band):
    """Run joint gravity + decoherence measurement. Returns FillResult fields or None."""
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

    cy = sum(positions[i][1] for i in range(len(positions))) / len(positions)

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

    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])

    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * len(positions)

    grav_vals, pur_vals, pur_coh_vals, sn_vals = [], [], [], []

    for k in k_band:
        # Gravity
        am = propagate_3d(positions, adj, field_m, src, k, blocked)
        af = propagate_3d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d])**2 for d in det_list)
        pf = sum(abs(af[d])**2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)

        # Decoherence (CL bath)
        aa = propagate_3d(positions, adj, field_m, src, k, blocked | set(sb))
        ab = propagate_3d(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes_3d(aa, positions, mid)
        bb = bin_amplitudes_3d(ab, positions, mid)
        S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
        NA = sum(abs(a)**2 for a in ba)
        NB = sum(abs(b)**2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM**2 * Sn)
        pc, pcoh = cl_purity(aa, ab, D_cl, det_list)
        if not math.isnan(pc):
            pur_vals.append(pc)
            pur_coh_vals.append(pcoh)
            sn_vals.append(Sn)

    if not grav_vals or not pur_vals:
        return None

    return {
        "pur_cl": sum(pur_vals) / len(pur_vals),
        "pur_coh": sum(pur_coh_vals) / len(pur_coh_vals),
        "s_norm": sum(sn_vals) / len(sn_vals),
        "gravity": sum(grav_vals) / len(grav_vals),
    }


# ---------- main ----------

def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m)**2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 90)
    print("GAP STABILITY UNDER PERTURBATION")
    print(f"  3D modular DAG, gap={GAP}, connect_radius={CONNECT_RADIUS}")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print(f"  Fill fractions: {FILL_FRACTIONS}")
    print("=" * 90)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]
    all_results = []

    for nl in N_LAYERS_LIST:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'fill':>6s}  {'pur_cl':>10s}  {'pur_coh':>10s}  {'S_norm':>10s}  "
              f"{'gravity':>10s}  {'fill_n':>6s}  {'bridge':>6s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 82}")

        for ff in FILL_FRACTIONS:
            t0 = time.time()
            pc_all, pcoh_all, sn_all, grav_all = [], [], [], []
            fill_n_all, bridge_all = [], []

            for seed in seeds:
                positions, adj, nfill, nbridge = generate_3d_dag_filled_gap(
                    n_layers=nl, nodes_per_layer=NPL, xyz_range=XYZ_RANGE,
                    connect_radius=CONNECT_RADIUS, rng_seed=seed,
                    gap=GAP, fill_fraction=ff,
                )
                r = measure_single(positions, adj, nl, K_BAND)
                if r:
                    pc_all.append(r["pur_cl"])
                    pcoh_all.append(r["pur_coh"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
                    fill_n_all.append(nfill)
                    bridge_all.append(nbridge)

                    all_results.append(FillResult(
                        n_layers=nl, fill_fraction=ff, seed=seed,
                        pur_cl=r["pur_cl"], pur_coh=r["pur_coh"],
                        s_norm=r["s_norm"], gravity=r["gravity"],
                        n_fill_nodes=nfill, n_bridging_edges=nbridge,
                    ))

            dt = time.time() - t0
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                mpcoh, _ = _mean_se(pcoh_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                mfill = sum(fill_n_all) / len(fill_n_all)
                mbridge = sum(bridge_all) / len(bridge_all)
                print(f"  {ff:6.2f}  {mpc:7.4f}±{sepc:.3f}  {mpcoh:7.4f}      "
                      f"{msn:10.4f}  {mg:+7.4f}±{seg:.3f}  {mfill:6.0f}  {mbridge:6.0f}  "
                      f"{len(pc_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {ff:6.2f}  FAIL (0 ok)  {dt:4.0f}s")

        print()

    # k=0 control
    print("  k=0 CONTROL (fill=0.00 and fill=1.00)")
    print(f"  {'fill':>6s}  {'N':>4s}  {'gravity_k0':>12s}")
    print(f"  {'-' * 30}")
    for ff in [0.00, 1.00]:
        for nl in N_LAYERS_LIST:
            g0_all = []
            for seed in seeds[:4]:
                positions, adj, _, _ = generate_3d_dag_filled_gap(
                    n_layers=nl, nodes_per_layer=NPL, xyz_range=XYZ_RANGE,
                    connect_radius=CONNECT_RADIUS, rng_seed=seed,
                    gap=GAP, fill_fraction=ff,
                )
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7:
                    continue
                src = by_layer[layers[0]]
                det_list = list(by_layer[layers[-1]])
                cy = sum(positions[i][1] for i in range(len(positions))) / len(positions)
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if positions[i][1] > cy + 3][:3]
                sb = [i for i in bi if positions[i][1] < cy - 3][:3]
                if not sa or not sb:
                    continue
                blocked = set(bi) - set(sa + sb)
                grav_layer = layers[2 * len(layers) // 3]
                mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
                if not mass_nodes:
                    continue
                field_m = compute_field_3d(positions, mass_nodes)
                field_f = [0.0] * len(positions)
                am = propagate_3d(positions, adj, field_m, src, 0.0, blocked)
                af = propagate_3d(positions, adj, field_f, src, 0.0, blocked)
                pm = sum(abs(am[d])**2 for d in det_list)
                pf = sum(abs(af[d])**2 for d in det_list)
                if pm > 1e-30 and pf > 1e-30:
                    ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
                    yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
                    g0_all.append(ym - yf)
            if g0_all:
                mg0 = sum(g0_all) / len(g0_all)
                print(f"  {ff:6.2f}  {nl:4d}  {mg0:+12.6e}")

    print()
    print("ANALYSIS:")
    print("  - pur_cl < 0.95 at fill=0.00 confirms baseline modular decoherence")
    print("  - Watch for sharp transition vs gradual degradation in pur_cl")
    print("  - S_norm should drop as gap fills (less which-path info)")
    print("  - Gravity should remain positive (phase valley independent of gap)")
    print("  - k=0 control must be zero for all conditions")


if __name__ == "__main__":
    main()
