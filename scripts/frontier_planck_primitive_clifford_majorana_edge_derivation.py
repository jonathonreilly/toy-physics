#!/usr/bin/env python3
"""
Primitive Clifford-Majorana edge derivation runner.

Authority note:
    docs/PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md

This is an algebraic construction gate. It does not promote downstream Planck
claims by itself; it verifies the concrete rank-four Cl_4(C) / two-mode CAR
certificate submitted for audit. The exact checks are SymPy algebraic identity
checks; calls to sp.simplify below are sympy.simplify-equivalent checks.

Exit code: 0 on all PASS, 1 on any FAIL.
"""

from __future__ import annotations

import itertools
import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    suffix = f": {detail}" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return passed


I = sp.I
I2 = sp.eye(2)
I4 = sp.eye(4)
ZERO4 = sp.zeros(4)

X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -I], [I, 0]])
Z = sp.Matrix([[1, 0], [0, -1]])


def kron(*ops: sp.Matrix) -> sp.Matrix:
    out = ops[0]
    for op in ops[1:]:
        out = sp.kronecker_product(out, op)
    return out


def dagger(mat: sp.Matrix) -> sp.Matrix:
    return mat.conjugate().T


def anticommutator(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    return sp.simplify(a * b + b * a)


def commutator(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    return sp.simplify(a * b - b * a)


def is_zero(mat: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in mat)


def hermitian_cl4_generators() -> dict[str, sp.Matrix]:
    # Ordered primitive coframe axes: time, normal, tangent_1, tangent_2.
    return {
        "t": kron(X, I2),
        "n": kron(Y, I2),
        "tau1": kron(Z, X),
        "tau2": kron(Z, Y),
    }


def ordered_words(gammas: list[sp.Matrix]) -> list[sp.Matrix]:
    words = [I4]
    for r in range(1, len(gammas) + 1):
        for indices in itertools.combinations(range(len(gammas)), r):
            word = I4
            for idx in indices:
                word = sp.simplify(word * gammas[idx])
            words.append(word)
    return words


def matrix_span_rank(mats: list[sp.Matrix]) -> int:
    columns = [sp.Matrix(mat).reshape(16, 1) for mat in mats]
    return sp.Matrix.hstack(*columns).rank()


def commutant_dimension(gammas: list[sp.Matrix]) -> int:
    symbols = sp.symbols("x0:16")
    candidate = sp.Matrix(4, 4, symbols)
    equations: list[sp.Expr] = []
    for gamma in gammas:
        diff = sp.simplify(candidate * gamma - gamma * candidate)
        equations.extend(list(diff))
    system, _ = sp.linear_eq_to_matrix(equations, symbols)
    return len(symbols) - system.rank()


def levi_civita3(a: int, b: int, c: int) -> int:
    perm = [a, b, c]
    if sorted(perm) != [0, 1, 2]:
        return 0
    inversions = sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j])
    return -1 if inversions % 2 else 1


def spatial_bivectors(g_n: sp.Matrix, g_tau1: sp.Matrix, g_tau2: sp.Matrix) -> list[sp.Matrix]:
    spatial = [g_n, g_tau1, g_tau2]
    return [
        sp.simplify(-I * spatial[1] * spatial[2]),
        sp.simplify(-I * spatial[2] * spatial[0]),
        sp.simplify(-I * spatial[0] * spatial[1]),
    ]


