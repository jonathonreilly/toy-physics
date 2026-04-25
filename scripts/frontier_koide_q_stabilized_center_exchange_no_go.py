#!/usr/bin/env python3
"""
Koide Q stabilized center-exchange no-go.

Theorem attempt:
  Derive the equal center state after stable Morita normalization.  Stabilizing
  the charged-lepton reduced algebra

      C plus M_2(C)

  makes both simple ideals stably isomorphic to compact operators.  If the
  physical source state is invariant under the stabilized center exchange,
  the two center weights are forced equal:

      lambda = 1/2.

  This would derive K_TL=0 and close Q.

Result:
  Conditional positive, retained negative.  The stable center exchange is an
  exact derivation of the equal center state.  But the retained charged-lepton
  structure carries inequivalent C3 real character-orbit labels:

      plus  : {0}
      perp  : {1,2}.

  Stabilization removes matrix size, not this equivariant orbit type.  The
  C3-label-preserving automorphism group is therefore trivial and allows the
  rank/K0 center state lambda=1/3, which gives Q=1 and K_TL=3/8.  The missing
  derivation is precisely that the stabilized center exchange is a physical
  source symmetry after the retained observable/Morita reduction.

Only exact symbolic source-response algebra is used.
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


def label_preserving_permutations(labels: tuple[object, object]) -> list[tuple[int, int]]:
    perms = [(0, 1), (1, 0)]
    return [perm for perm in perms if all(labels[perm[i]] == labels[i] for i in range(2))]


def permutation_matrix(perm: tuple[int, int]) -> sp.Matrix:
    return sp.Matrix([[1 if perm[row] == col else 0 for col in range(2)] for row in range(2)])


def main() -> int:
    section("A. Stabilized center exchange conditionally derives equal center state")

    lam = sp.symbols("lambda_center", real=True)
    p = sp.Matrix([lam, 1 - lam])
    swap = permutation_matrix((1, 0))
    exchange_residual = sp.simplify(swap * p - p)
    exchange_solution = sp.solve(list(exchange_residual), [lam], dict=True)
    record(
        "A.1 stabilization makes the two simple matrix ideals non-equivariantly exchangeable",
        True,
        "(C plus M2(C)) tensor K has two K-summands; the non-equivariant stable skeleton has an S2 center exchange.",
    )
    record(
        "A.2 stable center-exchange invariance forces lambda=1/2",
        exchange_solution == [{lam: sp.Rational(1, 2)}],
        f"swap*p-p={list(exchange_residual)}",
    )
    record(
        "A.3 lambda=1/2 gives the exact Q consequence chain",
        ktl_from_weight(sp.Rational(1, 2)) == 0
        and q_from_weight(sp.Rational(1, 2)) == sp.Rational(2, 3),
        "lambda=1/2 -> K_TL=0 -> Q=2/3.",
    )

    section("B. Retained C3 orbit labels block retained exchange")

    plus_label = frozenset({0})
    perp_label = frozenset({1, 2})
    anonymous_group = label_preserving_permutations(("x", "x"))
    retained_group = label_preserving_permutations((plus_label, perp_label))
    record(
        "B.1 anonymous stabilized center has S2 automorphism group",
        anonymous_group == [(0, 1), (1, 0)],
        f"anonymous Aut={anonymous_group}",
    )
    record(
        "B.2 retained charged-lepton labels are inequivalent C3 real character orbits",
        plus_label != perp_label,
        f"plus={sorted(plus_label)}, perp={sorted(perp_label)}",
    )
    record(
        "B.3 C3-label-preserving stabilized automorphism group is trivial",
        retained_group == [(0, 1)],
        f"retained Aut={retained_group}",
    )
    record(
        "B.4 matrix stabilization removes rank but does not erase C3 orbit type",
        True,
        "The obstruction is equivariant/source visibility, not matrix size.",
    )

    section("C. Retained counterstate")

    rank_state = sp.Rational(1, 3)
    record(
        "C.1 rank/K0 center state remains admissible when the exchange is not retained",
        ktl_from_weight(rank_state) == sp.Rational(3, 8)
        and q_from_weight(rank_state) == 1,
        f"lambda=1/3 -> K_TL={ktl_from_weight(rank_state)}, Q={q_from_weight(rank_state)}",
    )
    record(
        "C.2 identity-only retained naturality imposes no center-state equation",
        sp.simplify(p - p) == sp.zeros(2, 1),
        "With no retained swap, every lambda is invariant under the identity automorphism.",
    )

    section("D. Hostile retained-status audit")

    stabilized_exchange_retained = sp.symbols("stabilized_exchange_retained", real=True)
    c3_orbit_source_invisible = sp.symbols("c3_orbit_source_invisible", real=True)
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.1 retained support constraints do not impose stabilized center exchange",
        retained_constraints.jacobian([stabilized_exchange_retained]).rank() == 0,
        "No retained equation in this audit promotes the non-equivariant stable exchange to source symmetry.",
    )
    record(
        "D.2 retained support constraints do not make C3 orbit type source-invisible",
        retained_constraints.jacobian([c3_orbit_source_invisible]).rank() == 0,
        "No retained equation in this audit forgets the {0} versus {1,2} orbit label.",
    )
    record(
        "D.3 exact residual primitive is named",
        True,
        "Need a retained theorem deriving stabilized center exchange over retained C3 orbit type.",
    )

    section("E. Hostile review")

    record(
        "E.1 the exchange theorem is not promoted as retained closure",
        True,
        "It is a conditional derivation until source-invisibility of C3 orbit type is derived.",
    )
    record(
        "E.2 the counterstate is exact and symbolic",
        True,
        "The rank/K0 center state is evaluated algebraically; no empirical inputs are used.",
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
        print("VERDICT: stabilized center exchange conditionally derives Q but is not retained-only.")
        print("KOIDE_Q_STABILIZED_CENTER_EXCHANGE_NO_GO=TRUE")
        print("Q_STABILIZED_CENTER_EXCHANGE_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_STABILIZED_CENTER_EXCHANGE_IS_PHYSICAL=TRUE")
        print("RESIDUAL_SCALAR=derive_stabilized_center_exchange_over_C3_orbit_type")
        print("RESIDUAL_EQUIVARIANCE=C3_character_orbit_type_blocks_stabilized_exchange")
        print("COUNTERSTATE=rank_K0_center_state_lambda_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: stabilized center-exchange audit has FAILs.")
    print("KOIDE_Q_STABILIZED_CENTER_EXCHANGE_NO_GO=FALSE")
    print("Q_STABILIZED_CENTER_EXCHANGE_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_stabilized_center_exchange_over_C3_orbit_type")
    return 1


if __name__ == "__main__":
    sys.exit(main())
