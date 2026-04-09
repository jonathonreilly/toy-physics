#!/usr/bin/env python3
"""Basin-width probe for the parity-tapered elliptical-shell family v2."""

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

from CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP import (
    Family,
    _build_elliptical_shell_connectivity,
    _measure_family,
    _mean,
)
from gate_b_no_restore_farfield import grow


DRIFTS = [0.0, 0.02, 0.05, 0.10, 0.15, 0.20]
SEEDS = [0, 1, 2]


def main() -> None:
    print("=" * 96)
    print("CONNECTIVITY FAMILY V2 BASIN")
    print("  parity-tapered elliptical-shell family on the no-restore grown slice")
    print("=" * 96)
    print(f"drifts={DRIFTS}, seeds={SEEDS}")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}")
    print("-" * 96)

    rows = []
    for drift in DRIFTS:
        for seed in SEEDS:
            pos, adj, layers, _nmap = grow(drift, seed)
            fam = Family(pos, layers, adj)
            elliptical = _build_elliptical_shell_connectivity(fam)
            out = _measure_family(elliptical.positions, elliptical.adj, elliptical.layers)
            rows.append((drift, seed, out.zero, out.plus, out.minus, out.neutral, out.double, out.exponent, out.ok))
            print(
                f"{drift:5.2f} {seed:4d} "
                f"{out.zero:+12.3e} {out.plus:+12.3e} {out.minus:+12.3e} "
                f"{out.neutral:+12.3e} {out.double:+12.3e} {out.exponent:7.3f} "
                f"{'YES' if out.ok else 'no':>4s}"
            )

    passed = [r for r in rows if r[-1]]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        drift_vals = sorted({r[0] for r in passed})
        print(f"  drift coverage: {drift_vals}")
        print(f"  mean exponent among passes: {_mean([r[7] for r in passed]):.6f}")
        print("  this elliptical-shell slice sits inside the portable sign-law invariant")
        print("  it is not counted as a new retained family")
    else:
        print("  no row survived the exact zero/neutral gate")
        print("  this elliptical-shell family is a diagnosed failure on this slice")


if __name__ == "__main__":
    main()
