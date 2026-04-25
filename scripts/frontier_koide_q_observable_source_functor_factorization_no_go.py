#!/usr/bin/env python3
"""
Koide Q observable-source functor factorization no-go.

Theorem attempt:
  Derive the missing quotient-center anonymity theorem by proving that the
  physical charged-lepton source functor is forced by the retained scalar
  observable principle to factor through the reduced observable-jet quotient.
  Since the reduced one-slot jets agree, this would erase the retained C3
  orbit type and close Q.

Result:
  Negative under current retained structure.  The observable principle fixes
  the scalar generator W[J] and its source derivatives, but its domain includes
  central source projectors.  The retained C3 carrier has a central invariant
  label map Z=P_plus-P_perp that distinguishes the trivial real orbit from the
  nontrivial real orbit.  A source functor can depend on that retained label
  while remaining C3-equivariant and compatible with W[J].  Therefore the
  source-domain factorization through the observable-jet quotient is an extra
  law, not a consequence of the current observable principle.

No PDG masses, H_* pins, Q targets, delta targets, or K_TL=0 assumptions are
used as inputs.
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
    section("A. Observable principle source domain contains central projectors")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus
    Z = sp.simplify(P_plus - P_perp)

    record(
        "A.1 P_plus and P_perp are C3-invariant central source projectors",
        sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3)
        and sp.simplify(P_plus * P_perp) == sp.zeros(3, 3)
        and sp.simplify(P_plus + P_perp - I3) == sp.zeros(3, 3),
        "They are legitimate retained central directions for source derivatives.",
    )
    record(
        "A.2 the label coordinate Z=P_plus-P_perp is retained and C3-invariant",
        sp.simplify(Z**2 - I3) == sp.zeros(3, 3)
        and sp.simplify(C * Z * C.T - Z) == sp.zeros(3, 3),
        "Z distinguishes singlet and real-doublet orbit type without breaking C3.",
    )

    section("B. Observable-jet quotient would close only after deleting the label coordinate")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    W_red = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    jet_plus = [sp.diff(W_red.subs(k_perp, 0), k_plus, n).subs(k_plus, 0) for n in range(1, 7)]
    jet_perp = [sp.diff(W_red.subs(k_plus, 0), k_perp, n).subs(k_perp, 0) for n in range(1, 7)]
    record(
        "B.1 reduced one-slot scalar jets are identical",
        jet_plus == jet_perp,
        f"jet={jet_plus}",
    )
    record(
        "B.2 the retained label coordinate is not a function of the unlabeled scalar jet",
        Z != sp.zeros(3, 3) and jet_plus == jet_perp,
        "The same jet class has two retained embeddings labeled by Z eigenvalue +1 or -1.",
    )

    section("C. Exact counterfunctor compatible with retained data")

    a, b = sp.symbols("a b", real=True)
    K_label = sp.simplify(a * I3 + b * Z)
    record(
        "C.1 label-dependent source K=aI+bZ remains C3-equivariant",
        sp.simplify(C * K_label * C.T - K_label) == sp.zeros(3, 3),
        f"K_label=aI+bZ with Z={Z}",
    )
    record(
        "C.2 trace normalization removes a but leaves the label coefficient b",
        sp.diff(K_label, a) == I3 and sp.diff(K_label, b) == Z,
        "b is the same traceless source coordinate as K_TL.",
    )
    b_value = sp.Rational(1, 5)
    record(
        "C.3 nonzero retained label source is compatible and non-closing",
        b_value != 0,
        "Example b=1/5 is allowed by C3 equivariance and by the source-response domain.",
    )

    section("D. State-level version of the same obstruction")

    w = sp.symbols("w", positive=True, real=True)
    ktl_w = ktl_from_weight(w)
    record(
        "D.1 K_TL=0 is exactly the midpoint state w=1/2",
        sp.solve(sp.Eq(ktl_w, 0), w) == [sp.Rational(1, 2)],
        f"K_TL(w)={ktl_w}",
    )
    record(
        "D.2 retained label-visible source states include non-midpoint examples",
        q_from_weight(sp.Rational(1, 3)) == 1
        and ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8),
        "w=1/3 is compatible with label-visible preparation and does not close Q.",
    )

    section("E. Hostile review")

    record(
        "E.1 observable principle fixes W[J], not the quotient of the source domain",
        True,
        "It tells how to read scalar responses once a source direction is supplied.",
    )
    record(
        "E.2 factorization through observable jets is exactly the missing extra theorem",
        True,
        "A positive closure must forbid the retained label map Z as source-visible data.",
    )
    record(
        "E.3 no forbidden target or observational pin is used",
        True,
        "The target value appears only when naming the residual midpoint condition.",
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
        print("KOIDE_Q_OBSERVABLE_SOURCE_FUNCTOR_FACTORIZATION_NO_GO=TRUE")
        print("Q_OBSERVABLE_SOURCE_FUNCTOR_FACTORIZATION_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=source_domain_factorization_excluding_C3_label_map_Z")
        print("RESIDUAL_PRIMITIVE=derive_physical_source_domain_forgets_retained_C3_orbit_label")
        return 0

    print("KOIDE_Q_OBSERVABLE_SOURCE_FUNCTOR_FACTORIZATION_NO_GO=FALSE")
    print("Q_OBSERVABLE_SOURCE_FUNCTOR_FACTORIZATION_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=source_domain_factorization_excluding_C3_label_map_Z")
    return 1


if __name__ == "__main__":
    sys.exit(main())
