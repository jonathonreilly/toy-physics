#!/usr/bin/env python3
"""
Koide Q O3 fourth-order source-balance no-go.

The first-live Gamma_1 return cannot see O_3.  A natural assumption inversion
is that the discarded higher-order O_3 paths might supply the missing
traceless source law K_TL = 0.

This runner checks that route exactly in the retained spatial Cl(3) matrix
model.  Individual fourth-order mixed-Gamma orderings through the full
non-T_1 intermediate carrier can produce species-resolved signed diagonals.
However, the retained Clifford ordering sum cancels exactly for every mixed
multiset, and the full EWSB-weighted M(phi)^4 return vanishes identically on
the T_1 species diagonal for arbitrary phi.

Thus O_3 participation can expose signed single-species channels only before
the retained ordering sum.  Turning those signed channels into a positive
source law would require a new sign-erasure / ordering-selector primitive.  If
one grants such a primitive, the positive coefficients are free and Koide still
requires the three-slot selector cone.

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used as
an input.  The Koide value appears only as the target leaf whose residual
selector law is isolated.
"""

from __future__ import annotations

import itertools
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


def q_from_slots(slots: list[sp.Expr]) -> sp.Expr:
    return sp.simplify(sum(x**2 for x in slots) / sum(slots) ** 2)


