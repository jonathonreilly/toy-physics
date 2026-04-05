#!/usr/bin/env python3
"""Two-stage sourced-response probe for the mesoscopic surrogate lane.

This is the next bounded step after the one-step backreaction harness.

It asks:
1. start from the frozen broad top-N relaunch surrogate
2. propagate it through a weak field sourced by another broad surrogate
3. re-identify the output as the next-stage surrogate
4. repeat one more sourced stage

If the stage-2 response still looks like the stage-1 response up to a small
best-shift and width change, then the broad surrogate survives at least two
sourced-response stages as a mesoscopic control object.
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


TOPN = 196
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
MAX_SHIFT = 8


def detector_probs(amps: np.ndarray, det: list[int]) -> np.ndarray:
    probs = np.array([abs(amps[i]) ** 2 for i in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return probs
    return probs / total


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


def reidentify_topn(lat: Lattice3D, amps: np.ndarray, det: list[int], topn: int) -> tuple[np.ndarray, float]:
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
    init0, coord_weight = build_base_surrogate(lat, TOPN)
    field = surrogate_field(lat, coord_weight, SOURCE_Z, SOURCE_STRENGTH)

    free1, grav1 = propagate_pair(lat, init0, field)
    init1, capture1 = reidentify_topn(lat, grav1, det, TOPN)
    free2, grav2 = propagate_pair(lat, init1, field)
    _, capture2 = reidentify_topn(lat, grav2, det, TOPN)

    p1f = z_profile(free1, det, lat.pos, lat.h)
    p1g = z_profile(grav1, det, lat.pos, lat.h)
    p2f = z_profile(free2, det, lat.pos, lat.h)
    p2g = z_profile(grav2, det, lat.pos, lat.h)

    delta1 = centroid(p1g, lat.h) - centroid(p1f, lat.h)
    delta2 = centroid(p2g, lat.h) - centroid(p2f, lat.h)
    shift, score = best_shift_score(p1g, p2g)
    width_ratio = spread(p2g, lat.h) / max(spread(p1g, lat.h), 1e-30)

    print("=" * 96)
    print("MESOSCOPIC SURROGATE MULTI-STAGE PROBE")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  h={H}, W={PHYS_W}, segment_L={SEGMENT_L}, topN={TOPN}, source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}")
    print("  Goal: does the broad surrogate survive two sourced-response stages?")
    print("=" * 96)
    print()
    print(f"stage-1 capture          = {capture1:.3f}")
    print(f"stage-2 capture          = {capture2:.3f}")
    print(f"stage-1 delta            = {delta1:+.8f}")
    print(f"stage-2 delta            = {delta2:+.8f}")
    print(f"delta ratio              = {delta2 / max(delta1, 1e-30):.3f}")
    print(f"best-shift stage2 vs 1   = {shift:+d}")
    print(f"best-shift score         = {score:.4f}")
    print(f"width ratio stage2/stage1= {width_ratio:.4f}")
    print()
    print("SAFE READ")
    print("  - High best-shift score and near-unit width ratio mean the mesoscopic surrogate")
    print("    survives a second sourced-response stage as the same broad object family.")
    print("  - Large score loss, width blow-up, or delta collapse would mean the surrogate")
    print("    is only a one-step control.")


if __name__ == "__main__":
    main()
