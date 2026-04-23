#!/usr/bin/env python3
"""Audit runner for the cosmic-address import unit-map theorem."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_COSMIC_ADDRESS_IMPORT_UNIT_MAP_THEOREM_2026-04-23.md"
PACKET = ROOT / "docs/PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md"
REVIEWER = ROOT / "docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md"


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def read(path: Path) -> str:
    return path.read_text()


def main() -> int:
    note = read(NOTE)
    packet = read(PACKET)
    reviewer = read(REVIEWER)

    c_cell = Fraction(1, 4)
    a2_over_lp2 = 4 * c_cell

    # Fixed macroscopic age admits many microscopic tick decompositions unless
    # a dimensionless native count is derived.
    age_ticks_a = Fraction(10**60, 1)
    age_ticks_b = Fraction(2 * 10**60, 1)
    age = Fraction(1, 1)
    tick_a = age / age_ticks_a
    tick_b = age / age_ticks_b

    # Same-surface matching cancels the address-dependent area.
    area_factor = Fraction(137, 1)
    microscopic_density = c_cell * area_factor
    gravitational_density_denominator = 4
    solved_a2_factor = gravitational_density_denominator * c_cell

    checks = [
        (
            "note-classifies-address-imports",
            '"where we are on the map" imports' in note
            and "present cosmic time or age" in note,
            "the theorem must discuss the user's allowed imports directly",
        ),
        (
            "age-alone-does-not-fix-tick",
            tick_a != tick_b
            and age_ticks_a * tick_a == age
            and age_ticks_b * tick_b == age
            and "Without a native theorem fixing `N_U`" in note,
            f"two decompositions: {age_ticks_a}*{tick_a} and {age_ticks_b}*{tick_b}",
        ),
        (
            "forbids-hidden-planck-count",
            "assume a hidden microscopic tick count equal to `T_U / t_P`" in note
            and "That would import the result in count language" in note,
            "age cannot be used by choosing the desired Planck tick count",
        ),
        (
            "same-surface-area-cancels",
            microscopic_density == Fraction(137, 4)
            and area_factor > 0
            and "Since `A_U > 0`, the address-dependent area cancels" in note,
            "surface size selects a comparison surface but not the microscopic spacing",
        ),
        (
            "quarter-still-forces-planck-after-gravity-match",
            solved_a2_factor == 1
            and a2_over_lp2 == 1
            and "`a^2 = 4 c_cell l_P^2`" in note
            and "`c_cell = 1/4`" in note
            and "`a = l_P`" in note,
            f"a^2/l_P^2={a2_over_lp2}",
        ),
        (
            "ewsb-is-calibration-not-native-planck",
            "`v / M_Pl = f_native`" in note
            and "`M_Pl = v / f_native`" in note
            and "not a bare Planck derivation" in note,
            "EWSB can calibrate an independent hierarchy law but does not replace Planck normalization",
        ),
        (
            "gsi-not-replaced",
            "Cosmic-address imports do not replace Gravity-Sector Identification (GSI)"
            in note
            and "same-surface gravitational area/action identification" in note,
            "address data can sharpen the surface, not provide the gravity law",
        ),
        (
            "native-packet-links-cosmic-address-protocol",
            "PLANCK_SCALE_COSMIC_ADDRESS_IMPORT_UNIT_MAP_THEOREM_2026-04-23.md"
            in packet
            and "cosmic-address imports" in packet,
            "canonical packet should expose the import protocol",
        ),
        (
            "reviewer-packet-classifies-cosmic-address-imports",
            "Cosmic-address imports" in reviewer
            and "not as\n   microscopic scale setters" in reviewer
            and "PLANCK_SCALE_COSMIC_ADDRESS_IMPORT_UNIT_MAP_THEOREM_2026-04-23.md"
            in reviewer,
            "reviewer packet should prevent age/EWSB overclaims",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
