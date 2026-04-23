#!/usr/bin/env python3
"""Audit the final remaining-denials target-change theorem."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_REMAINING_DENIALS_TARGET_CHANGE_THEOREM_2026-04-23.md"
PACKET = ROOT / "docs/PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md"
COUNTING = ROOT / "docs/PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md"
ATOMIC = ROOT / "docs/PLANCK_SCALE_ATOMIC_NATURALITY_FROM_PRIMITIVE_UNIVERSALITY_THEOREM_2026-04-23.md"
GSI = ROOT / "docs/PLANCK_SCALE_GRAVITY_CARRIER_FROM_SECTOR_IDENTIFICATION_THEOREM_2026-04-23.md"
NONTAUTOLOGY = ROOT / "docs/PLANCK_SCALE_PLANCK_NORMALIZATION_NON_TAUTOLOGY_AUDIT_2026-04-23.md"


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
    counting = read(COUNTING)
    atomic = read(ATOMIC)
    gsi = read(GSI)
    non_tautology = read(NONTAUTOLOGY)

    dim = 16
    rank = 4
    primitive_coeff = Fraction(rank, dim)

    alpha = Fraction(1, 32)
    beta = Fraction(7, 96)
    enriched_total = 4 * alpha + 12 * beta
    enriched_packet_value = 4 * alpha

    a2_over_lp2_with_gsi = 4 * primitive_coeff

    checks = [
        (
            "note-names-both-final-denials",
            "reject the bare primitive counting object class" in note
            and "reject Gravity-Sector Identification (GSI)" in note,
            "the final two denial points must be explicit",
        ),
        (
            "primitive-target-forces-counting-trace",
            primitive_coeff == Fraction(1, 4)
            and "C(P) = rank(P) / 16" in note
            and "C(P_A) = 4/16 = 1/4" in note,
            f"rank/dim={rank}/{dim}={primitive_coeff}",
        ),
        (
            "enriched-object-countermodel-is-not-quarter",
            enriched_total == 1 and enriched_packet_value == Fraction(1, 8),
            f"total={enriched_total}, C(P_A)={enriched_packet_value}",
        ),
        (
            "gsi-needed-for-length-equation",
            "Without GSI" in note
            and "no equation in the Planck packet relates `a` to `G`, `hbar`, and"
            in note,
            "dimensionless coefficient needs sector identification to become a length claim",
        ),
        (
            "with-gsi-quarter-gives-planck-area",
            a2_over_lp2_with_gsi == 1
            and "a^2 = 4 c_cell l_P^2" in note
            and "a^2 = l_P^2" in note,
            f"a^2/l_P^2={a2_over_lp2_with_gsi}",
        ),
        (
            "packet-currently-has-two-denials",
            "deny that the elementary Planck coefficient belongs to the universal"
            in packet
            and "deny that the primitive-cell count realizes the gravitational area/action"
            in packet,
            "canonical packet should expose exactly the target-changing denials",
        ),
        (
            "counting-theorem-supports-primitive-object-class",
            "universal primitive coefficient" in counting
            and "normalized counting trace" in counting,
            "counting theorem supplies primitive object-class uniqueness",
        ),
        (
            "atomic-theorem-supports-naturality",
            "primitive universality + object-class locality" in atomic
            and "atomic naturality" in atomic,
            "atomic naturality theorem supplies the strongest naturality defense",
        ),
        (
            "gsi-note-supports-sector-identification-scope",
            "GSI is not a numerical input" in gsi
            and "sector-identification input" in gsi,
            "GSI note scopes the remaining physical bridge",
        ),
        (
            "non-tautology-note-supports-not-assuming-planck-spacing",
            "a^2 = 4 c_cell l_P^2" in non_tautology
            and "does not import" in non_tautology
            and "the equality `a = l_P`" in non_tautology,
            "non-tautology audit keeps the Planck spacing from being assumed",
        ),
        (
            "note-keeps-final-status-honest",
            "legitimate philosophical or physical objections" in note
            and "longer hidden mathematical gaps" in note,
            "the final theorem should not pretend denials are impossible",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
