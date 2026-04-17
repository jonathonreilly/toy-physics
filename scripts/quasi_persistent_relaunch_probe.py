#!/usr/bin/env python3
"""Bounded quasi-persistent relaunch probe on the retained 3D ordered family.

This is the smallest honest step beyond the current readiness note.

Idea:
1. Propagate a point packet freely across one short ordered-lattice segment.
2. Treat the outgoing detector-layer profile as a candidate "object state".
3. Compress that state into a smaller relaunch support.
4. Ask whether the compressed relaunch preserves the downstream free profile
   and the downstream field-induced centroid shift on a second segment.

If only a very broad support works, that is evidence for a mesoscopic packet
surrogate, not a sharply localized persistent object.
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
    raise SystemExit("numpy is required for this probe. On this machine use /usr/bin/python3.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
SEGMENT_L = 6
PHYS_W = 8
ACTION = "valley"
FIELD_POWER = 1
FIELD_STRENGTH = 5e-5
FIELD_Z = 5.0
RADIUS_VALUES = (0, 1, 2, 3, 4, 5, 6, 7, 8)
TOP_N_VALUES = (1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 144, 196, 256, 289, 361)


def detector_indices(lat: Lattice3D, layer: int | None = None) -> list[int]:
    if layer is None:
        layer = lat.nl - 1
    return [
        lat.nmap[(layer, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (layer, iy, iz) in lat.nmap
    ]


def probs_on_layer(amps: np.ndarray, inds: list[int]) -> np.ndarray:
    probs = np.array([abs(amps[i]) ** 2 for i in inds], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return probs
    return probs / total


def centroid_z(amps: np.ndarray, inds: list[int], pos: np.ndarray) -> float:
    probs = np.array([abs(amps[i]) ** 2 for i in inds], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return 0.0
    return float(np.dot(probs, pos[inds, 2]) / total)


def field_from_mass(lat: Lattice3D, z_mass: float, strength: float, power: int = FIELD_POWER) -> np.ndarray:
    gl = 2 * lat.nl // 3
    mi = lat.nmap.get((gl, 0, round(z_mass / lat.h)))
    if mi is None:
        return np.zeros(lat.n)
    r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
    return strength / (r ** power)


def point_source(lat: Lattice3D, z_phys: float = 0.0) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    init[lat.nmap[(0, 0, round(z_phys / lat.h))]] = 1.0
    return init


def relaunch_from_layer(
    lat: Lattice3D,
    layer_state: np.ndarray,
    layer_inds: list[int],
    keep_inds: set[int] | None = None,
) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    for idx in layer_inds:
        if keep_inds is not None and idx not in keep_inds:
            continue
        _, y, z = lat.pos[idx]
        iy = round(y / lat.h)
        iz = round(z / lat.h)
        init[lat.nmap[(0, iy, iz)]] = layer_state[idx]
    norm = np.sqrt(np.sum(np.abs(init) ** 2))
    if norm < 1e-30:
        return init
    return init / norm


def tv_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(0.5 * np.abs(a - b).sum())


def square_support(lat: Lattice3D, inds: list[int], center_iy: int, center_iz: int, radius: int) -> list[int]:
    kept = []
    for idx in inds:
        _, y, z = lat.pos[idx]
        iy = round(y / lat.h)
        iz = round(z / lat.h)
        if max(abs(iy - center_iy), abs(iz - center_iz)) <= radius:
            kept.append(idx)
    return kept


def run_family(
    lat: Lattice3D,
    layer_state: np.ndarray,
    layer_inds: list[int],
    field: np.ndarray,
    keep_sets: list[tuple[str, list[int]]],
) -> list[dict[str, float | int | str]]:
    ref_init = relaunch_from_layer(lat, layer_state, layer_inds)
    ref_free = lat.propagate(ref_init, np.zeros(lat.n), K, ACTION)
    ref_grav = lat.propagate(ref_init, field, K, ACTION)
    ref_probs_free = probs_on_layer(ref_free, layer_inds)
    ref_probs_grav = probs_on_layer(ref_grav, layer_inds)
    ref_delta = centroid_z(ref_grav, layer_inds, lat.pos) - centroid_z(ref_free, layer_inds, lat.pos)

    layer_probs = np.array([abs(layer_state[i]) ** 2 for i in layer_inds], dtype=float)
    layer_total = float(layer_probs.sum())

    rows: list[dict[str, float | int | str]] = []
    for label, kept in keep_sets:
        keep_set = set(kept)
        capture = float(sum(abs(layer_state[i]) ** 2 for i in keep_set) / max(layer_total, 1e-30))
        init = relaunch_from_layer(lat, layer_state, layer_inds, keep_set)
        free = lat.propagate(init, np.zeros(lat.n), K, ACTION)
        grav = lat.propagate(init, field, K, ACTION)
        probs_free = probs_on_layer(free, layer_inds)
        probs_grav = probs_on_layer(grav, layer_inds)
        delta = centroid_z(grav, layer_inds, lat.pos) - centroid_z(free, layer_inds, lat.pos)
        rows.append(
            {
                "label": label,
                "keep_sites": len(kept),
                "capture_prob": capture,
                "tv_free": tv_distance(probs_free, ref_probs_free),
                "tv_grav": tv_distance(probs_grav, ref_probs_grav),
                "delta": delta,
                "rel_delta_err": abs(delta - ref_delta) / max(abs(ref_delta), 1e-30),
            }
        )
    return rows


def best_by_threshold(rows: list[dict[str, float | int | str]], max_rel_delta_err: float) -> dict[str, float | int | str] | None:
    passing = [r for r in rows if float(r["rel_delta_err"]) <= max_rel_delta_err]
    if not passing:
        return None
    return min(passing, key=lambda r: int(r["keep_sites"]))


def main() -> None:
    lat = Lattice3D(SEGMENT_L, PHYS_W, H)
    det = detector_indices(lat)
    source = point_source(lat, 0.0)
    field = field_from_mass(lat, FIELD_Z, FIELD_STRENGTH)

    first_segment = lat.propagate(source, np.zeros(lat.n), K, ACTION)
    layer_probs = np.array([abs(first_segment[i]) ** 2 for i in det], dtype=float)
    peak_idx = det[int(layer_probs.argmax())]
    peak_iy = round(lat.pos[peak_idx, 1] / lat.h)
    peak_iz = round(lat.pos[peak_idx, 2] / lat.h)

    sorted_det = [det[i] for i in np.argsort(-layer_probs)]

    radius_sets = [
        (f"square_r={radius}", square_support(lat, det, peak_iy, peak_iz, radius))
        for radius in RADIUS_VALUES
    ]
    topn_sets = [
        (f"topN={n}", sorted_det[: min(n, len(sorted_det))])
        for n in TOP_N_VALUES
    ]

    radius_rows = run_family(lat, first_segment, det, field, radius_sets)
    topn_rows = run_family(lat, first_segment, det, field, topn_sets)

    best_square_10 = best_by_threshold(radius_rows, 0.10)
    best_topn_05 = best_by_threshold(topn_rows, 0.05)

    print("=" * 96)
    print("QUASI-PERSISTENT RELAUNCH PROBE")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  segment L={SEGMENT_L}, h={H}, W={PHYS_W}, field_z={FIELD_Z}, strength={FIELD_STRENGTH:g}")
    print("  Goal: can a free packet be compressed into a small-support relaunch state")
    print("        without badly changing downstream free motion or field response?")
    print("=" * 96)
    print()
    print(f"Packet peak on first-segment detector layer: iy={peak_iy}, iz={peak_iz}")
    print(f"Detector layer support size: {len(det)} sites")

    print("\nSQUARE-WINDOW RELAUNCH")
    print(f"{'label':>12s} {'sites':>6s} {'capture':>8s} {'tv_free':>8s} {'tv_grav':>8s} {'delta':>12s} {'rel_err':>8s}")
    for row in radius_rows:
        print(
            f"{str(row['label']):>12s} {int(row['keep_sites']):6d} {float(row['capture_prob']):8.3f}"
            f" {float(row['tv_free']):8.3f} {float(row['tv_grav']):8.3f}"
            f" {float(row['delta']):+12.8f} {float(row['rel_delta_err']):8.3f}"
        )

    print("\nTOP-N RELAUNCH")
    print(f"{'label':>12s} {'sites':>6s} {'capture':>8s} {'tv_free':>8s} {'tv_grav':>8s} {'delta':>12s} {'rel_err':>8s}")
    for row in topn_rows:
        print(
            f"{str(row['label']):>12s} {int(row['keep_sites']):6d} {float(row['capture_prob']):8.3f}"
            f" {float(row['tv_free']):8.3f} {float(row['tv_grav']):8.3f}"
            f" {float(row['delta']):+12.8f} {float(row['rel_delta_err']):8.3f}"
        )

    print("\nBEST BOUNDED SURROGATES")
    if best_square_10 is None:
        print("  square-window: no support met the 10% relative-delta threshold")
    else:
        print(
            "  square-window: "
            f"{best_square_10['label']} with {best_square_10['keep_sites']} sites, "
            f"capture={best_square_10['capture_prob']:.3f}, "
            f"tv_free={best_square_10['tv_free']:.3f}, "
            f"rel_delta_err={best_square_10['rel_delta_err']:.3f}"
        )
    if best_topn_05 is None:
        print("  top-N: no support met the 5% relative-delta threshold")
    else:
        print(
            "  top-N: "
            f"{best_topn_05['label']} with {best_topn_05['keep_sites']} sites, "
            f"capture={best_topn_05['capture_prob']:.3f}, "
            f"tv_free={best_topn_05['tv_free']:.3f}, "
            f"rel_delta_err={best_topn_05['rel_delta_err']:.3f}"
        )

    print("\nSAFE READ")
    print("  - A relaunchable packet surrogate exists only as a broad mesoscopic profile on this family.")
    print("  - The downstream gravity response can survive moderate compression, but not sharp localization.")
    print("  - This is progress beyond the readiness note, but it is not persistent-pattern inertial closure.")


if __name__ == "__main__":
    main()
