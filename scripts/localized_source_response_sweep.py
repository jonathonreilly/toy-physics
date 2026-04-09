#!/usr/bin/env python3
"""Localized source-response sweep on the retained 3D h=0.25 family.

This harness asks a narrow question:

Can any source object materially smaller than the broad mesoscopic top-N
control still source a field and preserve downstream sourced-response quality
well enough to matter for the inertial-response lane?

The setup is intentionally the same retained ordered-lattice family used by the
other mesoscopic surrogate controls, but the sweep compares smaller source
families against the broad top-N control under the same explicit floors.
"""

from __future__ import annotations

import math
import os
import sys
from collections import defaultdict

try:
    import numpy as np
except ModuleNotFoundError:
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit("numpy is required for this harness. On this machine use /usr/bin/python3.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.mesoscopic_surrogate_annular_tapered_sweep import (  # noqa: E402
    compress_annulus,
    compress_hollow_square,
    compress_tapered_ellipsoid,
    weighted_state,
)
from scripts.mesoscopic_surrogate_localization_family_sweep import (  # noqa: E402
    best_shift_score,
    build_base_surrogate,
    centroid,
    propagate_pair,
    spread,
    surrogate_field,
    z_profile,
)
from scripts.quasi_persistent_relaunch_probe import detector_indices  # noqa: E402
from scripts.two_body_momentum_harness import Lattice3D  # noqa: E402


H = 0.25
PHYS_W = 10
SEGMENT_L = 12
TOPN_BASE = 196
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
MIN_SUPPORT = 9
MIN_CAPTURE = 0.25
MAX_SHIFT = 8

TOPN_SWEEP = (9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196)
ANNULAR_SWEEP = ((1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6))
SQUARE_SWEEP = ((0, 1), (0, 2), (1, 3), (1, 4), (2, 5))
TAPERED_SWEEP = ((2, 1.0), (3, 1.5), (4, 2.0), (5, 2.5), (6, 3.0))


def stage_profile(lat: Lattice3D, det: list[int], amps: np.ndarray) -> dict[int, float]:
    profile: dict[int, float] = defaultdict(float)
    for idx in det:
        z_idx = int(round(lat.pos[idx, 2] / lat.h))
        profile[z_idx] += float(abs(amps[idx]) ** 2)
    total = sum(profile.values())
    if total > 0:
        profile = {z: p / total for z, p in profile.items()}
    return dict(sorted(profile.items()))


def compress_topn(source_state: np.ndarray, det: list[int], n: int) -> tuple[list[int], dict[int, float], float]:
    probs = np.array([abs(source_state[i]) ** 2 for i in det], dtype=float)
    total = float(probs.sum())
    order = np.argsort(-probs)
    keep = [det[i] for i in order[: min(n, len(det))]]
    keep_profile = {idx: float(abs(source_state[idx]) ** 2) for idx in keep}
    capture = float(sum(probs[order[: min(n, len(det))]]) / max(total, 1e-30))
    return keep, keep_profile, capture


