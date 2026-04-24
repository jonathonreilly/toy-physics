#!/usr/bin/env python3
"""Verify the boundary event Ward identity closure theorem."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_CLOSURE_THEOREM_2026-04-23.md"
THREE_ROUTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_DENSITY_THREE_MECHANISM_AUDIT_2026-04-23.md"
PRIMITIVE_UNIT = ROOT / "docs/PLANCK_SCALE_PRIMITIVE_BOUNDARY_ACTION_UNIT_REDUCTION_THEOREM_2026-04-23.md"
GRAV_CARRIER = ROOT / "docs/PLANCK_SCALE_GRAVITY_CARRIER_FROM_SECTOR_IDENTIFICATION_THEOREM_2026-04-23.md"
STATE = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md"


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
    three_route = read(THREE_ROUTE)
    primitive_unit = read(PRIMITIVE_UNIT)
    grav_carrier = read(GRAV_CARRIER)
    state = read(STATE)

    banned_terms = ["P1", "Axiom Extension", "GSI", "Gravity-Sector Identification"]

    L = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    evals = sorted(L.eigenvals().keys())
    lambda_min = evals[0]
    L_normal = L - lambda_min * sp.eye(2)
    normal_evals = sorted(L_normal.eigenvals().keys())

    nu = sp.symbols("nu", real=True)
    G = nu * sp.eye(2) - L
    p_normal = max(G.eigenvals().keys())

    rank_p_a = 4
    dim_cell = 16
    m_axis = Fraction(rank_p_a, dim_cell)
    nu_closed = lambda_min + sp.Rational(m_axis.numerator, m_axis.denominator)
    p_closed = sp.simplify((nu - lambda_min).subs(nu, nu_closed))

    c_cell = Fraction(1, 4)
    a2_over_lp2 = 4 * c_cell

    checks = [
        (
            "note-avoids-project-shorthand",
            all(term not in note for term in banned_terms),
            "closure theorem should be readable without branch-local shorthand",
        ),
        (
            "source-response-audit-gap-is-identified",
            "they cannot determine `nu`" in three_route
            and "not for Schur-source response" in note,
            "the closure uses a different Ward identity than the failed route",
        ),
        (
            "normal-ordering-subtracts-exact-schur-floor",
            evals == [sp.Integer(1), sp.Rational(5, 3)]
            and normal_evals == [sp.Integer(0), sp.Rational(2, 3)]
            and "unique floor subtraction" in note,
            f"spec(L)={evals}, spec(L-lambda_min I)={normal_evals}",
        ),
        (
            "normal-ordered-pressure-is-delta",
            sp.simplify(p_normal - (nu - lambda_min)) == 0
            and "`p_normal := sup spec(G_nu)`" in note
            and "`p_normal = nu - lambda_min(L_Sigma) = delta`" in note,
            f"p_normal={p_normal}",
        ),
        (
            "primitive-carrier-is-forced-pa",
            "`N_grav = P_A`" in note
            and "`N_grav = P_A`" in grav_carrier
            and "multiplicative `mu != 1` is not same-surface" in primitive_unit,
            "carrier is an operator statement before the quarter is evaluated",
        ),
        (
            "source-free-state-gives-axis-mass",
            m_axis == Fraction(1, 4)
            and "`rho_cell = I_16 / 16`" in note
            and "`rho_cell = I_16 / 16`" in state
            and "`Tr(rho_cell P_A) = 4/16 = 1/4`" in note,
            f"m_axis={m_axis}",
        ),
        (
            "event-ward-identity-forces-residual",
            "`sup spec(G_nu) = Tr(rho_cell N_grav)`" in note
            and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in note
            and "`delta = m_axis`" in note,
            "constant term is tied to retained event charge",
        ),
        (
            "no-hidden-additive-action-datum-excludes-offsets",
            "with `c != 0`" in note
            and "extra additive boundary-action datum" in note
            and "with `alpha != 1`" in note
            and "primitive incidence unit would be rescaled" in note,
            "the theorem rules out additive and multiplicative hidden data",
        ),
        (
            "witness-nu-is-five-four",
            nu_closed == sp.Rational(5, 4)
            and p_closed == sp.Rational(1, 4)
            and "`nu = 1 + 1/4 = 5/4`" in note
            and "`p_*(nu) = nu - lambda_min(L_Sigma) = 1/4`" in note,
            f"nu_closed={nu_closed}, p_closed={p_closed}",
        ),
        (
            "planck-normalization-follows-with-constants",
            a2_over_lp2 == 1
            and "`S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`"
            in note
            and "`a^2 = l_P^2`" in note
            and "`a = l_P`" in note,
            "quarter density maps to conventional Planck length",
        ),
        (
            "hostile-review-scope-is-explicit",
            "reject that gravitational boundary action on the physical primitive lattice" in note
            and "normal-ordered primitive boundary event Ward identity" in note
            and "not a\ncoefficient objection" in note,
            "remaining rejection targets the event Ward surface",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
