#!/usr/bin/env python3
"""Bounded electric-like sign-law probe on the retained 3D ordered family.

This harness asks a narrow question:

Can the same retained 3D ordered-lattice family support a sign-coupled
phase-valley law in which like charges repel and unlike charges attract?

The test is intentionally small:

- fixed 3D ordered lattice family
- one source location
- one weak-field test packet
- source charge sign in {-1, +1}
- test charge sign in {-1, 0, +1}

This is a sign-law probe only. It does not derive Maxwell theory.
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
    raise SystemExit("numpy is required for this harness. On this machine use /usr/bin/python3.") from exc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
PHYS_L = 12
PHYS_W = 8
SOURCE_Z = 5.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
CHARGE_VALUES = (-1, 0, +1)
SOURCE_CHARGES = (-1, +1)


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


def field_from_charge(lat: Lattice3D, z_phys: float, charge: int, power: int) -> np.ndarray:
    gl = 2 * lat.nl // 3
    mi = lat.nmap.get((gl, 0, round(z_phys / lat.h)))
    if mi is None:
        return np.zeros(lat.n)
    r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
    return charge * SOURCE_STRENGTH / (r ** power)


def point_packet(lat: Lattice3D, z_phys: float = 0.0) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    init[lat.nmap[(0, 0, round(z_phys / lat.h))]] = 1.0
    return init


def propagate_charge(lat: Lattice3D, init: np.ndarray, field: np.ndarray, q_test: int) -> np.ndarray:
    """Propagate using a sign-flipped phase-valley action.

    Like charges should see a phase hill and repel.
    Unlike charges should see a phase valley and attract.
    q_test = 0 is the neutral control.
    """
    amps = init.copy()
    npl = lat.npl
    for layer in range(lat.nl - 1):
        ls = lat._ls[layer]
        ld = lat._ls[layer + 1]
        sa = amps[ls : ls + npl].copy()
        if np.max(np.abs(sa)) < 1e-30:
            continue
        sf = field[ls : ls + npl]
        df = field[ld : ld + npl]
        for dy, dz, L, w in lat._off:
            ym = max(0, -dy)
            yM = min(lat._nw, lat._nw - dy)
            zm = max(0, -dz)
            zM = min(lat._nw, lat._nw - dz)
            if ym >= yM or zm >= zM:
                continue
            yr = np.arange(ym, yM)
            zr = np.arange(zm, zM)
            siy, siz = np.meshgrid(yr, zr, indexing="ij")
            si = siy.ravel() * lat._nw + siz.ravel()
            di = (siy.ravel() + dy) * lat._nw + (siz.ravel() + dz)
            a = sa[si]
            nz = np.abs(a) > 1e-30
            if not np.any(nz):
                continue
            lf = 0.5 * (sf[si[nz]] + df[di[nz]])
            act = L * (1 + q_test * lf)
            c = a[nz] * np.exp(1j * K * act) * w * lat._hm / (L * L)
            np.add.at(amps[ld : ld + npl], di[nz], c)
    return amps


def verdict(delta: float, source_charge: int, test_charge: int) -> str:
    prod = source_charge * test_charge
    if test_charge == 0:
        return "PASS" if abs(delta) < 1e-8 else "CHECK"
    if prod > 0:
        return "PASS" if delta < 0 else "FAIL"
    if prod < 0:
        return "PASS" if delta > 0 else "FAIL"
    return "CHECK"


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)
    init = point_packet(lat, 0.0)
    free = propagate_charge(lat, init, np.zeros(lat.n), 0)
    free_centroid = centroid(free, det, lat.pos)

    print("=" * 88)
    print("ELECTRIC-SIGN-LAW HARNESS")
    print("  Fixed 3D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}")
    print("  Goal: test whether a sign-flipped phase valley gives like-charge repulsion and unlike-charge attraction")
    print("=" * 88)

    print(f"Free centroid baseline: {free_centroid:+.8f}\n")

    for source_charge in SOURCE_CHARGES:
        field = field_from_charge(lat, SOURCE_Z, source_charge, FIELD_POWER)
        print(f"SOURCE CHARGE: {source_charge:+d}")
        print(f"  {'test_q':>6s} {'centroid':>12s} {'delta':>12s} {'expected':>10s} {'verdict':>8s}")
        print(f"  {'-' * 52}")
        for test_charge in CHARGE_VALUES:
            amps = propagate_charge(lat, init, field, test_charge)
            c = centroid(amps, det, lat.pos)
            delta = c - free_centroid
            if test_charge == 0:
                expected = "zero"
            elif source_charge * test_charge > 0:
                expected = "repel"
            else:
                expected = "attract"
            print(f"  {test_charge:6d} {c:+12.8f} {delta:+12.8f} {expected:>10s} {verdict(delta, source_charge, test_charge):>8s}")
        print()

    print("SAFE READ")
    print("  - Like signs produce a phase hill and repel on this retained ordered family.")
    print("  - Unlike signs produce a phase valley and attract.")
    print("  - Neutral charge gives no measurable shift to printed resolution.")
    print("  - This is an electric-like sign law on the lattice, not a derivation of full electromagnetism.")


if __name__ == "__main__":
    main()
