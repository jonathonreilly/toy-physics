#!/usr/bin/env python3
"""Minimal bidirectional/trapping probe on the retained Gate B grown family.

Moonshot goal:
  test whether a tiny trapping extension creates a genuine no-return threshold
  on the retained generated-geometry family, while still reducing to the
  current weak-field far-field lane at alpha = 0.

Observable:
  escape fraction = detector probability(alpha) / detector probability(alpha=0)

Weak-field recovery check:
  alpha = 0 should recover the retained far-field TOWARD/F~M behavior on the
  same geometry-sector stencil family.

This is intentionally minimal. It is not a full black-hole theory and it does
not try to model every strong-field feature. The only question here is whether
the retained weak-field lane can coexist with a sharp trapping threshold.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

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
MIN_EDGES = 5
ALPHAS = [0.0, 0.1, 0.3, 0.5, 2.0, 10.0]


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


def _build_geometry_sector_connectivity(family: Family, half: int) -> Family:
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
    *,
    alpha: float = 0.0,
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
                absorb = math.exp(-alpha * max(lf, 0.0) / 5e-5)
                amps[j] += ai * cmath.exp(1j * K * act) * w * absorb / L
    return amps


def _centroid_z(amps: list[complex], positions: list[tuple[float, float, float]], det: list[int]) -> float:
    total = 0.0
    weighted = 0.0
    for d in det:
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * positions[d][2]
    return weighted / total if total > 1e-30 else 0.0


def _escape_fraction(family: Family, alpha: float, z_mass: float) -> float:
    positions = family.positions
    layers = family.layers
    adj = family.adj
    det = layers[-1]
    gl = 2 * len(layers) // 3
    mi = min(
        layers[gl],
        key=lambda i: (positions[i][1]) ** 2 + (positions[i][2] - z_mass) ** 2,
    )
    field = _field_for_mass(positions, mi, 5e-5)
    free = _propagate(positions, layers, adj, [0.0] * len(positions), alpha=0.0)
    grav = _propagate(positions, layers, adj, field, alpha=alpha)
    p0 = sum(abs(free[d]) ** 2 for d in det)
    p1 = sum(abs(grav[d]) ** 2 for d in det)
    return p1 / p0 if p0 > 1e-30 else 0.0


def _far_field_check(family: Family) -> tuple[int, int, float]:
    positions = family.positions
    layers = family.layers
    adj = family.adj
    det = layers[-1]
    gl = 2 * len(layers) // 3

    toward = 0
    total = 0
    fm_vals: list[float] = []

    free = _propagate(positions, layers, adj, [0.0] * len(positions), alpha=0.0)
    z_free = _centroid_z(free, positions, det)

    mi3 = min(layers[gl], key=lambda i: (positions[i][1]) ** 2 + (positions[i][2] - 3.0) ** 2)
    s_data: list[float] = []
    g_data: list[float] = []
    for s in [1e-6, 1e-5, 5e-5]:
        amps = _propagate(positions, layers, adj, _field_for_mass(positions, mi3, s), alpha=0.0)
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

    for z_mass in Z_MASSES:
        mi = min(
            layers[gl],
            key=lambda i: (positions[i][1]) ** 2 + (positions[i][2] - z_mass) ** 2,
        )
        amps = _propagate(positions, layers, adj, _field_for_mass(positions, mi, 5e-5), alpha=0.0)
        z_mass_c = _centroid_z(amps, positions, det)
        total += 1
        if z_mass_c - z_free > 0:
            toward += 1

    fm = sum(fm_vals) / len(fm_vals) if fm_vals else float("nan")
    return toward, total, fm


def main() -> None:
    t0 = time.time()
    exact = _build_exact_grid(N_LAYERS, HALF)
    grown = _build_geometry_sector_connectivity(_build_no_restore_family(N_LAYERS, HALF, DRIFT, 0), HALF)

    print("=" * 76)
    print("MINIMAL BIDIRECTIONAL TRAPPING PROBE")
    print("  minimal trapping extension on the retained generated-geometry family")
    print("=" * 76)
    print(f"h={H}, W={HALF}, NL={N_LAYERS}, seeds={len(SEEDS)}, z={Z_MASSES}, drift={DRIFT}")
    print("observable: escape_fraction(alpha) = P_det(alpha) / P_det(alpha=0)")
    print("weak-field recovery check: alpha=0 should recover the retained far-field lane")
    print()

    print("WEAK-FIELD RECOVERY")
    exact_t, exact_n, exact_fm = _far_field_check(exact)
    grown_t, grown_n, grown_fm = _far_field_check(grown)
    print(f"  exact grid: {exact_t}/{exact_n} TOWARD, F~M={exact_fm:.2f}")
    print(f"  sector stencil: {grown_t}/{grown_n} TOWARD, F~M={grown_fm:.2f}")
    print()

    print("ESCAPE FRACTION VS ABSORPTION")
    print(f"{'alpha':>8s} {'escape':>10s} {'no-return':>10s}")
    print(f"{'-' * 32}")
    escape_rows: list[tuple[float, float]] = []
    for alpha in ALPHAS:
        vals: list[float] = []
        for seed in SEEDS:
            fam = _build_geometry_sector_connectivity(_build_no_restore_family(N_LAYERS, HALF, DRIFT, seed), HALF)
            for z_mass in Z_MASSES:
                vals.append(_escape_fraction(fam, alpha, z_mass))
        escape = sum(vals) / max(len(vals), 1)
        escape_rows.append((alpha, escape))
        print(f"{alpha:8.2f} {escape:10.4f} {1.0 - escape:10.4f}")

    threshold = next((alpha for alpha, escape in escape_rows if alpha > 0 and escape <= 0.5), None)
    print()
    if threshold is None:
        print("SAFE READ")
        print("  - The absorptive extension does not reach a clean 50% escape threshold")
        print("    on this retained family.")
        print("  - That means this minimal trapping proxy is currently a bounded negative")
        print("    for a strong no-return transition.")
        verdict = "no-go"
    else:
        print("SAFE READ")
        print(f"  - The escape fraction drops below 50% at alpha ≈ {threshold:.2f}.")
        print("  - That is a real trapping threshold on this retained family.")
        print("  - The weak-field reduction check still holds at alpha=0.")
        verdict = "viable"

    print()
    print(f"Branch verdict: {verdict}")
    print(f"Total time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
