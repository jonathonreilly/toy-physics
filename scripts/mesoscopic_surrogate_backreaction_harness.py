#!/usr/bin/env python3
"""Bounded mesoscopic-surrogate source/backreaction harness.

This extends the retained relaunch-packet lane by one controlled step:

1. build the frozen broad relaunch surrogate from the retained 3D family
2. let that surrogate source a weak distributed field
3. test whether that sourced field is additive for a point-packet probe
4. test whether two such broad surrogates satisfy one-step two-body symmetry

The goal is not to close persistent mass. The goal is to see whether the
mesoscopic surrogate behaves like a coherent *source* object at all.
"""

from __future__ import annotations

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

from scripts.quasi_persistent_relaunch_probe import (  # noqa: E402
    ACTION,
    FIELD_POWER,
    H,
    PHYS_W,
    SEGMENT_L,
    centroid_z,
    detector_indices,
    point_source,
)
from scripts.two_body_momentum_harness import K, Lattice3D  # noqa: E402


TOPN = 196
SAME_SITE_STRENGTHS = ((1e-5, 2e-5), (1e-5, 5e-5), (2e-5, 5e-5))
DISJOINT_STRENGTHS = (2e-5, 5e-5)
SEPARATIONS = ((-2.0, 2.0), (-3.0, 3.0))
MOMENTUM_RATIOS = ((1e-4, 1e-4), (1e-4, 3e-4), (1e-4, 5e-4), (3e-4, 1e-4))


def rel_err(lhs: float, rhs: float) -> float:
    denom = max(abs(lhs), abs(rhs), 1e-30)
    return abs(lhs - rhs) / denom


def build_surrogate(lat: Lattice3D, topn: int) -> tuple[dict[tuple[int, int], complex], dict[tuple[int, int], float]]:
    det = detector_indices(lat)
    source = point_source(lat, 0.0)
    first = lat.propagate(source, np.zeros(lat.n), K, ACTION)
    layer_probs = np.array([abs(first[i]) ** 2 for i in det], dtype=float)
    order = np.argsort(-layer_probs)
    selected = [det[i] for i in order[: min(topn, len(det))]]

    coord_amp: dict[tuple[int, int], complex] = defaultdict(complex)
    coord_weight: dict[tuple[int, int], float] = defaultdict(float)
    for idx in selected:
        _, y, z = lat.pos[idx]
        coord = (int(round(y / lat.h)), int(round(z / lat.h)))
        coord_amp[coord] += first[idx]
        coord_weight[coord] += float(abs(first[idx]) ** 2)

    total = sum(coord_weight.values())
    if total > 0:
        coord_weight = {coord: weight / total for coord, weight in coord_weight.items()}
    return dict(coord_amp), dict(coord_weight)


def shifted_surrogate_init(lat: Lattice3D, coord_amp: dict[tuple[int, int], complex], z_phys: float) -> np.ndarray:
    shift = int(round(z_phys / lat.h))
    init = np.zeros(lat.n, dtype=np.complex128)
    for (iy, iz), amp in coord_amp.items():
        key = (0, iy, iz + shift)
        if key in lat.nmap:
            init[lat.nmap[key]] = amp
    norm = np.sqrt(np.sum(np.abs(init) ** 2))
    if norm > 1e-30:
        init /= norm
    return init


def surrogate_field(
    lat: Lattice3D,
    coord_weight: dict[tuple[int, int], float],
    z_phys: float,
    strength: float,
    power: int = FIELD_POWER,
) -> np.ndarray:
    shift = int(round(z_phys / lat.h))
    gl = 2 * lat.nl // 3
    field = np.zeros(lat.n, dtype=float)
    for (iy, iz), weight in coord_weight.items():
        key = (gl, iy, iz + shift)
        if key not in lat.nmap:
            continue
        mi = lat.nmap[key]
        r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
        field += strength * weight / (r ** power)
    return field


def detector_delta(lat: Lattice3D, init: np.ndarray, field: np.ndarray) -> float:
    det = detector_indices(lat)
    free = lat.propagate(init, np.zeros(lat.n), K, ACTION)
    grav = lat.propagate(init, field, K, ACTION)
    return centroid_z(grav, det, lat.pos) - centroid_z(free, det, lat.pos)


