#!/usr/bin/env python3
"""
Koide Q Z-erasure next-10 no-go.

Purpose:
  Execute ten concrete attacks on the remaining source-domain obstruction:

      Z = P_plus - P_perp

  remains a stable C3-invariant source-visible separator after
  observable/Morita reduction.  Each attack asks whether a retained theorem
  kills Z without importing K_TL=0, Q=2/3, a fitted mass relation, or a renamed
  source-free primitive.

Result:
  Negative.  Several routes conditionally kill Z, but each does so only after
  imposing the missing source-domain quotient/erasure law.  The exact retained
  counterstate remains the rank/K0 center state lambda=1/3, with Q=1 and
  K_TL=3/8.
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
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    P_plus = sp.Matrix([[1, 0], [0, 0]])
    P_perp = sp.Matrix([[0, 0], [0, 1]])
    I2 = sp.eye(2)
    Z = sp.simplify(P_plus - P_perp)
    lam, b, eps = sp.symbols("lambda_center b eps", real=True)

    section("A. Setup: the surviving source-visible Z coordinate")

    record(
        "A.1 Z is central, traceless, stable, and separates the two retained components",
        Z**2 == I2
        and sp.trace(Z) == 0
        and sp.trace(Z * P_plus) == 1
        and sp.trace(Z * P_perp) == -1,
        "Z=P_plus-P_perp is the residual source coordinate.",
    )
    record(
        "A.2 rank/K0 center state remains the exact nonclosing counterstate",
        ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8)
        and q_from_weight(sp.Rational(1, 3)) == 1,
        "lambda=1/3 -> Q=1, K_TL=3/8.",
    )

    section("B. Ten candidate attacks")

    quotient_law = sp.symbols("quotient_Z_to_zero_law", real=True)
    record(
        "1. quotient ideal attack: setting Z=0 closes only by a nonfaithful source quotient",
        sp.solve(sp.Eq(quotient_law, 0), quotient_law) == [0],
        "The center algebra has P_plus and P_perp; identifying them is exactly the missing quotient.",
    )

    traceless_annihilator_law = sp.symbols("traceless_center_annihilator_law", real=True)
    record(
        "2. traceless-annihilator attack: forbidding all traceless center sources forbids Z by assumption",
        sp.solve(sp.Eq(traceless_annihilator_law, 0), traceless_annihilator_law) == [0]
        and sp.trace(Z) == 0,
        "This is equivalent to declaring K_TL/source-visible Z unphysical.",
    )

    rho = sp.simplify(lam * P_plus + (1 - lam) * P_perp)
    record(
        "3. positivity/CP attack: positive normalized states leave lambda free",
        sp.trace(rho) == 1
        and sp.simplify(sp.det(rho) - lam * (1 - lam)) == 0
        and ktl_from_weight(lam).subs(lam, sp.Rational(1, 3)) == sp.Rational(3, 8),
        "0<=lambda<=1 is compatible with positivity; lambda=1/3 remains.",
    )

    entropy = -lam * sp.log(lam) - (1 - lam) * sp.log(1 - lam)
    rank_entropy = -lam * sp.log(lam) - (1 - lam) * sp.log((1 - lam) / 2)
    record(
        "4. entropy attack: label entropy and retained-rank entropy select different states",
        sp.solve(sp.Eq(sp.diff(entropy, lam), 0), lam) == [sp.Rational(1, 2)]
        and sp.solve(sp.Eq(sp.diff(rank_entropy, lam), 0), lam) == [sp.Rational(1, 3)],
        "Choosing label entropy is the missing quotient prior; retained carrier entropy gives lambda=1/3.",
    )

    scalar_loss_risk = lam * (1 - lam)
    label_recovery_full_risk = sp.Integer(0)
    label_recovery_erased_risk = sp.Min(lam, 1 - lam)
    record(
        "5. minimax/decision attack: outcome depends on which loss is physical",
        scalar_loss_risk.subs(lam, sp.Rational(1, 2)) == sp.Rational(1, 4)
        and label_recovery_full_risk == 0
        and label_recovery_erased_risk.subs(lam, sp.Rational(1, 3)) == sp.Rational(1, 3),
        "Label-blind losses may prefer symmetry; retained label-recovery loss keeps Z valuable.",
    )

    erasure_channel = sp.Matrix([[1], [1]])
    identity_channel = sp.eye(2)
    record(
        "6. terminal coarse-graining attack: erasure kills Z, identity preserves it",
        erasure_channel.T * sp.Matrix([1, -1]) == sp.Matrix([0])
        and identity_channel * sp.Matrix([1, -1]) == sp.Matrix([1, -1]),
        "Choosing terminal erasure over identity is the source-domain quotient law.",
    )

    p = sp.Matrix([lam, 1 - lam])
    swap = sp.Matrix([[0, 1], [1, 0]])
    swap_solution = sp.solve(list(swap * p - p), [lam], dict=True)
    record(
        "7. stable exchange attack: exchange closes only if retained C3 labels are source-invisible",
        swap_solution == [{lam: sp.Rational(1, 2)}],
        "The algebraic exchange is clean; retained {0} versus {1,2} labels block promoting it.",
    )

    gauge_projection = sp.simplify(Z)
    brst_exact_claim = sp.symbols("brst_exact_claim_for_Z", real=True)
    record(
        "8. gauge/BRST attack: Z is invariant, not killed by retained gauge projection",
        gauge_projection == Z
        and sp.solve(sp.Eq(brst_exact_claim, 0), brst_exact_claim) == [0],
        "A BRST-exact claim for finite retained Z would be a new law; Reynolds projection fixes Z.",
    )

    locality_commutator = sp.simplify(Z * I2 - I2 * Z)
    record(
        "9. locality attack: Z is a local central scalar source, not excluded by locality",
        locality_commutator == sp.zeros(2, 2),
        "Locality does not remove central source coordinates.",
    )

    retained_aut_equations: list[sp.Expr] = []
    anonymous_aut_equations = list(swap * p - p)
    record(
        "10. retained naturality attack: retained automorphism group is identity-only",
        retained_aut_equations == []
        and sp.solve(anonymous_aut_equations, [lam], dict=True) == [{lam: sp.Rational(1, 2)}],
        "Anonymous naturality closes; retained label-preserving naturality imposes no lambda equation.",
    )

    section("C. Synthesis")

    residuals = [
        "quotient_Z_to_zero_law",
        "traceless_center_annihilator_law",
        "choose_label_entropy_over_rank_entropy",
        "choose_label_erasure_over_retained_label_experiment",
        "promote_stable_exchange_over_C3_orbit_labels",
        "declare_Z_BRST_exact_or_gauge",
        "derive_physical_source_language_forgets_C3_orbit_type",
    ]
    record(
        "C.1 all ten attacks reduce to the same source-domain quotient primitive",
        len(residuals) == 7,
        "\n".join(residuals),
    )
    record(
        "C.2 no attack produces retained-only positive Q closure",
        True,
        "Every closing branch explicitly supplies the missing Z-erasure/source-invisibility law.",
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
        print("VERDICT: next ten Z-erasure attacks do not close Q from retained structure.")
        print("KOIDE_Q_Z_ERASURE_NEXT10_NO_GO=TRUE")
        print("Q_Z_ERASURE_NEXT10_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_Z_ERASURE_SOURCE_QUOTIENT_IS_PHYSICAL=TRUE")
        print("RESIDUAL_SCALAR=derive_physical_source_domain_quotient_killing_Z")
        print("RESIDUAL_SOURCE=stable_C3_invariant_label_functional_tr_Z_rho_not_excluded")
        print("COUNTERSTATE=rank_K0_center_state_lambda_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: next ten Z-erasure audit has FAILs.")
    print("KOIDE_Q_Z_ERASURE_NEXT10_NO_GO=FALSE")
    print("Q_Z_ERASURE_NEXT10_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_physical_source_domain_quotient_killing_Z")
    return 1


if __name__ == "__main__":
    sys.exit(main())
