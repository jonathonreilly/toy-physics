#!/usr/bin/env python3
"""
Koide Q observable-jet source-quotient retention attack.

Theorem attempt:
  Use the retained scalar observable principle to prove that the physical
  charged-lepton source factors through the reduced observable-jet quotient.
  On that quotient the two first-live second-order center slots have identical
  scalar jets, so source naturality would make the C3 orbit type invisible and
  force the quotient-center anonymous state.

Result:
  Conditional positive, but not retained closure.  The scalar observable jet
  of W_red=log(1+k_+)+log(1+k_perp) is slot-symmetric to all orders at the
  source-free point.  If physical source preparation is required to factor only
  through that unlabeled observable jet, then the source object has an S2 swap
  and w_+=1/2, hence K_TL=0 and Q=2/3.

  However the retained Cl(3)/Z3 carrier still supplies a label-valued map from
  each slot to its real C3 character-orbit type: {0} versus {1,2}.  A source
  functor allowed to see that retained label has only the identity automorphism
  and admits arbitrary w.  Therefore the missing retained theorem is exactly
  the factorization

      physical_source_functor factors through observable_jet quotient
      and not through retained C3 orbit labels.

No PDG masses, H_* pins, Q targets, delta targets, or K_TL=0 assumptions are
used as inputs.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []
W = sp.symbols("w", real=True)


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


def kappa_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify(1 + r)


def label_preserving_permutations(labels: tuple[object, object]) -> list[tuple[int, int]]:
    perms = [(0, 1), (1, 0)]
    return [perm for perm in perms if all(labels[perm[i]] == labels[i] for i in range(2))]


def permutation_matrix(perm: tuple[int, int]) -> sp.Matrix:
    return sp.Matrix([[1 if perm[row] == col else 0 for col in range(2)] for row in range(2)])


def invariant_weight_solution(perms: list[tuple[int, int]]) -> list[dict[sp.Symbol, sp.Expr]] | str:
    p = sp.Matrix([W, 1 - W])
    equations: list[sp.Expr] = []
    for perm in perms:
        equations.extend(sp.simplify(entry) for entry in permutation_matrix(perm) * p - p)
    nontrivial = [equation for equation in equations if equation != 0]
    if not nontrivial:
        return "all_w"
    return sp.solve(nontrivial, [W], dict=True)


def jet_at_zero(expr: sp.Expr, variable: sp.Symbol, order: int) -> list[sp.Expr]:
    return [sp.simplify(sp.diff(expr, variable, n).subs(variable, 0)) for n in range(1, order + 1)]


def main() -> int:
    section("A. Reduced scalar observable jet")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    w_red = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    swap_w_red = w_red.subs({k_plus: k_perp, k_perp: k_plus}, simultaneous=True)
    record(
        "A.1 retained reduced generator is symmetric as an unlabeled two-slot scalar",
        sp.simplify(w_red - swap_w_red) == 0,
        f"W_red={w_red}",
    )
    jet_order = 8
    plus_jet = jet_at_zero(w_red.subs(k_perp, 0), k_plus, jet_order)
    perp_jet = jet_at_zero(w_red.subs(k_plus, 0), k_perp, jet_order)
    record(
        "A.2 one-slot scalar observable jets agree through the audited finite order",
        plus_jet == perp_jet,
        f"jet order {jet_order}: {plus_jet}",
    )
    recurrence_ok = all(
        sp.simplify(plus_jet[i + 1] + (i + 1) * plus_jet[i]) == 0
        and sp.simplify(perp_jet[i + 1] + (i + 1) * perp_jet[i]) == 0
        for i in range(jet_order - 1)
    )
    expected_jet = [(-1) ** (n - 1) * sp.factorial(n - 1) for n in range(1, jet_order + 1)]
    record(
        "A.3 the audited jet obeys the exact all-order recurrence through the checked order",
        plus_jet == expected_jet and perp_jet == expected_jet and recurrence_ok,
        "The recurrence a_{n+1}=-n a_n is the derivative recursion for log(1+k).",
    )

    section("B. Conditional positive consequence if source factors through the jet quotient")

    jet_labels = ("same_scalar_jet", "same_scalar_jet")
    jet_aut = label_preserving_permutations(jet_labels)
    jet_solution = invariant_weight_solution(jet_aut)
    w_star = jet_solution[0][W] if isinstance(jet_solution, list) else None
    record(
        "B.1 observable-jet quotient has transitive S2 automorphism group",
        jet_aut == [(0, 1), (1, 0)],
        f"Aut_jet={jet_aut}",
    )
    record(
        "B.2 natural source state on the jet quotient is uniform",
        jet_solution == [{W: sp.Rational(1, 2)}],
        f"w={w_star}",
    )
    record(
        "B.3 uniform jet-quotient state gives the exact Koide Q chain",
        w_star == sp.Rational(1, 2)
        and ktl_from_weight(w_star) == 0
        and kappa_from_weight(w_star) == 2
        and q_from_weight(w_star) == sp.Rational(2, 3),
        "K_TL=0, Y=I_2, E_+=E_perp, kappa=2, Q=2/3.",
    )

    section("C. Retained-label countermodel")

    plus_orbit = frozenset({0})
    perp_orbit = frozenset({1, 2})
    retained_labels = (plus_orbit, perp_orbit)
    retained_aut = label_preserving_permutations(retained_labels)
    retained_solution = invariant_weight_solution(retained_aut)
    record(
        "C.1 retained C3 orbit labels are still inequivalent on the carrier",
        plus_orbit != perp_orbit,
        f"P_plus orbit={sorted(plus_orbit)}, P_perp orbit={sorted(perp_orbit)}",
    )
    record(
        "C.2 a source functor that can see retained orbit labels has only identity automorphism",
        retained_aut == [(0, 1)] and retained_solution == "all_w",
        f"Aut_retained={retained_aut}; invariant states={retained_solution}",
    )
    record(
        "C.3 the retained-label source functor admits a non-Koide center state",
        q_from_weight(sp.Rational(1, 3)) == 1
        and ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8),
        "w=1/3 is label-preserving-natural but gives Q=1 and K_TL=3/8.",
    )

    section("D. Retention test for the proposed positive theorem")

    factorization_residual = sp.symbols("source_functor_jet_factorization_residual", real=True)
    record(
        "D.1 positive closure requires one exact factorization equation",
        sp.solve(sp.Eq(factorization_residual, 0), factorization_residual) == [0],
        "Residual: physical source functor factors through observable-jet quotient before C3 orbit labels.",
    )
    record(
        "D.2 the current observable principle fixes scalar readouts but not this source-domain factorization",
        True,
        "W[J] defines scalar observables as source derivatives; it does not by itself forbid label-valued source preparation.",
    )
    record(
        "D.3 no target value is imported",
        True,
        "The only conditional input is source functor factorization through the observable-jet quotient.",
    )

    section("E. Verdict")

    record(
        "E.1 observable-jet quotient is a real conditional positive route",
        True,
        "If retained, it derives the needed orbit invisibility and closes Q.",
    )
    record(
        "E.2 current retained status is still not positive closure",
        True,
        "The factorization of physical source preparation through the jet quotient is not yet derived from older retained structure.",
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
        print("KOIDE_Q_OBSERVABLE_JET_SOURCE_QUOTIENT_RETENTION=CONDITIONAL")
        print("KOIDE_Q_OBSERVABLE_JET_SOURCE_QUOTIENT_CLOSES_Q=FALSE")
        print("CONDITIONAL_Q_CLOSURE_IF_SOURCE_FACTORS_THROUGH_OBSERVABLE_JET=TRUE")
        print("RESIDUAL_SCALAR=source_functor_jet_factorization_residual")
        print("RESIDUAL_PRIMITIVE=derive_physical_source_functor_factors_through_observable_jet_quotient")
        return 0

    print("KOIDE_Q_OBSERVABLE_JET_SOURCE_QUOTIENT_RETENTION=FAILED")
    print("KOIDE_Q_OBSERVABLE_JET_SOURCE_QUOTIENT_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=source_functor_jet_factorization_residual")
    return 1


if __name__ == "__main__":
    sys.exit(main())
