#!/usr/bin/env python3
"""Generated-family support + mass-scaling probe.

Question:
  Does the retained compact generated-family support-recovery tweak also
  restore the weak-field mass-scaling class?

Scope:
  - baseline compact generated DAG family
  - retained connectivity-side tweak: next-layer k-nearest floor augmentation
  - one self-consistent Green readout
  - one support metric: detector effective support N_eff
  - one force/mass observable: centroid shift exponent vs source strength

This stays narrow and does not retune the source kernel broadly.
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


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    adj: dict[int, list[int]]
    layers: list[list[int]]


@dataclass
class StrengthRow:
    strength: float
    delta_mean: float
    delta_se: float
    toward_count: int
    total: int
    eff_support_mean: float
    eff_support_se: float
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


def _source_resolved_case(family: Family, strength: float, gain: float) -> dict[str, float]:
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
            "zero_shift": 0.0,
        }

    free = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
    z_free = centroid_y(free, positions, det)

    field0 = [gain * v for v in _green_field(
        positions,
        mass_ids,
        [1.0 / len(mass_ids)] * len(mass_ids),
        strength,
    )]
    amps0 = propagate(positions, adj, field0, layers[0], K)
    cluster_power = [abs(amps0[i]) ** 2 for i in mass_ids]
    weights = _normalize_weights(cluster_power)
    field_sc = [gain * v for v in _green_field(positions, mass_ids, weights, strength)]
    sc_amps = propagate(positions, adj, field_sc, layers[0], K)

    det_probs = [abs(sc_amps[d]) ** 2 for d in det]
    _, eff, _, _ = _entropy_and_support(det_probs)
    delta = centroid_y(sc_amps, positions, det) - z_free
    zero_amps = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
    zero_shift = centroid_y(zero_amps, positions, det) - z_free
    return {
        "delta": delta,
        "eff_support": eff,
        "zero_shift": zero_shift,
    }


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


def _summarize_family(label: str, family_builder) -> tuple[list[StrengthRow], float]:
    families = [family_builder(seed) for seed in range(N_SEEDS)]
    ref_max = 0.0
    for fam in families:
        positions = fam.positions
        all_ys = [y for _, y, _ in positions]
        cy = sum(all_ys) / len(all_ys)
        mass_ids = _select_mass_nodes(positions, fam.layers[len(fam.layers) // 2], cy)
        ref_raw = _green_field(positions, mass_ids, [1.0 / len(mass_ids)] * len(mass_ids), max(SOURCE_STRENGTHS))
        ref_max = max(ref_max, _field_abs_max(ref_raw))
    gain = FIELD_TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0

    rows: list[StrengthRow] = []
    for strength in SOURCE_STRENGTHS:
        per_seed = [_source_resolved_case(fam, strength, gain) for fam in families]
        delta_vals = [row["delta"] for row in per_seed]
        eff_vals = [row["eff_support"] for row in per_seed]
        toward = sum(1 for d in delta_vals if d > 0)
        rows.append(
            StrengthRow(
                strength=strength,
                delta_mean=_mean(delta_vals),
                delta_se=_stdev(delta_vals) / math.sqrt(len(delta_vals)) if len(delta_vals) >= 2 else 0.0,
                toward_count=toward,
                total=len(delta_vals),
                eff_support_mean=_mean(eff_vals),
                eff_support_se=_stdev(eff_vals) / math.sqrt(len(eff_vals)) if len(eff_vals) >= 2 else 0.0,
                zero_shift_max=max(abs(row["zero_shift"]) for row in per_seed),
            )
        )
    exponent = _fit_power([row.strength for row in rows], [abs(row.delta_mean) for row in rows]) or float("nan")
    return rows, exponent


def _print_summary(label: str, rows: list[StrengthRow], exponent: float) -> None:
    print(f"{label}")
    print(f"{'s':>8s} {'delta_mean':>12s} {'sign':>8s} {'N_eff':>10s} {'zero':>10s}")
    print("-" * 56)
    for row in rows:
        sign = "TOWARD" if row.delta_mean > 0 else "AWAY"
        print(
            f"{row.strength:8.4f} {row.delta_mean:+12.6e} {sign:>8s} "
            f"{row.eff_support_mean:10.2f} {row.zero_shift_max:10.3e}"
        )
    toward_strengths = sum(1 for row in rows if row.delta_mean > 0)
    mean_eff = _mean([row.eff_support_mean for row in rows])
    print(
        f"  sign rows: {toward_strengths}/{len(rows)} TOWARD; "
        f"mean N_eff={mean_eff:.2f}; F~M exponent={exponent:.3f}"
    )
    print()


def main() -> None:
    base_rows, base_exp = _summarize_family("baseline", _family)
    tweak_rows, tweak_exp = _summarize_family("kNN floor", lambda seed: _augment_knn_floor(_family(seed)))

    baseline_zero = max(row.zero_shift_max for row in base_rows)
    tweak_zero = max(row.zero_shift_max for row in tweak_rows)

    print("=" * 100)
    print("GENERATED SUPPORT + MASS-SCALING PROBE")
    print("  compact generated DAG family, baseline vs retained kNN-floor tweak")
    print("=" * 100)
    print(
        f"family seeds={N_SEEDS}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, "
        f"connect_radius={CONNECT_RADIUS}, k_nearest={K_NEAREST}, min_edges={MIN_EDGES}"
    )
    print(f"self-consistent Green kernel: exp(-mu r)/(r+eps), mu={GREEN_MU:.2f}, eps={GREEN_EPS:.2f}")
    print(f"source strengths={SOURCE_STRENGTHS}")
    print("observables: detector sign counts, N_eff support, and centroid-shift exponent")
    print("reduction check: source strength 0 should recover free propagation exactly")
    print()

    print("ZERO-SOURCE SANITY")
    print(f"  baseline max |zero-source shift| = {baseline_zero:.3e}")
    print(f"  tweak max |zero-source shift| = {tweak_zero:.3e}")
    print()

    _print_summary("BASELINE GENERATED FAMILY", base_rows, base_exp)
    _print_summary("BASELINE + kNN FLOOR", tweak_rows, tweak_exp)

    print("SAFE READ")
    print("  The retained connectivity tweak is only interesting if it broadens support")
    print("  without losing the weak-field sign, and if the centroid-shift exponent")
    print("  stays close to linear on the same generated family.")


if __name__ == "__main__":
    main()
