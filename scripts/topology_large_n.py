#!/usr/bin/env python3
"""Large-N scaling test for modular DAG decoherence.

Push to N=50, 60, 80 to determine asymptotic behavior:
  - Does pur_min keep dropping? (power law? exponential?)
  - Does decoh keep growing?
  - Is there a new floor, or does decoherence approach completeness?

Also tests: does the modular DAG still produce interference?
(Decoherence is meaningless if the two-slit pattern is gone.)
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


def interference_visibility(positions, adj, field, src, det_list, blocked_both):
    """Check two-slit interference visibility on the modular DAG."""
    k = 5.0
    # Both slits open
    amps_both = propagate(positions, adj, field, src, k, blocked_both)
    probs_both = [abs(amps_both[d]) ** 2 for d in det_list]

    # Single slit (slit A only — but we can't easily do this without
    # the slit info, so just check if both-slit pattern has structure)
    total = sum(probs_both)
    if total < 1e-30:
        return 0.0, 0.0

    probs_norm = [p / total for p in probs_both]
    # Visibility = (max - min) / (max + min) among detectors with signal
    active = [p for p in probs_norm if p > 1e-15]
    if len(active) < 2:
        return 0.0, total

    pmax, pmin = max(active), min(active)
    vis = (pmax - pmin) / (pmax + pmin) if (pmax + pmin) > 0 else 0.0
    return vis, total


def main():
    print("=" * 70)
    print("LARGE-N SCALING: Modular DAG Decoherence")
    print(f"  CL bath lambda={LAM}, gap=4.0, crosslink=0.02")
    print(f"  k-band [3,5,7], 4 seeds per N")
    print("=" * 70)
    print()

    n_layers_list = [12, 18, 25, 30, 40, 50, 60]
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 4

    print(f"  {'N':>4s}  {'pur_min':>8s}  {'pur_cl':>8s}  {'decoh':>8s}  "
          f"{'S_norm':>8s}  {'vis':>6s}  {'nodes':>6s}  {'time':>6s}")
    print(f"  {'-' * 62}")

    trajectory = {}

    for nl in n_layers_list:
        t0 = time.time()
        pm_all, pc_all, pcoh_all, sn_all, vis_all = [], [], [], [], []
        n_nodes = 0

        for seed in range(n_seeds):
            positions, adj, _ = generate_modular_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 11 + 7,
                crosslink_prob=0.02, gap=4.0,
            )
            n_nodes = len(positions)

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

            # Interference check (both slits open, only barrier blocks)
            vis, _ = interference_visibility(
                positions, adj, field, src, det_list, blocked)
            vis_all.append(vis)

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

        dt = time.time() - t0

        if pm_all:
            avg_pm = sum(pm_all) / len(pm_all)
            avg_pc = sum(pc_all) / len(pc_all)
            avg_pcoh = sum(pcoh_all) / len(pcoh_all)
            avg_sn = sum(sn_all) / len(sn_all)
            avg_vis = sum(vis_all) / len(vis_all) if vis_all else 0.0
            decoh = avg_pcoh - avg_pc
            trajectory[nl] = {
                "pur_min": avg_pm, "decoh": decoh,
                "s_norm": avg_sn, "vis": avg_vis,
            }
            print(f"  {nl:4d}  {avg_pm:8.4f}  {avg_pc:8.4f}  "
                  f"{decoh:+8.4f}  {avg_sn:8.5f}  {avg_vis:6.3f}  "
                  f"{n_nodes:6d}  {dt:5.0f}s")
        else:
            print(f"  {nl:4d}  {'FAIL':>8s}")

        sys.stdout.flush()

    # Fit power law to pur_min if we have enough points
    print()
    print("=" * 70)
    print("SCALING ANALYSIS")
    print("=" * 70)

    if len(trajectory) >= 4:
        ns = sorted(trajectory.keys())
        pms = [trajectory[n]["pur_min"] for n in ns]
        decohs = [trajectory[n]["decoh"] for n in ns]

        print(f"\n  pur_min trajectory: {' -> '.join(f'{p:.3f}' for p in pms)}")
        print(f"  decoh trajectory:   {' -> '.join(f'{d:+.3f}' for d in decohs)}")

        # Check monotonicity from N=25 onward
        large_ns = [n for n in ns if n >= 25]
        if len(large_ns) >= 2:
            large_pms = [trajectory[n]["pur_min"] for n in large_ns]
            if all(large_pms[i] <= large_pms[i-1] + 0.01 for i in range(1, len(large_pms))):
                print(f"\n  pur_min is NON-INCREASING at large N -> ceiling BROKEN")
            else:
                print(f"\n  pur_min shows rebound at large N -> ceiling may return")

        # Estimate asymptotic behavior
        if len(large_ns) >= 3:
            # log-log fit: pur_min ~ a * N^b + c
            # Simple: check if (1 - pur_min) grows
            gaps = [(n, 1 - trajectory[n]["pur_min"]) for n in large_ns]
            print(f"\n  (1 - pur_min) at large N:")
            for n, g in gaps:
                print(f"    N={n:3d}: 1-pur_min = {g:.4f}")

            # If growing -> decoherence strengthens
            if gaps[-1][1] > gaps[0][1]:
                ratio = gaps[-1][1] / gaps[0][1] if gaps[0][1] > 0 else 0
                n_ratio = gaps[-1][0] / gaps[0][0]
                if ratio > 1 and n_ratio > 1:
                    exponent = math.log(ratio) / math.log(n_ratio)
                    print(f"\n  Rough power law: (1-pur_min) ~ N^{exponent:.2f}")
                    if exponent > 0:
                        print(f"  -> decoherence STRENGTHENS with N (exponent > 0)")
                    else:
                        print(f"  -> decoherence weakens with N")

    print()
    print("INTERFERENCE CHECK:")
    for nl in sorted(trajectory.keys()):
        v = trajectory[nl]["vis"]
        status = "OK" if v > 0.1 else "WEAK" if v > 0.01 else "GONE"
        print(f"  N={nl:3d}: visibility={v:.3f}  [{status}]")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
