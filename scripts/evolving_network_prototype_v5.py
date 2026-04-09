#!/usr/bin/env python3
"""Gate B v5: cross-templated structured growth vs recomputed connectivity.

This is a bounded follow-up to the v4 crystal-like prototype.

The question is narrower here:

  If we grow the same layered 3D grid labels with a narrow cross-shaped
  structured backbone, does fixed-offset connectivity become more stable than
  recomputed KNN connectivity on the same grown positions?

The goal is not a broad search or a Gate B theorem. The goal is a single
reviewer-facing comparison that tests whether a tighter structured-
connectivity rule improves the mixed v4 result.
"""

from __future__ import annotations

import cmath
import math
import os
import random
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BETA = 0.8
K = 5.0
FIELD_SCALE = 5e-5
N_LAYERS = 13
HALF = 5
SEEDS = (5, 18, 31, 44, 57, 70)
MASS_Y_VALUES = (2, 3, 4)
MASS_STRENGTHS = (0.75, 1.0, 1.25)
DRIFT = 0.22
RESTORE = 0.70
CROSS_OFFSETS = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))


@dataclass
class Family:
    name: str
    positions: List[Tuple[float, float, float]]
    layers: List[List[int]]
    adj: Dict[int, List[int]]


def _grid_index(layer: int, iy: int, iz: int, half: int) -> int:
    span = 2 * half + 1
    return layer * span * span + (iy + half) * span + (iz + half)


def _build_ordered_family(n_layers: int, half: int) -> Family:
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []
    adj: Dict[int, List[int]] = {}

    for layer in range(n_layers):
        x = float(layer)
        nodes: List[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                idx = len(positions)
                positions.append((x, float(iy), float(iz)))
                nodes.append(idx)
        layers.append(nodes)

    for layer in range(n_layers - 1):
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                src = _grid_index(layer, iy, iz, half)
                nbs: List[int] = []
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        jy = iy + dy
                        jz = iz + dz
                        if -half <= jy <= half and -half <= jz <= half:
                            nbs.append(_grid_index(layer + 1, jy, jz, half))
                adj[src] = nbs

    return Family("ordered", positions, layers, adj)


def _build_cross_growth(n_layers: int, half: int, drift: float, seed: int) -> Family:
    """Template-copy growth with local drift and a cross-shaped backbone."""

    rng = random.Random(seed)
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []
    state: Dict[Tuple[int, int], Tuple[float, float]] = {}

    for layer in range(n_layers):
        x = float(layer)
        nodes: List[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                target_y = float(iy)
                target_z = float(iz)
                if layer == 0:
                    y, z = target_y, target_z
                else:
                    prev_y, prev_z = state[(iy, iz)]
                    drift_y = prev_y + rng.gauss(0.0, drift)
                    drift_z = prev_z + rng.gauss(0.0, drift)
                    # Keep the layer columnar: the label target remains the
                    # anchor, but local drift can shift the geometry within a
                    # narrow band.
                    y = RESTORE * target_y + (1.0 - RESTORE) * drift_y
                    z = RESTORE * target_z + (1.0 - RESTORE) * drift_z
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                state[(iy, iz)] = (y, z)
        layers.append(nodes)

    adj: Dict[int, List[int]] = {}
    for layer in range(n_layers - 1):
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                src = _grid_index(layer, iy, iz, half)
                nbs: List[int] = []
                for dy, dz in CROSS_OFFSETS:
                    jy = iy + dy
                    jz = iz + dz
                    if -half <= jy <= half and -half <= jz <= half:
                        nbs.append(_grid_index(layer + 1, jy, jz, half))
                adj[src] = nbs

    return Family(f"cross-growth drift={drift:g}", positions, layers, adj)


def _build_knn_control(family: Family, k: int = 5) -> Family:
    positions = family.positions
    layers = family.layers
    adj: Dict[int, List[int]] = {}
    for layer in range(len(layers) - 1):
        src_nodes = layers[layer]
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        for src in src_nodes:
            sx, sy, sz = positions[src]
            ranked = []
            for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, dst))
            ranked.sort(key=lambda item: item[0])
            adj[src] = [dst for _, dst in ranked[:k]]
    return Family(f"knn control k={k}", positions, layers, adj)