def evaluate_family(
    lat: Lattice3D,
    det: list[int],
    source_state: np.ndarray,
    field: np.ndarray,
    family: str,
    param: float | int | tuple[int, int] | tuple[int, float],
) -> dict[str, float | int | str]:
    if family == "topN":
        keep1, keep_profile1, cap1 = compress_topn(source_state, det, int(param))
        weights1 = None
    else:
        probs = np.array([abs(source_state[i]) ** 2 for i in det], dtype=float)
        peak_idx = det[int(probs.argmax())]
        peak_iy = int(round(lat.pos[peak_idx, 1] / lat.h))
        peak_iz = int(round(lat.pos[peak_idx, 2] / lat.h))

        if family == "annulus":
            inner, outer = param  # type: ignore[misc]
            keep_profile1, keep1, cap1 = compress_annulus(lat, source_state, det, peak_iy, peak_iz, inner, outer)
            weights1 = {idx: 1.0 for idx in keep1}
        elif family == "square":
            inner, outer = param  # type: ignore[misc]
            keep_profile1, keep1, cap1 = compress_hollow_square(lat, source_state, det, peak_iy, peak_iz, inner, outer)
            weights1 = {idx: 1.0 for idx in keep1}
        elif family == "tapered":
            outer, power = param  # type: ignore[misc]
            keep_profile1, keep1, cap1 = compress_tapered_ellipsoid(lat, source_state, det, peak_iy, peak_iz, outer, power)
            weights1 = {
                idx: keep_profile1[idx] / max(float(abs(source_state[idx]) ** 2), 1e-30)
                for idx in keep1
            }
        else:
            raise ValueError(f"unknown family: {family}")

    init1 = weighted_state(lat, source_state, keep1, weights1)
    free1, grav1 = propagate_pair(lat, init1, field)
    profile_free1 = z_profile(free1, det, lat.pos, lat.h)
    profile_grav1 = z_profile(grav1, det, lat.pos, lat.h)
    delta1 = centroid(profile_grav1, lat.h) - centroid(profile_free1, lat.h)

    if family == "topN":
        keep2, keep_profile2, cap2 = compress_topn(grav1, det, int(param))
        weights2 = None
    else:
        probs2 = np.array([abs(grav1[i]) ** 2 for i in det], dtype=float)
        peak_idx2 = det[int(probs2.argmax())]
        peak_iy2 = int(round(lat.pos[peak_idx2, 1] / lat.h))
        peak_iz2 = int(round(lat.pos[peak_idx2, 2] / lat.h))

        if family == "annulus":
            inner, outer = param  # type: ignore[misc]
            keep_profile2, keep2, cap2 = compress_annulus(lat, grav1, det, peak_iy2, peak_iz2, inner, outer)
            weights2 = {idx: 1.0 for idx in keep2}
        elif family == "square":
            inner, outer = param  # type: ignore[misc]
            keep_profile2, keep2, cap2 = compress_hollow_square(lat, grav1, det, peak_iy2, peak_iz2, inner, outer)
            weights2 = {idx: 1.0 for idx in keep2}
        elif family == "tapered":
            outer, power = param  # type: ignore[misc]
            keep_profile2, keep2, cap2 = compress_tapered_ellipsoid(lat, grav1, det, peak_iy2, peak_iz2, outer, power)
            weights2 = {
                idx: keep_profile2[idx] / max(float(abs(grav1[idx]) ** 2), 1e-30)
                for idx in keep2
            }
        else:
            raise ValueError(f"unknown family: {family}")

    init2 = weighted_state(lat, grav1, keep2, weights2)
    free2, grav2 = propagate_pair(lat, init2, field)
    profile_free2 = z_profile(free2, det, lat.pos, lat.h)
    profile_grav2 = z_profile(grav2, det, lat.pos, lat.h)
    delta2 = centroid(profile_grav2, lat.h) - centroid(profile_free2, lat.h)

    shift, score = best_shift_score(profile_grav1, profile_grav2, max_shift=MAX_SHIFT)
    width_ratio = spread(profile_grav2, lat.h) / max(spread(profile_grav1, lat.h), 1e-30)

    return {
        "family": family,
        "param": param,
        "support1": len(keep1),
        "support2": len(keep2),
        "capture1": cap1,
        "capture2": cap2,
        "delta1": delta1,
        "delta2": delta2,
        "delta_ratio": delta2 / max(delta1, 1e-30),
        "shift": shift,
        "score": score,
        "width_ratio": width_ratio,
        "pass_floor": (
            len(keep1) >= MIN_SUPPORT
            and len(keep2) >= MIN_SUPPORT
            and cap1 >= MIN_CAPTURE
            and cap2 >= MIN_CAPTURE
        ),
    }


def rank_key(row: dict[str, float | int | str]) -> tuple[float, float, float, float]:
    return (
        float(row["score"]),
        float(row["capture2"]),
        -abs(float(row["delta_ratio"]) - 1.0),
        -abs(float(row["width_ratio"]) - 1.0),
    )


