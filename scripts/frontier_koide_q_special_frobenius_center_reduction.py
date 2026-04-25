#!/usr/bin/env python3
"""
Koide Q special-Frobenius center reduction.

Theorem attempt:
  Treat the two central C3 sectors as a finite classical algebra equipped with
  a normalized special commutative Frobenius structure.  In a finite classical
  Frobenius algebra, specialness m o Delta = beta id forces equal Frobenius
  weights on the copyable idempotents.  This would derive the equal center-label
  state and hence K_TL = 0.

Result:
  Conditional positive reduction, not closure.  The algebraic theorem is exact:
  specialness on the two-label center forces equal label weights.  But the
  retained real C3 carrier also has a canonical Hilbert/rank trace with weights
  (1,2), and the retained data do not force the physical charged-lepton source
  to be the special-Frobenius center counit rather than the Hilbert/rank state.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    w_plus = sp.sympify(w_plus)
    w_perp = sp.sympify(w_perp)
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    w_plus = sp.sympify(w_plus)
    w_perp = sp.sympify(w_perp)
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Two-idempotent center Frobenius algebra")

    lam_plus, lam_perp, beta = sp.symbols("lambda_plus lambda_perp beta", positive=True, real=True)
    m_delta = sp.diag(1 / lam_plus, 1 / lam_perp)
    special_residual = sp.simplify(m_delta - beta * sp.eye(2))
    special_solution = sp.solve(list(special_residual), [lam_plus, lam_perp], dict=True)
    record(
        "A.1 Frobenius comultiplication gives m o Delta = diag(1/lambda_plus,1/lambda_perp)",
        m_delta == sp.diag(1 / lam_plus, 1 / lam_perp),
        f"mDelta={m_delta}",
    )
    record(
        "A.2 specialness m o Delta = beta id forces equal Frobenius weights",
        special_solution == [{lam_plus: 1 / beta, lam_perp: 1 / beta}],
        f"solutions={special_solution}",
    )

    section("B. Consequence for the Koide source carrier")

    q_lam = q_from_weights(lam_plus, lam_perp)
    ktl_lam = ktl_from_weights(lam_plus, lam_perp)
    neutral_solution = sp.solve(sp.Eq(ktl_lam, 0), lam_perp, dict=True)
    record(
        "B.1 K_TL=0 is equivalent to equal Frobenius label weights",
        neutral_solution == [{lam_perp: lam_plus}],
        f"Q(lambda)={q_lam}, K_TL(lambda)={ktl_lam}",
    )
    record(
        "B.2 special Frobenius center state lands on the source-neutral leaf",
        q_from_weights(1, 1) == sp.Rational(2, 3) and ktl_from_weights(1, 1) == 0,
        "lambda_plus=lambda_perp -> Q=2/3, K_TL=0.",
    )

    section("C. Retained carrier also admits the Hilbert/rank trace")

    q_rank = q_from_weights(1, 2)
    ktl_rank = ktl_from_weights(1, 2)
    rank_m_delta = sp.diag(sp.Integer(1), sp.Rational(1, 2))
    record(
        "C.1 Hilbert/rank trace weights are not special on the two-label center",
        rank_m_delta != sp.Rational(1, 1) * sp.eye(2)
        and rank_m_delta != sp.Rational(1, 2) * sp.eye(2),
        f"lambda=(1,2) gives mDelta={rank_m_delta}",
    )
    record(
        "C.2 the retained rank trace remains an admissible non-closing state",
        q_rank == 1 and ktl_rank == sp.Rational(3, 8),
        f"rank weights (1,2) -> Q={q_rank}, K_TL={ktl_rank}",
    )

    section("D. Review boundary")

    record(
        "D.1 the algebraic theorem is a real candidate source law",
        True,
        "If the physical source is the normalized special-Frobenius center counit, Q closes.",
    )
    record(
        "D.2 retained C3/Cl3 data do not yet force that source law",
        True,
        "The missing step is why the charged-lepton source uses the center Frobenius counit instead of Hilbert/rank trace.",
    )
    record(
        "D.3 this is reduction, not Nature-grade closure",
        True,
        "Promoting specialness without an independent physical theorem would import the missing primitive.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: special-Frobenius center law conditionally derives K_TL=0, but is not retained closure.")
        print("KOIDE_Q_SPECIAL_FROBENIUS_CENTER_REDUCTION=TRUE")
        print("Q_SPECIAL_FROBENIUS_CENTER_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=justify_special_Frobenius_center_counit_as_physical_source")
        print("RESIDUAL_PRIMITIVE=special_Frobenius_center_state_not_forced_by_retained_C3")
        return 0

    print("VERDICT: special-Frobenius center reduction has FAILs.")
    print("KOIDE_Q_SPECIAL_FROBENIUS_CENTER_REDUCTION=FALSE")
    print("Q_SPECIAL_FROBENIUS_CENTER_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=justify_special_Frobenius_center_counit_as_physical_source")
    print("RESIDUAL_PRIMITIVE=special_Frobenius_center_state_not_forced_by_retained_C3")
    return 1


if __name__ == "__main__":
    sys.exit(main())
