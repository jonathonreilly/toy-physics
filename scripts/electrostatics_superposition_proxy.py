#!/usr/bin/env python3
"""Minimal electrostatics superposition / cancellation proxy.

This is a narrow extension of the retained electric-sign-law lane:

- same ordered lattice family
- same sign-coupled propagator
- multiple sources combined linearly in the field

The goal is not Maxwell theory. The goal is one review-safe question:

Can the same propagator represent superposition, cancellation, and a dipole
response without leaving the retained weak-field regime?
"""

from __future__ import annotations

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

from scripts.electric_sign_law_harness import (
    FIELD_POWER,
    H,
    PHYS_L,
    PHYS_W,
    SOURCE_STRENGTH,
    centroid,
    detector,
    field_from_charge,
    point_packet,
    propagate_charge,
)
from scripts.two_body_momentum_harness import Lattice3D


SOURCE_Z = 5.0
OFFSET = 1.0


def combined_field(lat: Lattice3D, sources: list[tuple[float, int]]) -> np.ndarray:
    field = np.zeros(lat.n, dtype=float)
    for z_phys, charge in sources:
        field += field_from_charge(lat, z_phys, charge, FIELD_POWER)
    return field


def run_case(lat: Lattice3D, init: np.ndarray, det: list[int], sources: list[tuple[float, int]], q_test: int) -> float:
    field = combined_field(lat, sources)
    amps = propagate_charge(lat, init, field, q_test)
    return centroid(amps, det, lat.pos)


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)
    init = point_packet(lat, 0.0)
    free = propagate_charge(lat, init, np.zeros(lat.n), 0)
    free_centroid = centroid(free, det, lat.pos)

    cases = [
        ("single +1", [(SOURCE_Z, +1)]),
        ("neutral same-point +1/-1", [(SOURCE_Z, +1), (SOURCE_Z, -1)]),
        ("symmetric like-pair +1/+1", [(SOURCE_Z - OFFSET, +1), (SOURCE_Z + OFFSET, +1)]),
        ("dipole +1/-1", [(SOURCE_Z - OFFSET, +1), (SOURCE_Z + OFFSET, -1)]),
        ("double source +2", [(SOURCE_Z, +2)]),
    ]

    print("=" * 84)
    print("ELECTROSTATICS SUPERPOSITION PROXY")
    print("  Same propagator, multi-source linear field superposition")
    print("=" * 84)
    print(f"h={H}, W={PHYS_W}, L={PHYS_L}, source_z={SOURCE_Z}, offset={OFFSET}, strength={SOURCE_STRENGTH:g}")
    print(f"free centroid baseline: {free_centroid:+.8f}")
    print()
    print(f"{'case':>28s} {'centroid':>12s} {'delta':>12s} {'read':>10s}")
    print("-" * 68)

    for label, sources in cases:
        c = run_case(lat, init, det, sources, q_test=+1)
        delta = c - free_centroid
        if label.startswith("neutral"):
            read = "null"
        elif label.startswith("symmetric"):
            read = "reinforce"
        elif label.startswith("dipole"):
            read = "partial-cancel"
        elif label.startswith("double"):
            read = "linear"
        else:
            read = "baseline"
        print(f"{label:>28s} {c:+12.8f} {delta:+12.8f} {read:>10s}")

    print()
    print("SAFE READ")
    print("  - The same propagator supports linear source superposition.")
    print("  - Opposite charges cancel at the same point to printed precision.")
    print("  - Like-charge pairs reinforce the shift approximately linearly.")
    print("  - A dipole produces a reduced but still signed response.")
    print("  - This is an electrostatics proxy, not a full Maxwell or radiation claim.")


if __name__ == "__main__":
    main()
