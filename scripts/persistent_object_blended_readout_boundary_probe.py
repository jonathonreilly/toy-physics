#!/usr/bin/env python3
"""Blended readout boundary probe on the compact object response lane.

The compact inertial probe found a complementary split on the transferable top3
object:

  - source1.5 passes with adaptive readout but not broad
  - length7 passes with broad readout but not adaptive

The next constrained question is:

  Can one blended broad/adaptive readout architecture cover both sides of that
  split without breaking the rows that already pass?
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys
import time
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402
from scripts.persistent_object_adaptive_readout_probe import (  # noqa: E402
    _adaptive_readout_weights,
    _centroid_from_probs,
    _detector_probs,
)
from scripts.persistent_object_compact_inertial_probe import (  # noqa: E402
    KAPPA_DRIFT_THRESHOLD,
    _free_readout_centroids,
    _zero_source_shifts,
)
from scripts.persistent_object_compact_shared import (  # noqa: E402
    ALPHA_BAND,
    FIELD_TARGET_MAX,
    GREEN_EPS,
    GREEN_MU,
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
BLENDS = (0.0, 0.25, 0.5, 0.75, 1.0)


@dataclass(frozen=True)
class Case:
    label: str
    phys_l: int
    phys_w: int
    source_z: float


@dataclass(frozen=True)
class BlendResult:
    blend: float
    mean_overlap: float
    min_overlap: float
    mean_detector_eff: float
    mean_capture: float
    mean_delta: float
    step_alpha: tuple[float | None, ...]
    step_kappa: tuple[float, ...]
    max_kappa_drift: float
    admissible: bool


CASES = (
    Case("baseline", 6, 3, 2.0),
    Case("source1.5", 6, 3, 1.5),
    Case("width4", 6, 4, 2.0),
    Case("length7", 7, 3, 2.0),
)


def _blended_probs(lat: m.Lattice3D, det_probs: list[float], blend: float) -> tuple[list[float], float]:
    total = sum(det_probs)
    if total <= 1e-30:
        return det_probs[:], 0.0
    if blend <= 0.0:
        weights, _tau, _target, _hnorm = _adaptive_readout_weights(lat, det_probs)
    elif blend >= 1.0:
        weights = [1.0] * len(det_probs)
    else:
        adaptive_weights, _tau, _target, _hnorm = _adaptive_readout_weights(lat, det_probs)
        weights = [blend + (1.0 - blend) * w for w in adaptive_weights]
    masked = [p * w for p, w in zip(det_probs, weights)]
    capture = sum(masked) / total if total > 1e-30 else 0.0
    return masked, capture


def _free_centroid_for_blend(lat: m.Lattice3D, blend: float) -> float:
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free_amps = lat.propagate(zero_field, m.K)
    det_probs = _detector_probs(free_amps, lat)
    probs, _capture = _blended_probs(lat, det_probs, blend)
    return _centroid_from_probs(lat, probs)


def _run_case(case: Case, blend: float) -> BlendResult:
    lat = m.Lattice3D.build(case.phys_l, case.phys_w, H)
    source_nodes = _source_cluster_nodes(lat, case.source_z)
    ref_raw = _green_field_layers(
        lat,
        max(SOURCE_STRENGTHS),
        source_nodes,
        [1.0 / len(source_nodes)] * len(source_nodes),
    )
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0
    free_centroid = _free_centroid_for_blend(lat, blend)

    overlap_rows: list[list[float]] = [[] for _ in range(N_UPDATES)]
    deltas_by_step: list[list[float]] = [[] for _ in range(N_UPDATES)]
    detector_effs: list[list[float]] = [[] for _ in range(N_UPDATES)]
    captures: list[list[float]] = [[] for _ in range(N_UPDATES)]

    for strength in SOURCE_STRENGTHS:
        weights = [1.0 / len(source_nodes)] * len(source_nodes)
        prev_weights = weights[:]
        for step in range(N_UPDATES):
            raw = _green_field_layers(lat, strength, source_nodes, weights)
            field = [[gain * v for v in row] for row in raw]
            amps = lat.propagate(field, m.K)
            det_probs = _detector_probs(amps, lat)
            source_probs = [abs(amps[i]) ** 2 for i in source_nodes]

            norm_prev = _normalize_weights(prev_weights)
            norm_next = _normalize_weights(source_probs)
            overlap_num = sum(a * b for a, b in zip(norm_prev, norm_next))
            overlap_den = math.sqrt(sum(a * a for a in norm_prev) * sum(b * b for b in norm_next))
            overlap = overlap_num / overlap_den if overlap_den > 1e-30 else 0.0
            overlap_rows[step].append(overlap)

            probs, capture = _blended_probs(lat, det_probs, blend)
            total = sum(probs)
            norm_probs = [p / total for p in probs if p > 0.0] if total > 1e-30 else []
            detector_eff = math.exp(-sum(p * math.log(p) for p in norm_probs)) if norm_probs else 0.0
            delta = _centroid_from_probs(lat, probs) - free_centroid

            deltas_by_step[step].append(delta)
            detector_effs[step].append(detector_eff)
            captures[step].append(capture)

            prev_weights = weights[:]
            weights = _topk_weights(source_probs, TOP_KEEP)

    step_alpha: list[float | None] = []
    step_toward: list[int] = []
    step_kappa: list[float] = []
    for step in range(N_UPDATES):
        deltas = deltas_by_step[step]
        alpha = _fit_power(SOURCE_STRENGTHS, [abs(v) for v in deltas])
        kappas = [delta / strength for strength, delta in zip(SOURCE_STRENGTHS, deltas)]
        step_alpha.append(alpha)
        step_toward.append(sum(1 for delta in deltas if delta > 0))
        step_kappa.append(float(sum(kappas) / len(kappas)))

    drifts = [
        abs(step_kappa[i] - step_kappa[i - 1]) / max(abs(step_kappa[i - 1]), 1e-30)
        for i in range(1, len(step_kappa))
    ]
    mean_overlap = _mean([v for row in overlap_rows for v in row])
    admissible = (
        mean_overlap >= OVERLAP_THRESHOLD
        and all(t == len(SOURCE_STRENGTHS) for t in step_toward)
        and all(alpha is not None and ALPHA_BAND[0] <= alpha <= ALPHA_BAND[1] for alpha in step_alpha)
        and all(drift <= KAPPA_DRIFT_THRESHOLD for drift in drifts)
    )
    return BlendResult(
        blend=blend,
        mean_overlap=mean_overlap,
        min_overlap=min(v for row in overlap_rows for v in row),
        mean_detector_eff=_mean([v for row in detector_effs for v in row]),
        mean_capture=_mean([v for row in captures for v in row]),
        mean_delta=_mean([v for row in deltas_by_step for v in row]),
        step_alpha=tuple(step_alpha),
        step_kappa=tuple(step_kappa),
        max_kappa_drift=max(drifts) if drifts else 0.0,
        admissible=admissible,
    )


def main() -> None:
    t0 = time.time()
    print("=" * 126)
    print("PERSISTENT OBJECT BLENDED READOUT BOUNDARY PROBE")
    print("  top3 compact object, broad-adaptive readout blend on the complementary-miss exact-family rows")
    print("=" * 126)
    print(
        f"strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}, h={H}, top_keep={TOP_KEEP}, "
        f"blends={BLENDS}"
    )
    print(
        f"gates: overlap>={OVERLAP_THRESHOLD:.2f}, drift<={KAPPA_DRIFT_THRESHOLD:.2f}, "
        f"alpha in [{ALPHA_BAND[0]:.2f}, {ALPHA_BAND[1]:.2f}], all steps 4/4 TOWARD"
    )
    print(f"field target max={FIELD_TARGET_MAX}")
    print()

    universal_blends = 0
    any_blends = 0

    for case in CASES:
        lat = m.Lattice3D.build(case.phys_l, case.phys_w, H)
        source_nodes = _source_cluster_nodes(lat, case.source_z)
        ref_raw = _green_field_layers(
            lat,
            max(SOURCE_STRENGTHS),
            source_nodes,
            [1.0 / len(source_nodes)] * len(source_nodes),
        )
        gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0
        free_centroids = _free_readout_centroids(lat)
        zero_shifts = _zero_source_shifts(lat, source_nodes, gain, free_centroids)

        print(
            f"CASE: {case.label}  (h={H}, W={case.phys_w}, L={case.phys_l}, source_z={case.source_z}, "
            f"zero_broad={zero_shifts['broad']:+.3e}, zero_adaptive={zero_shifts['adaptive']:+.3e})"
        )
        print(
            f"{'blend':>7s} {'min_ov':>8s} {'mean_ov':>8s} {'det_eff':>9s} "
            f"{'capture':>8s} {'max_drift':>10s} {'step α':>24s} {'adm':>6s}"
        )
        print("-" * 108)

        case_results = [_run_case(case, blend) for blend in BLENDS]
        passing = [row for row in case_results if row.admissible]
        if passing:
            any_blends += 1
        for row in case_results:
            alpha_str = "[" + ",".join(
                f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in row.step_alpha
            ) + "]"
            print(
                f"{row.blend:7.2f} {row.min_overlap:8.3f} {row.mean_overlap:8.3f} "
                f"{row.mean_detector_eff:9.2f} {row.mean_capture:8.3f} "
                f"{row.max_kappa_drift:10.3%} {alpha_str:>24s} {str(row.admissible):>6s}"
            )

        if len(passing) == len(case_results):
            universal_blends += 1
        best = min(passing, key=lambda row: abs(row.blend - 0.5)) if passing else None
        verdict = f"best passing blend={best.blend:.2f}" if best is not None else "no passing blend"
        print(f"  verdict: {verdict}")
        print()

    print("SUMMARY")
    print(f"  cases with at least one passing blend: {any_blends}/{len(CASES)}")
    print(f"  cases where every tested blend passes: {universal_blends}/{len(CASES)}")
    print()
    print("SAFE READ")
    print("  - If one blend passes on the complementary-miss rows, the readout split is bridgeable without changing the object.")
    print("  - If the passing blends for source1.5 and length7 stay disjoint, the lane remains below a readout-invariant closure bar.")
    print("  - This is still a readout-boundary probe on the compact object response lane.")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
