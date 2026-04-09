#!/usr/bin/env python3
"""Split probe for why exact Green pockets survive while generated geometry fails.

This is intentionally narrow:
  - exact lattice: compare clipped vs interior source placement
  - generated DAG family: compare the same self-consistent Green architecture
  - single mechanistic culprit: detector support localization

The question is whether the generated-family failure is mainly explained by
downstream support collapse / concentration rather than the exact pocket's
source-cluster boundary clipping.
"""

from __future__ import annotations

import math
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402
from scripts.causal_field_gravity import centroid_y, generate_3d_dag, propagate  # noqa: E402


H = 0.25
NL_PHYS = 6
PW = 3
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
SOURCE_STRENGTH = 0.004
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08

GEN_N_LAYERS = 16
GEN_NODES_PER_LAYER = 24
GEN_Y_RANGE = 10.0
GEN_CONNECT_RADIUS = 3.2
GEN_N_SEEDS = 4
GEN_K = 5.0
GEN_TARGET_Y = 3.0
GEN_MASS_RADIUS = 2.5


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _stdev(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) >= 2 else math.nan


def _source_cluster_nodes(lat: m.Lattice3D, source_z: float) -> list[int]:
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(source_z / lat.h)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw:
            nodes.append(lat.nmap[(gl, y - lat.hw, z - lat.hw)])
    return nodes


def _green_field_exact(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    weights: list[float],
) -> list[list[float]]:
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    if not source_nodes:
        return field
    source_pos = [lat.pos[i] for i in source_nodes]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for w, (mx, my, mz) in zip(weights, source_pos):
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
                val += w * source_strength * math.exp(-GREEN_MU * r) / r
            field[layer][i] = val
    return field


def _field_abs_max_exact(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row)


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


def _detector_probs_exact(amps: list[complex], lat: m.Lattice3D) -> list[float]:
    det_start = lat.layer_start[lat.nl - 1]
    det_nodes = range(det_start, det_start + lat.npl)
    return [abs(amps[d]) ** 2 for d in det_nodes]


def _source_resolved_green_exact_case(source_z: float) -> dict[str, float]:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat, source_z)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    ref_raw = _green_field_exact(lat, SOURCE_STRENGTH, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes))
    gain = FIELD_TARGET_MAX / _field_abs_max_exact(ref_raw) if _field_abs_max_exact(ref_raw) > 1e-30 else 1.0

    green0 = [[gain * v for v in row] for row in _green_field_exact(
        lat, SOURCE_STRENGTH, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes)
    )]
    amps0 = lat.propagate(green0, m.K)
    cluster_power = [abs(amps0[i]) ** 2 for i in source_nodes]
    weights_sc = _normalize_weights(cluster_power)
    green_field = [[gain * v for v in row] for row in _green_field_exact(lat, SOURCE_STRENGTH, source_nodes, weights_sc)]
    green_amps = lat.propagate(green_field, m.K)

    det_probs = _detector_probs_exact(green_amps, lat)
    h, eff, top10, support_frac = _entropy_and_support(det_probs)
    delta = m._centroid_z(green_amps, lat) - z_free
    return {
        "source_nodes": float(len(source_nodes)),
        "delta": delta,
        "entropy": h,
        "eff_support": eff,
        "eff_frac": eff / len(det_probs) if det_probs else 0.0,
        "top10_frac": top10,
        "support_frac": support_frac,
        "max_prob_share": max(det_probs) / sum(det_probs) if sum(det_probs) > 1e-30 else 0.0,
    }


