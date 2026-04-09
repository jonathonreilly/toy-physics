#!/usr/bin/env python3
"""F~M transfer on the alternative connectivity family.

This checks whether the parity-rotated sector-transition family preserves the
weak-field mass-scaling law on the no-restore grown slice.
"""

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

from ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP import (
    Family,
    _build_alt_connectivity,
    _field_from_sources,
    _mean,
    _propagate,
    _centroid_z,
    H,
    SOURCE_Z,
)
from gate_b_no_restore_farfield import grow


DRIFTS = [0.0, 0.1, 0.2, 0.3, 0.5]
SEEDS = [0, 1, 2]
SOURCE_STRENGTHS = [5e-5, 1e-4]
BASE_STRENGTH = SOURCE_STRENGTHS[0]


def _measure(drift: float, seed: int) -> float:
    pos, adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, adj)
    alt = _build_alt_connectivity(fam)
    det = alt.layers[-1]
    free = _propagate(alt.positions, alt.adj, [0.0] * len(alt.positions))
    z_free = _centroid_z(free, alt.positions, det)

    deltas = []
    for s in SOURCE_STRENGTHS:
        field = _field_from_sources(alt.positions, alt.layers, [(SOURCE_Z, +1)])
        field = [v * (s / BASE_STRENGTH) for v in field]
        amps = _propagate(alt.positions, alt.adj, field)
        deltas.append(abs(_centroid_z(amps, alt.positions, det) - z_free))

    d1, d2 = deltas
    return math.log(d2 / d1) / math.log(2.0) if d1 > 1e-15 and d2 > 1e-15 else math.nan


def main() -> None:
    print("=" * 94)
    print("ALT CONNECTIVITY FAMILY F~M TRANSFER")
    print("  weak-field mass-scaling on the no-restore grown slice")
    print("=" * 94)
    print(f"drifts={DRIFTS}, seeds={SEEDS}")
    print(f"source strengths={SOURCE_STRENGTHS}")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'F~M':>8s} {'ok':>4s}")
    print("-" * 24)

    rows = []
    for drift in DRIFTS:
        for seed in SEEDS:
            fm = _measure(drift, seed)
            ok = not math.isnan(fm) and abs(fm - 1.0) < 0.05
            rows.append((drift, seed, fm, ok))
            print(f"{drift:5.2f} {seed:4d} {fm:8.3f} {'YES' if ok else 'no':>4s}")

    passed = [r for r in rows if r[-1]]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        print(f"  mean F~M among passes: {_mean([r[2] for r in passed]):.6f}")
        print("  the alternative family preserves weak-field linearity on this slice")
    else:
        print("  no row retained weak-field linearity on this slice")


if __name__ == "__main__":
    main()
