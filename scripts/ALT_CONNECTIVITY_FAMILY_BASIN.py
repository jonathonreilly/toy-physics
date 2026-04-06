#!/usr/bin/env python3
"""Basin-width probe for the alternative structured connectivity family.

This asks whether the parity-rotated sector-transition rule is a tiny basin or
just a sparse collection of retained rows.
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
    DRIFTS as BASE_DRIFTS,
    SEEDS as BASE_SEEDS,
    Family,
    _build_alt_connectivity,
    _field_from_sources,
    _mean,
    _propagate,
    _centroid_z,
    H,
    NL,
    SOURCE_Z,
)
from gate_b_no_restore_farfield import grow


DRIFTS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
SEEDS = [0, 1, 2, 3, 4]
SOURCE_STRENGTHS = [5e-5, 1e-4]


def _measure(drift: float, seed: int) -> tuple[float, float, float, float, float, float, bool]:
    pos, adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, adj)
    alt = _build_alt_connectivity(fam)
    det = alt.layers[-1]
    free = _propagate(alt.positions, alt.adj, [0.0] * len(alt.positions))
    z_free = _centroid_z(free, alt.positions, det)

    def run(charge: int) -> float:
        field = _field_from_sources(alt.positions, alt.layers, [(SOURCE_Z, charge)])
        amps = _propagate(alt.positions, alt.adj, field)
        return _centroid_z(amps, alt.positions, det) - z_free

    zero = run(0)
    plus = run(+1)
    minus = run(-1)
    neutral = _centroid_z(
        _propagate(
            alt.positions,
            alt.adj,
            _field_from_sources(alt.positions, alt.layers, [(SOURCE_Z, +1), (SOURCE_Z, -1)]),
        ),
        alt.positions,
        det,
    ) - z_free
    double = run(+2)
    exponent = math.log(abs(double / plus)) / math.log(2.0) if abs(plus) > 1e-30 and abs(double) > 1e-30 else math.nan
    ok = (
        abs(zero) < 1e-12
        and abs(neutral) < 1e-12
        and plus > 0.0
        and minus < 0.0
        and abs(exponent - 1.0) < 0.05
    )
    return zero, plus, minus, neutral, double, exponent, ok


def main() -> None:
    print("=" * 94)
    print("ALT CONNECTIVITY FAMILY BASIN")
    print("  parity-rotated sector-transition rule on the no-restore grown slice")
    print("=" * 94)
    print(f"drifts={DRIFTS}, seeds={SEEDS}")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}")
    print("-" * 94)

    rows = []
    for drift in DRIFTS:
        for seed in SEEDS:
            row = _measure(drift, seed)
            rows.append((drift, seed, *row))
            zero, plus, minus, neutral, double, exponent, ok = row
            print(
                f"{drift:5.2f} {seed:4d} "
                f"{zero:+12.3e} {plus:+12.3e} {minus:+12.3e} "
                f"{neutral:+12.3e} {double:+12.3e} {exponent:7.3f} "
                f"{'YES' if ok else 'no':>4s}"
            )

    passed = [r for r in rows if r[-1]]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        drift_vals = sorted({r[0] for r in passed})
        print(f"  drift coverage: {drift_vals}")
        print(f"  mean exponent among passes: {_mean([r[5] for r in passed]):.6f}")
        print("  this family has a real bounded basin")
    else:
        print("  no row survived the exact zero/neutral gate")
        print("  this alternative family is only a sparse row-level positive")


if __name__ == "__main__":
    main()