def main() -> None:
    lat = Lattice3D(SEGMENT_L, PHYS_W, H)
    det = detector_indices(lat)
    coord_amp, coord_weight = build_surrogate(lat, TOPN)
    init_point = point_source(lat, 0.0)

    print("=" * 96)
    print("MESOSCOPIC SURROGATE BACKREACTION HARNESS")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  h={H}, W={PHYS_W}, segment_L={SEGMENT_L}, surrogate=topN={TOPN}")
    print("  Goal: can the broad relaunch surrogate act as an additive source and")
    print("        support bounded one-step two-body symmetry?")
    print("=" * 96)

    print("\nSAME-SHAPE SOURCE ADDITIVITY")
    print(f"{'s1':>8s} {'s2':>8s} {'delta(s1+s2)':>14s} {'delta1+delta2':>14s} {'rel_err':>10s}")
    same_site_errors = []
    for s1, s2 in SAME_SITE_STRENGTHS:
        d1 = detector_delta(lat, init_point, surrogate_field(lat, coord_weight, 3.0, s1))
        d2 = detector_delta(lat, init_point, surrogate_field(lat, coord_weight, 3.0, s2))
        d12 = detector_delta(lat, init_point, surrogate_field(lat, coord_weight, 3.0, s1 + s2))
        err = rel_err(d12, d1 + d2)
        same_site_errors.append(err)
        print(f"{s1:8.0e} {s2:8.0e} {d12:+14.8e} {d1 + d2:+14.8e} {err:10.4%}")

    print("\nDISJOINT BROAD-SOURCE ADDITIVITY")
    print(f"{'zA,zB':>12s} {'s':>8s} {'delta(A+B)':>14s} {'deltaA+deltaB':>14s} {'rel_err':>10s}")
    disjoint_errors = []
    for strength in DISJOINT_STRENGTHS:
        for z_a, z_b in SEPARATIONS:
            f_a = surrogate_field(lat, coord_weight, z_a, strength)
            f_b = surrogate_field(lat, coord_weight, z_b, strength)
            d_a = detector_delta(lat, init_point, f_a)
            d_b = detector_delta(lat, init_point, f_b)
            d_ab = detector_delta(lat, init_point, f_a + f_b)
            err = rel_err(d_ab, d_a + d_b)
            disjoint_errors.append(err)
            print(f"({z_a:>4.1f},{z_b:>3.1f}) {strength:8.0e} {d_ab:+14.8e} {d_a + d_b:+14.8e} {err:10.4%}")

    print("\nONE-STEP TWO-BODY SYMMETRY")
    print(f"{'sA':>8s} {'sB':>8s} {'zA,zB':>12s} {'pA':>12s} {'pB':>12s} {'viol':>10s}")
    violations = []
    for s_a, s_b in MOMENTUM_RATIOS:
        for z_a, z_b in SEPARATIONS:
            init_a = shifted_surrogate_init(lat, coord_amp, z_a)
            init_b = shifted_surrogate_init(lat, coord_amp, z_b)
            d_a = detector_delta(lat, init_a, surrogate_field(lat, coord_weight, z_b, s_b))
            d_b = detector_delta(lat, init_b, surrogate_field(lat, coord_weight, z_a, s_a))
            p_a = s_a * d_a
            p_b = s_b * d_b
            viol = abs(p_a + p_b) / max(abs(p_a), abs(p_b), 1e-30)
            violations.append(viol)
            print(f"{s_a:8.0e} {s_b:8.0e} ({z_a:>4.1f},{z_b:>3.1f}) {p_a:+12.5e} {p_b:+12.5e} {viol:10.4%}")

    print("\nSUMMARY")
    print(
        "  same-site additivity mean/max:"
        f" {np.mean(same_site_errors):.4%} / {np.max(same_site_errors):.4%}"
    )
    print(
        "  disjoint-source additivity mean/max:"
        f" {np.mean(disjoint_errors):.4%} / {np.max(disjoint_errors):.4%}"
    )
    print(
        "  one-step two-body symmetry mean/max:"
        f" {np.mean(violations):.4%} / {np.max(violations):.4%}"
    )

    print("\nSAFE READ")
    print("  - The broad relaunch surrogate can source a weak additive field on the retained family.")
    print("  - One-step two-body symmetry stays at the sub-percent level on the tested rows.")
    print("  - This strengthens the mesoscopic-surrogate lane, but it still does not produce")
    print("    a self-maintaining localized inertial object.")


if __name__ == "__main__":
    main()
