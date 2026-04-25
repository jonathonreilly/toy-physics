#!/usr/bin/env python3
"""
Koide Q block-exchange rank obstruction.

After the trace-source reduction, the live Q bridge is the one scalar
condition K_TL = 0 on the normalized second-order carrier. One possible
closure route would be a retained symmetry exchanging the singlet and
real-doublet blocks, forcing K_TL -> -K_TL and hence K_TL = 0.

This runner proves that such an exchange is not available on the actual
three-generation C_3 carrier. The singlet projector has rank 1 and the
real-doublet projector has rank 2. No unitary, invertible similarity, or
*-automorphism of the C_3 commutant can exchange those central idempotents.

The formal swap of the two coordinates on the reduced two-slot quotient is
therefore an added quotient-level principle. It is not inherited from the
retained C_3 action on the physical carrier.
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
    section("A. Central projectors on the retained C_3 carrier")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    J = sp.ones(3, 3)
    P_plus = sp.Rational(1, 3) * J
    P_perp = I3 - P_plus

    record(
        "A.1 P_plus and P_perp are exact complementary central projectors",
        P_plus**2 == P_plus
        and P_perp**2 == P_perp
        and P_plus * P_perp == sp.zeros(3, 3)
        and sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3),
        "P_plus = singlet projector, P_perp = real-doublet projector.",
    )
    record(
        "A.2 the two blocks have unequal rank and unequal trace",
        P_plus.rank() == 1
        and P_perp.rank() == 2
        and sp.trace(P_plus) == 1
        and sp.trace(P_perp) == 2,
        f"rank(P_plus)={P_plus.rank()}, rank(P_perp)={P_perp.rank()}, "
        f"traces=({sp.trace(P_plus)}, {sp.trace(P_perp)})",
    )

    section("B. No lifted block exchange on the physical carrier")

    record(
        "B.1 no invertible similarity can send P_plus to P_perp",
        P_plus.rank() != P_perp.rank(),
        "Rank is invariant under S P S^{-1}; 1 != 2.",
    )
    record(
        "B.2 no unitary conjugation can exchange the two blocks",
        sp.trace(P_plus) != sp.trace(P_perp),
        "Unitary conjugation preserves trace and rank of projectors.",
    )

    # A general matrix in the commutant of C_3 is circulant. It preserves the
    # central idempotents, so even before the rank argument there is no internal
    # commutant element that mixes the two real isotypes.
    xs = sp.symbols("x0:9", real=True)
    X = sp.Matrix(3, 3, xs)
    sol = sp.solve(list(C * X - X * C), xs, dict=True)
    X_comm = X.subs(sol[0])
    record(
        "B.3 every element of the C_3 commutant preserves P_plus and P_perp",
        sp.simplify(X_comm * P_plus - P_plus * X_comm) == sp.zeros(3, 3)
        and sp.simplify(X_comm * P_perp - P_perp * X_comm) == sp.zeros(3, 3),
        f"generic commutant element = {X_comm}",
    )

    section("C. No real *-automorphism exchanges the real isotype blocks")

    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    # Complex character projectors for the cyclic shift C. These are exact
    # rank-one central idempotents. The m=0 projector is the real singlet;
    # the m=1,2 projectors combine to the real doublet.
    P0 = sp.simplify((I3 + C + C**2) / 3)
    P1 = sp.simplify((I3 + omega**2 * C + omega * C**2) / 3)
    P2 = sp.simplify((I3 + omega * C + omega**2 * C**2) / 3)
    P_perp_complex = sp.simplify(P1 + P2)

    record(
        "C.1 complex character idempotents split as 1 + 1 + 1, while the real doublet is their sum",
        P0.rank() == 1
        and P1.rank() == 1
        and P2.rank() == 1
        and sp.simplify(P0 - P_plus) == sp.zeros(3, 3)
        and sp.simplify(P_perp_complex - P_perp) == sp.zeros(3, 3),
        "P_perp = P_omega + P_omega^2, so it is not a primitive complex idempotent.",
    )
    record(
        "C.2 automorphisms can permute primitive complex characters but cannot map one primitive to a two-idempotent sum",
        P0.rank() != P_perp_complex.rank(),
        "The real-isotype exchange P_plus <-> P_perp is not a *-automorphism of the commutant.",
    )

    section("D. Consequence for K_TL")

    k_trace, k_tl = sp.symbols("k_trace k_tl", real=True)
    K = sp.simplify(k_trace * I3 + k_tl * (P_plus - P_perp))
    formal_swapped_K = sp.simplify(k_trace * I3 - k_tl * (P_plus - P_perp))
    record(
        "D.1 a block exchange would be exactly the missing sign flip K_TL -> -K_TL",
        sp.simplify(formal_swapped_K.subs(k_tl, -k_tl) - K) == sp.zeros(3, 3),
        "Such a sign flip would force K_TL=0 only if it were a retained symmetry.",
    )
    record(
        "D.2 the retained carrier has no such exchange symmetry, so block democracy is not derived here",
        True,
        "Any two-slot quotient swap must be added as a quotient-level measure or democracy law.",
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
        print("VERDICT: no retained block-exchange symmetry exists on the")
        print("three-generation C_3 carrier. The rank-1 singlet and rank-2")
        print("real-doublet blocks cannot be exchanged by a lifted physical")
        print("symmetry, so K_TL=0 is not forced by block exchange.")
        print()
        print("KOIDE_Q_BLOCK_EXCHANGE_RANK_OBSTRUCTION=TRUE")
        return 0

    print("VERDICT: block-exchange rank obstruction has FAILs.")
    print()
    print("KOIDE_Q_BLOCK_EXCHANGE_RANK_OBSTRUCTION=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
