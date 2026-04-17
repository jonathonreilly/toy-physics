#!/usr/bin/env python3
"""Inertial-response probe on the transferable compact repeated-update object.

The compact transfer sweep established that the exact-lattice repeated-update
object is portable across a nearby family, with top3 the stable compact floor
and top2 a narrower boundary on one longer slice.

The next honest question is therefore:

  Can that compact object carry a stable weak-field response as an object,
  rather than only exist as a portable source-side pattern?

This harness couples the transferable compact object ladder to two retained
readouts:
  - broad detector centroid
  - adaptive contour readout

and reuses the ordered-lattice inertial metrics:
  - stage-wise F~M exponent
  - stage-wise response coefficient kappa = delta / s
  - response-coefficient drift across repeated updates

while keeping the exact-lattice object-stability gate:
  - update overlap between successive source weights
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
from scripts.persistent_object_adaptive_readout_probe import (  # noqa: E402
    _adaptive_readout_weights,
    _centroid_from_probs,
    _detector_probs,
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
    _support_eff,
    _topk_weights,
)


KAPPA_DRIFT_THRESHOLD = 0.10


@dataclass(frozen=True)
class Case:
    label: str
    phys_l: int
    phys_w: int
    source_z: float


@dataclass(frozen=True)
class ReadoutResult:
    label: str
    mean_detector_eff: float
    mean_support_frac: float
    mean_capture: float
    mean_delta: float
    step_alpha: tuple[float | None, ...]
    step_toward: tuple[int, ...]
    step_kappa: tuple[float, ...]
    max_kappa_drift: float
    admissible: bool


@dataclass(frozen=True)
class ObjectModeResult:
    label: str
    mean_weight_eff: float
    mean_weight_support: float
    mean_overlap: float
    min_overlap: float
    broad: ReadoutResult
    adaptive: ReadoutResult


CASES = (
    Case("baseline", 6, 3, 2.0),
    Case("source1.5", 6, 3, 1.5),
    Case("width4", 6, 4, 2.0),
    Case("length7", 7, 3, 2.0),
)

OBJECT_MODES = (
    ("broad", None),
    ("top2", 2),
    ("top3", 3),
)


def _support_frac(norm_probs: list[float]) -> float:
    if not norm_probs:
        return 0.0
    peak = max(norm_probs)
    return sum(1 for p in norm_probs if p >= 0.01 * peak) / len(norm_probs)


def _readout_probs(lat: m.Lattice3D, det_probs: list[float], mode: str) -> tuple[list[float], float, float]:
    total = sum(det_probs)
    if mode == "broad":
        return det_probs[:], 1.0 if total > 1e-30 else 0.0, 1.0
    if mode != "adaptive":
        raise ValueError(mode)
    weights, _tau, _target, _hnorm = _adaptive_readout_weights(lat, det_probs)
    masked = [p * w for p, w in zip(det_probs, weights)]
    capture = sum(masked) / total if total > 1e-30 else 0.0
    weight_eff, _ = _support_eff(weights)
    return masked, capture, weight_eff


def _free_readout_centroids(lat: m.Lattice3D) -> dict[str, float]:
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free_amps = lat.propagate(zero_field, m.K)
    det_probs = _detector_probs(free_amps, lat)
    broad_probs, _capture, _weight_eff = _readout_probs(lat, det_probs, "broad")
    adaptive_probs, _capture, _weight_eff = _readout_probs(lat, det_probs, "adaptive")
    return {
        "broad": _centroid_from_probs(lat, broad_probs),
        "adaptive": _centroid_from_probs(lat, adaptive_probs),
    }


def _zero_source_shifts(lat: m.Lattice3D, source_nodes: list[int], gain: float, free_centroids: dict[str, float]) -> dict[str, float]:
    zero_raw = _green_field_layers(lat, 0.0, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes))
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_raw], m.K)
    det_probs = _detector_probs(zero_amps, lat)
    shifts: dict[str, float] = {}
    for mode in ("broad", "adaptive"):
        probs, _capture, _weight_eff = _readout_probs(lat, det_probs, mode)
        shifts[mode] = _centroid_from_probs(lat, probs) - free_centroids[mode]
    return shifts


def _build_readout_result(
    label: str,
    deltas_by_step: list[list[float]],
    detector_effs: list[list[float]],
    support_fracs: list[list[float]],
    captures: list[list[float]],
    overlap_mean: float,
) -> ReadoutResult:
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
    admissible = (
        overlap_mean >= OVERLAP_THRESHOLD
        and all(t == len(SOURCE_STRENGTHS) for t in step_toward)
        and all(alpha is not None and ALPHA_BAND[0] <= alpha <= ALPHA_BAND[1] for alpha in step_alpha)
        and all(drift <= KAPPA_DRIFT_THRESHOLD for drift in drifts)
    )
    return ReadoutResult(
        label=label,
        mean_detector_eff=_mean([v for row in detector_effs for v in row]),
        mean_support_frac=_mean([v for row in support_fracs for v in row]),
        mean_capture=_mean([v for row in captures for v in row]),
        mean_delta=_mean([v for row in deltas_by_step for v in row]),
        step_alpha=tuple(step_alpha),
        step_toward=tuple(step_toward),
        step_kappa=tuple(step_kappa),
        max_kappa_drift=max(drifts) if drifts else 0.0,
        admissible=admissible,
    )


def _run_object_mode(
    lat: m.Lattice3D,
    source_nodes: list[int],
    gain: float,
    free_centroids: dict[str, float],
    top_keep: int | None,
) -> ObjectModeResult:
    overlap_rows: list[list[float]] = [[] for _ in range(N_UPDATES)]
    weight_eff_rows: list[list[float]] = [[] for _ in range(N_UPDATES)]
    weight_support_rows: list[list[float]] = [[] for _ in range(N_UPDATES)]

    readout_deltas = {mode: [[] for _ in range(N_UPDATES)] for mode in ("broad", "adaptive")}
    readout_detector_effs = {mode: [[] for _ in range(N_UPDATES)] for mode in ("broad", "adaptive")}
    readout_support_fracs = {mode: [[] for _ in range(N_UPDATES)] for mode in ("broad", "adaptive")}
    readout_captures = {mode: [[] for _ in range(N_UPDATES)] for mode in ("broad", "adaptive")}

    for strength in SOURCE_STRENGTHS:
        weights = [1.0 / len(source_nodes)] * len(source_nodes)
        prev_weights = weights[:]
        for step in range(N_UPDATES):
            raw = _green_field_layers(lat, strength, source_nodes, weights)
            field = [[gain * v for v in row] for row in raw]
            amps = lat.propagate(field, m.K)
            det_probs = _detector_probs(amps, lat)
            source_probs = [abs(amps[i]) ** 2 for i in source_nodes]

            weight_eff, weight_support = _support_eff(weights)
            norm_prev = _normalize_weights(prev_weights)
            norm_next = _normalize_weights(source_probs)
            overlap_num = sum(a * b for a, b in zip(norm_prev, norm_next))
            overlap_den = math.sqrt(sum(a * a for a in norm_prev) * sum(b * b for b in norm_next))
            overlap = overlap_num / overlap_den if overlap_den > 1e-30 else 0.0

            overlap_rows[step].append(overlap)
            weight_eff_rows[step].append(weight_eff)
            weight_support_rows[step].append(weight_support)

            for readout_mode in ("broad", "adaptive"):
                probs, capture, _weight_eff = _readout_probs(lat, det_probs, readout_mode)
                total = sum(probs)
                norm_probs = [p / total for p in probs if p > 0.0] if total > 1e-30 else []
                readout_deltas[readout_mode][step].append(
                    _centroid_from_probs(lat, probs) - free_centroids[readout_mode]
                )
                readout_detector_effs[readout_mode][step].append(
                    math.exp(-sum(p * math.log(p) for p in norm_probs)) if norm_probs else 0.0
                )
                readout_support_fracs[readout_mode][step].append(_support_frac(norm_probs))
                readout_captures[readout_mode][step].append(capture)

            prev_weights = weights[:]
            if top_keep is None:
                weights = _normalize_weights(source_probs)
            else:
                weights = _topk_weights(source_probs, top_keep)

    mean_overlap = _mean([v for row in overlap_rows for v in row])
    label = "broad" if top_keep is None else f"top{top_keep}"
    broad = _build_readout_result(
        "broad",
        readout_deltas["broad"],
        readout_detector_effs["broad"],
        readout_support_fracs["broad"],
        readout_captures["broad"],
        mean_overlap,
    )
    adaptive = _build_readout_result(
        "adaptive",
        readout_deltas["adaptive"],
        readout_detector_effs["adaptive"],
        readout_support_fracs["adaptive"],
        readout_captures["adaptive"],
        mean_overlap,
    )

    return ObjectModeResult(
        label=label,
        mean_weight_eff=_mean([v for row in weight_eff_rows for v in row]),
        mean_weight_support=_mean([v for row in weight_support_rows for v in row]),
        mean_overlap=mean_overlap,
        min_overlap=min(v for row in overlap_rows for v in row),
        broad=broad,
        adaptive=adaptive,
    )


def main() -> None:
    t0 = time.time()
    print("=" * 128)
    print("PERSISTENT OBJECT COMPACT INERTIAL PROBE")
    print("  transferable compact repeated-update exact-lattice object with broad vs adaptive readout")
    print("=" * 128)
    print(
        f"strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}, h={H}, "
        f"kernel=exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}"
    )
    print(
        f"gates: overlap>={OVERLAP_THRESHOLD:.2f}, drift<={KAPPA_DRIFT_THRESHOLD:.2f}, "
        f"alpha in [{ALPHA_BAND[0]:.2f}, {ALPHA_BAND[1]:.2f}], all steps 4/4 TOWARD"
    )
    print(f"field target max={FIELD_TARGET_MAX}")
    print()

    top3_broad_pass = 0
    top3_adaptive_pass = 0
    top2_broad_pass = 0
    top2_adaptive_pass = 0

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
            f"{'object':>8s} {'readout':>9s} {'obj_eff':>9s} {'obj_sup':>8s} "
            f"{'min_ov':>8s} {'mean_ov':>8s} {'det_eff':>9s} {'capture':>8s} "
            f"{'max_drift':>10s} {'step α':>24s} {'adm':>6s}"
        )
        print("-" * 128)

        mode_results: list[ObjectModeResult] = []
        for object_label, top_keep in OBJECT_MODES:
            result = _run_object_mode(lat, source_nodes, gain, free_centroids, top_keep)
            mode_results.append(result)
            for readout in (result.broad, result.adaptive):
                alpha_str = "[" + ",".join(
                    f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in readout.step_alpha
                ) + "]"
                print(
                    f"{object_label:>8s} {readout.label:>9s} {result.mean_weight_eff:9.3f} "
                    f"{result.mean_weight_support:8.3f} {result.min_overlap:8.3f} "
                    f"{result.mean_overlap:8.3f} {readout.mean_detector_eff:9.2f} "
                    f"{readout.mean_capture:8.3f} {readout.max_kappa_drift:10.3%} "
                    f"{alpha_str:>24s} {str(readout.admissible):>6s}"
                )

            if object_label == "top3":
                top3_broad_pass += int(result.broad.admissible)
                top3_adaptive_pass += int(result.adaptive.admissible)
            elif object_label == "top2":
                top2_broad_pass += int(result.broad.admissible)
                top2_adaptive_pass += int(result.adaptive.admissible)

        broad_passers = [
            result.label
            for result in mode_results
            if result.label != "broad" and result.broad.admissible
        ]
        adaptive_passers = [
            result.label
            for result in mode_results
            if result.label != "broad" and result.adaptive.admissible
        ]
        broad_verdict = broad_passers[0] if broad_passers else "none"
        adaptive_verdict = adaptive_passers[0] if adaptive_passers else "none"
        print(f"  broad compact verdict: {broad_verdict}")
        print(f"  adaptive compact verdict: {adaptive_verdict}")
        print()

    total_cases = len(CASES)
    print("SUMMARY")
    print(f"  top3 broad admissible on {top3_broad_pass}/{total_cases} cases")
    print(f"  top3 adaptive admissible on {top3_adaptive_pass}/{total_cases} cases")
    print(f"  top2 broad admissible on {top2_broad_pass}/{total_cases} cases")
    print(f"  top2 adaptive admissible on {top2_adaptive_pass}/{total_cases} cases")
    print()
    print("SAFE READ")
    print("  - If top3 stays admissible across nearby cases, the transferable compact object carries a stable weak-field response.")
    print("  - If adaptive readout also stays admissible, the detector-side bridge remains usable on the same object family.")
    print("  - If only broad survives, the object is real but the readout side is still the limiting bottleneck.")
    print("  - This is still a compact-object response probe, not full matter closure.")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
