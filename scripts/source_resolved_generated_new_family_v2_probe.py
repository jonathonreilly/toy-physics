#!/usr/bin/env python3
"""Generated-family new-family v2 probe.

Question:
  Does the broader-support split-shell family recover more of the weak-field
  mass law if we remove the self-consistent source reweighting that may be
  distorting the response?

Scope:
  - retained compact bridge family as the baseline control
  - the split-shell family from the first reopening
  - static Green vs self-consistent wavefield vs fixed-weight wavefield
  - exact zero-source reduction check
  - detector effective support N_eff
  - centroid sign counts and weak-field F~M fit

The v1 split-shell probe showed that widening support by construction helps,
but the weak-field law is still weak. This v2 probe asks whether the law
improves when the wavefield update is made linear again by freezing the source
weights, rather than letting the preliminary detector response feed back into
the final field weights.
"""

from __future__ import annotations

import math
import os
import random
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts import source_resolved_generated_wavefield_bridge as bridge  # noqa: E402


N_LAYERS = 16
NODES_PER_LAYER = 30
N_SEEDS = 4
K = 5.0
TARGET_Y = 3.0
MASS_RADIUS = 2.5
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
FIELD_TARGET_MAX = 0.02

X_STEP = 0.75
BAND_CENTERS = (-7.5, 0.0, 7.5)
BAND_Z_CENTERS = (-3.5, 0.0, 3.5)
BAND_Y_JITTER = 0.85
BAND_Z_JITTER = 0.95
BAND_LAYER_Y_DRIFT = 0.12
BAND_LAYER_Z_DRIFT = 0.10
BAND_FLOOR = 7


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


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _entropy_and_support(probs: list[float]) -> tuple[float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    return h, eff


def _detector_metrics(probs: list[float]) -> tuple[float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0
    _, eff = _entropy_and_support(probs)
    return eff, total


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
    fam = bridge._family(seed)  # type: ignore[attr-defined]
    return Family(positions=fam.positions, adj=fam.adj, layers=fam.layers)


def _augment_knn_floor(family: Family) -> Family:
    augmented = bridge._augment_knn_floor(bridge.Family(family.positions, family.adj, family.layers))  # type: ignore[attr-defined]
    return Family(positions=augmented.positions, adj=augmented.adj, layers=augmented.layers)


def _split_shell_family(seed: int) -> Family:
    rng = random.Random(seed * 41 + 11)
    positions: list[tuple[float, float, float]] = []
    layers: list[list[int]] = []

    for layer in range(N_LAYERS):
        layer_nodes: list[int] = []
        x = layer * X_STEP
        for idx in range(NODES_PER_LAYER):
            band = idx % 3
            y = (
                BAND_CENTERS[band]
                + BAND_LAYER_Y_DRIFT * (layer - (N_LAYERS - 1) / 2.0)
                + rng.uniform(-BAND_Y_JITTER, BAND_Y_JITTER)
            )
            z = (
                BAND_Z_CENTERS[band]
                + BAND_LAYER_Z_DRIFT * (layer - (N_LAYERS - 1) / 2.0)
                + rng.uniform(-BAND_Z_JITTER, BAND_Z_JITTER)
            )
            positions.append((x, y, z))
            layer_nodes.append(len(positions) - 1)
        layers.append(layer_nodes)

    adj: dict[int, list[int]] = {}
    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        dst_band_ids = [
            min(range(len(BAND_CENTERS)), key=lambda b: abs(y - BAND_CENTERS[b]))
            for _, y, _ in dst_positions
        ]

        for src in layers[layer]:
            sx, sy, sz = positions[src]
            ranked: list[tuple[float, int, int]] = []
            for dst, (dx, dy, dz), band_id in zip(dst_nodes, dst_positions, dst_band_ids):
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, dst, band_id))
            ranked.sort(key=lambda item: item[0])

            selected: list[int] = []
            for band_id in range(len(BAND_CENTERS)):
                band_candidates = [item for item in ranked if item[2] == band_id]
                if band_candidates:
                    dst = min(band_candidates, key=lambda item: item[0])[1]
                    if dst not in selected:
                        selected.append(dst)

            for _, dst, _ in ranked:
                if len(selected) >= BAND_FLOOR:
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
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + bridge.GREEN_EPS  # type: ignore[attr-defined]
            val += w * strength * math.exp(-bridge.GREEN_MU * r) / r  # type: ignore[attr-defined]
        field[i] = val / len(source_pos)
    return field


