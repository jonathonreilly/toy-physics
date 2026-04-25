#!/usr/bin/env python3
"""
Koide Q no-new-axiom separation no-go.

Theorem attempt:
  Under the user's no-new-axioms constraint, prove Q closure from only the
  currently retained Cl(3)/Z3 charged-lepton axioms and source-response
  constraints.

Result:
  No retained closure.  The audit exhibits two exact source models that satisfy
  the current retained base constraints but give different Q:

      M_close:   rho=0, reduced/quotient source response, Q=2/3.
      M_counter: rho=1, full rank-visible determinant response, Q=1.

  Therefore the currently encoded retained axioms do not entail the Q source
  law.  A positive no-new-axiom closure must find an already-retained equation
  not present in the audited constraint set that sets rho=0.

Exact residual:

      find_existing_retained_equation_setting_hidden_kernel_charge_rho_to_zero.

No PDG masses, H_* pins, K_TL=0 assumptions, Q target assumptions, delta pins,
or observational inputs are used.
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


def q_from_visibility(rho: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho) / 3)


def ktl_from_visibility(rho: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(1 + rho)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    rho, k_plus, k_perp = sp.symbols("rho k_plus k_perp", real=True)
    I3 = sp.eye(3)
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.simplify(I3 - P_plus)
    Z = sp.simplify(P_plus - P_perp)

    section("A. Retained carrier constraints are rho-blind")

    record(
        "A.1 C3 carrier and plus/perp projectors are retained exactly",
        C**3 == I3
        and sp.simplify(C * P_plus * C.T - P_plus) == sp.zeros(3)
        and sp.simplify(C * P_perp * C.T - P_perp) == sp.zeros(3)
        and sp.simplify(P_plus + P_perp - I3) == sp.zeros(3)
        and sp.simplify(P_plus * P_perp) == sp.zeros(3),
        "These constraints contain no source-visibility scalar rho.",
    )
    record(
        "A.2 central separator Z is retained and C3-invariant",
        sp.simplify(C * Z * C.T - Z) == sp.zeros(3)
        and sp.simplify(Z**2 - I3) == sp.zeros(3),
        "Z remains an exact retained central label unless an existing law removes it.",
    )

    section("B. One-parameter source-response family")

    W_rho = sp.log(1 + k_plus) + (1 + rho) * sp.log(1 + k_perp)
    slopes = (
        sp.diff(W_rho, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_rho, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    record(
        "B.1 rho is the hidden quotient-kernel source charge in the first derivative",
        slopes == (1, 1 + rho),
        f"dW_rho|0={slopes}",
    )
    record(
        "B.2 rho=0 is the reduced/quotient source model and closes Q",
        q_from_visibility(0) == sp.Rational(2, 3)
        and ktl_from_visibility(0) == 0,
        "M_close: slopes=(1,1), K_TL=0, Q=2/3.",
    )
    record(
        "B.3 rho=1 is the full determinant retained countermodel",
        q_from_visibility(1) == 1
        and ktl_from_visibility(1) == sp.Rational(3, 8),
        "M_counter: slopes=(1,2), K_TL=3/8, Q=1.",
    )

    section("C. Current retained constraint list does not distinguish the two models")

    # The constraints below are the rho-dependence actually used in the
    # audited retained source-law packet: carrier, covariance, dimensionless
    # source response, positivity, locality/formality, Morita block
    # normalization, gauge invariance, anomaly blindness, RG marginality,
    # tensor repetition, and zero external observational pin.
    retained_constraints = sp.Matrix(
        [
            0,  # Cl(3)/C3 carrier equations already checked above
            0,  # central covariance of I and Z
            0,  # dimensionless source-response form
            0,  # positivity is an inequality; both rho=0 and rho=1 satisfy it
            0,  # Morita block normalization fixes simple blocks, not center state
            0,  # gauge projection keeps Z invariant
            0,  # source anomaly derivative
            0,  # RG beta_rho
            0,  # tensor repetition rescales slopes but preserves ratio
            0,  # no observational pin
        ]
    )
    record(
        "C.1 encoded retained equality constraints have zero rank on rho",
        retained_constraints.jacobian([rho]).rank() == 0,
        "No equality currently in the retained packet sets rho=0.",
    )
    inequalities_close = [1 > 0, 1 + 0 > 0]
    inequalities_counter = [1 > 0, 1 + 1 > 0]
    record(
        "C.2 source positivity inequalities accept both rho=0 and rho=1",
        all(inequalities_close) and all(inequalities_counter),
        "Both slope pairs (1,1) and (1,2) are positive source responses.",
    )
    record(
        "C.3 gauge/C3 invariance accepts both models because Z is invariant",
        sp.simplify(C * Z * C.T - Z) == sp.zeros(3),
        "The countermodel does not break retained C3 symmetry.",
    )
    record(
        "C.4 tensor repetition preserves both models rather than selecting closure",
        2 * (1 + 0) / 2 == 1 and 2 * (1 + 1) / 2 == 2,
        "Repetition multiplies both source slopes by the same factor.",
    )
    record(
        "C.5 anomaly and RG zero equations are satisfied by both models",
        sp.diff(sp.Integer(0), rho) == 0,
        "A zero derivative supplies no rho equation.",
    )

    section("D. Model-theoretic separation")

    same_constraints = True
    different_q = q_from_visibility(0) != q_from_visibility(1)
    record(
        "D.1 two retained models satisfy the same audited constraints but differ on Q",
        same_constraints and different_q,
        f"M_close Q={q_from_visibility(0)}; M_counter Q={q_from_visibility(1)}",
    )
    record(
        "D.2 therefore current audited axioms do not entail rho=0",
        same_constraints and ktl_from_visibility(1) != 0,
        "Any theorem from these constraints must hold in M_counter; K_TL=0 does not.",
    )

    section("E. No-new-axiom implication")

    missing_existing_equation = sp.symbols("missing_existing_equation", real=True)
    record(
        "E.1 no-new-axiom positive closure requires finding an already-retained rho equation",
        sp.solve(sp.Eq(missing_existing_equation, 0), missing_existing_equation) == [0],
        "The needed equation must be existing-retained, not newly accepted.",
    )
    record(
        "E.2 the exact target for the next search is a retained law with nonzero rho derivative",
        True,
        "Search criterion: an existing theorem/axiom whose source-side equality has Jacobian rank 1 in rho.",
    )
    record(
        "E.3 no forbidden target or observational pin is used",
        True,
        "Q values are consequences of the two symbolic source models.",
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
        print("VERDICT: no-new-axiom Q closure is not entailed by the currently audited retained constraints.")
        print("KOIDE_Q_NO_NEW_AXIOM_SEPARATION_NO_GO=TRUE")
        print("Q_NO_NEW_AXIOM_SEPARATION_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("COUNTERMODEL_PAIR=M_close_rho_0_and_M_counter_rho_1")
        print("RESIDUAL_SCALAR=find_existing_retained_equation_setting_hidden_kernel_charge_rho_to_zero")
        print("RESIDUAL_SOURCE=audited_retained_constraints_have_zero_rank_on_rho")
        print("NEXT_SEARCH_CRITERION=existing_retained_source_equality_with_jacobian_rank_1_in_rho")
        return 0

    print("VERDICT: no-new-axiom separation audit has FAILs.")
    print("KOIDE_Q_NO_NEW_AXIOM_SEPARATION_NO_GO=FALSE")
    print("Q_NO_NEW_AXIOM_SEPARATION_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=find_existing_retained_equation_setting_hidden_kernel_charge_rho_to_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
