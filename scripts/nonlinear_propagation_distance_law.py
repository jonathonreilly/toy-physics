#!/usr/bin/env python3
"""Bounded probe: can a minimal nonlinear propagation rule change the distance law?

Hypothesis:
  The current path-sum DAG model has structural b-independence under the
  corrected linear propagator. Maybe a minimal local nonlinearity can alter the
  impact-parameter trend and produce a genuine ~1/b-like falloff.

Test discipline:
  - Keep the graph family fixed: small retained 3D modular DAGs.
  - Keep the source/detector geometry fixed.
  - Use one simple nonlinear family only:
      a local saturation on each node amplitude,
      a_i -> a_i / (1 + lambda_nl * |a_i|^2)
  - Preserve the k=0 sanity check whenever possible.
  - Sweep b on a small set of retained modular instances.

This is a frontier probe, not a broad parameter search.
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
LAMBDA_FAMILY = (0.0, 0.25, 0.5, 1.0)


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def select_target_centered_mass_nodes(
    layer_nodes: list[int],
    positions: list[tuple[float, float, float]],
    center_y: float,
    target_b: float,
    mass_count: int,
    mean_offset_tol: float = MEAN_OFFSET_TOL,
) -> list[int]:
    """Choose a same-side contiguous y-window near the desired impact plane."""
    target_y = center_y + target_b
    same_side = [i for i in layer_nodes if positions[i][1] >= center_y]
    ordered = sorted(same_side, key=lambda i: positions[i][1])
    if len(ordered) < mass_count:
        return []

    best_nodes: list[int] = []
    best_score: tuple[float, float, float] | None = None
    for start in range(len(ordered) - mass_count + 1):
        candidate = ordered[start : start + mass_count]
        ys = [positions[i][1] for i in candidate]
        mean_y = statistics.fmean(ys)
        score = (
            abs(mean_y - target_y),
            max(abs(y - target_y) for y in ys),
            statistics.pstdev(ys) if len(ys) > 1 else 0.0,
        )
        if best_score is None or score < best_score:
            best_score = score
            best_nodes = candidate

    if not best_nodes:
        return []
    mean_offset = statistics.fmean(positions[i][1] for i in best_nodes) - center_y
    if abs(mean_offset - target_b) > mean_offset_tol:
        return []
    return best_nodes


def propagate_nonlinear(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    k: float,
    lambda_nl: float,
) -> list[complex]:
    """Path-sum propagation with a minimal local amplitude saturation."""
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for i in order:
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        ai_eff = ai / (1.0 + lambda_nl * (abs(ai) ** 2))
        if abs(ai_eff) < 1e-30:
            continue
        x1, y1, z1 = positions[i]
        for j in adj.get(i, []):
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            amps[j] += ai_eff * cmath.exp(1j * k * act) * w / L
    return amps


def centroid_y(amps: list[complex], positions: list[tuple[float, float, float]], det_list: list[int]) -> float:
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def paired_seed_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    lambda_nl: float,
) -> float | None:
    """Return the k-averaged paired delta for one seed and one mass selection."""
    field_with = compute_field_3d(positions, mass_nodes)
    field_without = [0.0] * len(positions)

    seed_deltas = []
    for k in K_BAND:
        amps_with = propagate_nonlinear(positions, adj, field_with, src, k, lambda_nl)
        amps_without = propagate_nonlinear(positions, adj, field_without, src, k, lambda_nl)

        probs_with = {d: abs(amps_with[d]) ** 2 for d in det_list}
        probs_without = {d: abs(amps_without[d]) ** 2 for d in det_list}
        tot_with = sum(probs_with.values())
        tot_without = sum(probs_without.values())
        if tot_with <= 1e-30 or tot_without <= 1e-30:
            continue

        y_with = sum(positions[d][1] * p for d, p in probs_with.items()) / tot_with
        y_without = sum(positions[d][1] * p for d, p in probs_without.items()) / tot_without
        seed_deltas.append(y_with - y_without)

    if not seed_deltas:
        return None
    return sum(seed_deltas) / len(seed_deltas)


def fit_power_law(bs: list[float], deltas: list[float]) -> tuple[float, float, float] | None:
    """Fit delta ~= c * b^alpha on positive mean deltas."""
    pairs = [(b, d) for b, d in zip(bs, deltas) if b > 0 and d > 0]
    if len(pairs) < 3:
        return None

    xs = [math.log(b) for b, _ in pairs]
    ys = [math.log(d) for _, d in pairs]
    n = len(xs)
    xbar = statistics.fmean(xs)
    ybar = statistics.fmean(ys)
    ss_xx = sum((x - xbar) ** 2 for x in xs)
    ss_xy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    if ss_xx <= 1e-30:
        return None

    alpha = ss_xy / ss_xx
    intercept = ybar - alpha * xbar
    c = math.exp(intercept)
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    ss_res = sum((y - (intercept + alpha * x)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return alpha, c, r2


def run_lambda_family(lambda_nl: float) -> None:
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    n_ok = 0
    mean_deg = None
    k0_delta = None

    for seed in range(N_SEEDS):
        positions, adj = generate_3d_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 5,
            gap=GAP,
        )

        if mean_deg is None:
            mean_deg = sum(len(v) for v in adj.values()) / len(positions) if positions else 0.0

        by_layer = defaultdict(list)
        for idx, (x, y, z) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 7:
            continue

        src = by_layer[layers[0]]
        det_list = list(by_layer[layers[-1]])
        if not det_list:
            continue

        all_ys = [y for _, y, _ in positions]
        center_y = statistics.fmean(all_ys)
        grav_layer = layers[2 * len(layers) // 3]

        for b_target in TARGET_BS:
            mass_nodes = select_target_centered_mass_nodes(
                by_layer[grav_layer],
                positions,
                center_y,
                b_target,
                MASS_COUNT,
            )
            if not mass_nodes:
                continue
            delta = paired_seed_delta(positions, adj, src, det_list, mass_nodes, lambda_nl)
            if delta is not None:
                by_b[b_target].append(delta)

        if k0_delta is None:
            test_b = TARGET_BS[len(TARGET_BS) // 2]
            mass_nodes = select_target_centered_mass_nodes(
                by_layer[grav_layer],
                positions,
                center_y,
                test_b,
                MASS_COUNT,
            )
            if mass_nodes:
                field_with = compute_field_3d(positions, mass_nodes)
                field_without = [0.0] * len(positions)
                am = propagate_nonlinear(positions, adj, field_with, src, 0.0, lambda_nl)
                af = propagate_nonlinear(positions, adj, field_without, src, 0.0, lambda_nl)
                k0_delta = centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list)

        n_ok += 1

    print(f"lambda={lambda_nl:.2f} | mean degree ~ {mean_deg:.2f} | seeds used={n_ok}")
    print(f"  k=0 sanity delta: {k0_delta:+.6e} (should be ~0)")
    print(f"  {'b':>4s}  {'mean_shift':>10s}  {'SE':>8s}  {'t':>7s}  {'shift*b':>10s}")
    print(f"  {'-' * 48}")

    means: list[float] = []
    bs: list[float] = []
    for b_target in TARGET_BS:
        vals = by_b[b_target]
        if not vals:
            print(f"  {b_target:4.1f}  FAIL")
            continue
        mean = statistics.fmean(vals)
        se = statistics.stdev(vals) / math.sqrt(len(vals)) if len(vals) > 1 else 0.0
        t = mean / se if se > 1e-10 else 0.0
        print(f"  {b_target:4.1f}  {mean:+10.4f}  {se:8.4f}  {t:+7.2f}  {mean * b_target:+10.4f}")
        means.append(mean)
        bs.append(b_target)

    fit = fit_power_law(bs, means)
    if fit is None:
        print("  Power-law fit unavailable (need at least 3 positive mean shifts).")
    else:
        alpha, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")
        if abs(alpha + 1.0) < 0.3:
            print("  Interpretation: consistent with ~1/b falloff.")
        elif abs(alpha) < 0.2:
            print("  Interpretation: effectively flat/topological.")
        else:
            print("  Interpretation: nontrivial power law, but not clean 1/b.")
    print()


def main() -> None:
    print("=" * 78)
    print("NONLINEAR PROPAGATION DISTANCE LAW")
    print("  Minimal local saturation rule on retained 3D modular DAGs")
    print(f"  gap={GAP}, b sweep={TARGET_BS}, k-band={K_BAND}, seeds={N_SEEDS}")
    print("=" * 78)
    print("Rule family: a_i -> a_i / (1 + lambda * |a_i|^2)")
    print("Goal: see whether any genuine ~1/b trend appears without changing the graph family.")
    print()

    for lambda_nl in LAMBDA_FAMILY:
        run_lambda_family(lambda_nl)

    print("=" * 78)
    print("BOTTOM LINE")
    print("  If all lambda values stay flat in b, the minimal nonlinearity does not")
    print("  rescue the distance law on the retained modular family.")
    print("=" * 78)


if __name__ == "__main__":
    main()
