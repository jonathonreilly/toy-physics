#!/usr/bin/env python3
"""Localization-family sweep for the mesoscopic surrogate lane.

This asks whether a more explicitly localized source family can preserve the
two-stage sourced-response stability already seen for the broad top-N control.

Families compared:
1. top-N compression
2. symmetric square window around the peak bin
3. compact Gaussian ansatz centered at the peak bin

The setup is intentionally the same retained 3D ordered-lattice family as the
other mesoscopic surrogate controls.
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

from scripts.quasi_persistent_relaunch_probe import ACTION, H, PHYS_W, SEGMENT_L, detector_indices, point_source
from scripts.two_body_momentum_harness import K, Lattice3D


TOPN_BASE = 196
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
MAX_SHIFT = 8
TOPN_SWEEP = (9, 25, 49, 81, 121, 144, 169, 196, 225)
SQUARE_SWEEP = tuple(range(0, 9))
GAUSSIAN_SWEEP = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)


def z_profile(amps: np.ndarray, det: list[int], pos: np.ndarray, h: float) -> dict[int, float]:
    profile: dict[int, float] = defaultdict(float)
    for idx in det:
        z_idx = int(round(pos[idx, 2] / h))
        profile[z_idx] += float(abs(amps[idx]) ** 2)
    total = sum(profile.values())
    if total > 0:
        profile = {z: p / total for z, p in profile.items()}
    return dict(sorted(profile.items()))


def centroid(profile: dict[int, float], h: float) -> float:
    total = sum(profile.values())
    if total < 1e-30:
        return 0.0
    return sum((z * h) * p for z, p in profile.items()) / total


def spread(profile: dict[int, float], h: float) -> float:
    total = sum(profile.values())
    if total < 1e-30:
        return 0.0
    mu = centroid(profile, h)
    return math.sqrt(sum((((z * h) - mu) ** 2) * p for z, p in profile.items()) / total)


def best_shift_score(p_a: dict[int, float], p_b: dict[int, float], max_shift: int = MAX_SHIFT) -> tuple[int, float]:
    best_s = 0
    best_score = -1.0
    keys_b = set(p_b.keys())
    for shift in range(-max_shift, max_shift + 1):
        score = 0.0
        keys = set(p_a.keys()) | {k + shift for k in keys_b}
        for k in keys:
            score += math.sqrt(p_a.get(k, 0.0) * p_b.get(k - shift, 0.0))
        if score > best_score:
            best_score = score
            best_s = shift
    return best_s, best_score


def profile_to_init(lat: Lattice3D, profile: dict[int, float]) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    for z_idx, p in profile.items():
        idx = lat.nmap[(0, 0, z_idx)]
        init[idx] = math.sqrt(max(p, 0.0))
    norm = np.sqrt(np.sum(np.abs(init) ** 2))
    if norm > 1e-30:
        init /= norm
    return init


def build_base_surrogate(lat: Lattice3D, topn: int) -> tuple[np.ndarray, dict[tuple[int, int], float]]:
    det = detector_indices(lat)
    source = point_source(lat, 0.0)
    first = lat.propagate(source, np.zeros(lat.n), K, ACTION)
    layer_probs = np.array([abs(first[i]) ** 2 for i in det], dtype=float)
    order = np.argsort(-layer_probs)
    selected = [det[i] for i in order[: min(topn, len(det))]]

    init = np.zeros(lat.n, dtype=np.complex128)
    coord_weight: dict[tuple[int, int], float] = defaultdict(float)
    for idx in selected:
        _, y, z = lat.pos[idx]
        iy = int(round(y / lat.h))
        iz = int(round(z / lat.h))
        init[lat.nmap[(0, iy, iz)]] = first[idx]
        coord_weight[(iy, iz)] += float(abs(first[idx]) ** 2)

    norm = np.sqrt(np.sum(np.abs(init) ** 2))
    if norm > 1e-30:
        init /= norm

    total = sum(coord_weight.values())
    if total > 0:
        coord_weight = {coord: w / total for coord, w in coord_weight.items()}

    return init, dict(coord_weight)


def surrogate_field(lat: Lattice3D, coord_weight: dict[tuple[int, int], float], z_phys: float, strength: float) -> np.ndarray:
    shift = int(round(z_phys / lat.h))
    gl = 2 * lat.nl // 3
    field = np.zeros(lat.n, dtype=float)
    for (iy, iz), weight in coord_weight.items():
        key = (gl, iy, iz + shift)
        if key not in lat.nmap:
            continue
        mi = lat.nmap[key]
        r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
        field += strength * weight / r
    return field


def propagate_pair(lat: Lattice3D, init: np.ndarray, field: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return lat.propagate(init, np.zeros(lat.n), K, ACTION), lat.propagate(init, field, K, ACTION)


def compress_topn(profile: dict[int, float], n: int) -> tuple[dict[int, float], int, float]:
    items = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    keep = items[: min(n, len(items))]
    total = sum(p for _, p in keep)
    capture = total / max(sum(profile.values()), 1e-30)
    return {z: p / total for z, p in keep}, len(keep), capture


def compress_square(profile: dict[int, float], radius: int) -> tuple[dict[int, float], int, float]:
    if not profile:
        return {}, 0, 0.0
    peak_z = max(profile, key=profile.get)
    keep = {z: p for z, p in profile.items() if abs(z - peak_z) <= radius}
    total = sum(keep.values())
    capture = total / max(sum(profile.values()), 1e-30)
    if total > 0:
        keep = {z: p / total for z, p in keep.items()}
    return keep, len(keep), capture


def compress_gaussian(profile: dict[int, float], sigma: float) -> tuple[dict[int, float], int, float]:
    if not profile:
        return {}, 0, 0.0
    peak_z = max(profile, key=profile.get)
    support_radius = max(1, int(math.ceil(3.0 * sigma)))
    weighted = {}
    for z, p in profile.items():
        d = z - peak_z
        if abs(d) > support_radius:
            continue
        mask = math.exp(-0.5 * (d / max(sigma, 1e-30)) ** 2)
        weighted[z] = p * mask
    total = sum(weighted.values())
    capture = total / max(sum(profile.values()), 1e-30)
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
    elif family == "square":
        compressed1, support1, capture1 = compress_square(stage1_profile, int(param))
    elif family == "gaussian":
        compressed1, support1, capture1 = compress_gaussian(stage1_profile, float(param))
    else:
        raise ValueError(f"unknown family: {family}")

    init1 = profile_to_init(lat, compressed1)
    free1, grav1 = propagate_pair(lat, init1, field)
    profile_free1 = z_profile(free1, det, lat.pos, lat.h)
    profile_grav1 = z_profile(grav1, det, lat.pos, lat.h)
    delta1 = centroid(profile_grav1, lat.h) - centroid(profile_free1, lat.h)

    if family == "topN":
        compressed2, support2, capture2 = compress_topn(profile_grav1, int(param))
    elif family == "square":
        compressed2, support2, capture2 = compress_square(profile_grav1, int(param))
    else:
        compressed2, support2, capture2 = compress_gaussian(profile_grav1, float(param))

    init2 = profile_to_init(lat, compressed2)
    free2, grav2 = propagate_pair(lat, init2, field)
    profile_free2 = z_profile(free2, det, lat.pos, lat.h)
    profile_grav2 = z_profile(grav2, det, lat.pos, lat.h)
    delta2 = centroid(profile_grav2, lat.h) - centroid(profile_free2, lat.h)

    shift, score = best_shift_score(profile_grav1, profile_grav2)
    width_ratio = spread(profile_grav2, lat.h) / max(spread(profile_grav1, lat.h), 1e-30)

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
    }


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
    for radius in SQUARE_SWEEP:
        rows.append(evaluate_family(lat, det, stage1_profile, field, "square", radius))
    for sigma in GAUSSIAN_SWEEP:
        rows.append(evaluate_family(lat, det, stage1_profile, field, "gaussian", sigma))

    print("=" * 96)
    print("MESOSCOPIC SURROGATE LOCALIZATION FAMILY SWEEP")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  h={H}, W={PHYS_W}, segment_L={SEGMENT_L}, base_topN={TOPN_BASE}, source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}")
    print("  Goal: can a more localized source family preserve two-stage sourced-response")
    print("        stability as well as, or better than, the broad top-N control?")
    print("=" * 96)
    print()
    print(f"stage-1 baseline centroid shift = {centroid(stage1_profile, lat.h):+.8f}")
    print(f"stage-1 baseline spread         = {spread(stage1_profile, lat.h):.8f}")
    print()
    print(f"{'family':>8s} {'param':>7s} {'supp1':>6s} {'supp2':>6s} {'cap1':>7s} {'cap2':>7s} {'score':>7s} {'wratio':>7s} {'d1':>11s} {'d2':>11s}")
    for row in rows:
        print(
            f"{str(row['family']):>8s} {str(row['param']):>7s} {int(row['support1']):6d} {int(row['support2']):6d}"
            f" {float(row['capture1']):7.3f} {float(row['capture2']):7.3f}"
            f" {float(row['score']):7.4f} {float(row['width_ratio']):7.4f}"
            f" {float(row['delta1']):+11.7f} {float(row['delta2']):+11.7f}"
        )

    def rank_key(row: dict[str, float | int | str]) -> tuple[float, float, int]:
        # Prefer high score, width ratio close to 1, and smaller support.
        return (
            -float(row["score"]),
            abs(float(row["width_ratio"]) - 1.0),
            int(row["support2"]),
        )

    best = min(rows, key=rank_key)
    print()
    print("BEST ROW")
    print(
        f"  {best['family']} {best['param']} with support2={best['support2']}, "
        f"score={float(best['score']):.4f}, width_ratio={float(best['width_ratio']):.4f}, "
        f"capture2={float(best['capture2']):.3f}"
    )

    print("\nSAFE READ")
    print("  - The more localized families can be stable, but the best score/width tradeoff")
    print("    still favors a fairly broad surrogate support.")
    print("  - If a narrower family wins on support, it should show up above with only a")
    print("    modest score penalty; otherwise, top-N remains the least-bad mesoscopic control.")


if __name__ == "__main__":
    main()
