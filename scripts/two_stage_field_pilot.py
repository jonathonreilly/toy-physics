#!/usr/bin/env python3
"""Two-stage field pilot on the retained 3D modular DAG family.

Question:
  Can a bounded two-stage field architecture beat the current
  causal-vs-Laplacian tradeoff at all?

Scope:
  - retained 3D modular family only
  - fixed-mass controls for distance sweeps
  - fixed impact parameter for mass sweeps
  - compare:
      1. Laplacian relaxed baseline
      2. Forward-only causal field
      3. Two-stage hybrid field: causal near-field + Laplacian far-field

The pilot is intentionally narrow:
  - it does not try to be a final model
  - it only asks whether a bounded hybrid can improve both
    mass-scaling strength and distance falloff relative to the pure lanes
"""

from __future__ import annotations

import cmath
import math
import os
import random
import statistics
import sys
from collections import defaultdict, deque
from typing import Callable

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


BETA = 0.8
CAUSAL_DECAY = 0.5
BLEND_WIDTH = 2.0
GAP = 3.0
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 16
N_LAYERS = 18
NODES_PER_LAYER = 40
XYZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
MASS_LAYER_INDEX = 2 * N_LAYERS // 3
DIST_BS = (1, 2, 3, 4, 5, 6, 7, 8, 10)
MASS_COUNTS = (2, 4, 6, 8, 12, 16)
FIXED_MASS_COUNT = 8
FIXED_B_FOR_MASS = 3.0
STAGE_CUTS = (1.0, 2.0, 3.0)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _fit_power_law(xs: list[float], ys: list[float]) -> tuple[float, float, float] | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    logs_x = [math.log(x) for x, _ in pairs]
    logs_y = [math.log(y) for _, y in pairs]
    n = len(pairs)
    sx = sum(logs_x)
    sy = sum(logs_y)
    sxx = sum(x * x for x in logs_x)
    sxy = sum(x * y for x, y in zip(logs_x, logs_y))
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in logs_y)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(logs_x, logs_y))
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
) -> tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]]]:
    """Retained 3D modular DAG family with channel separation after the barrier."""

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
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(0)
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
    undirected: dict[int, set[int]] = defaultdict(set)
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


def field_causal_forward(positions, adj, mass_nodes, decay: float = CAUSAL_DECAY):
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


def make_two_stage_field(stage_cut: float, blend_width: float = BLEND_WIDTH, decay: float = CAUSAL_DECAY):
    """Causal near-field, Laplacian far-field, smooth transition in between."""

    def _field(positions, adj, mass_nodes):
        causal = field_causal_forward(positions, adj, mass_nodes, decay=decay)
        lap = field_laplacian(positions, adj, mass_nodes)
        n = len(positions)
        if not mass_nodes:
            return lap

        mass_x = statistics.fmean(positions[m][0] for m in mass_nodes)
        field = [0.0] * n
        for i, (x, _, _) in enumerate(positions):
            rel = x - mass_x
            if rel <= stage_cut:
                field[i] = causal[i]
            elif rel >= stage_cut + blend_width:
                field[i] = lap[i]
            else:
                t = (rel - stage_cut) / blend_width
                field[i] = (1.0 - t) * causal[i] + t * lap[i]
        return field

    return _field


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
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
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


def select_target_centered_mass_nodes(layer_nodes, positions, center_y, target_b, mass_count):
    """Same-side contiguous y-window used for the mass-scaling pilot."""

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
    if abs(mean_offset - target_b) > 1.0:
        return []
    return best_nodes


def seed_delta(
    positions,
    adj,
    src,
    det_list,
    mass_nodes,
    field_fn: Callable,
) -> float | None:
    field = field_fn(positions, adj, mass_nodes)
    free = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_mass = propagate(positions, adj, field, src, k)
        amps_free = propagate(positions, adj, free, src, k)
        p_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        p_free = sum(abs(amps_free[d]) ** 2 for d in det_list)
        if p_mass <= 1e-30 or p_free <= 1e-30:
            continue
        y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / p_mass
        y_free = sum(abs(amps_free[d]) ** 2 * positions[d][1] for d in det_list) / p_free
        deltas.append(y_mass - y_free)
    return _mean(deltas) if deltas else None


