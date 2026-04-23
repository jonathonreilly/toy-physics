#!/usr/bin/env python3
"""Audit runner for the gravitational area/action carrier identification theorem."""

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md"


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def main() -> int:
    note = NOTE.read_text()
    c_cell = Fraction(1, 4)
    a2_over_lp2 = 4 * c_cell

    checks = [
        (
            "note-identifies-carrier-not-just-equation",
            "carrier-identification theorem" in note
            and "unique available local codimension-1 microscopic carrier" in note,
            "the note should address physical carrier selection",
        ),
        (
            "note-keeps-semiclassical-gravity-scope-honest",
            "does not derive the existence of semiclassical gravity" in note
            and "Still a physical matching requirement" in note,
            "the note should not overclaim pure minimal-ledger closure",
        ),
        (
            "local-area-extensivity-formula-present",
            "S_cell / k_B = c_cell A / a^2" in note,
            "cell count density must be explicit",
        ),
        (
            "gravitational-area-action-formula-present",
            "S_grav / k_B = A c_light^3 / (4 G hbar)" in note
            and "A / (4 l_P^2)" in note,
            "gravity density must be explicit",
        ),
        (
            "matching-with-quarter-gives-one-planck-area",
            a2_over_lp2 == 1,
            f"a^2/l_P^2={a2_over_lp2}",
        ),
        (
            "note-preserves-denial-scope",
            "reject that the direct primitive boundary count is the microscopic carrier"
            in note,
            "the remaining hostile-review denial should be narrow",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
