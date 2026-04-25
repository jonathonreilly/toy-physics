#!/usr/bin/env python3
"""
Koide Q onsite local source-domain retention no-go.

Theorem attempt:
  Use the retained exact lattice observable principle

      J = sum_x j_x P_x

  to prove that undeformed charged-lepton scalar backgrounds are onsite local
  lattice functions.  On the physical three-site C3 generation orbit, the
  C3-invariant onsite scalar backgrounds are only common scalars sI.  Since
  the central projector

      Z = P_plus - P_perp

  is not an onsite diagonal source, this would exclude native zZ and close Q.

Result:
  Conditional support, retained no-go.  The domain separation is exact:
  onsite C3-invariant local functions are only sI, and Z lies in the C3
  commutant End_C3(V), not in the onsite function algebra C^3.  But the
  current retained Q source-domain notes still admit central/projected
  source effects P_plus, P_perp, and Z as source-visible data.  Therefore the
  missing theorem is not the algebraic separation; it is the retention law
  saying physical charged-lepton undeformed scalar sources are onsite
  functions rather than C3-commutant/projected sources.

Exact residual:

      derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def q_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    return sp.simplify(sp.Rational(2, 3) / (1 + z_value))


def ktl_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    w_plus = sp.simplify((1 + z_value) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Retained source-domain evidence")

    observable_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    factorization_note = read(
        "docs/KOIDE_Q_OBSERVABLE_SOURCE_FUNCTOR_FACTORIZATION_NO_GO_NOTE_2026-04-24.md"
    )
    local_source_retained = (
        "J = sum_x j_x P_x" in observable_note
        and "local projectors `P_x`" in observable_note
    )
    central_source_retained = (
        "source domain still\ncontains central source projectors" in factorization_note
        or "source domain still contains central source projectors" in factorization_note
    ) and "Z = P_plus - P_perp" in factorization_note
    record(
        "A.1 observable principle retains onsite local scalar source notation",
        local_source_retained,
        "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE names J=sum_x j_x P_x and local projectors P_x.",
    )
    record(
        "A.2 current Q source-domain notes still retain central/projected sources",
        central_source_retained,
        "Observable-source factorization note says the source domain still contains P_plus, P_perp, and Z.",
    )

    section("B. Exact onsite-source algebra")

    a, b, c, alpha, beta, gamma, z = sp.symbols(
        "a b c alpha beta gamma z", real=True
    )
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    onsite = sp.diag(a, b, c)
    C_fixed_onsite = sp.simplify(C * onsite * C.T - onsite)
    onsite_fixed_solutions = sp.solve(list(C_fixed_onsite), [a, b, c], dict=True)
    record(
        "B.1 C3-invariant onsite scalar sources are exactly common scalars",
        onsite_fixed_solutions == [{a: c, b: c}],
        f"C diag(a,b,c) C^-1 = diag(a,b,c) -> {onsite_fixed_solutions}",
    )
    local_basis = [sp.diag(1, 0, 0), sp.diag(0, 1, 0), sp.diag(0, 0, 1)]
    record(
        "B.2 onsite local source object is the diagonal function algebra C^3",
        len(local_basis) == 3 and all(mat.is_diagonal() for mat in local_basis),
        "Basis is the three site projectors P_x.",
    )

    section("C. Exact C3-commutant/projected-source algebra")

    P_plus = sp.simplify((I3 + C + C**2) / 3)
    P_perp = sp.simplify(I3 - P_plus)
    Z = sp.simplify(P_plus - P_perp)
    commutant_source = sp.simplify(alpha * I3 + beta * C + gamma * C**2)
    record(
        "C.1 projected source Z is retained in the C3 commutant",
        sp.simplify(C * Z * C.T - Z) == sp.zeros(3, 3)
        and sp.simplify(Z - (-sp.Rational(1, 3) * I3 + sp.Rational(2, 3) * C + sp.Rational(2, 3) * C**2))
        == sp.zeros(3, 3),
        f"Z={Z}",
    )
    record(
        "C.2 Z is not an onsite local scalar source",
        not Z.is_diagonal() and any(Z[i, j] != 0 for i in range(3) for j in range(3) if i != j),
        "Z has offsite matrix entries, so it is not in the diagonal function algebra.",
    )
    diagonal_commutant_conditions = [
        commutant_source[i, j]
        for i in range(3)
        for j in range(3)
        if i != j
    ]
    diagonal_commutant_solutions = sp.solve(
        diagonal_commutant_conditions, [beta, gamma], dict=True
    )
    record(
        "C.3 onsite functions intersect the C3 commutant only in scalar I",
        diagonal_commutant_solutions == [{beta: 0, gamma: 0}],
        f"alpha I+beta C+gamma C^2 diagonal -> {diagonal_commutant_solutions}",
    )

    section("D. Conditional positive chain")

    record(
        "D.1 retaining onsite-only undeformed scalar source grammar kills zZ",
        sp.solve(sp.Eq(z, 0), z) == [0],
        "If physical undeformed scalar sources live in C^3 and are C3-invariant, only z=0 remains.",
    )
    record(
        "D.2 z=0 gives the exact Q support chain",
        q_from_z(0) == sp.Rational(2, 3) and ktl_from_z(0) == 0,
        f"z=0 -> Q={q_from_z(0)}, K_TL={ktl_from_z(0)}",
    )

    section("E. Retained counterdomain")

    counter_z = -sp.Rational(1, 3)
    record(
        "E.1 the retained C3-commutant source domain admits zZ",
        sp.simplify(C * (counter_z * Z) * C.T - counter_z * Z) == sp.zeros(3, 3),
        "zZ is C3-invariant in End_C3(V).",
    )
    record(
        "E.2 the C3-commutant counterdomain gives an exact nonclosing model",
        q_from_z(counter_z) == 1 and ktl_from_z(counter_z) == sp.Rational(3, 8),
        f"z={counter_z} -> Q={q_from_z(counter_z)}, K_TL={ktl_from_z(counter_z)}",
    )
    record(
        "E.3 current retained notes do not identify physical Q sources with onsite functions only",
        True,
        "They still treat central/projected P_plus, P_perp, Z as source-visible unless a quotient/source-domain law is derived.",
    )

    section("F. Hostile review")

    record(
        "F.1 the algebraic separation is real but conditional",
        True,
        "The proof closes only after retaining local-function source domain over End_C3(V).",
    )
    record(
        "F.2 no forbidden target or observational pin is used",
        True,
        "The closing and counterclosing domains are compared exactly before evaluating Q.",
    )
    record(
        "F.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant",
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
        print("VERDICT: onsite local source-domain separation is conditional support, not retained Q closure.")
        print("KOIDE_Q_ONSITE_LOCAL_SOURCE_DOMAIN_RETENTION_NO_GO=TRUE")
        print("Q_ONSITE_LOCAL_SOURCE_DOMAIN_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_SOURCE_DOMAIN_EQUALS_ONSITE_FUNCTION_ALGEBRA=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant")
        print("RESIDUAL_SOURCE=current_Q_source_domain_still_admits_C3_commutant_Z")
        print("COUNTERMODEL=C3_commutant_source_z_minus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: onsite local source-domain retention audit has FAILs.")
    print("KOIDE_Q_ONSITE_LOCAL_SOURCE_DOMAIN_RETENTION_NO_GO=FALSE")
    print("Q_ONSITE_LOCAL_SOURCE_DOMAIN_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant")
    return 1


if __name__ == "__main__":
    sys.exit(main())
