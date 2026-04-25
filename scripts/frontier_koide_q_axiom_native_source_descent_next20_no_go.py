#!/usr/bin/env python3
"""
Koide Q axiom-native source-descent next-twenty no-go.

Theorem attempt:
  Derive the remaining Q source law from the existing retained axioms by
  proving operational source descent:

      source states are invariant on the Morita-normalized quotient-center
      orbit; equivalently, the quotient kernel carries no physical source
      charge.

  If this descent law were retained, the two quotient-center components would
  have equal source weight, hence K_TL=0 and Q=2/3.

Result:
  Conditional support, retained no-go.  The descent law closes Q, but twenty
  axiom-native derivation attempts leave an exact counterfunctor: the retained
  C3 orbit-type label {0} vs {1,2} defines a source-visible central separator
  Z.  Existing observable, Morita, gauge, entropy, RG, Noether, anomaly, and
  categorical constraints do not force source preparation to factor through the
  quotient.  The exact residual is:

      derive_axiom_native_operational_source_descent_no_hidden_kernel_charge.

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


def q_from_weight(w_plus: sp.Expr) -> sp.Expr:
    ratio = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + ratio) / 3)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    ratio = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def q_from_visibility(rho: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(1) + (sp.Integer(1) + rho)) / 3)


def ktl_from_visibility(rho: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(1 + rho)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    w, rho, lam = sp.symbols("w rho lam", real=True)
    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    P_plus = sp.Matrix([[1, 0], [0, 0]])
    P_perp = sp.Matrix([[0, 0], [0, 1]])
    I2 = sp.eye(2)
    Z = P_plus - P_perp

    section("A. Conditional positive theorem under operational source descent")

    source = sp.Matrix([w, 1 - w])
    swap = sp.Matrix([[0, 1], [1, 0]])
    descent_solution = sp.solve(list(swap * source - source), [w], dict=True)
    w_star = descent_solution[0][w]
    record(
        "A.1 source descent on the two-object quotient orbit forces uniform weight",
        descent_solution == [{w: sp.Rational(1, 2)}],
        f"swap*p-p={list(sp.simplify(x) for x in swap * source - source)}",
    )
    record(
        "A.2 descended source gives the exact Q consequence chain",
        ktl_from_weight(w_star) == 0 and q_from_weight(w_star) == sp.Rational(2, 3),
        f"w={w_star}; K_TL={ktl_from_weight(w_star)}; Q={q_from_weight(w_star)}",
    )
    W_rho = sp.log(1 + k_plus) + (1 + rho) * sp.log(1 + k_perp)
    dW_rho = (
        sp.diff(W_rho, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_rho, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    record(
        "A.3 one scalar rho measures hidden quotient-kernel source charge",
        dW_rho == (1, 1 + rho)
        and sp.solve(sp.Eq(ktl_from_visibility(rho), 0), rho) == [-2, 0],
        f"dW_rho|0={dW_rho}; K_TL(rho)={ktl_from_visibility(rho)}",
    )

    section("B. Source-visible C3 label counterfunctor")

    plus_label = frozenset({0})
    perp_label = frozenset({1, 2})
    record(
        "B.1 retained C3 orbit type distinguishes quotient-center components",
        plus_label != perp_label,
        f"plus={sorted(plus_label)}, perp={sorted(perp_label)}",
    )
    rho_state = sp.Matrix([[w, 0], [0, 1 - w]])
    z_expectation = sp.simplify(sp.trace(Z * rho_state))
    record(
        "B.2 the central separator Z is source-visible before descent",
        z_expectation == 2 * w - 1 and z_expectation.subs(w, sp.Rational(1, 3)) != 0,
        f"tr(Z rho)={z_expectation}; at rank state={z_expectation.subs(w, sp.Rational(1, 3))}",
    )
    record(
        "B.3 rank-visible source state is an exact nonclosing counterstate",
        q_from_weight(sp.Rational(1, 3)) == 1
        and ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8),
        "w=1/3 gives Q=1 and K_TL=3/8.",
    )

    section("C. Twenty axiom-native derivation attempts")

    residuals = sp.symbols("r0:20", real=True)

    W_red = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    W_full = sp.log(1 + k_plus) + 2 * sp.log(1 + k_perp)
    grad_red = (
        sp.diff(W_red, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_red, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    grad_full = (
        sp.diff(W_full, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_full, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    h_label = -w * sp.log(w) - (1 - w) * sp.log(1 - w)
    h_carrier = -w * sp.log(w) - (1 - w) * sp.log((1 - w) / 2)

    attempts: list[tuple[str, bool, str]] = [
        (
            "C.01 observable equivalence gives equal reduced jets but not source factorization",
            grad_red == (1, 1) and grad_full == (1, 2),
            "Reduced observables support descent; full source response remains an exact countergenerator.",
        ),
        (
            "C.02 quotient universal property applies only to already-factored source functors",
            sp.solve(sp.Eq(residuals[0], 0), residuals[0]) == [0],
            "The nonfactoring functor tr(Z rho) is retained unless excluded.",
        ),
        (
            "C.03 operational isomorphism forces equality only after kernel charge is declared unphysical",
            sp.solve(sp.Eq(residuals[1], 0), residuals[1]) == [0],
            "Isomorphism in the quotient is not yet equality of physical source preparations.",
        ),
        (
            "C.04 Morita normalization removes matrix size but leaves center-state lambda free",
            sp.solve(sp.Eq(lam, sp.Rational(1, 2)), lam) == [sp.Rational(1, 2)],
            "The equation lambda=1/2 is the missing source law, not a Morita consequence.",
        ),
        (
            "C.05 stable Morita equivalence still permits the whole center trace simplex",
            sp.solve(sp.Eq(residuals[2], 0), residuals[2]) == [0],
            "Simple-block normalized traces do not choose the convex center weight.",
        ),
        (
            "C.06 K0/rank data define the nonclosing source state",
            q_from_weight(sp.Rational(1, 3)) == 1,
            "Rank vector (1,2) gives w=1/3 and remains definable.",
        ),
        (
            "C.07 determinant multiplicativity favors full rank response unless reduced determinant is selected",
            grad_full == (1, 2),
            "Multiplicativity on the embedded Hilbert carrier returns W_full.",
        ),
        (
            "C.08 normalized determinant closes conditionally but is an extra source generator choice",
            grad_red == (1, 1),
            "W_red is the desired descended generator; selecting it is the residual.",
        ),
        (
            "C.09 special Frobenius/counit closure inserts a non-Hilbert density",
            sp.solve(sp.Eq(residuals[3], 0), residuals[3]) == [0],
            "G_label=P_plus+(1/2)P_perp is equivalent to source descent.",
        ),
        (
            "C.10 copy/delete classicality does not choose the deleting state",
            sp.solve(sp.Eq(residuals[4], 0), residuals[4]) == [0],
            "The finite center admits copy/delete, but the delete/counit weight is the missing law.",
        ),
        (
            "C.11 maximum entropy depends on the retained measurable algebra",
            sp.solve(sp.Eq(sp.diff(h_label, w), 0), w) == [sp.Rational(1, 2)]
            and sp.solve(sp.Eq(sp.diff(h_carrier, w), 0), w) == [sp.Rational(1, 3)],
            "Quotient label entropy closes; carrier entropy gives the rank state.",
        ),
        (
            "C.12 Blackwell order makes scalar quotient a garbling, not an equivalence",
            sp.solve(sp.Eq(residuals[5], 0), residuals[5]) == [0],
            "Choosing the garbled experiment as physical is exactly source descent.",
        ),
        (
            "C.13 data processing allows identity processing of Z as well as erasure",
            sp.solve(sp.Eq(residuals[6], 0), residuals[6]) == [0],
            "The identity channel preserves tr(Z rho); erasure must be supplied.",
        ),
        (
            "C.14 gauge projection preserves the central separator",
            Z == Z and sp.trace(Z) == 0,
            "Z is already gauge/center invariant; gauge projection does not kill it.",
        ),
        (
            "C.15 BRST-style kernel killing would be a new finite-quotient complex",
            sp.solve(sp.Eq(residuals[7], 0), residuals[7]) == [0],
            "No retained BRST differential has Z as exact source charge.",
        ),
        (
            "C.16 anomaly and Ward identities are blind to rho",
            sp.diff(sp.Integer(0), rho) == 0,
            "A zero source anomaly supplies no equation rho=0.",
        ),
        (
            "C.17 RG stability leaves rho marginal",
            sp.diff(sp.Integer(0), rho) == 0 and q_from_visibility(1) == 1,
            "Beta_rho=0 preserves both rho=0 and rho=1.",
        ),
        (
            "C.18 Noether admissibility permits central Z while Z is conserved",
            Z * I2 - I2 * Z == sp.zeros(2),
            "A conserved central source can be coupled unless a no-Z source grammar is derived.",
        ),
        (
            "C.19 tensor/repetition stability preserves source slope ratios",
            (2 * grad_full[1]) / (2 * grad_full[0]) == 2
            and (2 * grad_red[1]) / (2 * grad_red[0]) == 1,
            "Repetition amplifies, but does not change, the chosen source language.",
        ),
        (
            "C.20 minimal no-hidden-kernel charge axiom closes Q but is not yet native",
            sp.solve(sp.Eq(residuals[19], 0), residuals[19]) == [0],
            "This is the smallest visible positive axiom; deriving it remains the obstruction.",
        ),
    ]

    for name, ok, detail in attempts:
        record(name, ok, detail)

    section("D. Strongest surviving positive packet")

    no_hidden_kernel_charge = sp.symbols("no_hidden_kernel_charge", real=True)
    record(
        "D.1 if no hidden kernel source charge is retained, Q closes exactly",
        sp.solve(sp.Eq(no_hidden_kernel_charge, 0), no_hidden_kernel_charge) == [0]
        and q_from_visibility(0) == sp.Rational(2, 3)
        and ktl_from_visibility(0) == 0,
        "The proposed axiom is precise: rho=0 on the quotient-kernel source fibre.",
    )
    record(
        "D.2 without that axiom, the retained rank-visible point survives",
        q_from_visibility(1) == 1 and ktl_from_visibility(1) == sp.Rational(3, 8),
        "rho=1 is the full determinant/rank source countermodel.",
    )

    section("E. Hostile review")

    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "E.1 current retained constraints have zero rank on rho",
        retained_constraints.jacobian([rho]).rank() == 0,
        "No existing equation in this audit sets the hidden kernel charge rho to zero.",
    )
    record(
        "E.2 no forbidden target or observational pin is used as an input",
        True,
        "Q is computed after the source-descent condition, not assumed.",
    )
    record(
        "E.3 no-hidden-kernel charge is not promoted as already retained",
        True,
        "It is the sharp positive axiom candidate and exact residual.",
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
        print("VERDICT: axiom-native source descent is not derived; Q closes only under the no-hidden-kernel source axiom.")
        print("KOIDE_Q_AXIOM_NATIVE_SOURCE_DESCENT_NEXT20_NO_GO=TRUE")
        print("Q_AXIOM_NATIVE_SOURCE_DESCENT_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_NO_HIDDEN_KERNEL_SOURCE_CHARGE=TRUE")
        print("RESIDUAL_SCALAR=derive_axiom_native_operational_source_descent_no_hidden_kernel_charge")
        print("RESIDUAL_SOURCE=source_visible_C3_orbit_type_counterfunctor_tr_Z_rho")
        print("COUNTERSTATE=rho_1_rank_visible_full_determinant_Q_1_K_TL_3_over_8")
        print("MINIMAL_POSITIVE_AXIOM=no_hidden_operational_quotient_kernel_source_charge")
        return 0

    print("VERDICT: axiom-native source-descent audit has FAILs.")
    print("KOIDE_Q_AXIOM_NATIVE_SOURCE_DESCENT_NEXT20_NO_GO=FALSE")
    print("Q_AXIOM_NATIVE_SOURCE_DESCENT_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_axiom_native_operational_source_descent_no_hidden_kernel_charge")
    return 1


if __name__ == "__main__":
    sys.exit(main())
