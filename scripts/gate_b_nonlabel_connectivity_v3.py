#!/usr/bin/env python3
"""Gate B v3: local degree-balancing forward connectivity without label-NN.

This is a bounded forward-connectivity candidate for Gate B.

Question:
  Can we replace the grid-label NN rule with a non-label rule that only uses
  local positions plus a degree-balancing penalty, while still preserving the
  far-field grown-geometry package?

The comparison is intentionally narrow:
  - exact grid control
  - no-restore grown geometry with label connectivity
  - no-restore grown geometry with degree-balanced matching connectivity

Only the far-field gravity sign and F~M scaling are measured here.
"""

from __future__ import annotations

import cmath
import math
import random
import time
from dataclasses import dataclass


BETA = 0.8
K = 5.0
FIELD_STRENGTH = 5e-5
H = 0.5
N_LAYERS = 25
HALF = 10
SEEDS = list(range(4))
Z_MASSES = [3, 4, 5]
DRIFT_ROWS = [0.0, 0.1, 0.2, 0.3, 0.5]
DEGREE_ALPHA = 0.03
TARGET_OUT_DEGREE = 9


@dataclass
class Family:
    name: str
    positions: list[tuple[float, float, float]]
    layers: list[list[int]]
    adj: dict[int, list[int]]


def _grid_index(layer: int, iy: int, iz: int, half: int) -> int:
    span = 2 * half + 1
    return layer * span * span + (iy + half) * span + (iz + half)


def _build_exact_grid(n_layers: int, half: int) -> Family:
    positions: list[tuple[float, float, float]] = []
    layers: list[list[int]] = []
    adj: dict[int, list[int]] = {}

    for layer in range(n_layers):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                idx = len(positions)
                positions.append((x, iy * H, iz * H))
                nodes.append(idx)
        layers.append(nodes)

    for layer in range(n_layers - 1):
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                src = _grid_index(layer, iy, iz, half)
                nbs: list[int] = []
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        jy = iy + dy
                        jz = iz + dz
                        if -half <= jy <= half and -half <= jz <= half:
                            nbs.append(_grid_index(layer + 1, jy, jz, half))
                adj[src] = nbs

    return Family("exact grid", positions, layers, adj)


def _build_no_restore_family(n_layers: int, half: int, drift: float, seed: int) -> Family:
    rng = random.Random(seed)
    positions: list[tuple[float, float, float]] = []
    layers: list[list[int]] = []
    state: dict[tuple[int, int], tuple[float, float]] = {}

    for layer in range(n_layers):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                if layer == 0:
                    y, z = iy * H, iz * H
                else:
                    py, pz = state[(iy, iz)]
                    y = py + rng.gauss(0.0, drift * H)
                    z = pz + rng.gauss(0.0, drift * H)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                state[(iy, iz)] = (y, z)
        layers.append(nodes)

    return Family(f"no-restore drift={drift:g}", positions, layers, {})


def _build_label_connectivity(family: Family, half: int) -> Family:
    adj: dict[int, list[int]] = {}
    for layer in range(len(family.layers) - 1):
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                src = _grid_index(layer, iy, iz, half)
                nbs: list[int] = []
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        jy = iy + dy
                        jz = iz + dz
                        if -half <= jy <= half and -half <= jz <= half:
                            nbs.append(_grid_index(layer + 1, jy, jz, half))
                adj[src] = nbs
    return Family(f"{family.name} + label connectivity", family.positions, family.layers, adj)


def _build_degree_balanced_connectivity(family: Family, half: int) -> Family:
    """Pick forward edges by distance plus a local target-load penalty.

    This avoids direct grid-label NN connectivity while still preserving a
    layered forward structure. Each source node selects the same number of
    outgoing edges as the label-NN control, but target selection is decided by
    actual geometry and current load only.
    """

    positions = family.positions
    layers = family.layers
    adj: dict[int, list[int]] = {}

    for layer in range(len(layers) - 1):
        src_nodes = layers[layer]
        dst_nodes = layers[layer + 1]
        target_load = {dst: 0 for dst in dst_nodes}

        for src in src_nodes:
            sx, sy, sz = positions[src]
            ranked: list[tuple[float, int]] = []
            for dst in dst_nodes:
                dx, dy, dz = positions[dst]
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                score = dist2 + DEGREE_ALPHA * target_load[dst]
                ranked.append((score, dst))
            ranked.sort(key=lambda item: (item[0], item[1]))

            selected: list[int] = []
            for _, dst in ranked:
                if dst not in selected:
                    selected.append(dst)
                    target_load[dst] += 1
                if len(selected) >= TARGET_OUT_DEGREE:
                    break
            adj[src] = selected

    return Family(f"{family.name} + degree-balanced matching", positions, layers, adj)