def _field_for_mass(
    positions: Sequence[Tuple[float, float, float]],
    mass_idx: int,
    strength: float,
) -> List[float]:
    mx, my, mz = positions[mass_idx]
    field = []
    for x, y, z in positions:
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
        field.append(strength / r)
    return field


def _propagate(
    positions: Sequence[Tuple[float, float, float]],
    layers: Sequence[Sequence[int]],
    adj: Dict[int, List[int]],
    field: Sequence[float],
) -> List[complex]:
    amps = [0j] * len(positions)
    source = layers[0][len(layers[0]) // 2]
    amps[source] = 1.0

    for layer in range(len(layers) - 1):
        for i in layers[layer]:
            ai = amps[i]
            if abs(ai) < 1e-30:
                continue
            xi, yi, zi = positions[i]
            for j in adj.get(i, []):
                xj, yj, zj = positions[j]
                dx = xj - xi
                dy = yj - yi
                dz = zj - zi
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                act = L * (1.0 - lf)
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                amps[j] += ai * cmath.exp(1j * K * act) * w / L
    return amps


def _centroid_y(
    amps: Sequence[complex],
    positions: Sequence[Tuple[float, float, float]],
    det: Sequence[int],
) -> float:
    total = 0.0
    weighted = 0.0
    for d in det:
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * positions[d][1]
    return weighted / total if total > 1e-30 else 0.0


def _detector_probs(amps: Sequence[complex], det: Sequence[int]) -> Dict[int, float]:
    raw = {d: abs(amps[d]) ** 2 for d in det}
    total = sum(raw.values())
    if total <= 1e-30:
        return {d: 0.0 for d in det}
    return {d: p / total for d, p in raw.items()}


def _mass_window_gain(
    probs_mass: Dict[int, float],
    probs_free: Dict[int, float],
    positions: Sequence[Tuple[float, float, float]],
    det: Sequence[int],
    y_mass: float,
    half_width: float = 1.5,
) -> float:
    gain = 0.0
    for d in det:
        if abs(positions[d][1] - y_mass) <= half_width:
            gain += probs_mass[d] - probs_free[d]
    return gain


def _fit_power(xs: Sequence[float], ys: Sequence[float]) -> float:
    pts = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pts) < 2:
        return math.nan
    lx = [math.log(x) for x, _ in pts]
    ly = [math.log(y) for _, y in pts]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    cov = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    var = sum((x - mx) ** 2 for x in lx)
    return cov / var if var > 0 else math.nan


