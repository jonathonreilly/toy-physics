#!/usr/bin/env python3
"""Soft domain wall: create gap via edge deletion, not node exclusion.

Gap-as-physics investigation, Experiment 5 (promoted due to Exp 1 results).

Start with a UNIFORM 3D DAG (no imposed gap). Apply edge deletion:
for each edge (i,j) where both nodes are post-barrier, compute
  y_mid = 0.5 * (y_i + y_j)
  P(delete) = 1 - exp(-tension * exp(-y_mid^2 / (2*sigma^2)))

This creates a soft gap centered at y=0. High tension -> more edges deleted
near y=0 -> stronger channel separation. The gap emerges from an interaction
rather than being imposed as a boundary condition.

Also test node-weight variant: instead of deleting edges, apply a propagation
penalty to edges crossing the gap region (amplitude attenuated by factor
exp(-penalty * exp(-y_mid^2 / (2*sigma^2)))).

Physics question: can a tension-like interaction create enough channel
separation for decoherence, without imposing hard node exclusion?
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
CONNECT_RADIUS = 4.0
XYZ_RANGE = 12.0
NPL = 30
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 16
N_LAYERS_LIST = [12, 25, 40]
TENSIONS = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0]
SIGMAS = [1.0, 2.0]


@dataclass(frozen=True)
class TensionResult:
    n_layers: int
    tension: float
    sigma: float
    mode: str
    seed: int
    pur_cl: float
    s_norm: float
    gravity: float
    edges_deleted: int
    edges_total: int
    connected: bool


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


def generate_3d_dag_uniform(n_layers, nodes_per_layer, xyz_range, connect_radius, rng_seed):
    """Generate standard uniform 3D DAG (no gap)."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
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

    return positions, dict(adj), barrier_layer


def apply_edge_tension(positions, adj, barrier_layer, tension, sigma, rng_seed):
    """Delete edges near y=0 in post-barrier region. Returns modified adj + stats."""
    rng = random.Random(rng_seed + 99999)
    new_adj = {}
    edges_deleted = 0
    edges_total = 0

    for i, neighbors in adj.items():
        new_neighbors = []
        for j in neighbors:
            xi = positions[i][0]
            xj = positions[j][0]
            edges_total += 1

            # Only apply tension to post-barrier edges
            if xi > barrier_layer and xj > barrier_layer:
                yi, yj = positions[i][1], positions[j][1]
                y_mid = 0.5 * (yi + yj)
                p_delete = 1 - math.exp(-tension * math.exp(-y_mid**2 / (2 * sigma**2)))
                if rng.random() < p_delete:
                    edges_deleted += 1
                    continue

            new_neighbors.append(j)
        if new_neighbors:
            new_adj[i] = new_neighbors

    return new_adj, edges_deleted, edges_total


def check_connectivity(adj, src, det_list, n):
    """Check if all detector nodes are reachable from source."""
    visited = set()
    queue = deque(src)
    for s in src:
        visited.add(s)
    while queue:
        node = queue.popleft()
        for nb in adj.get(node, []):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return all(d in visited for d in det_list)


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


def propagate_3d_with_penalty(positions, adj, field, src, k, blocked, penalty, sigma):
    """Propagate with amplitude penalty near y=0 instead of edge deletion."""
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

            # Soft penalty near y=0
            y_mid = 0.5 * (y1 + y2)
            gap_factor = math.exp(-penalty * math.exp(-y_mid**2 / (2 * sigma**2)))

            ea = cmath.exp(1j * k * act) * w * gap_factor / L
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
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


# ---------- measurement ----------

