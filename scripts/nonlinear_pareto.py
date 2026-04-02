#!/usr/bin/env python3
"""Pareto frontier: nonlinearity strength vs decoherence/Born trade-off.

The full nonlinear propagators beat the ceiling (pur_min=0.89) but
destroy Born (|I₃|/P=1). Is there a sweet spot?

For each nonlinear type, sweep the mixing parameter epsilon:
  amps_final = (1-eps) × amps_linear + eps × amps_nonlinear

eps=0: pure linear (Born OK, ceiling)
eps=1: pure nonlinear (ceiling broken, Born destroyed)
eps=?: find the Pareto frontier

Also test: INTERMITTENT nonlinearity — apply nonlinear step every
K layers instead of every layer. This gives the CLT partial time
to operate (maintaining Born) while periodically breaking it
(lowering ceiling).
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag

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


def propagate_mixed(positions, adj, field, src, k, blocked=None,
                     nl_type="layer_norm", epsilon=0.0, interval=1):
    """Propagate with partial nonlinearity.

    epsilon: mixing strength (0=linear, 1=full nonlinear)
    interval: apply nonlinearity every `interval` layers
    """
    n = len(positions)
    blocked = blocked or set()

    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for layer_idx, layer_key in enumerate(layers):
        for i in by_layer[layer_key]:
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

        # Apply partial nonlinearity
        if epsilon > 0 and layer_idx + 1 < len(layers) and (layer_idx % interval == 0):
            next_nodes = by_layer[layers[layer_idx + 1]]
            if nl_type == "layer_norm":
                total_sq = sum(abs(amps[i]) ** 2 for i in next_nodes)
                if total_sq > 1e-30:
                    norm = math.sqrt(total_sq)
                    for i in next_nodes:
                        linear_val = amps[i]
                        normed_val = amps[i] / norm
                        amps[i] = (1 - epsilon) * linear_val + epsilon * normed_val
            elif nl_type == "saturation":
                a0 = 0.01
                for i in next_nodes:
                    mag = abs(amps[i])
                    if mag > 1e-30:
                        sat_mag = math.tanh(mag / a0) * a0
                        sat_val = amps[i] / mag * sat_mag
                        amps[i] = (1 - epsilon) * amps[i] + epsilon * sat_val

    return amps


def cl_purity_min(amps_a, amps_b, det_list):
    """pur_min only (D=0)."""
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def born_test(positions, adj, field, src, det_list, k, blocked_base,
              slit_sets, nl_type, epsilon, interval):
    """3-slit Born rule: |I₃|/P."""
    all_slits = set()
    for s in slit_sets:
        all_slits.update(s)

    def P(open_set):
        block = blocked_base | (all_slits - open_set)
        amps = propagate_mixed(positions, adj, field, src, k, block,
                                nl_type, epsilon, interval)
        return sum(abs(amps[d]) ** 2 for d in det_list)

    sa, sb, sc = slit_sets
    P_abc = P(set(sa + sb + sc))
    P_ab = P(set(sa + sb))
    P_ac = P(set(sa + sc))
    P_bc = P(set(sb + sc))
    P_a = P(set(sa))
    P_b = P(set(sb))
    P_c = P(set(sc))

    I3 = P_abc - P_ab - P_ac - P_bc + P_a + P_b + P_c
    return abs(I3) / P_abc if P_abc > 1e-30 else math.nan


def run_pareto_point(nl, seed, nl_type, epsilon, interval=1):
    """Return (pur_min, born_violation) for one config."""
    k_band = [3.0, 5.0, 7.0]

    positions, adj, _ = generate_causal_dag(
        n_layers=nl, nodes_per_layer=25, y_range=12.0,
        connect_radius=3.0, rng_seed=seed,
    )

    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y in positions) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]

    slit_upper = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_lower = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not slit_upper or not slit_lower:
        return None
    blocked = set(bi) - set(slit_upper + slit_lower)

    # 3-slit groups for Born test
    sa = [i for i in bi if positions[i][1] > cy + 4][:2]
    sb = [i for i in bi if cy - 1 < positions[i][1] < cy + 1][:2]
    sc = [i for i in bi if positions[i][1] < cy - 4][:2]

    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))

    pm_vals, born_vals = [], []
    for k in k_band:
        amps_a = propagate_mixed(positions, adj, field, src, k,
                                  blocked | set(slit_lower), nl_type, epsilon, interval)
        amps_b = propagate_mixed(positions, adj, field, src, k,
                                  blocked | set(slit_upper), nl_type, epsilon, interval)
        pm = cl_purity_min(amps_a, amps_b, det_list)
        if not math.isnan(pm):
            pm_vals.append(pm)

        if sa and sb and sc:
            blocked_born = set(bi) - set(sa + sb + sc)
            bv = born_test(positions, adj, field, src, det_list, k,
                          blocked_born, [sa, sb, sc], nl_type, epsilon, interval)
            if not math.isnan(bv):
                born_vals.append(bv)

    if not pm_vals:
        return None
    return {
        "pm": sum(pm_vals) / len(pm_vals),
        "born": sum(born_vals) / len(born_vals) if born_vals else math.nan,
    }


def main():
    print("=" * 78)
    print("NONLINEAR PARETO FRONTIER")
    print("  Sweep epsilon (mixing) and interval (intermittency)")
    print(f"  N=60, 12 seeds, k-band [3,5,7]")
    print("=" * 78)
    print()

    nl = 60  # N where ceiling is clear but computation fast
    n_seeds = 12
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    # Part 1: Epsilon sweep (layer_norm)
    print("PART 1: Layer norm, epsilon sweep (every layer)")
    print(f"  {'eps':>6s}  {'pur_min':>8s}  {'|I₃|/P':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 32}")

    for eps in [0.0, 0.01, 0.03, 0.05, 0.10, 0.20, 0.50, 1.0]:
        pm_all, born_all = [], []
        for seed in seeds:
            r = run_pareto_point(nl, seed, "layer_norm", eps)
            if r:
                pm_all.append(r["pm"])
                if not math.isnan(r["born"]):
                    born_all.append(r["born"])

        if pm_all:
            apm = sum(pm_all) / len(pm_all)
            aborn = sum(born_all) / len(born_all) if born_all else math.nan
            born_str = f"{aborn:.4f}" if not math.isnan(aborn) else "N/A"
            print(f"  {eps:6.2f}  {apm:8.4f}  {born_str:>8s}  {len(pm_all):4d}")
        sys.stdout.flush()

    # Part 2: Intermittent nonlinearity (full strength, every K layers)
    print()
    print("PART 2: Layer norm eps=1.0, applied every K layers")
    print(f"  {'K':>4s}  {'pur_min':>8s}  {'|I₃|/P':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 30}")

    for K in [1, 2, 3, 5, 10, 20]:
        pm_all, born_all = [], []
        for seed in seeds:
            r = run_pareto_point(nl, seed, "layer_norm", 1.0, interval=K)
            if r:
                pm_all.append(r["pm"])
                if not math.isnan(r["born"]):
                    born_all.append(r["born"])

        if pm_all:
            apm = sum(pm_all) / len(pm_all)
            aborn = sum(born_all) / len(born_all) if born_all else math.nan
            born_str = f"{aborn:.4f}" if not math.isnan(aborn) else "N/A"
            print(f"  {K:4d}  {apm:8.4f}  {born_str:>8s}  {len(pm_all):4d}")
        sys.stdout.flush()

    # Part 3: Saturation sweep
    print()
    print("PART 3: Saturation, epsilon sweep")
    print(f"  {'eps':>6s}  {'pur_min':>8s}  {'|I₃|/P':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 32}")

    for eps in [0.0, 0.01, 0.05, 0.10, 0.50, 1.0]:
        pm_all, born_all = [], []
        for seed in seeds:
            r = run_pareto_point(nl, seed, "saturation", eps)
            if r:
                pm_all.append(r["pm"])
                if not math.isnan(r["born"]):
                    born_all.append(r["born"])

        if pm_all:
            apm = sum(pm_all) / len(pm_all)
            aborn = sum(born_all) / len(born_all) if born_all else math.nan
            born_str = f"{aborn:.4f}" if not math.isnan(aborn) else "N/A"
            print(f"  {eps:6.2f}  {apm:8.4f}  {born_str:>8s}  {len(pm_all):4d}")
        sys.stdout.flush()

    print()
    print("PARETO OPTIMAL: lowest pur_min where |I₃|/P < 2× baseline")


if __name__ == "__main__":
    main()
