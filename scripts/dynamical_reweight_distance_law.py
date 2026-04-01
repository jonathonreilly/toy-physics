#!/usr/bin/env python3
"""Dynamical graph reweighting: does field-dependent edge conductance rescue 1/b?

Every fixed-graph rescue has failed. This tests making the graph itself
respond to the field — a minimal metric emergence.

Mechanism: field-dependent edge conductance factor.
  conductance = (1 + alpha * f_avg)^gamma
  ea = exp(i*k*S) * directional_weight * conductance / L

At alpha=0: baseline (known flat).
At alpha>0: edges near mass get higher conductance → more amplitude
flows through near-mass paths.

Critical control: k=0 propagation also gets the conductance boost.
If b-dependence appears equally at k=0 and k>0, it's trivial geometric
bias (brute-force reweighting), not phase-mediated gravity. The k>0
EXCESS over k=0 is the real signal.

Fixed-mass discipline: same mass count and geometry across all b values.

PStack experiment: dynamical-reweight-distance-law
"""

from __future__ import annotations

import cmath
import math
import os
import statistics
import sys
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.three_d_joint_test import compute_field_3d, generate_3d_dag  # noqa: E402


def _make_layer_indices(positions):
    """Reconstruct layer indices from positions (grouped by integer x)."""
    by_layer = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    return [by_layer[k] for k in sorted(by_layer)]

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 8
N_LAYERS = 20
NODES_PER_LAYER = 24
XYZ_RANGE = 12.0
CONNECT_RADIUS = 3.0
GAP = 3.0
TARGET_BS = (1.5, 2.5, 3.5, 5.0, 7.0)
MASS_COUNT = 8
MEAN_OFFSET_TOL = 1.0


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


def select_target_centered_mass_nodes(layer_nodes, positions, center_y,
                                       target_b, mass_count,
                                       mean_offset_tol=MEAN_OFFSET_TOL):
    target_y = center_y + target_b
    same_side = [i for i in layer_nodes if positions[i][1] >= center_y]
    ordered = sorted(same_side, key=lambda i: positions[i][1])
    if len(ordered) < mass_count:
        return []
    best_nodes = []
    best_score = None
    for start in range(len(ordered) - mass_count + 1):
        candidate = ordered[start:start + mass_count]
        ys = [positions[i][1] for i in candidate]
        mean_y = statistics.fmean(ys)
        score = (abs(mean_y - target_y),
                 max(abs(y - target_y) for y in ys),
                 statistics.pstdev(ys) if len(ys) > 1 else 0.0)
        if best_score is None or score < best_score:
            best_score = score
            best_nodes = candidate
    if not best_nodes:
        return []
    mean_offset = statistics.fmean(positions[i][1] for i in best_nodes) - center_y
    if abs(mean_offset - target_b) > mean_offset_tol:
        return []
    return best_nodes


def propagate_reweighted(positions, adj, field, src, k, alpha_rw=0.0, gamma_rw=1.0):
    """Propagator with field-dependent edge conductance."""
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        x1, y1, z1 = positions[i]
        for j in adj.get(i, []):
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0.0))
            act = dl - ret
            conductance = (1.0 + alpha_rw * lf) ** gamma_rw
            amps[j] += ai * cmath.exp(1j * k * act) * w * conductance / L
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def _mean(vals):
    return sum(vals) / len(vals) if vals else math.nan


def _se(vals):
    if len(vals) < 2:
        return math.nan
    return statistics.stdev(vals) / math.sqrt(len(vals))


def paired_seed_delta(positions, adj, src, det_list, mass_nodes,
                      k, alpha_rw, gamma_rw):
    field_with = compute_field_3d(positions, mass_nodes)
    field_without = [0.0] * len(positions)
    amps_with = propagate_reweighted(positions, adj, field_with, src, k,
                                     alpha_rw, gamma_rw)
    amps_without = propagate_reweighted(positions, adj, field_without, src, k,
                                        alpha_rw, gamma_rw)
    return (centroid_y(amps_with, positions, det_list) -
            centroid_y(amps_without, positions, det_list))