def _measure_family(graph: Family, mass_strengths: Sequence[float], y_masses: Sequence[int]) -> dict:
    positions = graph.positions
    layers = graph.layers
    adj = graph.adj
    det = layers[-1]
    grav_layer = layers[2 * len(layers) // 3]
    field0 = [0.0] * len(positions)

    free = _propagate(positions, layers, adj, field0)
    free_probs = _detector_probs(free, det)

    toward = 0
    total = 0
    mass_deltas: List[float] = []
    scale_deltas: List[float] = []

    for y_mass in y_masses:
        mass_idx = None
        for node in grav_layer:
            if round(positions[node][1]) == y_mass and round(positions[node][2]) == 0:
                mass_idx = node
                break
        if mass_idx is None:
            continue

        scale_series = []
        for strength in mass_strengths:
            field = _field_for_mass(positions, mass_idx, strength * FIELD_SCALE)
            mass = _propagate(positions, layers, adj, field)
            probs_mass = _detector_probs(mass, det)
            delta = _mass_window_gain(probs_mass, free_probs, positions, det, float(y_mass))
            scale_series.append(max(delta, 1e-30))
            if strength == mass_strengths[len(mass_strengths) // 2]:
                mass_deltas.append(delta)
            if delta > 0:
                toward += 1
            total += 1
        scale_deltas.append(_fit_power(mass_strengths, scale_series))

    fpm = sum(v for v in scale_deltas if not math.isnan(v)) / max(
        1, sum(1 for v in scale_deltas if not math.isnan(v))
    )
    mean_delta = sum(mass_deltas) / len(mass_deltas) if mass_deltas else math.nan
    toward_frac = toward / total if total else math.nan
    return {
        "toward_frac": toward_frac,
        "mean_delta": mean_delta,
        "fpm": fpm,
    }


def _suite() -> List[Tuple[str, Family, dict]]:
    base = _build_ordered_family(N_LAYERS, HALF)
    cross = _build_cross_growth(N_LAYERS, HALF, DRIFT, seed=5)
    knn = _build_knn_control(cross, k=5)
    fams = [("ordered lattice", base), ("cross growth", cross), ("KNN control", knn)]

    rows = []
    for name, graph in fams:
        acc = []
        for seed in SEEDS:
            if name == "ordered lattice":
                g = base
            elif name == "cross growth":
                g = _build_cross_growth(N_LAYERS, HALF, DRIFT, seed=seed)
            else:
                g = _build_knn_control(_build_cross_growth(N_LAYERS, HALF, DRIFT, seed=seed), k=5)
            acc.append(_measure_family(g, MASS_STRENGTHS, MASS_Y_VALUES))
        rows.append(
            (
                name,
                {
                    "toward_frac": sum(r["toward_frac"] for r in acc) / len(acc),
                    "mean_delta": sum(r["mean_delta"] for r in acc) / len(acc),
                    "fpm": sum(r["fpm"] for r in acc) / len(acc),
                },
            )
        )
    return rows


def main() -> None:
    started = time.time()
    print("=" * 92)
    print("EVOLVING NETWORK PROTOTYPE V5")
    print("  Gate B: cross-templated growth vs KNN on the same positions")
    print("  Rule: local drift + narrow cross-shaped backbone, fixed-offset connectivity")
    print("  Control: KNN connectivity recomputed from the same grown positions")
    print("=" * 92)
    print()
    print(
        f"Setup: layers={N_LAYERS}, half-width={HALF}, drift={DRIFT}, "
        f"mass strengths={MASS_STRENGTHS}, mass y targets={MASS_Y_VALUES}"
    )
    print("Action: S = L(1-f), 3D forward propagation, valley-linear phase valley")
    print()
    print("Architecture comparison")
    print(f"  {'architecture':>18s}  {'toward':>8s}  {'mean_delta':>11s}  {'F~M':>6s}")
    print(f"  {'-' * 52}")
    rows = _suite()
    for name, row in rows:
        print(
            f"  {name:18s}  {row['toward_frac']*100:7.1f}%  "
            f"{row['mean_delta']:+11.6f}  {row['fpm']:6.2f}"
        )

    cross = rows[1][1]
    knn = rows[2][1]
    print()
    print("PAIRWISE READ")
    print(
        f"  cross vs knn: Δtoward={cross['toward_frac'] - knn['toward_frac']:+.2f}, "
        f"Δmean_delta={cross['mean_delta'] - knn['mean_delta']:+.6f}, "
        f"ΔF~M={cross['fpm'] - knn['fpm']:+.2f}"
    )
    print()
    print("SAFE INTERPRETATION")
    print("  - The fixed-offset cross rule is explicit and reviewable.")
    print("  - The control is fair: KNN on the same grown positions.")
    print("  - If the structured row beats KNN on toward and slope, that is a real gain.")
    print("  - If it only matches or trails KNN, the result still tightens the")
    print("    Gate B bottleneck to connectivity construction rather than raw noise.")
    print()
    print(f"Total time: {time.time() - started:.1f}s")
    print("=" * 92)


if __name__ == "__main__":
    main()
