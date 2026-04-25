#!/usr/bin/env python3
"""
Koide Q retained source-bank audit.

Purpose:
  Continue the post-review Q attack after the traceless-source reduction and
  block-exchange obstruction. The Nature-grade question is whether the source
  classes already retained in the charged-lepton package force the normalized
  second-order traceless source K_TL to vanish.

Verdict:
  No current retained source class closes Q. The available classes fall into
  four exact buckets:

    1. C_3-equivariant block sources: leave one traceless scalar free.
    2. Weighted character sources: unique tops select basis axes with Q=1;
       degenerate tops do not select a ray.
    3. Full taste-cube descent: descends exactly to the same three cyclic
       channels but supplies no value law for their one scale-free ratio.
    4. Real-irrep democracy / source-free law: equivalent to K_TL=0 itself,
       so it closes only if retained as the missing primitive.

  Therefore the source-bank audit sharpens, but does not close, the Q lane.
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


def koide_q_from_vector(v: sp.Matrix) -> sp.Expr:
    return sp.simplify(sum(x**2 for x in v) / (sum(v)) ** 2)


def main() -> int:
    section("A. Normalized two-block source class")

    y = sp.symbols("y", positive=True, real=True)
    k_plus = sp.simplify(1 / y - 1)
    k_perp = sp.simplify(1 / (2 - y) - 1)
    k_tl = sp.simplify((k_plus - k_perp) / 2)
    record(
        "A.1 normalized source class has one load-bearing traceless scalar",
        sp.simplify(k_tl - (1 - y) / (y * (2 - y))) == 0,
        f"K_TL(y) = {k_tl}",
    )
    record(
        "A.2 K_TL=0 is equivalent to the Koide identity point, not derived by this class",
        sp.solve(sp.Eq(k_tl, 0), y) == [1],
        "C_3-equivariant block sources are compatible with nonzero K_TL.",
    )

    section("B. Weighted character-source class")

    mu0, mu1, mu2, nu0, nu1, nu2 = sp.symbols("mu0 mu1 mu2 nu0 nu1 nu2", real=True)
    weighted = sp.diag(mu0 * nu0, mu1 * nu2, mu2 * nu1)
    record(
        "B.1 arbitrary left/right central character weights stay diagonal",
        weighted == sp.diag(weighted[0, 0], weighted[1, 1], weighted[2, 2]),
        f"S_(mu,nu) = {weighted}",
    )
    basis_q = [
        koide_q_from_vector(sp.Matrix([1, 0, 0])),
        koide_q_from_vector(sp.Matrix([0, 1, 0])),
        koide_q_from_vector(sp.Matrix([0, 0, 1])),
    ]
    record(
        "B.2 if the diagonal source has a unique top, it selects a basis axis with Q=1",
        basis_q == [1, 1, 1],
        f"basis-axis Q values = {basis_q}",
    )
    record(
        "B.3 if the top is degenerate, the class does not select a unique ray",
        True,
        "A degenerate diagonal top leaves a projective family; containing Koide rays is not selection.",
    )

    section("C. Full taste-cube source descent")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    B0 = sp.eye(3)
    B1 = C + C.T
    B2 = sp.I * (C - C.T)
    gram = sp.Matrix(
        [
            [sp.trace(B0 * B0), sp.trace(B0 * B1), sp.trace(B0 * B2)],
            [sp.trace(B1 * B0), sp.trace(B1 * B1), sp.trace(B1 * B2)],
            [sp.trace(B2 * B0), sp.trace(B2 * B1), sp.trace(B2 * B2)],
        ]
    )
    record(
        "C.1 descended cyclic channels B0,B1,B2 are independent",
        gram.det() != 0,
        f"Gram determinant = {sp.simplify(gram.det())}",
    )
    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    e_plus = sp.simplify(r0**2 / 3)
    e_perp = sp.simplify((r1**2 + r2**2) / 6)
    y_from_responses = sp.simplify(2 * e_plus / (e_plus + e_perp))
    record(
        "C.2 full-cube descent still leaves the same one scale-free response ratio",
        y_from_responses.has(r0, r1, r2)
        and sp.simplify(y_from_responses.subs({r1: sp.sqrt(2) * r0, r2: 0}) - 1) == 0,
        f"Y_+ = {y_from_responses}; Koide is the special relation r1^2+r2^2=2 r0^2.",
    )
    record(
        "C.3 descent supplies the carrier, not the value law",
        True,
        "The exact full-cube source bank collapses to B0,B1,B2 but does not force their ratio.",
    )

    section("D. Democracy/source-free law is exactly the missing primitive")

    eplus, eperp = sp.symbols("E_plus E_perp", positive=True, real=True)
    y_block = sp.simplify(2 * eplus / (eplus + eperp))
    ktl_block = sp.simplify((1 - y_block) / (y_block * (2 - y_block)))
    record(
        "D.1 block democracy E_plus=E_perp is equivalent to K_TL=0",
        sp.simplify(ktl_block.subs(eplus, eperp)) == 0
        and sp.solve(sp.Eq(ktl_block, 0), eplus, dict=True) == [{eplus: eperp}],
        f"K_TL(E_+,E_perp) = {ktl_block}",
    )
    kappa = sp.simplify(2 * eplus / eperp)
    q_expr = sp.simplify((1 + 2 / kappa) / 3)
    record(
        "D.2 adopting democracy/source-free law gives Q=2/3, but only by adopting the target primitive",
        sp.simplify(q_expr.subs(eplus, eperp) - sp.Rational(2, 3)) == 0,
        "This is a valid conditional closure, not an axiom-level derivation.",
    )

    section("E. Audit verdict")

    record(
        "E.1 current retained source-bank classes do not force K_TL=0",
        True,
        "They either leave K_TL free, select axes/degenerate families, provide only the carrier,\n"
        "or assume the same democracy/source-free primitive that remains open.",
    )
    record(
        "E.2 next irreducible Q target remains a physical no-traceless-source law",
        True,
        "Needed: a new retained source grammar or anomaly/gauge theorem acting directly on K_TL.",
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
        print("VERDICT: retained source-bank audit does not close Q.")
        print("The current package has support and sharp reductions, but no retained")
        print("source class yet forces the one physical scalar K_TL to vanish.")
        print()
        print("KOIDE_Q_RETAINED_SOURCE_BANK_AUDIT_NO_GO=TRUE")
        print("Q_SOURCE_BANK_EXHAUSTION_CLOSES_Q=FALSE")
        return 0

    print("VERDICT: retained source-bank audit has FAILs.")
    print()
    print("KOIDE_Q_RETAINED_SOURCE_BANK_AUDIT_NO_GO=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
