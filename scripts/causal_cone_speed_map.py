#!/usr/bin/env python3
"""Cone-speed map for the causal propagating-field observable.

Question
--------
On a retained grown family, does the dynamic causal-cone observable change
smoothly with cone speed c, collapse into a few discrete proxy regimes, or
behave like a noisy non-monotone knob?

Guard rails
-----------
- exact zero-source control first
- one retained family only
- keep c as a proxy knob, not a claim about a physical wave speed
- keep the report narrow: classify the c dependence, do not broaden to a
  universal statement
"""

from __future__ import annotations

import argparse
import math
import os
import statistics
import sys
from dataclasses import dataclass


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from evolving_network_prototype_v6 import build_structured_growth, centroid_y, propagate  # noqa: E402


H = 0.5
K = 5.0
N_LAYERS = 13
HALF = 5
SEEDS = tuple(range(6))
SOURCE_LAYER = 2 * N_LAYERS // 3
SOURCE_Y0 = 0.0
SOURCE_Z0 = 3.0
FIELD_STRENGTH = 5e-5
FIELD_EPS = 0.1
C_VALUES = (0.10, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50)


@dataclass(frozen=True)
class FamilyCase:
    label: str
    drift: float
    restore: float


@dataclass(frozen=True)
class ConeSummary:
    c: float
    mean_delta: float
    se_delta: float
    ratio_mean: float
    ratio_se: float
    toward: int
    total: int


FAMILY = FamilyCase("center grown family", 0.20, 0.70)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values) / math.sqrt(len(values))


def _select_source_node(
    positions: list[tuple[float, float, float]],
    layer_nodes: list[int],
) -> int:
    return min(
        layer_nodes,
        key=lambda i: (
            (positions[i][1] - SOURCE_Y0) ** 2 + (positions[i][2] - SOURCE_Z0) ** 2,
            abs(positions[i][1] - SOURCE_Y0),
            abs(positions[i][2] - SOURCE_Z0),
            i,
        ),
    )


def _source_anchor(
    positions: list[tuple[float, float, float]],
    layers: list[list[int]],
) -> tuple[int, tuple[float, float, float]]:
    source_node = _select_source_node(positions, layers[SOURCE_LAYER])
    return source_node, positions[source_node]


def _detector_extent(
    positions: list[tuple[float, float, float]],
    det: list[int],
    anchor: tuple[float, float, float],
) -> float:
    _, sy, sz = anchor
    return max(
        math.sqrt((positions[idx][1] - sy) ** 2 + (positions[idx][2] - sz) ** 2)
        for idx in det
    )


def _instantaneous_field(
    positions: list[tuple[float, float, float]],
    anchor: tuple[float, float, float],
    strength: float,
) -> list[float]:
    if strength == 0.0:
        return [0.0] * len(positions)
    sx, sy, sz = anchor
    field = [0.0] * len(positions)
    for idx, (x, y, z) in enumerate(positions):
        r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + FIELD_EPS
        field[idx] = strength / r
    return field


def _forward_only_field(
    positions: list[tuple[float, float, float]],
    layers: list[list[int]],
    anchor: tuple[float, float, float],
    strength: float,
) -> list[float]:
    if strength == 0.0:
        return [0.0] * len(positions)
    sx, sy, sz = anchor
    field = [0.0] * len(positions)
    for layer_idx, layer_nodes in enumerate(layers):
        if layer_idx < SOURCE_LAYER:
            continue
        for idx in layer_nodes:
            x, y, z = positions[idx]
            if x + 1e-12 < sx:
                continue
            r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + FIELD_EPS
            field[idx] = strength / r
    return field


def _dynamic_field(
    positions: list[tuple[float, float, float]],
    layers: list[list[int]],
    anchor: tuple[float, float, float],
    strength: float,
    c: float,
) -> list[float]:
    if strength == 0.0:
        return [0.0] * len(positions)
    sx, sy, sz = anchor
    det_radius = _detector_extent(positions, layers[-1], anchor)
    det_x = positions[layers[-1][0]][0]
    x_span = max(det_x - sx, 1e-12)
    field = [0.0] * len(positions)
    for layer_idx, layer_nodes in enumerate(layers):
        if layer_idx < SOURCE_LAYER:
            continue
        for idx in layer_nodes:
            x, y, z = positions[idx]
            dx = x - sx
            if dx < -1e-12:
                continue
            transverse = math.sqrt((y - sy) ** 2 + (z - sz) ** 2)
            cone_radius = c * det_radius * max(dx, 0.0) / x_span
            if transverse > cone_radius + 1e-12:
                continue
            r = math.sqrt(dx * dx + (y - sy) ** 2 + (z - sz) ** 2) + FIELD_EPS
            field[idx] = strength / r
    return field


