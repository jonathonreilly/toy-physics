#!/usr/bin/env python3
"""Generated-family discriminator probe.

Question:
  Is the best current generated-family bridge point family-limited by
  connectivity/support concentration, or by the field rule itself?

Scope:
  - compact generated 3D DAG family
  - retained k-nearest floor augmentation as the bridge family
  - compare at most two bridge variants:
      1) support rescue + static Green
      2) support rescue + wavefield bridge
  - exact zero-source reduction check
  - one support metric: detector effective support N_eff
  - one compact diagnostic: geometry-vs-field bottleneck label from the
    relative sign-count and support deltas between the two variants

This is intentionally narrow. It does not try to close generated-family
physics. It only asks whether the current bridge is failing because the family
is too support-concentrated or because the wavefield rule itself is not the
limiting factor.
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
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08

K_NEAREST = 3
MIN_EDGES = 5
WAVE_NEIGHBOR_K = 4
WAVE_BLEND = 0.65


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    adj: dict[int, list[int]]
    layers: list[list[int]]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _stdev(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) >= 2 else math.nan


def _entropy_and_support(probs: list[float]) -> tuple[float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    return h, eff


def _select_mass_nodes(
    positions: list[tuple[float, float, float]],
    layer_nodes: list[int],
    cy: float,
) -> list[int]:
    target_y = cy + TARGET_Y
    ranked = sorted(
        layer_nodes,
        key=lambda i: (
            (positions[i][1] - target_y) ** 2 + positions[i][2] ** 2,
            abs(positions[i][1] - target_y),
        ),
    )
    chosen: list[int] = []
    for idx in ranked:
        if abs(positions[idx][1] - target_y) <= MASS_RADIUS:
            chosen.append(idx)
    return chosen[:4] if len(chosen) >= 4 else ranked[:4]


def _family(seed: int) -> Family:
    positions, adj, layers = generate_3d_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=NODES_PER_LAYER,
        yz_range=Y_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=seed * 19 + 7,
    )
    return Family(positions=positions, adj=adj, layers=layers)


def _augment_knn_floor(family: Family) -> Family:
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
            for _, dst in ranked[:K_NEAREST]:
                if dst not in selected:
                    selected.append(dst)
            for _, dst in ranked:
                if len(selected) >= MIN_EDGES:
                    break
                if dst not in selected:
                    selected.append(dst)
            adj[src] = selected

    return Family(positions=positions, adj=adj, layers=layers)


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    indeg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            indeg[j] += 1
    from collections import deque

    q = deque(i for i in range(n) if indeg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            indeg[j] -= 1
            if indeg[j] == 0:
                q.append(j)
    return order


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


def _causal_field(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_ids: list[int],
    weights: list[float],
    strength: float,
) -> list[float]:
    n = len(positions)
    order = _topo_order(adj, n)
    green = _green_field(positions, mass_ids, weights, strength)
    field = [0.0] * n
    parents: dict[int, list[int]] = {}
    for src, nbs in adj.items():
        for dst in nbs:
            parents.setdefault(dst, []).append(src)

    mass_set = set(mass_ids)
    for i in order:
        if i in mass_set:
            field[i] = green[i]
            continue
        ps = parents.get(i, [])
        if not ps:
            field[i] = green[i]
            continue
        parent_mean = sum(field[p] for p in ps) / len(ps)
        field[i] = 0.70 * parent_mean + 0.30 * green[i]
    return field


def _same_layer_neighbors(family: Family) -> dict[int, list[int]]:
    neighbors: dict[int, list[int]] = {}
    positions = family.positions
    for layer in family.layers:
        for i in layer:
            sx, sy, sz = positions[i]
            ranked: list[tuple[float, int]] = []
            for j in layer:
                if j == i:
                    continue
                dx, dy, dz = positions[j]
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, j))
            ranked.sort(key=lambda item: item[0])
            neighbors[i] = [j for _, j in ranked[:WAVE_NEIGHBOR_K]]
    return neighbors


def _wavefield_field(
    family: Family,
    adj: dict[int, list[int]],
    mass_ids: list[int],
    weights: list[float],
    strength: float,
) -> list[float]:
    causal = _causal_field(family.positions, adj, mass_ids, weights, strength)
    neighbors = _same_layer_neighbors(family)
    field = causal[:]
    for i in range(len(field)):
        nbs = neighbors.get(i, [])
        if not nbs:
            continue
        neigh_mean = sum(causal[j] for j in nbs) / len(nbs)
        field[i] = WAVE_BLEND * causal[i] + (1.0 - WAVE_BLEND) * neigh_mean
    return field


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _detector_eff_support(probs: list[float]) -> float:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0
    _, eff = _entropy_and_support(probs)
    return eff


def _evaluate(family: Family, mode: str) -> tuple[list[dict[str, float]], float]:
    positions = family.positions
    adj = family.adj
    layers = family.layers
    det = layers[-1]
    all_ys = [y for _, y, _ in positions]
    cy = sum(all_ys) / len(all_ys)
    mass_ids = _select_mass_nodes(positions, layers[len(layers) // 2], cy)
    if not mass_ids:
        return [], 1.0

    gain_probe_strength = max(SOURCE_STRENGTHS)
    ref_raw = _green_field(positions, mass_ids, [1.0 / len(mass_ids)] * len(mass_ids), gain_probe_strength)
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    free = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
    z_free = centroid_y(free, positions, det)

    zero_field = [0.0] * len(positions)
    zero_amps = propagate(positions, adj, zero_field, layers[0], K)
    zero_shift = centroid_y(zero_amps, positions, det) - z_free

    rows: list[dict[str, float]] = []
    for s in SOURCE_STRENGTHS:
        base_weights = [1.0 / len(mass_ids)] * len(mass_ids)
        field0 = [gain * v for v in _green_field(positions, mass_ids, base_weights, s)]
        amps0 = propagate(positions, adj, field0, layers[0], K)
        cluster_power = [abs(amps0[i]) ** 2 for i in mass_ids]
        weights_sc = _normalize_weights(cluster_power)

        if mode == "support_rescue":
            field = [gain * v for v in _green_field(positions, mass_ids, weights_sc, s)]
        elif mode == "wavefield":
            field = [gain * v for v in _wavefield_field(family, adj, mass_ids, weights_sc, s)]
        else:
            raise ValueError(f"unknown mode: {mode}")

        amps = propagate(positions, adj, field, layers[0], K)
        delta = centroid_y(amps, positions, det) - z_free
        det_probs = [abs(amps[d]) ** 2 for d in det]
        eff_support = _detector_eff_support(det_probs)
        rows.append(
            {
                "s": s,
                "delta": delta,
                "toward": 1.0 if delta > 0 else 0.0,
                "eff_support": eff_support,
                "zero_shift": zero_shift,
            }
        )

    return rows, zero_shift


def _summarize(rows: list[dict[str, float]], zero_shift: float) -> dict[str, float]:
    deltas = [r["delta"] for r in rows]
    effs = [r["eff_support"] for r in rows]
    toward = sum(1 for d in deltas if d > 0)
    return {
        "delta_mean": _mean(deltas),
        "toward_count": toward,
        "total": len(deltas),
        "eff_support": _mean(effs),
        "zero_shift": abs(zero_shift),
    }


def main() -> None:
    print("=" * 100)
    print("SOURCE-RESOLVED GENERATED DISCRIMINATOR PROBE")
    print("  support rescue vs wavefield bridge on the compact generated family")
    print("=" * 100)
    print(f"family seeds=0..{N_SEEDS - 1}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, connect_radius={CONNECT_RADIUS}")
    print(f"bridge family: k-nearest floor augmentation (k={K_NEAREST}, min_edges={MIN_EDGES})")
    print(f"bridge variants: support_rescue (static Green) vs wavefield")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"field target max: {FIELD_TARGET_MAX}")
    print("observables: zero-source reduction, centroid sign counts, detector N_eff")
    print("diagnostic: geometry-vs-field bottleneck label from sign/support deltas")
    print()

    per_case_results: dict[str, list[dict[str, float]]] = {}
    per_case_zero: dict[str, float] = {}

    for seed in range(N_SEEDS):
        base = _family(seed)
        bridge = _augment_knn_floor(base)
        for mode in ["support_rescue", "wavefield"]:
            rows, zero_shift = _evaluate(bridge, mode)
            per_case_results.setdefault(mode, []).extend(rows)
            per_case_zero[mode] = max(per_case_zero.get(mode, 0.0), abs(zero_shift))
            summary = _summarize(rows, zero_shift)
            print(
                f"seed={seed} {mode:>14s} "
                f"zero={summary['zero_shift']:.3e} "
                f"TOWARD={summary['toward_count']}/{summary['total']} "
                f"N_eff={summary['eff_support']:.2f}"
            )

    print()
    print("SUMMARY")
    support_summary = _summarize(per_case_results["support_rescue"], per_case_zero["support_rescue"])
    wave_summary = _summarize(per_case_results["wavefield"], per_case_zero["wavefield"])
    print(
        f"{'support_rescue':>14s}  zero={support_summary['zero_shift']:.3e}  "
        f"TOWARD={support_summary['toward_count']}/{support_summary['total']}  "
        f"N_eff={support_summary['eff_support']:.2f}"
    )
    print(
        f"{'wavefield':>14s}  zero={wave_summary['zero_shift']:.3e}  "
        f"TOWARD={wave_summary['toward_count']}/{wave_summary['total']}  "
        f"N_eff={wave_summary['eff_support']:.2f}"
    )

    delta_toward = wave_summary["toward_count"] - support_summary["toward_count"]
    delta_neff = wave_summary["eff_support"] - support_summary["eff_support"]

    if delta_toward <= 0 and delta_neff <= 0:
        bottleneck = "geometry-limited"
    elif delta_toward > 0 and delta_neff <= 0:
        bottleneck = "field-limited"
    else:
        bottleneck = "mixed"

    print()
    print("DISCRIMINATOR")
    print(
        f"  delta_TOWARD={delta_toward:+d}  delta_N_eff={delta_neff:+.2f}  "
        f"bottleneck={bottleneck}"
    )
    print()
    print("SAFE READ")
    print("  - The generated-family bridge remains narrow.")
    print("  - If the wavefield candidate does not improve sign counts without")
    print("    broadening support, the family is likely geometry/support-limited.")
    print("  - If sign improves at nearly fixed support, the field rule is the")
    print("    limiting factor instead.")


if __name__ == "__main__":
    main()
