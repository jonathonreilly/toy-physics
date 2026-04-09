#!/usr/bin/env python3
"""Generated-family support recovery basin probe.

Question:
  Is the retained generated-family support recovery a one-point fluke or a
  small basin around the current kNN-floor tweak?

Scope:
  - compact generated 3D DAG family
  - tiny grid around the retained positive connectivity tweak
  - one retained observable: centroid sign relative to free propagation
  - one detector-support metric: support fraction above 1% of peak

This stays deliberately narrow. It does not broaden the source kernel or add a
new field architecture.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.causal_field_gravity import centroid_y, generate_3d_dag, propagate  # noqa: E402


N_LAYERS = 16
NODES_PER_LAYER = 24
Y_RANGE = 10.0
CONNECT_RADIUS = 3.2
N_SEEDS = 4
K = 5.0
TARGET_Y = 3.0
MASS_RADIUS = 2.5
SOURCE_STRENGTH = 0.004
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08

GRID = [
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 4),
    (3, 5),
    (3, 6),
    (4, 4),
    (4, 5),
    (4, 6),
]


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    adj: dict[int, list[int]]
    layers: list[list[int]]


@dataclass
class Row:
    k_nearest: int
    min_edges: int
    delta_mean: float
    toward_count: int
    total: int
    support_frac: float
    support_frac_se: float
    zero_shift_max: float


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _stdev(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) >= 2 else math.nan


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _select_mass_nodes(
    positions: list[tuple[float, float, float]],
    layer_nodes: list[int],
    cy: float,
) -> list[int]:
    target_y = cy + TARGET_Y
    ranked = sorted(
        layer_nodes,
        key=lambda i: ((positions[i][1] - target_y) ** 2 + positions[i][2] ** 2, abs(positions[i][1] - target_y)),
    )
    chosen: list[int] = []
    for idx in ranked:
        if abs(positions[idx][1] - target_y) <= MASS_RADIUS:
            chosen.append(idx)
    return chosen[:4] if len(chosen) >= 4 else ranked[:4]


def _green_field(
    positions: list[tuple[float, float, float]],
    mass_ids: list[int],
    weights: list[float],
    strength: float,
) -> list[float]:
    field = [0.0] * len(positions)
    source_pos = [positions[i] for i in mass_ids]
    if not source_pos:
        return field
    for i, (x, y, z) in enumerate(positions):
        val = 0.0
        for w, (mx, my, mz) in zip(weights, source_pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
            val += w * strength * math.exp(-GREEN_MU * r) / r
        field[i] = val / len(source_pos)
    return field


def _field_abs_max(field: list[float]) -> float:
    return max(abs(v) for v in field) if field else 0.0


def _family(seed: int) -> Family:
    positions, adj, layers = generate_3d_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=NODES_PER_LAYER,
        yz_range=Y_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=seed * 19 + 7,
    )
    return Family(positions=positions, adj=adj, layers=layers)


def _augment_knn_floor(family: Family, k_nearest: int, min_edges: int) -> Family:
    positions = family.positions
    layers = family.layers
    adj: dict[int, list[int]] = {i: list(nbs) for i, nbs in family.adj.items()}

    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        for src in layers[layer]:
            sx, sy, sz = positions[src]
            ranked: list[tuple[float, int]] = []
            for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, dst))
            ranked.sort(key=lambda item: item[0])
            selected = list(dict.fromkeys(adj.get(src, [])))
            for _, dst in ranked[:k_nearest]:
                if dst not in selected:
                    selected.append(dst)
            for _, dst in ranked:
                if len(selected) >= min_edges:
                    break
                if dst not in selected:
                    selected.append(dst)
            adj[src] = selected

    return Family(positions=positions, adj=adj, layers=layers)


def _support_frac(probs: list[float]) -> float:
    if not probs:
        return 0.0
    total = sum(probs)
    if total <= 1e-30:
        return 0.0
    norm = [p / total for p in probs if p > 0.0]
    if not norm:
        return 0.0
    peak = max(norm)
    return sum(1 for p in norm if p >= 0.01 * peak) / len(norm)


def _case(family: Family) -> dict[str, float]:
    positions = family.positions
    adj = family.adj
    layers = family.layers
    det = layers[-1]
    all_ys = [y for _, y, _ in positions]
    cy = sum(all_ys) / len(all_ys)
    mass_ids = _select_mass_nodes(positions, layers[len(layers) // 2], cy)
    if not mass_ids:
        return {"delta": 0.0, "support_frac": 0.0, "zero_shift": 0.0}

    raw = _green_field(
        positions,
        mass_ids,
        [1.0 / len(mass_ids)] * len(mass_ids),
        SOURCE_STRENGTH,
    )
    gain = FIELD_TARGET_MAX / _field_abs_max(raw) if _field_abs_max(raw) > 1e-30 else 1.0

    free = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
    z_free = centroid_y(free, positions, det)

    field0 = [gain * v for v in _green_field(
        positions,
        mass_ids,
        [1.0 / len(mass_ids)] * len(mass_ids),
        SOURCE_STRENGTH,
    )]
    amps0 = propagate(positions, adj, field0, layers[0], K)
    cluster_power = [abs(amps0[i]) ** 2 for i in mass_ids]
    weights = _normalize_weights(cluster_power)
    field_sc = [gain * v for v in _green_field(positions, mass_ids, weights, SOURCE_STRENGTH)]
    sc_amps = propagate(positions, adj, field_sc, layers[0], K)

    det_probs = [abs(sc_amps[d]) ** 2 for d in det]
    delta = centroid_y(sc_amps, positions, det) - z_free
    zero_amps = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
    zero_shift = centroid_y(zero_amps, positions, det) - z_free
    return {"delta": delta, "support_frac": _support_frac(det_probs), "zero_shift": zero_shift}


def _aggregate(rows: list[dict[str, float]]) -> tuple[float, int, int, float, float]:
    delta_vals = [r["delta"] for r in rows]
    support_vals = [r["support_frac"] for r in rows]
    toward = sum(1 for d in delta_vals if d > 0)
    return (
        _mean(delta_vals),
        toward,
        len(delta_vals),
        _mean(support_vals),
        max(abs(r["zero_shift"]) for r in rows),
    )


def main() -> None:
    families = [_family(seed) for seed in range(N_SEEDS)]

    print("=" * 100)
    print("GENERATED SUPPORT RECOVERY BASIN PROBE")
    print("  compact generated DAG family, tiny grid around the retained kNN-floor tweak")
    print("=" * 100)
    print(
        f"family seeds={N_SEEDS}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, "
        f"connect_radius={CONNECT_RADIUS}"
    )
    print(
        f"Green kernel: exp(-mu r)/(r+eps), mu={GREEN_MU:.2f}, eps={GREEN_EPS:.2f}, "
        f"field target max={FIELD_TARGET_MAX:.3f}"
    )
    print(f"source strength={SOURCE_STRENGTH:g}")
    print("observable: centroid sign count + detector support fraction")
    print("reduction check: zero source should recover free propagation exactly")
    print()

    print("BASELINE")
    base_rows = [_case(fam) for fam in families]
    base_delta, base_toward, base_total, base_support, base_zero = _aggregate(base_rows)
    print(f"  max |zero-source shift| = {base_zero:.3e}")
    print(
        f"  baseline delta = {base_delta:+.6e}, TOWARD = {base_toward}/{base_total}, "
        f"support_frac = {base_support:.3f}"
    )
    print()

    print(f"{'k':>2s} {'m':>2s} {'delta':>12s} {'TOWARD':>8s} {'support':>9s} {'zero':>10s}")
    print("-" * 52)
    for k_nearest, min_edges in GRID:
        tweak_rows = [_case(_augment_knn_floor(fam, k_nearest, min_edges)) for fam in families]
        delta, toward, total, support, zero = _aggregate(tweak_rows)
        print(f"{k_nearest:2d} {min_edges:2d} {delta:+12.6e} {toward:8d}/{total:<2d} {support:9.3f} {zero:10.3e}")

    print()
    print("SAFE READ")
    print(
        "  The basin is only real if the positive kNN-floor neighborhood broadens "
        "detector support while keeping the centroid sign TOWARD."
    )
    print(
        "  If only one point is positive, this collapses back to a fluke; if a small "
        "grid stays positive, the generated-family rescue is a small basin rather than "
        "a one-off."
    )


if __name__ == "__main__":
    main()
