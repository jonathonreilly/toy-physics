#!/usr/bin/env python3
"""Bounded blended-readout transfer sweep on the four boundary-probe cases.

The blended boundary probe found that a broad/adaptive blend of 0.25 bridges
the complementary miss pair on the top3 compact object across four cases:
baseline, source1.5, width4, length7. This sliced sweep replays the top3
admissibility check at the fixed blend on those same four boundary cases as
a sliced cached certificate matching what the auditor identified as the
supportable claim boundary. The two additional cases originally listed in
this file (source2.5, length5) and the top2 mode are not produced here; the
note's claim is narrowed accordingly.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800` mirrors the
# boundary probe budget; the sliced four-case top3 transfer typically
# completes well within this window but the larger ceiling avoids a
# false timeout under audit-lane concurrency contention.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys
import time
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402
from scripts.persistent_object_blended_readout_boundary_probe import (  # noqa: E402
    _blended_probs,
)
from scripts.persistent_object_compact_inertial_probe import (  # noqa: E402
    KAPPA_DRIFT_THRESHOLD,
    _free_readout_centroids,
    _zero_source_shifts,
)
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


BLEND = 0.25


@dataclass(frozen=True)
class Case:
    label: str
    phys_l: int
    phys_w: int
    source_z: float


@dataclass(frozen=True)
class ModeResult:
    label: str
    mean_overlap: float
    min_overlap: float
    mean_detector_eff: float
    mean_capture: float
    mean_delta: float
    step_alpha: tuple[float | None, ...]
    max_kappa_drift: float
    admissible: bool


CASES = (
    Case("baseline", 6, 3, 2.0),
    Case("source1.5", 6, 3, 1.5),
    Case("width4", 6, 4, 2.0),
    Case("length7", 7, 3, 2.0),
)

# Sliced to the top3 boundary-probe claim. The earlier `top2` mode is not
# carried forward here because the boundary probe never produced top2 data;
# downstream scripts that need a top2 run call `_run_mode(case, 2)` directly.
OBJECT_MODES = (
    ("top3", 3),
)


def _free_centroid_for_blend(lat: m.Lattice3D) -> float:
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free_amps = lat.propagate(zero_field, m.K)
    det_probs = [abs(a) ** 2 for a in free_amps[lat.layer_start[lat.nl - 1] : lat.layer_start[lat.nl - 1] + lat.npl]]
    probs, _capture = _blended_probs(lat, det_probs, BLEND)
    total = sum(probs)
    if total <= 1e-30:
        return 0.0
    det_start = lat.layer_start[lat.nl - 1]
    return sum(p * lat.pos[det_start + i][2] for i, p in enumerate(probs)) / total


def _run_mode(case: Case, top_keep: int) -> ModeResult:
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
            det_start = lat.layer_start[lat.nl - 1]
            det_probs = [abs(a) ** 2 for a in amps[det_start : det_start + lat.npl]]
            source_probs = [abs(amps[i]) ** 2 for i in source_nodes]

            norm_prev = _normalize_weights(prev_weights)
            norm_next = _normalize_weights(source_probs)
            overlap_num = sum(a * b for a, b in zip(norm_prev, norm_next))
            overlap_den = math.sqrt(sum(a * a for a in norm_prev) * sum(b * b for b in norm_next))
            overlap = overlap_num / overlap_den if overlap_den > 1e-30 else 0.0
            overlap_rows[step].append(overlap)

            probs, capture = _blended_probs(lat, det_probs, BLEND)
            total = sum(probs)
            norm_probs = [p / total for p in probs if p > 0.0] if total > 1e-30 else []
            det_eff = math.exp(-sum(p * math.log(p) for p in norm_probs)) if norm_probs else 0.0
            delta = 0.0
            if total > 1e-30:
                delta = sum(p * lat.pos[det_start + i][2] for i, p in enumerate(probs)) / total - free_centroid

            deltas_by_step[step].append(delta)
            detector_effs[step].append(det_eff)
            captures[step].append(capture)

            prev_weights = weights[:]
            weights = _topk_weights(source_probs, top_keep)

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

    return ModeResult(
        label=f"top{top_keep}",
        mean_overlap=mean_overlap,
        min_overlap=min(v for row in overlap_rows for v in row),
        mean_detector_eff=_mean([v for row in detector_effs for v in row]),
        mean_capture=_mean([v for row in captures for v in row]),
        mean_delta=_mean([v for row in deltas_by_step for v in row]),
        step_alpha=tuple(step_alpha),
        max_kappa_drift=max(drifts) if drifts else 0.0,
        admissible=admissible,
    )


def main() -> None:
    t0 = time.time()
    print("=" * 122)
    print("PERSISTENT OBJECT BLENDED READOUT TRANSFER SWEEP (sliced to four boundary-probe cases, top3 only)")
    print("  fixed blended readout (blend=0.25) on the four boundary cases: baseline, source1.5, width4, length7")
    print("=" * 122)
    print(
        f"strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}, h={H}, blend={BLEND:.2f}"
    )
    print(
        f"gates: overlap>={OVERLAP_THRESHOLD:.2f}, drift<={KAPPA_DRIFT_THRESHOLD:.2f}, "
        f"alpha in [{ALPHA_BAND[0]:.2f}, {ALPHA_BAND[1]:.2f}], all steps 4/4 TOWARD"
    )
    print(f"field target max={FIELD_TARGET_MAX}")
    print()

    top3_pass = 0

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
            f"{'mode':>8s} {'min_ov':>8s} {'mean_ov':>8s} {'det_eff':>9s} "
            f"{'capture':>8s} {'max_drift':>10s} {'step α':>24s} {'adm':>6s}"
        )
        print("-" * 106)

        top3 = _run_mode(case, 3)
        alpha_str = "[" + ",".join(
            f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in top3.step_alpha
        ) + "]"
        print(
            f"{top3.label:>8s} {top3.min_overlap:8.3f} {top3.mean_overlap:8.3f} "
            f"{top3.mean_detector_eff:9.2f} {top3.mean_capture:8.3f} "
            f"{top3.max_kappa_drift:10.3%} {alpha_str:>24s} {str(top3.admissible):>6s}"
        )

        top3_pass += int(top3.admissible)
        verdict = "top3 bridge" if top3.admissible else "no compact bridge"
        print(f"  verdict: {verdict}")
        print()

    total_cases = len(CASES)
    print("SUMMARY")
    print(f"  top3 admissible on {top3_pass}/{total_cases} boundary cases at fixed blend={BLEND:.2f}")
    print()
    print("SAFE READ")
    print("  - This sliced certificate covers only the four boundary-probe cases at fixed blend=0.25.")
    print("  - The two extra cases (source2.5, length5) listed in earlier framings of this row are not produced here.")
    print("  - The top2 mode is not produced here; downstream callers that need a top2 row call _run_mode directly.")
    print("  - This is still a bounded compact-object response transfer sweep, not matter closure.")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
