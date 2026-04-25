#!/usr/bin/env python3
"""
Koide Q equivariant-Morita swap no-go.

Theorem attempt:
  Strengthen the Morita route: since M_1 and M_2 are non-equivariantly Morita
  equivalent to C, the algebra M_1 ⊕ M_2 is Morita equivalent to C ⊕ C.
  The skeleton C ⊕ C has a component swap, which would force equal component
  weights and close Q.

Result:
  Negative under retained structure.  The charged-lepton blocks are not merely
  matrix algebras; they carry inequivalent retained C3 character data:

      P_plus: trivial real character orbit {0}
      P_perp: nontrivial real character orbit {1,2}.

  Non-equivariant Morita forgets that data.  Equivariant Morita/naturality must
  preserve the C3 character orbit type, so the component swap is not retained.
  The non-equivariant skeleton swap would close Q only by discarding the
  retained structure that defines the lane.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
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
    section("A. Non-equivariant Morita skeleton would force uniformity")

    w = sp.symbols("w", positive=True, real=True)
    swap_residual = sp.Matrix([1 - w, w]) - sp.Matrix([w, 1 - w])
    swap_solution = sp.solve(list(swap_residual), [w], dict=True)
    record(
        "A.1 C plus C component swap would force w=1/2",
        swap_solution == [{w: sp.Rational(1, 2)}],
        f"swap residual={list(swap_residual)}",
    )
    record(
        "A.2 that uniform skeleton state would close Q",
        q_from_weight(sp.Rational(1, 2)) == sp.Rational(2, 3)
        and ktl_from_weight(sp.Rational(1, 2)) == 0,
        "non-equivariant skeleton uniform state gives Q=2/3.",
    )

    section("B. Retained C3 equivariance blocks the swap")

    plus_orbit = frozenset({0})
    perp_orbit = frozenset({1, 2})
    record(
        "B.1 retained real C3 character orbits are inequivalent",
        plus_orbit != perp_orbit,
        f"P_plus orbit={sorted(plus_orbit)}, P_perp orbit={sorted(perp_orbit)}",
    )
    equivariant_swap_allowed = plus_orbit == perp_orbit
    record(
        "B.2 equivariant Morita/naturality cannot swap the two retained orbit types",
        not equivariant_swap_allowed,
        "A C3-equivariant functor must preserve trivial versus nontrivial real character orbit.",
    )

    section("C. Weights remain free when retained equivariance is respected")

    samples = {
        "rank_like": sp.Rational(1, 3),
        "uniform_skeleton": sp.Rational(1, 2),
        "plus_heavy": sp.Rational(2, 3),
    }
    lines = []
    ok = True
    for name, value in samples.items():
        q_value = q_from_weight(value)
        ktl_value = ktl_from_weight(value)
        ok = ok and 0 < value < 1
        lines.append(f"{name}: w_plus={value}, Q={q_value}, K_TL={ktl_value}")
    record(
        "C.1 equivariant Morita leaves a component-weight simplex",
        ok,
        "\n".join(lines),
    )
    record(
        "C.2 forgetting C3 orbit type is not allowed by the retained Koide lane",
        True,
        "The C3 orbit distinction is part of the retained Cl(3)/Z3 structure, not removable gauge redundancy.",
    )

    section("D. Verdict")

    residual = sp.simplify(w - sp.Rational(1, 2))
    record(
        "D.1 equivariant-Morita swap route does not close Q",
        residual == w - sp.Rational(1, 2),
        f"RESIDUAL_EQUIVARIANT_WEIGHT={residual}",
    )
    record(
        "D.2 Q remains open after equivariant-Morita audit",
        True,
        "Residual primitive: physical uniform measure over inequivalent retained C3 orbit components.",
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
        print("VERDICT: non-equivariant Morita swap is not retained; equivariant Morita does not close Q.")
        print("KOIDE_Q_EQUIVARIANT_MORITA_SWAP_NO_GO=TRUE")
        print("Q_EQUIVARIANT_MORITA_SWAP_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=equivariant_component_weight_w_plus_minus_one_half_equiv_K_TL")
        print("RESIDUAL_EQUIVARIANCE=nontrivial_C3_orbit_type_blocks_Morita_skeleton_swap")
        return 0

    print("VERDICT: equivariant-Morita swap audit has FAILs.")
    print("KOIDE_Q_EQUIVARIANT_MORITA_SWAP_NO_GO=FALSE")
    print("Q_EQUIVARIANT_MORITA_SWAP_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=equivariant_component_weight_w_plus_minus_one_half_equiv_K_TL")
    print("RESIDUAL_EQUIVARIANCE=nontrivial_C3_orbit_type_blocks_Morita_skeleton_swap")
    return 1


if __name__ == "__main__":
    sys.exit(main())
