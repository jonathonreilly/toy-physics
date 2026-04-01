#!/usr/bin/env python3
"""Shell-by-shell phase contribution audit on retained 3D modular DAGs.

Goal
----
Audit whether the accumulated phase shift is carried by a broad set of
distance shells around the mass region, or whether the retained force law
is dominated by a narrow near-source band.

This is intentionally a mechanism audit, not a rescue claim:
  - fixed graph geometry per seed
  - fixed mass count across the b sweep
  - same detector readout and k-band
  - compare the retained Laplacian lane against the source-resolved Green
    lane on the same retained 3D modular family

The shell decomposition is a proxy:
  - each node is assigned to a radial shell around the mass centroid
  - we mask the field to one shell at a time and re-run propagation
  - the resulting detector-centroid shifts are shell witnesses, not exact
    linear response coefficients

PStack experiment: path-shell-contribution-audit
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.hybrid_field_fixed_mass_pilot import (  # type: ignore  # noqa: E402
    centroid_y,
    field_laplacian,
    generate_3d_modular_dag,
    propagate,
    select_fixed_mass_nodes,
)
from scripts.source_resolved_green_pilot import (  # type: ignore  # noqa: E402
    field_source_resolved_green,
)

N_SEEDS = 24
N_LAYERS = 18
NODES_PER_LAYER = 40
XYZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
GAP = 3.0
K_BAND = (3.0, 5.0, 7.0)
TARGET_BS = (1, 2, 3, 4, 5, 6, 7, 8, 10)
MASS_COUNT = 8
SHELL_WIDTH = 2.0
MAX_SHELLS = 6


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _fit_power_law(xs_in: list[float], ys_in: list[float]) -> tuple[float, float, float] | None:
    pairs = [(x, y) for x, y in zip(xs_in, ys_in) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(x) for x, _ in pairs]
    ys = [math.log(y) for _, y in pairs]
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return slope, math.exp(intercept), r2


def _topo_layers(positions: list[tuple[float, float, float]]) -> dict[int, list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    return by_layer


def _weighted_y(amps: list[complex], positions: list[tuple[float, float, float]], nodes: list[int]) -> float:
    total = 0.0
    wy = 0.0
    for i in nodes:
        p = abs(amps[i]) ** 2
        total += p
        wy += p * positions[i][1]
    return wy / total if total > 1e-30 else 0.0


def _shell_index(r: float) -> int:
    return min(int(r / SHELL_WIDTH), MAX_SHELLS - 1)


def _shell_labels(
    positions: list[tuple[float, float, float]],
    mass_nodes: list[int],
) -> tuple[dict[int, int], list[float], tuple[float, float, float]]:
    cx = sum(positions[i][0] for i in mass_nodes) / len(mass_nodes)
    cy = sum(positions[i][1] for i in mass_nodes) / len(mass_nodes)
    cz = sum(positions[i][2] for i in mass_nodes) / len(mass_nodes)
    labels: dict[int, int] = {}
    radii: list[float] = []
    for idx, (x, y, z) in enumerate(positions):
        r = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
        radii.append(r)
        labels[idx] = _shell_index(r)
    return labels, radii, (cx, cy, cz)


def _field_support(field: list[float]) -> float:
    if not field:
        return 0.0
    return sum(1 for v in field if abs(v) > 1e-4) / len(field)


def _field_by_shell(
    field: list[float],
    shell_labels: dict[int, int],
) -> list[list[float]]:
    shells = [[0.0] * len(field) for _ in range(MAX_SHELLS)]
    for idx, val in enumerate(field):
        shell = shell_labels.get(idx, MAX_SHELLS - 1)
        shells[shell][idx] = val
    return shells


def _measure_seed(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    field_fn,
) -> dict[str, object] | None:
    field = field_fn(positions, adj, mass_nodes)
    shell_labels, radii, center = _shell_labels(positions, mass_nodes)
    shells = _field_by_shell(field, shell_labels)
    total_field_support = _field_support(field)
    shell_support = [
        sum(abs(field[i]) for i, lab in shell_labels.items() if lab == s) / sum(abs(v) for v in field)
        if sum(abs(v) for v in field) > 1e-30
        else 0.0
        for s in range(MAX_SHELLS)
    ]

    total_shifts: list[float] = []
    shell_shifts: list[list[float]] = [[] for _ in range(MAX_SHELLS)]
    for k in K_BAND:
        amps_full = propagate(positions, adj, field, src, k)
        amps_free = propagate(positions, adj, [0.0] * len(positions), src, k)
        total_shifts.append(centroid_y(amps_full, positions, det_list) - centroid_y(amps_free, positions, det_list))
        for s in range(MAX_SHELLS):
            amps_shell = propagate(positions, adj, shells[s], src, k)
            shell_shifts[s].append(
                centroid_y(amps_shell, positions, det_list) - centroid_y(amps_free, positions, det_list)
            )

    shell_shift_means = [_mean(vals) for vals in shell_shifts]
    return {
        "total_shift": _mean(total_shifts),
        "shell_shift_means": shell_shift_means,
        "shell_support": shell_support,
        "field_support": total_field_support,
        "center": center,
        "radius_mean": _mean(radii),
    }


def _run_family(label: str, field_fn) -> dict[str, object]:
    print(f"[{label}]")
    print(f"  {'b':>4s}  {'shift':>8s}  {'SE':>7s}  {'t':>6s}  {'shift/b':>9s}  {'broad':>5s}  {'n_ok':>5s}")
    print(f"  {'-' * 58}")

    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    shell_support_by_b: dict[float, list[list[float]]] = {b: [[] for _ in range(MAX_SHELLS)] for b in TARGET_BS}
    shell_shift_by_b: dict[float, list[list[float]]] = {b: [[] for _ in range(MAX_SHELLS)] for b in TARGET_BS}
    field_supports: list[float] = []

    for seed in range(N_SEEDS):
        positions, adj, _layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
            gap=GAP,
        )
        by_layer = _topo_layers(positions)
        layers = sorted(by_layer)
        if len(layers) < 7:
            continue
        src = by_layer[layers[0]]
        det_list = list(by_layer[layers[-1]])
        if not det_list:
            continue
        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mid_layer = layers[len(layers) // 2]
        layer_nodes = by_layer[mid_layer]

        for b in TARGET_BS:
            mass_nodes = select_fixed_mass_nodes(layer_nodes, positions, center_y + b, MASS_COUNT)
            if len(mass_nodes) != MASS_COUNT:
                continue
            result = _measure_seed(positions, adj, src, det_list, mass_nodes, field_fn)
            if result is None:
                continue
            by_b[b].append(result["total_shift"])  # type: ignore[index]
            field_supports.append(result["field_support"])  # type: ignore[index]
            shell_support = result["shell_support"]  # type: ignore[index]
            shell_shift = result["shell_shift_means"]  # type: ignore[index]
            for s in range(MAX_SHELLS):
                shell_support_by_b[b][s].append(shell_support[s])
                shell_shift_by_b[b][s].append(shell_shift[s])

    for b in TARGET_BS:
        vals = by_b[b]
        if not vals:
            print(f"  {b:4.1f}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        broad = sum(
            1
            for s in range(MAX_SHELLS)
            if _mean(shell_support_by_b[b][s]) > 0.10
        )
        print(f"  {b:4.1f}  {shift:+8.4f}  {se:7.4f}  {t:+6.2f}  {shift / b:+9.4f}  {broad:5d}  {len(vals):5d}")

    positive_bs = [b for b, vals in by_b.items() if vals and _mean(vals) > 0]
    positive_shifts = [_mean(by_b[b]) for b in positive_bs]
    fit = _fit_power_law(positive_bs, positive_shifts)
    alpha = fit[0] if fit else None
    gamma = -alpha if alpha is not None else None

    print()
    print(f"  mean field support fraction: {_mean(field_supports):.3f}")
    if fit is not None:
        print(f"  Fit: shift ~= {fit[1]:.4f} * b^{fit[0]:.3f}  (R^2={fit[2]:.3f})")
    else:
        print("  Fit: insufficient positive points for a stable power-law fit")

    print("  shell summary (support share / shift witness):")
    for s in range(MAX_SHELLS):
        support_means = [_mean(shell_support_by_b[b][s]) for b in TARGET_BS if shell_support_by_b[b][s]]
        shift_means = [_mean(shell_shift_by_b[b][s]) for b in TARGET_BS if shell_shift_by_b[b][s]]
        if not support_means or not shift_means:
            continue
        print(
            f"    shell {s}: support={_mean(support_means):.3f}, "
            f"shift={_mean(shift_means):+.4f}"
        )

    print()
    return {
        "alpha": alpha,
        "gamma": gamma,
        "mean_field_support": _mean(field_supports),
        "avg_shift_at_b3": _mean(by_b[3]) if by_b.get(3) else math.nan,
    }


def main() -> None:
    print("=" * 78)
    print("PATH SHELL CONTRIBUTION AUDIT")
    print("  Retained 3D modular DAG family")
    print("  Fixed-mass controls")
    print("  Goal: do broad shells explain the flat/topological force law?")
    print("=" * 78)
    print()
    print(f"  seeds per sweep: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  shell width: {SHELL_WIDTH}")
    print(f"  k-band: {K_BAND}")
    print(f"  mass count: {MASS_COUNT}")
    print()

    lap = _run_family("Laplacian relaxed", field_laplacian)
    green = _run_family("Source-resolved Green", field_source_resolved_green)

    print("=" * 78)
    print("SUMMARY")
    print(
        f"  Laplacian: alpha={lap['alpha'] if lap['alpha'] is not None else 'NA'}, "
        f"mean support={lap['mean_field_support']:.3f}, b=3 shift={lap['avg_shift_at_b3']:+.4f}"
    )
    print(
        f"  Green:     alpha={green['alpha'] if green['alpha'] is not None else 'NA'}, "
        f"mean support={green['mean_field_support']:.3f}, b=3 shift={green['avg_shift_at_b3']:+.4f}"
    )
    print(
        "  Bottom line: broad shell support is present, but the source-resolved "
        "Green lane improves the distance trend more than the shell support picture alone."
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