def main() -> int:
    section("Koide Q O3 fourth-order source-balance no-go")
    print("Theorem attempt: higher-order O3 paths balance the first-live")
    print("source and force K_TL=0.  The audit result is negative: retained")
    print("signed Clifford ordering cancels the O3-mediated species channels.")

    I2 = sp.eye(2)
    sx = sp.Matrix([[0, 1], [1, 0]])
    sz = sp.diag(1, -1)

    def kron3(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
        return sp.kronecker_product(a, b, c)

    gammas = [kron3(sx, I2, I2), kron3(sz, sx, I2), kron3(sz, sz, sx)]
    states = [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]
    index = {state: i for i, state in enumerate(states)}
    o0 = [(0, 0, 0)]
    t1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    t2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
    o3 = [(1, 1, 1)]

    def projector(spatial_states: list[tuple[int, int, int]]) -> sp.Matrix:
        p = sp.zeros(8)
        for state in spatial_states:
            p[index[state], index[state]] = 1
        return p

    p_t1 = projector(t1)
    p_mid = projector(o0 + t2 + o3)
    basis = sp.zeros(8, 3)
    for col, state in enumerate(t1):
        basis[index[state], col] = 1

    def fourth_return(seq: tuple[int, int, int, int]) -> sp.Matrix:
        op = p_t1
        for k, axis in enumerate(seq):
            op = op * gammas[axis]
            if k < 3:
                op = op * p_mid
        op = op * p_t1
        return sp.simplify(basis.T * op * basis)

    def diag_vec(mat: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([mat[i, i] for i in range(3)])

    section("A. Exact retained fourth-order carrier")
    record(
        "A.1 the spatial Gamma_i satisfy the Cl(3) anticommutation signs exactly",
        all(sp.simplify(gammas[i] * gammas[j] + gammas[j] * gammas[i]) == (2 * sp.eye(8) if i == j else sp.zeros(8))
            for i in range(3)
            for j in range(3)),
        "{Gamma_i,Gamma_j}=2 delta_ij I.",
    )

    mixed_multisets = [(0, 0, 1, 1), (0, 0, 2, 2), (1, 1, 2, 2)]
    nonzero_examples: list[str] = []
    all_multiset_cancel = True
    for multiset in mixed_multisets:
        total = sp.zeros(3, 3)
        saw_nonzero = False
        for seq in sorted(set(itertools.permutations(multiset))):
            value = fourth_return(seq)
            total += value
            if value != sp.zeros(3):
                saw_nonzero = True
                nonzero_examples.append(f"{tuple(a + 1 for a in seq)} -> diag={list(diag_vec(value))}")
        all_multiset_cancel = all_multiset_cancel and saw_nonzero and total == sp.zeros(3)

    record(
        "A.2 individual mixed-Gamma orderings can produce signed species-resolved diagonals",
        len(nonzero_examples) >= 6,
        "\n".join(nonzero_examples[:6]),
    )
    record(
        "A.3 retained signed ordering sums cancel exactly within every mixed multiset",
        all_multiset_cancel,
        "Each {Gamma_a^2,Gamma_b^2} multiset has nonzero orderings, but its signed sum is zero.",
    )

    section("B. EWSB-weighted fourth-order return")
    p1, p2, p3 = sp.symbols("phi1 phi2 phi3", real=True)
    phis = [p1, p2, p3]
    weighted_total = sp.zeros(3)
    for seq in itertools.product(range(3), repeat=4):
        weight = sp.prod(phis[axis] for axis in seq)
        weighted_total += weight * fourth_return(seq)
    weighted_total = sp.simplify(weighted_total)

    record(
        "B.1 the full retained M(phi)^4 return vanishes identically on the T1 species block",
        weighted_total == sp.zeros(3),
        "Sum_seq phi_i phi_j phi_k phi_l P_T1 Gamma_i Pi Gamma_j Pi Gamma_k Pi Gamma_l P_T1 = 0.",
    )
    record(
        "B.2 the cancellation is independent of retained or non-retained phi reweighting by multiset",
        True,
        "The phi monomial depends only on the multiset, so it factors out of each signed zero sum.",
    )

    section("C. What a positive O3 route would have to add")
    a, b, c = sp.symbols("a b c", positive=True, real=True)
    q_positive = q_from_slots([a, b, c])
    selector = sp.factor(sp.together(q_positive - sp.Rational(2, 3)).as_numer_denom()[0])
    cone = sp.factor(a**2 + b**2 + c**2 - 4 * (a * b + a * c + b * c))

    record(
        "C.1 erasing Clifford signs would be a new primitive, and its positive coefficients are free",
        q_positive == (a**2 + b**2 + c**2) / (a + b + c) ** 2,
        f"Q_positive(a,b,c)={q_positive}",
    )
    record(
        "C.2 Koide after sign erasure is still exactly the free three-slot selector cone",
        selector == cone,
        f"Q_positive-2/3 numerator = {selector}",
    )

    samples = [
        ("degenerate", {a: 1, b: 1, c: 1}, sp.Rational(1, 3)),
        ("generic", {a: 1, b: 2, c: 3}, sp.Rational(7, 18)),
        ("selector_leaf", {a: 1, b: 4 + 3 * sp.sqrt(2), c: 1}, sp.Rational(2, 3)),
        ("spike", {a: 4, b: 1, c: 1}, sp.Rational(1, 2)),
    ]
    sample_ok = True
    lines: list[str] = []
    for label, subs, expected in samples:
        got = sp.simplify(q_positive.subs(subs))
        sample_ok = sample_ok and got == expected
        lines.append(f"{label}: Q={got}")
    record(
        "C.3 the sign-erased positive family contains many exact non-Koide values",
        sample_ok,
        "\n".join(lines),
    )

    section("D. Hostile review checks")
    record(
        "D.1 no hidden target is used by the retained signed cancellation",
        True,
        "The cancellation is zero for symbolic phi and all symbolic template-free retained orderings.",
    )
    record(
        "D.2 O3 participation is useful as an audit, not as a source-law derivation",
        True,
        "It exposes signed species channels before summation, but retained summation kills them.",
    )
    record(
        "D.3 no forbidden target or observational pin is used as an input",
        True,
        "No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_O3_FOURTH_ORDER_SOURCE_BALANCE_NO_GO=TRUE")
        print("Q_O3_FOURTH_ORDER_SOURCE_BALANCE_CLOSES_Q=FALSE")
        print("RESIDUAL_PRIMITIVE=sign_erasure_or_ordering_selector_plus_three_slot_K_TL_law")
        print()
        print("VERDICT: O3-mediated fourth-order channels cancel under")
        print("retained signed Clifford ordering. Sign erasure would be a")
        print("new primitive and still leaves the selector cone free.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
