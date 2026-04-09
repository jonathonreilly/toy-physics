#!/usr/bin/env python3
"""Gate B connectivity tolerance replay.

This freezes a bounded question:

  If we keep the valley-linear 3D propagation law fixed, how much position
  noise can we tolerate before the gravity signal degrades, and how much does
  the connectivity rule matter compared with the node positions?

The harness compares a small fixed set of architectures:
  - ordered lattice baseline
  - jittered lattice with fixed connectivity
  - templated growth with fixed-offset connectivity
  - grown geometry with K-NN connectivity
  - snapped/grid-like connectivity

The goal is review-safe comparison, not a Gate B theorem.
"""

from __future__ import annotations

import cmath
import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


BETA = 0.8
K = 5.0
FIELD_STRENGTH = 5e-5
N_LAYERS = 13
HALF = 5
Y_MASSES = (2, 3, 4)
SEEDS = (5, 18, 31, 44, 57, 70)
JITTER_SWEEP = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)
MASS_STRENGTHS = (0.75, 1.0, 1.25)


@dataclass
class GraphFamily:
    name: str
    positions: List[Tuple[float, float, float]]
    layers: List[List[int]]
    adj: Dict[int, List[int]]


def _grid_index(layer: int, iy: int, iz: int, half: int) -> int:
    span = 2 * half + 1
    return layer * (span * span) + (iy + half) * span + (iz + half)


def _build_fixed_connectivity(n_layers: int, half: int) -> GraphFamily:
    span = 2 * half + 1
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

    return GraphFamily("ordered", positions, layers, adj)


def _jitter_positions(base: GraphFamily, jitter: float, seed: int) -> GraphFamily:
    rng = random.Random(seed)
    positions = []
    for x, y, z in base.positions:
        positions.append((x, y + rng.gauss(0.0, jitter), z + rng.gauss(0.0, jitter)))
    return GraphFamily(f"jitter={jitter:g}", positions, base.layers, base.adj)


