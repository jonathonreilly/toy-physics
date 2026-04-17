#!/usr/bin/env python3
"""Gate B non-label connectivity v2 harness.

Question:
  Can a forward-only connectivity rule built from actual positions, but not
  from grid-label NN connectivity, preserve the far-field grown-geometry
  gravity package?

This v2 rule uses a forward cone plus a minimum-edge floor.
It is intentionally distinct from the earlier KNN+floor candidate.
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
DRIFT = 0.2
CONE_ANGLE = 0.85
MIN_EDGES = 5
MAX_EDGES = 9
STRENGTHS = [1e-6, 1e-5, 5e-5]


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


def _build_forward_cone_floor_connectivity(family: Family, half: int) -> Family:
    positions = family.positions
    layers = family.layers
    adj: dict[int, list[int]] = {}

    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                src = _grid_index(layer, iy, iz, half)
                sx, sy, sz = positions[src]
                ranked: list[tuple[float, float, int]] = []
                for dst, (dxp, dyp, dzp) in zip(dst_nodes, dst_positions):
                    dx = dxp - sx
                    dy = dyp - sy
                    dz = dzp - sz
                    if dx <= 0:
                        continue
                    dist2 = dx * dx + dy * dy + dz * dz
                    angle = math.atan2(math.sqrt(dy * dy + dz * dz), dx)
                    ranked.append((angle, dist2, dst))
                ranked.sort(key=lambda item: (item[0], item[1]))
                selected: list[int] = []
                for angle, _dist2, dst in ranked:
                    if angle <= CONE_ANGLE and dst not in selected:
                        selected.append(dst)
                    if len(selected) >= MAX_EDGES:
                        break
                if len(selected) < MIN_EDGES:
                    for _angle, _dist2, dst in ranked:
                        if dst not in selected:
                            selected.append(dst)
                        if len(selected) >= MIN_EDGES:
                            break
                if len(selected) > MAX_EDGES:
                    selected = selected[:MAX_EDGES]
                adj[src] = selected

    return Family(
        f"{family.name} + cone-floor angle={CONE_ANGLE:g} min={MIN_EDGES} max={MAX_EDGES}",
        positions,
        layers,
        adj,
    )


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


def _measure_row_for_family(family: Family) -> tuple[int, int, float]:
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
        mi = _grid_index(gl, 0, iz_m, HALF)
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

    mi = _grid_index(gl, 0, round(3 / H), HALF)
    if mi < len(positions):
        series = []
        for strength in STRENGTHS:
            field = _field_for_mass(positions, mi, strength)
            amp = _propagate(positions, layers, adj, field)
            z_mass_c = _centroid_z(amp, positions, det)
            delta = z_mass_c - z_free
            series.append(max(delta, 1e-30))
        lx = [math.log(v) for v in STRENGTHS]
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
        t, tot, fpm = _measure_row_for_family(family)
        toward += t
        total += tot
        if math.isfinite(fpm):
            fm_vals.append(fpm)
    return toward, total, sum(fm_vals) / len(fm_vals) if fm_vals else math.nan


def main() -> None:
    t0 = time.time()
    print("=" * 80)
    print("GATE B NON-LABEL CONNECTIVITY V2")
    print("  No-restore grown geometry: label connectivity vs forward-cone floor")
    print("=" * 80)
    print(
        f"h={H}, W={2*HALF}, layers={N_LAYERS}, drift={DRIFT}, "
        f"seeds={len(SEEDS)}, z_masses={Z_MASSES}"
    )
    print(
        f"candidate rule: forward cone angle<={CONE_ANGLE}, "
        f"minimum edges={MIN_EDGES}, maximum edges={MAX_EDGES}"
    )
    print()
    print(f"{'family':<34} {'TOWARD':>10} {'F~M':>8}")

    rows = [
        ("exact grid", lambda _seed: _build_exact_grid(N_LAYERS, HALF)),
        (
            "no-restore label-NN",
            lambda seed: _build_label_connectivity(
                _build_no_restore_family(N_LAYERS, HALF, drift=DRIFT, seed=seed), HALF
            ),
        ),
        (
            "no-restore cone-floor",
            lambda seed: _build_forward_cone_floor_connectivity(
                _build_no_restore_family(N_LAYERS, HALF, drift=DRIFT, seed=seed), HALF
            ),
        ),
    ]

    for name, builder in rows:
        toward, total, fpm = _average_across_seeds(builder)
        pct = 100.0 * toward / total if total else 0.0
        fm_s = f"{fpm:.2f}" if math.isfinite(fpm) else "n/a"
        print(f"{name:<34} {toward:>2d}/{total:<2d} ({pct:>5.1f}%) {fm_s:>8}")

    print()
    print("SAFE INTERPRETATION")
    print("  This harness freezes one non-label forward-connectivity candidate only.")
    print("  Read the result as: does a forward-cone geometric rule preserve")
    print("  the far-field sign and F~M scaling on the retained grown family?")
    print("  If not, the connectivity bottleneck is stricter than a simple")
    print("  geometry-based forward fan.")
    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
