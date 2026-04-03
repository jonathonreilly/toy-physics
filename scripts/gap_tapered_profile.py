#!/usr/bin/env python3
"""Tapered gap profile: vary gap width along the causal direction.

Gap-as-physics investigation, Experiment 2.

Profiles:
  uniform   - gap=4.0 everywhere (control)
  narrowing - gap=4.0 at barrier, gap_min at detector
  widening  - gap_min at barrier, gap=4.0 at detector
  pinch     - gap=4.0 at ends, gap_min at midpoint
  partial   - gap=4.0 in first 33% post-barrier (env layers), then 0

Key insight: CL bath environment nodes come from the first ~N/6 post-barrier
layers. The 'partial' profile tests whether the gap only needs to exist where
those environment nodes are.

Physics question: does the gap need to be uniform, or is there a minimal
'throat' width / location requirement?
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
GAP_MAX = 4.0
CONNECT_RADIUS = 4.0
XYZ_RANGE = 12.0
NPL = 30
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 16
N_LAYERS_LIST = [12, 25, 40]
GAP_MINS = [0.0, 1.0, 2.0, 3.0]


@dataclass(frozen=True)
class TaperResult:
    n_layers: int
    profile: str
    gap_min: float
    seed: int
    pur_cl: float
    pur_coh: float
    s_norm: float
    gravity: float
    throat_width: float


# ---------- gap profile functions ----------

def uniform_profile(x_frac, gap_max, gap_min):
    return gap_max


def narrowing_profile(x_frac, gap_max, gap_min):
    """Wide at barrier (x_frac=0), narrow at detector (x_frac=1)."""
    return gap_max + (gap_min - gap_max) * x_frac


def widening_profile(x_frac, gap_max, gap_min):
    """Narrow at barrier (x_frac=0), wide at detector (x_frac=1)."""
    return gap_min + (gap_max - gap_min) * x_frac


def pinch_profile(x_frac, gap_max, gap_min):
    """Wide at ends, narrow at midpoint."""
    return gap_max + (gap_min - gap_max) * (1 - abs(2 * x_frac - 1))


def partial_profile(x_frac, gap_max, gap_min):
    """Gap only in first 33% post-barrier (covers env layers), then zero."""
    return gap_max if x_frac < 0.33 else 0.0


PROFILES = {
    "uniform": uniform_profile,
    "narrowing": narrowing_profile,
    "widening": widening_profile,
    "pinch": pinch_profile,
    "partial": partial_profile,
}


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


def generate_3d_dag_tapered(n_layers, nodes_per_layer, xyz_range, connect_radius,
                             rng_seed, profile_fn, gap_max, gap_min):
    """Generate 3D DAG with gap width varying along causal direction."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    n_post = n_layers - barrier_layer - 1
    throat = gap_max  # track minimum gap encountered

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            # Compute local gap for this layer
            if layer > barrier_layer and n_post > 0:
                x_frac = (layer - barrier_layer - 1) / max(1, n_post - 1)
                local_gap = profile_fn(x_frac, gap_max, gap_min)
                throat = min(throat, local_gap)
            else:
                local_gap = 0.0  # pre-barrier: uniform placement

            use_channels = layer > barrier_layer and local_gap > 0

            for node_i in range(nodes_per_layer):
                z = rng.uniform(-xyz_range, xyz_range)
                if use_channels:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(local_gap / 2, xyz_range)
                    else:
                        y = rng.uniform(-xyz_range, -local_gap / 2)
                else:
                    y = rng.uniform(-xyz_range, xyz_range)

                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)

                        if use_channels and positions[prev_idx][0] > barrier_layer:
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

        layer_indices.append(layer_nodes)

    return positions, dict(adj), throat


# ---------- physics (same as Exp 1) ----------

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


# ---------- measurement ----------

def measure_single(positions, adj, n_layers, k_band):
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
        am = propagate_3d(positions, adj, field_m, src, k, blocked)
        af = propagate_3d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d])**2 for d in det_list)
        pf = sum(abs(af[d])**2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)

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
    print("TAPERED GAP PROFILE EXPERIMENT")
    print(f"  3D modular DAG, gap_max={GAP_MAX}, connect_radius={CONNECT_RADIUS}")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print(f"  Profiles: {list(PROFILES.keys())}")
    print(f"  gap_min values: {GAP_MINS}")
    print("=" * 90)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    for nl in N_LAYERS_LIST:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'profile':>12s}  {'g_min':>5s}  {'throat':>6s}  {'pur_cl':>10s}  "
              f"{'S_norm':>8s}  {'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 72}")

        for pname, pfn in PROFILES.items():
            for gmin in GAP_MINS:
                # uniform doesn't depend on gap_min, run once
                if pname == "uniform" and gmin != GAP_MINS[0]:
                    continue
                # partial doesn't depend on gap_min either
                if pname == "partial" and gmin != GAP_MINS[0]:
                    continue

                t0 = time.time()
                pc_all, sn_all, grav_all, throat_all = [], [], [], []

                for seed in seeds:
                    positions, adj, throat = generate_3d_dag_tapered(
                        n_layers=nl, nodes_per_layer=NPL, xyz_range=XYZ_RANGE,
                        connect_radius=CONNECT_RADIUS, rng_seed=seed,
                        profile_fn=pfn, gap_max=GAP_MAX, gap_min=gmin,
                    )
                    r = measure_single(positions, adj, nl, K_BAND)
                    if r:
                        pc_all.append(r["pur_cl"])
                        sn_all.append(r["s_norm"])
                        grav_all.append(r["gravity"])
                        throat_all.append(throat)

                dt = time.time() - t0
                if pc_all:
                    mpc, sepc = _mean_se(pc_all)
                    msn, _ = _mean_se(sn_all)
                    mg, seg = _mean_se(grav_all)
                    mt = sum(throat_all) / len(throat_all)
                    print(f"  {pname:>12s}  {gmin:5.1f}  {mt:6.1f}  {mpc:7.4f}±{sepc:.3f}  "
                          f"{msn:8.4f}  {mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")
                else:
                    print(f"  {pname:>12s}  {gmin:5.1f}  FAIL  {dt:4.0f}s")

        print()

    # Summary comparison
    print("KEY COMPARISONS:")
    print("  narrowing (wide@barrier, narrow@detector) vs widening (narrow@barrier, wide@detector)")
    print("  → If narrowing >> widening: gap matters most at bath location (early post-barrier)")
    print("  → If widening >> narrowing: gap matters most at detector")
    print()
    print("  partial (gap in first 33% only) vs uniform")
    print("  → If partial ≈ uniform: gap only needed where env nodes are")
    print("  → If partial << uniform: gap needed everywhere")


if __name__ == "__main__":
    main()
