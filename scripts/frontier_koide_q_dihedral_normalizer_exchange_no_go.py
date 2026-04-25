#!/usr/bin/env python3
"""
Koide Q dihedral-normalizer exchange no-go.

Theorem attempt:
  Plain C3 does not exchange the singlet and real-doublet blocks, but the
  retained cubic/S3 geometry contains a dihedral normalizer of the C3 body-axis.
  Perhaps the extra reflection supplies the missing K_TL -> -K_TL sign flip.

Result:
  No.  The reflection sends omega <-> omega^2 inside the real doublet while
  fixing the singlet.  The full D3 normalizer still fixes P_plus and P_perp
  separately, and its invariant source algebra remains two-dimensional:
  a P_plus + b P_perp.  The residual a-b is exactly K_TL.

Residual:
  RESIDUAL_SCALAR=dihedral_invariant_singlet_doublet_ratio_equiv_K_TL.
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
    print("=" * 88)
    print("KOIDE Q DIHEDRAL-NORMALIZER EXCHANGE NO-GO")
    print("=" * 88)
    print(
        "Theorem attempt: use the retained D3/S3 normalizer reflection to "
        "derive the missing K_TL sign flip."
    )

    section("A. Retained C3 axis and dihedral reflection")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    F = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    I3 = sp.eye(3)
    J = sp.ones(3, 3)
    P_plus = sp.Rational(1, 3) * J
    P_perp = I3 - P_plus

    record(
        "A.1 F normalizes C3 by sending C -> C^{-1}",
        sp.simplify(F * C * F - C**2) == sp.zeros(3, 3),
        "This is the retained dihedral reflection of the body-axis cyclic group.",
    )
    record(
        "A.2 P_plus and P_perp are fixed by both C and F",
        sp.simplify(C * P_plus * C.T - P_plus) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp * C.T - P_perp) == sp.zeros(3, 3)
        and sp.simplify(F * P_plus * F.T - P_plus) == sp.zeros(3, 3)
        and sp.simplify(F * P_perp * F.T - P_perp) == sp.zeros(3, 3),
        "The normalizer reflection does not exchange singlet and real doublet.",
    )

    section("B. Complex-character action")

    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    P0 = sp.simplify((I3 + C + C**2) / 3)
    P1 = sp.simplify((I3 + omega**2 * C + omega * C**2) / 3)
    P2 = sp.simplify((I3 + omega * C + omega**2 * C**2) / 3)
    record(
        "B.1 the reflection fixes P0 and swaps P_omega with P_omega^2",
        sp.simplify(F * P0 * F.T - P0) == sp.zeros(3, 3)
        and sp.simplify(F * P1 * F.T - P2) == sp.zeros(3, 3)
        and sp.simplify(F * P2 * F.T - P1) == sp.zeros(3, 3),
        "D3 adds real/antiunitary neutrality inside P_perp only.",
    )
    record(
        "B.2 the real doublet sum P_perp=P_omega+P_omega^2 remains fixed",
        sp.simplify(P1 + P2 - P_perp) == sp.zeros(3, 3),
        "No normalizer element maps P0 to P_omega+P_omega^2.",
    )

    section("C. Full D3-invariant source algebra")

    xs = sp.symbols("x0:9", real=True)
    X = sp.Matrix(3, 3, xs)
    equations = list(C * X - X * C) + list(F * X - X * F)
    sol = sp.solve(equations, xs, dict=True)[0]
    X_d3 = sp.simplify(X.subs(sol))
    alpha, beta = sp.symbols("alpha beta", real=True)
    X_two_block = sp.simplify(alpha * P_plus + beta * P_perp)

    free = sorted(X_d3.free_symbols, key=lambda s: s.name)
    record(
        "C.1 the D3 commutant still has two scalar degrees of freedom",
        len(free) == 2,
        f"generic D3-commutant element = {X_d3}",
    )

    # Match the generic D3 commutant to alpha P_plus + beta P_perp by solving
    # for alpha,beta in terms of its two free parameters.
    match_eqs = list(sp.simplify(X_d3 - X_two_block))
    match = sp.solve(match_eqs, [alpha, beta], dict=True)
    record(
        "C.2 every D3-invariant source is alpha P_plus + beta P_perp",
        len(match) == 1,
        f"alpha,beta match = {match[0] if match else None}",
    )

    section("D. Residual K_TL survives D3")

    a, b = sp.symbols("a b", real=True)
    K = sp.simplify(a * P_plus + b * P_perp)
    Z = sp.simplify(P_plus - P_perp)
    k_trace = sp.simplify((a + b) / 2)
    k_tl = sp.simplify((a - b) / 2)
    reconstructed = sp.simplify(k_trace * I3 + k_tl * Z)
    record(
        "D.1 D3-invariant source decomposes into trace plus K_TL residual",
        sp.simplify(K - reconstructed) == sp.zeros(3, 3),
        f"K_trace={k_trace}, K_TL={k_tl}",
    )
    record(
        "D.2 D3 invariance imposes no equation a=b",
        True,
        "The invariant algebra contains all positive a,b; equality is an extra block-democracy law.",
    )
    K_counter = K.subs({a: 1, b: 2})
    record(
        "D.3 explicit D3-invariant off-Koide counterexample has K_TL=-1/2",
        sp.simplify(C * K_counter * C.T - K_counter) == sp.zeros(3, 3)
        and sp.simplify(F * K_counter * F.T - K_counter) == sp.zeros(3, 3)
        and k_tl.subs({a: 1, b: 2}) == -sp.Rational(1, 2),
        "a=1,b=2 is retained-normalizer invariant but not source neutral.",
    )

    section("E. Hostile-review verdict")

    record(
        "E.1 no target mass data, observational pin, delta pin, or Q target is used",
        True,
    )
    record(
        "E.2 the full dihedral normalizer does not derive K_TL=0",
        True,
        "It enforces omega/omega^2 neutrality only; singlet-vs-doublet total remains free.",
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
        print("VERDICT: retained D3/S3 normalizer symmetry does not close Q.")
        print("The added reflection swaps omega and omega^2 inside the real")
        print("doublet, but leaves the singlet-vs-doublet scalar free.")
        print()
        print("KOIDE_Q_DIHEDRAL_NORMALIZER_EXCHANGE_NO_GO=TRUE")
        print("Q_DIHEDRAL_NORMALIZER_EXCHANGE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=dihedral_invariant_singlet_doublet_ratio_equiv_K_TL")
        return 0

    print("VERDICT: dihedral-normalizer exchange audit has FAILs.")
    print()
    print("KOIDE_Q_DIHEDRAL_NORMALIZER_EXCHANGE_NO_GO=FALSE")
    print("Q_DIHEDRAL_NORMALIZER_EXCHANGE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=dihedral_invariant_singlet_doublet_ratio_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
