#!/usr/bin/env python3
"""Multi-stage persistence / inertial-response probe for the widened top3 lane.

This is the next honest escalation after the widened local transfer sweep.

The exact-lattice top3 compact object plus the retained blended readout now
survives:
  - the full nearby family
  - most of a second transfer ring

The remaining question is stronger:

  Can that same top3 branch survive multiple full sourced-response segments as
  the same compact object family while keeping a stable weak-field response?
"""

from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402
from scripts.persistent_object_blended_readout_boundary_probe import _blended_probs  # noqa: E402
from scripts.persistent_object_blended_readout_transfer_sweep import BLEND  # noqa: E402
from scripts.persistent_object_compact_inertial_probe import KAPPA_DRIFT_THRESHOLD  # noqa: E402
from scripts.persistent_object_compact_shared import (  # noqa: E402
    ALPHA_BAND,
    FIELD_TARGET_MAX,
    H,
    N_UPDATES,
    OVERLAP_THRESHOLD,
    SOURCE_STRENGTHS,
    _field_abs_max,
    _fit_power,
    _green_field_layers,
    _mean,
    _normalize_weights,
    _source_cluster_nodes,
    _topk_weights,
)


TOP_KEEP = 3
N_STAGES = 3
CARRY_THRESHOLD = 0.90
CARRY_MIN_THRESHOLD = 0.85


@dataclass(frozen=True)
class Case:
    label: str
    phys_l: int
    phys_w: int
    source_z: float


@dataclass(frozen=True)
class CaseResult:
    label: str
    stage_mean_overlap: tuple[float, ...]
    stage_min_overlap: tuple[float, ...]
    stage_mean_capture: tuple[float, ...]
    stage_alpha: tuple[float | None, ...]
    stage_toward: tuple[int, ...]
    stage_kappa: tuple[float, ...]
    stage_carry_mean: tuple[float, ...]
    stage_carry_min: tuple[float, ...]
    max_kappa_drift: float
    admissible: bool


CASES = (
    Case("baseline", 6, 3, 2.0),
    Case("source1.5", 6, 3, 1.5),
    Case("source2.75", 6, 3, 2.75),
    Case("width5", 6, 5, 2.0),
    Case("length8", 8, 3, 2.0),
)


def _overlap(a: list[float], b: list[float]) -> float:
    na = _normalize_weights(a)
    nb = _normalize_weights(b)
    num = sum(x * y for x, y in zip(na, nb))
    den = math.sqrt(sum(x * x for x in na) * sum(y * y for y in nb))
    return num / den if den > 1e-30 else 0.0


def _free_centroid_for_blend(lat: m.Lattice3D) -> float:
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free_amps = lat.propagate(zero_field, m.K)
    det_start = lat.layer_start[lat.nl - 1]
    det_probs = [abs(a) ** 2 for a in free_amps[det_start : det_start + lat.npl]]
    probs, _capture = _blended_probs(lat, det_probs, BLEND)
    total = sum(probs)
    if total <= 1e-30:
        return 0.0
    return sum(p * lat.pos[det_start + i][2] for i, p in enumerate(probs)) / total


