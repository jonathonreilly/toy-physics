#!/usr/bin/env python3
"""Large-N with 8 seeds to smooth out noise in modular DAG decoherence."""

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


def build_setup(positions, adj, env_depth_layers=1):
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
    blocked = set(bi) - set(sa + sb)
    start = bl_idx + 1
    stop = min(len(layers), start + max(1, env_depth_layers))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    if len(mass_nodes) < 2:
        return None
    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))
    return {
        "by_layer": by_layer, "layers": layers, "src": src,
        "det_list": det_list, "cy": cy, "blocked": blocked, "field": field,
    }


def bin_amplitudes(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS  # -12 to +12
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity_triple(amps_a, amps_b, D, det_list):
    def _pur(Dv):
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                    + Dv * amps_a[d1].conjugate() * amps_b[d2]
                    + Dv * amps_b[d1].conjugate() * amps_a[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real
    return _pur(D), _pur(1.0), _pur(0.0)


def main():
    print("=" * 70)
    print("LARGE-N SCALING (8 seeds, smoothed)")
    print(f"  Modular DAG, CL bath lambda={LAM}")
    print("=" * 70)
    print()

    n_layers_list = [12, 18, 25, 30, 35, 40, 45, 50, 60]
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 8

    print(f"  {'N':>4s}  {'pur_min':>8s}  {'std':>6s}  {'decoh':>8s}  "
          f"{'S_norm':>8s}  {'n_ok':>4s}  {'time':>6s}")
    print(f"  {'-' * 54}")

    trajectory = {}

    for nl in n_layers_list:
        t0 = time.time()
        pm_per_seed = []

        for seed in range(n_seeds):
            positions, adj, _ = generate_modular_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 7 + 3,
                crosslink_prob=0.02, gap=4.0,
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
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]

            pm_k, pc_k, pcoh_k, sn_k = [], [], [], []
            for k in k_band:
                amps_a = propagate(positions, adj, field, src, k, blocked | set(sb))
                amps_b = propagate(positions, adj, field, src, k, blocked | set(sa))

                start = bl_idx + 1
                stop = min(len(layers), start + max(1, round(nl / 6)))
                mid = []
                for layer in layers[start:stop]:
                    mid.extend(by_layer[layer])

                ba = bin_amplitudes(amps_a, positions, mid)
                bb = bin_amplitudes(amps_b, positions, mid)
                S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
                NA = sum(abs(a) ** 2 for a in ba)
                NB = sum(abs(b) ** 2 for b in bb)
                Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
                D = math.exp(-LAM ** 2 * Sn)

                pc, pcoh, pmin = cl_purity_triple(amps_a, amps_b, D, det_list)
                if not math.isnan(pc):
                    pm_k.append(pmin)
                    pc_k.append(pc)
                    pcoh_k.append(pcoh)
                    sn_k.append(Sn)

            if pm_k:
                pm_per_seed.append({
                    "pm": sum(pm_k) / len(pm_k),
                    "pc": sum(pc_k) / len(pc_k),
                    "pcoh": sum(pcoh_k) / len(pcoh_k),
                    "sn": sum(sn_k) / len(sn_k),
                })

        dt = time.time() - t0

        if pm_per_seed:
            pms = [s["pm"] for s in pm_per_seed]
            pcs = [s["pc"] for s in pm_per_seed]
            pcohs = [s["pcoh"] for s in pm_per_seed]
            sns = [s["sn"] for s in pm_per_seed]

            avg_pm = sum(pms) / len(pms)
            avg_pc = sum(pcs) / len(pcs)
            avg_pcoh = sum(pcohs) / len(pcohs)
            avg_sn = sum(sns) / len(sns)
            std_pm = (sum((p - avg_pm) ** 2 for p in pms) / len(pms)) ** 0.5
            decoh = avg_pcoh - avg_pc

            trajectory[nl] = {"pm": avg_pm, "std": std_pm, "decoh": decoh, "sn": avg_sn}
            print(f"  {nl:4d}  {avg_pm:8.4f}  {std_pm:6.4f}  {decoh:+8.4f}  "
                  f"{avg_sn:8.5f}  {len(pm_per_seed):4d}  {dt:5.0f}s")
        else:
            print(f"  {nl:4d}  FAIL")

        sys.stdout.flush()

    print()
    if trajectory:
        ns = sorted(trajectory.keys())
        print("SUMMARY:")
        print(f"  pur_min range: {min(trajectory[n]['pm'] for n in ns):.3f} - "
              f"{max(trajectory[n]['pm'] for n in ns):.3f}")
        print(f"  decoh range:   {min(trajectory[n]['decoh'] for n in ns):+.3f} - "
              f"{max(trajectory[n]['decoh'] for n in ns):+.3f}")

        large = [n for n in ns if n >= 25]
        if large:
            large_pms = [trajectory[n]["pm"] for n in large]
            avg_large = sum(large_pms) / len(large_pms)
            print(f"\n  Mean pur_min for N>=25: {avg_large:.4f}")
            print(f"  (Uniform DAG baseline at N=25: ~0.986)")
            print(f"  (Modular DAG improvement: {0.986 - avg_large:+.3f})")

            # Is the trend flat, improving, or worsening?
            if len(large) >= 3:
                first_third = large_pms[:len(large_pms)//3+1]
                last_third = large_pms[-(len(large_pms)//3+1):]
                avg_first = sum(first_third) / len(first_third)
                avg_last = sum(last_third) / len(last_third)
                if avg_last < avg_first - 0.005:
                    print(f"  Trend: IMPROVING (later N has lower pur_min)")
                elif avg_last > avg_first + 0.005:
                    print(f"  Trend: WORSENING (later N has higher pur_min)")
                else:
                    print(f"  Trend: STABLE (pur_min plateau)")


if __name__ == "__main__":
    main()
