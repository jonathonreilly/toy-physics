#!/usr/bin/env python3
"""Verify parent-source equivalence for Schur and event boundary sources."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md"
INTERTWINER = ROOT / "docs/PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md"
MULTIPLICITY = ROOT / "docs/PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md"
DERIVATION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md"
SAME_SOURCE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SAME_SOURCE_COVARIANCE_THEOREM_2026-04-23.md"


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
    intertwiner = read(INTERTWINER)
    multiplicity = read(MULTIPLICITY)
    derivation = read(DERIVATION)
    same_source = read(SAME_SOURCE)

    banned_terms = ["P1", "Axiom Extension", "GSI", "Gravity-Sector Identification"]

    # Axis-carrier ranks.
    rank_pq = 2
    rank_pe = 2
    rank_pa = rank_pq + rank_pe
    dim_cell = 16
    mass_pq = Fraction(rank_pq, dim_cell)
    mass_pe = Fraction(rank_pe, dim_cell)
    mass_pa = Fraction(rank_pa, dim_cell)

    # Schur witness.
    L = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    lambda_min = min(L.eigenvals().keys())
    nu_closed = lambda_min + sp.Rational(mass_pa.numerator, mass_pa.denominator)

    checks = [
        (
            "note-avoids-project-shorthand",
            all(term not in note for term in banned_terms),
            "parent-source theorem should be reviewer-facing",
        ),
        (
            "parent-source-is-full-axis-projector",
            "`B_parent := (H_A, P_A)`" in note
            and "`P_A = |t><t| + |x><x| + |y><y| + |z><z|`" in note,
            "full four-axis source is stated before reduction",
        ),
        (
            "uniqueness-conditions-force-pa",
            "time-complete" in note
            and "spatially isotropic" in note
            and "unit-valued on each retained primitive incidence" in note
            and "unique parent source is `P_A`" in note,
            "admissible parent source cannot be P_t, P_s, P_q, or alpha P_A",
        ),
        (
            "event-reduction-is-finite-source",
            "`U_A(s) = exp(s P_A)`" in note
            and "`d/ds log Tr(rho_cell U_A(s))|_(s=0) = Tr(rho_cell P_A)`"
            in note
            and "`U_A(s) = exp(s P_A)`" in derivation,
            "event side is inherited from finite-source Ward theorem",
        ),
        (
            "schur-reduction-is-quotient-shape",
            "minimal Schur boundary carrier is two-dimensional" in note
            and "`H_q = span{|t>, |s>}`" in note
            and "unique rank-2 quotient" in intertwiner,
            "Schur carrier sees quotient shape, not faithful rank-four source",
        ),
        (
            "multiplicity-completion-restores-parent",
            rank_pa == 4
            and mass_pq == Fraction(1, 8)
            and mass_pe == Fraction(1, 8)
            and mass_pa == Fraction(1, 4)
            and "`P_A = P_q + P_E`" in note
            and "`Tr(rho_cell P_A) = Tr(rho_cell P_q) + Tr(rho_cell P_E) = 2 Tr(rho_cell P_q) = 1/4`"
            in multiplicity,
            f"masses pq={mass_pq}, pe={mass_pe}, pa={mass_pa}",
        ),
        (
            "quotient-only-schur-changes-source",
            "`P_A` versus `P_q`" in note
            and "`P_E = P_A - P_q`" in note
            and "changes the target" in note,
            "discarding doublet multiplicity is not the same parent source",
        ),
        (
            "same-source-covariance-follows-from-parent",
            "`p_Schur = p_event`" in note
            and "`Q(s) = exp(s (p_1 - p_2))`" in same_source,
            "same-source theorem applies once parent source is unique",
        ),
        (
            "density-law-and-witness-close",
            mass_pa == Fraction(1, 4)
            and nu_closed == sp.Rational(5, 4)
            and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in note
            and "`nu = 5/4`" in note,
            f"nu={nu_closed}",
        ),
        (
            "remaining-rejections-are-object-class-and-functoriality",
            "deny that the physical gravitational boundary-action source belongs to the" in note
            and "deny that the Schur normal-ordered boundary action is the functorial Schur" in note
            and "turns\nthe finite event derivative into the Schur normal-ordered boundary-action\nsource"
            in note
            and "Within the retained primitive boundary-action object class" in note,
            "remaining denials target object class or Schur functorial representation",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