def _run_case(case: Case) -> CaseResult:
    lat = m.Lattice3D.build(case.phys_l, case.phys_w, H)
    source_nodes = _source_cluster_nodes(lat, case.source_z)
    ref_raw = _green_field_layers(
        lat,
        max(SOURCE_STRENGTHS),
        source_nodes,
        [1.0 / len(source_nodes)] * len(source_nodes),
    )
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0
    free_centroid = _free_centroid_for_blend(lat)

    stage_overlaps = [[] for _ in range(N_STAGES)]
    stage_min_overlaps = [[] for _ in range(N_STAGES)]
    stage_captures = [[] for _ in range(N_STAGES)]
    stage_deltas = [[] for _ in range(N_STAGES)]
    stage_carry = [[] for _ in range(N_STAGES - 1)]

    for strength in SOURCE_STRENGTHS:
        seed_weights = [1.0 / len(source_nodes)] * len(source_nodes)
        prev_stage_final: list[float] | None = None

        for stage in range(N_STAGES):
            weights = seed_weights[:]
            prev_weights = weights[:]
            update_overlaps: list[float] = []
            final_capture = 0.0
            final_delta = 0.0

            for _update in range(N_UPDATES):
                raw = _green_field_layers(lat, strength, source_nodes, weights)
                field = [[gain * v for v in row] for row in raw]
                amps = lat.propagate(field, m.K)
                det_start = lat.layer_start[lat.nl - 1]
                det_probs = [abs(a) ** 2 for a in amps[det_start : det_start + lat.npl]]
                source_probs = [abs(amps[i]) ** 2 for i in source_nodes]

                update_overlaps.append(_overlap(prev_weights, source_probs))

                probs, capture = _blended_probs(lat, det_probs, BLEND)
                total = sum(probs)
                final_capture = capture
                final_delta = 0.0
                if total > 1e-30:
                    final_delta = (
                        sum(p * lat.pos[det_start + i][2] for i, p in enumerate(probs)) / total
                        - free_centroid
                    )

                prev_weights = weights[:]
                weights = _topk_weights(source_probs, TOP_KEEP)

            if prev_stage_final is not None:
                stage_carry[stage - 1].append(_overlap(prev_stage_final, weights))

            prev_stage_final = weights[:]
            seed_weights = weights[:]
            stage_overlaps[stage].append(_mean(update_overlaps))
            stage_min_overlaps[stage].append(min(update_overlaps))
            stage_captures[stage].append(final_capture)
            stage_deltas[stage].append(final_delta)

    stage_alpha: list[float | None] = []
    stage_toward: list[int] = []
    stage_kappa: list[float] = []
    for stage in range(N_STAGES):
        deltas = stage_deltas[stage]
        alpha = _fit_power(SOURCE_STRENGTHS, [abs(v) for v in deltas])
        kappas = [delta / strength for strength, delta in zip(SOURCE_STRENGTHS, deltas)]
        stage_alpha.append(alpha)
        stage_toward.append(sum(1 for delta in deltas if delta > 0))
        stage_kappa.append(_mean(kappas))

    drifts = [
        abs(stage_kappa[i] - stage_kappa[i - 1]) / max(abs(stage_kappa[i - 1]), 1e-30)
        for i in range(1, len(stage_kappa))
    ]
    carry_means = tuple(_mean(row) for row in stage_carry)
    carry_mins = tuple(min(row) for row in stage_carry)

    admissible = (
        all(_mean(row) >= OVERLAP_THRESHOLD for row in stage_overlaps)
        and all(t == len(SOURCE_STRENGTHS) for t in stage_toward)
        and all(alpha is not None and ALPHA_BAND[0] <= alpha <= ALPHA_BAND[1] for alpha in stage_alpha)
        and all(drift <= KAPPA_DRIFT_THRESHOLD for drift in drifts)
        and all(val >= CARRY_THRESHOLD for val in carry_means)
        and all(val >= CARRY_MIN_THRESHOLD for val in carry_mins)
    )

    return CaseResult(
        label=case.label,
        stage_mean_overlap=tuple(_mean(row) for row in stage_overlaps),
        stage_min_overlap=tuple(min(row) for row in stage_min_overlaps),
        stage_mean_capture=tuple(_mean(row) for row in stage_captures),
        stage_alpha=tuple(stage_alpha),
        stage_toward=tuple(stage_toward),
        stage_kappa=tuple(stage_kappa),
        stage_carry_mean=carry_means,
        stage_carry_min=carry_mins,
        max_kappa_drift=max(drifts) if drifts else 0.0,
        admissible=admissible,
    )


def main() -> None:
    t0 = time.time()
    print("=" * 134)
    print("PERSISTENT OBJECT TOP3 MULTI-STAGE PROBE")
    print("  widened exact-lattice top3 branch under the retained blended readout across chained sourced-response segments")
    print("=" * 134)
    print(
        f"h={H}, top_keep={TOP_KEEP}, blend={BLEND:.2f}, updates/segment={N_UPDATES}, segments={N_STAGES}, "
        f"strengths={SOURCE_STRENGTHS}"
    )
    print(
        f"gates: stage overlap>={OVERLAP_THRESHOLD:.2f}, carry_mean>={CARRY_THRESHOLD:.2f}, "
        f"carry_min>={CARRY_MIN_THRESHOLD:.2f}, drift<={KAPPA_DRIFT_THRESHOLD:.2f}, "
        f"alpha in [{ALPHA_BAND[0]:.2f}, {ALPHA_BAND[1]:.2f}], every stage 4/4 TOWARD"
    )
    print()

    passes = 0
    for case in CASES:
        row = _run_case(case)
        passes += int(row.admissible)
        alpha_str = "[" + ",".join(
            f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in row.stage_alpha
        ) + "]"
        kappa_str = "[" + ",".join(f"{kappa:+.5e}" for kappa in row.stage_kappa) + "]"
        carry_mean_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_carry_mean) + "]"
        carry_min_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_carry_min) + "]"
        overlap_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_mean_overlap) + "]"
        min_overlap_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_min_overlap) + "]"
        capture_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_mean_capture) + "]"
        toward_str = "[" + ",".join(str(val) for val in row.stage_toward) + "]"

        print(f"CASE: {case.label}  (W={case.phys_w}, L={case.phys_l}, source_z={case.source_z})")
        print(f"  stage_mean_overlap  = {overlap_str}")
        print(f"  stage_min_overlap   = {min_overlap_str}")
        print(f"  stage_mean_capture  = {capture_str}")
        print(f"  stage_alpha         = {alpha_str}")
        print(f"  stage_toward        = {toward_str}")
        print(f"  stage_kappa         = {kappa_str}")
        print(f"  carry_mean          = {carry_mean_str}")
        print(f"  carry_min           = {carry_min_str}")
        print(f"  max_kappa_drift     = {row.max_kappa_drift:.3%}")
        print(f"  admissible          = {row.admissible}")
        print()

    total_cases = len(CASES)
    print("SUMMARY")
    print(f"  top3 multistage-admissible on {passes}/{total_cases} stable widened-regime cases")
    print()
    print("SAFE READ")
    print("  - If top3 stays admissible here, the widened local branch survives chained sourced-response segments as the same compact-object family.")
    print("  - If the response drifts or the carry collapses stage-to-stage, the widened branch is still only a transfer result, not a stronger persistent-object regime.")
    print("  - This is still a bounded exact-lattice multistage probe, not matter closure.")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
