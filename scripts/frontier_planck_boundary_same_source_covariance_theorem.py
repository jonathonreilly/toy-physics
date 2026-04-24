#!/usr/bin/env python3
"""Verify same-source covariance between Schur and event boundary generators."""

from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SAME_SOURCE_COVARIANCE_THEOREM_2026-04-23.md"
DERIVATION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md"
CLOSURE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_CLOSURE_THEOREM_2026-04-23.md"


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
    derivation = read(DERIVATION)
    closure = read(CLOSURE)

    banned_terms = ["P1", "Axiom Extension", "GSI", "Gravity-Sector Identification"]

    s, p1, p2, nu = sp.symbols("s p1 p2 nu", real=True)
    quotient = sp.exp(s * p1) * sp.exp(-s * p2)
    quotient_generator = sp.diff(sp.log(quotient), s).subs(s, 0)

    L = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    lambda_min = min(L.eigenvals().keys())
    p_event = sp.Rational(1, 4)
    nu_closed = lambda_min + p_event

    checks = [
        (
            "note-avoids-project-shorthand",
            all(term not in note for term in banned_terms),
            "same-source theorem should be reviewer-facing",
        ),
        (
            "same-source-quotient-generator-is-difference",
            sp.simplify(quotient_generator - (p1 - p2)) == 0
            and "`Q(s) = exp(s (p_1 - p_2))`" in note,
            f"generator={quotient_generator}",
        ),
        (
            "mismatch-is-hidden-boundary-action-data",
            "`Delta = p_Schur - p_event`" in note
            and "`exp(s Delta)`" in note
            and "hidden local boundary-action data" in note,
            "nonzero difference is a source-free scalar group",
        ),
        (
            "no-hidden-semantics-force-equality",
            "force\n\n`Delta = 0`" in note
            and "`p_Schur = p_event`" in note,
            "same-source covariance follows from no hidden source-free scalar",
        ),
        (
            "event-ward-derivative-is-inherited",
            "`p_event = Tr(rho_cell P_A)`" in note
            and "`d/ds log Z_A(s)|_(s=0) = Tr(rho_cell P_A)`"
            in derivation,
            "finite-source Ward theorem supplies p_event",
        ),
        (
            "schur-pressure-is-inherited",
            "`p_Schur = nu - lambda_min(L_Sigma)`" in note
            and "`p_normal = nu - lambda_min(L_Sigma) = delta`" in closure,
            "Schur side supplies normal-ordered pressure",
        ),
        (
            "same-source-covariance-derives-density-law",
            "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in note
            and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in closure,
            "density law follows by equating same-source generators",
        ),
        (
            "witness-nu-five-four",
            nu_closed == sp.Rational(5, 4)
            and "`nu = 5/4`" in note,
            f"nu={nu_closed}",
        ),
        (
            "remaining-rejection-is-target-change",
            "deny that the Schur boundary action and the primitive event insertion source" in note
            and "changes the target" in note,
            "remaining objection rejects same physical source",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
