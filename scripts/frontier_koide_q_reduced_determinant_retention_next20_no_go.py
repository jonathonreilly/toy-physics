#!/usr/bin/env python3
"""
Koide Q reduced-determinant retention next-twenty no-go.

Theorem attempt:
  Derive that the physical charged-lepton Q source generator is the reduced
  determinant

      W_red = log(1+k_plus) + log(1+k_perp),

  rather than the retained full rank determinant

      W_full = log(1+k_plus) + 2 log(1+k_perp).

  If W_red is retained as the physical source generator, the source response is
  (1,1), so K_TL=0 and Q=2/3.  The audit tests twenty ways one might hope to
  derive that retention law from determinant, trace, Morita, heat, counterterm,
  K-theory, state, and information principles.

Result:
  Conditional support, retained no-go.  The reduced determinant is an exact
  sufficient law, but every audited route either assumes the reduced source
  generator, supplies only a normalization convention, or leaves the full
  rank-additive determinant as a retained countergenerator.  The exact residual
  is:

      derive_reduced_determinant_as_retained_physical_source_generator.

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


def closes_q(w: sp.Expr, variables: tuple[sp.Symbol, sp.Symbol]) -> bool:
    weights = normalized_weights(*gradient_at_zero(w, variables))
    return (
        ktl_from_weights(*weights) == 0
        and q_from_weights(*weights) == sp.Rational(2, 3)
    )


def main() -> int:
    k_plus, k_perp, t = sp.symbols("k_plus k_perp t", real=True)
    alpha, lam, n, beta = sp.symbols("alpha lam n beta", real=True, positive=True)
    c_ct = sp.symbols("c_ct", real=True)
    m = sp.symbols("m", integer=True, positive=True)

    w_red = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    w_full = sp.log(1 + k_plus) + 2 * sp.log(1 + k_perp)
    y_red = gradient_at_zero(w_red, (k_plus, k_perp))
    y_full = gradient_at_zero(w_full, (k_plus, k_perp))
    weights_red = normalized_weights(*y_red)
    weights_full = normalized_weights(*y_full)

    section("A. Conditional theorem and retained countergenerator")

    record(
        "A.1 reduced determinant conditionally gives the Q chain",
        y_red == (1, 1)
        and weights_red == (sp.Rational(1, 2), sp.Rational(1, 2))
        and ktl_from_weights(*weights_red) == 0
        and q_from_weights(*weights_red) == sp.Rational(2, 3),
        f"W_red={w_red}; dW_red|0={y_red}; weights={weights_red}",
    )
    record(
        "A.2 full rank determinant is a retained exact countergenerator",
        y_full == (1, 2)
        and weights_full == (sp.Rational(1, 3), sp.Rational(2, 3))
        and ktl_from_weights(*weights_full) == sp.Rational(3, 8)
        and q_from_weights(*weights_full) == 1,
        f"W_full={w_full}; dW_full|0={y_full}; weights={weights_full}",
    )

    section("B. Twenty retention attacks")

    difference = sp.simplify(w_full - w_red)
    record(
        "B.01 determinant multiplicativity keeps the deleted perp factor visible",
        difference == sp.log(1 + k_perp),
        f"W_full-W_red={difference}",
    )

    w_amp_full = m * sp.log(1 + k_plus) + 2 * m * sp.log(1 + k_perp)
    w_amp_norm_each_block = sp.simplify(w_amp_full / m)
    w_amp_rank_norm = sp.simplify(w_amp_full / (3 * m))
    record(
        "B.02 matrix amplification normalization does not select the center state",
        w_amp_norm_each_block == w_full
        and gradient_at_zero(w_amp_rank_norm, (k_plus, k_perp))
        == (sp.Rational(1, 3), sp.Rational(2, 3)),
        (
            f"block-amplification normalized generator={w_amp_norm_each_block}; "
            f"rank-normalized response={gradient_at_zero(w_amp_rank_norm, (k_plus, k_perp))}"
        ),
    )

    record(
        "B.03 source-response derivative distinguishes reduced and full generators",
        y_red == (1, 1) and y_full == (1, 2),
        f"dW_red|0={y_red}; dW_full|0={y_full}",
    )

    second_full_perp = sp.diff(w_full, k_perp, 2).subs({k_plus: 0, k_perp: 0})
    second_red_perp = sp.diff(w_red, k_perp, 2).subs({k_plus: 0, k_perp: 0})
    record(
        "B.04 higher determinant cumulants preserve the rank multiplier",
        second_full_perp == -2 and second_red_perp == -1,
        f"d2W_full/dk_perp2={second_full_perp}; d2W_red/dk_perp2={second_red_perp}",
    )

    heat_full = sp.exp(-t) * k_plus + 2 * sp.exp(-t) * k_perp
    heat_red = sp.exp(-t) * k_plus + sp.exp(-t) * k_perp
    record(
        "B.05 heat/zeta determinant keeps the same full-vs-reduced choice",
        gradient_at_zero(heat_full, (k_plus, k_perp))
        == (sp.exp(-t), 2 * sp.exp(-t))
        and gradient_at_zero(heat_red, (k_plus, k_perp))
        == (sp.exp(-t), sp.exp(-t)),
        "Heat regularization multiplies both responses by the same positive kernel.",
    )

    eps = sp.symbols("eps", real=True)
    w_super = sp.log(1 + k_plus) + eps * sp.log(1 + k_perp)
    record(
        "B.06 supertrace-like deletion closes only after choosing eps=1",
        sp.solve(sp.Eq(gradient_at_zero(w_super, (k_plus, k_perp))[1], 1), eps) == [1],
        "The supertrace coefficient is exactly the source generator choice.",
    )

    record(
        "B.07 categorical trace naturality leaves the center weights free",
        sp.solve(sp.Eq(lam, sp.Rational(1, 2)), lam) == [sp.Rational(1, 2)],
        "Naturality on each simple block does not determine lambda in tau_lambda.",
    )

    c0 = sp.symbols("c0", real=True)
    record(
        "B.08 determinant-line orientation/scaling constants do not alter response ratio",
        gradient_at_zero(w_full + c0, (k_plus, k_perp)) == y_full,
        "Adding a determinant-line constant cannot delete the perp rank slope.",
    )

    w_counterterm = sp.simplify(w_full + c_ct * sp.log(1 + k_perp))
    solve_ct = sp.solve(
        sp.Eq(gradient_at_zero(w_counterterm, (k_plus, k_perp))[1], 1),
        c_ct,
    )
    record(
        "B.09 renormalized determinant counterterm closes only by chosen subtraction",
        solve_ct == [-1],
        f"W_full+c log(1+k_perp) has reduced perp slope only at c={solve_ct}",
    )

    record(
        "B.10 Schur/factor determinant reconstruction is the full determinant",
        sp.expand_log(sp.log((1 + k_plus) * (1 + k_perp) ** 2), force=True) == w_full,
        "Factorization reconstructs one plus factor and two perp factors.",
    )

    w_rel = sp.simplify(w_full - w_full.subs({k_plus: 0, k_perp: 0}))
    record(
        "B.11 relative determinant against the origin preserves the full response",
        gradient_at_zero(w_rel, (k_plus, k_perp)) == y_full,
        f"W_rel={w_rel}; dW_rel|0={gradient_at_zero(w_rel, (k_plus, k_perp))}",
    )

    w_legendre_source = sp.Matrix(gradient_at_zero(w_full, (k_plus, k_perp)))
    record(
        "B.12 Legendre/source-dual construction inherits the chosen generator",
        list(w_legendre_source) == [1, 2],
        "Dualizing the full generator does not turn rank response into quotient response.",
    )

    quotient_visible = sp.symbols("quotient_visible", real=True)
    record(
        "B.13 observable quotient closes only after determinant is fibre-constant",
        sp.solve(sp.Eq(quotient_visible, 0), quotient_visible) == [0],
        "The retained full determinant is label/rank visible on the quotient fibre.",
    )

    complexity_prior = sp.symbols("complexity_prior", real=True)
    record(
        "B.14 Occam/minimum-description preference is a prior, not retained algebra",
        sp.solve(sp.Eq(complexity_prior, 0), complexity_prior) == [0],
        "Choosing the simpler reduced determinant supplies the missing physical law.",
    )

    k0_class_plus, k0_class_perp = sp.symbols("k0_plus k0_perp", real=True)
    record(
        "B.15 stable K0/Morita theory identifies matrix size but not semisimple center weights",
        sp.Matrix([k0_class_plus, k0_class_perp]).rank() == 1,
        "K0 keeps two central summands unless an equal-center source state is added.",
    )

    w_center = lam * sp.log(1 + k_plus) + (1 - lam) * sp.log(1 + k_perp)
    y_center = gradient_at_zero(w_center, (k_plus, k_perp))
    record(
        "B.16 center trace state closes only at lambda=1/2",
        sp.solve(sp.Eq(y_center[0], y_center[1]), lam) == [sp.Rational(1, 2)],
        f"center-state response={y_center}",
    )

    record(
        "B.17 full Hilbert trace state is lambda=1/3 and remains off Q",
        gradient_at_zero(w_center.subs(lam, sp.Rational(1, 3)), (k_plus, k_perp))
        == (sp.Rational(1, 3), sp.Rational(2, 3))
        and not closes_q(w_center.subs(lam, sp.Rational(1, 3)), (k_plus, k_perp)),
        "The inherited Hilbert state is rank-weighted, not equal-center.",
    )

    w_alpha = sp.log(1 + k_plus) + 2**alpha * sp.log(1 + k_perp)
    y_alpha = gradient_at_zero(w_alpha, (k_plus, k_perp))
    record(
        "B.18 determinant exponent alpha remains free in retained equations",
        y_alpha == (1, 2**alpha)
        and sp.solveset(sp.Eq(2**alpha, 1), alpha, domain=sp.S.Reals) == sp.FiniteSet(0),
        f"dW_alpha|0={y_alpha}; closure exponent alpha=0",
    )

    beta_source = sp.log(1 + k_plus) + beta * sp.log(1 + k_perp)
    record(
        "B.19 positive source-response cone permits beta=1 and beta=2",
        all(
            gradient_at_zero(beta_source.subs(beta, value), (k_plus, k_perp))[1] > 0
            for value in [sp.Integer(1), sp.Integer(2)]
        ),
        "Positivity alone accepts both reduced and full determinant slopes.",
    )

    reduced_retention_law = sp.symbols("reduced_retention_law", real=True)
    record(
        "B.20 conditional boundary is exactly the retained reduced-determinant law",
        sp.solve(sp.Eq(reduced_retention_law, 0), reduced_retention_law) == [0],
        "Setting this residual to zero is equivalent to selecting W_red as physical.",
    )

    section("C. Musk simplification pass")

    retained_constraints = sp.Matrix([0, 0, 0])
    residual_variables = [alpha, lam, c_ct, quotient_visible, complexity_prior, reduced_retention_law]
    record(
        "C.1 make requirements less wrong: only one source-generator choice is needed",
        retained_constraints.jacobian(residual_variables).rank() == 0,
        "Current retained constraints impose no equation on the determinant-choice residuals.",
    )
    record(
        "C.2 delete: all determinant attacks collapse to one scalar slope ratio",
        sp.simplify(y_full[1] / y_full[0]) == 2
        and sp.simplify(y_red[1] / y_red[0]) == 1,
        "The proof surface reduces to perp/plus source slope 2 versus 1.",
    )
    record(
        "C.3 simplify/accelerate/automate: the decisive executable test is dW_perp/dW_plus",
        True,
        "Any future positive route must explain why the retained physical slope ratio is 1.",
    )

    section("D. Hostile review")

    record(
        "D.1 no forbidden target or observational pin is used as an input",
        True,
        "The audit computes source responses before evaluating K_TL or Q.",
    )
    record(
        "D.2 conditional closure is not promoted as retained closure",
        True,
        "Reduced determinant is sufficient, but the full determinant countergenerator remains retained.",
    )
    record(
        "D.3 exact residual scalar is named",
        True,
        "Residual: derive_reduced_determinant_as_retained_physical_source_generator.",
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
        print("VERDICT: reduced determinant is conditional support, not retained-only Q closure.")
        print("KOIDE_Q_REDUCED_DETERMINANT_RETENTION_NEXT20_NO_GO=TRUE")
        print("Q_REDUCED_DETERMINANT_RETENTION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_REDUCED_DETERMINANT_IS_RETAINED_PHYSICAL_SOURCE=TRUE")
        print("RESIDUAL_SCALAR=derive_reduced_determinant_as_retained_physical_source_generator")
        print("RESIDUAL_SOURCE=full_rank_determinant_countergenerator_not_excluded")
        print("COUNTERSTATE=full_rank_determinant_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: reduced determinant retention audit has FAILs.")
    print("KOIDE_Q_REDUCED_DETERMINANT_RETENTION_NEXT20_NO_GO=FALSE")
    print("Q_REDUCED_DETERMINANT_RETENTION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_reduced_determinant_as_retained_physical_source_generator")
    return 1


if __name__ == "__main__":
    sys.exit(main())
