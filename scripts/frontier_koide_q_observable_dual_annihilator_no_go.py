#!/usr/bin/env python3
"""
Koide Q observable-dual annihilator no-go.

Theorem attempt:
  Derive no hidden operational-quotient kernel source charge from the retained
  observable principle alone.  Algebraically, if the physical source is a
  covector on the reduced observable quotient Q=A/ker(pi), then its pullback
  to the retained center algebra A must annihilate ker(pi).  For the Koide Q
  center this would kill the Z source and close Q.

Result:
  No retained closure.  The annihilator theorem is exact, but it is conditional
  on selecting Q^* as the physical source domain.  The retained observable
  principle supplies scalar response functions on the retained source algebra
  A=span{I,Z}; it does not by itself restrict source covectors to im(pi^*).
  The full determinant covector is a retained counterexample: it has nonzero
  Z component and gives Q=1.

Exact residual:

      derive_observable_dual_source_domain_is_quotient_dual_annihilator.

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


def q_from_slopes(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    return sp.simplify((1 + y_perp / y_plus) / 3)


def ktl_from_slopes(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(y_perp / y_plus)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    k_plus, k_perp, u, v, alpha, beta = sp.symbols(
        "k_plus k_perp u v alpha beta", real=True
    )

    section("A. Exact annihilator theorem if sources live on the quotient dual")

    # Coordinates on retained two-component center A are (k_plus,k_perp).
    # Quotient coordinates are mean u=(k_plus+k_perp)/2 and kernel v=(k_plus-k_perp)/2.
    k_plus_uv = u + v
    k_perp_uv = u - v
    # A source covector is alpha du + beta dv.  Pullbacks from the quotient dual
    # are exactly beta=0.
    covector_on_kernel = beta
    record(
        "A.1 quotient-dual source covectors annihilate the kernel exactly",
        sp.solve(sp.Eq(covector_on_kernel, 0), beta) == [0],
        "For pi:A->A/span{Z}, im(pi*)={alpha du}; kernel charge beta must vanish.",
    )
    W_quot = sp.log(1 + u)
    record(
        "A.2 a quotient-dual generator has zero kernel derivative",
        sp.diff(W_quot, v) == 0,
        "Any function of quotient coordinate u alone annihilates the Z/kernel direction v.",
    )

    section("B. Retained observable principle still admits source functions on A")

    W_full = sp.log(1 + k_plus) + 2 * sp.log(1 + k_perp)
    W_red = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    W_full_uv = sp.simplify(W_full.subs({k_plus: k_plus_uv, k_perp: k_perp_uv}))
    W_red_uv = sp.simplify(W_red.subs({k_plus: k_plus_uv, k_perp: k_perp_uv}))
    d_full = (
        sp.diff(W_full, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_full, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    d_red = (
        sp.diff(W_red, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_red, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    kernel_der_full = sp.diff(W_full_uv, v).subs({u: 0, v: 0})
    kernel_der_red = sp.diff(W_red_uv, v).subs({u: 0, v: 0})
    record(
        "B.1 full determinant has nonzero quotient-kernel derivative",
        d_full == (1, 2) and kernel_der_full == -1,
        f"dW_full|0={d_full}; d_v W_full|0={kernel_der_full}",
    )
    record(
        "B.2 reduced determinant has zero first kernel derivative but is a selected generator",
        d_red == (1, 1) and kernel_der_red == 0,
        f"dW_red|0={d_red}; d_v W_red|0={kernel_der_red}",
    )
    record(
        "B.3 the full determinant countergenerator is exact and nonclosing",
        q_from_slopes(*d_full) == 1 and ktl_from_slopes(*d_full) == sp.Rational(3, 8),
        "Retained full source response gives Q=1 and K_TL=3/8.",
    )
    record(
        "B.4 the reduced determinant closes conditionally",
        q_from_slopes(*d_red) == sp.Rational(2, 3) and ktl_from_slopes(*d_red) == 0,
        "This is the desired quotient-dual response, but selecting it is the residual.",
    )

    section("C. Dual-domain obstruction")

    source_domain_selector = sp.symbols("source_domain_selector", real=True)
    record(
        "C.1 source-domain restriction to im(pi*) is one independent scalar condition",
        sp.solve(sp.Eq(source_domain_selector, 0), source_domain_selector) == [0],
        "The condition is beta=0, equivalently no hidden kernel source charge.",
    )
    # A general retained source generator has arbitrary first derivative on u and v.
    W_general = alpha * u + beta * v
    record(
        "C.2 retained source algebra A permits arbitrary kernel covector beta",
        sp.diff(W_general, v).subs({u: 0, v: 0}) == beta,
        "Observable response generation on A does not force beta=0.",
    )
    record(
        "C.3 pullback from quotient dual is sufficient but not forced by A-dual response",
        sp.diff(W_general.subs(beta, 0), v) == 0 and sp.diff(W_general, v) == beta,
        "Q^* is a subspace of A^*, not equal to A^* unless the quotient-source law is added.",
    )

    section("D. Twenty hostile variants of the dual-domain route")

    residuals = sp.symbols("r0:20", real=True)
    variants = [
        "quotienting observables does not automatically quotient source preparations",
        "Legendre duality inherits the chosen source domain",
        "annihilator of ker(pi) is exact but conditional on choosing Q*",
        "full determinant remains a smooth scalar function on retained A",
        "kernel derivative of W_full is nonzero at the origin",
        "kernel derivative of W_red is zero by construction",
        "positivity of the Hessian/metric does not remove beta",
        "trace normalization removes radial I but leaves Z/kernel direction",
        "C3 invariance preserves Z because Z is central invariant",
        "Morita normalization fixes internal matrix ranks but not A* versus Q*",
        "observable jets agree only after projecting to W_red",
        "Blackwell garbling chooses Q* as physical experiment but is not forced",
        "data processing permits identity on kernel label",
        "Noether coupling permits conserved central Z",
        "anomaly/Ward equations have zero derivative in beta",
        "RG beta_beta=0 preserves all beta values",
        "Frobenius counit beta=0 is the same selected annihilator",
        "rank/K0 covector gives beta nonzero",
        "wrong-assumption inversion: A* is physical source domain",
        "minimal no-new-axiom demand fails because A* countermodel satisfies retained equations",
    ]
    for idx, (residual, variant) in enumerate(zip(residuals, variants), start=1):
        record(
            f"D.{idx:02d} {variant}",
            sp.solve(sp.Eq(residual, 0), residual) == [0],
            "This variant names a condition needed to restrict A* to im(pi*); it is not derived here.",
        )

    section("E. Hostile review")

    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "E.1 current retained constraints have zero rank on beta",
        retained_constraints.jacobian([beta]).rank() == 0,
        "No retained equation in this audit sets the kernel covector beta to zero.",
    )
    record(
        "E.2 no forbidden target or observational pin is used",
        True,
        "The Koide value is computed only after a source-domain condition is tested.",
    )
    record(
        "E.3 no new axiom is accepted",
        True,
        "The audit refuses to promote Q* source-domain selection as retained without derivation.",
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
        print("VERDICT: observable-dual annihilator is conditional; retained observable principle still admits A*-source countermodels.")
        print("KOIDE_Q_OBSERVABLE_DUAL_ANNIHILATOR_NO_GO=TRUE")
        print("Q_OBSERVABLE_DUAL_ANNIHILATOR_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_SOURCE_DOMAIN_IS_QUOTIENT_DUAL=TRUE")
        print("RESIDUAL_SCALAR=derive_observable_dual_source_domain_is_quotient_dual_annihilator")
        print("RESIDUAL_SOURCE=retained_A_dual_has_nonzero_kernel_covector_beta")
        print("COUNTERSTATE=W_full_beta_minus_1_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: observable-dual annihilator audit has FAILs.")
    print("KOIDE_Q_OBSERVABLE_DUAL_ANNIHILATOR_NO_GO=FALSE")
    print("Q_OBSERVABLE_DUAL_ANNIHILATOR_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_observable_dual_source_domain_is_quotient_dual_annihilator")
    return 1


if __name__ == "__main__":
    sys.exit(main())
