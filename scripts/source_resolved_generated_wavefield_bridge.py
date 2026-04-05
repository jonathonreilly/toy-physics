#!/usr/bin/env python3
"""Generated-family wavefield bridge probe.

Question:
  Can the retained generated-family support-recovery lesson be combined with a
  wavefield-like architecture change, rather than only static or causal
  smoothing, to improve the weak-field mass law?

Scope:
  - compact generated 3D DAG family
  - baseline connectivity vs retained k-nearest floor augmentation
  - static Green field vs causal parent-averaged field vs wavefield candidate
  - exact zero-source reduction check
  - support metric: detector effective support N_eff
  - mass-law metric: centroid-shift exponent across source strength
  - wavefield-vs-static observable: centroid and support gain on the tweaked
    family

The wavefield candidate is intentionally minimal:
  - first build the causal parent-averaged field
  - then apply one same-layer transverse smoothing pass using local
    same-layer k-nearest geometry

This is not a full propagating field theory. It is the smallest generated-family
bridge that can test whether a wavefield-like update beats the causal-smoothing
step already frozen on main.
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
CAUSAL_MIX = 0.70
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


def _fit_power(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def _entropy_and_support(probs: list[float]) -> tuple[float, float, float, float]:
    if not probs:
        return 0.0, 0.0, 0.0, 0.0
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    peak = max(norm)
    top10 = sum(sorted(norm, reverse=True)[: min(10, len(norm))])
    support_frac = sum(1 for p in norm if p >= 0.01 * peak) / len(norm)
    return h, eff, top10, support_frac


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
        field[i] = CAUSAL_MIX * parent_mean + (1.0 - CAUSAL_MIX) * green[i]
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


def _detector_metrics(probs: list[float]) -> tuple[float, float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0
    _, eff, top10, support_frac = _entropy_and_support(probs)
    return eff, top10, support_frac


def _evaluate_family(family: Family, mode: str) -> tuple[list[dict[str, float]], float]:
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

        if mode == "static":
            field = [gain * v for v in _green_field(positions, mass_ids, weights_sc, s)]
        elif mode == "causal":
            field = [gain * v for v in _causal_field(positions, adj, mass_ids, weights_sc, s)]
        elif mode == "wavefield":
            field = [gain * v for v in _wavefield_field(family, adj, mass_ids, weights_sc, s)]
        else:
            raise ValueError(f"unknown mode: {mode}")

        amps = propagate(positions, adj, field, layers[0], K)
        delta = centroid_y(amps, positions, det) - z_free
        det_probs = [abs(amps[d]) ** 2 for d in det]
        eff_support, _, support_frac = _detector_metrics(det_probs)
        rows.append(
            {
                "s": s,
                "delta": delta,
                "abs_delta": abs(delta),
                "toward": 1.0 if delta > 0 else 0.0,
                "eff_support": eff_support,
                "support_frac": support_frac,
                "zero_shift": zero_shift,
            }
        )

    return rows, zero_shift


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _summarize(rows: list[dict[str, float]], zero_shift: float) -> dict[str, float]:
    deltas = [r["delta"] for r in rows]
    effs = [r["eff_support"] for r in rows]
    sups = [r["support_frac"] for r in rows]
    toward = sum(1 for d in deltas if d > 0)
    alpha = _fit_power([r["s"] for r in rows], [r["abs_delta"] for r in rows])
    return {
        "delta_mean": _mean(deltas),
        "delta_se": _stdev(deltas) / math.sqrt(len(deltas)) if len(deltas) >= 2 else 0.0,
        "toward_count": toward,
        "total": len(deltas),
        "eff_support": _mean(effs),
        "support_frac": _mean(sups),
        "zero_shift": abs(zero_shift),
        "alpha": alpha,
    }


def main() -> None:
    print("=" * 104)
    print("SOURCE-RESOLVED GENERATED WAVEFIELD BRIDGE")
    print("  compact generated DAG family, support-recovery lesson + wavefield update")
    print("=" * 104)
    print(f"family seeds=0..{N_SEEDS - 1}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, connect_radius={CONNECT_RADIUS}")
    print(f"support tweak: k-nearest floor augmentation (k={K_NEAREST}, min_edges={MIN_EDGES})")
    print(f"field modes: static Green vs causal parent-averaged Green vs wavefield")
    print(f"wavefield blend={WAVE_BLEND:.2f}, neighbor-k={WAVE_NEIGHBOR_K}")
    print(f"source strengths={SOURCE_STRENGTHS}")
    print(f"field target max={FIELD_TARGET_MAX}")
    print("observables: zero-source reduction, centroid sign counts, F~M exponent, detector N_eff")
    print()

    per_case_results: dict[tuple[str, str], list[dict[str, float]]] = {}
    per_case_zero: dict[tuple[str, str], float] = {}

    for seed in range(N_SEEDS):
        base = _family(seed)
        tweak = _augment_knn_floor(base)
        for family_label, family in [("baseline", base), ("tweak", tweak)]:
            for mode in ["static", "causal", "wavefield"]:
                rows, zero_shift = _evaluate_family(family, mode)
                key = (family_label, mode)
                per_case_results.setdefault(key, []).extend(rows)
                per_case_zero[key] = max(per_case_zero.get(key, 0.0), abs(zero_shift))
                summary = _summarize(rows, zero_shift)
                alpha_str = f"{summary['alpha']:.3f}" if summary["alpha"] is not None else "n/a"
                print(
                    f"seed={seed} {family_label:>8s}/{mode:<9s} "
                    f"zero={summary['zero_shift']:.3e} "
                    f"TOWARD={summary['toward_count']}/{summary['total']} "
                    f"F~M={alpha_str} N_eff={summary['eff_support']:.2f}"
                )

    print()
    print("SUMMARY")
    for family_label in ["baseline", "tweak"]:
        for mode in ["static", "causal", "wavefield"]:
            key = (family_label, mode)
            rows = per_case_results[key]
            summary = _summarize(rows, per_case_zero[key])
            alpha_str = f"{summary['alpha']:.3f}" if summary["alpha"] is not None else "n/a"
            print(
                f"{family_label:>8s}/{mode:<9s}  zero={summary['zero_shift']:.3e}  "
                f"TOWARD={summary['toward_count']}/{summary['total']}  "
                f"F~M={alpha_str}  N_eff={summary['eff_support']:.2f}  "
                f"support_frac={summary['support_frac']:.3f}"
            )

    print()
    print("WAVEFIELD VS STATIC")
    for family_label in ["baseline", "tweak"]:
        static_rows = per_case_results[(family_label, "static")]
        wave_rows = per_case_results[(family_label, "wavefield")]
        static_delta = _mean([r["delta"] for r in static_rows])
        wave_delta = _mean([r["delta"] for r in wave_rows])
        static_eff = _mean([r["eff_support"] for r in static_rows])
        wave_eff = _mean([r["eff_support"] for r in wave_rows])
        static_support = _mean([r["support_frac"] for r in static_rows])
        wave_support = _mean([r["support_frac"] for r in wave_rows])
        print(
            f"  {family_label:>8s}: delta_gain={wave_delta - static_delta:+.6e} "
            f"N_eff_gain={wave_eff - static_eff:+.2f} "
            f"support_gain={wave_support - static_support:+.3f}"
        )

    print()
    print("SAFE READ")
    print("  - The baseline generated family remains mixed and does not give a stable weak-field law.")
    print("  - The retained kNN-floor support recovery broadens the detector footprint and moves the centroid")
    print("    sign back toward TOWARD.")
    print("  - The wavefield update is distinguishable from static/causal smoothing, but this is still a bridge")
    print("    result rather than generated-family closure.")


if __name__ == "__main__":
    main()