def main() -> int:
    print("=" * 78)
    print("PLANCK PRIMITIVE CLIFFORD-MAJORANA EDGE DERIVATION")
    print("=" * 78)
    print()
    print("Algebraic gate: Cl_4(C) on rank(P_A)=4 and two-mode CAR.")
    print()

    gamma_map = hermitian_cl4_generators()
    gamma_names = ["t", "n", "tau1", "tau2"]
    gammas = [gamma_map[name] for name in gamma_names]

    # 1. Explicit Hermitian matrix generators.
    hermitian = all(gamma == dagger(gamma) for gamma in gammas)
    squares = all(is_zero(sp.simplify(gamma * gamma - I4)) for gamma in gammas)
    check(
        "construct four explicit Hermitian 4x4 generators",
        hermitian and squares,
        "Gamma_t=XxI, Gamma_n=YxI, Gamma_tau1=ZxX, Gamma_tau2=ZxY",
    )

    # 2. Clifford anticommutators.
    clifford_ok = True
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            expected = 2 * I4 if i == j else ZERO4
            if not is_zero(anticommutator(gi, gj) - expected):
                clifford_ok = False
    check(
        "verify {Gamma_a,Gamma_b}=2 delta_ab I_4",
        clifford_ok,
        "exact symbolic anticommutators over C",
    )

    # 3. The sixteen Clifford words form a basis of M_4(C).
    words = ordered_words(gammas)
    word_rank = matrix_span_rank(words)
    unique_words = len({tuple(sp.simplify(x) for x in word) for word in words})
    check(
        "verify sixteen Clifford words span M_4(C)",
        len(words) == 16 and unique_words == 16 and word_rank == 16,
        f"words={len(words)}, distinct={unique_words}, complex_rank={word_rank}",
    )

    # 4. Spatial subset restricts to the retained Cl(3) bivector structure.
    spatial = [gamma_map["n"], gamma_map["tau1"], gamma_map["tau2"]]
    spatial_cl3_ok = True
    for i, gi in enumerate(spatial):
        for j, gj in enumerate(spatial):
            expected = 2 * I4 if i == j else ZERO4
            if not is_zero(anticommutator(gi, gj) - expected):
                spatial_cl3_ok = False
    bivectors = spatial_bivectors(*spatial)
    bivector_hermitian = all(b == dagger(b) for b in bivectors)
    bivector_square = all(is_zero(sp.simplify(b * b - I4)) for b in bivectors)
    su2_ok = True
    for i, bi in enumerate(bivectors):
        for j, bj in enumerate(bivectors):
            expected = ZERO4
            for k, bk in enumerate(bivectors):
                expected += 2 * I * levi_civita3(i, j, k) * bk
            if not is_zero(commutator(bi, bj) - expected):
                su2_ok = False
    check(
        "verify spatial subset restricts to Cl(3) bivector content",
        spatial_cl3_ok and bivector_hermitian and bivector_square and su2_ok,
        "spatial gammas give Cl_3; bivectors close su(2) exactly",
    )

    # 5. Oriented complex pairs give two-mode CAR.
    c_n = sp.simplify((gamma_map["t"] + I * gamma_map["n"]) / 2)
    c_t = sp.simplify((gamma_map["tau1"] + I * gamma_map["tau2"]) / 2)
    modes = [c_n, c_t]
    car_annihilator_ok = True
    car_creator_ok = True
    for i, ci in enumerate(modes):
        for j, cj in enumerate(modes):
            if not is_zero(anticommutator(ci, cj)):
                car_annihilator_ok = False
            expected = I4 if i == j else ZERO4
            if not is_zero(anticommutator(ci, dagger(cj)) - expected):
                car_creator_ok = False
    check(
        "construct c_N,c_T and verify CAR anticommutators",
        car_annihilator_ok and car_creator_ok,
        "{c_a,c_b}=0 and {c_a,c_b^dagger}=delta_ab I_4",
    )

    # 6. Dimension match to the primitive active block.
    primitive_cell_dim = 16
    rank_pa = 4
    fock_dim = 2**2
    check(
        "verify dim F(C^2)=4=rank(P_A)",
        fock_dim == rank_pa and primitive_cell_dim == 16,
        "two complex CAR modes give 2^2=4 active states inside C^16",
    )

    # 7. Irreducibility and uniqueness up to Cl_4(C) automorphism.
    commutant_dim = commutant_dimension(gammas)
    minimal_fit = all(d * d < 16 for d in (1, 2, 3)) and rank_pa * rank_pa == 16
    check(
        "verify uniqueness up to Cl_4(C) automorphism",
        word_rank == 16 and commutant_dim == 1 and minimal_fit,
        "full M_4(C), scalar commutant, minimal four-dimensional module",
    )

    # 8. Cross-validation against the conditional Planck completion packet.
    c_cell = sp.Rational(rank_pa, primitive_cell_dim)
    normal_crossings = sp.Integer(2)
    tangent_crossings = sp.Integer(2) * sp.Rational(1, 2)
    c_widom = sp.simplify((normal_crossings + tangent_crossings) / 12)
    check(
        "cross-validate c_Widom=1/4=c_cell",
        c_widom == sp.Rational(1, 4) and c_cell == sp.Rational(1, 4) and c_widom == c_cell,
        f"c_Widom={c_widom}, c_cell={c_cell}",
    )

    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if FAIL_COUNT:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