def measure_single(positions, adj, n_layers, k_band, propagate_fn=None):
    if propagate_fn is None:
        propagate_fn = lambda pos, a, f, s, k, b: propagate_3d(pos, a, f, s, k, b)

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

    grav_vals, pur_vals, sn_vals = [], [], []

    for k in k_band:
        am = propagate_fn(positions, adj, field_m, src, k, blocked)
        af = propagate_fn(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d])**2 for d in det_list)
        pf = sum(abs(af[d])**2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)

        aa = propagate_fn(positions, adj, field_m, src, k, blocked | set(sb))
        ab = propagate_fn(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes_3d(aa, positions, mid)
        bb = bin_amplitudes_3d(ab, positions, mid)
        S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
        NA = sum(abs(a)**2 for a in ba)
        NB = sum(abs(b)**2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM**2 * Sn)
        pc = cl_purity(aa, ab, D_cl, det_list)
        if not math.isnan(pc):
            pur_vals.append(pc)
            sn_vals.append(Sn)

    if not grav_vals or not pur_vals:
        return None

    return {
        "pur_cl": sum(pur_vals) / len(pur_vals),
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
    print("=" * 95)
    print("SOFT DOMAIN WALL: GAP VIA EDGE TENSION")
    print(f"  3D uniform DAG + edge deletion near y=0")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print(f"  Tensions: {TENSIONS}")
    print(f"  Sigmas: {SIGMAS}")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    # Part 1: Edge deletion mode
    print("PART 1: EDGE DELETION")
    print()
    for sig in SIGMAS:
        for nl in N_LAYERS_LIST:
            print(f"  sigma={sig}, N_LAYERS={nl}")
            print(f"  {'tension':>8s}  {'pur_cl':>10s}  {'S_norm':>8s}  {'gravity':>10s}  "
                  f"{'del%':>5s}  {'conn':>4s}  {'ok':>3s}  {'time':>5s}")
            print(f"  {'-' * 68}")

            for tension in TENSIONS:
                t0 = time.time()
                pc_all, sn_all, grav_all = [], [], []
                del_pct_all = []
                n_connected = 0

                for seed in seeds:
                    positions, adj_raw, barrier_layer = generate_3d_dag_uniform(
                        n_layers=nl, nodes_per_layer=NPL, xyz_range=XYZ_RANGE,
                        connect_radius=CONNECT_RADIUS, rng_seed=seed,
                    )

                    if tension > 0:
                        adj_mod, n_del, n_tot = apply_edge_tension(
                            positions, adj_raw, barrier_layer, tension, sig, seed,
                        )
                        del_pct = 100 * n_del / max(1, n_tot)
                    else:
                        adj_mod = adj_raw
                        n_del, n_tot = 0, sum(len(v) for v in adj_raw.values())
                        del_pct = 0.0

                    del_pct_all.append(del_pct)

                    # Check connectivity
                    by_layer = defaultdict(list)
                    for idx, (x, y, z) in enumerate(positions):
                        by_layer[round(x)].append(idx)
                    layers_sorted = sorted(by_layer.keys())
                    src = by_layer[layers_sorted[0]]
                    det_list = list(by_layer[layers_sorted[-1]])
                    conn = check_connectivity(adj_mod, src, det_list, len(positions))
                    if conn:
                        n_connected += 1

                    r = measure_single(positions, adj_mod, nl, K_BAND)
                    if r:
                        pc_all.append(r["pur_cl"])
                        sn_all.append(r["s_norm"])
                        grav_all.append(r["gravity"])

                dt = time.time() - t0
                if pc_all:
                    mpc, sepc = _mean_se(pc_all)
                    msn, _ = _mean_se(sn_all)
                    mg, seg = _mean_se(grav_all)
                    mdel = sum(del_pct_all) / len(del_pct_all)
                    print(f"  {tension:8.1f}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                          f"{mg:+7.4f}±{seg:.3f}  {mdel:4.1f}%  {n_connected:4d}  "
                          f"{len(pc_all):3d}  {dt:4.0f}s")
                else:
                    mdel = sum(del_pct_all) / len(del_pct_all) if del_pct_all else 0
                    print(f"  {tension:8.1f}  FAIL  del={mdel:.1f}%  conn={n_connected}  {dt:4.0f}s")

            print()

    # Part 2: Amplitude penalty mode (no edge deletion)
    print()
    print("PART 2: AMPLITUDE PENALTY (no edge deletion)")
    print()
    PENALTIES = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]
    for sig in [2.0]:  # single sigma for penalty mode
        for nl in N_LAYERS_LIST:
            print(f"  sigma={sig}, N_LAYERS={nl}")
            print(f"  {'penalty':>8s}  {'pur_cl':>10s}  {'S_norm':>8s}  {'gravity':>10s}  "
                  f"{'ok':>3s}  {'time':>5s}")
            print(f"  {'-' * 56}")

            for penalty in PENALTIES:
                t0 = time.time()
                pc_all, sn_all, grav_all = [], [], []

                for seed in seeds:
                    positions, adj_raw, barrier_layer = generate_3d_dag_uniform(
                        n_layers=nl, nodes_per_layer=NPL, xyz_range=XYZ_RANGE,
                        connect_radius=CONNECT_RADIUS, rng_seed=seed,
                    )

                    prop_fn = lambda pos, a, f, s, k, b, pen=penalty, si=sig: \
                        propagate_3d_with_penalty(pos, a, f, s, k, b, pen, si)

                    r = measure_single(positions, adj_raw, nl, K_BAND, propagate_fn=prop_fn)
                    if r:
                        pc_all.append(r["pur_cl"])
                        sn_all.append(r["s_norm"])
                        grav_all.append(r["gravity"])

                dt = time.time() - t0
                if pc_all:
                    mpc, sepc = _mean_se(pc_all)
                    msn, _ = _mean_se(sn_all)
                    mg, seg = _mean_se(grav_all)
                    print(f"  {penalty:8.1f}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                          f"{mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")
                else:
                    print(f"  {penalty:8.1f}  FAIL  {dt:4.0f}s")

            print()

    # Hard-gap baseline for comparison
    print()
    print("BASELINE: HARD-GAP MODULAR (gap=4.0)")
    from scripts.gap_stability_perturbation import generate_3d_dag_filled_gap
    for nl in N_LAYERS_LIST:
        pc_all, sn_all, grav_all = [], [], []
        for seed in seeds:
            positions, adj, _, _ = generate_3d_dag_filled_gap(
                n_layers=nl, nodes_per_layer=NPL, xyz_range=XYZ_RANGE,
                connect_radius=CONNECT_RADIUS, rng_seed=seed,
                gap=4.0, fill_fraction=0.0,
            )
            r = measure_single(positions, adj, nl, K_BAND)
            if r:
                pc_all.append(r["pur_cl"])
                sn_all.append(r["s_norm"])
                grav_all.append(r["gravity"])
        if pc_all:
            mpc, sepc = _mean_se(pc_all)
            msn, _ = _mean_se(sn_all)
            mg, seg = _mean_se(grav_all)
            print(f"  N={nl:3d}  pur_cl={mpc:.4f}±{sepc:.3f}  S_norm={msn:.4f}  "
                  f"gravity={mg:+.4f}±{seg:.3f}")

    print()
    print("ANALYSIS:")
    print("  - Compare edge-deletion pur_cl to hard-gap baseline")
    print("  - Does tension create enough separation for decoherence?")
    print("  - Does amplitude penalty work as well as edge deletion?")
    print("  - At what tension does connectivity break?")


if __name__ == "__main__":
    main()