def _field_abs_max(field: list[float]) -> float:
    return max(abs(v) for v in field) if field else 0.0


def _topo_parents(adj: dict[int, list[int]]) -> dict[int, list[int]]:
    parents: dict[int, list[int]] = {}
    for src, nbs in adj.items():
        for dst in nbs:
            parents.setdefault(dst, []).append(src)
    return parents


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
    parents = _topo_parents(adj)

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
        field[i] = bridge.CAUSAL_MIX * parent_mean + (1.0 - bridge.CAUSAL_MIX) * green[i]  # type: ignore[attr-defined]
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
            neighbors[i] = [j for _, j in ranked[: bridge.WAVE_NEIGHBOR_K]]  # type: ignore[attr-defined]
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
        field[i] = bridge.WAVE_BLEND * causal[i] + (1.0 - bridge.WAVE_BLEND) * neigh_mean  # type: ignore[attr-defined]
    return field


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

    free = bridge.propagate(positions, adj, [0.0] * len(positions), layers[0], K)  # type: ignore[attr-defined]
    z_free = bridge.centroid_y(free, positions, det)  # type: ignore[attr-defined]

    zero_field = [0.0] * len(positions)
    zero_amps = bridge.propagate(positions, adj, zero_field, layers[0], K)  # type: ignore[attr-defined]
    zero_shift = bridge.centroid_y(zero_amps, positions, det) - z_free  # type: ignore[attr-defined]

    rows: list[dict[str, float]] = []
    for s in SOURCE_STRENGTHS:
        base_weights = [1.0 / len(mass_ids)] * len(mass_ids)
        field0 = [gain * v for v in _green_field(positions, mass_ids, base_weights, s)]
        amps0 = bridge.propagate(positions, adj, field0, layers[0], K)  # type: ignore[attr-defined]
        cluster_power = [abs(amps0[i]) ** 2 for i in mass_ids]
        weights_sc = _normalize_weights(cluster_power)

        if mode == "static":
            field = [gain * v for v in _green_field(positions, mass_ids, base_weights, s)]
        elif mode == "wavefield":
            field = [gain * v for v in _wavefield_field(family, adj, mass_ids, weights_sc, s)]
        elif mode == "fixedwave":
            field = [gain * v for v in _wavefield_field(family, adj, mass_ids, base_weights, s)]
        else:
            raise ValueError(f"unknown mode: {mode}")

        amps = bridge.propagate(positions, adj, field, layers[0], K)  # type: ignore[attr-defined]
        delta = bridge.centroid_y(amps, positions, det) - z_free  # type: ignore[attr-defined]
        det_probs = [abs(amps[d]) ** 2 for d in det]
        eff_support, _ = _detector_metrics(det_probs)
        rows.append(
            {
                "s": s,
                "delta": delta,
                "abs_delta": abs(delta),
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
    alpha = _fit_power([r["s"] for r in rows], [r["abs_delta"] for r in rows])
    return {
        "delta_mean": _mean(deltas),
        "delta_se": _stdev(deltas) / math.sqrt(len(deltas)) if len(deltas) >= 2 else 0.0,
        "toward_count": toward,
        "total": len(deltas),
        "eff_support": _mean(effs),
        "zero_shift": abs(zero_shift),
        "alpha": alpha,
    }


def main() -> None:
    print("=" * 108)
    print("SOURCE-RESOLVED GENERATED NEW FAMILY V2 PROBE")
    print("  split-shell support family, fixed-weight wavefield law test")
    print("=" * 108)
    print(f"family seeds=0..{N_SEEDS - 1}")
    print(f"baseline family: retained compact kNN-floor bridge")
    print(
        "new family: three-band split-shell geometry "
        f"(bands={BAND_CENTERS}, floor={BAND_FLOOR})"
    )
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"field target max: {FIELD_TARGET_MAX}")
    print("modes: static Green vs self-consistent wavefield vs fixed-weight wavefield")
    print("observables: zero-source reduction, centroid sign counts, F~M exponent, detector N_eff")
    print("law-first check: compare the fixed-weight wavefield against the self-consistent one")
    print()

    per_case_results: dict[tuple[str, str], list[dict[str, float]]] = {}
    per_case_zero: dict[tuple[str, str], float] = {}

    for seed in range(N_SEEDS):
        compact = bridge._augment_knn_floor(bridge._family(seed))  # type: ignore[attr-defined]
        split_shell = _split_shell_family(seed)
        for family_label, family in [("bridge", compact), ("split", split_shell)]:
            for mode in ["static", "wavefield", "fixedwave"]:
                rows, zero_shift = _evaluate_family(family, mode)
                key = (family_label, mode)
                per_case_results.setdefault(key, []).extend(rows)
                per_case_zero[key] = max(per_case_zero.get(key, 0.0), abs(zero_shift))
                summary = _summarize(rows, zero_shift)
                alpha = summary["alpha"]
                alpha_str = f"{alpha:.3f}" if alpha is not None and math.isfinite(alpha) else "n/a"
                print(
                    f"seed={seed} {family_label:>7s}/{mode:<9s} "
                    f"zero={summary['zero_shift']:.3e} "
                    f"TOWARD={summary['toward_count']}/{summary['total']} "
                    f"F~M={alpha_str} N_eff={summary['eff_support']:.2f}"
                )

    print()
    print("SUMMARY")
    for family_label in ["bridge", "split"]:
        for mode in ["static", "wavefield", "fixedwave"]:
            key = (family_label, mode)
            rows = per_case_results[key]
            summary = _summarize(rows, per_case_zero[key])
            alpha = summary["alpha"]
            alpha_str = f"{alpha:.3f}" if alpha is not None and math.isfinite(alpha) else "n/a"
            print(
                f"{family_label:>7s}/{mode:<9s}  zero={summary['zero_shift']:.3e}  "
                f"TOWARD={summary['toward_count']}/{summary['total']}  "
                f"F~M={alpha_str}  N_eff={summary['eff_support']:.2f}"
            )

    print()
    print("LAW COMPARISON")
    split_wave = _summarize(per_case_results[("split", "wavefield")], per_case_zero[("split", "wavefield")])
    split_fixed = _summarize(per_case_results[("split", "fixedwave")], per_case_zero[("split", "fixedwave")])
    bridge_wave = _summarize(per_case_results[("bridge", "wavefield")], per_case_zero[("bridge", "wavefield")])
    bridge_alpha = bridge_wave["alpha"]
    split_wave_alpha = split_wave["alpha"]
    split_fixed_alpha = split_fixed["alpha"]
    bridge_alpha_str = f"{bridge_alpha:.3f}" if bridge_alpha is not None and math.isfinite(bridge_alpha) else "n/a"
    split_wave_alpha_str = f"{split_wave_alpha:.3f}" if split_wave_alpha is not None and math.isfinite(split_wave_alpha) else "n/a"
    split_fixed_alpha_str = f"{split_fixed_alpha:.3f}" if split_fixed_alpha is not None and math.isfinite(split_fixed_alpha) else "n/a"
    print(
        f"  bridge/wavefield  F~M={bridge_alpha_str}  N_eff={bridge_wave['eff_support']:.2f}"
    )
    print(
        f"  split/wavefield   F~M={split_wave_alpha_str}  N_eff={split_wave['eff_support']:.2f}"
    )
    print(
        f"  split/fixedwave   F~M={split_fixed_alpha_str}  N_eff={split_fixed['eff_support']:.2f}"
    )

    print()
    print("SAFE READ")
    print("  - The compact generated-family bridge remains closed as before.")
    print("  - The split-shell family still widens support by construction.")
    print("  - The new fixed-weight wavefield is the law-first test: if it improves F~M materially,")
    print("    the broader-support family is helping the weak-field law rather than just detector support.")
    print("  - If the fixed-weight wavefield does not materially beat the current wavefield, this is")
    print("    a bounded bridge/no-go for the law-improvement question on this family.")


if __name__ == "__main__":
    main()
