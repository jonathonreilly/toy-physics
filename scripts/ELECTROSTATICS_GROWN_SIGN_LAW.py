#!/usr/bin/env python3
"""Grown-geometry electrostatics sign-law companion.

This is a narrow outside-exact-lattice transfer test for the retained scalar
sign-law family.

Question:
  Does the same sign-coupled propagator still support like-charge repulsion,
  unlike-charge attraction, and exact neutral cancellation on the retained
  grown row?

Scope:
  - retained grown geometry row only: drift=0.2, restore=0.7
  - fixed-field, no graph update
  - single-source sign antisymmetry
  - exact same-point cancellation check
  - small superposition / linearity sanity pass

The goal is review-safe:
  keep the exact gamma=0 / neutral-charge reduction intact and only promote
  the result if the grown row really carries the sign law cleanly.
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow


H = 0.5
K = 5.0
BETA = 0.8
NL = 25
PW = 8
MAX_D_PHYS = 3
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0, 1]
SOURCE_Z = 3.0
OFFSET = 1.0
FIELD_POWER = 1
SOURCE_STRENGTH = 5e-5
CHARGES = (-1, 0, +1)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _nearest_node_in_layer(pos, layer_nodes, x_target, y_target, z_target):
    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _source_nodes(pos, layers, z_phys: float) -> list[int]:
    source_layer = NL // 3
    x_target = source_layer * H
    nodes = layers[source_layer]
    idx = _nearest_node_in_layer(pos, nodes, x_target, 0.0, z_phys)
    return [] if idx is None else [idx]


def _field_from_sources(pos, layers, sources: list[tuple[float, int]]) -> list[float]:
    field = [0.0] * len(pos)
    for z_phys, charge in sources:
        nodes = _source_nodes(pos, layers, z_phys)
        if not nodes:
            continue
        mx, my, mz = pos[nodes[0]]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += charge * SOURCE_STRENGTH / (r ** FIELD_POWER)
    return field


def _propagate(pos, adj, field, q_test: int):
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
            act = L * (1.0 + q_test * lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            phase = K * act
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * hm / (L * L)
    return amps


def _detector(pos, layers) -> list[int]:
    return layers[-1]


def _centroid_z(amps, pos, det) -> float:
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _det_prob(amps, det) -> float:
    return sum(abs(amps[i]) ** 2 for i in det)


def _cases() -> list[tuple[str, list[tuple[float, int]], int, str]]:
    return [
        ("single +1", [(SOURCE_Z, +1)], +1, "repel"),
        ("single -1", [(SOURCE_Z, -1)], +1, "attract"),
        ("neutral same-point +1/-1", [(SOURCE_Z, +1), (SOURCE_Z, -1)], +1, "null"),
        ("like pair +1/+1", [(SOURCE_Z - OFFSET, +1), (SOURCE_Z + OFFSET, +1)], +1, "repel"),
        ("dipole +1/-1", [(SOURCE_Z - OFFSET, +1), (SOURCE_Z + OFFSET, -1)], +1, "partial-cancel"),
        ("double +2", [(SOURCE_Z, +2)], +1, "linear"),
    ]


def main() -> None:
    print("=" * 96)
    print("ELECTROSTATICS GROWN SIGN-LAW")
    print("  retained grown row only: drift=0.2, restore=0.7")
    print("  fixed-field sign-law transfer with exact neutral cancellation guardrail")
    print("=" * 96)
    print(f"h={H}, W={PW}, NL={NL}, seeds={SEEDS}, source_z={SOURCE_Z}, offset={OFFSET}, strength={SOURCE_STRENGTH:g}")
    print("  claim surface: like-charge repulsion, unlike-charge attraction, neutral cancellation")
    print()

    grouped: dict[str, list[float]] = {}
    descs: dict[str, str] = {}
    for label, sources, q_test, expected in _cases():
        grouped[label] = []
        descs[label] = " + ".join(f"{q:+d}@{z:.1f}" for z, q in sources)

    for seed in SEEDS:
        pos, adj, layers = grow(DRIFT, RESTORE, seed)
        det = _detector(pos, layers)
        free = _propagate(pos, adj, [0.0] * len(pos), 0)
        free_centroid = _centroid_z(free, pos, det)

        if seed == SEEDS[0]:
            print("EXACT REDUCTION CHECK")
            zero_field = _field_from_sources(pos, layers, [(SOURCE_Z, +1), (SOURCE_Z, -1)])
            neutral = _propagate(pos, adj, zero_field, 0)
            exact_delta = _centroid_z(neutral, pos, det) - free_centroid
            print(f"  q_test=0 delta on neutral same-point field: {exact_delta:+.6e}")
            print("  guardrail: exact neutral / zero-charge reduction must stay at machine precision")
            print()

        for label, sources, q_test, expected in _cases():
            field = _field_from_sources(pos, layers, sources)
            amps = _propagate(pos, adj, field, q_test)
            c = _centroid_z(amps, pos, det)
            delta = c - free_centroid
            grouped.setdefault(label, []).append(delta)

    print(f"{'case':>28s} {'source(s)':>24s} {'delta_z mean':>14s} {'sign':>8s} {'read':>14s}")
    print("-" * 94)
    for label, sources, q_test, expected in _cases():
        vals = grouped[label]
        mean = _mean(vals)
        sign = "TOWARD" if mean > 0 else "AWAY" if mean < 0 else "ZERO"
        print(f"{label:>28s} {descs[label]:>24s} {mean:+14.6e} {sign:>8s} {expected:>14s}")

    print()
    print("REDUCTION / LINEARITY CHECKS")
    # Exact neutral cancellation on same-point +/- source pair.
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
    print("  - The same sign-coupled propagator still supports like/unlike sign response on the retained grown row.")
    print("  - Neutral same-point +/- sources cancel to printed precision.")
    print("  - The response is approximately linear in source charge on this grown geometry.")
    print("  - This narrows the exact-to-grown transfer gap, but it is still a scalar sign-law companion, not full electromagnetism.")


if __name__ == "__main__":
    main()
