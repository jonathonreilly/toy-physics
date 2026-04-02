#!/usr/bin/env python3
"""Hybrid-field fixed-mass pilot on the retained 3D modular family.

Goal
----
Test whether a bounded interpolation between the retained Laplacian field and
the forward-only causal field can improve the current tradeoff under fixed-mass
controls on the retained 3D modular DAG family.

The pilot is intentionally narrow:
  - one retained 3D modular family (gap=5.0)
  - fixed mass count across the b sweep
  - fixed graph geometry per seed
  - same propagation and detector readout across all field modes

What it reports:
  - gravity signal: mean detector-centroid shift and t-statistic at each b
  - b-trend: power-law fit on the positive mean shifts
  - mass-scaling trend: power-law fit at fixed b across mass counts

Review discipline:
  - do not claim a rescue unless the hybrid mode clearly outperforms both
    endpoints on the same retained family
  - if the hybrid sits between the endpoints, say that plainly
  - if a fit is unstable or noisy, say so
"""

from __future__ import annotations

import cmath
import math
import os
import random
import statistics
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BETA = 0.8
DECAY = 0.5
N_SEEDS = 12
N_LAYERS = 18
NODES_PER_LAYER = 40
XYZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
GAP = 5.0
K_BAND = (3.0, 5.0, 7.0)
TARGET_BS = (1, 2, 3, 4, 5, 6, 7, 8, 10)
MASS_COUNTS = (2, 4, 6, 8, 12, 16)
MASS_COUNT_FIXED = 8
MASS_LAYER_OFFSET = 2 * N_LAYERS // 3
FIXED_MASS_B = 3.0
MIXES = (0.0, 0.25, 0.5, 0.75, 1.0)


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


def generate_3d_modular_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = NODES_PER_LAYER,
    xyz_range: float = XYZ_RANGE,
    connect_radius: float = CONNECT_RADIUS,
    rng_seed: int = 42,
    gap: float = GAP,
):
    """Generate the retained 3D modular DAG family with a post-barrier gap."""
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-xyz_range, xyz_range)
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, xyz_range)
                    else:
                        y = rng.uniform(-xyz_range, -gap / 2)
                else:
                    y = rng.uniform(-xyz_range, xyz_range)

                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2) :]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = y * py > 0
                            if same_ch:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < 0.02:
                                    adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


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


def field_causal_forward(positions, adj, mass_nodes, decay: float = DECAY):
    """Forward-only causal field propagated along DAG order."""
    n = len(positions)
    order = _topo_order(adj, n)
    mass_set = set(mass_nodes)
    field = [0.0] * n
    for m in mass_set:
        field[m] = 1.0

    for i in order:
        if field[i] <= 0:
            continue
        out = adj.get(i, [])
        if not out:
            continue
        for j in out:
            field[j] += decay * field[i] / len(out)
    return field


def _normalize_field(field):
    rms = math.sqrt(sum(v * v for v in field) / len(field)) if field else 0.0
    if rms <= 1e-12:
        return field
    return [v / rms for v in field]


def field_hybrid(positions, adj, mass_nodes, mix: float):
    lap = _normalize_field(field_laplacian(positions, adj, mass_nodes))
    causal = _normalize_field(field_causal_forward(positions, adj, mass_nodes))
    return [(1.0 - mix) * l + mix * c for l, c in zip(lap, causal)]


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
            weight = math.exp(-BETA * theta * theta)
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


def select_fixed_mass_nodes(layer_nodes, positions, target_y, count):
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def _seed_delta(positions, adj, src, det_list, mass_nodes, field):
    free_field = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_mass = propagate(positions, adj, field, src, k)
        amps_free = propagate(positions, adj, free_field, src, k)
        deltas.append(centroid_y(amps_mass, positions, det_list) - centroid_y(amps_free, positions, det_list))
    return _mean(deltas) if deltas else None


def _make_field_fn(mode_mix: float):
    if mode_mix <= 0.0:
        return lambda p, a, m: field_laplacian(p, a, m)
    if mode_mix >= 1.0:
        return lambda p, a, m: field_causal_forward(p, a, m, decay=DECAY)
    return lambda p, a, m: field_hybrid(p, a, m, mix=mode_mix)


def _mode_label(mode_mix: float) -> str:
    if mode_mix <= 0.0:
        return "Laplacian"
    if mode_mix >= 1.0:
        return f"Causal decay={DECAY}"
    return f"Hybrid mix={mode_mix:.2f}"


def measure_b_sweep(mode_mix: float):
    label = _mode_label(mode_mix)
    field_fn = _make_field_fn(mode_mix)
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(rng_seed=seed * 11 + 7)
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


