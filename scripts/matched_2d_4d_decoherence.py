#!/usr/bin/env python3
"""Matched 2D-vs-4D decoherence comparison on the retained modular family.

This script tries to isolate dimensionality as cleanly as the current
infrastructure allows:

  - 2D uses the retained modular DAG family from `topology_families`
  - 4D uses the retained modular DAG family from `four_d_decoherence_large_n`
  - Both use the same slit/barrier convention, same mass-selection rule,
    same k-band, and the same `pur_min` metric
  - The 4D connect radius is chosen per-N to match the 2D mean degree as
    closely as possible on the same seed set

If the 4D exponent still flattens after degree matching, that is stronger
evidence that dimension is doing real work. If not, the current 4D claim is
likely confounded by density/connectivity.
"""

from __future__ import annotations

import argparse
import cmath
import math
import os
import statistics
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.four_d_decoherence_large_n import generate_4d_modular_dag  # type: ignore  # noqa: E402
from scripts.topology_families import generate_modular_dag  # type: ignore  # noqa: E402

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
DEFAULT_N_LIST = (25, 40, 60, 80, 100)
DEFAULT_SEEDS = 8
DEFAULT_2D_RADIUS = 3.0
DEFAULT_4D_RADIUS_GRID = (
    3.5,
    3.75,
    4.0,
    4.25,
    4.5,
    4.75,
    5.0,
    5.25,
    5.5,
    5.75,
    6.0,
)


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


def _mean_degree(adj: dict[int, list[int]], n: int) -> float:
    if n <= 0:
        return math.nan
    return sum(len(nbs) for nbs in adj.values()) / n


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _fit_power_law(ns: list[int], ys: list[float]) -> tuple[float, float, float] | None:
    pairs = [(n, y) for n, y in zip(ns, ys) if n > 0 and y > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(n) for n, _ in pairs]
    zs = [math.log(y) for _, y in pairs]
    n = len(xs)
    mx = sum(xs) / n
    mz = sum(zs) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (z - mz) for x, z in zip(xs, zs))
    szz = sum((z - mz) ** 2 for z in zs)
    if sxx <= 1e-30 or szz <= 1e-30:
        return None
    alpha = sxy / sxx
    intercept = mz - alpha * mx
    r2 = (sxy**2) / (sxx * szz) if sxx > 0 and szz > 0 else 0.0
    return alpha, math.exp(intercept), r2


def _compute_field(positions, adj, mass_idx, iterations: int = 50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    mass_set = set(mass_idx)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        next_field = [0.0] * n
        for i in range(n):
            if i in mass_set:
                next_field[i] = 1.0
            elif undirected.get(i):
                next_field[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = next_field
    return field


def _propagate(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        pi = positions[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pj = positions[j]
            dx = pj[0] - pi[0]
            L = math.sqrt(sum((a - b) ** 2 for a, b in zip(pi, pj)))
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def _pur_min(amps_a, amps_b, det_list):
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


def _setup_2d(nl: int, seed: int, npl: int, radius: float, gap: float):
    positions, adj, layer_indices = generate_modular_dag(
        n_layers=nl,
        nodes_per_layer=npl,
        y_range=12.0,
        connect_radius=radius,
        rng_seed=seed,
        crosslink_prob=0.02,
        gap=gap,
    )
    return positions, adj, layer_indices


def _setup_4d(nl: int, seed: int, npl: int, radius: float, gap: float):
    positions, adj, layer_indices = generate_4d_modular_dag(
        n_layers=nl,
        nodes_per_layer=npl,
        spatial_range=5.0,
        connect_radius=radius,
        rng_seed=seed * 13 + 5,
        gap=gap,
    )
    return positions, adj, layer_indices


def _measure_graph(positions, adj, layer_indices, n_layers: int):
    by_layer: dict[int, list[int]] = {}
    for idx, (x, *_rest) in enumerate(positions):
        by_layer.setdefault(round(x), []).append(idx)
    layers = sorted(by_layer)
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not src or not det_list:
        return None

    cy = sum(pos[1] for pos in positions) / len(positions)
    bl_idx = len(layers) // 3
    barrier = by_layer[layers[bl_idx]]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:3]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:3]
    if not slit_a or not slit_b:
        return None

    blocked = set(barrier) - set(slit_a + slit_b)
    blocked_a = blocked | set(slit_b)
    blocked_b = blocked | set(slit_a)

    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(n_layers / 6)))
    mass_nodes: list[int] = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes.extend(i for i in by_layer[grav_layer] if positions[i][1] > cy + 1)
    if len(mass_nodes) < 2:
        return None

    field = _compute_field(positions, adj, list(set(mass_nodes)))
    pur_vals = []
    for k in K_BAND:
        amps_a = _propagate(positions, adj, field, src, k, blocked_a)
        amps_b = _propagate(positions, adj, field, src, k, blocked_b)
        pur = _pur_min(amps_a, amps_b, det_list)
        if not math.isnan(pur):
            pur_vals.append(pur)

    if not pur_vals:
        return None

    return {
        "pur_min": _mean(pur_vals),
        "mean_degree": _mean_degree(adj, len(positions)),
    }


