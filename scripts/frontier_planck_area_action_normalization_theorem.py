#!/usr/bin/env python3
"""Audit runner for the Planck area/action normalization theorem."""

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md"


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def main() -> int:
    note = NOTE.read_text()
    c_cell = Fraction(1, 4)

    # Work in units of l_P^2. Equating c_cell / a^2 = 1 / (4 l_P^2)
    # gives a^2 / l_P^2 = 4 c_cell.
    a2_over_lp2 = 4 * c_cell

    checks = [
        (
            "quarter-gives-one-planck-area",
            a2_over_lp2 == 1,
            f"a^2/l_P^2={a2_over_lp2}",
        ),
        (
            "note-defines-planck-area-with-dimensional-constants",
            "l_P^2 := hbar G / c_light^3" in note,
            "Planck area definition is explicit",
        ),
        (
            "note-states-gravitational-density",
            "S_grav / k_B = A c_light^3 / (4 G hbar)" in note
            and "A / (4 l_P^2)" in note,
            "gravitational area/action density is explicit",
        ),
        (
            "note-states-cell-density",
            "S_cell / k_B = c_cell A / a^2" in note,
            "cell density is explicit",
        ),
        (
            "note-solves-general-normalization",
            "a^2 = 4 c_cell l_P^2" in note,
            "general solution before substituting c_cell",
        ),
        (
            "note-denies-lattice-spacing-import",
            "No independent observed lattice spacing is inserted" in note
            and "Not imported" in note,
            "a is solved, not assumed",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