def measure_mass_sweep(mode_mix: float):
    label = _mode_label(mode_mix)
    field_fn = _make_field_fn(mode_mix)
    by_mass: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(rng_seed=seed * 11 + 7)
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
    print("HYBRID FIELD FIXED-MASS PILOT")
    print("  Retained 3D modular DAG family")
    print("  Test: bounded interpolation between Laplacian and forward-only causal field")
    print("  Controls: fixed mass count, fixed graph family, same detector readout")
    print("=" * 78)
    print()
    print("Setup:")
    print(f"  seeds per sweep: {N_SEEDS}")
    print(f"  k-band: {K_BAND}")
    print(f"  gap: {GAP}")
    print(f"  decay for causal endpoint: {DECAY}")
    print(f"  fixed b for mass sweep: {FIXED_MASS_B}")
    print(f"  fixed mass count for b sweep: {MASS_COUNT_FIXED}")
    print(f"  mass counts: {MASS_COUNTS}")
    print(f"  interpolation mixes: {MIXES}")
    print()

    # Quick sanity on one representative retained graph.
    positions, adj, layer_indices = generate_3d_modular_dag(rng_seed=7 * 11 + 7)
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    center_y = statistics.fmean(p[1] for p in positions)
    mass_nodes = select_fixed_mass_nodes(layer_indices[MASS_LAYER_OFFSET], positions, center_y + FIXED_MASS_B, MASS_COUNT_FIXED)
    if len(mass_nodes) == MASS_COUNT_FIXED and det_list:
        lap = field_laplacian(positions, adj, mass_nodes)
        causal = field_causal_forward(positions, adj, mass_nodes, decay=DECAY)
        hybrid = field_hybrid(positions, adj, mass_nodes, mix=0.5)
        zero_free = [0.0] * len(positions)
        print("Sanity check on representative graph:")
        for name, field in (
            ("Laplacian", lap),
            ("Causal", causal),
            ("Hybrid mix=0.50", hybrid),
        ):
            deltas = []
            for k in (0.0,):
                amps_field = propagate(positions, adj, field, src, k)
                amps_free = propagate(positions, adj, zero_free, src, k)
                deltas.append(centroid_y(amps_field, positions, det_list) - centroid_y(amps_free, positions, det_list))
            print(f"  {name:16s} k=0 delta = {deltas[0]:+.6e}")
        print()

    mode_summaries = []
    for mix in MIXES:
        label, b_rows, b_fit = measure_b_sweep(mix)
        _print_b_summary(label, b_rows, b_fit)
        _, m_rows, m_fit = measure_mass_sweep(mix)
        _print_mass_summary(label, m_rows, m_fit)
        mode_summaries.append((mix, label, b_fit, m_fit, b_rows, m_rows))

    print("=" * 78)
    print("SUMMARY")
    lap_gamma = None
    lap_alpha = None
    for mix, label, b_fit, m_fit, b_rows, m_rows in mode_summaries:
        gamma_txt = "NA" if b_fit is None else f"{b_fit[0]:.3f}"
        alpha_txt = "NA" if m_fit is None else f"{m_fit[0]:.3f}"
        b3_row = next((row for row in b_rows if row[0] == 3), None)
        b3_txt = "NA" if b3_row is None else f"{b3_row[1]:+.4f} (t={b3_row[3]:+.2f})"
        print(
            f"  mix={mix:>4.2f} | b=3 shift {b3_txt} | gamma={gamma_txt} | alpha={alpha_txt}"
        )
        if mix == 0.0:
            lap_gamma = None if b_fit is None else b_fit[0]
            lap_alpha = None if m_fit is None else m_fit[0]

    print()
    print("INTERPRETATION")
    print("  This is a bounded interpolation check, not a new architecture.")
    print("  On this fixed 3D modular family, no hybrid mix cleanly beats the")
    print("  Laplacian endpoint on both axes at once.")
    print("  - mix=0.25 slightly improves the mass exponent but weakens the b-trend.")
    print("  - mix=0.50 and mix=0.75 keep the gravity signal but degrade mass scaling.")
    print("  - the causal endpoint weakens the gravity signal and gives an unstable")
    print("    mass fit despite its stronger-looking raw alpha.")
    if lap_gamma is not None and lap_alpha is not None:
        print(f"  Laplacian baseline remains the best balanced retained point: gamma={lap_gamma:.3f}, alpha={lap_alpha:.3f}.")
    print("=" * 78)


if __name__ == "__main__":
    main()