def _measure_family(field_strength: float) -> tuple[float, float, list[ConeSummary], float, float]:
    zero_max_delta = 0.0
    zero_max_field = 0.0
    inst_deltas: list[float] = []
    cone_deltas: dict[float, list[float]] = {c: [] for c in C_VALUES}

    for seed in SEEDS:
        fam = build_structured_growth(N_LAYERS, HALF, H, FAMILY.drift, FAMILY.restore, seed)
        positions, layers, adj = fam.positions, fam.layers, fam.adj
        det = layers[-1]
        _, anchor = _source_anchor(positions, layers)

        zero_field = [0.0] * len(positions)
        zero_amps = propagate(positions, layers, adj, zero_field)
        free_amps = propagate(positions, layers, adj, zero_field)
        free_centroid = centroid_y(free_amps, positions, det)
        zero_centroid = centroid_y(zero_amps, positions, det)
        zero_max_delta = max(zero_max_delta, abs(zero_centroid - free_centroid))
        zero_max_field = max(zero_max_field, max(abs(v) for v in zero_field))

        inst_field = _instantaneous_field(positions, anchor, field_strength)
        inst_amps = propagate(positions, layers, adj, inst_field)
        inst_delta = centroid_y(inst_amps, positions, det) - free_centroid
        inst_deltas.append(inst_delta)

        for c in C_VALUES:
            dyn_field = _dynamic_field(positions, layers, anchor, field_strength, c)
            dyn_amps = propagate(positions, layers, adj, dyn_field)
            dyn_delta = centroid_y(dyn_amps, positions, det) - free_centroid
            cone_deltas[c].append(dyn_delta)

    inst_mean = _mean(inst_deltas)
    summaries: list[ConeSummary] = []
    for c in C_VALUES:
        vals = cone_deltas[c]
        ratios = [dyn / inst for dyn, inst in zip(vals, inst_deltas) if abs(inst) > 1e-30]
        summaries.append(
            ConeSummary(
                c=c,
                mean_delta=_mean(vals),
                se_delta=_se(vals),
                ratio_mean=(_mean(vals) / inst_mean if abs(inst_mean) > 1e-30 else math.nan),
                ratio_se=_se(ratios),
                toward=sum(1 for v in vals if v > 0),
                total=len(vals),
            )
        )

    return zero_max_delta, zero_max_field, summaries, inst_mean, _se(inst_deltas)


def _classify(summaries: list[ConeSummary]) -> str:
    ratios = [s.ratio_mean for s in summaries]
    diffs = [b - a for a, b in zip(ratios, ratios[1:])]
    nondecreasing = all(d >= -0.03 for d in diffs)
    smoothish = max(abs(d) for d in diffs) < 0.30 if diffs else True
    distinct_regimes = len({round(r, 2) for r in ratios}) <= 4 and max(ratios) - min(ratios) > 0.20
    if nondecreasing and smoothish:
        return "smooth monotone control parameter with saturation"
    if distinct_regimes:
        return "few discrete proxy regimes"
    return "noisy / non-monotone knob"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--field-strength",
        type=float,
        default=FIELD_STRENGTH,
        help="proxy source strength used for the cone-speed sweep",
    )
    args = parser.parse_args()

    zero_delta, zero_field, summaries, inst_mean, inst_se = _measure_family(args.field_strength)
    classification = _classify(summaries)

    print("=" * 94)
    print("CAUSAL CONE SPEED MAP")
    print("  exact-null control first, then c-sweep on the center grown family")
    print("=" * 94)
    print("Question:")
    print(
        "Does the causal-field observable change smoothly with cone speed c, "
        "or does it fall into only a few proxy regimes?"
    )
    print()
    print(f"family = {FAMILY.label} (drift={FAMILY.drift:g}, restore={FAMILY.restore:g})")
    print(f"seeds = {SEEDS}, source_layer = {SOURCE_LAYER}, field_strength = {args.field_strength:.1e}")
    print(f"source anchor target = (y, z)=({SOURCE_Y0:.1f}, {SOURCE_Z0:.1f})")
    print(f"c values = {list(C_VALUES)}")
    print()
    print("ZERO-NUL CONTROL")
    print(f"  max |delta_y| = {zero_delta:.3e}")
    print(f"  max |field| = {zero_field:.3e}")
    print("  -> exact-null control survives")
    print()
    print("REFERENCE")
    print(f"  instantaneous delta = {inst_mean:+.3e} ± {inst_se:.1e}")
    print()
    print("C-SWEEP")
    print(f"{'c':>6s} {'mean delta':>14s} {'ratio/delta':>12s} {'toward':>9s}")
    print("-" * 50)
    for s in summaries:
        print(
            f"{s.c:6.2f} {s.mean_delta:+14.3e}±{s.se_delta:.1e} "
            f"{s.ratio_mean:12.3f}±{s.ratio_se:.3f} {s.toward:2d}/{s.total:<2d}"
        )
    print()
    print("CLASSIFICATION")
    print(f"  {classification}")
    print()
    print("SAFE READ")
    print("  - c is a proxy control knob for the finite-cone field.")
    print("  - exact null remains exact.")
    print("  - the retained family shows a structured c dependence, not a random one.")
    print("  - do not interpret this as a physical wave-speed claim; it is a cone-speed proxy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
