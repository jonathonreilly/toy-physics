#!/usr/bin/env python3
"""Localization frontier for the mesoscopic two-stage source surrogate.

This probe maps the tradeoff between source compactness and multistage
stability on the retained 3D ordered-lattice family.

The key question is not just "does the surrogate survive two stages?" but:

- how does two-stage self-similarity change as the broad source is shrunk?
- how much source strength is lost as the source becomes more localized?

The expected outcome is a frontier rather than a single threshold.
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


SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
TOPNS = (9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256)
MAX_SHIFT = 8


def z_profile(lat: Lattice3D, det: list[int], amps: np.ndarray) -> dict[int, float]:
    profile: dict[int, float] = defaultdict(float)
    for idx in det:
        z_idx = int(round(lat.pos[idx, 2] / lat.h))
        profile[z_idx] += float(abs(amps[idx]) ** 2)
    total = sum(profile.values())
    if total > 0:
        profile = {z: p / total for z, p in profile.items()}
    return dict(sorted(profile.items()))


def centroid(lat: Lattice3D, profile: dict[int, float]) -> float:
    total = sum(profile.values())
    if total < 1e-30:
        return 0.0
    return sum((z * lat.h) * p for z, p in profile.items()) / total


def spread(lat: Lattice3D, profile: dict[int, float]) -> float:
    total = sum(profile.values())
    if total < 1e-30:
        return 0.0
    mu = centroid(lat, profile)
    return math.sqrt(sum((((z * lat.h) - mu) ** 2) * p for z, p in profile.items()) / total)


def best_shift_score(a: dict[int, float], b: dict[int, float], max_shift: int = MAX_SHIFT) -> tuple[int, float]:
    best_shift = 0
    best_score = -1.0
    b_keys = set(b.keys())
    for shift in range(-max_shift, max_shift + 1):
        score = 0.0
        keys = set(a.keys()) | {k + shift for k in b_keys}
        for key in keys:
            score += math.sqrt(a.get(key, 0.0) * b.get(key - shift, 0.0))
        if score > best_score:
            best_score = score
            best_shift = shift
    return best_shift, best_score


def build_base(lat: Lattice3D, topn: int) -> tuple[np.ndarray, dict[tuple[int, int], float]]:
    det = detector_indices(lat)
    src = point_source(lat, 0.0)
    first = lat.propagate(src, np.zeros(lat.n), K, ACTION)
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


def reidentify_topn(lat: Lattice3D, det: list[int], amps: np.ndarray, topn: int) -> tuple[np.ndarray, float]:
    layer_probs = np.array([abs(amps[i]) ** 2 for i in det], dtype=float)
    total = layer_probs.sum()
    order = np.argsort(-layer_probs)
    selected = [det[i] for i in order[: min(topn, len(det))]]
    capture = float(sum(abs(amps[i]) ** 2 for i in selected) / max(total, 1e-30))

    init = np.zeros(lat.n, dtype=np.complex128)
    for idx in selected:
        _, y, z = lat.pos[idx]
        iy = int(round(y / lat.h))
        iz = int(round(z / lat.h))
        init[lat.nmap[(0, iy, iz)]] = amps[idx]
    norm = np.sqrt(np.sum(np.abs(init) ** 2))
    if norm > 1e-30:
        init /= norm

    return init, capture


def propagate_pair(lat: Lattice3D, init: np.ndarray, field: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return lat.propagate(init, np.zeros(lat.n), K, ACTION), lat.propagate(init, field, K, ACTION)


def main() -> None:
    lat = Lattice3D(SEGMENT_L, PHYS_W, H)
    det = detector_indices(lat)

    print("=" * 100)
    print("MESOSCOPIC SURROGATE LOCALIZATION FRONTIER")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  h={H}, W={PHYS_W}, segment_L={SEGMENT_L}, source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}")
    print("  Goal: map the tradeoff between source compactness and two-stage")
    print("        sourced-response stability")
    print("=" * 100)
    print()
    print(f"{'topN':>5s} {'cap1':>6s} {'cap2':>6s} {'delta1':>11s} {'delta2':>11s} {'ratio':>6s} {'shift':>5s} {'score':>7s} {'w2/w1':>7s}")

    for topn in TOPNS:
        init0, coord_weight = build_base(lat, topn)
        field = surrogate_field(lat, coord_weight, SOURCE_Z, SOURCE_STRENGTH)

        free1, grav1 = propagate_pair(lat, init0, field)
        init1, cap1 = reidentify_topn(lat, det, grav1, topn)
        free2, grav2 = propagate_pair(lat, init1, field)
        _, cap2 = reidentify_topn(lat, det, grav2, topn)

        p1f = z_profile(lat, det, free1)
        p1g = z_profile(lat, det, grav1)
        p2f = z_profile(lat, det, free2)
        p2g = z_profile(lat, det, grav2)

        delta1 = centroid(lat, p1g) - centroid(lat, p1f)
        delta2 = centroid(lat, p2g) - centroid(lat, p2f)
        ratio = delta2 / max(delta1, 1e-30)
        shift, score = best_shift_score(p1g, p2g)
        width_ratio = spread(lat, p2g) / max(spread(lat, p1g), 1e-30)

        print(
            f"{topn:5d} {cap1:6.3f} {cap2:6.3f} {delta1:+11.8f} {delta2:+11.8f}"
            f" {ratio:6.3f} {shift:5d} {score:7.4f} {width_ratio:7.4f}"
        )

    print("\nSAFE READ")
    print("  - There need not be a single collapse threshold.")
    print("  - Small sources can remain self-similar across two stages while becoming weak.")
    print("  - Larger sources can carry stronger response while remaining mesoscopic.")
    print("  - This probe is about the localization/strength frontier, not persistent mass.")


if __name__ == "__main__":
    main()
