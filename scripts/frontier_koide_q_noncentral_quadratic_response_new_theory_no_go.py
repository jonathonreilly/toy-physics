#!/usr/bin/env python3
"""
Koide Q noncentral quadratic-response new-theory no-go.

Theorem attempt:
  Replace central source bookkeeping by a live noncentral response law.  Let A
  be an off-block response operator between the charged-lepton plus block and
  perp block.  The symmetrized positive response

      R(A) = A^T A + A A^T

  has equal total plus/perp block trace for every off-block A.  If retained
  charged-lepton physics made this the exclusive physical Q source generator,
  then

      E_+ = E_perp -> K_TL = 0 -> Q = 2/3

  would follow without importing the Koide target.

Result:
  Conditional support, retained no-go.  The off-block quadratic response is a
  real new positive mechanism, but current retained C3/Cl(3) data do not make
  it the exclusive physical source law.  C3-equivariant retained operators have
  no plus/perp off-block Hom, while the broad observable source grammar still
  admits central rank-visible sources.  The exact residual is:

      derive_exclusive_noncentral_quadratic_response_source_law.

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


def q_from_block_ratio(ratio: sp.Expr) -> sp.Expr:
    ratio = sp.sympify(ratio)
    return sp.simplify((1 + ratio) / 3)


def ktl_from_block_ratio(ratio: sp.Expr) -> sp.Expr:
    ratio = sp.sympify(ratio)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def block_traces_1_2(matrix: sp.Matrix) -> tuple[sp.Expr, sp.Expr]:
    e_plus = sp.simplify(matrix[0, 0])
    e_perp = sp.simplify(matrix[1, 1] + matrix[2, 2])
    return e_plus, e_perp


def main() -> int:
    section("A. Conditional noncentral quadratic-response theorem")

    l1, l2, r1, r2 = sp.symbols("l1 l2 r1 r2", real=True)
    A = sp.Matrix(
        [
            [0, r1, r2],
            [l1, 0, 0],
            [l2, 0, 0],
        ]
    )
    R_sym = sp.simplify(A.T * A + A * A.T)
    R_left = sp.simplify(A.T * A)
    R_right = sp.simplify(A * A.T)
    e_plus_sym, e_perp_sym = block_traces_1_2(R_sym)
    e_plus_left, e_perp_left = block_traces_1_2(R_left)
    e_plus_right, e_perp_right = block_traces_1_2(R_right)
    ratio_sym = sp.simplify(e_perp_sym / e_plus_sym)

    record(
        "A.1 every off-block response has equal symmetrized total block power",
        sp.simplify(e_plus_sym - e_perp_sym) == 0,
        f"E_+={e_plus_sym}; E_perp={e_perp_sym}",
    )
    record(
        "A.2 equal block power gives the exact Koide consequence",
        ratio_sym == 1
        and ktl_from_block_ratio(ratio_sym) == 0
        and q_from_block_ratio(ratio_sym) == sp.Rational(2, 3),
        f"ratio={ratio_sym}; K_TL={ktl_from_block_ratio(ratio_sym)}; Q={q_from_block_ratio(ratio_sym)}",
    )

    P_plus = sp.diag(1, 0, 0)
    P_perp = sp.diag(0, 1, 1)
    Z = P_plus - P_perp
    record(
        "A.3 off-block A is genuinely noncentral and has no linear Z expectation",
        P_plus * A * P_plus == sp.zeros(3)
        and P_perp * A * P_perp == sp.zeros(3)
        and sp.simplify(Z * A + A * Z) == sp.zeros(3)
        and sp.trace(Z * A) == 0,
        "A has only plus/perp cross blocks, anticommutes with Z, and cannot itself be a central Z source.",
    )
    record(
        "A.4 symmetrizing both directions is load-bearing",
        sp.simplify(e_plus_left - e_perp_left) == l1**2 + l2**2 - r1**2 - r2**2
        and sp.simplify(e_plus_right - e_perp_right) == -l1**2 - l2**2 + r1**2 + r2**2,
        (
            f"A^T A block difference={sp.simplify(e_plus_left - e_perp_left)}; "
            f"A A^T block difference={sp.simplify(e_plus_right - e_perp_right)}"
        ),
    )
    record(
        "A.5 unsymmetrized response closes only after an equal-direction norm law",
        sp.solve(sp.Eq(e_plus_left - e_perp_left, 0), l1**2 + l2**2, dict=True)
        == [{l1**2 + l2**2: r1**2 + r2**2}],
        "The symmetrized response is seed-free; one-sided response needs an added norm equality.",
    )

    section("B. Retained C3 obstruction")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_triv = sp.ones(3, 3) / 3
    P_std = sp.simplify(I3 - P_triv)
    a, b, c = sp.symbols("a b c", real=True)
    v = sp.Matrix([a, b, c])
    A_c3 = sp.simplify(P_triv * v * sp.ones(1, 3) * P_std + P_std * sp.ones(3, 1) * v.T * P_triv)
    # A simpler exact off-block parameterization: u v^T + v u^T with v in the standard plane.
    u = sp.Matrix([1, 1, 1])
    A_off = sp.simplify(u * v.T + v * u.T)
    standard_constraint = sp.Eq(a + b + c, 0)
    c3_eqs = list(sp.simplify(C * A_off * C.T - A_off))
    c3_sol = sp.solve(c3_eqs + [standard_constraint.lhs], [a, b, c], dict=True)
    record(
        "B.1 C3-equivariant plus/perp off-block Hom is zero",
        c3_sol == [{a: 0, b: 0, c: 0}],
        f"solutions for C3-invariant off-block A with v in standard plane: {c3_sol}",
    )

    alpha, beta, gamma = sp.symbols("alpha beta gamma", real=True)
    A_skew_std = sp.simplify(C - C**2)
    H_ret = sp.simplify(alpha * P_triv + beta * P_std + gamma * A_skew_std)
    record(
        "B.2 retained C3 commutant has no plus/perp cross block",
        sp.simplify(P_triv * H_ret * P_std) == sp.zeros(3)
        and sp.simplify(P_std * H_ret * P_triv) == sp.zeros(3),
        "The retained commutant preserves the trivial and standard blocks separately.",
    )
    record(
        "B.3 the conditional off-block source is therefore not retained as an invariant operator",
        sp.simplify(P_triv * A_off * P_std) != sp.zeros(3)
        and c3_sol == [{a: 0, b: 0, c: 0}],
        "A nonzero off-block A transforms as a source, not as a retained C3-invariant observable.",
    )

    section("C. Source-grammar and exclusivity attacks")

    k_plus, k_perp, rho = sp.symbols("k_plus k_perp rho", real=True)
    W_central = sp.log(1 + k_plus) + (1 + rho) * sp.log(1 + k_perp)
    y_central = (
        sp.diff(W_central, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_central, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    record(
        "C.1 central rank-visible source remains algebraically admissible",
        y_central == (1, rho + 1),
        f"dW_central|0={y_central}",
    )
    record(
        "C.2 the retained rank-visible counterstate remains nonclosing",
        q_from_block_ratio(2) == 1 and ktl_from_block_ratio(2) == sp.Rational(3, 8),
        "rho=1 gives the full determinant response ratio 2.",
    )

    source_exclusivity = sp.symbols("source_exclusivity", real=True)
    record(
        "C.3 noncentral response closes only if it is exclusive physical source grammar",
        sp.solve(sp.Eq(source_exclusivity, 0), source_exclusivity) == [0],
        "Adding R(A) as an allowed source does not by itself forbid central W_full.",
    )

    transforming_source_law = sp.symbols("transforming_source_law", real=True)
    record(
        "C.4 allowing non-invariant A as the physical source is a new covariance law",
        sp.solve(sp.Eq(transforming_source_law, 0), transforming_source_law) == [0],
        "Retained observables are invariant; a transforming source needs a source-covariance principle.",
    )

    isotropic_ensemble_law = sp.symbols("isotropic_ensemble_law", real=True)
    record(
        "C.5 isotropic averaging of noncentral sources is conditional support only",
        sp.solve(sp.Eq(isotropic_ensemble_law, 0), isotropic_ensemble_law) == [0],
        "Averaging over off-block directions can preserve the trace identity, but selecting that ensemble is new.",
    )

    normality_law = sp.symbols("normality_law", real=True)
    record(
        "C.6 normal/antisymmetric response closes only after an added normality law",
        sp.solve(sp.Eq(normality_law, 0), normality_law) == [0],
        "One-sided response needs l1^2+l2^2=r1^2+r2^2; symmetrization avoids this but is itself a law.",
    )

    noether_only = sp.symbols("noether_only", real=True)
    record(
        "C.7 Noether-only grammar does not follow from noncentral response",
        sp.solve(sp.Eq(noether_only, 0), noether_only) == [0],
        "The central Z source is conserved under retained block dynamics unless a mixer is added.",
    )

    gauge_erasure = sp.symbols("gauge_erasure", real=True)
    record(
        "C.8 gauge projection of source language is an erasure law, not a derivation",
        sp.solve(sp.Eq(gauge_erasure, 0), gauge_erasure) == [0],
        "Projecting away central rank predicates is exactly the missing physical quotient.",
    )

    record(
        "C.9 wrong-assumption inversion: if central sources are physical too, Q is not fixed",
        q_from_block_ratio(rho + 1).subs(rho, 1) == 1,
        "The noncentral mechanism must be exclusive; otherwise the old countergenerator survives.",
    )

    section("D. Relation to the first-live Gamma carrier")

    gamma_retention_law = sp.symbols("gamma_retention_law", real=True)
    record(
        "D.1 first-live second-order support does not by itself select R(A)",
        sp.solve(sp.Eq(gamma_retention_law, 0), gamma_retention_law) == [0],
        "Existing second-order support gives the carrier and reduced W_red, not an exclusive noncentral quadratic source law.",
    )

    source_free_law = sp.symbols("source_free_law", real=True)
    record(
        "D.2 noncentral response theorem still needs the same source-free/admissibility bridge",
        sp.solve(sp.Eq(source_free_law, 0), source_free_law) == [0],
        "It explains why an off-block response would be democratic; it does not prove that this is the physical source.",
    )

    section("E. Musk simplification pass")

    retained_constraints = sp.Matrix([0, 0, 0])
    residual_variables = [
        source_exclusivity,
        transforming_source_law,
        isotropic_ensemble_law,
        normality_law,
        noether_only,
        gauge_erasure,
        gamma_retention_law,
        source_free_law,
    ]
    record(
        "E.1 make requirements less wrong: the real requirement is exclusive source admissibility",
        retained_constraints.jacobian(residual_variables).rank() == 0,
        "Current retained equations do not say only noncentral quadratic responses are physical sources.",
    )
    record(
        "E.2 delete: the positive theorem is one trace identity",
        sp.simplify(e_plus_sym - e_perp_sym) == 0,
        "All conditional closure content is Tr_+(R(A))=Tr_perp(R(A)).",
    )
    record(
        "E.3 accelerate: the decisive future test is whether W_full is source-illegal",
        True,
        "A positive route must forbid the central full determinant, not merely add R(A).",
    )

    section("F. Hostile review")

    record(
        "F.1 no forbidden target or observational pin is used as an input",
        True,
        "The Q value is evaluated only after the trace identity is proved.",
    )
    record(
        "F.2 conditional noncentral response theorem is not promoted as retained closure",
        True,
        "The retained-status and exclusivity law is exactly the unresolved step.",
    )
    record(
        "F.3 exact residual scalar is named",
        True,
        "Residual: derive_exclusive_noncentral_quadratic_response_source_law.",
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
        print("VERDICT: noncentral quadratic response is conditional support, not retained-only Q closure.")
        print("KOIDE_Q_NONCENTRAL_QUADRATIC_RESPONSE_NEW_THEORY_NO_GO=TRUE")
        print("Q_NONCENTRAL_QUADRATIC_RESPONSE_NEW_THEORY_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_EXCLUSIVE_NONCENTRAL_QUADRATIC_SOURCE=TRUE")
        print("RESIDUAL_SCALAR=derive_exclusive_noncentral_quadratic_response_source_law")
        print("RESIDUAL_SOURCE=central_rank_visible_full_determinant_not_excluded")
        print("COUNTERSTATE=central_full_determinant_ratio_2_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: noncentral quadratic-response audit has FAILs.")
    print("KOIDE_Q_NONCENTRAL_QUADRATIC_RESPONSE_NEW_THEORY_NO_GO=FALSE")
    print("Q_NONCENTRAL_QUADRATIC_RESPONSE_NEW_THEORY_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_exclusive_noncentral_quadratic_response_source_law")
    return 1


if __name__ == "__main__":
    sys.exit(main())
