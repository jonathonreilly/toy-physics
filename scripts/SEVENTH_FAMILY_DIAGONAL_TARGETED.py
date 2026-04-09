#!/usr/bin/env python3
"""Targeted scout for the seventh-family diagonal-stripe construction.

This reuses the diagonal-stripe family but only checks a few anchor rows so the
result comes back quickly enough to be useful for the next cycle.
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

from SEVENTH_FAMILY_DIAGONAL_SWEEP import (
    Family,
    _build_diagonal_stripe_connectivity,
    _measure_family,
    _mean,
)
from gate_b_no_restore_farfield import grow


TARGETS = [
    (0.05, 0),
    (0.05, 1),
    (0.20, 0),
    (0.20, 1),
    (0.30, 0),
    (0.30, 1),
]


def main() -> None:
    print("=" * 96)
    print("SEVENTH FAMILY DIAGONAL TARGETED SCOUT")
    print("  question: can a non-shell diagonal-stripe family carry the signed-source")
    print("  package on a small anchor set of no-restore rows?")
    print("=" * 96)
    print(f"targets={TARGETS}")
    print("guards: exact zero-source baseline, exact neutral cancellation, sign orientation, weak-field F~M")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}")
    print("-" * 96)

    rows = []
    for drift, seed in TARGETS:
        pos, adj, layers, _nmap = grow(drift, seed)
        fam = Family(pos, layers, adj)
        diag = _build_diagonal_stripe_connectivity(fam)
        out = _measure_family(diag.positions, diag.adj, diag.layers)
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
        seed_vals = sorted({r[1] for r in passed})
        print(f"  drift coverage: {drift_vals}")
        print(f"  seed coverage: {seed_vals}")
        print(f"  mean charge exponent among passes: {_mean([r[7] for r in passed]):.6f}")
        print("  boundary read: a tiny seed-selective pocket, not a family-wide basin")
    else:
        print("  no row survived the exact zero/neutral gate")
        print("  the diagonal-stripe rule is a diagnosed failure on this slice")


if __name__ == "__main__":
    main()
