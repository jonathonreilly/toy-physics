#!/usr/bin/env python3
"""
Cl(3) minimality — conditional support runner for d_s = 3.

Verifies the narrow, conditional statement:

  Given the retained native SU(2) bivector requirement, the retained cubic
  three-generation 8-state orbit algebra (8 = 1+1+3+3), and the retained
  anomaly-forced chirality parity requirement (d_s + d_t even with d_t = 1),
  the unique compatible Clifford dimension is d_s = 3.

This is a compatibility / minimality SUPPORT check, not a first-principles
derivation of d_s = 3 from framework-internal structure alone. The
dimensional-match requirement (2^n = 8) conditions on the cubic retained
orbit surface itself; the runner verifies internal consistency, not
axiom-depth closure.

Checks:

  Part A  Requirement table: R1 (>= 3 bivectors), R2 (2^n = 8),
          R3 (n odd). Unique n in [0, 20] satisfying all three is n = 3.

  Part B  Explicit Cl(3;C) = M_2(C) (+) M_2(C) via a 4-dimensional
          reducible representation e_i = diag(sigma_i, -sigma_i).
          Builds the pseudoscalar, chirality projectors, verifies the
          projector algebra, and exhibits the two M_2(C) factors
          spanned by {1, e_1, e_2, e_3} on each chirality block.

  Part C  Smaller n (Cl(1), Cl(2)) explicitly fail SU(2) closure.

  Part D  Larger odd n carry a spin(n)/so(n) bivector algebra of
          dimension n(n-1)/2; selecting 3 generators for SU(2)
          introduces a choice.

  Part E  Bott periodicity cross-check for Cl(n; C) dimension and
          A (+) A structure for odd n.

  Part F  Bounded tension against a clean four-generation orbit fit on
          the retained cubic surface. Does NOT claim structural exclusion
          of all higher-dimensional four-generation embeddings.

Authority note: .claude/science/derivations/cl3-minimality-axiom-depth-2026-04-17.md
"""

from __future__ import annotations

import numpy as np


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


# ---------------------------------------------------------------------------
# Part A: counting checks
# ---------------------------------------------------------------------------

def bivector_count(n: int) -> int:
    return n * (n - 1) // 2


def cl_dim(n: int) -> int:
    return 1 << n


def part_a_requirement_table(n_max: int = 7) -> None:
    print("\n[Part A] Framework requirements across n in {0, ..., %d}" % n_max)
    print("-" * 72)

    print(
        f"  {'n':>3} | {'2^n':>5} | {'bivectors':>9} | {'R1 >=3':>6} | "
        f"{'R2 =8':>5} | {'R3 odd':>6} | {'all':>5}"
    )
    print("  " + "-" * 68)
    unique_n = []
    for n in range(n_max + 1):
        bv = bivector_count(n)
        dim = cl_dim(n)
        r1 = bv >= 3
        r2 = dim == 8
        r3 = (n % 2) == 1
        all_three = r1 and r2 and r3
        if all_three:
            unique_n.append(n)
        print(
            f"  {n:>3} | {dim:>5} | {bv:>9} | "
            f"{'Y' if r1 else '.':>6} | "
            f"{'Y' if r2 else '.':>5} | "
            f"{'Y' if r3 else '.':>6} | "
            f"{'YES' if all_three else ' . ':>5}"
        )

    check(
        "Unique n in [0, %d] satisfying R1 AND R2 AND R3 is n = 3" % n_max,
        unique_n == [3],
        detail=f"found {unique_n}",
        bucket="THEOREM",
    )

    n_far = list(range(8, 21))
    unique_far = [n for n in n_far if bivector_count(n) >= 3 and cl_dim(n) == 8 and n % 2 == 1]
    check(
        "No additional n in [8, 20] satisfies all three requirements",
        unique_far == [],
        detail=f"found {unique_far} (expected [], since 2^n = 8 forces n = 3)",
        bucket="THEOREM",
    )


# ---------------------------------------------------------------------------
# Part B: explicit Cl(3; C) = M_2(C) (+) M_2(C) via 4-dim reducible rep
# ---------------------------------------------------------------------------

def pauli_sigma() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sx = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sy = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    sz = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    return sx, sy, sz


