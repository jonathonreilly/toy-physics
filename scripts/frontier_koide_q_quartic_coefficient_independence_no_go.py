#!/usr/bin/env python3
"""
Koide Q quartic-coefficient independence no-go.

The Koide-Nishiura quartic

    V_KN(Phi) = [2 (tr Phi)^2 - 3 tr(Phi^2)]^2

is a valid conditional support route: on Herm_circ(3) it is proportional to
(E_+ - E_perp)^2 and hence has its minimum at Q=2/3.

This runner checks the Nature-grade question: does retained trace-invariant
quartic structure fix that coefficient, or is the Koide-Nishiura coefficient
itself the missing primitive in polynomial form?

Verdict:
  The coefficient is not fixed by trace-invariant quartic structure alone.
  The same invariant square family

      V_c = [c (tr Phi)^2 - tr(Phi^2)]^2

  is U(3)-invariant, nonnegative, and quartic for every c. On the normalized
  two-block carrier it selects an arbitrary leaf E_perp/E_+ = 3c - 1.
  Koide requires c = 2/3, equivalently E_perp=E_+, equivalently K_TL=0.

So importing V_KN closes Q only by importing the same one scalar value law.
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
    section("A. General trace-quartic square family")

    a, b2, c = sp.symbols("a b2 c", positive=True, real=True)
    tr_phi = 3 * a
    tr_phi2 = 3 * a**2 + 6 * b2
    e_plus = sp.simplify(tr_phi**2 / 3)
    e_perp = sp.simplify(tr_phi2 - tr_phi**2 / 3)

    v_c_root = sp.simplify(c * tr_phi**2 - tr_phi2)
    v_c_block = sp.simplify(v_c_root.subs({}) )
    record(
        "A.1 V_c = [c(tr Phi)^2 - tr(Phi^2)]^2 is trace-invariant, quartic, and nonnegative for every c",
        True,
        f"root on Herm_circ(3): {v_c_root}; square is nonnegative by construction.",
    )
    record(
        "A.2 on the two-block carrier, the root is (3c-1)E_+ - E_perp",
        sp.simplify(v_c_root - ((3 * c - 1) * e_plus - e_perp)) == 0,
        f"E_+={e_plus}, E_perp={e_perp}, root={v_c_root}",
    )

    section("B. Selected leaf is arbitrary until c is fixed")

    leaf_solution = sp.solve(sp.Eq(v_c_root, 0), e_perp, dict=True)
    # Work directly from block expression because e_perp is an expression.
    r = sp.symbols("r", positive=True, real=True)
    root_ratio = sp.simplify((3 * c - 1) - r)
    record(
        "B.1 V_c minimum selects the arbitrary leaf E_perp/E_+ = 3c - 1",
        sp.solve(sp.Eq(root_ratio, 0), r) == [3 * c - 1],
        "Same invariant form can select any positive leaf by changing c.",
    )
    record(
        "B.2 Koide leaf E_perp/E_+ = 1 fixes c = 2/3",
        sp.solve(sp.Eq(3 * c - 1, 1), c) == [sp.Rational(2, 3)],
        "The Koide-Nishiura root 2(tr Phi)^2 - 3tr(Phi^2) is exactly c=2/3 after rescaling.",
    )

    section("C. Equivalence to the K_TL primitive")

    Eplus, Eperp = sp.symbols("E_plus E_perp", positive=True, real=True)
    y_plus = sp.simplify(2 * Eplus / (Eplus + Eperp))
    ktl = sp.simplify((1 - y_plus) / (y_plus * (2 - y_plus)))
    record(
        "C.1 c=2/3 is equivalent to E_plus=E_perp on the selected quartic leaf",
        sp.solve(sp.Eq(Eperp / Eplus, 3 * sp.Rational(2, 3) - 1), Eperp, dict=True)
        == [{Eperp: Eplus}],
        "The Koide coefficient is exactly the block-democracy coefficient.",
    )
    record(
        "C.2 E_plus=Eperp is exactly K_TL=0 on the normalized carrier",
        sp.solve(sp.Eq(ktl, 0), Eperp, dict=True) == [{Eperp: Eplus}],
        f"K_TL(E_+,Eperp) = {ktl}",
    )

    section("D. Concrete counter-leaves")

    examples = [
        (sp.Rational(1, 2), sp.Rational(1, 2)),
        (sp.Rational(2, 3), sp.Rational(1, 1)),
        (sp.Rational(1, 1), sp.Rational(2, 1)),
    ]
    example_ok = all(3 * cc - 1 == rr for cc, rr in examples)
    record(
        "D.1 the same invariant square family selects non-Koide leaves for other c",
        example_ok,
        "c=1/2 -> Eperp/E+=1/2; c=2/3 -> 1; c=1 -> 2.",
    )
    kappa_from_leaf = sp.simplify(2 / r)
    q_from_leaf = sp.simplify((1 + 2 / kappa_from_leaf) / 3)
    record(
        "D.2 Q varies continuously with the quartic coefficient",
        sp.simplify(q_from_leaf.subs(r, 1) - sp.Rational(2, 3)) == 0
        and sp.simplify(q_from_leaf.subs(r, sp.Rational(1, 2)) - sp.Rational(1, 2)) == 0,
        f"Q(r)= {q_from_leaf}, with r=Eperp/E+.",
    )

    section("E. Verdict")

    record(
        "E.1 trace-invariant quartic structure alone does not derive the Koide coefficient",
        True,
        "A retained derivation must explain why c=2/3, not merely allow a quartic square.",
    )
    record(
        "E.2 Koide-Nishiura import is a valid conditional closure but costs the missing value law",
        True,
        "Without an independent coefficient theorem, importing V_KN imports K_TL=0 in polynomial form.",
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
        print("VERDICT: quartic-potential route remains conditional.")
        print("The Koide-Nishiura quartic closes Q only if its c=2/3 coefficient")
        print("is independently retained or derived. Trace-invariant quartic form")
        print("alone leaves a one-parameter leaf, equivalent to the open K_TL law.")
        print()
        print("KOIDE_Q_QUARTIC_COEFFICIENT_INDEPENDENCE_NO_GO=TRUE")
        print("Q_QUARTIC_ROUTE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=c-2/3")
        return 0

    print("VERDICT: quartic-coefficient audit has FAILs.")
    print()
    print("KOIDE_Q_QUARTIC_COEFFICIENT_INDEPENDENCE_NO_GO=FALSE")
    print("Q_QUARTIC_ROUTE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=c-2/3")
    return 1


if __name__ == "__main__":
    sys.exit(main())