def _templated_growth(n_layers: int, half: int, drift: float, seed: int, snap: bool = False) -> GraphFamily:
    rng = random.Random(seed)
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []

    # Keep the same layer-wise grid labels, but let the coordinates drift
    # locally from layer to layer.
    layer_state: Dict[Tuple[int, int], Tuple[float, float]] = {}
    for layer in range(n_layers):
        x = float(layer)
        nodes: List[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                if layer == 0:
                    y, z = float(iy), float(iz)
                else:
                    py, pz = layer_state[(iy, iz)]
                    y = py + rng.gauss(0.0, drift)
                    z = pz + rng.gauss(0.0, drift)
                    if snap:
                        y = round(y)
                        z = round(z)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                layer_state[(iy, iz)] = (y, z)
        layers.append(nodes)

    base = _build_fixed_connectivity(n_layers, half)
    name = "snapped" if snap else f"templated drift={drift:g}"
    return GraphFamily(name, positions, layers, base.adj)


def _knn_growth(n_layers: int, half: int, drift: float, k: int, seed: int) -> GraphFamily:
    rng = random.Random(seed)
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []
    layer_state: Dict[Tuple[int, int], Tuple[float, float]] = {}

    for layer in range(n_layers):
        x = float(layer)
        nodes: List[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                if layer == 0:
                    y, z = float(iy), float(iz)
                else:
                    py, pz = layer_state[(iy, iz)]
                    y = py + rng.gauss(0.0, drift)
                    z = pz + rng.gauss(0.0, drift)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                layer_state[(iy, iz)] = (y, z)
        layers.append(nodes)

    adj: Dict[int, List[int]] = {}
    for layer in range(n_layers - 1):
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

    return GraphFamily(f"knn k={k}", positions, layers, adj)


def _field_for_mass(positions: Sequence[Tuple[float, float, float]], mass_idx: int, strength: float) -> List[float]:
    mx, my, mz = positions[mass_idx]
    field = []
    for x, y, z in positions:
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
        field.append(strength / r)
    return field


def _blocked_barrier(layer_nodes: Sequence[int], positions: Sequence[Tuple[float, float, float]]) -> set[int]:
    blocked = set()
    for idx in layer_nodes:
        y = positions[idx][1]
        if -1.0 < y < 1.0:
            blocked.add(idx)
    return blocked


def _propagate(
    positions: Sequence[Tuple[float, float, float]],
    layers: Sequence[Sequence[int]],
    adj: Dict[int, List[int]],
    field: Sequence[float],
    blocked: set[int],
) -> List[complex]:
    n = len(positions)
    amps = [0j] * n
    source = layers[0][len(layers[0]) // 2]
    amps[source] = 1.0

    for layer in range(len(layers) - 1):
        for i in layers[layer]:
            if i in blocked:
                continue
            ai = amps[i]
            if abs(ai) < 1e-30:
                continue
            xi, yi, zi = positions[i]
            for j in adj.get(i, []):
                if j in blocked:
                    continue
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


def _centroid_y(amps: Sequence[complex], positions: Sequence[Tuple[float, float, float]], det: Sequence[int]) -> float:
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
    if len(xs) < 2:
        return math.nan
    lx = [math.log(x) for x in xs if x > 0]
    ly = [math.log(y) for y in ys if y > 0]
    if len(lx) != len(xs) or len(ly) != len(ys):
        return math.nan
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-30:
        return math.nan
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def _measure_family(graph: GraphFamily, mass_strengths: Sequence[float], y_masses: Sequence[int]) -> dict:
    positions = graph.positions
    layers = graph.layers
    adj = graph.adj
    det = layers[-1]
    bl = len(layers) // 3
    gl = 2 * len(layers) // 3
    barrier = layers[bl]
    blocked = _blocked_barrier(barrier, positions)
    field0 = [0.0] * len(positions)

    free = _propagate(positions, layers, adj, field0, blocked)
    free_probs = _detector_probs(free, det)

    toward = 0
    total = 0
    mass_deltas: List[float] = []
    scale_deltas: List[float] = []

    for y_mass in y_masses:
        mass_idx = None
        for node in layers[gl]:
            if round(positions[node][1]) == y_mass and round(positions[node][2]) == 0:
                mass_idx = node
                break
        if mass_idx is None:
            continue

        for strength in mass_strengths:
            field = _field_for_mass(positions, mass_idx, strength * FIELD_STRENGTH)
            mass = _propagate(positions, layers, adj, field, blocked)
            mass_probs = _detector_probs(mass, det)
            delta = _mass_window_gain(mass_probs, free_probs, positions, det, float(y_mass))
            if strength == mass_strengths[len(mass_strengths) // 2]:
                mass_deltas.append(delta)
            if delta > 0:
                toward += 1
            total += 1

        # Estimate the mass-scaling exponent from the fixed z_mass, using the
        # same strength sweep for every family.
        scale_series = []
        for strength in mass_strengths:
            field = _field_for_mass(positions, mass_idx, strength * FIELD_STRENGTH)
            mass = _propagate(positions, layers, adj, field, blocked)
            delta = _mass_window_gain(_detector_probs(mass, det), free_probs, positions, det, float(y_mass))
            scale_series.append(max(delta, 1e-30))
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
        "free_centroid": _centroid_y(free, positions, det),
    }


def _jitter_sweep(base: GraphFamily) -> List[Tuple[float, dict]]:
    rows = []
    for jitter in JITTER_SWEEP:
        acc = []
        for seed in SEEDS:
            graph = _jitter_positions(base, jitter=jitter, seed=seed)
            acc.append(_measure_family(graph, MASS_STRENGTHS, Y_MASSES))
        rows.append(
            (
                jitter,
                {
                    "toward_frac": sum(r["toward_frac"] for r in acc) / len(acc),
                    "mean_delta": sum(r["mean_delta"] for r in acc) / len(acc),
                    "fpm": sum(r["fpm"] for r in acc) / len(acc),
                },
            )
        )
    return rows


def _architecture_suite() -> List[Tuple[str, GraphFamily, dict]]:
    base = _build_fixed_connectivity(N_LAYERS, HALF)
    ordered = base
    jittered = _jitter_positions(base, jitter=0.5, seed=5)
    templated = _templated_growth(N_LAYERS, HALF, drift=0.22, seed=5, snap=False)
    knn = _knn_growth(N_LAYERS, HALF, drift=0.22, k=9, seed=5)
    snapped = _templated_growth(N_LAYERS, HALF, drift=0.22, seed=5, snap=True)
    fams = [
        ("ordered lattice", ordered),
        ("jittered lattice", jittered),
        ("templated growth", templated),
        ("K-NN grown", knn),
        ("snapped/grid-like", snapped),
    ]

    rows = []
    for name, graph in fams:
        acc = []
        for seed in SEEDS:
            if name == "ordered lattice":
                g = base
            elif name == "jittered lattice":
                g = _jitter_positions(base, jitter=0.5, seed=seed)
            elif name == "templated growth":
                g = _templated_growth(N_LAYERS, HALF, drift=0.22, seed=seed, snap=False)
            elif name == "K-NN grown":
                g = _knn_growth(N_LAYERS, HALF, drift=0.22, k=9, seed=seed)
            else:
                g = _templated_growth(N_LAYERS, HALF, drift=0.22, seed=seed, snap=True)
            acc.append(_measure_family(g, MASS_STRENGTHS, Y_MASSES))
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
    base = _build_fixed_connectivity(N_LAYERS, HALF)
    print("=" * 88)
    print("GATE B CONNECTIVITY TOLERANCE REPLAY")
    print("  Valley-linear gravity on layered 3D graphs")
    print("  Question: is position noise tolerated while connectivity structure matters?")
    print("=" * 88)
    print()
    print(
        f"Setup: layers={N_LAYERS}, half-width={HALF}, mass strengths={MASS_STRENGTHS}, "
        f"mass y targets={Y_MASSES}"
    )
    print("Action: S = L(1-f), 3D forward propagation, fixed valley-linear phase valley")
    print()

    print("Jitter sweep on fixed connectivity")
    print(f"  {'jitter':>6s}  {'toward':>8s}  {'mean_delta':>11s}  {'F~M':>6s}")
    print(f"  {'-' * 40}")
    for jitter, row in _jitter_sweep(base):
        print(
            f"  {jitter:6.2f}  {row['toward_frac']*100:7.1f}%  "
            f"{row['mean_delta']:+11.6f}  {row['fpm']:6.2f}"
        )

    print()
    print("Architecture comparison")
    print(f"  {'architecture':>18s}  {'toward':>8s}  {'mean_delta':>11s}  {'F~M':>6s}")
    print(f"  {'-' * 52}")
    for name, row in _architecture_suite():
        print(
            f"  {name:18s}  {row['toward_frac']*100:7.1f}%  "
            f"{row['mean_delta']:+11.6f}  {row['fpm']:6.2f}"
        )

    print()
    print("Interpretation:")
    print("  - Fixed connectivity tolerates substantial position noise.")
    print("  - Once connectivity is recomputed from geometry, the gain becomes mixed.")
    print("  - The local F~M fit stays in a non-catastrophic linear-response band.")
    print("  - This is a connectivity-vs-noise audit, not a Gate B theorem.")


if __name__ == "__main__":
    main()
