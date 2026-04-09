#!/usr/bin/env python3
"""Targeted fifth-family sweep for the radial-shell connectivity slice.

This is the fifth independent structured family candidate:
- no-restore grown slice
- radial-shell connectivity instead of the earlier sector/quadrant rules

The first gate is exact zero/neutral control.  The targeted rows below are the
same ones used to establish the narrow retained basin and its interior
orientation miss.
"""

from __future__ import annotations

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
    _measure_family,
    _mean,
)
from gate_b_no_restore_farfield import grow


TARGETS = [(0.05, 0), (0.20, 0), (0.30, 1)]


def main() -> None:
    print("=" * 96)
    print("FIFTH FAMILY RADIAL SWEEP")
    print("  radial-shell connectivity on the no-restore grown slice")
    print("=" * 96)
    print(f"targets={TARGETS}")
    print("guards: exact zero-source baseline, exact neutral cancellation, sign orientation")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}")
    print("-" * 96)

    rows = []
    for drift, seed in TARGETS:
        pos, adj, layers, _nmap = grow(drift, seed)
        fam = Family(pos, layers, adj)
        radial = _build_radial_shell_connectivity(fam)
        out = _measure_family(radial.positions, radial.adj, radial.layers)
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
        print(f"  mean exponent among passes: {_mean([r[6] for r in passed]):.6f}")
        print("  this radial-shell family is a real fifth-family basin on the sampled rows")
    else:
        print("  no row survived the exact zero/neutral gate")
        print("  the radial-shell rule is a diagnosed failure on this slice")


if __name__ == "__main__":
    main()
