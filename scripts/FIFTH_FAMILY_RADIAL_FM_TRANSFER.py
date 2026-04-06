#!/usr/bin/env python3
"""Weak-field F~M transfer for the fifth-family radial-shell slice."""

from __future__ import annotations

import math
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from CONNECTIVITY_FAMILY_V2_QUADRANT_SWEEP import (
    Family,
    _build_radial_shell_connectivity,
    _field_from_sources,
    _centroid_z,
    _propagate,
    _mean,
    SOURCE_Z,
    SOURCE_STRENGTH,
)
from gate_b_no_restore_farfield import grow


TARGETS = [(0.05, 0), (0.30, 1)]


def _fm(drift: float, seed: int) -> float:
    pos, adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, adj)
    radial = _build_radial_shell_connectivity(fam)
    det = radial.layers[-1]
    free = _propagate(radial.positions, radial.adj, [0.0] * len(radial.positions))
    z_free = _centroid_z(free, radial.positions, det)
    values = []
    for strength in (5e-5, 1e-4):
        field = _field_from_sources(radial.positions, radial.layers, [(SOURCE_Z, +1)])
        field = [v * (strength / SOURCE_STRENGTH) for v in field]
        amps = _propagate(radial.positions, radial.adj, field)
        values.append(abs(_centroid_z(amps, radial.positions, det) - z_free))
    d1, d2 = values
    return math.log(d2 / d1) / math.log(2.0) if d1 > 1e-15 and d2 > 1e-15 else math.nan


def main() -> None:
    print("=" * 96)
    print("FIFTH FAMILY RADIAL F~M TRANSFER")
    print("  weak-field mass scaling on the no-restore grown slice")
    print("=" * 96)
    print(f"targets={TARGETS}")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'F~M':>8s} {'ok':>4s}")
    print("-" * 24)

    rows = []
    for drift, seed in TARGETS:
        fm = _fm(drift, seed)
        ok = not math.isnan(fm) and abs(fm - 1.0) < 0.05
        rows.append((drift, seed, fm, ok))
        print(f"{drift:5.2f} {seed:4d} {fm:8.3f} {'YES' if ok else 'no':>4s}")

    passed = [r for r in rows if r[-1]]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        print(f"  mean F~M among passes: {_mean([r[2] for r in passed]):.6f}")
        print("  the fifth-family radial-shell slice preserves weak-field linearity on the sampled rows")
    else:
        print("  no row retained weak-field linearity on this slice")


if __name__ == "__main__":
    main()