def _field_for_mass(positions: list[tuple[float, float, float]], mass_idx: int, strength: float) -> list[float]:
    mx, my, mz = positions[mass_idx]
    field = []
    for x, y, z in positions:
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
        field.append(strength / r)
    return field


def _propagate(
    positions: list[tuple[float, float, float]],
    layers: list[list[int]],
    adj: dict[int, list[int]],
    field: list[float],
) -> list[complex]:
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


def _centroid_z(amps: list[complex], positions: list[tuple[float, float, float]], det: list[int]) -> float:
    total = 0.0
    weighted = 0.0
    for d in det:
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * positions[d][2]
    return weighted / total if total > 1e-30 else 0.0


def _measure_row_for_family(family: Family, half: int) -> tuple[int, int, float]:
    positions = family.positions
    layers = family.layers
    adj = family.adj
    det = layers[-1]
    gl = 2 * len(layers) // 3
    toward = 0
    total = 0
    fm_vals: list[float] = []

    free = _propagate(positions, layers, adj, [0.0] * len(positions))
    z_free = _centroid_z(free, positions, det)
    for z_mass in Z_MASSES:
        iz_m = round(z_mass / H)
        mi = _grid_index(gl, 0, iz_m, half)
        if mi >= len(positions):
            continue
        field = _field_for_mass(positions, mi, FIELD_STRENGTH)
        amp = _propagate(positions, layers, adj, field)
        z_mass_c = _centroid_z(amp, positions, det)
        if not math.isfinite(z_mass_c) or not math.isfinite(z_free):
            continue
        delta = z_mass_c - z_free
        total += 1
        if delta > 0:
            toward += 1

    mi = _grid_index(gl, 0, round(3 / H), half)
    if mi < len(positions):
        series = []
        for strength in [1e-6, 1e-5, 5e-5]:
            amp = _propagate(positions, layers, adj, _field_for_mass(positions, mi, strength))
            z_mass_c = _centroid_z(amp, positions, det)
            if math.isfinite(z_mass_c):
                delta = z_mass_c - z_free
                series.append(max(delta, 1e-30))
        if len(series) >= 3:
            lx = [math.log(v) for v in [1e-6, 1e-5, 5e-5]]
            ly = [math.log(v) for v in series]
            mx = sum(lx) / len(lx)
            my = sum(ly) / len(ly)
            sxx = sum((x - mx) ** 2 for x in lx)
            if sxx > 1e-30:
                sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
                fm_vals.append(sxy / sxx)

    fpm = sum(fm_vals) / len(fm_vals) if fm_vals else math.nan
    return toward, total, fpm


def _average_across_seeds(builder) -> tuple[int, int, float]:
    toward = 0
    total = 0
    fm_vals: list[float] = []
    for seed in SEEDS:
        family = builder(seed)
        t, tot, fpm = _measure_row_for_family(family, HALF)
        toward += t
        total += tot
        if math.isfinite(fpm):
            fm_vals.append(fpm)
    return toward, total, sum(fm_vals) / len(fm_vals) if fm_vals else math.nan


def main() -> None:
    t0 = time.time()
    print("=" * 80)
    print("GATE B NON-LABEL CONNECTIVITY V3")
    print("  No-restore grown geometry: label connectivity vs degree-balanced matching")
    print("=" * 80)
    print(
        f"h={H}, W={2*HALF}, layers={N_LAYERS}, drift sweep={DRIFT_ROWS}, "
        f"seeds={len(SEEDS)}, z_masses={Z_MASSES}"
    )
    print(
        f"non-label rule: local degree-balanced matching with target out-degree "
        f"{TARGET_OUT_DEGREE} and alpha={DEGREE_ALPHA}"
    )
    print()
    print(f"{'family':<36} {'TOWARD':>10} {'F~M':>8}")

    rows = [
        ("exact grid", lambda _seed: _build_exact_grid(N_LAYERS, HALF)),
        (
            "no-restore label-NN",
            lambda seed: _build_label_connectivity(
                _build_no_restore_family(N_LAYERS, HALF, drift=0.2, seed=seed), HALF
            ),
        ),
        (
            "no-restore degree-balanced",
            lambda seed: _build_degree_balanced_connectivity(
                _build_no_restore_family(N_LAYERS, HALF, drift=0.2, seed=seed), HALF
            ),
        ),
    ]

    for name, builder in rows:
        toward, total, fpm = _average_across_seeds(builder)
        pct = 100.0 * toward / total if total else 0.0
        fm_s = f"{fpm:.2f}" if math.isfinite(fpm) else "n/a"
        print(f"{name:<36} {toward:>2d}/{total:<2d} ({pct:>5.1f}%) {fm_s:>8}")

    print()
    print("SAFE INTERPRETATION")
    print("  This harness freezes one non-label forward-connectivity candidate only.")
    print("  Read the result as: can local degree balancing preserve the far-field")
    print("  grown-geometry package, or does the signal collapse once direct label")
    print("  matching is removed?")
    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
