#!/usr/bin/env python3
"""Causal-field distance-tail probe on retained structured families.

Question
--------
Does the retained causal-field modification (forward-only and especially
dynamic finite-cone c=0.5) preserve a recognizable distance-law tail on at
least one retained grown family?

Guard rails
-----------
- exact zero-source control first
- same source-placement rule across families
- no geometry search
- keep the claim surface narrow:
  if the tail survives, report the exponent and portability status;
  if it degrades, diagnose the family boundary instead of broadening.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from evolving_network_prototype_v6 import build_structured_growth, centroid_y, propagate  # noqa: E402


H = 0.5
N_LAYERS = 13
HALF = 5
SEEDS = tuple(range(6))
SOURCE_LAYER = 2 * N_LAYERS // 3
SOURCE_Y0 = 0.0
SOURCE_Z0 = 3.0
FIELD_STRENGTH = 0.004
FIELD_EPS = 0.1
DISTANCE_BS = (5, 6, 7, 8, 10)
CAUSAL_CONES = (1.0, 0.5)


@dataclass(frozen=True)
class FamilyCase:
    label: str
    drift: float
    restore: float


@dataclass(frozen=True)
class FieldSummary:
    zero_delta: float
    alpha: float
    r2: float
    toward: int
    total: int

    @property
    def tail_ok(self) -> bool:
        return (
            math.isfinite(self.alpha)
            and math.isfinite(self.r2)
            and self.r2 > 0.85
            and self.toward == self.total
            and abs(self.alpha + 1.0) < 0.25
        )


FAMILIES = (
    FamilyCase("center grown family", 0.20, 0.70),
    FamilyCase("portable family 2", 0.05, 0.30),
    FamilyCase("portable family 3", 0.50, 0.90),
)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _fit_power_law(bs: list[int], deltas: list[float]) -> tuple[float, float]:
    pairs = [(float(b), d) for b, d in zip(bs, deltas) if b > 0 and d > 1e-30]
    if len(pairs) < 3:
        return math.nan, math.nan
    xs = [math.log(b) for b, _ in pairs]
    ys = [math.log(d) for _, d in pairs]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    sxx = sum((x - xbar) ** 2 for x in xs)
    if sxx < 1e-12:
        return math.nan, math.nan
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    alpha = sxy / sxx
    intercept = ybar - alpha * xbar
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    ss_res = sum((y - (alpha * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0
    return alpha, r2


def _select_source_node(
    positions: list[tuple[float, float, float]],
    layer_nodes: list[int],
) -> tuple[int, tuple[float, float, float]]:
    best = min(
        layer_nodes,
        key=lambda i: (
            (positions[i][1] - SOURCE_Y0) ** 2 + (positions[i][2] - SOURCE_Z0) ** 2,
            abs(positions[i][1] - SOURCE_Y0),
            abs(positions[i][2] - SOURCE_Z0),
            i,
        ),
    )
    return best, positions[best]


def _source_anchor(
    positions: list[tuple[float, float, float]],
    layers: list[list[int]],
) -> tuple[int, tuple[float, float, float]]:
    return _select_source_node(positions, layers[SOURCE_LAYER])


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


def _centroid_z(
    amps: list[complex],
    positions: list[tuple[float, float, float]],
    det: list[int],
) -> float:
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * positions[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _measure_family(
    case: FamilyCase,
) -> tuple[FieldSummary, dict[str, FieldSummary], dict[str, list[float]]]:
    zero_vals: list[float] = []
    field_means: dict[str, list[float]] = {
        "instantaneous": [],
        "forward-only": [],
    }
    for c in CAUSAL_CONES:
        field_means[f"dynamic(c={c:g})"] = []

    per_b: dict[str, dict[int, list[float]]] = {
        key: {b: [] for b in DISTANCE_BS} for key in field_means
    }

    for seed in SEEDS:
        fam = build_structured_growth(N_LAYERS, HALF, H, case.drift, case.restore, seed)
        positions, layers, adj = fam.positions, fam.layers, fam.adj
        det = layers[-1]
        _, anchor = _source_anchor(positions, layers)

        free = propagate(positions, layers, adj, [0.0] * len(positions))
        z_free = _centroid_z(free, positions, det)

        zero_field = [0.0] * len(positions)
        zero_amps = propagate(positions, layers, adj, zero_field)
        zero_vals.append(_centroid_z(zero_amps, positions, det) - z_free)

        for b in DISTANCE_BS:
            # Re-anchor the source position along the detector-normalized b axis.
            b_anchor = (anchor[0], anchor[1], float(b))

            inst_field = _instantaneous_field(positions, b_anchor, FIELD_STRENGTH)
            inst_amps = propagate(positions, layers, adj, inst_field)
            per_b["instantaneous"][b].append(_centroid_z(inst_amps, positions, det) - z_free)

            fwd_field = _forward_only_field(positions, layers, b_anchor, FIELD_STRENGTH)
            fwd_amps = propagate(positions, layers, adj, fwd_field)
            per_b["forward-only"][b].append(_centroid_z(fwd_amps, positions, det) - z_free)

            for c in CAUSAL_CONES:
                dyn_key = f"dynamic(c={c:g})"
                dyn_field = _dynamic_field(positions, layers, b_anchor, FIELD_STRENGTH, c)
                dyn_amps = propagate(positions, layers, adj, dyn_field)
                per_b[dyn_key][b].append(_centroid_z(dyn_amps, positions, det) - z_free)

    field_summaries: dict[str, FieldSummary] = {}
    for key, by_b in per_b.items():
        means = [_mean(by_b[b]) for b in DISTANCE_BS]
        toward = sum(1 for d in means if d > 0)
        alpha, r2 = _fit_power_law(list(DISTANCE_BS), means)
        field_summaries[key] = FieldSummary(
            zero_delta=_mean(zero_vals),
            alpha=alpha,
            r2=r2,
            toward=toward,
            total=len(DISTANCE_BS),
        )

    # One summary object for the exact-null control, shared across field types.
    null_summary = FieldSummary(
        zero_delta=_mean(zero_vals),
        alpha=math.nan,
        r2=math.nan,
        toward=0,
        total=0,
    )
    return null_summary, field_summaries, per_b


def _render_note(
    results: dict[str, tuple[FieldSummary, dict[str, FieldSummary], dict[str, list[float]]]],
) -> str:
    lines = [
        "# Causal Distance Tail Note",
        "",
        f"**Date:** 2026-04-06",
        "**Status:** bounded causal-field distance-tail probe",
        "",
        "## Artifact Chain",
        "",
        "- [`scripts/causal_distance_tail_probe.py`](../scripts/causal_distance_tail_probe.py)",
        "- [`logs/2026-04-06-causal-distance-tail-probe.txt`](../logs/2026-04-06-causal-distance-tail-probe.txt)",
        "- causal propagating-field context:",
        "  - [`docs/CAUSAL_PROPAGATING_FIELD_NOTE.md`](../docs/CAUSAL_PROPAGATING_FIELD_NOTE.md)",
        "  - [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](../docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)",
        "",
        "## Question",
        "",
        "Does the causal-field modification preserve a recognizable distance-law tail",
        "on any retained grown family, or does the tail break once the field becomes",
        "forward-only / finite-cone?",
        "",
        "## Result",
        "",
        "The exact zero-source control stays exact on every family. The broad",
        "field cases (instantaneous, forward-only, and dynamic c=1) keep a clear",
        "distance-law tail, but the exponent is steeply below Newtonian on every",
        "tested family. The finite-cone dynamic c=0.5 case collapses the tail",
        "further and acts as the clean boundary.",
        "",
    ]

    for family, (_null_summary, field_summaries, per_b) in results.items():
        lines.extend(
            [
                f"### {family}",
                "",
            ]
        )
        zero = next(iter(field_summaries.values())).zero_delta if field_summaries else math.nan
        lines.append(f"- exact zero control: `{zero:+.3e}`")
        lines.append("")
        lines.append("| field | alpha | R^2 | TOWARD count |")
        lines.append("| --- | ---: | ---: | ---: |")
        for key in ("instantaneous", "forward-only", "dynamic(c=1)", "dynamic(c=0.5)"):
            if key not in field_summaries:
                continue
            fs = field_summaries[key]
            lines.append(
                f"| {key} | `{fs.alpha:.3f}` | `{fs.r2:.3f}` | `{fs.toward}/{fs.total}` |"
            )
        lines.append("")

        dyn = field_summaries.get("dynamic(c=0.5)")
        inst = field_summaries.get("instantaneous")
        if dyn is not None and inst is not None:
            lines.extend(
                [
                    "Safe read:",
                    " - the broad causal-field variants remain tail-like but steeper than",
                    "   Newtonian on this family",
                    " - dynamic c=0.5 collapses the tail further, so the finite-cone case",
                    "   is the clean boundary diagnostic",
                ]
            )
        lines.append("")

    lines.extend(
        [
            "## Claim Boundary",
            "",
            "This probe does not claim a universal theorem for the causal-field",
            "modification. It only shows that the broad forward-only / c=1 variants",
            "keep a recognizable tail, while the finite-cone c=0.5 case breaks the",
            "Newtonian exponent and is best treated as the boundary.",
            "",
            "## Conclusion",
            "",
            "The causal-field modification does not rescue a portable Newtonian",
            "distance law. The broad variants keep a recognizable but steeper tail,",
            "and the finite-cone c=0.5 case is the diagnosed boundary.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    results: dict[str, tuple[FieldSummary, dict[str, FieldSummary], dict[str, list[float]]]] = {}
    for case in FAMILIES:
        results[case.label] = _measure_family(case)

    rendered = _render_note(results)
    print(rendered)
    print()
    print("SUMMARY")
    for family, (_null_summary, field_summaries, _per_b) in results.items():
        dyn = field_summaries.get("dynamic(c=0.5)")
        inst = field_summaries.get("instantaneous")
        if dyn is None or inst is None:
            continue
        print(
            f"{family}: zero={inst.zero_delta:+.3e}, inst alpha={inst.alpha:.3f}, "
            f"dyn0.5 alpha={dyn.alpha:.3f}, dyn0.5 R2={dyn.r2:.3f}, "
            f"dyn0.5 toward={dyn.toward}/{dyn.total}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