def measure_distance_family(label: str, field_fn: Callable) -> dict[str, object]:
    print(f"[{label}]")
    print(f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift*b':>8s}  {'samples':>7s}")
    print(f"  {'-' * 44}")

    by_b: dict[float, list[float]] = {b: [] for b in DIST_BS}

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(rng_seed=seed * 17 + 3)
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mass_layer = layer_indices[MASS_LAYER_INDEX]
        for b in DIST_BS:
            mass_nodes = select_fixed_mass_nodes(mass_layer, positions, center_y + b, FIXED_MASS_COUNT)
            if len(mass_nodes) != FIXED_MASS_COUNT:
                continue
            delta = seed_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_b[b].append(delta)

    pos_bs: list[float] = []
    pos_shifts: list[float] = []
    b_rows = []
    for b in DIST_BS:
        vals = by_b[b]
        if not vals:
            print(f"  {b:3d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"  {b:3d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift * b:+8.3f}  {len(vals):7d}")
        b_rows.append((b, shift, se, t, len(vals)))
        if shift > 0.0:
            pos_bs.append(b)
            pos_shifts.append(shift)

    fit = _fit_power_law(pos_bs, pos_shifts)
    if fit is not None:
        gamma, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * b^{gamma:.3f}  (R^2={r2:.3f})")
    else:
        gamma = math.nan
        c = math.nan
        r2 = math.nan
        print("  Fit: insufficient positive points for a stable power-law fit")
    print()
    return {"rows": b_rows, "gamma": gamma, "c": c, "r2": r2}


def measure_mass_family(label: str, field_fn: Callable) -> dict[str, object]:
    print(f"[{label}]")
    print(f"  {'M':>4s}  {'shift':>10s}  {'SE':>8s}  {'t':>6s}  {'shift/M':>10s}  {'samples':>7s}")
    print(f"  {'-' * 52}")

    by_mass: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(rng_seed=seed * 11 + 7)
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mass_layer = layer_indices[MASS_LAYER_INDEX]
        for target_n in MASS_COUNTS:
            mass_nodes = select_target_centered_mass_nodes(
                mass_layer, positions, center_y, FIXED_B_FOR_MASS, target_n
            )
            if len(mass_nodes) != target_n:
                continue
            delta = seed_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_mass[target_n].append(delta)

    counts: list[int] = []
    shifts: list[float] = []
    mass_rows = []
    for target_n in MASS_COUNTS:
        vals = by_mass[target_n]
        if not vals:
            print(f"  {target_n:4d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"  {target_n:4d}  {shift:+10.4f}  {se:8.4f}  {t:+6.2f}  {shift / target_n:+10.4f}  {len(vals):7d}")
        mass_rows.append((target_n, shift, se, t, len(vals)))
        if shift > 0.0:
            counts.append(target_n)
            shifts.append(shift)

    fit = _fit_power_law(counts, shifts)
    if fit is not None:
        alpha, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * M^{alpha:.3f}  (R^2={r2:.3f})")
    else:
        alpha = math.nan
        c = math.nan
        r2 = math.nan
        print("  Fit: insufficient positive points for a stable power-law fit")
    print()
    return {"rows": mass_rows, "alpha": alpha, "c": c, "r2": r2}


def representative_sanity(field_fn: Callable, label: str) -> float:
    positions, adj, layer_indices = generate_3d_modular_dag(rng_seed=5)
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
    mass_layer = layer_indices[MASS_LAYER_INDEX]
    mass_nodes = select_fixed_mass_nodes(mass_layer, positions, center_y + FIXED_B_FOR_MASS, FIXED_MASS_COUNT)
    if len(mass_nodes) != FIXED_MASS_COUNT:
        return math.nan
    field = field_fn(positions, adj, mass_nodes)
    free = [0.0] * len(positions)
    amps_mass = propagate(positions, adj, field, src, 0.0)
    amps_free = propagate(positions, adj, free, src, 0.0)
    p_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
    p_free = sum(abs(amps_free[d]) ** 2 for d in det_list)
    if p_mass <= 1e-30 or p_free <= 1e-30:
        return math.nan
    y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / p_mass
    y_free = sum(abs(amps_free[d]) ** 2 * positions[d][1] for d in det_list) / p_free
    delta = y_mass - y_free
    print(f"  {label}: k=0 delta = {delta:+.6e}")
    return delta


def build_modes() -> list[tuple[str, Callable]]:
    modes: list[tuple[str, Callable]] = [
        ("Laplacian baseline", lambda p, a, m: field_laplacian(p, a, m)),
        (f"Causal forward field (decay={CAUSAL_DECAY})", lambda p, a, m: field_causal_forward(p, a, m)),
    ]
    for cut in STAGE_CUTS:
        modes.append(
            (
                f"Two-stage hybrid (cut={cut:g})",
                make_two_stage_field(stage_cut=cut, blend_width=BLEND_WIDTH, decay=CAUSAL_DECAY),
            )
        )
    return modes


def main() -> None:
    print("=" * 78)
    print("TWO-STAGE FIELD PILOT")
    print("  Retained 3D modular DAG family, gap=3")
    print("  Fixed-mass controls on distance sweeps; fixed b on mass sweeps")
    print("  Question: can a causal-near / Laplacian-far hybrid beat the")
    print("            current causal-vs-Laplacian tradeoff at all?")
    print("=" * 78)
    print()
    print(f"  seeds per sweep: {N_SEEDS}")
    print(f"  k-band: {K_BAND}")
    print(f"  fixed mass count for distance sweep: {FIXED_MASS_COUNT}")
    print(f"  fixed b for mass sweep: {FIXED_B_FOR_MASS}")
    print(f"  hybrid stage cuts: {STAGE_CUTS}")
    print()

    modes = build_modes()
    mode_results: dict[str, dict[str, object]] = {}

    print("K=0 SANITY")
    for label, field_fn in modes:
        representative_sanity(field_fn, label)
    print()

    for label, field_fn in modes:
        print("=" * 78)
        print(label.upper())
        print("=" * 78)
        dist = measure_distance_family(label, field_fn)
        mass = measure_mass_family(label, field_fn)
        mode_results[label] = {"distance": dist, "mass": mass}

    lap = mode_results["Laplacian baseline"]
    causal = mode_results[f"Causal forward field (decay={CAUSAL_DECAY})"]

    lap_gamma = lap["distance"]["gamma"]
    causal_alpha = causal["mass"]["alpha"]
    causal_gamma = causal["distance"]["gamma"]

    print("=" * 78)
    print("COMPARISON")
    print(f"  Laplacian gamma = {lap_gamma:.3f}" if math.isfinite(lap_gamma) else "  Laplacian gamma = NA")
    print(
        f"  Causal alpha    = {causal_alpha:.3f}" if math.isfinite(causal_alpha) else "  Causal alpha    = NA"
    )
    print(
        f"  Causal gamma    = {causal_gamma:.3f}" if math.isfinite(causal_gamma) else "  Causal gamma    = NA"
    )

    best_hybrid = None
    best_hybrid_name = None
    best_score = -1e9
    for label, _field_fn in modes:
        if not label.startswith("Two-stage hybrid"):
            continue
        dist = mode_results[label]["distance"]
        mass = mode_results[label]["mass"]
        alpha = mass["alpha"]
        gamma = dist["gamma"]
        if not (math.isfinite(alpha) and math.isfinite(gamma)):
            continue
        score = alpha - gamma
        if score > best_score:
            best_score = score
            best_hybrid = (alpha, gamma)
            best_hybrid_name = label

    if best_hybrid is not None:
        alpha_h, gamma_h = best_hybrid
        print(f"  Best hybrid = {best_hybrid_name}")
        print(f"    alpha = {alpha_h:.3f}")
        print(f"    gamma = {gamma_h:.3f}")
        print(f"    score(alpha - gamma) = {best_score:.3f}")
        improves_mass = alpha_h > causal_alpha + 0.05 if math.isfinite(causal_alpha) else False
        improves_distance = gamma_h < lap_gamma - 0.05 if math.isfinite(lap_gamma) else False
        print(
            f"  Beats tradeoff? {'YES' if improves_mass and improves_distance else 'NO'} "
            "(mass wants higher alpha; distance wants lower gamma)"
        )
    else:
        print("  Best hybrid = NA")
        print("  Beats tradeoff? NO")

    print("=" * 78)


if __name__ == "__main__":
    main()
