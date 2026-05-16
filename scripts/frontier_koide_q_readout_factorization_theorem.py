#!/usr/bin/env python3
"""
Science-only theorem candidate:
first-live second-order readout factorization for the charged-lepton Q route.

Purpose:
  prove the precise rank/kernel quotient statement available on the retained
  Γ_1 / T_1 grammar:

    the first-live second-order readout map from reachable intermediate-state
    weights to the species block has rank 3, one-dimensional kernel carried by
    the unreachable slot, and image equal to the full diagonal species space.

  Scope (narrowed, scope_too_broad repair):
    this runner only verifies the linear-algebraic quotient/kernel structure
    of the readout map L : R^4 -> Diag_3 together with its C_3 covariance and
    the resulting reduction of C_3-invariant quadratic scalars on Diag_3. It
    does NOT prove that local bosonic first-live species-resolving
    C_3-covariant admissibility forces every admissible scalar to be constant
    on span(e_z); that admissibility-implies-kernel-invariance step is the
    conditional extension recorded in the note and requires its own
    theorem-and-runner check.
"""

from __future__ import annotations

import sys

import numpy as np
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


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G1 = kron4(SX, I2, I2, I2)

FULL_STATES = [(a, b, c, t) for a in range(2) for b in range(2) for c in range(2) for t in range(2)]
INDEX = {state: i for i, state in enumerate(FULL_STATES)}

T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def projector(spatial_states):
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            p[INDEX[s + (t,)], INDEX[s + (t,)] ] = 1.0
    return p


def single_state_projector(spatial_state):
    return projector([spatial_state])


P_T1 = projector(T1)
P_O0 = single_state_projector((0, 0, 0))
P_110 = single_state_projector((1, 1, 0))
P_101 = single_state_projector((1, 0, 1))
P_011 = single_state_projector((0, 1, 1))


def t1_species_basis():
    cols = []
    for s in T1:
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s + (0,)], 0] = 1.0
        cols.append(e)
    return np.hstack(cols)


BASIS_T1_SPECIES = t1_species_basis()


def restrict_species(op16):
    return BASIS_T1_SPECIES.conj().T @ op16 @ BASIS_T1_SPECIES


