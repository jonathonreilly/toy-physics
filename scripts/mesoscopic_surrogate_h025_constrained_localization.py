#!/usr/bin/env python3
"""Final constrained localization attempt on the retained 3D h=0.25 family.

This is the last non-degenerate localization shot on the retained ordered-lattice
mesoscopic surrogate lane. The question is intentionally narrow:

1. Build the frozen broad surrogate source from the retained h=0.25 family.
2. Enforce explicit support/capture floors from the start.
3. Compare the broad top-N control against a localized annular family.

If the broad top-N control still owns the admissible frontier, this lane closes
cleanly as a broad-source mesoscopic control result.
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

from scripts.mesoscopic_surrogate_localization_family_sweep import (  # noqa: E402
    build_base_surrogate,
    best_shift_score,
    centroid,
    propagate_pair,
    spread,
    surrogate_field,
    z_profile,
)
from scripts.quasi_persistent_relaunch_probe import ACTION  # noqa: E402
from scripts.two_body_momentum_harness import K, Lattice3D  # noqa: E402


H = 0.25
PHYS_L = 12
PHYS_W = 10
TOPN_BASE = 196
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
MAX_SHIFT = 8

TOPN_SWEEP = (121, 144, 169, 196, 225, 256, 289, 324)
ANNULAR_SWEEP = ("1:5", "1:6", "2:6", "2:7", "3:7", "3:8")

MIN_SUPPORT_BINS = 9
MIN_CAPTURE = 0.25


def layer_coords(lat: Lattice3D, idx: int) -> tuple[int, int]:
    _, y, z = lat.pos[idx]
    return int(round(y / lat.h)), int(round(z / lat.h))


def weighted_state(
    lat: Lattice3D,
    source_state: np.ndarray,
    keep_inds: list[int],
    weights: dict[int, float] | None = None,
) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    keep_set = set(keep_inds)
    for idx in keep_inds:
        w = 1.0 if weights is None else weights.get(idx, 1.0)
        init[idx] = source_state[idx] * w
    norm = np.sqrt(np.sum(np.abs(init[list(keep_set)]) ** 2))
    if norm > 1e-30:
        init /= norm
    return init


def compress_topn(profile: np.ndarray, det: list[int], n: int) -> tuple[list[int], float]:
    probs = np.array([abs(profile[i]) ** 2 for i in det], dtype=float)
    order = np.argsort(-probs)
    keep = [det[i] for i in order[: min(n, len(det))]]
    capture = float(sum(probs[order[: min(n, len(det))]]) / max(probs.sum(), 1e-30))
    return keep, capture


def compress_annulus(
    lat: Lattice3D,
    profile: np.ndarray,
    det: list[int],
    peak_iy: int,
    peak_iz: int,
    inner: int,
    outer: int,
) -> tuple[list[int], float]:
    keep: list[int] = []
    total = float(np.sum(np.abs(profile[det]) ** 2))
    kept_mass = 0.0
    for idx in det:
        iy, iz = layer_coords(lat, idx)
        r = math.hypot(iy - peak_iy, iz - peak_iz)
        if inner <= r <= outer:
            keep.append(idx)
            kept_mass += float(abs(profile[idx]) ** 2)
    capture = kept_mass / max(total, 1e-30)
    return keep, capture


def relaunch_and_measure(
    lat: Lattice3D,
    source_state: np.ndarray,
    det: list[int],
    field: np.ndarray,
    keep_inds: list[int],
    weights: dict[int, float] | None = None,
) -> tuple[np.ndarray, np.ndarray, dict[int, float], dict[int, float], float]:
    init = weighted_state(lat, source_state, keep_inds, weights)
    free, grav = propagate_pair(lat, init, field)
    prof_free = z_profile(free, det, lat.pos, lat.h)
    prof_grav = z_profile(grav, det, lat.pos, lat.h)
    delta = centroid(prof_grav, lat.h) - centroid(prof_free, lat.h)
    return free, grav, prof_free, prof_grav, delta


def evaluate_topn(
    lat: Lattice3D,
    det: list[int],
    source_state: np.ndarray,
    field: np.ndarray,
    n: int,
) -> dict[str, float | int | str]:
    keep1, capture1 = compress_topn(source_state, det, n)
    free1, grav1, prof_free1, prof_grav1, delta1 = relaunch_and_measure(lat, source_state, det, field, keep1)

    keep2, capture2 = compress_topn(grav1, det, n)
    free2, grav2, prof_free2, prof_grav2, delta2 = relaunch_and_measure(lat, grav1, det, field, keep2)

    shift, score = best_shift_score(prof_grav1, prof_grav2, max_shift=MAX_SHIFT)
    width_ratio = spread(prof_grav2, lat.h) / max(spread(prof_grav1, lat.h), 1e-30)

    return {
        "family": "topN",
        "param": n,
        "support1": len(keep1),
        "support2": len(keep2),
        "capture1": capture1,
        "capture2": capture2,
        "delta1": delta1,
        "delta2": delta2,
        "delta_ratio": delta2 / max(delta1, 1e-30),
        "shift": shift,
        "score": score,
        "width_ratio": width_ratio,
        "pass_floor": (
            len(keep1) >= MIN_SUPPORT_BINS
            and len(keep2) >= MIN_SUPPORT_BINS
            and capture1 >= MIN_CAPTURE
            and capture2 >= MIN_CAPTURE
        ),
    }


def evaluate_annulus(
    lat: Lattice3D,
    det: list[int],
    source_state: np.ndarray,
    field: np.ndarray,
    param: str,
) -> dict[str, float | int | str]:
    stage1_probs = np.array([abs(source_state[i]) ** 2 for i in det], dtype=float)
    peak_idx = det[int(stage1_probs.argmax())]
    peak_iy, peak_iz = layer_coords(lat, peak_idx)
    inner, outer = map(int, param.split(":"))

    keep1, capture1 = compress_annulus(lat, source_state, det, peak_iy, peak_iz, inner, outer)
    free1, grav1, prof_free1, prof_grav1, delta1 = relaunch_and_measure(lat, source_state, det, field, keep1)

    stage2_probs = np.array([abs(grav1[i]) ** 2 for i in det], dtype=float)
    peak_idx2 = det[int(stage2_probs.argmax())]
    peak_iy2, peak_iz2 = layer_coords(lat, peak_idx2)
    keep2, capture2 = compress_annulus(lat, grav1, det, peak_iy2, peak_iz2, inner, outer)
    free2, grav2, prof_free2, prof_grav2, delta2 = relaunch_and_measure(lat, grav1, det, field, keep2)

    shift, score = best_shift_score(prof_grav1, prof_grav2, max_shift=MAX_SHIFT)
    width_ratio = spread(prof_grav2, lat.h) / max(spread(prof_grav1, lat.h), 1e-30)

    return {
        "family": "annulus",
        "param": param,
        "support1": len(keep1),
        "support2": len(keep2),
        "capture1": capture1,
        "capture2": capture2,
        "delta1": delta1,
        "delta2": delta2,
        "delta_ratio": delta2 / max(delta1, 1e-30),
        "shift": shift,
        "score": score,
        "width_ratio": width_ratio,
        "pass_floor": (
            len(keep1) >= MIN_SUPPORT_BINS
            and len(keep2) >= MIN_SUPPORT_BINS
            and capture1 >= MIN_CAPTURE
            and capture2 >= MIN_CAPTURE
        ),
    }


def best_candidate(rows: list[dict[str, float | int | str]], family: str) -> dict[str, float | int | str] | None:
    passing = [r for r in rows if str(r["family"]) == family and bool(r["pass_floor"])]
    if not passing:
        return None
    return max(
        passing,
        key=lambda r: (
            float(r["score"]),
            float(r["capture2"]),
            -abs(float(r["delta_ratio"]) - 1.0),
            -float(r["width_ratio"]),
        ),
    )


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]

    source, coord_weight = build_base_surrogate(lat, TOPN_BASE)
    field = surrogate_field(lat, coord_weight, SOURCE_Z, SOURCE_STRENGTH)
    first_segment = lat.propagate(source, np.zeros(lat.n), K, ACTION)
    stage1_probs = np.array([abs(first_segment[i]) ** 2 for i in det], dtype=float)
    peak_idx = det[int(stage1_probs.argmax())]
    peak_iy, peak_iz = layer_coords(lat, peak_idx)

    rows: list[dict[str, float | int | str]] = []
    for n in TOPN_SWEEP:
        rows.append(evaluate_topn(lat, det, first_segment, field, int(n)))
    for param in ANNULAR_SWEEP:
        rows.append(evaluate_annulus(lat, det, first_segment, field, param))

    best_topn = best_candidate(rows, "topN")
    best_annulus = best_candidate(rows, "annulus")
    passing = [r for r in rows if bool(r["pass_floor"])]
    overall_best = max(
        passing,
        key=lambda r: (
            float(r["score"]),
            float(r["capture2"]),
            -abs(float(r["delta_ratio"]) - 1.0),
            -float(r["width_ratio"]),
        ),
    ) if passing else None

    print("=" * 104)
    print("MESOSCOPIC SURROGATE H025 CONSTRAINED LOCALIZATION")
    print("  Final non-degenerate localization attempt on the retained 3D h=0.25 family")
    print(f"  h={H}, W={PHYS_W}, segment_L={PHYS_L}, base_topN={TOPN_BASE}, source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}")
    print(f"  explicit floors: support >= {MIN_SUPPORT_BINS} bins, capture >= {MIN_CAPTURE:.2f} in both stages")
    print(f"  detector-layer peak seed: iy={peak_iy}, iz={peak_iz}")
    print("  Goal: does any non-degenerate annular localization beat the broad top-N control under the same floors?")
    print("=" * 104)
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
    if best_annulus is None:
        print("  annulus: no candidate met the floor")
    else:
        print(
            "  annulus: "
            f"{best_annulus['param']}, capture2={float(best_annulus['capture2']):.3f}, "
            f"score={float(best_annulus['score']):.4f}, width={float(best_annulus['width_ratio']):.3f}"
        )

    print("\nFINAL COMPARISON")
    if best_topn is None or best_annulus is None or overall_best is None:
        print("  comparison unavailable because one side did not meet the floors")
    else:
        improves_score = float(best_annulus["score"]) > float(best_topn["score"]) + 1e-9
        improves_capture = float(best_annulus["capture2"]) >= float(best_topn["capture2"]) - 1e-9
        improves_width = abs(float(best_annulus["width_ratio"]) - 1.0) <= abs(float(best_topn["width_ratio"]) - 1.0)
        meaningful = improves_score and improves_capture and improves_width
        print(
            "  topN benchmark: "
            f"{best_topn['family']} {best_topn['param']} with capture2={float(best_topn['capture2']):.3f}, "
            f"score={float(best_topn['score']):.4f}, width={float(best_topn['width_ratio']):.3f}"
        )
        print(
            "  best annulus: "
            f"{best_annulus['family']} {best_annulus['param']} with capture2={float(best_annulus['capture2']):.3f}, "
            f"score={float(best_annulus['score']):.4f}, width={float(best_annulus['width_ratio']):.3f}"
        )
        print(f"  meaningful improvement over topN: {meaningful}")
        print(
            "  overall best admissible row: "
            f"{overall_best['family']} {overall_best['param']} "
            f"(score={float(overall_best['score']):.4f}, capture2={float(overall_best['capture2']):.3f})"
        )

    print("\nSAFE READ")
    if best_annulus is None:
        print("  - No annular candidate met both floors on the retained h=0.25 family.")
        print("  - Broad topN remains the least-bad admissible mesoscopic control.")
        print("  - The localization lane closes here as a bounded negative result.")
    else:
        print("  - The annular candidates were admissible, but they must still beat topN on the same floors.")
        print("  - If the broad topN control remains the overall best admissible row, the localization lane closes here.")
        print("  - This is the final constrained localization attempt on the retained h=0.25 family.")


if __name__ == "__main__":
    main()