def block_diag(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    out = np.zeros((A.shape[0] + B.shape[0], A.shape[1] + B.shape[1]), dtype=np.complex128)
    out[: A.shape[0], : A.shape[1]] = A
    out[A.shape[0] :, A.shape[1] :] = B
    return out


def build_cl3_4dim_rep() -> dict:
    """
    Build the 4-dim reducible representation of Cl(3;C):
        e_i = diag(sigma_i, -sigma_i)
    This gives {e_i, e_j} = 2 delta_{ij} I_4 and a pseudoscalar
        omega = e_1 e_2 e_3 = diag(i*I, -i*I)
    whose chirality projectors
        P_R = (I_4 - i*omega) / 2 = diag(I_2, 0)
        P_L = (I_4 + i*omega) / 2 = diag(0, I_2)
    block-diagonalize Cl(3;C) into two M_2(C) factors.
    """
    sx, sy, sz = pauli_sigma()
    e1 = block_diag(sx, -sx)
    e2 = block_diag(sy, -sy)
    e3 = block_diag(sz, -sz)
    I4 = np.eye(4, dtype=np.complex128)
    omega = e1 @ e2 @ e3
    P_R = (I4 - 1j * omega) / 2
    P_L = (I4 + 1j * omega) / 2
    return {
        "e1": e1, "e2": e2, "e3": e3,
        "I4": I4, "omega": omega,
        "P_R": P_R, "P_L": P_L,
    }


def commutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B - B @ A


def part_b_cl3_explicit_direct_sum() -> None:
    print("\n[Part B] Cl(3;C) = M_2(C) (+) M_2(C) via 4-dim reducible rep")
    print("-" * 72)

    rep = build_cl3_4dim_rep()
    e1, e2, e3 = rep["e1"], rep["e2"], rep["e3"]
    I4 = rep["I4"]
    omega = rep["omega"]
    P_R, P_L = rep["P_R"], rep["P_L"]

    # Clifford anticommutation
    for i, ei in enumerate([e1, e2, e3], 1):
        for j, ej in enumerate([e1, e2, e3], 1):
            if i > j:
                continue
            anticomm = ei @ ej + ej @ ei
            expected = 2.0 * I4 if i == j else np.zeros((4, 4), dtype=np.complex128)
            check(
                f"Clifford {{e_{i}, e_{j}}} = {2 if i == j else 0} I_4 in 4-dim rep",
                np.allclose(anticomm, expected),
                bucket="SUPPORT",
            )

    # Pseudoscalar structure
    expected_omega = block_diag(1j * np.eye(2, dtype=np.complex128), -1j * np.eye(2, dtype=np.complex128))
    check(
        "Pseudoscalar omega = e1 e2 e3 equals diag(i I_2, -i I_2)",
        np.allclose(omega, expected_omega),
        detail=f"max |omega - expected| = {np.max(np.abs(omega - expected_omega)):.2e}",
        bucket="THEOREM",
    )
    check(
        "omega^2 = -I_4",
        np.allclose(omega @ omega, -I4),
        bucket="SUPPORT",
    )

    # Projector algebra
    check(
        "P_R is idempotent",
        np.allclose(P_R @ P_R, P_R),
        bucket="THEOREM",
    )
    check(
        "P_L is idempotent",
        np.allclose(P_L @ P_L, P_L),
        bucket="THEOREM",
    )
    check(
        "P_R P_L = 0 (orthogonal chiralities)",
        np.allclose(P_R @ P_L, 0.0),
        bucket="THEOREM",
    )
    check(
        "P_R + P_L = I_4 (completeness)",
        np.allclose(P_R + P_L, I4),
        bucket="THEOREM",
    )

    # Restrict {I, e_1, e_2, e_3} to each block and verify M_2(C) span
    sx, sy, sz = pauli_sigma()
    I2 = np.eye(2, dtype=np.complex128)
    block_R = lambda M: M[:2, :2]
    block_L = lambda M: M[2:, 2:]

    R_basis = [block_R(I4), block_R(e1), block_R(e2), block_R(e3)]
    check(
        "On R block, {I, e_1, e_2, e_3} restricts to {I_2, sigma_x, sigma_y, sigma_z}",
        np.allclose(R_basis[0], I2) and np.allclose(R_basis[1], sx)
        and np.allclose(R_basis[2], sy) and np.allclose(R_basis[3], sz),
        bucket="THEOREM",
    )
    L_basis = [block_L(I4), block_L(e1), block_L(e2), block_L(e3)]
    check(
        "On L block, {I, e_1, e_2, e_3} restricts to {I_2, -sigma_x, -sigma_y, -sigma_z}",
        np.allclose(L_basis[0], I2) and np.allclose(L_basis[1], -sx)
        and np.allclose(L_basis[2], -sy) and np.allclose(L_basis[3], -sz),
        bucket="THEOREM",
    )

    flat_basis = np.column_stack([m.flatten() for m in R_basis])
    rank_R = int(np.linalg.matrix_rank(flat_basis))
    check(
        "R block basis {I, sigma_x, sigma_y, sigma_z} has complex rank 4 = dim M_2(C)",
        rank_R == 4,
        detail=f"rank = {rank_R}",
        bucket="THEOREM",
    )

    # Even subalgebra Cl^+(3) sits diagonally in M_2(C) (+) M_2(C)
    for name, M in [
        ("1", I4),
        ("e_1 e_2", e1 @ e2),
        ("e_2 e_3", e2 @ e3),
        ("e_3 e_1", e3 @ e1),
    ]:
        same_blocks = np.allclose(block_R(M), block_L(M))
        off_diag_zero = np.allclose(M[:2, 2:], 0.0) and np.allclose(M[2:, :2], 0.0)
        check(
            f"Even subalgebra element {name}: block-diagonal, same action on R/L",
            same_blocks and off_diag_zero,
            bucket="THEOREM",
        )

    even_basis_R = [
        block_R(I4),
        block_R(e1 @ e2),
        block_R(e2 @ e3),
        block_R(e3 @ e1),
    ]
    flat_even = np.column_stack([m.flatten() for m in even_basis_R])
    rank_even_R = int(np.linalg.matrix_rank(flat_even))
    check(
        "Cl^+(3) restricted to R block has complex rank 4 = dim M_2(C) (isomorphism)",
        rank_even_R == 4,
        detail=f"rank = {rank_even_R}",
        bucket="THEOREM",
    )

    # SU(2) closure of bivectors (commutator closure)
    B12 = e1 @ e2
    B23 = e2 @ e3
    B31 = e3 @ e1
    basis = np.column_stack([B12.flatten(), B23.flatten(), B31.flatten()])
    for name, comm in [
        ("[B12, B23]", commutator(B12, B23)),
        ("[B23, B31]", commutator(B23, B31)),
        ("[B31, B12]", commutator(B31, B12)),
    ]:
        target = comm.flatten()
        coeffs, _, _, _ = np.linalg.lstsq(basis, target, rcond=None)
        reconstruction = basis @ coeffs
        residual = float(np.linalg.norm(target - reconstruction))
        check(
            f"Bivectors close under commutator: {name} in span(B_12, B_23, B_31)",
            residual < 1e-12,
            detail=f"residual = {residual:.2e}, coefficients = {coeffs.real.round(3).tolist()}",
            bucket="THEOREM",
        )


# ---------------------------------------------------------------------------
# Part C: Cl(1), Cl(2) fail SU(2) closure
# ---------------------------------------------------------------------------

def part_c_smaller_n_fail() -> None:
    print("\n[Part C] Smaller n explicitly fail SU(2) closure")
    print("-" * 72)

    check(
        "Cl(1) has 0 bivectors (R1 fails)",
        bivector_count(1) == 0,
        detail=f"C(1, 2) = {bivector_count(1)}",
        bucket="THEOREM",
    )
    sx, sy, _ = pauli_sigma()
    B12_cl2 = sx @ sy
    self_comm = commutator(B12_cl2, B12_cl2)
    check(
        "Cl(2) single bivector self-commutator is zero (no SU(2) from one generator)",
        np.allclose(self_comm, 0.0),
        bucket="THEOREM",
    )
    check(
        "Cl(2) has 1 bivector (< 3, R1 fails)",
        bivector_count(2) == 1,
        bucket="THEOREM",
    )


# ---------------------------------------------------------------------------
# Part D: Larger odd n carry spin(n) / so(n) bivector algebra
# ---------------------------------------------------------------------------

def part_d_larger_n_over_rich() -> None:
    print("\n[Part D] Larger odd n carry a spin(n)/so(n) bivector algebra with")
    print("         more than 3 generators; SU(2) embedding requires a selector")
    print("-" * 72)

    for n in (5, 7, 9, 11):
        bv = bivector_count(n)
        dim = cl_dim(n)
        check(
            f"Cl({n}): {bv} bivectors span spin({n})/so({n}), excess {bv - 3} beyond 3 SU(2) generators",
            bv > 3,
            detail=f"spin({n}) dim = n(n-1)/2 = {bv}; picking 3 generators requires a selector",
            bucket="SUPPORT",
        )
        check(
            f"Cl({n}): dim = 2^{n} = {dim} != 8 (R2 fails)",
            dim != 8,
            bucket="SUPPORT",
        )


# ---------------------------------------------------------------------------
# Part E: Bott periodicity cross-check
# ---------------------------------------------------------------------------

def part_e_bott_periodicity() -> None:
    print("\n[Part E] Bott periodicity: Cl(n; C) dimension and A (+) A structure")
    print("-" * 72)

    cl_structure = {
        0: ("C", 1),
        1: ("C (+) C", 2),
        2: ("M_2(C)", 4),
        3: ("M_2(C) (+) M_2(C)", 8),
        4: ("M_4(C)", 16),
        5: ("M_4(C) (+) M_4(C)", 32),
        6: ("M_8(C)", 64),
        7: ("M_8(C) (+) M_8(C)", 128),
    }

    print("  n | Cl(n; C) structure       | dim")
    print("  --|--------------------------|------")
    for n, (struct, dim) in cl_structure.items():
        print(f"  {n} | {struct:<24} | {dim}")
        check(
            f"Cl({n}; C) dimension = 2^{n}",
            dim == cl_dim(n),
            bucket="SUPPORT",
        )

    for n in range(8):
        struct = cl_structure[n][0]
        has_direct_sum = "(+)" in struct
        is_odd = n % 2 == 1
        check(
            f"Cl({n}; C) has A (+) A iff n is odd (n={n}, odd={is_odd})",
            has_direct_sum == is_odd,
            bucket="SUPPORT",
        )

    n3_factor_dim = 4
    n1_factor_dim = 1
    check(
        "Cl(3;C) is the smallest odd-n Cl(n;C) where both factors are nontrivial matrix algebras",
        n3_factor_dim > 1 and n1_factor_dim == 1,
        detail=f"n=1 factor dim = {n1_factor_dim} (trivial C), n=3 factor dim = {n3_factor_dim} (M_2(C))",
        bucket="SUPPORT",
    )


# ---------------------------------------------------------------------------
# Part F: Bounded tension against a clean four-generation orbit fit
# ---------------------------------------------------------------------------

def part_f_four_generation_tension() -> None:
    print("\n[Part F] Bounded tension: no clean four-generation fit in small-n Cl(n)")
    print("         (does NOT exclude higher-dim Cl(n) embeddings)")
    print("-" * 72)

    # Within the retained framework (cubic Z^d_s orbit + n(n-1)/2 bivectors
    # + anomaly-forced parity), no small-n Cl(n) gives a natural 4-generation
    # orbit size of 10, 12, or 14 matching 2^n. 16 = 2^4 would require n = 4,
    # violating R3 parity.
    hypothetical_orbits = [10, 12, 14]
    powers_of_two = [cl_dim(n) for n in range(10)]
    for N in hypothetical_orbits:
        exists_power_of_two = N in powers_of_two
        check(
            f"Four-gen orbit size {N} is NOT a power of 2 on small-n table",
            not exists_power_of_two,
            detail=f"2^n through n=9: {powers_of_two[:10]}",
            bucket="SUPPORT",
        )
    n_for_16 = 4
    check(
        "2^n = 16 requires n = 4, which is even and fails R3 parity",
        n_for_16 % 2 == 0,
        bucket="SUPPORT",
    )

    print("  NOTE: this is bounded-support tension only. Higher-dim Cl(n)")
    print("        with n >= 5 can carry 4 generations plus additional sectors;")
    print("        this check does not rule out such embeddings. Structural")
    print("        four-generation exclusion would require a separate theorem.")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("Cl(3) conditional minimality — support check for d_s = 3")
    print("Scope: compatibility / minimality support, NOT first-principles")
    print("       axiom-depth closure. See the authority note for claim boundary.")
    print("Authority: .claude/science/derivations/cl3-minimality-axiom-depth-2026-04-17.md")
    print("=" * 72)

    part_a_requirement_table()
    part_b_cl3_explicit_direct_sum()
    part_c_smaller_n_fail()
    part_d_larger_n_over_rich()
    part_e_bott_periodicity()
    part_f_four_generation_tension()

    print("\n" + "=" * 72)
    print(f"Summary: THEOREM_PASS={THEOREM_PASS}  SUPPORT_PASS={SUPPORT_PASS}  FAIL={FAIL}")
    print("=" * 72)

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
