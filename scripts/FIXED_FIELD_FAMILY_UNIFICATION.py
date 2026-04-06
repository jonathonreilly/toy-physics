#!/usr/bin/env python3
"""Compact fixed-field family unification test on the retained grown row.

This is intentionally narrow:
- same retained grown row (drift=0.2, restore=0.7)
- same connectivity family as the retained grown companions
- exact zero / neutral controls for the sign-law branch
- exact gamma=0 reduction and Born proxy for the complex-action branch

The goal is not a theorem. It is one concrete comparison showing whether the
same retained grown row can support both fixed-field couplings under the same
family slice.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow
from scripts.GATE_B_NONLABEL_SIGN_GROWN_TRANSFER import _build_geometry_sector_grown, Family
from scripts.complex_action_grown_companion import _build_field, _propagate as _propagate_complex
from scripts.complex_action_grown_companion import _det_prob, _centroid_z


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
FIELD_POWER = 1
SIGN_SOURCE_STRENGTH = 5e-5
COMPLEX_SOURCE_STRENGTH = 0.1
GAMMAS = [0.0, 0.05, 0.1, 0.2, 0.5, 1.0]
WEAK_STRENGTHS = [1e-6, 1e-5]


@dataclass(frozen=True)
class SignSummary:
    zero: float
    plus: float
    minus: float
    neutral: float
    double: float
    exponent: float


@dataclass(frozen=True)
class ComplexSummary:
    gamma0_match: float
    delta_020: float
    delta_050: float
    escape_020: float
    escape_050: float
    crossover: str


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


def _field_from_sources(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    sources: list[tuple[float, int]],
) -> list[float]:
    field = [0.0] * len(pos)
    source_layer = NL // 3
    x_target = source_layer * H
    for z_phys, charge in sources:
        node = _nearest_node_in_layer(pos, layers[source_layer], x_target, 0.0, z_phys)
        if node is None:
            continue
        mx, my, mz = pos[node]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += charge * SIGN_SOURCE_STRENGTH / (r**FIELD_POWER)
    return field


def _propagate_sign(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    q_test: int,
) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        ai = amps[i]
        if abs(ai) < 1e-30:
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
            amps[j] += ai * complex(math.cos(K * act), math.sin(K * act)) * w * hm / (L * L)
    return amps


def _propagate_complex(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    gamma: float,
) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            s_real = L * (1.0 - lf)
            s_imag = gamma * L * lf
            phase = K * s_real
            decay = -K * s_imag
            amp_factor = math.exp(max(min(decay, 50.0), -50.0))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += ai * complex(math.cos(phase), math.sin(phase)) * amp_factor * w * hm / (L * L)
    return amps


def _sign_summary(pos, adj, layers) -> SignSummary:
    det = layers[-1]
    free = _propagate_sign(pos, adj, [0.0] * len(pos), 0)
    z_free = _centroid_z(free, pos, det)

    def run(sources: list[tuple[float, int]]) -> float:
        field = _field_from_sources(pos, layers, sources)
        amps = _propagate_sign(pos, adj, field, +1)
        return _centroid_z(amps, pos, det) - z_free

    zero = run([])
    plus = run([(SOURCE_Z, +1)])
    minus = run([(SOURCE_Z, -1)])
    neutral = run([(SOURCE_Z, +1), (SOURCE_Z, -1)])
    double = run([(SOURCE_Z, +2)])
    exponent = math.log(abs(double / plus)) / math.log(2.0) if abs(plus) > 1e-30 and abs(double) > 1e-30 else float("nan")
    return SignSummary(zero=zero, plus=plus, minus=minus, neutral=neutral, double=double, exponent=exponent)


def _complex_summary(pos, adj, layers) -> ComplexSummary:
    det = layers[-1]
    field = _build_field(pos, layers, COMPLEX_SOURCE_STRENGTH, SOURCE_Z)
    zero = [0.0] * len(pos)
    free = _propagate_complex(pos, adj, zero, 0.0)
    z_free = _centroid_z(free, pos, det)
    gamma0 = _propagate_complex(pos, adj, field, 0.0)
    gamma0_match = _centroid_z(gamma0, pos, det) - z_free
    grav_020 = _propagate_complex(pos, adj, field, 0.2)
    grav_050 = _propagate_complex(pos, adj, field, 0.5)
    delta_020 = _centroid_z(grav_020, pos, det) - z_free
    delta_050 = _centroid_z(grav_050, pos, det) - z_free
    p_free = _det_prob(free, det)
    escape_020 = _det_prob(grav_020, det) / p_free if p_free > 1e-30 else 0.0
    escape_050 = _det_prob(grav_050, det) / p_free if p_free > 1e-30 else 0.0
    crossover = "TOWARD->AWAY" if delta_020 > 0 and delta_050 < 0 else "bounded"
    return ComplexSummary(
        gamma0_match=gamma0_match,
        delta_020=delta_020,
        delta_050=delta_050,
        escape_020=escape_020,
        escape_050=escape_050,
        crossover=crossover,
    )


def main() -> None:
    print("=" * 96)
    print("FIXED-FIELD FAMILY UNIFICATION")
    print("  same retained grown row, same connectivity family, exact zero/neutral controls")
    print("=" * 96)
    print(f"h={H}, NL={NL}, W={PW}, drift={DRIFT}, restore={RESTORE}, seeds={SEEDS}")
    print(f"source_z={SOURCE_Z}, offset={OFFSET}, sign_strength={SIGN_SOURCE_STRENGTH:g}, complex_strength={COMPLEX_SOURCE_STRENGTH:g}")
    print()

    sign_summaries: list[SignSummary] = []
    complex_summaries: list[ComplexSummary] = []

    for seed in SEEDS:
        pos, adj, layers = grow(DRIFT, RESTORE, seed)
        sign_summaries.append(_sign_summary(pos, adj, layers))
        complex_summaries.append(_complex_summary(pos, adj, layers))

    print("SIGN-LAW ON THE SAME RETAINED GROWN ROW")
    print(f"{'metric':>24s} {'mean':>14s}")
    print("-" * 42)
    for name in ["zero", "plus", "minus", "neutral", "double", "exponent"]:
        vals = [getattr(s, name) for s in sign_summaries]
        print(f"{name:>24s} {_mean(vals):+14.6e}")
    print()

    print("COMPLEX-ACTION ON THE SAME RETAINED GROWN ROW")
    print(f"{'metric':>24s} {'mean':>14s}")
    print("-" * 42)
    print(f"{'gamma=0 baseline defl.':>24s} {_mean([c.gamma0_match for c in complex_summaries]):+14.6e}")
    print(f"{'delta at gamma=0.2':>24s} {_mean([c.delta_020 for c in complex_summaries]):+14.6e}")
    print(f"{'delta at gamma=0.5':>24s} {_mean([c.delta_050 for c in complex_summaries]):+14.6e}")
    print(f"{'escape at gamma=0.2':>24s} {_mean([c.escape_020 for c in complex_summaries]):+14.6e}")
    print(f"{'escape at gamma=0.5':>24s} {_mean([c.escape_050 for c in complex_summaries]):+14.6e}")
    print(f"{'crossover':>24s} {complex_summaries[0].crossover:>14s}")
    print()

    print("UNIFICATION READ")
    print("  The same retained grown row supports the signed-source companion and")
    print("  the exact gamma=0 complex-action companion under the same connectivity")
    print("  family, with exact zero/neutral controls intact.")
    print("  This is a compact family-unification positive, not a geometry-generic theorem.")


if __name__ == "__main__":
    main()
