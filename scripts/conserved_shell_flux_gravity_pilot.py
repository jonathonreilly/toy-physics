#!/usr/bin/env python3
"""Conserved shell-flux gravity pilot on retained 3D modular DAGs.

This tests a different gravity architecture idea:

1. Build graph-distance shells outward from each mass node on the undirected
   shadow graph.
2. Inject a fixed amount of source per shell so the per-node influence dilutes
   as shell occupancy grows.
3. Compare that shell-flux field against the retained Laplacian baseline and a
   source-projected shell-flux variant under the same strict fit discipline.

The goal is narrow and review-safe:
  - not "solve gravity"
  - ask whether a conserved shell-area dilution mechanism gives a more stable
    distance trend than the fragile interference-only seams

PStack experiment: conserved-shell-flux-gravity-pilot
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.source_resolved_green_pilot import (  # type: ignore  # noqa: E402
    CONNECT_RADIUS,
    FIXED_MASS_B,
    GAP,
    GREEN_EPS,
    K_BAND,
    MASS_COUNT_FIXED,
    MASS_COUNTS,
    MASS_LAYER_OFFSET,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    centroid_y,
    field_laplacian,
    generate_3d_modular_dag,
    propagate,
)


N_SEEDS = 32
FLUX_STRENGTH = 0.20


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


def _fit_full_positive_power_law(xs_in: list[float], ys_in: list[float]) -> tuple[float, float, float] | None:
    if len(xs_in) < 3 or any(y <= 0 for y in ys_in):
        return None
    return _fit_power_law(xs_in, ys_in)


def _select_fixed_mass_nodes(
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


def _undirected_adj(adj: dict[int, list[int]]) -> dict[int, set[int]]:
    undirected: dict[int, set[int]] = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    return undirected


def _shell_sizes(undirected: dict[int, set[int]], source: int, n: int) -> dict[int, int]:
    dist = [-1] * n
    dist[source] = 0
    q: deque[int] = deque([source])
    while q:
        i = q.popleft()
        for j in undirected.get(i, ()):
            if dist[j] >= 0:
                continue
            dist[j] = dist[i] + 1
            q.append(j)
    counts: dict[int, int] = defaultdict(int)
    for d in dist:
        if d >= 0:
            counts[d] += 1
    return counts


def field_conserved_shell_flux(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    strength: float = FLUX_STRENGTH,
    eps: float = GREEN_EPS,
) -> list[float]:
    """Assign per-node field by shell-occupancy dilution on the graph shadow."""
    n = len(positions)
    undirected = _undirected_adj(adj)
    field = [0.0] * n
    for m in mass_nodes:
        shell_counts = _shell_sizes(undirected, m, n)
        if not shell_counts:
            continue
        dist = [-1] * n
        dist[m] = 0
        q: deque[int] = deque([m])
        while q:
            i = q.popleft()
            for j in undirected.get(i, ()):
                if dist[j] >= 0:
                    continue
                dist[j] = dist[i] + 1
                q.append(j)
        for i, d in enumerate(dist):
            if d < 0:
                continue
            shell_size = shell_counts.get(d, 0)
            if shell_size <= 0:
                continue
            field[i] += strength / (shell_size + eps)
    return field


def field_source_projected_shell_flux(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    strength: float = FLUX_STRENGTH,
    eps: float = GREEN_EPS,
) -> list[float]:
    """Conserved shell flux with a source-direction projection factor."""
    n = len(positions)
    undirected = _undirected_adj(adj)
    field = [0.0] * n
    sx, sy, sz = positions[0]
    for m in mass_nodes:
        mx, my, mz = positions[m]
        u_x = mx - sx
        u_y = my - sy
        u_z = mz - sz
        u_norm = math.sqrt(u_x * u_x + u_y * u_y + u_z * u_z)
        if u_norm < 1e-12:
            continue
        shell_counts = _shell_sizes(undirected, m, n)
        dist = [-1] * n
        dist[m] = 0
        q: deque[int] = deque([m])
        while q:
            i = q.popleft()
            for j in undirected.get(i, ()):
                if dist[j] >= 0:
                    continue
                dist[j] = dist[i] + 1
                q.append(j)
        for i, d in enumerate(dist):
            if d < 0:
                continue
            shell_size = shell_counts.get(d, 0)
            if shell_size <= 0:
                continue
            x, y, z = positions[i]
            v_x = x - sx
            v_y = y - sy
            v_z = z - sz
            v_norm = math.sqrt(v_x * v_x + v_y * v_y + v_z * v_z)
            if v_norm < 1e-12:
                continue
            align = (u_x * v_x + u_y * v_y + u_z * v_z) / (u_norm * v_norm)
            if align <= 0:
                continue
            field[i] += strength * align / (shell_size + eps)
    return field


def _paired_seed_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    field_fn,
    k_band: tuple[float, ...] = K_BAND,
) -> float | None:
    field_with = field_fn(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)
    deltas = []
    for k in k_band:
        amps_with = propagate(positions, adj, field_with, src, k)
        amps_without = propagate(positions, adj, field_without, src, k)
        deltas.append(
            centroid_y(amps_with, positions, det_list)
            - centroid_y(amps_without, positions, det_list)
        )
    return _mean(deltas) if deltas else None


def _measure_b_sweep(field_fn) -> tuple[float | None, float | None]:
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
            gap=GAP,
        )
        if len(layer_indices) < 7:
            continue
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue
        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        layer_nodes = layer_indices[MASS_LAYER_OFFSET]
        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + b, MASS_COUNT_FIXED)
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            delta = _paired_seed_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_b[b].append(delta)

    fit_bs: list[float] = []
    fit_shifts: list[float] = []
    saw_nonpositive = False
    print(f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/b':>8s}  {'samples':>7s}")
    print(f"  {'-' * 44}")
    for b in TARGET_BS:
        vals = by_b[b]
        if not vals:
            print(f"{b:3d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"{b:3d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift / b:+8.3f}  {len(vals):7d}")
        fit_bs.append(b)
        fit_shifts.append(shift)
        if shift <= 0:
            saw_nonpositive = True

    fit = _fit_full_positive_power_law(fit_bs, fit_shifts)
    if fit is None:
        if saw_nonpositive:
            print("  Fit: not reported because the full sweep includes non-positive mean shifts")
        else:
            print("  Fit: insufficient positive points for a stable power-law fit")
        return None, None
    alpha, c, r2 = fit
    print(f"  Fit: shift ~= {c:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")
    return alpha, r2


def _measure_mass_sweep(field_fn) -> tuple[float | None, float | None]:
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
        if len(layer_indices) < 7:
            continue
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue
        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        layer_nodes = layer_indices[MASS_LAYER_OFFSET]
        ranked = _select_fixed_mass_nodes(layer_nodes, positions, center_y + FIXED_MASS_B, max(MASS_COUNTS))
        if len(ranked) < max(MASS_COUNTS):
            continue
        for m in MASS_COUNTS:
            mass_nodes = ranked[:m]
            delta = _paired_seed_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_m[m].append(delta)

    fit_ms: list[float] = []
    fit_shifts: list[float] = []
    saw_nonpositive = False
    print(f"  {'M':>4s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/M':>8s}  {'samples':>7s}")
    print(f"  {'-' * 46}")
    for m in MASS_COUNTS:
        vals = by_m[m]
        if not vals:
            print(f"{m:4d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"{m:4d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift / m:+8.3f}  {len(vals):7d}")
        fit_ms.append(float(m))
        fit_shifts.append(shift)
        if shift <= 0:
            saw_nonpositive = True

    fit = _fit_full_positive_power_law(fit_ms, fit_shifts)
    if fit is None:
        if saw_nonpositive:
            print("  Fit: not reported because the full sweep includes non-positive mean shifts")
        else:
            print("  Fit: insufficient positive points for a stable power-law fit")
        return None, None
    alpha, c, r2 = fit
    print(f"  Fit: shift ~= {c:.4f} * M^{alpha:.3f}  (R^2={r2:.3f})")
    return alpha, r2


def _measure_k0_control(field_fn) -> float:
    deltas: list[float] = []
    for seed in range(8):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
            gap=GAP,
        )
        if len(layer_indices) < 7:
            continue
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        layer_nodes = layer_indices[MASS_LAYER_OFFSET]
        mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + FIXED_MASS_B, MASS_COUNT_FIXED)
        if len(mass_nodes) != MASS_COUNT_FIXED:
            continue
        delta = _paired_seed_delta(positions, adj, src, det_list, mass_nodes, field_fn, k_band=(0.0,))
        if delta is not None:
            deltas.append(abs(delta))
    return _mean(deltas) if deltas else math.nan


def _print_field_summary(label: str, field_fn) -> tuple[float | None, float | None, float | None, float | None, float]:
    print("=" * 84)
    print(label)
    print("=" * 84)
    print(f"  seeds: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  k-band: {K_BAND}")
    print(f"  flux strength: {FLUX_STRENGTH}")
    print()
    print("[k=0 sanity]")
    k0 = _measure_k0_control(field_fn)
    print(f"  mean |delta| at k=0: {k0:.6g}")
    print()
    print("[b sweep]")
    b_alpha, b_r2 = _measure_b_sweep(field_fn)
    print()
    print("[mass sweep]")
    m_alpha, m_r2 = _measure_mass_sweep(field_fn)
    print()
    return b_alpha, b_r2, m_alpha, m_r2, k0


def main() -> None:
    print("=" * 84)
    print("CONSERVED SHELL-FLUX GRAVITY PILOT")
    print("  retained 3D modular family: gap=3.0")
    print("  same strict harness as source-aware reaudits")
    print("=" * 84)
    print()

    by_mode: dict[str, tuple[float | None, float | None, float | None, float | None, float]] = {}
    by_mode["Laplacian baseline"] = _print_field_summary(
        "LAPLACIAN BASELINE",
        lambda positions, adj, mass_nodes: field_laplacian(positions, adj, mass_nodes),
    )
    by_mode["Conserved shell flux"] = _print_field_summary(
        "CONSERVED SHELL FLUX",
        lambda positions, adj, mass_nodes: field_conserved_shell_flux(positions, adj, mass_nodes),
    )
    by_mode["Projected shell flux"] = _print_field_summary(
        "PROJECTED SHELL FLUX",
        lambda positions, adj, mass_nodes: field_source_projected_shell_flux(positions, adj, mass_nodes),
    )

    print("=" * 84)
    print("COMPARISON")
    for label, (b_alpha, b_r2, m_alpha, m_r2, k0) in by_mode.items():
        b_s = "NA" if b_alpha is None else f"{b_alpha:.3f}"
        m_s = "NA" if m_alpha is None else f"{m_alpha:.3f}"
        br2_s = "NA" if b_r2 is None else f"{b_r2:.3f}"
        mr2_s = "NA" if m_r2 is None else f"{m_r2:.3f}"
        print(
            f"  {label:>22s}: b alpha = {b_s} (R^2={br2_s}) | "
            f"M alpha = {m_s} (R^2={mr2_s}) | k0 mean |delta| = {k0:.3g}"
        )
    print()
    print("REVIEW-SAFE INTERPRETATION")
    print("  Promote only if the full-sweep-positive fit survives and the k=0 control stays near zero.")
    print("  If shell flux improves b without a mass fit, call it a distance-side partial mover only.")
    print("=" * 84)


if __name__ == "__main__":
    main()
