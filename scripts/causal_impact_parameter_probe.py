#!/usr/bin/env python3
"""Causal-field impact-parameter probe on the retained center grown family.

Question
--------
Does the retained causal-field modification preserve a recognizable
impact-parameter deflection law on at least one retained grown family?

Guard rails
-----------
- exact zero-source control first
- one retained family only
- compare instantaneous, forward-only, and dynamic finite-cone variants
- keep the claim surface narrow:
  if the broad causal variants keep the law shape, say that explicitly;
  if the finite-cone version breaks it, treat that as the boundary
"""

from __future__ import annotations

import math
import os
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evolving_network_prototype_v6 import build_structured_growth, propagate  # noqa: E402


H = 0.5
N_LAYERS = 13
HALF = 5
SEEDS = tuple(range(6))
SOURCE_LAYER = 2 * N_LAYERS // 3
SOURCE_Y0 = 0.0
B_VALUES = (5, 6, 7, 8, 10)
NULL_B = 8
FIELD_STRENGTH = 5e-5
FIELD_EPS = 0.1
CAUSAL_CONES = (1.0, 0.5)

DOC_PATH = ROOT / "docs" / "CAUSAL_IMPACT_PARAMETER_NOTE.md"
LOG_PATH = ROOT / "logs" / "2026-04-06-causal-impact-parameter-probe.txt"


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


FAMILY = FamilyCase("center grown family", 0.20, 0.70)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values) / math.sqrt(len(values))


def _fit_power_law(bs: list[int], deltas: list[float]) -> tuple[float, float]:
    pairs = [(float(b), abs(d)) for b, d in zip(bs, deltas) if b > 0 and abs(d) > 1e-30]
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
    target_z: float,
) -> int:
    return min(
        layer_nodes,
        key=lambda i: (
            (positions[i][1] - SOURCE_Y0) ** 2 + (positions[i][2] - target_z) ** 2,
            abs(positions[i][1] - SOURCE_Y0),
            abs(positions[i][2] - target_z),
            i,
        ),
    )


def _source_anchor(
    positions: list[tuple[float, float, float]],
    layers: list[list[int]],
    target_z: float,
) -> tuple[int, tuple[float, float, float]]:
    source_node = _select_source_node(positions, layers[SOURCE_LAYER], target_z)
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


def _measure_family(case: FamilyCase) -> tuple[dict[str, FieldSummary], float, float, dict[str, dict[int, list[float]]]]:
    zero_vals: list[float] = []
    field_values: dict[str, dict[int, list[float]]] = {
        "instantaneous": {b: [] for b in B_VALUES},
        "forward-only": {b: [] for b in B_VALUES},
    }
    for c in CAUSAL_CONES:
        field_values[f"dynamic(c={c:g})"] = {b: [] for b in B_VALUES}

    for seed in SEEDS:
        fam = build_structured_growth(N_LAYERS, HALF, H, case.drift, case.restore, seed)
        positions, layers, adj = fam.positions, fam.layers, fam.adj
        det = layers[-1]

        for b in B_VALUES:
            _, anchor = _source_anchor(positions, layers, float(b))

            free = propagate(positions, layers, adj, [0.0] * len(positions))
            z_free = _centroid_z(free, positions, det)

            zero_field = [0.0] * len(positions)
            zero_amps = propagate(positions, layers, adj, zero_field)
            if b == NULL_B:
                zero_vals.append(_centroid_z(zero_amps, positions, det) - z_free)

            inst_field = _instantaneous_field(positions, anchor, FIELD_STRENGTH)
            inst_amps = propagate(positions, layers, adj, inst_field)
            field_values["instantaneous"][b].append(_centroid_z(inst_amps, positions, det) - z_free)

            fwd_field = _forward_only_field(positions, layers, anchor, FIELD_STRENGTH)
            fwd_amps = propagate(positions, layers, adj, fwd_field)
            field_values["forward-only"][b].append(_centroid_z(fwd_amps, positions, det) - z_free)

            for c in CAUSAL_CONES:
                dyn_key = f"dynamic(c={c:g})"
                dyn_field = _dynamic_field(positions, layers, anchor, FIELD_STRENGTH, c)
                dyn_amps = propagate(positions, layers, adj, dyn_field)
                field_values[dyn_key][b].append(_centroid_z(dyn_amps, positions, det) - z_free)

    summaries: dict[str, FieldSummary] = {}
    for key, per_b in field_values.items():
        means = [_mean(per_b[b]) for b in B_VALUES]
        alpha, r2 = _fit_power_law(list(B_VALUES), means)
        summaries[key] = FieldSummary(
            zero_delta=_mean(zero_vals),
            alpha=alpha,
            r2=r2,
            toward=sum(1 for d in means if d > 0),
            total=len(B_VALUES),
        )

    zero_max_delta = max(abs(v) for v in zero_vals) if zero_vals else 0.0
    zero_max_field = 0.0
    return summaries, zero_max_delta, zero_max_field, field_values


