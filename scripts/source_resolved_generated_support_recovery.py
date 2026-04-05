#!/usr/bin/env python3
"""Generated-family support recovery probe.

Question:
  Can one simple connectivity-side modification partially recover broad
  downstream detector support on the compact generated DAG family?

Scope:
  - baseline compact generated DAG family
  - one connectivity tweak: k-nearest floor augmentation on next-layer edges
  - one retained observable: detector support localization
  - one retained observable: detector centroid sign relative to free propagation

This is deliberately narrow. It does not retune the source kernel broadly and
does not introduce a new field architecture.
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

K_NEAREST = 3
MIN_EDGES = 5


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    adj: dict[int, list[int]]
    layers: list[list[int]]


@dataclass
class Row:
    label: str
    delta_mean: float
    delta_se: float
    toward_count: int
    total: int
    eff_support: float
    eff_support_se: float
    eff_frac: float
    top10_frac: float
    support_frac: float
    max_prob_share: float
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


def _support_case(family: Family) -> dict[str, float]:
    positions = family.positions
    adj = family.adj
    layers = family.layers
    det = layers[-1]
    all_ys = [y for _, y, _ in positions]
    cy = sum(all_ys) / len(all_ys)
    mass_ids = _select_mass_nodes(positions, layers[len(layers) // 2], cy)
    if not mass_ids:
        return {
            "delta": 0.0,
            "eff_support": 0.0,
            "eff_frac": 0.0,
            "top10_frac": 0.0,
            "support_frac": 0.0,
            "max_prob_share": 0.0,
            "zero_shift": 0.0,
        }

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
    h, eff, top10, support_frac = _entropy_and_support(det_probs)
    delta = centroid_y(sc_amps, positions, det) - z_free
    zero_field = [0.0] * len(positions)
    zero_amps = propagate(positions, adj, zero_field, layers[0], K)
    zero_shift = centroid_y(zero_amps, positions, det) - z_free
    return {
        "delta": delta,
        "eff_support": eff,
        "eff_frac": eff / len(det_probs) if det_probs else 0.0,
        "top10_frac": top10,
        "support_frac": support_frac,
        "max_prob_share": max(det_probs) / sum(det_probs) if sum(det_probs) > 1e-30 else 0.0,
        "zero_shift": zero_shift,
    }


def _aggregate(label: str, rows: list[dict[str, float]]) -> Row:
    delta_vals = [r["delta"] for r in rows]
    eff_vals = [r["eff_support"] for r in rows]
    toward = sum(1 for d in delta_vals if d > 0)
    return Row(
        label=label,
        delta_mean=_mean(delta_vals),
        delta_se=_stdev(delta_vals) / math.sqrt(len(delta_vals)) if len(delta_vals) >= 2 else 0.0,
        toward_count=toward,
        total=len(delta_vals),
        eff_support=_mean(eff_vals),
        eff_support_se=_stdev(eff_vals) / math.sqrt(len(eff_vals)) if len(eff_vals) >= 2 else 0.0,
        eff_frac=_mean([r["eff_frac"] for r in rows]),
        top10_frac=_mean([r["top10_frac"] for r in rows]),
        support_frac=_mean([r["support_frac"] for r in rows]),
        max_prob_share=_mean([r["max_prob_share"] for r in rows]),
        zero_shift_max=max(abs(r["zero_shift"]) for r in rows),
    )


def main() -> None:
    baseline_rows: list[dict[str, float]] = []
    tweaked_rows: list[dict[str, float]] = []

    print("=" * 100)
    print("GENERATED SUPPORT RECOVERY PROBE")
    print("  compact generated DAG family, baseline vs one connectivity-side tweak")
    print("=" * 100)
    print(
        f"family seeds={N_SEEDS}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, "
        f"connect_radius={CONNECT_RADIUS}, k_nearest={K_NEAREST}, min_edges={MIN_EDGES}"
    )
    print(
        f"self-consistent Green kernel: exp(-mu r)/(r+eps), mu={GREEN_MU:.2f}, "
        f"eps={GREEN_EPS:.2f}, field target max={FIELD_TARGET_MAX:.3f}"
    )
    print(f"source strength={SOURCE_STRENGTH:g}")
    print("observables: detector support localization + centroid sign only")
    print("reduction check: zero source should recover free propagation exactly")
    print()

    for seed in range(N_SEEDS):
        base = _family(seed)
        tweak = _augment_knn_floor(base)
        baseline_rows.append(_support_case(base))
        tweaked_rows.append(_support_case(tweak))

    base = _aggregate("baseline generated family", baseline_rows)
    tweak = _aggregate("baseline + kNN floor", tweaked_rows)

    print("ZERO-SOURCE SANITY")
    print(f"  baseline max |zero-source shift| = {base.zero_shift_max:.3e}")
    print(f"  tweak max |zero-source shift| = {tweak.zero_shift_max:.3e}")
    print()

    print(
        f"{'case':<24} {'delta':>12} {'sign':>8} {'N_eff':>10} {'N_eff/N':>9} "
        f"{'top10':>9} {'support':>9} {'peak':>9}"
    )
    print("-" * 100)
    for row in [base, tweak]:
        sign = "TOWARD" if row.delta_mean > 0 else "AWAY" if row.delta_mean < 0 else "ZERO"
        print(
            f"{row.label:<24} {row.delta_mean:+12.6e} {sign:>8} "
            f"{row.eff_support:10.2f} {row.eff_frac:9.3f} {row.top10_frac:9.3f} "
            f"{row.support_frac:9.3f} {row.max_prob_share:9.3f}"
        )

    print()
    print("SIGN COUNTS")
    print(f"  baseline: {base.toward_count}/{base.total} TOWARD")
    print(f"  tweak:    {tweak.toward_count}/{tweak.total} TOWARD")
    print()
    print("SAFE READ")
    print(
        "  The connectivity tweak is only interesting if it broadens detector support "
        "without flipping the centroid sign against the retained weak-field direction."
    )
    print(
        "  If support improves but sign stays AWAY, that is still a useful bounded "
        "negative: connectivity helps breadth, but not the generated-family gravity lane."
    )


if __name__ == "__main__":
    main()
