#!/usr/bin/env python3
"""Anisotropic-field pilot on the retained 3D modular family.

Goal
----
Test whether a bounded anisotropic/localized field surrogate can improve the
gravity distance/mass tradeoff on the retained 3D modular DAG family without
collapsing the retained mass-scaling signal.

This is intentionally narrow:
  - one retained 3D modular family (gap=5.0)
  - fixed mass count across the b sweep
  - fixed graph geometry per seed
  - same propagation and detector readout across all field modes
  - compare only a Laplacian baseline against a few anisotropic Gaussian
    surrogates

The point is not to rescue the distance law. The point is to ask whether a
directionally localized field can move the retained family toward a better
tradeoff than the pure Laplacian or the earlier causal scalar field.

Review discipline:
  - if anisotropy only weakens the signal, say that plainly
  - if it improves b-trend but kills mass scaling, say that plainly
  - if it sits between the retained endpoints, do not overclaim
"""

from __future__ import annotations

import cmath
import math
import os
import statistics
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.hybrid_field_fixed_mass_pilot import (  # noqa: E402
    GAP,
    K_BAND,
    MASS_COUNTS,
    MASS_LAYER_OFFSET,
    MASS_COUNT_FIXED,
    N_SEEDS,
    FIXED_MASS_B,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    CONNECT_RADIUS,
    generate_3d_modular_dag,
    select_fixed_mass_nodes,
)


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


def field_laplacian(positions, adj, mass_nodes, iterations: int = 50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)

    mass_set = set(mass_nodes)
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


def field_anisotropic(
    positions,
    adj,
    mass_nodes,
    axial_sigma: float = 4.5,
    transverse_sigma: float = 1.25,
    strength: float = 0.1,
):
    """Ellipsoidal Gaussian centered on the mass nodes.

    The x-direction is kept looser than the transverse directions so this is a
    bounded anisotropic localization surrogate rather than a hard cutoff.
    """
    field = [0.0] * len(positions)
    for m in mass_nodes:
        mx, my, mz = positions[m]
        for i, (x, y, z) in enumerate(positions):
            dx = (x - mx) / axial_sigma
            dy = (y - my) / transverse_sigma
            dz = (z - mz) / transverse_sigma
            field[i] += strength * math.exp(-0.5 * (dx * dx + dy * dy + dz * dz))
    return field


def propagate(positions, adj, field, src, k):
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            weight = math.exp(-0.8 * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            amps[j] += amps[i] * cmath.exp(1j * k * act) * weight / L
    return amps


def centroid_y(amps, positions, det_list):
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def _seed_delta(positions, adj, src, det_list, mass_nodes, field):
    free_field = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_mass = propagate(positions, adj, field, src, k)
        amps_free = propagate(positions, adj, free_field, src, k)
        deltas.append(centroid_y(amps_mass, positions, det_list) - centroid_y(amps_free, positions, det_list))
    return _mean(deltas) if deltas else None


def _fmt_alpha(fit) -> str:
    return "NA" if fit is None else f"{fit[0]:.3f}"


def measure_b_sweep(field_fn, label: str):
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 11 + 7,
            gap=GAP,
        )
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue
        center_y = statistics.fmean(p[1] for p in positions)
        mid_layer = layer_indices[len(layer_indices) // 2]
        for b in TARGET_BS:
            mass_nodes = select_fixed_mass_nodes(mid_layer, positions, center_y + b, MASS_COUNT_FIXED)
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            field = field_fn(positions, adj, mass_nodes)
            delta = _seed_delta(positions, adj, src, det_list, mass_nodes, field)
            if delta is not None:
                by_b[b].append(delta)

    rows = []
    for b in TARGET_BS:
        vals = by_b[b]
        if not vals:
            continue
        mean = _mean(vals)
        se = _se(vals)
        t = mean / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        rows.append((b, mean, se, t, mean * b, len(vals)))
    fit = _fit_power_law([r[0] for r in rows], [r[1] for r in rows])
    return label, rows, fit


def measure_mass_sweep(field_fn, label: str):
    by_mass: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 11 + 7,
            gap=GAP,
        )
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue
        center_y = statistics.fmean(p[1] for p in positions)
        mass_layer = layer_indices[MASS_LAYER_OFFSET]
        for mass_count in MASS_COUNTS:
            mass_nodes = select_fixed_mass_nodes(mass_layer, positions, center_y + FIXED_MASS_B, mass_count)
            if len(mass_nodes) != mass_count:
                continue
            field = field_fn(positions, adj, mass_nodes)
            delta = _seed_delta(positions, adj, src, det_list, mass_nodes, field)
            if delta is not None:
                by_mass[mass_count].append(delta)

    rows = []
    for mass_count in MASS_COUNTS:
        vals = by_mass[mass_count]
        if not vals:
            continue
        mean = _mean(vals)
        se = _se(vals)
        t = mean / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        rows.append((mass_count, mean, se, t, mean / mass_count, len(vals)))
    fit = _fit_power_law([r[0] for r in rows], [r[1] for r in rows])
    return label, rows, fit


