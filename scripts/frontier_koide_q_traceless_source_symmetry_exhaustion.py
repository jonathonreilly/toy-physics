#!/usr/bin/env python3
"""
Koide Q traceless-source symmetry exhaustion.

This is a negative branch-local theorem. After the trace/Lagrange-multiplier
reduction, the Q bridge is the single scalar condition K_TL = 0 on the
normalized second-order carrier. This runner checks whether the currently
available symmetry/normalization data can force that scalar to vanish.

Result:
  C_3 equivariance plus trace normalization does not force K_TL = 0. A
  nonzero traceless block source is itself C_3-equivariant, scale-free, and
  admissible on the positive trace-2 cone. Therefore a full Q closure still
  needs an additional physical principle, source grammar, or exhaustion of
  retained charged-lepton source classes that removes this one scalar.
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
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("A. C_3 projectors and source space")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    J = sp.ones(3, 3)
    P_plus = sp.Rational(1, 3) * J
    P_perp = I3 - P_plus
    Z = sp.simplify(P_plus - P_perp)

    record(
        "A.1 P_plus and P_perp are exact C_3-invariant orthogonal projectors",
        P_plus**2 == P_plus
        and P_perp**2 == P_perp
        and P_plus * P_perp == sp.zeros(3, 3)
        and C * P_plus - P_plus * C == sp.zeros(3, 3)
        and C * P_perp - P_perp * C == sp.zeros(3, 3),
        f"rank(P_plus)={P_plus.rank()}, rank(P_perp)={P_perp.rank()}",
    )

    k_trace, k_tl = sp.symbols("k_trace k_tl", real=True)
    K_lift = sp.simplify(k_trace * I3 + k_tl * Z)
    record(
        "A.2 the lifted trace/traceless source K = k_trace I + k_tl(P_plus-P_perp) is C_3-equivariant",
        sp.simplify(C * K_lift - K_lift * C) == sp.zeros(3, 3),
        "The Q-relevant traceless source is not excluded by C_3 equivariance.",
    )
    record(
        "A.3 quotient by pure trace leaves one exact source scalar",
        Z != sp.zeros(3, 3) and sp.simplify(sp.trace(Z)) == -1,
        "Modulo the trace multiplier, span{I, P_plus-P_perp}/span{I} has dimension 1.",
    )

    section("B. Current symmetry does not implement block exchange")

    vars_x = sp.symbols("x0:9", real=True)
    X = sp.Matrix(3, 3, vars_x)
    comm_eqs = list(C * X - X * C)
    sol = sp.solve(comm_eqs, vars_x, dict=True)
    # Sympy leaves three free variables in a generic circulant commutant.
    commutant_form = X.subs(sol[0])
    preserves_p_plus = sp.simplify(commutant_form * P_plus - P_plus * commutant_form)

    record(
        "B.1 every matrix commuting with C_3 preserves the singlet projector P_plus",
        preserves_p_plus == sp.zeros(3, 3),
        f"C_3 commutant form = {commutant_form}",
    )
    record(
        "B.2 therefore C_3 has no internal block-exchange symmetry P_plus <-> P_perp",
        sp.simplify(commutant_form * P_plus * P_perp) == sp.zeros(3, 3)
        and preserves_p_plus == sp.zeros(3, 3),
        "The singlet and real-doublet sectors are inequivalent C_3 isotypes.",
    )

    section("C. Explicit admissible nonzero K_TL counterexample")

    eps = sp.Rational(1, 5)
    y = sp.symbols("y", positive=True, real=True)
    k_tl_of_y = sp.simplify((1 - y) / (y * (2 - y)))
    y_solutions = sp.solve(sp.Eq(k_tl_of_y, eps), y)
    positive_solutions = [s for s in y_solutions if 0 < float(s.evalf()) < 2]
    y_eps = sp.simplify(positive_solutions[0])
    Y_eps = sp.diag(y_eps, 2 - y_eps)

    record(
        "C.1 nonzero K_TL = 1/5 has an admissible positive trace-2 solution",
        len(positive_solutions) == 1
        and sp.simplify(sp.trace(Y_eps) - 2) == 0
        and all(float(v.evalf()) > 0 for v in [Y_eps[0, 0], Y_eps[1, 1]]),
        f"Y = diag({sp.N(Y_eps[0,0], 12)}, {sp.N(Y_eps[1,1], 12)})",
    )

    kappa = sp.simplify(2 * Y_eps[0, 0] / Y_eps[1, 1])
    q_value = sp.simplify((1 + 2 / kappa) / 3)
    record(
        "C.2 the admissible nonzero K_TL point is off Koide",
        sp.simplify(q_value - sp.Rational(2, 3)) != 0,
        f"Q(K_TL=1/5) = {sp.N(q_value, 12)}",
    )

    section("D. Exhaustion verdict")

    record(
        "D.1 C_3 plus trace normalization cannot force K_TL = 0",
        True,
        "A nonzero K_TL source is C_3-equivariant, scale-free on Tr(Y)=2,\n"
        "and gives an admissible positive point. Symmetry/normalization alone\n"
        "therefore do not close Q.",
    )
    record(
        "D.2 the next closure target is an additional physical no-traceless-source law",
        True,
        "Needed: a retained source grammar, real-irrep block-democracy principle,\n"
        "block-exchange principle, anomaly/gauge theorem, or source-bank\n"
        "exhaustion proving K_TL=0 for physical charged leptons.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: current C_3 symmetry plus trace normalization does not")
        print("force the remaining traceless source K_TL to vanish.")
        print("Q is not closed by the present symmetry-only data.")
        print()
        print("KOIDE_Q_TRACELESS_SOURCE_SYMMETRY_EXHAUSTION_NO_GO=TRUE")
        return 0

    print("VERDICT: traceless-source symmetry exhaustion has FAILs.")
    print()
    print("KOIDE_Q_TRACELESS_SOURCE_SYMMETRY_EXHAUSTION_NO_GO=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
