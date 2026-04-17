#!/usr/bin/env python3
"""Constrained localization sweep for mesoscopic surrogate source families.

This harness asks whether any *non-degenerate* localized source family can
match or beat the retained broad top-N surrogate on the score/capture tradeoff
without collapsing into a point-like source.

Families compared:
1. top-N compression
2. annular shell in the detector-layer plane
3. hollow square shell in the detector-layer plane
4. tapered ellipsoidal shell in the detector-layer plane

The sweep reuses the retained 3D ordered-lattice mesoscopic surrogate family
and keeps explicit support/capture floors so tiny point-like cases cannot win
by construction.
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

from scripts.mesoscopic_surrogate_localization_family_sweep import (
    build_base_surrogate,
    best_shift_score,
    centroid,
    propagate_pair,
    spread,
    surrogate_field,
    z_profile,
)
from scripts.quasi_persistent_relaunch_probe import ACTION, H, PHYS_W, SEGMENT_L, detector_indices, point_source
from scripts.two_body_momentum_harness import K, Lattice3D


TOPN_BASE = 196
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
MAX_SHIFT = 8

TOPN_SWEEP = (9, 25, 49, 81, 121, 144, 169, 196, 225)
ANNULAR_INNERS = (1, 2, 3, 4)
ANNULAR_OUTER_STEPS = (1, 2, 3, 4)
HOLLOW_INNERS = (1, 2, 3, 4)
HOLLOW_OUTER_STEPS = (1, 2, 3, 4)
TAPERED_OUTERS = (2, 3, 4, 5, 6)
TAPERED_POWERS = (1.0, 2.0, 3.0)

MIN_SUPPORT = 9
MIN_CAPTURE = 0.25


def layer_coords(lat: Lattice3D, idx: int) -> tuple[int, int]:
    _, y, z = lat.pos[idx]
    return int(round(y / lat.h)), int(round(z / lat.h))


def weighted_state(lat: Lattice3D, source_state: np.ndarray, keep_inds: list[int], weights: dict[int, float] | None = None) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    keep_set = set(keep_inds)
    for idx in keep_inds:
        w = 1.0 if weights is None else weights.get(idx, 1.0)
        init[idx] = source_state[idx] * w
    # Keep the selected layer state normalized before relaunch.
    norm = np.sqrt(np.sum(np.abs(init[list(keep_set)]) ** 2))
    if norm > 1e-30:
        init /= norm
    return init


def relaunch_from_selection(
    lat: Lattice3D,
    source_state: np.ndarray,
    layer_inds: list[int],
    keep_inds: list[int],
    weights: dict[int, float] | None = None,
) -> np.ndarray:
    return lat.propagate(weighted_state(lat, source_state, keep_inds, weights), np.zeros(lat.n), K, ACTION)


def compress_topn(profile: dict[int, float], n: int) -> tuple[dict[int, float], int, float]:
    items = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    keep = items[: min(n, len(items))]
    total = sum(p for _, p in keep)
    capture = total / max(sum(profile.values()), 1e-30)
    if total > 0:
        keep_profile = {z: p / total for z, p in keep}
    else:
        keep_profile = {}
    return keep_profile, len(keep), capture


def compress_annulus(
    lat: Lattice3D,
    profile: np.ndarray,
    det: list[int],
    peak_iy: int,
    peak_iz: int,
    inner: int,
    outer: int,
) -> tuple[dict[int, float], list[int], float]:
    keep: list[int] = []
    keep_profile: dict[int, float] = defaultdict(float)
    total = float(np.sum(np.abs(profile[det]) ** 2))
    for idx in det:
        iy, iz = layer_coords(lat, idx)
        r = math.hypot(iy - peak_iy, iz - peak_iz)
        if inner <= r <= outer:
            keep.append(idx)
            keep_profile[idx] = float(abs(profile[idx]) ** 2)
    capture = sum(keep_profile.values()) / max(total, 1e-30)
    return dict(keep_profile), keep, capture


def compress_hollow_square(
    lat: Lattice3D,
    profile: np.ndarray,
    det: list[int],
    peak_iy: int,
    peak_iz: int,
    inner: int,
    outer: int,
) -> tuple[dict[int, float], list[int], float]:
    keep: list[int] = []
    keep_profile: dict[int, float] = defaultdict(float)
    total = float(np.sum(np.abs(profile[det]) ** 2))
    for idx in det:
        iy, iz = layer_coords(lat, idx)
        r = max(abs(iy - peak_iy), abs(iz - peak_iz))
        if inner <= r <= outer:
            keep.append(idx)
            keep_profile[idx] = float(abs(profile[idx]) ** 2)
    capture = sum(keep_profile.values()) / max(total, 1e-30)
    return dict(keep_profile), keep, capture


def compress_tapered_ellipsoid(
    lat: Lattice3D,
    profile: np.ndarray,
    det: list[int],
    peak_iy: int,
    peak_iz: int,
    outer: int,
    power: float,
) -> tuple[dict[int, float], list[int], float]:
    keep: list[int] = []
    keep_profile: dict[int, float] = defaultdict(float)
    total = float(np.sum(np.abs(profile[det]) ** 2))
    ay = max(1.0, float(outer))
    az = max(1.0, float(outer) - 0.5)
    for idx in det:
        iy, iz = layer_coords(lat, idx)
        rho = math.sqrt(((iy - peak_iy) / ay) ** 2 + ((iz - peak_iz) / az) ** 2)
        if rho > 1.0:
            continue
        weight = max(0.0, (1.0 - rho) ** power)
        if weight <= 0.0:
            continue
        keep.append(idx)
        keep_profile[idx] = float(abs(profile[idx]) ** 2) * weight
    capture = sum(keep_profile.values()) / max(total, 1e-30)
    return dict(keep_profile), keep, capture


def zscore_from_state(lat: Lattice3D, det: list[int], amps: np.ndarray) -> dict[int, float]:
    return z_profile(amps, det, lat.pos, lat.h)


def evaluate_family(
    lat: Lattice3D,
    det: list[int],
    source_state: np.ndarray,
    field: np.ndarray,
    family: str,
    param: str,
) -> dict[str, float | int | str]:
    stage1_probs = np.array([abs(source_state[i]) ** 2 for i in det], dtype=float)
    peak_idx1 = det[int(stage1_probs.argmax())]
    peak_iy1, peak_iz1 = layer_coords(lat, peak_idx1)

    if family == "topN":
        n = int(param)
        order1 = np.argsort(-stage1_probs)
        keep1 = [det[i] for i in order1[: min(n, len(det))]]
        weights1 = None
        keep_profile1 = {i: float(abs(source_state[i]) ** 2) for i in keep1}
        cap1 = float(sum(stage1_probs[order1[: min(n, len(det))]]) / max(stage1_probs.sum(), 1e-30))
    elif family == "annulus":
        inner, outer = map(int, param.split(":"))
        keep_profile1, keep1, cap1 = compress_annulus(lat, source_state, det, peak_iy1, peak_iz1, inner, outer)
        weights1 = {idx: 1.0 for idx in keep1}
    elif family == "square":
        inner, outer = map(int, param.split(":"))
        keep_profile1, keep1, cap1 = compress_hollow_square(lat, source_state, det, peak_iy1, peak_iz1, inner, outer)
        weights1 = {idx: 1.0 for idx in keep1}
    elif family == "tapered":
        outer, power = param.split(":")
        keep_profile1, keep1, cap1 = compress_tapered_ellipsoid(lat, source_state, det, peak_iy1, peak_iz1, int(outer), float(power))
        weights1 = {idx: keep_profile1[idx] / max(float(abs(source_state[idx]) ** 2), 1e-30) for idx in keep1}
    else:
        raise ValueError(f"unknown family: {family}")

    init1 = weighted_state(lat, source_state, keep1, weights1)
    free1, grav1 = propagate_pair(lat, init1, field)
    prof_free1 = z_profile(free1, det, lat.pos, lat.h)
    prof_grav1 = z_profile(grav1, det, lat.pos, lat.h)
    delta1 = centroid(prof_grav1, lat.h) - centroid(prof_free1, lat.h)

    stage2_probs = np.array([abs(grav1[i]) ** 2 for i in det], dtype=float)
    peak_idx2 = det[int(stage2_probs.argmax())]
    peak_iy2, peak_iz2 = layer_coords(lat, peak_idx2)

    if family == "topN":
        n = int(param)
        order2 = np.argsort(-stage2_probs)
        keep2 = [det[i] for i in order2[: min(n, len(det))]]
        weights2 = None
        keep_profile2 = {i: float(abs(grav1[i]) ** 2) for i in keep2}
        cap2 = sum(keep_profile2.values()) / max(float(stage2_probs.sum()), 1e-30)
    elif family == "annulus":
        inner, outer = map(int, param.split(":"))
        keep_profile2, keep2, cap2 = compress_annulus(lat, grav1, det, peak_iy2, peak_iz2, inner, outer)
        weights2 = {idx: 1.0 for idx in keep2}
    elif family == "square":
        inner, outer = map(int, param.split(":"))
        keep_profile2, keep2, cap2 = compress_hollow_square(lat, grav1, det, peak_iy2, peak_iz2, inner, outer)
        weights2 = {idx: 1.0 for idx in keep2}
    else:
        outer, power = param.split(":")
        keep_profile2, keep2, cap2 = compress_tapered_ellipsoid(lat, grav1, det, peak_iy2, peak_iz2, int(outer), float(power))
        weights2 = {idx: keep_profile2[idx] / max(float(abs(grav1[idx]) ** 2), 1e-30) for idx in keep2}

    init2 = weighted_state(lat, grav1, keep2, weights2)
    free2, grav2 = propagate_pair(lat, init2, field)
    prof_free2 = z_profile(free2, det, lat.pos, lat.h)
    prof_grav2 = z_profile(grav2, det, lat.pos, lat.h)
    delta2 = centroid(prof_grav2, lat.h) - centroid(prof_free2, lat.h)

    shift, score = best_shift_score(prof_grav1, prof_grav2)
    width_ratio = spread(prof_grav2, lat.h) / max(spread(prof_grav1, lat.h), 1e-30)

    admissible = (
        len(keep1) >= MIN_SUPPORT
        and len(keep2) >= MIN_SUPPORT
        and cap1 >= MIN_CAPTURE
        and cap2 >= MIN_CAPTURE
    )

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
        "admissible": admissible,
    }


def topn_rows(det: list[int], source_state: np.ndarray, field: np.ndarray, lat: Lattice3D) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    stage1_probs = np.array([abs(source_state[i]) ** 2 for i in det], dtype=float)
    order1 = np.argsort(-stage1_probs)
    for n in TOPN_SWEEP:
        keep1 = [det[i] for i in order1[: min(int(n), len(det))]]
        cap1 = float(sum(stage1_probs[order1[: min(int(n), len(det))]]) / max(stage1_probs.sum(), 1e-30))
        init1 = weighted_state(lat, source_state, keep1, None)
        free1, grav1 = propagate_pair(lat, init1, field)
        prof_free1 = z_profile(free1, det, lat.pos, lat.h)
        prof_grav1 = z_profile(grav1, det, lat.pos, lat.h)
        delta1 = centroid(prof_grav1, lat.h) - centroid(prof_free1, lat.h)

        stage2_probs = np.array([abs(grav1[i]) ** 2 for i in det], dtype=float)
        order2 = np.argsort(-stage2_probs)
        keep2 = [det[i] for i in order2[: min(int(n), len(det))]]
        cap2 = float(sum(stage2_probs[order2[: min(int(n), len(det))]]) / max(stage2_probs.sum(), 1e-30))
        init2 = weighted_state(lat, grav1, keep2, None)
        free2, grav2 = propagate_pair(lat, init2, field)
        prof_free2 = z_profile(free2, det, lat.pos, lat.h)
        prof_grav2 = z_profile(grav2, det, lat.pos, lat.h)
        delta2 = centroid(prof_grav2, lat.h) - centroid(prof_free2, lat.h)
        shift, score = best_shift_score(prof_grav1, prof_grav2)
        width_ratio = spread(prof_grav2, lat.h) / max(spread(prof_grav1, lat.h), 1e-30)
        rows.append(
            {
                "family": "topN",
                "param": str(n),
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
                "admissible": len(keep1) >= MIN_SUPPORT and len(keep2) >= MIN_SUPPORT and cap1 >= MIN_CAPTURE and cap2 >= MIN_CAPTURE,
            }
        )
    return rows


def parse_candidate_rows(lat: Lattice3D, source_state: np.ndarray, field: np.ndarray) -> list[dict[str, float | int | str]]:
    det = detector_indices(lat)
    rows = topn_rows(det, source_state, field, lat)

    annulus_params = [f"{inner}:{inner + step}" for inner in ANNULAR_INNERS for step in ANNULAR_OUTER_STEPS if step > 0]
    square_params = [f"{inner}:{inner + step}" for inner in HOLLOW_INNERS for step in HOLLOW_OUTER_STEPS if step > 0]
    tapered_params = [f"{outer}:{power}" for outer in TAPERED_OUTERS for power in TAPERED_POWERS]

    for param in annulus_params:
        rows.append(evaluate_family(lat, det, source_state, field, "annulus", param))
    for param in square_params:
        rows.append(evaluate_family(lat, det, source_state, field, "square", param))
    for param in tapered_params:
        rows.append(evaluate_family(lat, det, source_state, field, "tapered", param))
    return rows


def best_row(rows: list[dict[str, float | int | str]]) -> dict[str, float | int | str] | None:
    admissible = [r for r in rows if bool(r["admissible"])]
    if not admissible:
        return None
    return max(
        admissible,
        key=lambda r: (
            float(r["score"]),
            float(r["capture2"]),
            float(r["capture1"]),
            int(r["support2"]),
        ),
    )


def best_by_family(rows: list[dict[str, float | int | str]], family: str) -> dict[str, float | int | str] | None:
    family_rows = [r for r in rows if r["family"] == family and bool(r["admissible"])]
    if not family_rows:
        return None
    return max(
        family_rows,
        key=lambda r: (
            float(r["score"]),
            float(r["capture2"]),
            float(r["capture1"]),
            int(r["support2"]),
        ),
    )


def main() -> None:
    lat = Lattice3D(SEGMENT_L, PHYS_W, H)
    det = detector_indices(lat)
    source, coord_weight = build_base_surrogate(lat, TOPN_BASE)
    field = surrogate_field(lat, coord_weight, SOURCE_Z, SOURCE_STRENGTH)

    first_segment = lat.propagate(source, np.zeros(lat.n), K, ACTION)
    stage1_probs = np.array([abs(first_segment[i]) ** 2 for i in det], dtype=float)
    peak_idx = det[int(stage1_probs.argmax())]
    peak_iy, peak_iz = layer_coords(lat, peak_idx)

    rows = parse_candidate_rows(lat, first_segment, field)
    topn_best = best_by_family(rows, "topN")
    annular_best = best_by_family(rows, "annulus")
    square_best = best_by_family(rows, "square")
    tapered_best = best_by_family(rows, "tapered")
    overall_best = best_row(rows)

    print("=" * 104)
    print("MESOSCOPIC SURROGATE ANNULAR / TAPERED SWEEP")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(
        f"  h={H}, W={PHYS_W}, segment_L={SEGMENT_L}, base_topN={TOPN_BASE}, "
        f"source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}"
    )
    print(
        f"  explicit floors: support >= {MIN_SUPPORT}, capture >= {MIN_CAPTURE:.2f} "
        "(stage 1 and stage 2)"
    )
    print(f"  detector-layer peak seed: iy={peak_iy}, iz={peak_iz}")
    print("=" * 104)
    print()

    print(f"{'family':>10s} {'param':>10s} {'sup1':>5s} {'sup2':>5s} {'cap1':>7s} {'cap2':>7s} {'score':>7s} {'wratio':>7s} {'adm':>4s}")
    for row in rows:
        print(
            f"{str(row['family']):>10s} {str(row['param']):>10s} {int(row['support1']):5d} {int(row['support2']):5d}"
            f" {float(row['capture1']):7.3f} {float(row['capture2']):7.3f}"
            f" {float(row['score']):7.4f} {float(row['width_ratio']):7.4f} {('Y' if bool(row['admissible']) else 'N'):>4s}"
        )

    print("\nBEST ADMISSIBLE PER FAMILY")
    for label, row in (
        ("topN", topn_best),
        ("annulus", annular_best),
        ("square", square_best),
        ("tapered", tapered_best),
    ):
        if row is None:
            print(f"  {label:>8s}: no row met the floors")
            continue
        print(
            f"  {label:>8s}: {row['param']} "
            f"score={float(row['score']):.4f}, capture2={float(row['capture2']):.3f}, "
            f"support2={int(row['support2'])}, width_ratio={float(row['width_ratio']):.4f}"
        )

    if overall_best is None:
        print("\nSAFE READ")
        print("  No non-degenerate family met the floors.")
    else:
        print("\nBEST OVERALL")
        print(
            f"  {overall_best['family']} {overall_best['param']} with "
            f"score={float(overall_best['score']):.4f}, capture2={float(overall_best['capture2']):.3f}, "
            f"support2={int(overall_best['support2'])}, width_ratio={float(overall_best['width_ratio']):.4f}"
        )
        if overall_best["family"] == "topN":
            print("  No non-degenerate annular / hollow / tapered family beat topN on the admissible score/capture frontier.")
        else:
            print("  A non-topN family reached the admissible frontier; compare directly with the topN row above.")

    print("\nSAFE READ")
    print("  - The explicit floors exclude point-source collapse by construction.")
    print("  - Broad topN remains the strongest admissible control if the best row is topN.")
    print("  - Any annular / hollow / tapered win would have to clear the floors and still match or beat topN on score and capture.")


if __name__ == "__main__":
    main()
