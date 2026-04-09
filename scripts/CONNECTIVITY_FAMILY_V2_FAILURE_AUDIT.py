#!/usr/bin/env python3
"""Boundary audit for the parity-tapered elliptical-shell family v2."""

from __future__ import annotations

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
)
from gate_b_no_restore_farfield import grow


DRIFTS = [0.10, 0.15, 0.20]
SEEDS = [0, 1, 2]


def main() -> None:
    print("=" * 96)
    print("CONNECTIVITY FAMILY V2 FAILURE AUDIT")
    print("  parity-tapered elliptical-shell boundary on the no-restore grown slice")
    print("=" * 96)
    print(f"drifts={DRIFTS}, seeds={SEEDS}")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}")
    print("-" * 96)

    failing_rows = []
    for drift in DRIFTS:
        for seed in SEEDS:
            pos, adj, layers, _nmap = grow(drift, seed)
            fam = Family(pos, layers, adj)
            elliptical = _build_elliptical_shell_connectivity(fam)
            out = _measure_family(elliptical.positions, elliptical.adj, elliptical.layers)
            print(
                f"{drift:5.2f} {seed:4d} "
                f"{out.zero:+12.3e} {out.plus:+12.3e} {out.minus:+12.3e} "
                f"{out.neutral:+12.3e} {out.double:+12.3e} {out.exponent:7.3f} "
                f"{'YES' if out.ok else 'no':>4s}"
            )
            if not out.ok:
                failing_rows.append((drift, seed, out.plus, out.minus, out.exponent))

    print()
    print("SAFE READ")
    print(f"  failing rows: {len(failing_rows)}")
    if failing_rows:
        print("  representative boundary pattern:")
        for drift, seed, plus, minus, exponent in failing_rows[:5]:
            print(
                f"    drift={drift:.2f} seed={seed} plus={plus:+.3e} "
                f"minus={minus:+.3e} exp={exponent:.3f}"
            )
        print("  the failure is a sign-orientation boundary, not a control leak")
    else:
        print("  no boundary failures found in this audit window")


if __name__ == "__main__":
    main()
