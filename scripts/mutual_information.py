#!/usr/bin/env python3
"""Mutual information I(slit; detector) — the physically relevant quantity.

Purity measures total coherence loss. Mutual information measures
how much information about which-slit is available at the detector.
This is what actually matters for decoherence.

I(S;D) = H(S) + H(D) - H(S,D)

where S = slit label {A, B}, D = detector node.

P(S=A) = P(S=B) = 0.5 (by construction, equal slits).
P(D=j|S=A) = |ψ_A(j)|² / Σ_j |ψ_A(j)|²
P(D=j|S=B) = |ψ_B(j)|² / Σ_j |ψ_B(j)|²
P(D=j) = 0.5 × P(D=j|A) + 0.5 × P(D=j|B)

H(S) = log(2) = 1 bit
H(D) = -Σ_j P(D=j) log P(D=j)
H(S,D) = -Σ_{s,j} P(S=s,D=j) log P(S=s,D=j)
       = 0.5 × [-Σ_j P(j|A) log(0.5×P(j|A)) - Σ_j P(j|B) log(0.5×P(j|B))]
       = 1 + 0.5 × [H(D|A) + H(D|B)]

I(S;D) = H(D) - 0.5 × [H(D|A) + H(D|B)]

If I(S;D) > 0, the detector carries which-slit information.
If I(S;D) = 0, the detector is completely ignorant of the slit.
Maximum I(S;D) = 1 bit (perfect which-slit discrimination).

Key question: does I(S;D) scale differently from (1-pur_min)?
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.topology_families import generate_modular_dag

BETA = 0.8


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


def compute_field(positions, mass_nodes):
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


def entropy(probs):
    """Shannon entropy in bits."""
    return -sum(p * math.log2(p) for p in probs if p > 1e-30)


def mutual_info_slit_detector(amps_a, amps_b, det_list):
    """Compute I(slit; detector) in bits.

    Returns (MI, H_D, H_D_given_A, H_D_given_B, pur_min).
    """
    # P(D=j|A) and P(D=j|B)
    pa = [abs(amps_a[d]) ** 2 for d in det_list]
    pb = [abs(amps_b[d]) ** 2 for d in det_list]
    na = sum(pa)
    nb = sum(pb)
    if na < 1e-30 or nb < 1e-30:
        return None

    pa = [p / na for p in pa]
    pb = [p / nb for p in pb]

    # P(D=j) = 0.5 * P(j|A) + 0.5 * P(j|B)
    pd = [0.5 * a + 0.5 * b for a, b in zip(pa, pb)]

    H_D = entropy(pd)
    H_D_A = entropy(pa)
    H_D_B = entropy(pb)

    MI = H_D - 0.5 * (H_D_A + H_D_B)

    # Also compute pur_min for comparison
    rho = {}
    for i, d1 in enumerate(det_list):
        for j, d2 in enumerate(det_list):
            rho[(d1, d2)] = (amps_a[d1].conjugate() * amps_a[d2] / na
                              + amps_b[d1].conjugate() * amps_b[d2] / nb)
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    pur_min = sum(abs(v) ** 2 for v in rho.values()).real

    return {"MI": MI, "H_D": H_D, "H_D_A": H_D_A, "H_D_B": H_D_B,
            "pur_min": pur_min}


def run_mi(nl, seed, gap=0.0):
    k_band = [3.0, 5.0, 7.0]

    if gap > 0:
        positions, adj, _ = generate_modular_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=seed, gap=gap)
    else:
        positions, adj, _ = generate_causal_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=seed)

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
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mn = []
    for layer in layers[start:stop]:
        mn.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, list(set(mn) | set(mass)))

    mi_vals, pm_vals = [], []
    for k in k_band:
        aa = propagate(positions, adj, field, src, k, blocked | set(sb))
        ab = propagate(positions, adj, field, src, k, blocked | set(sa))
        r = mutual_info_slit_detector(aa, ab, det_list)
        if r:
            mi_vals.append(r["MI"])
            pm_vals.append(r["pur_min"])

    if not mi_vals:
        return None
    return {
        "MI": sum(mi_vals) / len(mi_vals),
        "pm": sum(pm_vals) / len(pm_vals),
    }


def main():
    print("=" * 70)
    print("MUTUAL INFORMATION I(slit; detector)")
    print("  Does MI scale differently from (1-pur_min)?")
    print("  16 seeds, k-band [3,5,7]")
    print("=" * 70)
    print()

    n_seeds = 16
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    for label, gap in [("2D uniform", 0.0), ("2D modular gap=4", 4.0)]:
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'MI(bits)':>9s}  {'1-pm':>7s}  {'MI/max':>7s}  {'n_ok':>4s}")
        print(f"  {'-' * 38}")

        data_mi, data_pm = {}, {}
        for nl in [12, 18, 25, 30, 40, 60, 80]:
            mi_all, pm_all = [], []
            for seed in seeds:
                r = run_mi(nl, seed, gap)
                if r:
                    mi_all.append(r["MI"])
                    pm_all.append(r["pm"])

            if mi_all:
                avg_mi = sum(mi_all) / len(mi_all)
                avg_pm = sum(pm_all) / len(pm_all)
                data_mi[nl] = avg_mi
                data_pm[nl] = avg_pm
                print(f"  {nl:4d}  {avg_mi:9.6f}  {1-avg_pm:7.4f}  "
                      f"{avg_mi/1.0:7.4f}  {len(mi_all):4d}")
            sys.stdout.flush()

        # Fit MI scaling
        fit_ns = [n for n in sorted(data_mi.keys()) if data_mi[n] > 1e-8]
        if len(fit_ns) >= 3:
            xs = [math.log(n) for n in fit_ns]
            ys = [math.log(data_mi[n]) for n in fit_ns]
            n = len(xs)
            mx = sum(xs) / n
            my = sum(ys) / n
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            syy = sum((y - my) ** 2 for y in ys)
            alpha_mi = sxy / sxx
            r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0
            print(f"\n  MI scaling: MI ~ N^{alpha_mi:.3f}  R²={r2:.3f}")

        # Compare with pur_min scaling
        fit_ns2 = [n for n in sorted(data_pm.keys()) if 1 - data_pm[n] > 0.001]
        if len(fit_ns2) >= 3:
            xs2 = [math.log(n) for n in fit_ns2]
            ys2 = [math.log(1 - data_pm[n]) for n in fit_ns2]
            n2 = len(xs2)
            mx2 = sum(xs2) / n2
            my2 = sum(ys2) / n2
            sxx2 = sum((x - mx2) ** 2 for x in xs2)
            sxy2 = sum((x - mx2) * (y - my2) for x, y in zip(xs2, ys2))
            syy2 = sum((y - my2) ** 2 for y in ys2)
            alpha_pm = sxy2 / sxx2
            r2_pm = (sxy2 ** 2) / (sxx2 * syy2) if syy2 > 0 else 0
            print(f"  pm scaling: (1-pm) ~ N^{alpha_pm:.3f}  R²={r2_pm:.3f}")

            if abs(alpha_mi - alpha_pm) < 0.3:
                print(f"  → MI and (1-pm) scale SIMILARLY (same exponent)")
            else:
                print(f"  → MI and (1-pm) scale DIFFERENTLY")
                print(f"  → MI exponent {alpha_mi:.2f} vs pm exponent {alpha_pm:.2f}")
        print()


if __name__ == "__main__":
    main()
