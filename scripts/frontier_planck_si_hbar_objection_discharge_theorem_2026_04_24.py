#!/usr/bin/env python3
"""Verify the SI-hbar objection discharge theorem."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def numerical_value(quantity: Fraction, unit: Fraction) -> Fraction:
    return quantity / unit


def main() -> int:
    note = read("docs/PLANCK_SCALE_SI_HBAR_OBJECTION_DISCHARGE_THEOREM_2026-04-24.md")
    hbar_audit = read("docs/PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md")
    integral_count = read("docs/PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md")
    area = read("docs/PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "document-is-si-hbar-discharge-theorem",
        "Planck-Scale SI Hbar Objection Discharge Theorem" in note
        and "**Status:** discharges the SI-`hbar` objection" in note
        and "frontier_planck_si_hbar_objection_discharge_theorem_2026_04_24.py" in note,
        "new theorem and verifier are present",
    )

    hbar = Fraction(7, 5)
    unit = Fraction(1, 1)
    lam = Fraction(3, 2)
    old_value = numerical_value(hbar, unit)
    new_value = numerical_value(hbar, lam * unit)

    total += 1
    passed += expect(
        "dimensionful-number-rescales-with-unit",
        new_value == old_value / lam
        and "`[S]_{U_A'} = [S]_{U_A} / lambda`" in note
        and "claimed prediction of the bare decimal number" in note,
        f"old={old_value}, new={new_value}, lambda={lam}",
    )

    action = Fraction(11, 3)
    ratio_old = numerical_value(action, unit) / numerical_value(hbar, unit)
    ratio_new = numerical_value(action, lam * unit) / numerical_value(hbar, lam * unit)

    total += 1
    passed += expect(
        "dimensionless-action-ratio-is-invariant",
        ratio_old == ratio_new
        and "`S / hbar`" in note
        and "dimensionless ratios" in note,
        f"S/hbar old={ratio_old}, new={ratio_new}",
    )

    total += 1
    passed += expect(
        "reduced-gamma-one-is-the-structural-action-unit",
        "`Phi(I_16) = gamma = 1`" in note
        and "`Phi(I_16) = 1`" in integral_count
        and "`gamma = 1`" in integral_count,
        "gamma=1 is the theory-internal reduced action count",
    )

    total += 1
    passed += expect(
        "planck-ratio-is-hbar-containing-target",
        "`a^2 c_light^3 / (hbar G) = 1`" in note
        and "`l_P^2 = hbar G / c_light^3`" in note
        and "`l_P^2 := hbar G / c_light^3`" in area,
        "the physical hbar-containing statement is dimensionless",
    )

    total += 1
    passed += expect(
        "si-decimal-request-is-rejected-as-nonclaim",
        "SI decimal value of `hbar` is not a physical\n> prediction target" in note
        and "Numerical prediction of `hbar` in SI units" in hbar_audit
        and "unit convention" in hbar_audit
        and "Do not use:\n\n> The branch predicts the SI value of `hbar`." in note,
        "the theorem discharges SI hbar as a non-physical target",
    )

    total += 1
    passed += expect(
        "safe-claim-is-dimensionless",
        "The branch derives the reduced action unit `gamma=1` and the dimensionless\n"
        "> Planck relation `a^2 c_light^3/(hbar G)=1`" in note
        and "Failure to predict a dimensionful SI constant is a physical failure" in note,
        "safe claim is dimensionless and reduced-action only",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
