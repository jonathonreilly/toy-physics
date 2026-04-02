#!/usr/bin/env python3
"""Local continuation backreaction confirmation for the d=0.50 pocket.

This is a narrow rerun of the retained modular backreaction pocket at
depth_weight=0.50 with a larger seed count than the original stability map.

Controls:
  - retained 3D modular DAG family only
  - same graph geometry per seed
  - k=0 -> 0 hard control
  - depth_weight fixed to 0.50
  - same k-band and mass readout as the earlier backreaction map

The point is to check whether the d=0.50 pocket stays near
  b alpha ~= -0.43
  M alpha ~= +0.53
under more seeds than the stability map.
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

from scripts.hybrid_field_fixed_mass_pilot import (  # type: ignore  # noqa: E402
    BETA,
    CONNECT_RADIUS,
    FIXED_MASS_B,
    GAP,
    K_BAND,
    MASS_COUNTS,
    MASS_COUNT_FIXED,
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
DEPTH_WEIGHT = 0.50
EPS = 0.50
STRENGTHS = (0.04, 0.08, 0.12, 0.20)
CONTINUATION_ALIGN_FLOOR = 0.15
GAP = 3.0


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
    sx, sy = sum(xs), sum(ys)
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


def _fit_full_positive_means(
    xs_in: list[float],
    means_by_x: dict[float | int, list[float]],
) -> tuple[float, float, float] | None:
    xs_fit: list[float] = []
    ys_fit: list[float] = []
    for x in xs_in:
        vals = means_by_x[x]
        if not vals:
            return None
        mean = _mean(vals)
        if not math.isfinite(mean) or mean <= 0.0:
            return None
        xs_fit.append(float(x))
        ys_fit.append(mean)
    return _fit_power_law(xs_fit, ys_fit)


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


def _normalize_edge_field(edge_field: dict[tuple[int, int], float]) -> dict[tuple[int, int], float]:
    if not edge_field:
        return {}
    max_abs = max(abs(v) for v in edge_field.values())
    if max_abs <= 1e-30:
        return {k: 0.0 for k in edge_field}
    return {k: v / max_abs for k, v in edge_field.items()}


def field_source_projected(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    strength: float = 0.08,
    eps: float = 0.5,
) -> list[float]:
    """Source-direction-aware projected field used as a control reference."""
    n = len(positions)
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
        for i, (x, y, z) in enumerate(positions):
            v_x = x - sx
            v_y = y - sy
            v_z = z - sz
            v_norm = math.sqrt(v_x * v_x + v_y * v_y + v_z * v_z)
            if v_norm < 1e-12:
                continue
            align = (u_x * v_x + u_y * v_y + u_z * v_z) / (u_norm * v_norm)
            if align <= 0:
                continue
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2)
            field[i] += strength * align / (r + eps)
    return field


def make_backreaction_edge_field(
    strength: float,
    eps: float,
    depth_weight: float,
):
    """Create a shape-normalized continuation field with explicit scale."""

    def edge_field_fn(
        positions: list[tuple[float, float, float]],
        adj: dict[int, list[int]],
        mass_nodes: list[int],
    ) -> dict[tuple[int, int], float]:
        sx, sy, sz = positions[0]
        edge_field: dict[tuple[int, int], float] = {}
        sigs: dict[int, tuple[float, tuple[float, float, float], float]] = {}

        for j in range(len(positions)):
            outs = adj.get(j, [])
            if not outs:
                sigs[j] = (1.0, (0.0, 0.0, 0.0), 0.0)
                continue
            x0, y0, z0 = positions[j]
            vectors: list[tuple[float, float, float]] = []
            two_hop = 0.0
            for ch in outs:
                two_hop += len(adj.get(ch, []))
                dx = positions[ch][0] - x0
                dy = positions[ch][1] - y0
                dz = positions[ch][2] - z0
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L > 1e-12:
                    vectors.append((dx / L, dy / L, dz / L))
            if vectors:
                mx_ = sum(v[0] for v in vectors) / len(vectors)
                my_ = sum(v[1] for v in vectors) / len(vectors)
                mz_ = sum(v[2] for v in vectors) / len(vectors)
                coherence = math.sqrt(mx_ * mx_ + my_ * my_ + mz_ * mz_)
                mean_dir = (
                    (mx_ / coherence, my_ / coherence, mz_ / coherence)
                    if coherence > 1e-12
                    else (0.0, 0.0, 0.0)
                )
            else:
                coherence = 0.0
                mean_dir = (0.0, 0.0, 0.0)
            capacity = 1.0 + len(outs) + depth_weight * two_hop
            sigs[j] = (capacity, mean_dir, coherence)

        for i, outs in adj.items():
            x1, y1, z1 = positions[i]
            for j in outs:
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-12:
                    continue
                ex, ey, ez = dx / L, dy / L, dz / L
                mid_x, mid_y, mid_z = 0.5 * (x1 + x2), 0.5 * (y1 + y2), 0.5 * (z1 + z2)
                cap, cont_dir, coherence = sigs[j]
                if cap <= 1e-12 or coherence <= 1e-12:
                    continue
                continuity_align = max(0.0, ex * cont_dir[0] + ey * cont_dir[1] + ez * cont_dir[2])
                if continuity_align <= 0.0:
                    continue
                v_x, v_y, v_z = mid_x - sx, mid_y - sy, mid_z - sz
                v_norm = math.sqrt(v_x * v_x + v_y * v_y + v_z * v_z)
                if v_norm < 1e-12:
                    continue

                response = 0.0
                for m in mass_nodes:
                    mx, my, mz = positions[m]
                    u_x, u_y, u_z = mx - sx, my - sy, mz - sz
                    u_norm = math.sqrt(u_x * u_x + u_y * u_y + u_z * u_z)
                    if u_norm < 1e-12:
                        continue
                    source_align = (u_x * v_x + u_y * v_y + u_z * v_z) / (u_norm * v_norm)
                    if source_align <= 0:
                        continue
                    r = math.sqrt((mid_x - mx) ** 2 + (mid_y - my) ** 2 + (mid_z - mz) ** 2)
                    if r < 1e-12:
                        continue
                    response += (
                        source_align
                        * continuity_align
                        * max(coherence, CONTINUATION_ALIGN_FLOOR)
                        / (cap * (r + eps))
                    )
                edge_field[(i, j)] = response
        normalized = _normalize_edge_field(edge_field)
        return {edge: strength * value for edge, value in normalized.items()}

    return edge_field_fn


def propagate_edge_field(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    node_field: list[float],
    src: list[int],
    k: float,
    edge_field: dict[tuple[int, int], float],
) -> list[complex]:
    """Propagate amplitudes using a node field plus an edge-response phase."""
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
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            weight = math.exp(-BETA * theta * theta)
            lf = 0.5 * (node_field[i] + node_field[j]) + edge_field.get((i, j), 0.0)
            # The continuation response perturbs phase only, so k=0 remains null.
            act = L * (1.0 + lf)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * weight / L
    return amps


def propagate_node_field(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    node_field: list[float],
    src: list[int],
    k: float,
) -> list[complex]:
    """Propagate using the node field alone."""
    return propagate_edge_field(positions, adj, node_field, src, k, {})


def propagate_node_and_edge_field(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    node_field: list[float],
    src: list[int],
    k: float,
    edge_field: dict[tuple[int, int], float],
) -> list[complex]:
    """Propagate using a node field plus an edge-response phase."""
    return propagate_edge_field(positions, adj, node_field, src, k, edge_field)


def _paired_seed_delta_edge(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    base_field: list[float],
    mass_nodes: list[int],
    edge_field_fn,
) -> float | None:
    edge_field = edge_field_fn(positions, adj, mass_nodes)
    zero_field = {}
    deltas: list[float] = []
    for k in K_BAND:
        amps_with = propagate_edge_field(positions, adj, base_field, src, k, edge_field)
        amps_free = propagate_edge_field(positions, adj, [0.0] * len(positions), src, k, zero_field)
        deltas.append(centroid_y(amps_with, positions, det_list) - centroid_y(amps_free, positions, det_list))
    return _mean(deltas) if deltas else None


def _measure_backreaction(
    strength: float,
    *,
    depth_weight: float = DEPTH_WEIGHT,
    n_seeds: int = N_SEEDS,
) -> tuple[float | None, float | None, dict[str, list[float]]]:
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    by_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    edge_fn = make_backreaction_edge_field(strength, EPS, depth_weight)

    for seed in range(n_seeds):
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

        center_y = statistics.fmean(p[1] for p in positions)
        mass_layer = layer_indices[MASS_LAYER_OFFSET]

        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(mass_layer, positions, center_y + b, MASS_COUNT_FIXED)
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            base_field = field_source_projected(positions, adj, mass_nodes)
            delta = _paired_seed_delta_edge(positions, adj, src, det_list, base_field, mass_nodes, edge_fn)
            if delta is not None:
                by_b[b].append(delta)

        max_m = max(MASS_COUNTS)
        ranked = _select_fixed_mass_nodes(mass_layer, positions, center_y + FIXED_MASS_B, max_m)
        if len(ranked) < max_m:
            continue
        for m in MASS_COUNTS:
            mass_nodes = ranked[:m]
            base_field = field_source_projected(positions, adj, mass_nodes)
            delta = _paired_seed_delta_edge(positions, adj, src, det_list, base_field, mass_nodes, edge_fn)
            if delta is not None:
                by_m[m].append(delta)

    b_fit = _fit_full_positive_means(list(TARGET_BS), by_b)
    b_alpha = b_fit[0] if b_fit else None

    m_fit = _fit_full_positive_means(list(MASS_COUNTS), by_m)
    m_alpha = m_fit[0] if m_fit else None

    return b_alpha, m_alpha, {"by_b": by_b, "by_m": by_m}


def main() -> None:
    print("=" * 82)
    print("LOCAL CONTINUATION BACKREACTION d=0.50 CONFIRMATION")
    print("  Retained 3D modular DAG family only")
    print("  Goal: verify whether the d=0.50 pocket survives with more seeds")
    print("=" * 82)
    print()
    print(f"  seeds per sweep: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  k-band: {K_BAND}")
    print(f"  fixed mass count for b sweep: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass sweep: {FIXED_MASS_B}")
    print(f"  mass counts: {MASS_COUNTS}")
    print(f"  depth_weight: {DEPTH_WEIGHT}")
    print(f"  continuation strengths: {STRENGTHS}")
    print()

    # Hard k=0 sanity on a representative seed.
    positions, adj, layer_indices = generate_3d_modular_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=NODES_PER_LAYER,
        xyz_range=XYZ_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=7 * 17 + 3,
        gap=GAP,
    )
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    center_y = statistics.fmean(p[1] for p in positions)
    mass_layer = layer_indices[MASS_LAYER_OFFSET]
    mass_nodes = _select_fixed_mass_nodes(mass_layer, positions, center_y + FIXED_MASS_B, MASS_COUNT_FIXED)

    print("K=0 SANITY")
    print(
        f"  Laplacian baseline: k=0 delta = "
        f"{centroid_y(propagate_node_field(positions, adj, field_laplacian(positions, adj, mass_nodes), src, 0.0), positions, det_list) - centroid_y(propagate_node_field(positions, adj, [0.0] * len(positions), src, 0.0), positions, det_list):+.6e}"
    )
    print(
        f"  Source-projected node field: k=0 delta = "
        f"{centroid_y(propagate_node_field(positions, adj, field_source_projected(positions, adj, mass_nodes), src, 0.0), positions, det_list) - centroid_y(propagate_node_field(positions, adj, [0.0] * len(positions), src, 0.0), positions, det_list):+.6e}"
    )
    for strength in STRENGTHS:
        edge_fn = make_backreaction_edge_field(strength, EPS, DEPTH_WEIGHT)
        edge_field = edge_fn(positions, adj, mass_nodes)
        base_field = field_source_projected(positions, adj, mass_nodes)
        with_field = propagate_edge_field(positions, adj, base_field, src, 0.0, edge_field)
        no_field = propagate_edge_field(positions, adj, [0.0] * len(positions), src, 0.0, {})
        delta0 = centroid_y(with_field, positions, det_list) - centroid_y(no_field, positions, det_list)
        print(f"  d=0.50 strength={strength:0.2f}: k=0 delta = {delta0:+.6e}")
    print()

    print("=" * 82)
    print("REFERENCE MODELS")
    print("=" * 82)
    print("  Laplacian and source-projected node field are the companion controls.")
    print()

    print("=" * 82)
    print("LOCAL CONTINUATION BACKREACTION d=0.50")
    print("=" * 82)
    print(f"  depth_weight fixed to {DEPTH_WEIGHT}")
    print(f"  seed count increased to {N_SEEDS} (above the 24-seed stability map)")
    print()

    base_b_alpha, base_m_alpha, base_data = _measure_backreaction(0.0, depth_weight=DEPTH_WEIGHT, n_seeds=N_SEEDS)
    print("[source-projected node field baseline]")
    print(f"  b alpha = {base_b_alpha if base_b_alpha is not None else 'NA'}")
    print(f"  M alpha = {base_m_alpha if base_m_alpha is not None else 'NA'}")
    print()

    summary: list[tuple[float, float | None, float | None]] = []
    for strength in STRENGTHS:
        b_alpha, m_alpha, data = _measure_backreaction(strength, depth_weight=DEPTH_WEIGHT, n_seeds=N_SEEDS)
        summary.append((strength, b_alpha, m_alpha))

        print(f"[d=0.50 strength={strength:0.2f}]")
        by_b = data["by_b"]
        by_m = data["by_m"]
        print(f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/b':>8s}  {'samples':>7s}")
        print(f"  {'-' * 44}")
        for b in TARGET_BS:
            vals = by_b[b]
            if not vals:
                print(f"  {b:3d}  FAIL")
                continue
            shift = _mean(vals)
            se = _se(vals)
            t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
            print(f"  {b:3d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift / b:+8.3f}  {len(vals):7d}")
        if b_alpha is not None:
            print(f"  Fit: shift ~= C * b^{b_alpha:.3f}")
        else:
            print("  Fit: full-sweep-positive power-law fit unavailable")
        print()

        print(f"  {'M':>4s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/M':>8s}  {'samples':>7s}")
        print(f"  {'-' * 46}")
        for m in MASS_COUNTS:
            vals = by_m[m]
            if not vals:
                print(f"  {m:4d}  FAIL")
                continue
            shift = _mean(vals)
            se = _se(vals)
            t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
            print(f"  {m:4d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift / m:+8.3f}  {len(vals):7d}")
        if m_alpha is not None:
            print(f"  Fit: shift ~= C * M^{m_alpha:.3f}")
        else:
            print("  Fit: full-sweep-positive power-law fit unavailable")
        print()

    print("=" * 82)
    print("COMPARISON")
    print(f"  strength values swept: {STRENGTHS}")
    for strength, b_alpha, m_alpha in summary:
        b_str = "NA" if b_alpha is None else f"{b_alpha:.3f}"
        m_str = "NA" if m_alpha is None else f"{m_alpha:.3f}"
        print(f"  strength={strength:0.2f}: b alpha = {b_str} | M alpha = {m_str}")
    print()
    print("REVIEW-SAFE INTERPRETATION")
    print("  If the d=0.50 pocket remains near b alpha ~ -0.43 and M alpha ~ +0.53")
    print("  with 32 seeds, it is stable enough to carry forward as the best modular")
    print("  backreaction pocket. If either exponent drifts materially, the pocket is")
    print("  still a partial lead but not a frozen result.")
    print("=" * 82)


if __name__ == "__main__":
    main()
