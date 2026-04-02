#!/usr/bin/env python3
"""Nonlinear propagator: can mild nonlinearity beat the 1/N ceiling?

The 1/N ceiling comes from CLT: linear path-sum amplitudes at
detectors converge between slits as N grows. The convergence is
driven by amplitude concentration in dominant paths.

Three nonlinear variants:

NL1: LAYER NORMALIZATION
  After propagating to each layer, normalize: amp[i] /= sqrt(sum|amp|²)
  Prevents amplitude concentration. Preserves relative phases.

NL2: AMPLITUDE SATURATION
  Apply soft saturation: amp → amp × tanh(|amp|/a₀) / |amp|
  Large amplitudes are compressed, small ones pass through.
  a₀ controls saturation threshold.

NL3: PHASE-PRESERVING EQUALIZATION
  After each layer: amp[i] → amp[i] / |amp[i]| × (mean |amp|)
  All amplitudes get the same magnitude but keep their phases.
  This maximally breaks CLT while preserving interference.

For each: test decoherence ceiling AND Born rule (I₃ from 3-slit).
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


def propagate_nonlinear(positions, adj, field, src, k, blocked=None,
                         nl_type="linear", nl_param=1.0):
    """Propagate with optional nonlinearity applied per layer."""
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
        # Propagate from this layer to next
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

        # Apply nonlinearity at the END of propagation from this layer
        if nl_type == "linear":
            pass
        elif nl_type == "layer_norm":
            # Normalize next layer amplitudes
            if layer_idx + 1 < len(layers):
                next_nodes = by_layer[layers[layer_idx + 1]]
                total_sq = sum(abs(amps[i]) ** 2 for i in next_nodes)
                if total_sq > 1e-30:
                    norm = math.sqrt(total_sq)
                    for i in next_nodes:
                        amps[i] /= norm
        elif nl_type == "saturation":
            a0 = nl_param
            if layer_idx + 1 < len(layers):
                next_nodes = by_layer[layers[layer_idx + 1]]
                for i in next_nodes:
                    mag = abs(amps[i])
                    if mag > 1e-30:
                        sat = math.tanh(mag / a0) * a0
                        amps[i] = amps[i] / mag * sat
        elif nl_type == "phase_eq":
            if layer_idx + 1 < len(layers):
                next_nodes = by_layer[layers[layer_idx + 1]]
                mags = [abs(amps[i]) for i in next_nodes if abs(amps[i]) > 1e-30]
                if mags:
                    mean_mag = sum(mags) / len(mags)
                    for i in next_nodes:
                        mag = abs(amps[i])
                        if mag > 1e-30:
                            amps[i] = amps[i] / mag * mean_mag

    return amps


def cl_purity(amps_a, amps_b, D, det_list):
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


def born_rule_test(positions, adj, field, src, k, blocked, slit_sets):
    """3-slit Born rule test: compute I₃ = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C.

    slit_sets = [sa, sb, sc] (three slit node lists).
    I₃ should be ~0 for Born rule compliance.
    """
    all_slits = set()
    for s in slit_sets:
        all_slits.update(s)

    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    det_list = list(by_layer[layers[-1]])

    def total_prob(open_slits, nl_type="linear", nl_param=1.0):
        block = blocked | (all_slits - open_slits)
        amps = propagate_nonlinear(positions, adj, field, src, k, block, nl_type, nl_param)
        return sum(abs(amps[d]) ** 2 for d in det_list)

    return total_prob, det_list


def run_test(nl, seed, nl_type, nl_param):
    """Run decoherence + Born rule for one graph."""
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

    # For 3-slit Born test, need 3 slit groups
    sa = [i for i in bi if positions[i][1] > cy + 4][:2]
    sb = [i for i in bi if cy - 1 < positions[i][1] < cy + 1][:2]
    sc = [i for i in bi if positions[i][1] < cy - 4][:2]

    # For decoherence, use upper/lower slits
    slit_upper = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_lower = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not slit_upper or not slit_lower:
        return None
    blocked = set(bi) - set(slit_upper + slit_lower)

    # Mass/field
    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))

    # Decoherence
    pm_vals = []
    for k in k_band:
        amps_a = propagate_nonlinear(
            positions, adj, field, src, k, blocked | set(slit_lower), nl_type, nl_param)
        amps_b = propagate_nonlinear(
            positions, adj, field, src, k, blocked | set(slit_upper), nl_type, nl_param)

        mid = []
        for layer in layers[start:stop]:
            mid.extend(by_layer[layer])

        ba = [0j] * N_YBINS
        bb = [0j] * N_YBINS
        bw = 24.0 / N_YBINS
        for m in mid:
            b_idx = int((positions[m][1] + 12.0) / bw)
            b_idx = max(0, min(N_YBINS - 1, b_idx))
            ba[b_idx] += amps_a[m]
            bb[b_idx] += amps_b[m]

        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D = math.exp(-LAM ** 2 * Sn)
        pc, pcoh, pmin = cl_purity(amps_a, amps_b, D, det_list)
        if not math.isnan(pc):
            pm_vals.append(pmin)

    # Born rule (3-slit I₃)
    born_vals = []
    if sa and sb and sc:
        blocked_born = set(bi) - set(sa + sb + sc)
        for k in k_band:
            def P(open_set):
                block = blocked_born | (set(sa + sb + sc) - open_set)
                amps = propagate_nonlinear(
                    positions, adj, field, src, k, block, nl_type, nl_param)
                return sum(abs(amps[d]) ** 2 for d in det_list)

            P_abc = P(set(sa + sb + sc))
            P_ab = P(set(sa + sb))
            P_ac = P(set(sa + sc))
            P_bc = P(set(sb + sc))
            P_a = P(set(sa))
            P_b = P(set(sb))
            P_c = P(set(sc))

            I3 = P_abc - P_ab - P_ac - P_bc + P_a + P_b + P_c
            if P_abc > 1e-30:
                born_vals.append(abs(I3) / P_abc)

    if not pm_vals:
        return None
    return {
        "pm": sum(pm_vals) / len(pm_vals),
        "born": sum(born_vals) / len(born_vals) if born_vals else math.nan,
    }


def main():
    print("=" * 78)
    print("NONLINEAR PROPAGATOR: Can nonlinearity beat the 1/N ceiling?")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7], 16 seeds")
    print("=" * 78)
    print()

    n_seeds = 16
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    variants = [
        ("Linear (baseline)", "linear", 1.0),
        ("Layer norm", "layer_norm", 1.0),
        ("Saturation a0=0.01", "saturation", 0.01),
        ("Saturation a0=0.001", "saturation", 0.001),
        ("Phase equalize", "phase_eq", 1.0),
    ]

    for name, nl_type, nl_param in variants:
        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'|I₃|/P':>8s}  {'n_ok':>4s}")
        print(f"  {'-' * 30}")

        for nl in [25, 40, 60, 80]:
            pm_all, born_all = [], []
            for seed in seeds:
                r = run_test(nl, seed, nl_type, nl_param)
                if r:
                    pm_all.append(r["pm"])
                    if not math.isnan(r["born"]):
                        born_all.append(r["born"])

            if pm_all:
                apm = sum(pm_all) / len(pm_all)
                aborn = sum(born_all) / len(born_all) if born_all else math.nan
                born_str = f"{aborn:.2e}" if not math.isnan(aborn) else "N/A"
                print(f"  {nl:4d}  {apm:8.4f}  {born_str:>8s}  {len(pm_all):4d}")
            else:
                print(f"  {nl:4d}  FAIL")
            sys.stdout.flush()

        print()

    print("VERDICT:")
    print("  If nonlinear pur_min < linear pur_min at N=80:")
    print("    → nonlinearity breaks the ceiling")
    print("  If |I₃|/P >> 1e-10:")
    print("    → Born rule violated (bad)")
    print("  Best case: pur_min lower AND |I₃|/P < 1e-5")


if __name__ == "__main__":
    main()
