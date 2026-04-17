#!/usr/bin/env python3
"""Gate B non-label forward-connectivity candidate v1.

This freezes one bounded question:

  Can we replace the label-based next-layer stencil with a geometry-only
  forward-sector rule that uses actual node positions, not grid labels, and
  still preserve the retained far-field grown-geometry package better than the
  naive KNN+floor control?

The comparison is intentionally narrow:
  - exact grid control
  - no-restore grown geometry with naive KNN+floor connectivity
  - no-restore grown geometry with a geometry-sector stencil connectivity

Only far-field TOWARD fraction and F~M are measured here.
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
K_NEIGHBORS = 3
MIN_EDGES = 5


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


def _build_knn_floor_connectivity(family: Family, half: int) -> Family:
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
                ranked = []
                for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                    dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                    ranked.append((dist2, dst))
                ranked.sort(key=lambda item: item[0])
                selected: list[int] = [dst for _, dst in ranked[:K_NEIGHBORS]]
                for _, dst in ranked:
                    if len(selected) >= MIN_EDGES:
                        break
                    if dst not in selected:
                        selected.append(dst)
                adj[src] = selected

    return Family(f"{family.name} + knn-floor k={K_NEIGHBORS} min={MIN_EDGES}", positions, layers, adj)


def _build_geometry_sector_connectivity(family: Family, half: int) -> Family:
    """Geometry-only forward stencil.

    For each source node, use the source's actual position and the next-layer
    node positions to select one representative in each of the local 3x3
    (dy,dz) sectors, then backfill to the minimum edge floor.
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
                for _, dst in sorted(ranked, key=lambda item: item[0]):
                    if len(selected) >= MIN_EDGES:
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
        mi = min(
            layers[gl],
            key=lambda i: (positions[i][1]) ** 2 + (positions[i][2] - z_mass) ** 2,
        )
        amps = _propagate(positions, layers, adj, _field_for_mass(positions, mi, 5e-5))
        z_mass_c = _centroid_z(amps, positions, det)
        if not math.isfinite(z_mass_c) or not math.isfinite(z_free):
            continue
        total += 1
        if z_mass_c - z_free > 0:
            toward += 1

    mi3 = min(layers[gl], key=lambda i: (positions[i][1]) ** 2 + (positions[i][2] - 3.0) ** 2)
    s_data: list[float] = []
    g_data: list[float] = []
    for s in [1e-6, 1e-5, 5e-5]:
        amps = _propagate(positions, layers, adj, _field_for_mass(positions, mi3, s))
        z_s = _centroid_z(amps, positions, det)
        delta = z_s - z_free
        if delta > 0:
            s_data.append(s)
            g_data.append(delta)
    if len(s_data) >= 3:
        lx = [math.log(x) for x in s_data]
        ly = [math.log(y) for y in g_data]
        mx = sum(lx) / len(lx)
        my = sum(ly) / len(ly)
        sxx = sum((x - mx) ** 2 for x in lx)
        if sxx > 1e-12:
            sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
            fm_vals.append(sxy / sxx)

    fm = sum(fm_vals) / len(fm_vals) if fm_vals else float("nan")
    return toward, total, fm


def _measure_grown_connectivity(
    connectivity_builder,
    half: int,
    drift: float,
) -> tuple[int, int, float]:
    toward = 0
    total = 0
    fm_vals: list[float] = []

    for seed in SEEDS:
        grown = _build_no_restore_family(N_LAYERS, half, drift, seed)
        family = connectivity_builder(grown, half)
        fam_toward, fam_total, fam_fm = _measure_row_for_family(family)
        toward += fam_toward
        total += fam_total
        if math.isfinite(fam_fm):
            fm_vals.append(fam_fm)

    fm = sum(fm_vals) / len(fm_vals) if fm_vals else float("nan")
    return toward, total, fm


def _print_row(label: str, family: Family) -> None:
    toward, total, fm = _measure_row_for_family(family)
    pct = toward / max(total, 1)
    fm_s = f"{fm:.2f}" if math.isfinite(fm) else "n/a"
    print(f"{label:28s}: {toward}/{total} TOWARD ({pct:.0%}), F~M={fm_s}")


def main() -> None:
    t0 = time.time()
    print("=" * 72)
    print("GATE B NON-LABEL CONNECTIVITY V1")
    print("  exact grid vs geometry-sector forward stencil vs KNN+floor")
    print("=" * 72)
    print(f"h={H}, W={HALF}, NL={N_LAYERS}, seeds={len(SEEDS)}, z={Z_MASSES}, drift={DRIFT}")
    print("growth rule: template previous layer + drift, then geometry-only connectivity")
    print()

    exact = _build_exact_grid(N_LAYERS, HALF)
    knn = _measure_grown_connectivity(_build_knn_floor_connectivity, HALF, DRIFT)
    sector = _measure_grown_connectivity(_build_geometry_sector_connectivity, HALF, DRIFT)

    _print_row("exact grid", exact)
    pct = knn[0] / max(knn[1], 1)
    fm_s = f"{knn[2]:.2f}" if math.isfinite(knn[2]) else "n/a"
    print(f"{'no-restore KNN+floor':28s}: {knn[0]}/{knn[1]} TOWARD ({pct:.0%}), F~M={fm_s}")
    pct = sector[0] / max(sector[1], 1)
    fm_s = f"{sector[2]:.2f}" if math.isfinite(sector[2]) else "n/a"
    print(f"{'geometry-sector stencil':28s}: {sector[0]}/{sector[1]} TOWARD ({pct:.0%}), F~M={fm_s}")

    print(f"\nTotal time: {time.time() - t0:.0f}s")
    print()
    print("SAFE INTERPRETATION")
    print("  This harness freezes one geometry-only forward-connectivity candidate.")
    print("  It should be read as a bounded comparison on the no-restore grown family,")
    print("  not as a full Gate B closure or a universal non-label connectivity theorem.")


if __name__ == "__main__":
    main()
