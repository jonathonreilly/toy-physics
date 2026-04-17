#!/usr/bin/env python3
"""Bounded packet re-identification control on the retained 3D ordered lattice.

This is the smallest honest control for the persistent-pattern / inertial-
response lane.

Question:
  Can a localized packet on the retained ordered-lattice family be
  re-identified well enough after propagation to support any inertial-response
  claim?

What it measures:
  - centroid shift relative to free propagation
  - width change relative to free propagation
  - best-shift similarity against the free packet shape

This is a control / diagnostic, not a persistent-particle theorem.
"""

from __future__ import annotations

import math
import os
import sys

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this harness. On this machine use /usr/bin/python3."
    ) from exc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
PHYS_L = 12
PHYS_W = 8
SOURCE_Z = 5.0
PACKET_SIGMA = 1.25
FIELD_STRENGTHS = (2e-5, 5e-5, 1e-4)
LAYER_SAMPLES = (4, 8, 12, 16, 20, 24)
ACTIONS = ("valley", "spent_delay")
MAX_SHIFT = 4


def gaussian_packet(lat: Lattice3D, sigma: float = PACKET_SIGMA) -> np.ndarray:
    """Localized initial packet on the source layer."""

    init = np.zeros(lat.n, dtype=np.complex128)
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap[(0, iy, iz)]
            y = iy * lat.h
            z = iz * lat.h
            weight = math.exp(-0.5 * (y * y + z * z) / (sigma * sigma))
            init[idx] = weight
    norm = np.linalg.norm(init)
    if norm < 1e-30:
        return init
    return init / norm


def source_field(lat: Lattice3D, z_phys: float, strength: float) -> np.ndarray:
    """Weak external field used for the re-identification control."""

    gl = 2 * lat.nl // 3
    mi = lat.nmap.get((gl, 0, round(z_phys / lat.h)))
    if mi is None:
        return np.zeros(lat.n)
    r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
    return strength / r


def layer_distribution(lat: Lattice3D, amps: np.ndarray, layer: int) -> np.ndarray:
    """Return a normalized y-z probability matrix for one x-layer."""

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
    n = dist.shape[0]
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
    for dy in range(-MAX_SHIFT, MAX_SHIFT + 1):
        for dz in range(-MAX_SHIFT, MAX_SHIFT + 1):
            score = shifted_overlap(free_dist, field_dist, dy, dz)
            if score > best:
                best = score
                best_shift = (dy, dz)
    return best, best_shift


def make_summary_row(
    lat: Lattice3D,
    free_dist: np.ndarray,
    field_dist: np.ndarray,
    label: str,
) -> tuple[float, float, float, float, float, tuple[int, int]]:
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
        free_w,
        field_w,
        best_shift,
    )


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    init = gaussian_packet(lat)
    field = source_field(lat, SOURCE_Z, FIELD_STRENGTHS[1])
    free_field = np.zeros(lat.n)

    print("=" * 92)
    print("ORDERED-LATTICE PACKET RE-IDENTIFICATION CONTROL")
    print("  Localized packet vs free baseline on the retained 3D ordered family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, sigma={PACKET_SIGMA}, source_z={SOURCE_Z}")
    print("  Goal: can we re-identify the packet well enough to support any inertial-response claim?")
    print("=" * 92)
    print()

    for action in ACTIONS:
        print(f"ACTION: {action}")
        print(
            f"{'strength':>10s} {'layer':>6s} {'dcy':>9s} {'dcz':>9s} "
            f"{'width×':>8s} {'best_score':>11s} {'best_shift':>12s}"
        )
        print("-" * 72)

        free_amps = lat.propagate(init, free_field, K, action)
        for strength in FIELD_STRENGTHS:
            field = source_field(lat, SOURCE_Z, strength)
            amps = lat.propagate(init, field, K, action)
            rows = []
            for layer in LAYER_SAMPLES:
                free_dist = layer_distribution(lat, free_amps, layer)
                field_dist = layer_distribution(lat, amps, layer)
                dcy, dcz, width_ratio, score, free_w, field_w, best_shift = make_summary_row(
                    lat, free_dist, field_dist, action
                )
                rows.append((score, width_ratio))
                print(
                    f"{strength:10.0e} {layer:6d} {dcy:+9.4f} {dcz:+9.4f} "
                    f"{width_ratio:8.3f} {score:11.3f} {str(best_shift):>12s}"
                )
            mean_score = sum(s for s, _ in rows) / len(rows)
            mean_width = sum(w for _, w in rows) / len(rows)
            print(f"  summary: mean best-score={mean_score:.3f}, mean width ratio={mean_width:.3f}")
        print()

    print("SAFE READ")
    print("  - If the best-shift score stays high while width ratio stays near 1,")
    print("    the packet is re-identifiable enough to support a bounded inertial-response control.")
    print("  - If the score is low or width blows up, the codebase still lacks a usable persistent-pattern probe.")
    print("  - This is a diagnostic only; it does not create a persistent-mass theorem.")


if __name__ == "__main__":
    main()
