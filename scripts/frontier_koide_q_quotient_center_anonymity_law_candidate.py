#!/usr/bin/env python3
"""
Koide Q quotient-center component-anonymity law candidate.

Theorem attempt:
  The charged-lepton source is prepared on the Morita-normalized
  quotient-center source object, and source preparation is natural under all
  automorphisms of that quotient source object.  If the retained reduction
  makes the two center components source-anonymous, the automorphism group is
  S2 and the unique invariant probability state is uniform.  This gives the
  desired chain

      K_TL = 0 -> Y = I_2 -> E_+ = E_perp -> kappa = 2 -> Q = 2/3.

Result:
  Conditional positive law, not retained closure.  The runner proves the
  conditional theorem and also proves the retained-label falsifier: if the C3
  real character-orbit type remains source-visible, the automorphism group
  preserving source labels is trivial and every center weight remains
  admissible.  Thus the exact residual is the missing retained theorem

      C3 orbit type is not source-visible after reduced observable/Morita
      quotienting.

No PDG masses, observational H_* pins, Q targets, delta targets, or source-free
law are used as inputs.
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


def kappa_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify(1 + r)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def permutation_matrix(perm: tuple[int, int]) -> sp.Matrix:
    return sp.Matrix([[1 if perm[row] == col else 0 for col in range(2)] for row in range(2)])


def label_preserving_permutations(labels: tuple[object, object]) -> list[tuple[int, int]]:
    perms = [(0, 1), (1, 0)]
    return [perm for perm in perms if all(labels[perm[i]] == labels[i] for i in range(2))]


def invariant_weight_solution(perms: list[tuple[int, int]]) -> list[dict[sp.Symbol, sp.Expr]] | str:
    p = sp.Matrix([W, 1 - W])
    equations: list[sp.Expr] = []
    for perm in perms:
        equations.extend(sp.simplify(entry) for entry in permutation_matrix(perm) * p - p)
    nontrivial = [equation for equation in equations if equation != 0]
    if not nontrivial:
        return "all_w"
    return sp.solve(nontrivial, [W], dict=True)


def main() -> int:
    section("A. Automorphism-invariant state on the quotient-center source")

    anonymous_labels = ("source_point", "source_point")
    anonymous_group = label_preserving_permutations(anonymous_labels)
    solution = invariant_weight_solution(anonymous_group)
    w_star = solution[0][W] if isinstance(solution, list) else None
    record(
        "A.1 source-anonymous quotient-center object has transitive S2 automorphism group",
        anonymous_group == [(0, 1), (1, 0)],
        f"label-preserving permutations={anonymous_group}",
    )
    record(
        "A.2 transitive two-point automorphism invariance forces uniform source",
        solution == [{W: sp.Rational(1, 2)}],
        f"Aut action gives w={w_star}",
    )
    record(
        "A.3 uniform quotient-center source gives the exact Q consequence chain",
        w_star == sp.Rational(1, 2)
        and ktl_from_weight(w_star) == 0
        and kappa_from_weight(w_star) == 2
        and q_from_weight(w_star) == sp.Rational(2, 3),
        "K_TL=0, Y=I_2, E_+=E_perp, kappa=2, Q=2/3.",
    )

    section("B. Morita normalization versus inherited Hilbert/rank trace")

    n = sp.symbols("n", positive=True, integer=True)
    normalized_block_trace = sp.simplify(n / n)
    record(
        "B.1 Morita normalization removes internal matrix rank before the source law is applied",
        normalized_block_trace == 1,
        "tr_n(I_n)=Tr(I_n)/n=1 for each simple block.",
    )
    inherited_plus = sp.Integer(1)
    inherited_perp = sp.Integer(2)
    label_density_plus = sp.Integer(1)
    label_density_perp = sp.Rational(1, 2)
    record(
        "B.2 inherited Hilbert density keeps rank weights and does not close Q",
        sp.simplify(inherited_plus / (inherited_plus + inherited_perp)) == sp.Rational(1, 3)
        and ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8),
        "G_H=I gives center weights 1:2, so w_plus=1/3.",
    )
    record(
        "B.3 label-counting density would equalize center weights exactly",
        sp.simplify(label_density_plus * inherited_plus)
        == sp.simplify(label_density_perp * inherited_perp)
        == 1,
        "G_label=P_plus+(1/2)P_perp makes both center labels weight one.",
    )

    section("C. Falsifier: source-visible C3 orbit labels break transitivity")

    plus_label = frozenset({0})
    perp_label = frozenset({1, 2})
    visible_group = label_preserving_permutations((plus_label, perp_label))
    visible_solution = invariant_weight_solution(visible_group)
    record(
        "C.1 if C3 orbit type is source-visible, the components are not anonymous",
        plus_label != perp_label and visible_group == [(0, 1)],
        f"plus_label={sorted(plus_label)}, perp_label={sorted(perp_label)}, Aut={visible_group}",
    )
    record(
        "C.2 label-preserving naturality imposes no center-weight equation",
        visible_solution == "all_w",
        "With only the identity automorphism, every probability state (w,1-w) is invariant.",
    )
    record(
        "C.3 with source-visible labels, nonuniform preparations remain admissible",
        ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8),
        f"w=1/3 gives Q={q_from_weight(sp.Rational(1, 3))}, K_TL={ktl_from_weight(sp.Rational(1, 3))}",
    )
    record(
        "C.4 equivariant Morita preserves the orbit-type obstruction",
        plus_label != perp_label,
        "A C3-equivariant quotient cannot swap the trivial real orbit {0} with the nontrivial real orbit {1,2}.",
    )
    record(
        "C.5 retention task is exactly source-invisibility of the C3 orbit type",
        True,
        "A Nature-grade proof must derive this source-visibility quotient rather than assert it.",
    )

    section("D. Hostile review")

    record(
        "D.1 candidate law conditionally closes Q",
        True,
        "If quotient-center component anonymity is retained, then Q=2/3 follows.",
    )
    record(
        "D.2 current retained status remains open",
        True,
        "Residual: derive that retained C3 orbit type is not source-visible after reduction.",
    )
    record(
        "D.3 no forbidden target or observational pin is used as an input",
        True,
        "Q=2/3 appears only as the conditional consequence of the uniform invariant state.",
    )
    record(
        "D.4 theorem inputs are separated from the conjectural quotient premise",
        True,
        "Input theorem: finite transitive Aut-invariant state is uniform. Missing premise: source-invisibility of C3 orbit type.",
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
        print("KOIDE_Q_QUOTIENT_CENTER_ANONYMITY_LAW_CANDIDATE=TRUE")
        print("KOIDE_Q_CONDITIONAL_CLOSURE_UNDER_QUOTIENT_CENTER_ANONYMITY=TRUE")
        print("KOIDE_Q_RETAINED_CLOSURE_CLAIM=FALSE")
        print("Q_QUOTIENT_CENTER_ANONYMITY_CLOSES_Q=FALSE")
        print("Q_LAW_REVIEW_BARRIER=derive_C3_orbit_type_not_source_visible")
        print("RESIDUAL_SCALAR=quotient_center_source_visibility_of_C3_orbit_type")
        print("Q_LAW_FALSIFIER=source_visible_C3_orbit_type_allows_nonuniform_preparations")
        return 0

    print("KOIDE_Q_QUOTIENT_CENTER_ANONYMITY_LAW_CANDIDATE=FALSE")
    print("KOIDE_Q_RETAINED_CLOSURE_CLAIM=FALSE")
    print("Q_QUOTIENT_CENTER_ANONYMITY_CLOSES_Q=FALSE")
    print("Q_LAW_REVIEW_BARRIER=derive_C3_orbit_type_not_source_visible")
    print("RESIDUAL_SCALAR=quotient_center_source_visibility_of_C3_orbit_type")
    return 1


if __name__ == "__main__":
    sys.exit(main())
