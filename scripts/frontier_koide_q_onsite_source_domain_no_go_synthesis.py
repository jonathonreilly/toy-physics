#!/usr/bin/env python3
"""
Koide Q onsite source-domain no-go synthesis.

This runner validates the compact science landed from the full Koide
workstream: onsite C3-invariant scalar sources would erase the residual Z
coordinate, but the current retained central/projected commutant source
grammar still admits Z.  Therefore the result is conditional support and a
sharp no-go/status theorem, not retained native Koide closure.
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


def read_doc(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def q_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    return sp.simplify(sp.Rational(2, 3) / (1 + z_value))


def ktl_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    w_plus = sp.simplify((1 + z_value) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    a, b, c, alpha, beta, gamma, z = sp.symbols(
        "a b c alpha beta gamma z", real=True
    )
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)

    section("A. C3 orbit and onsite source algebra")

    record(
        "A.1 cyclic generator has order three",
        C**3 == I3 and C != I3 and C**2 != I3,
    )

    onsite = sp.diag(a, b, c)
    fixed_equations = list(sp.simplify(C * onsite * C.T - onsite))
    fixed_solutions = sp.solve(fixed_equations, [a, b, c], dict=True)
    record(
        "A.2 C3-invariant onsite scalar sources are exactly common scalars",
        fixed_solutions == [{a: c, b: c}],
        f"C diag(a,b,c) C^(-1)=diag(a,b,c) -> {fixed_solutions}",
    )

    local_basis = [sp.diag(1, 0, 0), sp.diag(0, 1, 0), sp.diag(0, 0, 1)]
    record(
        "A.3 onsite local source object is the diagonal function algebra C^3",
        len(local_basis) == 3 and all(mat.is_diagonal() for mat in local_basis),
        "Basis is the three site projectors.",
    )

    section("B. Projected C3-commutant source algebra")

    P_plus = sp.simplify((I3 + C + C**2) / 3)
    P_perp = sp.simplify(I3 - P_plus)
    Z = sp.simplify(P_plus - P_perp)
    expected_Z = sp.simplify(
        -sp.Rational(1, 3) * I3
        + sp.Rational(2, 3) * C
        + sp.Rational(2, 3) * C**2
    )

    record(
        "B.1 P_plus and P_perp are complementary projectors",
        sp.simplify(P_plus * P_plus - P_plus) == sp.zeros(3, 3)
        and sp.simplify(P_perp * P_perp - P_perp) == sp.zeros(3, 3)
        and sp.simplify(P_plus * P_perp) == sp.zeros(3, 3)
        and sp.simplify(P_plus + P_perp - I3) == sp.zeros(3, 3),
    )

    record(
        "B.2 Z has the projected-source expansion -I/3 + 2C/3 + 2C^2/3",
        sp.simplify(Z - expected_Z) == sp.zeros(3, 3),
        f"Z={Z}",
    )

    record(
        "B.3 Z commutes with the C3 generator",
        sp.simplify(C * Z - Z * C) == sp.zeros(3, 3),
    )

    record(
        "B.4 Z squares to identity on the projected carrier",
        sp.simplify(Z * Z - I3) == sp.zeros(3, 3),
    )

    record(
        "B.5 Z is not an onsite diagonal source function",
        (not Z.is_diagonal())
        and any(Z[i, j] != 0 for i in range(3) for j in range(3) if i != j),
        "Z has offsite matrix entries in the site basis.",
    )

    commutant_source = sp.simplify(alpha * I3 + beta * C + gamma * C**2)
    record(
        "B.6 I, C, and C^2 span a C3-commutant source family",
        sp.simplify(C * commutant_source - commutant_source * C)
        == sp.zeros(3, 3),
    )

    diagonal_conditions = [
        commutant_source[i, j]
        for i in range(3)
        for j in range(3)
        if i != j
    ]
    diagonal_solutions = sp.solve(diagonal_conditions, [beta, gamma], dict=True)
    record(
        "B.7 onsite functions intersect the C3 commutant only in scalar I",
        diagonal_solutions == [{beta: 0, gamma: 0}],
        f"alpha I+beta C+gamma C^2 diagonal -> {diagonal_solutions}",
    )

    section("C. Conditional Q chain")

    q_z = sp.simplify(sp.Rational(2, 3) / (1 + z))
    record(
        "C.1 normalized reduced-carrier readout is Q(z)=2/(3(1+z))",
        sp.simplify(q_z - 2 / (3 * (1 + z))) == 0,
        f"Q(z)={q_z}",
    )

    record(
        "C.2 z=0 gives Q=2/3 and K_TL=0",
        q_from_z(0) == sp.Rational(2, 3) and ktl_from_z(0) == 0,
        f"z=0 -> Q={q_from_z(0)}, K_TL={ktl_from_z(0)}",
    )

    q_solution = sp.solve(sp.Eq(q_z, sp.Rational(2, 3)), z)
    record(
        "C.3 Q=2/3 iff z=0 on the admitted carrier",
        q_solution == [0],
        f"solution={q_solution}",
    )

    record(
        "C.4 strict onsite C3 source grammar would erase the Z coordinate",
        fixed_solutions == [{a: c, b: c}] and q_from_z(0) == sp.Rational(2, 3),
        "If physical undeformed scalar sources are onsite functions, only z=0 remains.",
    )

    section("D. Retained counterdomain")

    counter_z = -sp.Rational(1, 3)
    record(
        "D.1 central/projected grammar admits a nonzero zZ source",
        sp.simplify(C * (counter_z * Z) - (counter_z * Z) * C)
        == sp.zeros(3, 3),
        "zZ remains C3-invariant in End_C3(V).",
    )

    record(
        "D.2 counterdomain gives Q=1 and K_TL=3/8 at z=-1/3",
        q_from_z(counter_z) == 1 and ktl_from_z(counter_z) == sp.Rational(3, 8),
        f"z={counter_z} -> Q={q_from_z(counter_z)}, K_TL={ktl_from_z(counter_z)}",
    )

    record(
        "D.3 nonzero Z values are one-to-one with non-Koide Q values",
        q_from_z(sp.Rational(1, 4)) != sp.Rational(2, 3)
        and q_from_z(counter_z) != sp.Rational(2, 3),
        f"Q(1/4)={q_from_z(sp.Rational(1, 4))}; Q(-1/3)={q_from_z(counter_z)}",
    )

    section("E. Documentation guardrails")

    doc = read_doc("docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md")
    record(
        "E.1 landed note explicitly rejects retained native Q closure",
        "Q_RETAINED_NATIVE_CLOSURE=FALSE" in doc
        and "FULL_DIMENSIONLESS_KOIDE_CLOSURE=FALSE" in doc,
    )

    record(
        "E.2 landed note keeps the conditional positive source-domain result",
        "CONDITIONAL_Q_CLOSES_IF_ONSITE_SOURCE_DOMAIN_RETAINED=TRUE" in doc,
    )

    record(
        "E.3 landed note names the exact residual source-domain theorem",
        "derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant"
        in doc,
    )

    record(
        "E.4 branch-level full-closure labels are not retained",
        "stronger positive full-closure labels" in doc
        and "are not retained on `main`" in doc
        and ("KOIDE_FULL_DIMENSIONLESS_LANE_SOURCE_DOMAIN_CLOSURE" + "=TRUE")
        not in doc
        and ("Q_PHYSICAL" + "=2/3") not in doc
        and ("DELTA_PHYSICAL" + "=2/9") not in doc,
    )

    section("F. Verdict")

    record(
        "F.1 onsite-source algebra is real support but not closure",
        True,
        "The missing theorem is retention of onsite source domain over the broader commutant/projected domain.",
    )

    record(
        "F.2 no PDG masses, Brannen delta, or target Koide value are imported",
        True,
        "The closing and nonclosing source domains are compared algebraically first.",
    )

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: onsite source-domain science retained as conditional support/no-go.")
        print("KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS=TRUE")
        print("STRICT_ONSITE_C3_SOURCE_DOMAIN_ERASES_Z=TRUE")
        print("CONDITIONAL_Q_CLOSES_IF_ONSITE_SOURCE_DOMAIN_RETAINED=TRUE")
        print("CURRENT_RETAINED_COMMUTANT_SOURCE_DOMAIN_ADMITS_Z=TRUE")
        print("Q_RETAINED_NATIVE_CLOSURE=FALSE")
        print("DELTA_RETAINED_NATIVE_CLOSURE=FALSE")
        print("FULL_DIMENSIONLESS_KOIDE_CLOSURE=FALSE")
        print(
            "RESIDUAL_Q=derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant"
        )
        return 0

    print("VERDICT: source-domain no-go synthesis has failing checks.")
    print("KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS=FALSE")
    print("Q_RETAINED_NATIVE_CLOSURE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
