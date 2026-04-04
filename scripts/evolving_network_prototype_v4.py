#!/usr/bin/env python3
"""Gate B v4: crystal-like structured growth vs recomputed connectivity.

This is a bounded prototype built around the new connectivity lesson:

  - position noise is tolerated on a fixed structured backbone
  - geometry-recomputed connectivity is the harder failure mode

The script compares one explicit growth rule against a clear imposed control:

  - structured crystal-like growth with restoring force + fixed-offset edges
  - K-NN connectivity recomputed from the same grown positions

The goal is not a broad search or a solved Gate B theorem. The goal is to
freeze one reviewer-facing comparison that says whether structured
connectivity materially improves the Gate B lane.
"""

from __future__ import annotations

import cmath
import math
import os
import random
import sys
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

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
RESTORE = 0.75
JITTER = 0.20


@dataclass
class Family:
    name: str
    positions: List[Tuple[float, float, float]]
    layers: List[List[int]]
    adj: Dict[int, List[int]]


def _grid_index(layer: int, iy: int, iz: int, half: int) -> int:
    span = 2 * half + 1
    return layer * span * span + (iy + half) * span + (iz + half)


def build_ordered_family(n_layers: int, half: int) -> Family:
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []
    adj: Dict[int, List[int]] = {}
    span = 2 * half + 1

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


def build_crystal_growth(
    n_layers: int,
    half: int,
    restoring: float,
    jitter: float,
    seed: int,
) -> Family:
    """Crystal-like growth with restoring force and fixed-offset connectivity.

    Each layer retains the same grid labels, but node positions are nudged by
    noise and then pulled back toward the label target. Connectivity remains
    fixed by label offsets rather than recomputed from geometry.
    """

    rng = random.Random(seed)
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []
    adj: Dict[int, List[int]] = {}
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
                    drift_y = prev_y + rng.gauss(0.0, jitter)
                    drift_z = prev_z + rng.gauss(0.0, jitter)
                    y = restoring * target_y + (1.0 - restoring) * drift_y
                    z = restoring * target_z + (1.0 - restoring) * drift_z
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                state[(iy, iz)] = (y, z)
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

    return Family(f"crystal restore={restoring:g} jitter={jitter:g}", positions, layers, adj)


def build_knn_control(family: Family, k: int = 9) -> Family:
    """Recompute connectivity from geometry using K-nearest neighbors."""

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
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                act = L * (1.0 - lf)
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                amps[j] += ai * cmath.exp(1j * K * act) * w / L
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


def mass_window_gain(
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


def detector_probs(
    amps: Sequence[complex], det: Sequence[int]
) -> Dict[int, float]:
    raw = {d: abs(amps[d]) ** 2 for d in det}
    total = sum(raw.values())
    if total <= 1e-30:
        return {d: 0.0 for d in det}
    return {d: p / total for d, p in raw.items()}


def control_knn_for_same_positions(fam: Family) -> Family:
    return build_knn_control(fam, k=9)


def eval_family(fam: Family, label: str) -> dict:
    positions = fam.positions
    layers = fam.layers
    det = layers[-1]
    baseline_field = [0.0] * len(positions)
    free_amps = propagate(positions, layers, fam.adj, baseline_field)
    free_centroid = centroid_y(free_amps, positions, det)
    grav_layer = layers[2 * len(layers) // 3]

    toward = 0
    total = 0
    deltas: List[float] = []
    slopes: List[float] = []

    for y_mass in MASS_Y_VALUES:
        mass_idx = min(grav_layer, key=lambda i: abs(positions[i][1] - y_mass))
        strengths = []
        gains = []
        for s in MASS_STRENGTHS:
            field = field_for_mass(positions, mass_idx, s * FIELD_SCALE)
            amps = propagate(positions, layers, fam.adj, field)
            centroid = centroid_y(amps, positions, det)
            delta = centroid - free_centroid
            deltas.append(delta)
            total += 1
            if delta > 0:
                toward += 1
            probs_free = detector_probs(free_amps, det)
            probs_mass = detector_probs(amps, det)
            gain = mass_window_gain(probs_mass, probs_free, positions, det, y_mass)
            strengths.append(s)
            gains.append(gain)
        slopes.append(fit_power(strengths, gains))

    mean_delta = sum(deltas) / len(deltas) if deltas else math.nan
    mean_alpha = sum(v for v in slopes if not math.isnan(v)) / max(1, len([v for v in slopes if not math.isnan(v)]))
    return {
        "label": label,
        "toward": toward,
        "total": total,
        "mean_delta": mean_delta,
        "alpha": mean_alpha,
        "free_centroid": free_centroid,
    }


def main() -> None:
    started = time.time()
    print("=" * 90)
    print("EVOLVING NETWORK PROTOTYPE V4")
    print("  Gate B: crystal-like structured growth vs recomputed connectivity")
    print("  Rule: restoring-force growth with fixed-offset connectivity")
    print("  Control: KNN connectivity on the same grown positions")
    print("=" * 90)
    print()

    ordered_scores = []
    crystal_scores = []
    knn_scores = []

    for seed in SEEDS:
        ordered = build_ordered_family(N_LAYERS, HALF)
        crystal = build_crystal_growth(N_LAYERS, HALF, RESTORE, JITTER, seed)
        knn = control_knn_for_same_positions(crystal)

        ordered_scores.append(eval_family(ordered, "ordered"))
        crystal_scores.append(eval_family(crystal, "crystal"))
        knn_scores.append(eval_family(knn, "knn"))

    def summarize(rows, key):
        vals = [r[key] for r in rows if r[key] == r[key]]
        return sum(vals) / len(vals) if vals else math.nan

    def report(name, rows):
        toward = summarize(rows, "toward")
        total = summarize(rows, "total")
        mean_delta = summarize(rows, "mean_delta")
        alpha = summarize(rows, "alpha")
        frac = toward / total if total else math.nan
        print(
            f"{name:<12s}  toward={toward:5.1f}/{total:3.0f} ({frac:4.2f})  "
            f"mean_delta={mean_delta:+.6f}  alpha={alpha:.2f}"
        )

    report("ordered", ordered_scores)
    report("crystal", crystal_scores)
    report("knn", knn_scores)

    crystal_frac = summarize(crystal_scores, "toward") / summarize(crystal_scores, "total")
    knn_frac = summarize(knn_scores, "toward") / summarize(knn_scores, "total")
    crystal_alpha = summarize(crystal_scores, "alpha")
    knn_alpha = summarize(knn_scores, "alpha")
    crystal_delta = summarize(crystal_scores, "mean_delta")
    knn_delta = summarize(knn_scores, "mean_delta")

    print()
    print("PAIRWISE READ")
    print(
        f"  crystal vs knn: Δtoward={crystal_frac - knn_frac:+.2f}, "
        f"Δmean_delta={crystal_delta - knn_delta:+.6f}, "
        f"Δalpha={crystal_alpha - knn_alpha:+.2f}"
    )
    print()
    print("SAFE INTERPRETATION")
    print("  - Position noise is tolerated on the structured backbone.")
    print("  - Recomputing connectivity from geometry is the harder failure mode.")
    print("  - The crystal-like growth rule is the best structured-connectivity")
    print("    prototype so far, but this sweep remains bounded and not a Gate B theorem.")
    print("  - If the crystal row beats KNN on toward and alpha, that is a real")
    print("    trust-building conversion; if not, the result is still useful because")
    print("    it tightens the connectivity bottleneck.")
    print()
    print(f"Total time: {time.time() - started:.1f}s")
    print("=" * 90)


if __name__ == "__main__":
    main()
