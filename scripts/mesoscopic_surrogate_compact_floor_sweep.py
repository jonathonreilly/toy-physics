#!/usr/bin/env python3
"""Compact-family floor sweep for the mesoscopic surrogate lane.

This is a constrained follow-up to the localization-family sweep. The question
is no longer whether tiny point-like compressions can match the broad surrogate;
those were already identified as degenerate. Instead, we ask whether any
compact family still wins once we enforce a minimum support and capture floor.

Families compared:
1. top-N compression (baseline)
2. compact Gaussian compression
3. tapered compact compression

The retained 3D ordered-lattice family is unchanged. The only new constraint is
that a candidate must satisfy explicit support/capture floors in both stages so
that point-like winners are excluded by construction.
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
    raise SystemExit("numpy is required for this sweep. On this machine use /usr/bin/python3.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.mesoscopic_surrogate_localization_family_sweep import (  # type: ignore
    ACTION,
    H,
    PHYS_W,
    SEGMENT_L,
    TOPN_BASE,
    SOURCE_STRENGTH,
    SOURCE_Z,
    best_shift_score,
    build_base_surrogate,
    centroid,
    detector_indices,
    propagate_pair,
    spread,
    surrogate_field,
    z_profile,
)
from scripts.two_body_momentum_harness import Lattice3D


MIN_SUPPORT_BINS = 5
MIN_CAPTURE = 0.25
MAX_SHIFT = 8

TOPN_SWEEP = (25, 49, 81, 121, 144, 169, 196, 225, 256)
GAUSSIAN_SWEEP = (0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0)
TAPERED_SWEEP = (2, 3, 4, 5, 6, 7, 8)


def compress_topn(profile: dict[int, float], n: int) -> tuple[dict[int, float], int, float]:
    items = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    keep = items[: min(n, len(items))]
    total = sum(p for _, p in keep)
    capture = total / max(sum(profile.values()), 1e-30)
    if total > 0:
        keep_profile = {z: p / total for z, p in keep}
    else:
        keep_profile = {}
    return keep_profile, len(keep_profile), capture


def compress_gaussian(profile: dict[int, float], sigma: float) -> tuple[dict[int, float], int, float]:
    if not profile:
        return {}, 0, 0.0
    peak_z = max(profile, key=profile.get)
    support_radius = max(1, int(math.ceil(3.0 * sigma)))
    weighted = {}
    support_mass = 0.0
    raw_total = sum(profile.values())
    for z, p in profile.items():
        d = z - peak_z
        if abs(d) > support_radius:
            continue
        support_mass += p
        mask = math.exp(-0.5 * (d / max(sigma, 1e-30)) ** 2)
        weighted[z] = p * mask
    total = sum(weighted.values())
    capture = support_mass / max(raw_total, 1e-30)
    if total > 0:
        weighted = {z: p / total for z, p in weighted.items()}
    return weighted, len(weighted), capture


def compress_tapered(profile: dict[int, float], radius: int) -> tuple[dict[int, float], int, float]:
    if not profile:
        return {}, 0, 0.0
    peak_z = max(profile, key=profile.get)
    raw_total = sum(profile.values())
    support_mass = 0.0
    weighted = {}
    for z, p in profile.items():
        d = abs(z - peak_z)
        if d > radius:
            continue
        support_mass += p
        x = d / max(radius, 1)
        taper = math.cos(0.5 * math.pi * x) ** 2
        weighted[z] = p * taper
    total = sum(weighted.values())
    capture = support_mass / max(raw_total, 1e-30)
    if total > 0:
        weighted = {z: p / total for z, p in weighted.items()}
    return weighted, len(weighted), capture


def evaluate_family(
    lat: Lattice3D,
    det: list[int],
    stage1_profile: dict[int, float],
    field: np.ndarray,
    family: str,
    param: float | int,
) -> dict[str, float | int | str]:
    if family == "topN":
        compressed1, support1, capture1 = compress_topn(stage1_profile, int(param))
    elif family == "gaussian":
        compressed1, support1, capture1 = compress_gaussian(stage1_profile, float(param))
    elif family == "tapered":
        compressed1, support1, capture1 = compress_tapered(stage1_profile, int(param))
    else:
        raise ValueError(f"unknown family: {family}")

    init1 = np.zeros(lat.n, dtype=np.complex128)
    for z_idx, p in compressed1.items():
        init1[lat.nmap[(0, 0, z_idx)]] = math.sqrt(max(p, 0.0))
    norm = np.sqrt(np.sum(np.abs(init1) ** 2))
    if norm > 1e-30:
        init1 /= norm

    free1, grav1 = propagate_pair(lat, init1, field)
    profile_free1 = z_profile(free1, det, lat.pos, lat.h)
    profile_grav1 = z_profile(grav1, det, lat.pos, lat.h)
    delta1 = centroid(profile_grav1, lat.h) - centroid(profile_free1, lat.h)

    if family == "topN":
        compressed2, support2, capture2 = compress_topn(profile_grav1, int(param))
    elif family == "gaussian":
        compressed2, support2, capture2 = compress_gaussian(profile_grav1, float(param))
    else:
        compressed2, support2, capture2 = compress_tapered(profile_grav1, int(param))

    init2 = np.zeros(lat.n, dtype=np.complex128)
    for z_idx, p in compressed2.items():
        init2[lat.nmap[(0, 0, z_idx)]] = math.sqrt(max(p, 0.0))
    norm2 = np.sqrt(np.sum(np.abs(init2) ** 2))
    if norm2 > 1e-30:
        init2 /= norm2

    free2, grav2 = propagate_pair(lat, init2, field)
    profile_free2 = z_profile(free2, det, lat.pos, lat.h)
    profile_grav2 = z_profile(grav2, det, lat.pos, lat.h)
    delta2 = centroid(profile_grav2, lat.h) - centroid(profile_free2, lat.h)

    shift, score = best_shift_score(profile_grav1, profile_grav2, max_shift=MAX_SHIFT)
    width_ratio = spread(profile_grav2, lat.h) / max(spread(profile_grav1, lat.h), 1e-30)
    pass_floor = (
        int(support1) >= MIN_SUPPORT_BINS
        and int(support2) >= MIN_SUPPORT_BINS
        and float(capture1) >= MIN_CAPTURE
        and float(capture2) >= MIN_CAPTURE
    )

    return {
        "family": family,
        "param": param,
        "support1": support1,
        "support2": support2,
        "capture1": capture1,
        "capture2": capture2,
        "delta1": delta1,
        "delta2": delta2,
        "delta_ratio": delta2 / max(delta1, 1e-30),
        "shift": shift,
        "score": score,
        "width_ratio": width_ratio,
        "pass_floor": pass_floor,
    }


def best_candidate(rows: list[dict[str, float | int | str]], family: str | None = None) -> dict[str, float | int | str] | None:
    passing = [r for r in rows if bool(r["pass_floor"]) and (family is None or str(r["family"]) == family)]
    if not passing:
        return None
    return max(
        passing,
        key=lambda r: (
            float(r["score"]),
            float(r["capture2"]),
            -abs(float(r["delta_ratio"]) - 1.0),
            -float(r["tv_grav"]) if "tv_grav" in r else 0.0,
        ),
    )


def main() -> None:
    lat = Lattice3D(SEGMENT_L, PHYS_W, H)
    det = detector_indices(lat)
    init0, coord_weight = build_base_surrogate(lat, TOPN_BASE)
    field = surrogate_field(lat, coord_weight, SOURCE_Z, SOURCE_STRENGTH)

    free1, grav1 = propagate_pair(lat, init0, field)
    stage1_profile = z_profile(grav1, det, lat.pos, lat.h)

    rows: list[dict[str, float | int | str]] = []
    for n in TOPN_SWEEP:
        rows.append(evaluate_family(lat, det, stage1_profile, field, "topN", n))
    for sigma in GAUSSIAN_SWEEP:
        rows.append(evaluate_family(lat, det, stage1_profile, field, "gaussian", sigma))
    for radius in TAPERED_SWEEP:
        rows.append(evaluate_family(lat, det, stage1_profile, field, "tapered", radius))

    best_topn = best_candidate(rows, "topN")
    best_gaussian = best_candidate(rows, "gaussian")
    best_tapered = best_candidate(rows, "tapered")
    best_compact = None
    compact_candidates = [r for r in rows if str(r["family"]) in {"gaussian", "tapered"} and bool(r["pass_floor"])]
    if compact_candidates:
        best_compact = max(
            compact_candidates,
            key=lambda r: (
                float(r["score"]),
                float(r["capture2"]),
                -abs(float(r["delta_ratio"]) - 1.0),
                -float(r["width_ratio"]),
            ),
        )

    print("=" * 100)
    print("MESOSCOPIC SURROGATE COMPACT-FLOOR SWEEP")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  h={H}, W={PHYS_W}, segment_L={SEGMENT_L}, base_topN={TOPN_BASE}, source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}")
    print(f"  Floors: support >= {MIN_SUPPORT_BINS} bins, capture >= {MIN_CAPTURE:.2f} in both stages")
    print("  Goal: do any compact Gaussian or tapered compact families beat the broad top-N control once point-like winners are excluded?")
    print("=" * 100)
    print()

    print(f"Stage-1 detector support size: {len(det)} bins")
    print("\nALL CANDIDATES")
    print(
        f"{'family':>10s} {'param':>8s} {'sup1':>5s} {'cap1':>7s} {'sup2':>5s} {'cap2':>7s} "
        f"{'floor':>6s} {'score':>7s} {'d_ratio':>8s} {'width':>7s}"
    )
    for row in rows:
        print(
            f"{str(row['family']):>10s} {str(row['param']):>8s} {int(row['support1']):5d} {float(row['capture1']):7.3f}"
            f" {int(row['support2']):5d} {float(row['capture2']):7.3f} {str(bool(row['pass_floor'])):>6s}"
            f" {float(row['score']):7.4f} {float(row['delta_ratio']):8.3f} {float(row['width_ratio']):7.3f}"
        )

    print("\nBEST PASSING CANDIDATES")
    if best_topn is None:
        print("  topN: no candidate met the floor")
    else:
        print(
            "  topN: "
            f"{best_topn['param']} bins, capture2={float(best_topn['capture2']):.3f}, "
            f"score={float(best_topn['score']):.4f}, width={float(best_topn['width_ratio']):.3f}"
        )
    if best_gaussian is None:
        print("  gaussian: no candidate met the floor")
    else:
        print(
            "  gaussian: "
            f"sigma={best_gaussian['param']}, capture2={float(best_gaussian['capture2']):.3f}, "
            f"score={float(best_gaussian['score']):.4f}, width={float(best_gaussian['width_ratio']):.3f}"
        )
    if best_tapered is None:
        print("  tapered: no candidate met the floor")
    else:
        print(
            "  tapered: "
            f"radius={best_tapered['param']}, capture2={float(best_tapered['capture2']):.3f}, "
            f"score={float(best_tapered['score']):.4f}, width={float(best_tapered['width_ratio']):.3f}"
        )

    print("\nSAFE READ")
    if best_compact is None:
        print("  - No compact Gaussian or tapered compact family met both floors on the retained 3D family.")
        print("  - Once point-like winners are excluded by construction, topN remains the least-bad mesoscopic control.")
    else:
        print(
            "  - A compact family survived the floors, but it still must be compared against the broad topN control."
        )
        print(
            f"  - Best compact survivor: {best_compact['family']} {best_compact['param']} with "
            f"capture2={float(best_compact['capture2']):.3f}, score={float(best_compact['score']):.4f}, "
            f"width={float(best_compact['width_ratio']):.3f}"
        )
        print("  - The key question is whether it meaningfully improves on topN at the same floors.")


if __name__ == "__main__":
    main()
