#!/usr/bin/env python3
"""Gate B v6: h=0.5 structured-growth sweep.

This is a bounded replay of the reported Gate B h=0.5 result:

  template previous layer + local drift + restoring force + NN connectivity

The script freezes a small review-friendly sweep over drift/restore pairs:

  - drift=0.3, restore=0.5
  - drift=0.2, restore=0.7
  - drift=0.1, restore=0.9
  - drift=0.0, restore=1.0

The goal is not a broad search or a dynamics theorem. The goal is one
artifact chain that says whether the structured-growth rule remains TOWARD
on the h=0.5 working regime.
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
H = 0.5
N_LAYERS = 13
HALF = 5
SEEDS = (5, 18, 31, 44)
MASS_Y_VALUES = (1.0, 1.5, 2.0)
MASS_STRENGTHS = (0.75, 1.0, 1.25)
SWEEP_ROWS = (
    (0.3, 0.5),
    (0.2, 0.7),
    (0.1, 0.9),
    (0.0, 1.0),
)


@dataclass
class Family:
    name: str
    positions: List[Tuple[float, float, float]]
    layers: List[List[int]]
    adj: Dict[int, List[int]]


def _grid_index(layer: int, iy: int, iz: int, half: int) -> int:
    span = 2 * half + 1
    return layer * span * span + (iy + half) * span + (iz + half)


def build_ordered_family(n_layers: int, half: int, h: float) -> Family:
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []
    adj: Dict[int, List[int]] = {}

    for layer in range(n_layers):
        x = layer * h
        nodes: List[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                idx = len(positions)
                positions.append((x, iy * h, iz * h))
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

    return Family("ordered lattice", positions, layers, adj)


def build_structured_growth(
    n_layers: int,
    half: int,
    h: float,
    drift: float,
    restore: float,
    seed: int,
) -> Family:
    """Template-copy growth with local drift and fixed NN connectivity."""

    rng = random.Random(seed)
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []
    state: Dict[Tuple[int, int], Tuple[float, float]] = {}

    for layer in range(n_layers):
        x = layer * h
        nodes: List[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                target_y = iy * h
                target_z = iz * h
                if layer == 0:
                    y, z = target_y, target_z
                else:
                    prev_y, prev_z = state[(iy, iz)]
                    drift_y = prev_y + rng.gauss(0.0, drift * h)
                    drift_z = prev_z + rng.gauss(0.0, drift * h)
                    y = restore * target_y + (1.0 - restore) * drift_y
                    z = restore * target_z + (1.0 - restore) * drift_z
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
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        jy = iy + dy
                        jz = iz + dz
                        if -half <= jy <= half and -half <= jz <= half:
                            nbs.append(_grid_index(layer + 1, jy, jz, half))
                adj[src] = nbs

    return Family(
        f"structured growth drift={drift:g} restore={restore:g}",
        positions,
        layers,
        adj,
    )


def field_for_mass(
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


def propagate(
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
                lval = math.sqrt(dx * dx + dy * dy + dz * dz)
                if lval < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                act = lval * (1.0 - lf)
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                amps[j] += ai * cmath.exp(1j * K * act) * w / lval
    return amps


def centroid_y(
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


def detector_probs(amps: Sequence[complex], det: Sequence[int]) -> Dict[int, float]:
    raw = {d: abs(amps[d]) ** 2 for d in det}
    total = sum(raw.values())
    if total <= 1e-30:
        return {d: 0.0 for d in det}
    return {d: p / total for d, p in raw.items()}


def mass_window_gain(
    probs_mass: Dict[int, float],
    probs_free: Dict[int, float],
    positions: Sequence[Tuple[float, float, float]],
    det: Sequence[int],
    y_mass: float,
    half_width: float = 0.75,
) -> float:
    gain = 0.0
    for d in det:
        if abs(positions[d][1] - y_mass) <= half_width:
            gain += probs_mass[d] - probs_free[d]
    return gain


def fit_power(xs: Sequence[float], ys: Sequence[float]) -> float:
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


def measure_family(fam: Family) -> dict:
    positions = fam.positions
    layers = fam.layers
    adj = fam.adj
    det = layers[-1]
    grav_layer = layers[2 * len(layers) // 3]

    free = propagate(positions, layers, adj, [0.0] * len(positions))
    free_centroid = centroid_y(free, positions, det)
    free_probs = detector_probs(free, det)

    toward = 0
    total = 0
    deltas: List[float] = []
    slopes: List[float] = []

    for y_mass in MASS_Y_VALUES:
        mass_idx = min(
            grav_layer,
            key=lambda i: abs(positions[i][1] - y_mass) + abs(positions[i][2]),
        )
        strengths = []
        gains = []
        for strength in MASS_STRENGTHS:
            field = field_for_mass(positions, mass_idx, strength * FIELD_SCALE)
            amps = propagate(positions, layers, adj, field)
            centroid = centroid_y(amps, positions, det)
            delta = centroid - free_centroid
            deltas.append(delta)
            total += 1
            if delta > 0:
                toward += 1
            probs_mass = detector_probs(amps, det)
            gain = mass_window_gain(probs_mass, free_probs, positions, det, y_mass)
            strengths.append(strength)
            gains.append(gain)
        slopes.append(fit_power(strengths, gains))

    mean_delta = sum(deltas) / len(deltas) if deltas else math.nan
    finite_slopes = [v for v in slopes if not math.isnan(v)]
    fpm = sum(finite_slopes) / len(finite_slopes) if finite_slopes else math.nan
    return {
        "toward": toward,
        "total": total,
        "mean_delta": mean_delta,
        "fpm": fpm,
    }


def main() -> None:
    started = time.time()
    print("=" * 92)
    print("EVOLVING NETWORK PROTOTYPE V6")
    print("  Gate B: h=0.5 structured-growth sweep")
    print("  Rule: template previous layer + drift + restore + NN connectivity")
    print("  Control: none; this is the frozen growth-rule sweep itself")
    print("=" * 92)
    print()
    print(
        f"Setup: h={H}, layers={N_LAYERS}, half-width={HALF}, "
        f"seeds={SEEDS}, mass strengths={MASS_STRENGTHS}, mass y targets={MASS_Y_VALUES}"
    )
    print("Coverage: 4 drift/restore rows x 4 seeds x 3 y targets x 3 strengths = 144 tests")
    print("Action: S = L(1-f), 3D forward propagation, valley-linear phase valley")
    print()
    print(f"{'drift':>6s} {'restore':>7s} {'toward':>8s} {'mean_delta':>11s} {'F~M':>6s} {'samples':>8s}")
    print(f"{'-' * 54}")

    rows = []
    for drift, restore in SWEEP_ROWS:
        acc = []
        for seed in SEEDS:
            fam = build_structured_growth(N_LAYERS, HALF, H, drift, restore, seed)
            acc.append(measure_family(fam))
        toward = sum(r["toward"] for r in acc)
        total = sum(r["total"] for r in acc)
        mean_delta = sum(r["mean_delta"] for r in acc) / len(acc)
        fpm_vals = [r["fpm"] for r in acc if not math.isnan(r["fpm"])]
        fpm = sum(fpm_vals) / len(fpm_vals) if fpm_vals else math.nan
        rows.append((drift, restore, toward, total, mean_delta, fpm))
        print(
            f"{drift:6.1f} {restore:7.1f} {toward:8d}/{total:<3d} "
            f"{mean_delta:+11.6f} {fpm:6.2f} {total:8d}"
        )

    if rows:
        best = max(rows, key=lambda row: (row[2] / row[3], row[5] if not math.isnan(row[5]) else -999))
        print()
        print("PAIRWISE READ")
        print(
            f"  best row: drift={best[0]:.1f}, restore={best[1]:.1f}, "
            f"toward={best[2]}/{best[3]}, mean_delta={best[4]:+.6f}, F~M={best[5]:.2f}"
        )
    print()
    print("SAFE INTERPRETATION")
    print("  - This replay is the small h=0.5 structured-growth sweep.")
    print("  - The row count is the review-safe evidence unit; do not generalize")
    print("    beyond the tested drift/restore matrix.")
    print("  - If all rows are TOWARD, that means the growth rule is robust on the")
    print("    tested h=0.5 window, not that Gate B is closed everywhere.")
    print("  - If any row is mixed, keep the note conservative and treat the sweep")
    print("    as a bounded Gate B advance rather than a theorem.")
    print()
    print(f"Total time: {time.time() - started:.1f}s")
    print("=" * 92)


if __name__ == "__main__":
    main()