def _print_b_summary(label: str, rows, fit):
    print(f"[{label}] b-sweep, fixed mass count = {MASS_COUNT_FIXED}")
    print(f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift*b':>8s}  {'samples':>7s}")
    print(f"  {'-' * 44}")
    for b, mean, se, t, scaled, n_ok in rows:
        print(f"  {b:3d}  {mean:+8.4f}  {se:6.4f}  {t:+6.2f}  {scaled:+8.3f}  {n_ok:7d}")
    if fit is not None:
        gamma, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * b^{gamma:.3f}  (R^2={r2:.3f})")
    else:
        print("  Fit: insufficient positive points for a stable power-law fit")
    print()


def _print_mass_summary(label: str, rows, fit):
    print(f"[{label}] mass-sweep, fixed b = {FIXED_MASS_B}")
    print(f"  {'M':>4s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/M':>8s}  {'samples':>7s}")
    print(f"  {'-' * 46}")
    for mass_count, mean, se, t, scaled, n_ok in rows:
        print(f"  {mass_count:4d}  {mean:+8.4f}  {se:6.4f}  {t:+6.2f}  {scaled:+8.3f}  {n_ok:7d}")
    if fit is not None:
        alpha, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * M^{alpha:.3f}  (R^2={r2:.3f})")
    else:
        print("  Fit: insufficient positive points for a stable power-law fit")
    print()


def main() -> None:
    print("=" * 78)
    print("ANISOTROPIC FIELD PILOT")
    print("  Retained 3D modular DAG family")
    print("  Test: bounded directional localization under fixed-mass controls")
    print("=" * 78)
    print()
    print("Setup:")
    print(f"  seeds per sweep: {N_SEEDS}")
    print(f"  k-band: {K_BAND}")
    print(f"  gap: {GAP}")
    print(f"  fixed b for mass sweep: {FIXED_MASS_B}")
    print(f"  fixed mass count for b sweep: {MASS_COUNT_FIXED}")
    print(f"  mass counts: {MASS_COUNTS}")
    print("  anisotropic field: ellipsoidal Gaussian with looser x axis")
    print()

    field_modes = [
        ("Laplacian relaxed (baseline)", field_laplacian),
        (
            "Anisotropic mild",
            lambda p, a, m: field_anisotropic(p, a, m, axial_sigma=4.5, transverse_sigma=1.75),
        ),
        (
            "Anisotropic strong",
            lambda p, a, m: field_anisotropic(p, a, m, axial_sigma=4.5, transverse_sigma=1.10),
        ),
    ]

    rows_out = []
    for label, fn in field_modes:
        b_label, b_rows, b_fit = measure_b_sweep(fn, label)
        _print_b_summary(b_label, b_rows, b_fit)
        _, m_rows, m_fit = measure_mass_sweep(fn, label)
        _print_mass_summary(label, m_rows, m_fit)
        rows_out.append((label, b_fit, m_fit, b_rows, m_rows))

    print("=" * 78)
    print("SUMMARY")
    for label, b_fit, m_fit, b_rows, m_rows in rows_out:
        gamma_txt = "NA" if b_fit is None else f"{b_fit[0]:.3f}"
        alpha_txt = "NA" if m_fit is None else f"{m_fit[0]:.3f}"
        b3_row = next((row for row in b_rows if row[0] == 3), None)
        b3_txt = "NA" if b3_row is None else f"{b3_row[1]:+.4f} (t={b3_row[3]:+.2f})"
        print(f"  {label}: b=3 shift {b3_txt} | gamma={gamma_txt} | alpha={alpha_txt}")

    print()
    print("INTERPRETATION")
    print("  This is a bounded anisotropic-localization check, not a new architecture.")
    print("  The question is whether directional localization improves the")
    print("  distance/mass tradeoff relative to the Laplacian baseline on the")
    print("  same retained 3D modular family.")
    print("  If the anisotropic mode only weakens the signal or mass scaling,")
    print("  then it is not a retained rescue of the distance law.")
    print("=" * 78)


if __name__ == "__main__":
    main()