def _gen_green_case(seed: int) -> dict[str, float]:
    positions, adj, layers = generate_3d_dag(
        n_layers=GEN_N_LAYERS,
        nodes_per_layer=GEN_NODES_PER_LAYER,
        yz_range=GEN_Y_RANGE,
        connect_radius=GEN_CONNECT_RADIUS,
        rng_seed=seed * 19 + 7,
    )
    det = layers[-1]
    all_ys = [y for _, y, _ in positions]
    cy = sum(all_ys) / len(all_ys)
    mass_ids = [
        idx for idx in sorted(
            layers[len(layers) // 2],
            key=lambda i: ((positions[i][1] - (cy + GEN_TARGET_Y)) ** 2 + positions[i][2] ** 2, abs(positions[i][1] - (cy + GEN_TARGET_Y))),
        )
        if abs(positions[idx][1] - (cy + GEN_TARGET_Y)) <= GEN_MASS_RADIUS
    ]
    if len(mass_ids) < 4:
        mass_ids = sorted(
            layers[len(layers) // 2],
            key=lambda i: ((positions[i][1] - (cy + GEN_TARGET_Y)) ** 2 + positions[i][2] ** 2, abs(positions[i][1] - (cy + GEN_TARGET_Y))),
        )[:4]
    if not mass_ids:
        return {"delta": 0.0, "entropy": 0.0, "eff_support": 0.0, "eff_frac": 0.0, "top10_frac": 0.0, "support_frac": 0.0, "max_prob_share": 0.0}

    ref_raw = _green_field_gen(positions, mass_ids, [1.0 / len(mass_ids)] * len(mass_ids), SOURCE_STRENGTH)
    gain = FIELD_TARGET_MAX / _field_abs_max_gen(ref_raw) if _field_abs_max_gen(ref_raw) > 1e-30 else 1.0

    weights = [1.0 / len(mass_ids)] * len(mass_ids)
    field0 = [gain * v for v in _green_field_gen(positions, mass_ids, weights, SOURCE_STRENGTH)]
    amps0 = propagate(positions, adj, field0, layers[0], GEN_K)
    power = [abs(amps0[i]) ** 2 for i in mass_ids]
    weights2 = _normalize_weights(power)
    field_sc = [gain * v for v in _green_field_gen(positions, mass_ids, weights2, SOURCE_STRENGTH)]
    sc_amps = propagate(positions, adj, field_sc, layers[0], GEN_K)

    det_probs = [abs(sc_amps[d]) ** 2 for d in det]
    h, eff, top10, support_frac = _entropy_and_support(det_probs)
    free = propagate(positions, adj, [0.0] * len(positions), layers[0], GEN_K)
    delta = centroid_y(sc_amps, positions, det) - centroid_y(free, positions, det)
    return {
        "delta": delta,
        "entropy": h,
        "eff_support": eff,
        "eff_frac": eff / len(det_probs) if det_probs else 0.0,
        "top10_frac": top10,
        "support_frac": support_frac,
        "max_prob_share": max(det_probs) / sum(det_probs) if sum(det_probs) > 1e-30 else 0.0,
    }


def _green_field_gen(
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


def _field_abs_max_gen(field: list[float]) -> float:
    return max(abs(v) for v in field) if field else 0.0


def _gen_case_mean(n_seeds: int = GEN_N_SEEDS) -> dict[str, float]:
    rows = [_gen_green_case(seed) for seed in range(n_seeds)]
    keys = [k for k in rows[0].keys()]
    out: dict[str, float] = {}
    for key in keys:
        vals = [row[key] for row in rows]
        out[key] = _mean(vals)
        out[f"{key}_se"] = _stdev(vals) / math.sqrt(len(vals)) if len(vals) >= 2 else 0.0
    return out


def _print_row(label: str, row: dict[str, float], source_nodes: str) -> None:
    print(
        f"{label:<16s} {source_nodes:>5s} "
        f"{row['delta']:+11.6e} {row['eff_support']:11.2f} {row['eff_frac']:9.3f} "
        f"{row['top10_frac']:10.3f} {row['support_frac']:10.3f} {row['max_prob_share']:10.3f}"
    )


def main() -> None:
    clipped = _source_resolved_green_exact_case(3.0)
    centered = _source_resolved_green_exact_case(2.5)
    generated = _gen_case_mean()

    print("=" * 100)
    print("SOURCE-RESOLVED SUPPORT LOCALIZATION SPLIT PROBE")
    print("  exact clipped vs exact interior vs generated-family self-consistent Green pocket")
    print("  mechanistic culprit under test: detector support localization")
    print("=" * 100)
    print(f"exact lattice: h={H}, W={PW}, L={NL_PHYS}, source_strength={SOURCE_STRENGTH:g}")
    print(
        f"generated family: seeds={GEN_N_SEEDS}, layers={GEN_N_LAYERS}, nodes/layer={GEN_NODES_PER_LAYER}, "
        f"connect_radius={GEN_CONNECT_RADIUS}"
    )
    print("support metrics: detector entropy -> effective support / fraction, top-10 fraction, 1% peak support fraction")
    print()
    print(
        f"{'case':<16s} {'srcN':>5s} {'delta':>11s} {'N_eff':>11s} {'N_eff/N':>9s} "
        f"{'top10':>10s} {'supp1%':>10s} {'peak':>10s}"
    )
    print("-" * 100)
    _print_row("exact-clipped", clipped, f"{int(clipped['source_nodes']):d}")
    _print_row("exact-centered", centered, f"{int(centered['source_nodes']):d}")
    _print_row("generated-mean", generated, "4")
    print()
    print("SAFE READ")
    print("  - exact clipped and exact interior are compared explicitly, so clipping alone can be tested")
    print("  - if the exact rows stay broad while generated collapses, the culprit is detector/connectivity localization")
    print("  - if the rows are similar, support localization is not the main explanation")


if __name__ == "__main__":
    main()
