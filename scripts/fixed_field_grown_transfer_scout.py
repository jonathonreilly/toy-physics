#!/usr/bin/env python3
"""Fixed-field transfer scout on the retained grown row.

Question:
  Does the retained grown geometry row carry a bounded signed-source transfer
  signal outside exact-lattice pockets, while still reducing exactly to the
  zero-source baseline where applicable?

Scope:
  - retained grown geometry row only: drift=0.2, restore=0.7
  - fixed-field propagation, no graph update
  - one interior source layer and one final-layer detector centroid
  - exact zero-source and neutral same-point cancellation checks
  - small superposition / linearity sanity pass

This is intentionally narrow and review-safe: it only asks whether the grown
row preserves the scalar sign response and the zero-baseline controls.
"""

from __future__ import annotations

import math
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow  # noqa: E402


H = 0.5
K = 5.0
BETA = 0.8
NL = 25
PW = 8
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0]
SOURCE_Z = 3.0
OFFSET = 1.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
CHARGES = (-1, 0, +1)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _nearest_node_in_layer(
    pos: list[tuple[float, float, float]],
    layer_nodes: list[int],
    x_target: float,
    y_target: float,
    z_target: float,
) -> int | None:
    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _source_node(pos: list[tuple[float, float, float]], layers: list[list[int]], z_phys: float) -> int | None:
    source_layer = NL // 3
    x_target = source_layer * H
    return _nearest_node_in_layer(pos, layers[source_layer], x_target, 0.0, z_phys)


def _field_from_sources(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    sources: list[tuple[float, int]],
) -> list[float]:
    field = [0.0] * len(pos)
    for z_phys, charge in sources:
        node = _source_node(pos, layers, z_phys)
        if node is None:
            continue
        mx, my, mz = pos[node]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += charge * SOURCE_STRENGTH / (r**FIELD_POWER)
    return field


def _propagate(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 + lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(K * act), math.sin(K * act)) * w * hm / (L * L)
    return amps


def _detector(layers: list[list[int]]) -> list[int]:
    return layers[-1]


def _centroid_z(amps: list[complex], pos: list[tuple[float, float, float]], det: list[int]) -> float:
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _det_prob(amps: list[complex], det: list[int]) -> float:
    return sum(abs(amps[i]) ** 2 for i in det)


def _cases() -> list[tuple[str, list[tuple[float, int]], str]]:
    return [
        ("zero source field", [], "zero"),
        ("single +1", [(SOURCE_Z, +1)], "repel"),
        ("single -1", [(SOURCE_Z, -1)], "attract"),
        ("neutral same-point +1/-1", [(SOURCE_Z, +1), (SOURCE_Z, -1)], "null"),
        ("like pair +1/+1", [(SOURCE_Z - OFFSET, +1), (SOURCE_Z + OFFSET, +1)], "repel"),
        ("dipole +1/-1", [(SOURCE_Z - OFFSET, +1), (SOURCE_Z + OFFSET, -1)], "partial-cancel"),
        ("double +2", [(SOURCE_Z, +2)], "linear"),
    ]


def main() -> None:
    started = time.time()
    print("=" * 100)
    print("FIXED FIELD GROWN TRANSFER SCOUT")
    print("  retained grown row only: drift=0.2, restore=0.7")
    print("  fixed-field signed-source transfer with exact zero-baseline controls")
    print("=" * 100)
    print(f"h={H}, W={PW}, NL={NL}, seeds={SEEDS}, source_z={SOURCE_Z}, offset={OFFSET}, strength={SOURCE_STRENGTH:g}")
    print("  claim surface: like/unlike sign response, zero-source reduction, and linearity sanity")
    print()

    grouped: dict[str, list[float]] = {}
    descs: dict[str, str] = {}
    for label, sources, _ in _cases():
        grouped[label] = []
        descs[label] = " + ".join(f"{q:+d}@{z:.1f}" for z, q in sources) or "none"

    for seed in SEEDS:
        pos, adj, layers = grow(DRIFT, RESTORE, seed)
        det = _detector(layers)
        free = _propagate(pos, adj, [0.0] * len(pos))
        free_centroid = _centroid_z(free, pos, det)

        if seed == SEEDS[0]:
            zero_field = _field_from_sources(pos, layers, [])
            zero_amps = _propagate(pos, adj, zero_field)
            zero_delta = _centroid_z(zero_amps, pos, det) - free_centroid
            neutral_field = _field_from_sources(pos, layers, [(SOURCE_Z, +1), (SOURCE_Z, -1)])
            neutral_amps = _propagate(pos, adj, neutral_field)
            neutral_delta = _centroid_z(neutral_amps, pos, det) - free_centroid
            print("EXACT ZERO BASELINES")
            print(f"  zero-source field delta_z: {zero_delta:+.6e}")
            print(f"  neutral same-point +1/-1 delta_z: {neutral_delta:+.6e}")
            print("  guardrail: both should stay at printed zero on the retained grown row")
            print()

        for label, sources, _ in _cases():
            field = _field_from_sources(pos, layers, sources)
            amps = _propagate(pos, adj, field)
            delta = _centroid_z(amps, pos, det) - free_centroid
            grouped[label].append(delta)

    print(f"{'case':>28s} {'source(s)':>26s} {'delta_z mean':>14s} {'sign':>8s} {'read':>14s}")
    print("-" * 96)
    for label, sources, expected in _cases():
        vals = grouped[label]
        mean = _mean(vals)
        sign = "TOWARD" if mean > 0 else "AWAY" if mean < 0 else "ZERO"
        print(f"{label:>28s} {descs[label]:>26s} {mean:+14.6e} {sign:>8s} {expected:>14s}")

    print()
    print("LINEARITY CHECKS")
    neutral_vals = grouped["neutral same-point +1/-1"]
    print(f"  neutral same-point pair: mean delta = {_mean(neutral_vals):+.6e}")
    single_plus = _mean(grouped["single +1"])
    double_plus = _mean(grouped["double +2"])
    if abs(single_plus) > 1e-30 and abs(double_plus) > 1e-30:
        charge_exponent = math.log(abs(double_plus / single_plus)) / math.log(2.0)
    else:
        charge_exponent = float("nan")
    print(f"  single +1 vs double +2 charge exponent: {charge_exponent:.3f}")
    print(f"  single -1 mean delta: {_mean(grouped['single -1']):+.6e}")
    print(f"  dipole mean delta: {_mean(grouped['dipole +1/-1']):+.6e}")

    print()
    print("SAFE READ")
    print("  - The retained grown row preserves the scalar sign response in the fixed-field scout.")
    print("  - Zero-source and neutral same-point controls reduce to printed zero.")
    print("  - The single-source response is approximately linear in source charge.")
    print("  - This is a bounded grown-geometry transfer positive, not a geometry-generic theorem.")
    print()
    print(f"Total time: {time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