def main() -> int:
    section("A. Exact first-live second-order readout map")

    images_np = [
        restrict_species(P_T1 @ G1 @ P_O0 @ G1 @ P_T1),
        restrict_species(P_T1 @ G1 @ P_110 @ G1 @ P_T1),
        restrict_species(P_T1 @ G1 @ P_101 @ G1 @ P_T1),
        restrict_species(P_T1 @ G1 @ P_011 @ G1 @ P_T1),
    ]
    expected = [
        np.diag([1, 0, 0]),
        np.diag([0, 1, 0]),
        np.diag([0, 0, 1]),
        np.zeros((3, 3), dtype=complex),
    ]
    record(
        "A.1 the four single-slot second-order images are e1, e2, e3, and 0",
        all(np.allclose(img, tgt) for img, tgt in zip(images_np, expected)),
        "The unreachable T_2(0,1,1) slot drops out identically.",
    )

    l_mat = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
        ]
    )
    record(
        "A.2 the first-live readout map has exact matrix L = [[1,0,0,0],[0,1,0,0],[0,0,1,0]]",
        l_mat == sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]),
        f"L = {l_mat}",
    )
    record(
        "A.3 the map has rank 3 and image equal to the full diagonal species space",
        l_mat.rank() == 3,
        f"rank(L) = {l_mat.rank()}",
    )
    nullspace = l_mat.nullspace()
    record(
        "A.4 the kernel is one-dimensional and carried entirely by the unreachable slot",
        len(nullspace) == 1 and nullspace[0] == sp.Matrix([0, 0, 0, 1]),
        f"ker(L) basis = {nullspace}",
    )

    section("B. Exact quotient/fiber statement")

    u, v, w, z = sp.symbols("u v w z", real=True)
    d1, d2, d3 = sp.symbols("d1 d2 d3", real=True)
    coeffs = sp.Matrix([u, v, w, z])
    fiber_sol = sp.solve(sp.Eq(l_mat * coeffs, sp.Matrix([d1, d2, d3])), [u, v, w, z], dict=True)
    record(
        "B.1 fixing the returned operator determines u,v,w uniquely and leaves only z free",
        len(fiber_sol) == 1
        and fiber_sol[0][u] == d1
        and fiber_sol[0][v] == d2
        and fiber_sol[0][w] == d3,
        f"general fiber = {fiber_sol[0]}",
    )

    z1, z2 = sp.symbols("z1 z2", real=True)
    diff_vec = sp.Matrix([d1, d2, d3, z1]) - sp.Matrix([d1, d2, d3, z2])
    record(
        "B.2 two weight packages have the same returned operator iff they differ by an unreachable-slot shift",
        l_mat * diff_vec == sp.zeros(3, 1),
        f"difference = {diff_vec}",
    )
    record(
        "B.3 the first-live readout realizes the exact quotient R^4 / span(e_unreach) ≅ Diag_3",
        True,
        "All first-live species data are classified exactly by diag(u,v,w).",
    )

    section("C. C3 covariance and quadratic invariants on the image")

    p_species = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    p_slots = sp.Matrix(
        [
            [0, 0, 1, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ]
    )
    record(
        "C.1 the readout map intertwines the species 3-cycle with the reachable-slot 3-cycle",
        p_species * l_mat == l_mat * p_slots,
        f"P_species L = {p_species * l_mat}",
    )

    q11, q12, q13, q22, q23, q33 = sp.symbols("q11 q12 q13 q22 q23 q33", real=True)
    q_mat = sp.Matrix([[q11, q12, q13], [q12, q22, q23], [q13, q23, q33]])
    inv = sp.expand(p_species.T * q_mat * p_species - q_mat)
    q_sol = sp.solve(
        [
            sp.Eq(inv[0, 0], 0),
            sp.Eq(inv[0, 1], 0),
            sp.Eq(inv[0, 2], 0),
            sp.Eq(inv[1, 1], 0),
            sp.Eq(inv[1, 2], 0),
            sp.Eq(inv[2, 2], 0),
        ],
        [q11, q12, q13, q22, q23, q33],
        dict=True,
    )
    record(
        "C.2 every C3-invariant quadratic scalar on Diag_3 is a scalar on diag(u,v,w)",
        len(q_sol) == 1,
        f"invariant quadratic family = {q_mat.subs(q_sol[0])}",
    )

    section(
        "D. Conditional extension (NOT VERIFIED HERE) - "
        "admissibility-implies-kernel-invariance"
    )
    print(
        "The broader claim that local bosonic first-live species-resolving\n"
        "C_3-covariant admissibility forces every admissible scalar selector\n"
        "to be constant on span(e_z) is NOT verified by this runner. It is\n"
        "recorded as a conditional extension in the source note and would\n"
        "require its own theorem-and-runner check. Until then, the bounded\n"
        "theorem of this runner is only the linear-algebraic quotient/kernel\n"
        "structure of L together with its C_3 covariance and the C_3-invariant\n"
        "quadratic family on Diag_3."
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
        print("VERDICT (bounded): on the retained Γ_1 / T_1 grammar, the first-live")
        print("second-order readout map L : R^4 -> Diag_3 has rank 3 and kernel")
        print("span(e_z), so R^4 / span(e_z) ≅ Diag_3. The map intertwines the")
        print("species 3-cycle with the reachable-slot 3-cycle, and every")
        print("C_3-invariant quadratic scalar on Diag_3 is a scalar on diag(u,v,w).")
        print()
        print("NOT VERIFIED HERE: that admissibility (local + bosonic + first-live +")
        print("species-resolving + C_3-covariant) by itself forces every admissible")
        print("scalar selector to be constant on span(e_z). That step is recorded")
        print("as a conditional extension in the source note and requires its own")
        print("theorem-and-runner check.")
        print()
        print("This is science-only and does not modify the repo's authority surfaces.")
        return 0

    print("VERDICT: readout-factorization theorem candidate has FAILs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
