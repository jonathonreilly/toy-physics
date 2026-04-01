#!/usr/bin/env python3
"""Source-projected parameter map on retained 3D modular DAGs.

Goal
----
Check whether the source-projected improvement is stable across nearby
projection strengths or just a narrow parameter accident.

The map stays narrow:
  - fixed retained 3D modular family (gap=3.0)
  - fixed graph geometry per seed
  - fixed mass count across the b sweep
  - fixed b across the mass sweep
  - compare Laplacian baseline, source-resolved Green, and a small
    family of source-projected strengths

Review discipline:
  - do not overclaim a rescue from one lucky strength
  - if stronger projection improves distance but worsens mass scaling,
    say so plainly
  - if the trend is stable across a band of strengths, say so plainly

PStack experiment: source-projected-parameter-map
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict, deque
from functools import partial

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.source_projected_field_pilot import (  # type: ignore  # noqa: E402
    CONNECT_RADIUS,
    GAP,
    K_BAND,
    MASS_COUNTS,
    MASS_COUNT_FIXED,
    N_SEEDS,
    FIXED_MASS_B,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    centroid_y,
    field_laplacian,
    field_source_projected,
    generate_3d_modular_dag,
    propagate,
)
from scripts.source_resolved_green_pilot import (  # type: ignore  # noqa: E402
    GREEN_EPS,
    GREEN_STRENGTH,
    _select_fixed_mass_nodes,
    field_source_resolved_green,
)

PROJECTION_STRENGTHS = (0.02, 0.04, 0.08, 0.12, 0.16, 0.24)


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


def _select_mass_nodes(
    layer_nodes: list[int],
    positions: list[tuple[float, float, float]],
    target_y: float,
    count: int,
) -> list[int]:
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def _seed_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    field_fn,
) -> float | None:
    field_with = field_fn(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_with = propagate(positions, adj, field_with, src, k)
        amps_without = propagate(positions, adj, field_without, src, k)
        deltas.append(
            centroid_y(amps_with, positions, det_list)
            - centroid_y(amps_without, positions, det_list)
        )
    return _mean(deltas) if deltas else None


def _measure_config(label: str, field_fn) -> dict[str, float | list[tuple[int, float, float, float]]]:
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    by_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
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
            mass_nodes = _select_mass_nodes(
                layer_nodes, positions, center_y + b, MASS_COUNT_FIXED
            )
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            delta = _seed_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_b[b].append(delta)

        fixed_mass_nodes = _select_mass_nodes(
            layer_nodes, positions, center_y + FIXED_MASS_B, max(MASS_COUNTS)
        )
        if fixed_mass_nodes:
            for m in MASS_COUNTS:
                subset = fixed_mass_nodes[:m]
                if len(subset) != m:
                    continue
                delta = _seed_delta(positions, adj, src, det_list, subset, field_fn)
                if delta is not None:
                    by_m[m].append(delta)

    b_vals = []
    b_pos = []
    for b in TARGET_BS:
        vals = by_b[b]
        if not vals:
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        if shift > 0:
            b_vals.append((b, shift, se, t))
            b_pos.append(b)

    m_vals = []
    m_pos = []
    for m in MASS_COUNTS:
        vals = by_m[m]
        if not vals:
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        if shift > 0:
            m_vals.append((m, shift, se, t))
            m_pos.append(m)

    b_fit = _fit_power_law(b_pos, [_mean(by_b[b]) for b in b_pos])
    m_fit = _fit_power_law(m_pos, [_mean(by_m[m]) for m in m_pos])

    return {
        "label": label,
        "b_fit": b_fit[0] if b_fit else math.nan,
        "m_fit": m_fit[0] if m_fit else math.nan,
        "b_r2": b_fit[2] if b_fit else math.nan,
        "m_r2": m_fit[2] if m_fit else math.nan,
        "b_rows": b_vals,
        "m_rows": m_vals,
    }


def main() -> None:
    print("=" * 78)
    print("SOURCE-PROJECTED PARAMETER MAP")
    print("  Retained 3D modular DAG family")
    print("  Question: is the source-projected improvement stable nearby?")
    print("=" * 78)
    print()
    print(f"  seeds/config: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  k-band: {K_BAND}")
    print(f"  fixed mass count for b sweep: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass sweep: {FIXED_MASS_B}")
    print(f"  projection strengths: {PROJECTION_STRENGTHS}")
    print()

    baseline = _measure_config("Laplacian baseline", field_laplacian)
    green = _measure_config(
        "Source-resolved Green",
        lambda p, a, m: field_source_resolved_green(
            p, a, m, strength=GREEN_STRENGTH, eps=GREEN_EPS
        ),
    )

    rows = [baseline, green]
    for s in PROJECTION_STRENGTHS:
        rows.append(
            _measure_config(
                f"Source-projected strength={s:.2f}",
                lambda p, a, m, strength=s: field_source_projected(
                    p, a, m, strength=strength, eps=GREEN_EPS
                ),
            )
        )

    print("CONFIG SWEEP")
    print(
        f"  {'label':>28s}  {'b alpha':>7s}  {'b R2':>5s}  {'M alpha':>7s}  {'M R2':>5s}  "
        f"{'b@3':>6s}  {'M@3':>6s}"
    )
    print(f"  {'-' * 90}")
    for row in rows:
        b_at_3 = next((shift for b, shift, _se, _t in row["b_rows"] if b == 3), math.nan)
        m_at_3 = next((shift for m, shift, _se, _t in row["m_rows"] if m == 3), math.nan)
        print(
            f"  {row['label']:>28s}  "
            f"{row['b_fit']:7.3f}  {row['b_r2']:5.3f}  {row['m_fit']:7.3f}  {row['m_r2']:5.3f}  "
            f"{b_at_3:6.3f}  {m_at_3:6.3f}"
        )

    print()
    print("VERDICT")
    candidates = [
        row for row in rows[2:]
        if math.isfinite(row["b_fit"]) and math.isfinite(row["m_fit"]) and row["m_fit"] > 0
    ]
    if not candidates:
        print("  No positive source-projected candidate survived with a stable mass trend.")
    else:
        best = min(candidates, key=lambda r: (r["b_fit"], -r["m_fit"]))
        print(
            f"  Best projected strength = {best['label']}; b alpha={best['b_fit']:.3f}, "
            f"M alpha={best['m_fit']:.3f}."
        )
        if best["b_fit"] < 0 and best["m_fit"] > 1.0:
            print(
                "  The source-projected lane is robustly the best distance trend so far, "
                "but it still strengthens mass scaling rather than relaxing it."
            )
        else:
            print(
                "  The projected lane is still a parameter-sensitive partial move, not a clean rescue."
            )
    print("=" * 78)


if __name__ == "__main__":
    main()
