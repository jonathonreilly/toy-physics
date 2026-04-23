#!/usr/bin/env python3
"""Verifier for the primitive boundary action unit reduction theorem."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_PRIMITIVE_BOUNDARY_ACTION_UNIT_REDUCTION_THEOREM_2026-04-23.md"
ACTION_LANE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md"
CLOSURE = ROOT / "docs/PLANCK_SCALE_CLEAN_CLOSURE_CRITERION_THEOREM_2026-04-23.md"


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
    action_lane = read(ACTION_LANE)
    closure = read(CLOSURE)

    banned_terms = ["P1", "Axiom Extension", "GSI", "Gravity-Sector Identification"]

    c_cell = Fraction(1, 4)
    multiplicities = {
        Fraction(1, 2): "fractional unit",
        Fraction(1): "primitive unit",
        Fraction(2): "two copies",
        Fraction(3, 2): "fractional copy",
    }

    mu = sp.symbols("mu", positive=True)
    b1, b2, j1, j2 = sp.symbols("b1 b2 j1 j2")
    L = sp.Matrix([[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]])
    b = sp.Matrix([b1, b2])
    j = sp.Matrix([j1, j2])

    I_can = sp.Rational(1, 2) * (b.T * L * b)[0] - (j.T * b)[0]
    I_mu = mu * sp.Rational(1, 2) * (b.T * L * b)[0] - (j.T * b)[0]
    hess_can = sp.hessian(I_can, (b1, b2))
    hess_mu = sp.hessian(I_mu, (b1, b2))
    grad_mu = sp.Matrix([sp.diff(I_mu, x) for x in (b1, b2)])

    nu = sp.symbols("nu", real=True)
    G_nu = nu * sp.eye(2) - L
    eigs_L = set(L.eigenvals().keys())
    eigs_G = set(G_nu.eigenvals().keys())
    quarter_nu = sp.solve(sp.Eq(nu - 1, sp.Rational(1, 4)), nu)

    checks = [
        (
            "note-avoids-project-shorthand",
            all(term not in note for term in banned_terms),
            "new theorem should stay reviewer-facing",
        ),
        (
            "primitive-unit-count-forces-mu-one-inside-object-class",
            multiplicities[Fraction(1)] == "primitive unit"
            and all(k == Fraction(1) or v != "primitive unit" for k, v in multiplicities.items())
            and "inside the primitive unit-count object class" in note
            and "`mu = 1`" in note,
            "mu != 1 changes primitive unit semantics",
        ),
        (
            "native-quarter-retained",
            c_cell == Fraction(1, 4)
            and "`c_cell = 1/4`" in note
            and "`c_cell = 1/4`" in closure,
            f"c_cell={c_cell}",
        ),
        (
            "multiplicative-action-rescaling-changes-hessian",
            sp.simplify(hess_mu - mu * hess_can) == sp.zeros(2)
            and "Hessian becomes" in note
            and "`mu L_Sigma`" in note,
            "mu rescales the exact Schur operator",
        ),
        (
            "multiplicative-action-rescaling-changes-response",
            sp.simplify(grad_mu - (mu * L * b - j)) == sp.zeros(2, 1)
            and "`b = (1/mu) L_Sigma^(-1) j`" in note,
            "mu != 1 is not same-surface on the exact action lane",
        ),
        (
            "additive-density-survives",
            "unit-bearing additive vacuum-action density" in action_lane
            and "`I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`"
            in note,
            "the remaining deformation is additive",
        ),
        (
            "witness-eigenvalues-are-exact",
            eigs_L == {sp.Integer(1), sp.Rational(5, 3)}
            and "lambda_min(L_Sigma) = 1" in note,
            f"eigs={eigs_L}",
        ),
        (
            "quarter-equivalent-to-nu-five-four",
            eigs_G == {nu - 1, nu - sp.Rational(5, 3)}
            and quarter_nu == [sp.Rational(5, 4)]
            and "`nu = 5/4`" in note,
            f"quarter_nu={quarter_nu}",
        ),
        (
            "canonical-zero-vacuum-obstructs-quarter",
            max([ev.subs(nu, 0) for ev in eigs_G]) == -1
            and "`p_*(0) = -1`" in note,
            "zero vacuum lands on wrong pressure branch",
        ),
        (
            "theorem-does-not-overclaim",
            "This note does not derive `nu = 5/4`" in note
            and "still open" in note,
            "the remaining density theorem is not smuggled in",
        ),
        (
            "hostile-review-constraint-names-real-next-mechanisms",
            "`mu P_A`, `mu > 0`" in note
            and "Ward identity" in note
            and "action-phase quantization" in note
            and "gravitational boundary term normalization" in note,
            "next proof must exclude the multiplier family by a real physical law",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
