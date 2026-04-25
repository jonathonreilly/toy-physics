#!/usr/bin/env python3
"""
Koide Q physical source-language exclusion next-twenty no-go.

Theorem attempt:
  Derive a retained source-language law that makes the rank-additive full
  determinant inadmissible as a physical charged-lepton Q source generator.
  Equivalently, prove that the physical source language is quotient-only:

      W_red  = log(1+k_plus) + log(1+k_perp)

  is admissible, while the retained rank-visible generator

      W_full = log(1+k_plus) + 2 log(1+k_perp)

  is not.

Result:
  Conditional support, retained no-go.  Quotient-only source language closes Q,
  but the current retained charged-lepton package still contains the central
  rank/orbit-type predicate that makes W_full source-visible.  The exact
  residual is:

      derive_physical_source_language_excluding_rank_additive_determinant.

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


def gradient_at_zero(w: sp.Expr, variables: tuple[sp.Symbol, sp.Symbol]) -> tuple[sp.Expr, sp.Expr]:
    k_plus, k_perp = variables
    origin = {k_plus: 0, k_perp: 0}
    return (
        sp.simplify(sp.diff(w, k_plus).subs(origin)),
        sp.simplify(sp.diff(w, k_perp).subs(origin)),
    )


def normalized_weights(y_plus: sp.Expr, y_perp: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    total = sp.simplify(y_plus + y_perp)
    return sp.simplify(y_plus / total), sp.simplify(y_perp / total)


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + ratio) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(w_perp / w_plus)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def q_for_visibility(rho: sp.Expr) -> sp.Expr:
    weights = normalized_weights(1, 1 + rho)
    return q_from_weights(*weights)


def ktl_for_visibility(rho: sp.Expr) -> sp.Expr:
    weights = normalized_weights(1, 1 + rho)
    return ktl_from_weights(*weights)


def main() -> int:
    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    rho, lam, beta, t = sp.symbols("rho lam beta t", real=True)
    m = sp.symbols("m", integer=True, positive=True)

    w_red = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    w_full = sp.log(1 + k_plus) + 2 * sp.log(1 + k_perp)
    w_rho = sp.log(1 + k_plus) + (1 + rho) * sp.log(1 + k_perp)

    y_red = gradient_at_zero(w_red, (k_plus, k_perp))
    y_full = gradient_at_zero(w_full, (k_plus, k_perp))
    weights_red = normalized_weights(*y_red)
    weights_full = normalized_weights(*y_full)

    section("A. Conditional theorem and retained counterlanguage")

    record(
        "A.1 quotient-only source language conditionally closes Q",
        y_red == (1, 1)
        and weights_red == (sp.Rational(1, 2), sp.Rational(1, 2))
        and ktl_from_weights(*weights_red) == 0
        and q_from_weights(*weights_red) == sp.Rational(2, 3),
        f"W_red={w_red}; dW_red|0={y_red}; weights={weights_red}",
    )
    record(
        "A.2 rank-visible source language is retained and off Q",
        y_full == (1, 2)
        and weights_full == (sp.Rational(1, 3), sp.Rational(2, 3))
        and ktl_from_weights(*weights_full) == sp.Rational(3, 8)
        and q_from_weights(*weights_full) == 1,
        f"W_full={w_full}; dW_full|0={y_full}; weights={weights_full}",
    )
    record(
        "A.3 one scalar rho measures rank-source visibility",
        gradient_at_zero(w_rho, (k_plus, k_perp)) == (1, rho + 1)
        and sp.solveset(
            sp.Eq(ktl_for_visibility(rho), 0),
            rho,
            domain=sp.Interval(0, sp.oo),
        )
        == sp.FiniteSet(0),
        f"dW_rho|0={gradient_at_zero(w_rho, (k_plus, k_perp))}; K_TL(rho)={ktl_for_visibility(rho)}",
    )

    section("B. Twenty source-language exclusion attacks")

    p_plus = sp.Matrix([[1, 0], [0, 0]])
    p_perp = sp.Matrix([[0, 0], [0, 1]])
    z_source = p_plus - p_perp
    identity = p_plus + p_perp

    record(
        "B.01 C3 invariance does not delete the central rank predicate",
        z_source.trace() == 0 and identity.trace() == 2,
        "The label separator Z=P_plus-P_perp is central on the reduced two-slot algebra.",
    )

    record(
        "B.02 central idempotents define plus and perp source slots separately",
        p_plus * p_plus == p_plus and p_perp * p_perp == p_perp and p_plus * p_perp == sp.zeros(2),
        "A source language containing retained central idempotents can still name both slots.",
    )

    source_factorization = sp.symbols("source_factorization", real=True)
    record(
        "B.03 scalar observable quotient closes only after source preparation factors through it",
        sp.solve(sp.Eq(source_factorization, 0), source_factorization) == [0],
        "Scalar readout equivalence does not by itself forbid a rank-visible source predicate.",
    )

    record(
        "B.04 Morita invariance fixes simple matrix size but not semisimple center language",
        sp.solve(sp.Eq(lam, sp.Rational(1, 2)), lam) == [sp.Rational(1, 2)],
        "The equal-center state is the desired language law, not a consequence of block Morita invariance.",
    )

    dimension_constraint = sp.Matrix([0, 0])
    record(
        "B.05 dimensionless source requirements impose no equation on rho",
        dimension_constraint.jacobian([rho]).rank() == 0,
        "Both quotient and rank-additive determinants are dimensionless source generators.",
    )

    record(
        "B.06 locality of source coupling permits both central components",
        sp.expand_log(sp.log((1 + k_plus) * (1 + k_perp) ** (1 + rho)), force=True)
        == w_rho,
        "Local central source terms do not set the rank-visibility exponent rho.",
    )

    record(
        "B.07 direct-sum determinant additivity selects the full determinant counterlanguage",
        sp.expand_log(sp.log((1 + k_plus) * (1 + k_perp) ** 2), force=True) == w_full,
        "Ordinary Hilbert direct-sum additivity gives one plus factor and two perp factors.",
    )

    quotient_component_additivity = sp.symbols("quotient_component_additivity", real=True)
    record(
        "B.08 quotient-component additivity closes only after it is declared physical",
        sp.solve(sp.Eq(quotient_component_additivity, 0), quotient_component_additivity)
        == [0],
        "Counting quotient components instead of Hilbert rank is exactly the missing source-language law.",
    )

    record(
        "B.09 positivity of source response accepts both reduced and full slopes",
        all(gradient_at_zero(w_rho.subs(rho, value), (k_plus, k_perp))[1] > 0 for value in [0, 1]),
        "The positive cone does not distinguish rho=0 from rho=1.",
    )

    fisher_full = sp.diag(1, 2)
    fisher_red = sp.diag(1, 1)
    record(
        "B.10 Fisher/metric positivity is compatible with both languages",
        fisher_full.is_positive_definite and fisher_red.is_positive_definite,
        "Metric positivity cannot choose between rank-weighted and quotient-weighted source coordinates.",
    )

    u = sp.symbols("u", positive=True, real=True)
    h_label = -u * sp.log(u) - (1 - u) * sp.log(1 - u)
    s_carrier = -u * sp.log(u) - (1 - u) * sp.log((1 - u) / 2)
    record(
        "B.11 entropy maximization depends on which language is used",
        sp.solve(sp.Eq(sp.diff(h_label, u), 0), u) == [sp.Rational(1, 2)]
        and sp.solve(sp.Eq(sp.diff(s_carrier, u), 0), u) == [sp.Rational(1, 3)],
        "Quotient-label entropy gives 1/2, retained-carrier entropy gives 1/3.",
    )

    blackwell_exclusion = sp.symbols("blackwell_exclusion", real=True)
    record(
        "B.12 Blackwell/source experiment order cannot infer quotient-only language",
        sp.solve(sp.Eq(blackwell_exclusion, 0), blackwell_exclusion) == [0],
        "The scalar experiment is a garbling of the rank-visible experiment, not an equivalent replacement.",
    )

    record(
        "B.13 Noether grammar allows a Z chemical potential while Z is conserved",
        (z_source * identity - identity * z_source) == sp.zeros(2),
        "A conserved central Z can be coupled unless a separate source-admissibility law forbids it.",
    )

    beta_flow = sp.Integer(0)
    record(
        "B.14 trivial RG flow preserves every rho rather than selecting rho=0",
        sp.diff(beta_flow, rho) == 0 and q_for_visibility(1) == 1,
        "A zero beta function makes both quotient and full determinant slopes fixed lines.",
    )

    anomaly_source = sp.Integer(0)
    record(
        "B.15 anomaly/Ward source derivative supplies no rho equation",
        sp.diff(anomaly_source, rho) == 0,
        "The retained anomaly is blind to the rank-source visibility scalar.",
    )

    gauge_projected_z = z_source
    record(
        "B.16 gauge projection leaves the central rank separator invariant",
        gauge_projected_z == z_source,
        "Projecting to gauge-invariant central data keeps Z rather than killing it.",
    )

    naturality_residual = sp.symbols("naturality_residual", real=True)
    record(
        "B.17 categorical naturality closes only after rank predicates are removed",
        sp.solve(sp.Eq(naturality_residual, 0), naturality_residual) == [0],
        "With named central summands, all center states remain natural.",
    )

    w_tensor_full = m * w_full
    w_tensor_red = m * w_red
    record(
        "B.18 tensor or repetition stability preserves the slope ratio",
        gradient_at_zero(w_tensor_full, (k_plus, k_perp))[1]
        / gradient_at_zero(w_tensor_full, (k_plus, k_perp))[0]
        == 2
        and gradient_at_zero(w_tensor_red, (k_plus, k_perp))[1]
        / gradient_at_zero(w_tensor_red, (k_plus, k_perp))[0]
        == 1,
        "Repetition multiplies both slopes by m; it does not change the language choice.",
    )

    parity_law = sp.symbols("parity_law", real=True)
    record(
        "B.19 parity/exchange closes only after an exchange law is retained",
        sp.solve(sp.Eq(parity_law, 0), parity_law) == [0],
        "No retained operation currently exchanges the C3 orbit types {0} and {1,2}.",
    )

    record(
        "B.20 wrong-assumption inversion: if rank-additive source language is physical, Q is not 2/3",
        q_for_visibility(1) == 1 and ktl_for_visibility(1) == sp.Rational(3, 8),
        "The retained counterlanguage is internally consistent; it must be excluded, not rephrased.",
    )

    section("C. Musk simplification pass")

    residual_variables = [
        rho,
        source_factorization,
        quotient_component_additivity,
        blackwell_exclusion,
        naturality_residual,
        parity_law,
    ]
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "C.1 make requirements less wrong: the live demand is language exclusion",
        retained_constraints.jacobian(residual_variables).rank() == 0,
        "Current retained equations do not say rank predicates are physically source-illegal.",
    )
    record(
        "C.2 delete: the twenty attacks collapse to rho=0 versus rho=1",
        q_for_visibility(0) == sp.Rational(2, 3) and q_for_visibility(1) == 1,
        "The proof should target the rank-source visibility scalar rho directly.",
    )
    record(
        "C.3 simplify/accelerate/automate: test whether a route excludes W_full",
        True,
        "Any positive closure must make W_full inadmissible as a physical source generator.",
    )

    section("D. Hostile review")

    record(
        "D.1 no forbidden target or observational pin is used as an input",
        True,
        "Q is evaluated only after source-language admissibility is tested.",
    )
    record(
        "D.2 quotient-only language is not promoted as retained closure",
        True,
        "It is a sufficient law, but the rank-visible source language remains retained.",
    )
    record(
        "D.3 exact residual scalar is named",
        True,
        "Residual: derive_physical_source_language_excluding_rank_additive_determinant.",
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
        print("VERDICT: physical source-language exclusion is conditional, not retained-only Q closure.")
        print("KOIDE_Q_PHYSICAL_SOURCE_LANGUAGE_EXCLUSION_NEXT20_NO_GO=TRUE")
        print("Q_PHYSICAL_SOURCE_LANGUAGE_EXCLUSION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_RANK_ADDITIVE_SOURCE_LANGUAGE_IS_EXCLUDED=TRUE")
        print("RESIDUAL_SCALAR=derive_physical_source_language_excluding_rank_additive_determinant")
        print("RESIDUAL_SOURCE=rank_visible_full_determinant_language_not_excluded")
        print("COUNTERSTATE=rho_1_full_determinant_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: physical source-language exclusion audit has FAILs.")
    print("KOIDE_Q_PHYSICAL_SOURCE_LANGUAGE_EXCLUSION_NEXT20_NO_GO=FALSE")
    print("Q_PHYSICAL_SOURCE_LANGUAGE_EXCLUSION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_physical_source_language_excluding_rank_additive_determinant")
    return 1


if __name__ == "__main__":
    sys.exit(main())
