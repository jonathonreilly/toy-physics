#!/usr/bin/env python3
"""Confirm modular DAG pur_min plateau at N=40, N=50.

If pur_min stays ~0.94 (not climbing toward 1), the topology pivot is real.
Also sweeps gap size to find the critical separation threshold.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.topology_families import generate_modular_dag

BETA = 0.8
N_YBINS = 8
LAM = 10.0


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


def compute_field(positions, adj, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate(positions, adj, field, src, k, blocked=None):
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
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def build_setup(positions, adj, env_depth_layers=1, mass_y_half=3.0):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None
    src = by_layer[layers[0]]
    det = set(by_layer[layers[-1]])
    det_list = list(det)
    if not det:
        return None
    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)
    bl_idx = len(layers) // 3
    bl = layers[bl_idx]
    bi = by_layer[bl]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    si = set(sa + sb)
    blocked = set(bi) - si
    start = bl_idx + 1
    stop = min(len(layers), start + max(1, env_depth_layers))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(
            i for i in by_layer[layer]
            if abs(positions[i][1] - cy) <= mass_y_half
        )
    if len(mass_nodes) < 2:
        return None
    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    full_mass = set(mass_nodes) | set(grav_mass)
    field = compute_field(positions, adj, list(full_mass))
    return {
        "n": n, "by_layer": by_layer, "layers": layers,
        "src": src, "det": det, "det_list": det_list, "cy": cy,
        "blocked": blocked, "mass_set": set(mass_nodes), "field": field,
    }


def bin_amplitudes(amps, positions, nodes, y_min, y_max, n_bins=N_YBINS):
    bw = (y_max - y_min) / n_bins
    bins = [0j] * n_bins
    for m in nodes:
        y = positions[m][1]
        b = int((y - y_min) / bw)
        b = max(0, min(n_bins - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity(amps_a, amps_b, D, det_list):
    def _pur(D_val):
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                    + D_val * amps_a[d1].conjugate() * amps_b[d2]
                    + D_val * amps_b[d1].conjugate() * amps_a[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real
    return _pur(D), _pur(1.0), _pur(0.0)


def run_one(nl, gap=4.0, crosslink_prob=0.02, n_seeds=4):
    """Run modular DAG at one N value. Returns dict or None."""
    k_band = [3.0, 5.0, 7.0]
    pm_all, pc_all, pcoh_all, sn_all = [], [], [], []

    for seed in range(n_seeds):
        # Patch gap into generate_modular_dag
        positions, adj, _ = generate_modular_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=seed * 11 + 7,
            crosslink_prob=crosslink_prob,
        )
        setup = build_setup(positions, adj, env_depth_layers=max(1, round(nl / 6)))
        if setup is None:
            continue

        blocked = setup["blocked"]
        field = setup["field"]
        src = setup["src"]
        det_list = setup["det_list"]
        cy = setup["cy"]
        by_layer = setup["by_layer"]
        layers = setup["layers"]
        bl_idx = len(layers) // 3
        bl = layers[bl_idx]
        bi = by_layer[bl]
        sa = [i for i in bi if positions[i][1] > cy + 3][:3]
        sb = [i for i in bi if positions[i][1] < cy - 3][:3]

        pm_k, pc_k, pcoh_k, sn_k = [], [], [], []
        for k in k_band:
            amps_a = propagate(positions, adj, field, src, k, blocked | set(sb))
            amps_b = propagate(positions, adj, field, src, k, blocked | set(sa))

            start = bl_idx + 1
            stop = min(len(layers), start + max(1, round(nl / 6)))
            mid_nodes = []
            for layer in layers[start:stop]:
                mid_nodes.extend(by_layer[layer])

            bins_a = bin_amplitudes(amps_a, positions, mid_nodes, -12.0, 12.0)
            bins_b = bin_amplitudes(amps_b, positions, mid_nodes, -12.0, 12.0)
            S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
            NA = sum(abs(a) ** 2 for a in bins_a)
            NB = sum(abs(b) ** 2 for b in bins_b)
            denom = NA + NB
            S_norm = S / denom if denom > 0 else 0.0
            D = math.exp(-LAM ** 2 * S_norm)

            pc, pcoh, pmin = cl_purity(amps_a, amps_b, D, det_list)
            if not math.isnan(pc):
                pm_k.append(pmin)
                pc_k.append(pc)
                pcoh_k.append(pcoh)
                sn_k.append(S_norm)

        if pm_k:
            pm_all.append(sum(pm_k) / len(pm_k))
            pc_all.append(sum(pc_k) / len(pc_k))
            pcoh_all.append(sum(pcoh_k) / len(pcoh_k))
            sn_all.append(sum(sn_k) / len(sn_k))

    if not pm_all:
        return None
    return {
        "pur_min": sum(pm_all) / len(pm_all),
        "pur_cl": sum(pc_all) / len(pc_all),
        "pur_coh": sum(pcoh_all) / len(pcoh_all),
        "s_norm": sum(sn_all) / len(sn_all),
        "n_ok": len(pm_all),
    }


def main():
    print("=" * 70)
    print("PLATEAU CONFIRMATION: Modular DAG N=8..50")
    print(f"  CL bath lambda={LAM}, gap=4.0, crosslink=0.02")
    print("=" * 70)
    print()

    # Part 1: N extension
    print("PART 1: pur_min vs N (extending to N=40, 50)")
    print(f"  {'N':>4s}  {'pur_min':>8s}  {'pur_cl':>8s}  {'decoh':>8s}  "
          f"{'S_norm':>8s}  {'time':>6s}")
    print(f"  {'-' * 50}")

    for nl in [8, 12, 18, 25, 30, 40]:
        t0 = time.time()
        r = run_one(nl)
        dt = time.time() - t0
        if r:
            decoh = r["pur_coh"] - r["pur_cl"]
            print(f"  {nl:4d}  {r['pur_min']:8.4f}  {r['pur_cl']:8.4f}  "
                  f"{decoh:+8.4f}  {r['s_norm']:8.5f}  {dt:5.0f}s")
        else:
            print(f"  {nl:4d}  FAIL")
        sys.stdout.flush()

    print()
    print("PART 2: Gap size sweep at N=25")
    print(f"  {'gap':>5s}  {'pur_min':>8s}  {'pur_cl':>8s}  {'decoh':>8s}")
    print(f"  {'-' * 35}")

    for gap in [0.0, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0]:
        # Override gap by generating with custom gap parameter
        k_band = [3.0, 5.0, 7.0]
        pm_all, pc_all, pcoh_all = [], [], []
        for seed in range(4):
            positions, adj, _ = generate_modular_dag(
                n_layers=25, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 11 + 7,
                crosslink_prob=0.02, gap=gap,
            )
            setup = build_setup(positions, adj, env_depth_layers=max(1, round(25 / 6)))
            if setup is None:
                continue
            blocked = setup["blocked"]
            field = setup["field"]
            src = setup["src"]
            det_list = setup["det_list"]
            cy = setup["cy"]
            by_layer = setup["by_layer"]
            layers = setup["layers"]
            bl_idx = len(layers) // 3
            bl = layers[bl_idx]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]

            pm_k, pc_k, pcoh_k = [], [], []
            for k in k_band:
                amps_a = propagate(positions, adj, field, src, k, blocked | set(sb))
                amps_b = propagate(positions, adj, field, src, k, blocked | set(sa))

                start = bl_idx + 1
                stop = min(len(layers), start + max(1, round(25 / 6)))
                mid_nodes = []
                for layer in layers[start:stop]:
                    mid_nodes.extend(by_layer[layer])

                bins_a = bin_amplitudes(amps_a, positions, mid_nodes, -12.0, 12.0)
                bins_b = bin_amplitudes(amps_b, positions, mid_nodes, -12.0, 12.0)
                S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
                NA = sum(abs(a) ** 2 for a in bins_a)
                NB = sum(abs(b) ** 2 for b in bins_b)
                denom = NA + NB
                S_norm = S / denom if denom > 0 else 0.0
                D = math.exp(-LAM ** 2 * S_norm)
                pc, pcoh, pmin = cl_purity(amps_a, amps_b, D, det_list)
                if not math.isnan(pc):
                    pm_k.append(pmin)
                    pc_k.append(pc)
                    pcoh_k.append(pcoh)
            if pm_k:
                pm_all.append(sum(pm_k) / len(pm_k))
                pc_all.append(sum(pc_k) / len(pc_k))
                pcoh_all.append(sum(pcoh_k) / len(pcoh_k))

        if pm_all:
            avg_pm = sum(pm_all) / len(pm_all)
            avg_pc = sum(pc_all) / len(pc_all)
            avg_pcoh = sum(pcoh_all) / len(pcoh_all)
            decoh = avg_pcoh - avg_pc
            print(f"  {gap:5.1f}  {avg_pm:8.4f}  {avg_pc:8.4f}  {decoh:+8.4f}")
        else:
            print(f"  {gap:5.1f}  FAIL")

    print()
    print("gap=0 is uniform random (no channel separation)")
    print("Expect: pur_min decreases as gap increases (more separation)")


if __name__ == "__main__":
    main()