def _match_4d_radius(target_deg: float, nl: int, npl: int, gap: float, seeds: list[int]) -> float | None:
    best = None
    for radius in DEFAULT_4D_RADIUS_GRID:
        degs = []
        for seed in seeds:
            positions, adj, layer_indices = _setup_4d(nl, seed, npl, radius, gap)
            degs.append(_mean_degree(adj, len(positions)))
        mean_deg = _mean(degs)
        if math.isnan(mean_deg):
            continue
        diff = abs(mean_deg - target_deg)
        if best is None or diff < best[0]:
            best = (diff, radius, mean_deg)
    if best is None:
        return None
    return best[1]


def _fit_per_seed(series: dict[int, dict[int, float]]) -> tuple[list[float], float, float] | None:
    if len(series) < 3:
        return None
    ns = sorted(series)
    common_seeds = set.intersection(*(set(series[n]) for n in ns))
    if len(common_seeds) < 2:
        return None

    alphas = []
    for seed in sorted(common_seeds):
        ys = [series[n][seed] for n in ns]
        fit = _fit_power_law(ns, [1 - y for y in ys])
        if fit is not None:
            alphas.append(fit[0])
    if not alphas:
        return None
    return alphas, _mean(alphas), _se(alphas)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=list(DEFAULT_N_LIST))
    parser.add_argument("--n-seeds", type=int, default=DEFAULT_SEEDS)
    parser.add_argument("--npl", type=int, default=25)
    parser.add_argument("--gap", type=float, default=3.0)
    parser.add_argument("--2d-radius", dest="radius_2d", type=float, default=DEFAULT_2D_RADIUS)
    args = parser.parse_args()

    seeds = [s * 17 + 3 for s in range(args.n_seeds)]
    ns = list(args.n_layers)

    print("=" * 92)
    print("MATCHED 2D vs 4D DECOHERENCE EXPONENT COMPARISON")
    print("  Same modular family, same slit/mass rule, degree-matched 4D radius")
    print(f"  n_layers={ns}, seeds={args.n_seeds}, npl={args.npl}, gap={args.gap}")
    print(f"  2D radius fixed at {args.radius_2d}")
    print("=" * 92)
    print()

    series_2d: dict[int, dict[int, float]] = {}
    mean_deg_2d: dict[int, float] = {}
    mean_deg_4d: dict[int, float] = {}
    radius_4d: dict[int, float] = {}
    series_4d: dict[int, dict[int, float]] = {}

    for nl in ns:
        vals_2d: dict[int, float] = {}
        deg_2d: list[float] = []
        for seed in seeds:
            graph = _setup_2d(nl, seed, args.npl, args.radius_2d, args.gap)
            meas = _measure_graph(*graph, n_layers=nl)
            if meas is None:
                continue
            vals_2d[seed] = meas["pur_min"]
            deg_2d.append(meas["mean_degree"])
        if not vals_2d:
            continue
        series_2d[nl] = vals_2d
        mean_deg_2d[nl] = _mean(deg_2d)

        r4 = _match_4d_radius(mean_deg_2d[nl], nl, args.npl, args.gap, seeds)
        if r4 is None:
            continue
        radius_4d[nl] = r4

        vals_4d: dict[int, float] = {}
        deg_4d: list[float] = []
        for seed in seeds:
            graph4 = _setup_4d(nl, seed, args.npl, r4, args.gap)
            meas4 = _measure_graph(*graph4, n_layers=nl)
            if meas4 is None:
                continue
            vals_4d[seed] = meas4["pur_min"]
            deg_4d.append(meas4["mean_degree"])
        if vals_4d:
            series_4d[nl] = vals_4d
            mean_deg_4d[nl] = _mean(deg_4d)

    print(f"  {'N':>4s}  {'2D pur_min':>10s}  {'2D <k>':>7s}  {'4D pur_min':>10s}  {'4D <k>':>7s}  {'r4d':>6s}")
    print(f"  {'-' * 60}")
    for nl in ns:
        if nl not in series_2d or nl not in series_4d:
            print(f"  {nl:4d}  FAIL")
            continue
        print(
            f"  {nl:4d}  { _mean(list(series_2d[nl].values())):10.4f}  {mean_deg_2d[nl]:7.2f}  "
            f"{ _mean(list(series_4d[nl].values())):10.4f}  {mean_deg_4d[nl]:7.2f}  {radius_4d[nl]:6.2f}"
        )

    fit_2d = _fit_per_seed({n: series_2d[n] for n in ns if n in series_2d})
    fit_4d = _fit_per_seed({n: series_4d[n] for n in ns if n in series_4d})

    print()
    if fit_2d:
        _, alpha2, se2 = fit_2d
        print(f"  2D matched alpha: {alpha2:+.3f} ± {se2:.3f}")
    else:
        print("  2D matched alpha: FAIL")
    if fit_4d:
        _, alpha4, se4 = fit_4d
        print(f"  4D matched alpha: {alpha4:+.3f} ± {se4:.3f}")
    else:
        print("  4D matched alpha: FAIL")

    if fit_2d and fit_4d:
        delta = fit_4d[1] - fit_2d[1]
        print(f"  alpha delta (4D - 2D): {delta:+.3f}")
        if abs(delta) < 0.2:
            print("  Verdict: dimension alone is weak after degree matching")
        elif delta > 0:
            print("  Verdict: 4D still flattens the ceiling after degree matching")
        else:
            print("  Verdict: 4D does not flatten the ceiling after degree matching")

    # Bounded-table assertions tied to docs/MATCHED_2D_4D_DECOHERENCE_NOTE.md.
    # The note's claim is the bounded numerical replay of the table at the
    # default arguments (n_layers=[25,40,60,80,100], 8 seeds, npl=25,
    # gap=3.0, 2D radius=3.0). Skip the assertion check if the runner is
    # invoked with non-default arguments.
    default_ns = (25, 40, 60, 80, 100)
    is_default_run = (
        tuple(ns) == default_ns
        and args.n_seeds == 8
        and args.npl == 25
        and args.gap == 3.0
        and args.radius_2d == 3.0
    )
    if is_default_run and fit_2d and fit_4d:
        expected_pur = {
            #  N    2D pur     2D <k>   4D pur     4D <k>    r4
            25: (0.9341, 9.76, 0.9647, 9.52, 4.75),
            40: (0.9577, 9.98, 0.9559, 9.69, 4.75),
            60: (0.9555, 10.11, 0.9378, 9.78, 4.75),
            80: (0.9667, 10.24, 0.9812, 9.89, 4.75),
            100: (0.9428, 10.25, 0.9991, 9.89, 4.75),
        }
        for n in default_ns:
            assert n in series_2d and n in series_4d, (
                f"matched comparison missing rows for N={n}"
            )
            p2 = _mean(list(series_2d[n].values()))
            p4 = _mean(list(series_4d[n].values()))
            k2 = mean_deg_2d[n]
            k4 = mean_deg_4d[n]
            r4 = radius_4d[n]
            ep2, ek2, ep4, ek4, er4 = expected_pur[n]
            assert abs(p2 - ep2) <= 0.005, f"2D pur_min N={n} drift: {p2:.4f} vs {ep2}"
            assert abs(p4 - ep4) <= 0.005, f"4D pur_min N={n} drift: {p4:.4f} vs {ep4}"
            assert abs(k2 - ek2) <= 0.05, f"2D <k> N={n} drift: {k2:.2f} vs {ek2}"
            assert abs(k4 - ek4) <= 0.05, f"4D <k> N={n} drift: {k4:.2f} vs {ek4}"
            assert abs(r4 - er4) <= 0.01, f"r4 N={n} drift: {r4:.2f} vs {er4}"
        # Pinned alpha values from the note.
        assert abs(fit_2d[1] - (-0.158)) <= 0.05, (
            f"2D matched alpha drift: got {fit_2d[1]:+.3f}, expected -0.158"
        )
        assert abs(fit_4d[1] - (-2.704)) <= 0.05, (
            f"4D matched alpha drift: got {fit_4d[1]:+.3f}, expected -2.704"
        )
        delta_e = -2.546
        delta_got = fit_4d[1] - fit_2d[1]
        assert abs(delta_got - delta_e) <= 0.1, (
            f"alpha delta drift: got {delta_got:+.3f}, expected {delta_e}"
        )
        print(
            "PASS: bounded matched-2D-vs-4D table matches the note "
            "(pur_min, <k>, r4 within tolerance; alphas within +/-0.05; "
            "delta within +/-0.1)."
        )


if __name__ == "__main__":
    main()
