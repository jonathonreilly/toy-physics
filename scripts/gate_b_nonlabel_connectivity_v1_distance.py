#!/usr/bin/env python3
"""Gate B non-label connectivity V1 distance-law companion.

Bounded companion to gate_b_nonlabel_connectivity_v1.py.

Question:
  On the retained h = 0.5 no-restore grown family, does the positive
  geometry-sector stencil still support a positive declining far-field
  distance-law fit better than the naive KNN+floor control?

This harness stays narrow:
  - exact grid control
  - no-restore grown geometry with geometry-sector connectivity

Only the far-field TOWARD fraction and the declining distance-law fit are
measured here.
"""

from __future__ import annotations

import cmath
import math
import random
import time
from dataclasses import dataclass


BETA = 0.8
K = 5.0
H = 0.5
N_LAYERS = 25
HALF = 10
SEEDS = list(range(4))
Z_MASSES = [3, 4, 5]
DRIFT = 0.2


@dataclass
class Family:
    name: str
    positions: list[tuple[float, float, float]]
    layers: list[list[int]]
    adj: dict[int, list[int]]


@dataclass
class DistanceRow:
    label: str
    toward: int
    total: int
    slope: float
    r2: float
    peak_z: int


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


def _build_geometry_sector_connectivity(family: Family, half: int) -> Family:
    """Geometry-only forward stencil.

    For each source node, use the source's actual position and the next-layer
    node positions to select one representative in each of the local 3x3
    (dy,dz) sectors, then backfill to a minimum edge floor.
    """

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
                sector_best: dict[tuple[int, int], tuple[float, int]] = {}
                ranked: list[tuple[float, int]] = []
                for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                    dyc = dy - sy
                    dzc = dz - sz
                    by = max(-1, min(1, int(round(dyc / H))))
                    bz = max(-1, min(1, int(round(dzc / H))))
                    dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                    ranked.append((dist2, dst))
                    key = (by, bz)
                    prev = sector_best.get(key)
                    if prev is None or dist2 < prev[0]:
                        sector_best[key] = (dist2, dst)

                selected = [dst for _, dst in sorted(sector_best.values(), key=lambda item: item[0])]
                for _, dst in sorted(ranked, key=lambda item: item[0]):
                    if len(selected) >= 9:
                        break
                    if dst not in selected:
                        selected.append(dst)
                adj[src] = selected

    return Family(f"{family.name} + geometry-sector stencil", positions, layers, adj)


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


def _fit_power(b_data: list[float], d_data: list[float]) -> tuple[float | None, float | None]:
    if len(b_data) < 3:
        return None, None
    lx = [math.log(float(v)) for v in b_data]
    ly = [math.log(float(v)) for v in d_data]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None, None
    slope = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sxx
    ss_res = sum((y - (my + slope * (x - mx))) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def _measure_row(label: str, family_builder) -> tuple[DistanceRow, dict[int, float]]:
    toward = 0
    total = 0
    z_to_deltas = {z: [] for z in Z_MASSES}

    for seed in SEEDS:
        family = family_builder(seed)
        positions = family.positions
        layers = family.layers
        adj = family.adj
        det = layers[-1]
        gl = 2 * len(layers) // 3

        free = _propagate(positions, layers, adj, [0.0] * len(positions))
        z_free = _centroid_z(free, positions, det)

        for z_mass in Z_MASSES:
            mi = min(
                layers[gl],
                key=lambda i: (positions[i][1]) ** 2 + (positions[i][2] - z_mass) ** 2,
            )
            amps = _propagate(positions, layers, adj, _field_for_mass(positions, mi, 5e-5))
            z_mass_c = _centroid_z(amps, positions, det)
            if not math.isfinite(z_mass_c) or not math.isfinite(z_free):
                continue
            delta = z_mass_c - z_free
            z_to_deltas[z_mass].append(delta)
            total += 1
            if delta > 0:
                toward += 1

    mean_deltas = {z: sum(vals) / len(vals) for z, vals in z_to_deltas.items() if vals}
    b_data = [z for z in Z_MASSES if z in mean_deltas and mean_deltas[z] > 0]
    d_data = [mean_deltas[z] for z in b_data]
    if len(d_data) < 3:
        raise SystemExit(f"not enough positive mean deltas to fit distance law for {label}")
    peak_i = max(range(len(d_data)), key=lambda i: d_data[i])
    slope, r2 = _fit_power(b_data[peak_i:], d_data[peak_i:])
    if slope is None or r2 is None:
        raise SystemExit(f"distance fit failed for {label}")
    return DistanceRow(label=label, toward=toward, total=total, slope=slope, r2=r2, peak_z=b_data[peak_i]), mean_deltas


def main() -> None:
    t0 = time.time()
    print("=" * 74)
    print("GATE B NON-LABEL CONNECTIVITY V1 DISTANCE-LAW COMPANION")
    print("  exact grid vs geometry-sector stencil on the retained no-restore family")
    print("=" * 74)
    print(f"h={H}, W={HALF}, NL={N_LAYERS}, seeds={len(SEEDS)}, z={Z_MASSES}, drift={DRIFT}")
    print("growth rule: template previous layer + drift, no restore, then geometry-only connectivity")
    print()

    exact = _build_exact_grid(N_LAYERS, HALF)

    def exact_builder(_seed: int) -> Family:
        return exact

    def sector_builder(seed: int) -> Family:
        grown = _build_no_restore_family(N_LAYERS, HALF, DRIFT, seed)
        return _build_geometry_sector_connectivity(grown, HALF)

    rows = [
        _measure_row("exact grid", exact_builder),
        _measure_row("geometry-sector stencil", sector_builder),
    ]

    for row, mean_deltas in rows:
        pct = row.toward / max(row.total, 1)
        print(f"{row.label:28s}: {row.toward}/{row.total} TOWARD ({pct:.0%}), tail=b^({row.slope:.2f}), R^2={row.r2:.3f}, peak_z={row.peak_z}")
        for z in Z_MASSES:
            if z in mean_deltas:
                print(f"    z={z}: mean delta={mean_deltas[z]:+.8f}")
        print()

    print(f"Total time: {time.time() - t0:.0f}s")
    print()
    print("SAFE INTERPRETATION")
    print("  This harness freezes the h=0.5 distance-law comparison only.")
    print("  It should be read as a bounded refinement check on the same")
    print("  no-restore grown family, not as a full Gate B closure.")


if __name__ == "__main__":
    main()
