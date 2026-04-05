#!/usr/bin/env python3
"""Compare a broad surrogate source against an equivalent point source.

This probe asks a narrow interpretive question on the retained 3D ordered
lattice family:

If we source a weak field from the broad relaunch surrogate found in the
quasi-persistent controls, does it behave like a soft point source, or does
its distributed structure materially matter?

The test is deliberately bounded:
1. construct a broad surrogate source from a detector-layer packet profile
2. construct an equivalent-strength point source at the same centroid
3. compare the downstream response of a fixed test packet

The comparison is done on the retained valley-linear ordered-lattice family.
"""

from __future__ import annotations

import math
import os
import sys

try:
    import numpy as np
except ModuleNotFoundError:
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit("numpy is required for this harness. On this machine use /usr/bin/python3.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
PHYS_L = 12
PHYS_W = 8
FIELD_POWER = 1
FIELD_STRENGTH = 5e-5
SOURCE_Z = 5.0
SURROGATE_WEIGHTS = {
    -2: 0.10,
    -1: 0.40,
    0: 1.00,
    1: 0.40,
    2: 0.10,
}
TOPK = 5
KERNEL_LABEL = "valley"
PROBE_ZS = (0.0, 1.0, 2.0, -1.0, -2.0)


def detector_nodes(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def source_packet(lat: Lattice3D, weights: dict[int, float]) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    norm = math.sqrt(sum(w * w for w in weights.values()))
    for z_idx, weight in weights.items():
        idx = lat.nmap[(0, 0, z_idx)]
        init[idx] = weight / norm
    return init


def z_profile(amps: np.ndarray, det: list[int], pos: np.ndarray, h: float) -> dict[int, float]:
    profile: dict[int, float] = {}
    for d in det:
        z_idx = int(round(pos[d, 2] / h))
        profile[z_idx] = profile.get(z_idx, 0.0) + float(abs(amps[d]) ** 2)
    total = sum(profile.values())
    if total > 0:
        profile = {k: v / total for k, v in profile.items()}
    return dict(sorted(profile.items()))


def profile_centroid(profile: dict[int, float], h: float) -> float:
    total = sum(profile.values())
    if total <= 0:
        return 0.0
    return sum((z * h) * p for z, p in profile.items()) / total


def field_from_profile(lat: Lattice3D, profile: dict[int, float], strength: float, power: int = FIELD_POWER) -> np.ndarray:
    gl = 2 * lat.nl // 3
    field = np.zeros(lat.n)
    total = sum(profile.values())
    if total <= 0:
        return field
    for z_idx, frac in profile.items():
        mi = lat.nmap.get((gl, 0, z_idx))
        if mi is None:
            continue
        r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
        field += (strength * frac) / (r ** power)
    return field


def point_source_from_centroid(lat: Lattice3D, centroid_z: float, strength: float, power: int = FIELD_POWER) -> np.ndarray:
    gl = 2 * lat.nl // 3
    z_idx = round(centroid_z / lat.h)
    mi = lat.nmap.get((gl, 0, z_idx))
    if mi is None:
        return np.zeros(lat.n)
    r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
    return strength / (r ** power)


def layer_distribution(lat: Lattice3D, amps: np.ndarray, layer: int) -> np.ndarray:
    n = 2 * lat.hw + 1
    dist = np.zeros((n, n), dtype=float)
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap[(layer, iy, iz)]
            dist[iy + lat.hw, iz + lat.hw] = abs(amps[idx]) ** 2
    total = dist.sum()
    if total > 1e-30:
        dist /= total
    return dist


def centroid_yz(lat: Lattice3D, dist: np.ndarray) -> tuple[float, float]:
    coords = np.arange(-lat.hw, lat.hw + 1, dtype=float) * lat.h
    y_grid, z_grid = np.meshgrid(coords, coords, indexing="ij")
    total = dist.sum()
    if total < 1e-30:
        return 0.0, 0.0
    cy = float(np.sum(dist * y_grid) / total)
    cz = float(np.sum(dist * z_grid) / total)
    return cy, cz


def width_yz(lat: Lattice3D, dist: np.ndarray) -> float:
    cy, cz = centroid_yz(lat, dist)
    coords = np.arange(-lat.hw, lat.hw + 1, dtype=float) * lat.h
    y_grid, z_grid = np.meshgrid(coords, coords, indexing="ij")
    total = dist.sum()
    if total < 1e-30:
        return 0.0
    var = np.sum(dist * ((y_grid - cy) ** 2 + (z_grid - cz) ** 2)) / total
    return float(math.sqrt(max(var, 0.0)))


def overlap_score(a: np.ndarray, b: np.ndarray) -> float:
    flat_a = a.ravel()
    flat_b = b.ravel()
    denom = math.sqrt(float(np.dot(flat_a, flat_a) * np.dot(flat_b, flat_b)))
    if denom < 1e-30:
        return 0.0
    return float(np.dot(flat_a, flat_b) / denom)


def shifted_overlap(a: np.ndarray, b: np.ndarray, dy: int, dz: int) -> float:
    n = a.shape[0]
    y0 = max(0, dy)
    y1 = min(n, n + dy)
    z0 = max(0, dz)
    z1 = min(n, n + dz)
    if y0 >= y1 or z0 >= z1:
        return 0.0
    a_slice = a[y0:y1, z0:z1]
    b_slice = b[y0 - dy:y1 - dy, z0 - dz:z1 - dz]
    return overlap_score(a_slice, b_slice)


def best_shift_match(free_dist: np.ndarray, field_dist: np.ndarray) -> tuple[float, tuple[int, int]]:
    best = -1.0
    best_shift = (0, 0)
    for dy in range(-4, 5):
        for dz in range(-4, 5):
            score = shifted_overlap(free_dist, field_dist, dy, dz)
            if score > best:
                best = score
                best_shift = (dy, dz)
    return best, best_shift


def make_summary_row(lat: Lattice3D, free_dist: np.ndarray, field_dist: np.ndarray) -> tuple[float, float, float, float, tuple[int, int]]:
    free_cy, free_cz = centroid_yz(lat, free_dist)
    field_cy, field_cz = centroid_yz(lat, field_dist)
    free_w = width_yz(lat, free_dist)
    field_w = width_yz(lat, field_dist)
    best_score, best_shift = best_shift_match(free_dist, field_dist)
    return (
        field_cy - free_cy,
        field_cz - free_cz,
        field_w / free_w if free_w > 1e-30 else 0.0,
        best_score,
        best_shift,
    )


def source_field(lat: Lattice3D, field_strength: float) -> np.ndarray:
    source = point_source_from_centroid(lat, SOURCE_Z, field_strength)
    return source


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector_nodes(lat)
    broad_packet = source_packet(lat, SURROGATE_WEIGHTS)
    broad_profile = z_profile(lat.propagate(broad_packet, np.zeros(lat.n), K, KERNEL_LABEL), det, lat.pos, lat.h)

    broad_centroid = profile_centroid(broad_profile, lat.h)
    broad_field = field_from_profile(lat, broad_profile, FIELD_STRENGTH)
    point_field = point_source_from_centroid(lat, broad_centroid, FIELD_STRENGTH)

    probe_rows = []
    for probe_z in PROBE_ZS:
        test_packet = source_packet(lat, {round(probe_z / H): 1.0})
        free = np.zeros(lat.n)
        test_free = lat.propagate(test_packet, free, K, KERNEL_LABEL)
        broad_resp = lat.propagate(test_packet, broad_field, K, KERNEL_LABEL)
        point_resp = lat.propagate(test_packet, point_field, K, KERNEL_LABEL)

        free_dist = layer_distribution(lat, test_free, lat.nl - 1)
        broad_dist = layer_distribution(lat, broad_resp, lat.nl - 1)
        point_dist = layer_distribution(lat, point_resp, lat.nl - 1)

        broad_delta = make_summary_row(lat, free_dist, broad_dist)
        point_delta = make_summary_row(lat, free_dist, point_dist)

        broad_score = best_shift_match(free_dist, broad_dist)[0]
        point_score = best_shift_match(free_dist, point_dist)[0]
        tv_broad_point = 0.5 * np.abs(broad_dist - point_dist).sum()
        probe_rows.append(
            {
                "probe_z": probe_z,
                "broad_delta": broad_delta,
                "point_delta": point_delta,
                "broad_score": broad_score,
                "point_score": point_score,
                "tv_broad_point": tv_broad_point,
            }
        )

    print("=" * 92)
    print("BROAD SURROGATE VS POINT SOURCE COMPARISON")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, source_z={SOURCE_Z}, strength={FIELD_STRENGTH:g}")
    print("  Goal: does the broad surrogate behave like a soft point source, or does")
    print("        its distributed structure materially matter?")
    print("=" * 92)
    print()
    print(f"Broad surrogate centroid z = {broad_centroid:+.4f}")
    print(f"Broad surrogate support bins = {len(broad_profile)}")
    print(f"Broad surrogate field built from {len(broad_profile)} z-bins at the detector layer")
    print()
    print(f"{'probe_z':>8s} {'case':>14s} {'dcy':>9s} {'dcz':>9s} {'width×':>8s} {'best_score':>11s} {'best_shift':>12s}")
    print("-" * 86)
    for row in probe_rows:
        probe_z = row["probe_z"]
        broad_delta = row["broad_delta"]
        point_delta = row["point_delta"]
        print(
            f"{probe_z:8.1f} {'broad':>14s} {broad_delta[0]:+9.4f} {broad_delta[1]:+9.4f}"
            f" {broad_delta[2]:8.3f} {broad_delta[3]:11.3f} {str(broad_delta[4]):>12s}"
        )
        print(
            f"{probe_z:8.1f} {'point':>14s} {point_delta[0]:+9.4f} {point_delta[1]:+9.4f}"
            f" {point_delta[2]:8.3f} {point_delta[3]:11.3f} {str(point_delta[4]):>12s}"
        )
        print(
            f"{'':8s} {'TV(b,p)':>14s} {'':>9s} {'':>9s} {'':>8s}"
            f" {row['tv_broad_point']:11.6f} {'':>12s}"
        )
    print()
    print(f"best-shift score broad = {max(row['broad_score'] for row in probe_rows):.3f}")
    print(f"best-shift score point = {max(row['point_score'] for row in probe_rows):.3f}")
    print(f"max TV distance broad vs point = {max(row['tv_broad_point'] for row in probe_rows):.6f}")
    print()
    print("SAFE READ")
    print("  - If the broad and point responses are close, the surrogate acts like a soft point source.")
    print("  - If the TV distance stays large or the shift differs materially, the distributed structure matters.")
    print("  - This is an interpretive diagnostic, not a new inertial theorem.")


if __name__ == "__main__":
    main()
