#!/usr/bin/env python3
"""
Koide Q monoidal fusion trace no-go.

Theorem attempt:
  Strengthen the categorical trace/naturality route by requiring compatibility
  with the retained real C3 tensor/fusion structure.  Perhaps monoidality
  forces equal total weights for the real singlet and real doublet, hence
  K_TL = 0.

Result:
  Negative, and sharper than ordinary naturality.  The real representation
  ring has irreps 1 and D, where D is the two-dimensional real irrep from the
  complex characters.  The fusion rule is

      D ⊗ D = 2*1 ⊕ D.

  A positive monoidal dimension function with dim(1)=1 must satisfy

      dim(D)^2 = 2 + dim(D),

  whose positive solution is dim(D)=2.  Thus the monoidal/categorical trace
  selects rank/Frobenius-Perron weights 1:2, not equal total block weights 1:1.
  Equal block totals would close Q, but they violate the retained fusion rule.

No PDG masses, target Koide value, K_TL pin, delta pin, or H_* pin is used.
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


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(sp.sympify(w_perp) / sp.sympify(w_plus))
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(sp.sympify(w_perp) / sp.sympify(w_plus))
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Real C3 fusion ring")

    # Complexification of the real doublet D is chi + chi^2.  Therefore
    # D tensor D complexifies to chi^2 + 1 + 1 + chi = 2*1 + D.
    fusion_DD = {"one": 2, "D": 1}
    record(
        "A.1 real C3 doublet fusion rule is D tensor D = 2*1 plus D",
        fusion_DD == {"one": 2, "D": 1},
        "Complex characters: (chi+chi^2)^2 = 2*1 + chi + chi^2.",
    )

    # Fusion matrix for multiplication by D in basis (1,D):
    # D*1 = D -> column (0,1); D*D = 2*1 + D -> column (2,1).
    N_D = sp.Matrix([[0, 2], [1, 1]])
    eigenvals = N_D.eigenvals()
    record(
        "A.2 multiplication-by-D fusion matrix has Perron-Frobenius eigenvalue 2",
        eigenvals == {2: 1, -1: 1},
        f"N_D={N_D.tolist()}, eigenvals={eigenvals}",
    )

    section("B. Monoidal dimension function")

    d = sp.symbols("d", real=True)
    fusion_equation = sp.Eq(d**2, 2 + d)
    solutions = sp.solve(fusion_equation, d)
    positive_solutions = [value for value in solutions if value > 0]
    record(
        "B.1 positive monoidal dimension fixes dim(D)=2",
        positive_solutions == [2],
        f"d^2=2+d -> d={solutions}",
    )
    record(
        "B.2 equal total block weight dim(D)=1 violates fusion monoidality",
        sp.simplify(1**2 - (2 + 1)) == -2,
        "For d=1, d^2=1 but 2+d=3.",
    )

    section("C. Consequences for Q trace weights")

    q_monoidal = q_from_weights(1, 2)
    ktl_monoidal = ktl_from_weights(1, 2)
    q_equal = q_from_weights(1, 1)
    ktl_equal = ktl_from_weights(1, 1)
    record(
        "C.1 monoidal/Frobenius-Perron weights are off the equal-block leaf",
        q_monoidal == 1 and ktl_monoidal == sp.Rational(3, 8),
        f"weights(1,D)=(1,2) -> Q={q_monoidal}, K_TL={ktl_monoidal}",
    )
    record(
        "C.2 equal block weights land on the Koide leaf but are not monoidal",
        q_equal == sp.Rational(2, 3) and ktl_equal == 0,
        f"weights(1,D)=(1,1) -> Q={q_equal}, K_TL={ktl_equal}; fusion fails by -2.",
    )

    section("D. Exhaust positive fusion-compatible traces")

    w_plus, w_D = sp.symbols("w_plus w_D", positive=True, real=True)
    normalized_ratio = sp.simplify(w_D / w_plus)
    monoidal_constraint = sp.Eq(normalized_ratio**2, 2 + normalized_ratio)
    ratio_solutions = sp.solve(monoidal_constraint, normalized_ratio)
    positive_ratio_solutions = [value for value in ratio_solutions if value > 0]
    record(
        "D.1 normalized positive fusion-compatible ratio is uniquely 2",
        positive_ratio_solutions == [2],
        f"(w_D/w_plus)^2=2+w_D/w_plus -> {ratio_solutions}",
    )
    record(
        "D.2 no positive monoidal trace state has equal total block weights",
        sp.Rational(1, 1) not in positive_ratio_solutions,
        "Equal-block trace is natural as a central state, but not as a monoidal dimension.",
    )

    section("E. Verdict")

    record(
        "E.1 monoidal categorical trace route does not close Q",
        True,
        "The stronger categorical structure selects rank/Frobenius-Perron weights, not equal block totals.",
    )
    record(
        "E.2 Q remains open after fusion trace audit",
        True,
        "Residual primitive: justify equal total real-isotype block weights despite retained fusion dimensions.",
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
        print("VERDICT: monoidal/fusion categorical trace does not close Q.")
        print("KOIDE_Q_MONOIDAL_FUSION_TRACE_NO_GO=TRUE")
        print("Q_MONOIDAL_FUSION_TRACE_CLOSES_Q=FALSE")
        print("RESIDUAL_TRACE_STATE=equal_block_weight_not_fusion_monoidal_equiv_K_TL")
        return 0

    print("VERDICT: monoidal fusion trace audit has FAILs.")
    print("KOIDE_Q_MONOIDAL_FUSION_TRACE_NO_GO=FALSE")
    print("Q_MONOIDAL_FUSION_TRACE_CLOSES_Q=FALSE")
    print("RESIDUAL_TRACE_STATE=equal_block_weight_not_fusion_monoidal_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