def main() -> None:
    lat = Lattice3D(SEGMENT_L, PHYS_W, H)
    det = detector_indices(lat)

    init0, coord_weight = build_base_surrogate(lat, TOPN_BASE)
    field = surrogate_field(lat, coord_weight, SOURCE_Z, SOURCE_STRENGTH)

    free0, broad_grav = propagate_pair(lat, init0, field)
    stage1_profile = stage_profile(lat, det, broad_grav)

    rows: list[dict[str, float | int | str]] = []
    for n in TOPN_SWEEP:
        rows.append(evaluate_family(lat, det, broad_grav, field, "topN", n))
    for inner, outer in ANNULAR_SWEEP:
        rows.append(evaluate_family(lat, det, broad_grav, field, "annulus", (inner, outer)))
    for inner, outer in SQUARE_SWEEP:
        rows.append(evaluate_family(lat, det, broad_grav, field, "square", (inner, outer)))
    for outer, power in TAPERED_SWEEP:
        rows.append(evaluate_family(lat, det, broad_grav, field, "tapered", (outer, power)))

    broad_row = next(r for r in rows if str(r["family"]) == "topN" and int(r["param"]) == TOPN_BASE)
    broad_support = int(broad_row["support2"])

    admissible = [r for r in rows if bool(r["pass_floor"])]
    best_overall = max(admissible, key=rank_key) if admissible else None
    smaller = [r for r in admissible if int(r["support2"]) < broad_support]
    best_smaller = max(smaller, key=rank_key) if smaller else None

    print("=" * 108)
    print("LOCALIZED SOURCE-RESPONSE SWEEP")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  h={H}, W={PHYS_W}, segment_L={SEGMENT_L}, broad_topN={TOPN_BASE}, source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}")
    print(f"  Floors: support >= {MIN_SUPPORT} bins, capture >= {MIN_CAPTURE:.2f} in both stages")
    print("  Goal: can any source object materially smaller than the broad mesoscopic control")
    print("        still source a field and preserve downstream sourced-response quality?")
    print("=" * 108)
    print()
    print(f"Stage-1 broad-source centroid shift = {centroid(stage1_profile, lat.h):+.8f}")
    print(f"Stage-1 broad-source spread         = {spread(stage1_profile, lat.h):.8f}")
    print()
    print(
        f"{'family':>8s} {'param':>9s} {'sup1':>5s} {'sup2':>5s} {'cap1':>7s} {'cap2':>7s} "
        f"{'score':>7s} {'wratio':>7s} {'d1':>11s} {'d2':>11s}"
    )
    for row in rows:
        print(
            f"{str(row['family']):>8s} {str(row['param']):>9s}"
            f" {int(row['support1']):5d} {int(row['support2']):5d}"
            f" {float(row['capture1']):7.3f} {float(row['capture2']):7.3f}"
            f" {float(row['score']):7.4f} {float(row['width_ratio']):7.4f}"
            f" {float(row['delta1']):+11.7f} {float(row['delta2']):+11.7f}"
        )

    print()
    print("CONTROL ROW")
    print(
        f"  broad topN {TOPN_BASE}: support2={broad_support}, capture2={float(broad_row['capture2']):.3f}, "
        f"score={float(broad_row['score']):.4f}, wratio={float(broad_row['width_ratio']):.4f}"
    )

    if best_smaller is not None:
        print("BEST SMALLER ADMISSIBLE ROW")
        print(
            f"  {best_smaller['family']} {best_smaller['param']}: support2={int(best_smaller['support2'])}, "
            f"capture2={float(best_smaller['capture2']):.3f}, score={float(best_smaller['score']):.4f}, "
            f"wratio={float(best_smaller['width_ratio']):.4f}, delta_ratio={float(best_smaller['delta_ratio']):.3f}"
        )
    else:
        print("BEST SMALLER ADMISSIBLE ROW")
        print("  none passed the explicit support/capture floors")

    print()
    print("BEST OVERALL ADMISSIBLE ROW")
    if best_overall is not None:
        print(
            f"  {best_overall['family']} {best_overall['param']}: support2={int(best_overall['support2'])}, "
            f"capture2={float(best_overall['capture2']):.3f}, score={float(best_overall['score']):.4f}, "
            f"wratio={float(best_overall['width_ratio']):.4f}"
        )
    else:
        print("  none passed the explicit support/capture floors")

    print("\nSAFE READ")
    if best_smaller is not None and rank_key(best_smaller) > rank_key(broad_row):
        print("  - At least one smaller source object remains admissible, but broad top-N still sets the frontier.")
        print("  - The smaller object can source a field and stay self-similar, but it does not beat the broad control.")
    else:
        print("  - No smaller source object beats the broad top-N control on the same floors.")
        print("  - The source-response lane closes as a bounded negative for localization.")


if __name__ == "__main__":
    main()
