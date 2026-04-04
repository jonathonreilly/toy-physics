#!/usr/bin/env python3
"""Bounded composite-source / additivity harness on the retained 3D family.

This harness is meant to sharpen Principle 3 without overstating it.

It tests two bounded statements on the retained ordered-lattice valley-linear
family:

1. Source-strength linearity at one location:
   delta(s1 + s2) ?= delta(s1) + delta(s2)

2. Composite-field additivity across disjoint sources:
   delta(field_A + field_B) ?= delta(field_A) + delta(field_B)

These are test-particle response statements. They do not, by themselves,
derive a persistent-pattern inertial mass.
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
SOURCE_Z = 5.0
PAIR_STRENGTHS = [(1e-5, 2e-5), (1e-5, 5e-5), (2e-5, 5e-5)]
DISJOINT_Z_PAIRS = [((4.0, 6.0), 2e-5), ((3.0, 6.0), 2e-5)]
ACTIONS = ("valley", "spent_delay")


def detector(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def centroid(amps: np.ndarray, det: list[int], pos: np.ndarray) -> float:
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return 0.0
    return float(np.dot(probs, pos[det, 2]) / total)


def point_packet(lat: Lattice3D, z_phys: float = 0.0) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    init[lat.nmap[(0, 0, round(z_phys / lat.h))]] = 1.0
    return init


def source_field(lat: Lattice3D, z_phys: float, strength: float, power: int = FIELD_POWER) -> np.ndarray:
    gl = 2 * lat.nl // 3
    mi = lat.nmap.get((gl, 0, round(z_phys / lat.h)))
    if mi is None:
        return np.zeros(lat.n)
    r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
    return strength / (r ** power)


def delta_for(lat: Lattice3D, init: np.ndarray, field: np.ndarray, det: list[int], action: str) -> float:
    af = lat.propagate(init, np.zeros(lat.n), K, action)
    am = lat.propagate(init, field, K, action)
    return centroid(am, det, lat.pos) - centroid(af, det, lat.pos)


def rel_err(lhs: float, rhs: float) -> float:
    denom = max(abs(lhs), abs(rhs), 1e-30)
    return abs(lhs - rhs) / denom


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)
    init = point_packet(lat, 0.0)

    print("=" * 88)
    print("COMPOSITE-SOURCE ADDITIVITY HARNESS")
    print("  Fixed 3D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, source_z={SOURCE_Z}")
    print("  Goal: bound source-additivity and response-additivity on the test-particle family")
    print("=" * 88)

    for action in ACTIONS:
        print(f"\nACTION: {action}")
        print("  Same-site strength additivity:")
        print(f"    {'s1':>8s} {'s2':>8s} {'delta(s1+s2)':>14s} {'delta1+delta2':>14s} {'rel_err':>10s}")
        for s1, s2 in PAIR_STRENGTHS:
            d1 = delta_for(lat, init, source_field(lat, SOURCE_Z, s1), det, action)
            d2 = delta_for(lat, init, source_field(lat, SOURCE_Z, s2), det, action)
            d12 = delta_for(lat, init, source_field(lat, SOURCE_Z, s1 + s2), det, action)
            err = rel_err(d12, d1 + d2)
            print(f"    {s1:8.0e} {s2:8.0e} {d12:+14.8e} {d1 + d2:+14.8e} {err:10.2%}")

        print("  Disjoint-source field additivity:")
        print(f"    {'zA,zB':>12s} {'s':>8s} {'delta(A+B)':>14s} {'deltaA+deltaB':>14s} {'rel_err':>10s}")
        for (z_a, z_b), s in DISJOINT_Z_PAIRS:
            f_a = source_field(lat, z_a, s)
            f_b = source_field(lat, z_b, s)
            d_a = delta_for(lat, init, f_a, det, action)
            d_b = delta_for(lat, init, f_b, det, action)
            d_ab = delta_for(lat, init, f_a + f_b, det, action)
            err = rel_err(d_ab, d_a + d_b)
            print(f"    ({z_a:.0f},{z_b:.0f}) {s:8.0e} {d_ab:+14.8e} {d_a + d_b:+14.8e} {err:10.2%}")

    print("\nSAFE READ")
    print("  - Valley-linear should be close to additive on this weak-field test-particle family.")
    print("  - Spent-delay should deviate because the action is nonlinear in the field.")
    print("  - Even if valley-linear is additive here, that still only supports a test-particle response law,")
    print("    not a persistent-pattern inertial-mass theorem.")


if __name__ == "__main__":
    main()