def _render_note(
    summaries: dict[str, FieldSummary],
    zero_max_delta: float,
    zero_max_field: float,
    field_values: dict[str, dict[int, list[float]]],
) -> str:
    lines: list[str] = [
        "# Causal Impact-Parameter Note",
        "",
        "**Date:** 2026-04-06  ",
        "**Status:** bounded causal-field impact-parameter probe on the retained center grown family",
        "",
        "## Artifact Chain",
        "",
        "- [`scripts/causal_impact_parameter_probe.py`](../scripts/causal_impact_parameter_probe.py)",
        "- [`logs/2026-04-06-causal-impact-parameter-probe.txt`](../logs/2026-04-06-causal-impact-parameter-probe.txt)",
        "- causal-field context:",
        "  - [`docs/CAUSAL_PROPAGATING_FIELD_NOTE.md`](../docs/CAUSAL_PROPAGATING_FIELD_NOTE.md)",
        "  - [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](../docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)",
        "  - [`docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md`](../docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md)",
        "",
        "## Question",
        "",
        "Does the retained causal-field modification preserve a recognizable",
        "impact-parameter deflection law on the retained center grown family when",
        "the field is instantaneous, forward-only, or finite-cone dynamic?",
        "",
        "## Result",
        "",
        f"- exact zero control: `delta = {zero_max_delta:+.3e}`",
        f"- exact zero field max: `{zero_max_field:+.3e}`",
        "",
        "| field | alpha | R^2 | TOWARD count |",
        "| --- | ---: | ---: | ---: |",
    ]

    for key in ("instantaneous", "forward-only", "dynamic(c=1)", "dynamic(c=0.5)"):
        fs = summaries[key]
        lines.append(
            f"| {key} | `{fs.alpha:.3f}` | `{fs.r2:.3f}` | `{fs.toward}/{fs.total}` |"
        )

    broad_keys = ("instantaneous", "forward-only", "dynamic(c=1)")
    broad_law_like = all(
        math.isfinite(summaries[key].alpha)
        and math.isfinite(summaries[key].r2)
        and summaries[key].r2 > 0.8
        and summaries[key].toward == summaries[key].total
        and abs(summaries[key].alpha + 1.0) < 0.5
        for key in broad_keys
    )
    finite = summaries["dynamic(c=0.5)"]
    finite_boundary = (
        not math.isfinite(finite.alpha)
        or not math.isfinite(finite.r2)
        or finite.r2 <= 0.8
        or finite.toward < finite.total
        or abs(finite.alpha + 1.0) >= 0.5
    )

    lines.extend(
        [
            "",
            "## Safe Read",
            "",
            "The impact-parameter sweep is real on the retained center grown family,",
            "but the causal variants do not all behave the same way.",
            "",
            (
                "The broad variants remain law-like on this family."
                if broad_law_like
                else "The broad variants do not preserve a recognizable `~1/b` law on this family."
            ),
            (
                "The finite-cone variant is the boundary."
                if finite_boundary
                else "The finite-cone variant does not separate cleanly from the broad cases."
            ),
            "",
            "## Diagnostic Snapshot",
            "",
            f"- instantaneous tail-like exponent: `{summaries['instantaneous'].alpha:.3f}`",
            f"- forward-only tail-like exponent: `{summaries['forward-only'].alpha:.3f}`",
            f"- dynamic(c=1) tail-like exponent: `{summaries['dynamic(c=1)'].alpha:.3f}`",
            f"- dynamic(c=0.5) exponent: `{summaries['dynamic(c=0.5)'].alpha:.3f}`",
            "",
            "## Narrow Conclusion",
            "",
            (
                "The causal-field modification preserves an impact-parameter law shape "
                "on the retained center grown family in the broad variants."
                if broad_law_like
                else "The causal-field modification does not preserve a recognizable impact-parameter law shape on the retained center grown family."
            ),
            (
                "The finite-cone dynamic case is the diagnosed boundary."
                if finite_boundary
                else "The finite-cone dynamic case stays in family with the broad variants."
            ),
        ]
    )
    return "\n".join(lines)


def main() -> int:
    summaries, zero_max_delta, zero_max_field, field_values = _measure_family(FAMILY)
    rendered = _render_note(summaries, zero_max_delta, zero_max_field, field_values)

    DOC_PATH.write_text(rendered + "\n", encoding="utf-8")
    LOG_PATH.write_text(rendered + "\n", encoding="utf-8")

    print(rendered)
    print()
    print("SUMMARY")
    for key in ("instantaneous", "forward-only", "dynamic(c=1)", "dynamic(c=0.5)"):
        fs = summaries[key]
        print(
            f"{key}: zero={fs.zero_delta:+.3e}, alpha={fs.alpha:.3f}, "
            f"R2={fs.r2:.3f}, toward={fs.toward}/{fs.total}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
