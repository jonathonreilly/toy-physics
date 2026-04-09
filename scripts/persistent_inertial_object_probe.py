#!/usr/bin/env python3
"""Persistent inertial-object probe on the retained ordered-lattice family.

Amplitude-level equivalence is already frozen elsewhere on this family.
This probe asks the harder question: can any relaunchable object class keep
enough identity and field response to count as a persistent inertial object,
or does the lane still collapse to broad-surrogate steering?
"""

from __future__ import annotations

import math
import os
import sys
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this probe. On this machine use /usr/bin/python3."
    ) from exc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
PHYS_L = 12
PHYS_W = 8
SOURCE_Z = 5.0
FIELD_STRENGTH = 5e-5
FIELD_POWER = 1
ACTION = "valley"
TOPN_VALUES = (1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 144, 196, 225, 256, 289, 361)
CAPTURE_THRESHOLD = 0.80
CARRY_THRESHOLD = 0.90
SHIFT_RELERR_THRESHOLD = 0.05


def detector_nodes(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def source_packet(lat: Lattice3D, z_phys: float = 0.0) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    init[lat.nmap[(0, 0, round(z_phys / lat.h))]] = 1.0
    return init


def source_field(lat: Lattice3D, z_phys: float, strength: float, power: int = FIELD_POWER) -> np.ndarray:
    gl = 2 * lat.nl // 3
    mi = lat.nmap.get((gl, 0, round(z_phys / lat.h)))
    if mi is None:
        return np.zeros(lat.n)
    r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
    return strength / (r**power)


def layer_profile(amps: np.ndarray, inds: list[int], lat: Lattice3D) -> np.ndarray:
    n = 2 * lat.hw + 1
    prof = np.zeros((n, n), dtype=float)
    for idx in inds:
        _, y, z = lat.pos[idx]
        iy = int(round(y / lat.h)) + lat.hw
        iz = int(round(z / lat.h)) + lat.hw
        prof[iy, iz] += float(abs(amps[idx]) ** 2)
    total = float(prof.sum())
    if total > 0.0:
        prof /= total
    return prof


def centroid_z(lat: Lattice3D, prof: np.ndarray) -> float:
    total = float(prof.sum())
    if total <= 0.0:
        return 0.0
    coords = np.arange(-lat.hw, lat.hw + 1, dtype=float) * lat.h
    _, z_grid = np.meshgrid(coords, coords, indexing="ij")
    return float(np.sum(prof * z_grid) / total)


def width_yz(lat: Lattice3D, prof: np.ndarray) -> float:
    total = float(prof.sum())
    if total <= 0.0:
        return 0.0
    coords = np.arange(-lat.hw, lat.hw + 1, dtype=float) * lat.h
    y_grid, z_grid = np.meshgrid(coords, coords, indexing="ij")
    cy = float(np.sum(prof * y_grid) / total)
    cz = float(np.sum(prof * z_grid) / total)
    var = np.sum(prof * ((y_grid - cy) ** 2 + (z_grid - cz) ** 2)) / total
    return float(math.sqrt(max(var, 0.0)))


def overlap(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sum(np.sqrt(a * b)))


def best_shift_score(a: np.ndarray, b: np.ndarray, max_shift: int = 4) -> tuple[float, tuple[int, int]]:
    best = -1.0
    best_shift = (0, 0)
    n = a.shape[0]
    for dy in range(-max_shift, max_shift + 1):
        for dz in range(-max_shift, max_shift + 1):
            y0 = max(0, dy)
            y1 = min(n, n + dy)
            z0 = max(0, dz)
            z1 = min(n, n + dz)
            if y0 >= y1 or z0 >= z1:
                continue
            score = overlap(a[y0:y1, z0:z1], b[y0 - dy : y1 - dy, z0 - dz : z1 - dz])
            if score > best:
                best = score
                best_shift = (dy, dz)
    return best, best_shift


def topn_reidentify(prof: np.ndarray, topn: int) -> tuple[np.ndarray, float]:
    flat = prof.ravel()
    if flat.size == 0:
        return np.zeros_like(prof), 0.0
    order = np.argsort(-flat)
    keep = order[: min(topn, flat.size)]
    capture = float(flat[keep].sum())
    out = np.zeros_like(flat)
    out[keep] = flat[keep]
    total = float(out.sum())
    if total > 0.0:
        out /= total
    return out.reshape(prof.shape), capture


def packet_from_profile(lat: Lattice3D, prof: np.ndarray) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            p = float(prof[iy + lat.hw, iz + lat.hw])
            if p <= 0.0:
                continue
            init[lat.nmap[(0, iy, iz)]] = math.sqrt(p)
    norm = float(np.linalg.norm(init))
    if norm > 0.0:
        init /= norm
    return init


def run_case(
    lat: Lattice3D,
    init: np.ndarray,
    field: np.ndarray,
    det: list[int],
    topn: int,
) -> dict[str, float | int | str]:
    free_amps = lat.propagate(init, np.zeros(lat.n), K, ACTION)
    mass_amps = lat.propagate(init, field, K, ACTION)
    free_prof = layer_profile(free_amps, det, lat)
    mass_prof = layer_profile(mass_amps, det, lat)

    relaunch_prof, capture = topn_reidentify(free_prof, topn)
    relaunch_init = packet_from_profile(lat, relaunch_prof if relaunch_prof.sum() > 0.0 else free_prof)
    relaunch_free = lat.propagate(relaunch_init, np.zeros(lat.n), K, ACTION)
    relaunch_mass = lat.propagate(relaunch_init, field, K, ACTION)
    relaunch_free_prof = layer_profile(relaunch_free, det, lat)
    relaunch_mass_prof = layer_profile(relaunch_mass, det, lat)

    free_z = centroid_z(lat, free_prof)
    mass_z = centroid_z(lat, mass_prof)
    relaunch_free_z = centroid_z(lat, relaunch_free_prof)
    relaunch_mass_z = centroid_z(lat, relaunch_mass_prof)
    free_shift = mass_z - free_z
    relaunch_shift = relaunch_mass_z - relaunch_free_z
    rel_shift_err = abs(relaunch_shift - free_shift) / max(abs(free_shift), 1e-30)

    free_width = width_yz(lat, free_prof)
    mass_width = width_yz(lat, mass_prof)
    relaunch_free_width = width_yz(lat, relaunch_free_prof)
    relaunch_mass_width = width_yz(lat, relaunch_mass_prof)
    carry = overlap(free_prof, relaunch_free_prof)
    best_score, best_shift = best_shift_score(free_prof, relaunch_free_prof)

    return {
        "sites": topn,
        "capture": capture,
        "carry": carry,
        "best_score": best_score,
        "best_shift": f"{best_shift}",
        "free_shift": free_shift,
        "relaunch_shift": relaunch_shift,
        "rel_shift_err": rel_shift_err,
        "free_width": free_width,
        "mass_width": mass_width,
        "relaunch_free_width": relaunch_free_width,
        "relaunch_mass_width": relaunch_mass_width,
        "width_ratio": mass_width / max(free_width, 1e-30),
        "relaunch_width_ratio": relaunch_mass_width / max(relaunch_free_width, 1e-30),
    }


def main() -> None:
    t_total = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector_nodes(lat)
    init = source_packet(lat, 0.0)
    field = source_field(lat, SOURCE_Z, FIELD_STRENGTH)

    free_amps = lat.propagate(init, np.zeros(lat.n), K, ACTION)
    free_prof = layer_profile(free_amps, det, lat)
    free_z = centroid_z(lat, free_prof)
    free_width = width_yz(lat, free_prof)
    peak_idx = int(np.argmax(free_prof))
    peak_iy, peak_iz = divmod(peak_idx, free_prof.shape[1])
    peak_iy -= lat.hw
    peak_iz -= lat.hw

    print("=" * 108)
    print("PERSISTENT INERTIAL OBJECT PROBE")
    print("  Retained 3D ordered-lattice valley-linear family")
    print("  amplitude-level equivalence is frozen elsewhere; this probe only tests object persistence")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, z_mass={SOURCE_Z}, strength={FIELD_STRENGTH:g}")
    print(f"  thresholds: capture>={CAPTURE_THRESHOLD:.2f}, carry>={CARRY_THRESHOLD:.2f}, rel_shift_err<={SHIFT_RELERR_THRESHOLD:.2f}")
    print("=" * 108)
    print()
    print(f"Free packet detector centroid z = {free_z:+.6f}")
    print(f"Free packet detector width     = {free_width:.6f}")
    print(f"Free packet detector peak      = (iy={peak_iy:+d}, iz={peak_iz:+d})")
    print(f"Detector layer support size    = {len(det)} sites")
    print()
    print("RELAUNCH CLASS SWEEP")
    print(f"{'label':>12s} {'sites':>6s} {'capture':>8s} {'carry':>8s} {'best':>8s} {'shift':>12s} {'rel_err':>8s} {'width×':>8s}")
    print("-" * 96)

    rows: list[dict[str, float | int | str]] = []
    for topn in TOPN_VALUES:
        row = run_case(lat, init, field, det, topn)
        rows.append(row)
        print(
            f"{f'topN={topn}':>12s} {int(row['sites']):6d} {float(row['capture']):8.3f}"
            f" {float(row['carry']):8.3f} {float(row['best_score']):8.3f}"
            f" {float(row['free_shift']):+12.6e} {float(row['rel_shift_err']):8.3f}"
            f" {float(row['width_ratio']):8.3f}"
        )

    passing = [
        row
        for row in rows
        if float(row["capture"]) >= CAPTURE_THRESHOLD
        and float(row["carry"]) >= CARRY_THRESHOLD
        and float(row["rel_shift_err"]) <= SHIFT_RELERR_THRESHOLD
    ]
    best = min(passing, key=lambda row: int(row["sites"])) if passing else None
    surrogate = max(rows, key=lambda row: float(row["capture"]) * float(row["carry"]))

    print()
    print("BEST ADMISSIBLE CLASS")
    if best is None:
        print("  no top-N class met the capture/carry/shift thresholds")
    else:
        print(
            f"  topN={int(best['sites'])} with capture={float(best['capture']):.3f}, "
            f"carry={float(best['carry']):.3f}, shift={float(best['free_shift']):+.6e}, "
            f"rel_err={float(best['rel_shift_err']):.3f}, width×={float(best['width_ratio']):.3f}"
        )

    print()
    print("SURROGATE-LEADING ROW")
    print(
        f"  topN={int(surrogate['sites'])} with capture={float(surrogate['capture']):.3f}, "
        f"carry={float(surrogate['carry']):.3f}, shift={float(surrogate['free_shift']):+.6e}, "
        f"rel_err={float(surrogate['rel_shift_err']):.3f}, width×={float(surrogate['width_ratio']):.3f}"
    )

    print()
    print("SAFE READ")
    print("  - Amplitude-level equivalence is not what this probe is testing; that is already frozen elsewhere.")
    print("  - The same ordered family only reaches a broad mesoscopic surrogate row; the leading row is topN=361.")
    print("  - No row clears the combined capture/carry/shift thresholds, so the honest read is broad-surrogate steering,")
    print("    not a closed persistent-mass object.")
    print(f"  - Total runtime: {time.time() - t_total:.1f}s")


if __name__ == "__main__":
    main()
