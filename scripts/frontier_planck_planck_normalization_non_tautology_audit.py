#!/usr/bin/env python3
"""Audit runner for the Planck-normalization non-tautology note."""

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_PLANCK_NORMALIZATION_NON_TAUTOLOGY_AUDIT_2026-04-23.md"
AREA_NOTE = ROOT / "docs/PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md"
CARRIER_NOTE = ROOT / "docs/PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md"
PACKET_NOTE = ROOT / "docs/PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md"


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def main() -> int:
    note = NOTE.read_text()
    area_note = AREA_NOTE.read_text()
    carrier_note = CARRIER_NOTE.read_text()
    packet_note = PACKET_NOTE.read_text()

    c_cell = Fraction(1, 4)
    a2_over_lp2 = 4 * c_cell
    lambda_from_cell = 4 * c_cell
    counterfactuals = {
        Fraction(1, 8): Fraction(1, 2),
        Fraction(1, 4): Fraction(1, 1),
        Fraction(1, 1): Fraction(4, 1),
    }

    checks = [
        (
            "note-names-tautology-objection",
            "tautology objection" in note and "Does matching" in note,
            "issue #5 should be explicitly scoped",
        ),
        (
            "imports-gravity-law-and-constants",
            "S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)" in note
            and "l_P^2 := hbar G / c_light^3" in note
            and "`G`, `hbar`,\n`c_light`, and `k_B`" in note,
            "imports are gravitational area/action normalization plus constants",
        ),
        (
            "does-not-import-lattice-spacing",
            "the value of `a`" in note
            and "the equality `a = l_P`" in note
            and "a convention that one primitive cell has Planck area" in note,
            "lattice spacing should be listed as not imported",
        ),
        (
            "cell-density-is-explicit",
            "S_cell / k_B = c_cell A / a^2" in note,
            "microscopic density retains unknown a",
        ),
        (
            "general-matching-before-substitution",
            "a^2 = 4 c_cell l_P^2" in note
            and "a = 2 sqrt(c_cell) l_P" in note,
            "matching alone leaves a coefficient-dependent spacing",
        ),
        (
            "lambda-counterfactual-present",
            "c_cell = lambda / 4" in note
            and "a^2 = lambda l_P^2" in note
            and "a = sqrt(lambda) l_P" in note,
            "arbitrary coefficient would give sqrt(lambda) times l_P",
        ),
        (
            "quarter-derived-from-native-packet",
            "dim(H_cell) = 16" in note
            and "rank(P_A) = 4" in note
            and "c_cell = Tr(rho_cell P_A) = 4/16 = 1/4" in note,
            "exact quarter should be a microscopic input, not a fitted scale",
        ),
        (
            "quarter-forces-one-planck-area",
            a2_over_lp2 == 1 and lambda_from_cell == 1,
            f"a^2/l_P^2={a2_over_lp2}, lambda={lambda_from_cell}",
        ),
        (
            "counterfactuals-show-not-tautological",
            counterfactuals[Fraction(1, 8)] == Fraction(1, 2)
            and counterfactuals[Fraction(1, 4)] == 1
            and counterfactuals[Fraction(1, 1)] == 4
            and "c_cell = 1/8" in note
            and "c_cell = 1" in note,
            "other dimensionless coefficients would not give a=l_P",
        ),
        (
            "related-notes-linked",
            "PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md" in note
            and "PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md"
            in note
            and "PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md" in note,
            "audit should point to the theorem sources it connects",
        ),
        (
            "existing-area-note-supports-general-normalization",
            "a^2 = 4 c_cell l_P^2" in area_note
            and "No independent observed lattice spacing is inserted" in area_note,
            "existing normalization note already keeps a solved",
        ),
        (
            "existing-carrier-note-scopes-physical-matching",
            "Still a physical matching requirement" in carrier_note
            and "reject that the direct primitive boundary count is the microscopic carrier"
            in carrier_note,
            "carrier identification remains the honest denial point",
        ),
        (
            "existing-packet-note-supplies-quarter",
            "c_cell = Tr(rho_cell P_A) = 4/16 = 1/4" in packet_note
            and "a^2 = 4 c_cell l_P^2" in packet_note,
            "native packet supplies the dimensionless coefficient before normalization",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