def run_b_sweep(alpha_rw, gamma_rw=1.0):
    """Run b-sweep with given reweighting parameters. Returns results dict."""
    by_b = {b: [] for b in TARGET_BS}
    k0_deltas = []

    for seed in range(N_SEEDS):
        positions, adj = generate_3d_dag(
            n_layers=N_LAYERS, nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE, connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 11 + 7, gap=GAP,
        )
        layer_indices = _make_layer_indices(positions)
        if len(layer_indices) < 7:
            continue

        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        grav_layer_idx = 2 * len(layer_indices) // 3
        grav_layer = layer_indices[grav_layer_idx]

        # k=0 sanity at fixed b=3.5
        mass_k0 = select_target_centered_mass_nodes(
            grav_layer, positions, center_y, 3.5, MASS_COUNT)
        if mass_k0:
            d0 = paired_seed_delta(positions, adj, src, det_list, mass_k0,
                                   0.0, alpha_rw, gamma_rw)
            k0_deltas.append(d0)

        for target_b in TARGET_BS:
            mass_nodes = select_target_centered_mass_nodes(
                grav_layer, positions, center_y, target_b, MASS_COUNT)
            if not mass_nodes:
                continue
            deltas = [paired_seed_delta(positions, adj, src, det_list,
                                        mass_nodes, k, alpha_rw, gamma_rw)
                      for k in K_BAND]
            by_b[target_b].append(_mean(deltas))

    return by_b, k0_deltas


def fit_power_law(bs, shifts):
    pairs = [(b, s) for b, s in zip(bs, shifts) if b > 0 and s > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(b) for b, _ in pairs]
    ys = [math.log(s) for _, s in pairs]
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxy = sum(x*y for x, y in zip(xs, ys))
    sxx = sum(x*x for x in xs)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    ss_tot = sum((y - sy/n)**2 for y in ys)
    ss_res = sum((y - (slope*x + intercept))**2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return slope, r2


def main():
    print("=" * 74)
    print("DYNAMICAL GRAPH REWEIGHTING: Metric Emergence Pilot")
    print("  conductance = (1 + alpha * f_avg)^gamma")
    print("  Fixed mass geometry, k=0 control")
    print("=" * 74)
    print()

    alpha_sweep = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]

    for alpha_rw in alpha_sweep:
        by_b, k0_deltas = run_b_sweep(alpha_rw)

        k0_mean = _mean(k0_deltas) if k0_deltas else math.nan
        print(f"[alpha={alpha_rw:.1f}] k=0 delta: {k0_mean:+.4e}"
              f" ({'ZERO' if abs(k0_mean) < 0.01 else 'NONZERO — trivial bias!'})")
        print(f"  {'b':>5s}  {'shift':>8s}  {'SE':>6s}  {'t':>5s}  {'shift*b':>8s}  {'n':>3s}")
        print(f"  {'-'*40}")

        bs_for_fit = []
        shifts_for_fit = []

        for b in TARGET_BS:
            vals = by_b[b]
            if not vals:
                print(f"  {b:5.1f}  FAIL")
                continue
            avg = _mean(vals)
            se = _se(vals)
            t = avg / se if se and math.isfinite(se) and se > 1e-12 else 0
            print(f"  {b:5.1f}  {avg:+8.4f}  {se:6.4f}  {t:+5.2f}  {avg*b:+8.3f}  {len(vals):3d}")
            bs_for_fit.append(b)
            shifts_for_fit.append(avg)

        fit = fit_power_law(bs_for_fit, shifts_for_fit)
        if fit:
            slope, r2 = fit
            print(f"  → shift ~ b^{slope:.3f} (R²={r2:.3f})")
            if slope < -0.7:
                if abs(k0_mean) < 0.01:
                    print(f"  ★ DISTANCE FALLOFF with phase-mediated gravity!")
                else:
                    print(f"  ⚠ DISTANCE FALLOFF but k=0 nonzero — may be trivial bias")
            elif slope < -0.3:
                print(f"  → partial falloff")
            else:
                print(f"  → flat or increasing")
        else:
            print(f"  → fit failed (insufficient positive points)")
        print()

    print("=" * 74)
    print("CONTROLS:")
    print("  alpha=0: must reproduce flat b-dependence")
    print("  k=0 ZERO: gravitational deflection requires phase")
    print("  k=0 NONZERO: trivial conductance bias (not gravity)")
    print()
    print("SUCCESS: slope < -0.7 AND k=0 ≈ 0")
    print("FAILURE: slope ≈ 0 (flat) OR k=0 nonzero (trivial)")
    print("=" * 74)


if __name__ == "__main__":
    main()
