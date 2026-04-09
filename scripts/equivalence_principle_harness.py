#!/usr/bin/env python3
"""Bounded equivalence-principle probe on the retained 3D ordered family.

This harness separates two different claims that are easy to conflate:

1. Amplitude-scaling invariance:
   If the whole initial state is multiplied by a scalar c, does the centroid
   shift stay unchanged? In a linear propagator it should.

2. Internal-composition invariance:
   If two localized packets have the same center but different internal shape,
   do they deflect the same amount? This is not guaranteed and is the more
   interesting proxy for an effective inertial response.

The goal is to keep the derivation chain honest:
  - exact amplitude invariance is structural and action-independent
  - composition dependence, if present, is a finite-size / extended-body effect
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
PHYS_L = 12
PHYS_W = 8
Z_MASS = 5.0
STRENGTH = 5e-5
FIELD_POWER = 1
ACTIONS = ("valley", "spent_delay")
AMPLITUDES = (0.5, 1.0, 2.0, 5.0)


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


def field_from_mass(lat: Lattice3D, z_mass: float, strength: float, power: int) -> np.ndarray:
    gl = 2 * lat.nl // 3
    mi = lat.nmap.get((gl, 0, round(z_mass / lat.h)))
    if mi is None:
        return np.zeros(lat.n)
    r = np.sqrt(np.sum((lat.pos - lat.pos[mi]) ** 2, axis=1)) + 0.1
    return strength / (r ** power)


def normalized_packet(lat: Lattice3D, weights: dict[int, float]) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    norm = math.sqrt(sum(w * w for w in weights.values()))
    for z_lattice, w in weights.items():
        idx = lat.nmap[(0, 0, z_lattice)]
        init[idx] = w / norm
    return init


def point_packet(lat: Lattice3D, z_phys: float = 0.0) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    init[lat.nmap[(0, 0, round(z_phys / lat.h))]] = 1.0
    return init


def delta_for(lat: Lattice3D, init: np.ndarray, field: np.ndarray, det: list[int], action: str) -> float:
    af = lat.propagate(init, np.zeros(lat.n), K, action)
    am = lat.propagate(init, field, K, action)
    return centroid(am, det, lat.pos) - centroid(af, det, lat.pos)


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)
    field = field_from_mass(lat, Z_MASS, STRENGTH, FIELD_POWER)

    center = round(0.0 / H)
    packets = {
        "point": point_packet(lat, 0.0),
        "gauss3": normalized_packet(lat, {center - 1: 0.25, center: 1.0, center + 1: 0.25}),
        "flat3": normalized_packet(lat, {center - 1: 1.0, center: 1.0, center + 1: 1.0}),
        "gauss5": normalized_packet(
            lat,
            {center - 2: 0.10, center - 1: 0.40, center: 1.0, center + 1: 0.40, center + 2: 0.10},
        ),
        "flat5": normalized_packet(
            lat,
            {center - 2: 1.0, center - 1: 1.0, center: 1.0, center + 1: 1.0, center + 2: 1.0},
        ),
    }

    print("=" * 88)
    print("EQUIVALENCE-PRINCIPLE HARNESS")
    print("  Fixed 3D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, z_mass={Z_MASS}, strength={STRENGTH:g}")
    print("  Goal: separate amplitude invariance from packet-shape dependence")
    print("=" * 88)

    for action in ACTIONS:
        print(f"\nACTION: {action}")
        print("  Amplitude scaling (same point packet, different global amplitude):")
        point = packets["point"]
        ref = None
        for amp in AMPLITUDES:
            delta = delta_for(lat, amp * point, field, det, action)
            if ref is None:
                ref = delta
            drift = delta - ref
            print(f"    amp={amp:>4.1f}  delta={delta:+.8f}  delta-ref={drift:+.2e}")

        print("  Packet-shape dependence (normalized packets, same center):")
        deltas = {}
        for name, init in packets.items():
            delta = delta_for(lat, init, field, det, action)
            deltas[name] = delta
            print(f"    {name:<7s} delta={delta:+.8f}")

        vals = np.array(list(deltas.values()), dtype=float)
        mean = float(vals.mean())
        spread = float(vals.max() - vals.min())
        rel = spread / max(abs(mean), 1e-30)
        print(f"    spread={spread:.3e}, relative_spread={rel:.2%}")

    print("\nSAFE READ")
    print("  - Global amplitude scaling cancels exactly in the centroid ratio on this linear family.")
    print("  - Packet shape can still matter because extended packets sample different field regions.")
    print("  - So linearity gives an amplitude-level equivalence statement, not a full persistent-pattern mass law.")


if __name__ == "__main__":
    main()
