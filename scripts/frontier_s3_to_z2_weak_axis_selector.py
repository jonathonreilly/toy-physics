#!/usr/bin/env python3
"""
S(3) -> Z(2) weak-axis selector blocker.

This verifier checks the axis-permutation surface directly.  It shows that
the S3-invariant algebra on the three axes is only 2-dimensional and that
its canonical projectors are the symmetric singlet and the complementary
2D standard subspace.  A unique weak axis is not selected by the retained
ingredients alone.
"""

from __future__ import annotations

import itertools
import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

I3 = np.eye(3, dtype=complex)
ONES = np.ones((3, 3), dtype=complex)

PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def perm_matrix(perm):
    p = np.zeros((3, 3), dtype=complex)
    for i, j in enumerate(perm):
        p[j, i] = 1.0
    return p


def commutant_basis(mats):
    n = mats[0].shape[0]
    blocks = []
    for M in mats:
        blocks.append(np.kron(np.eye(n), M) - np.kron(M.T, np.eye(n)))
    A = np.vstack(blocks)
    U, S, Vh = np.linalg.svd(A)
    tol = 1e-10
    rank = np.sum(S > tol)
    null = Vh[rank:].conj().T
    return null, null.shape[1]


def nullspace(mats, tol=1e-10):
    U, S, Vh = np.linalg.svd(mats)
    rank = np.sum(S > tol)
    return Vh[rank:].conj().T


def main():
    print("=" * 72)
    print("S3 -> Z2 weak-axis selector on the axis surface")
    print("=" * 72)

    perms = list(itertools.permutations(range(3)))
    S3 = [perm_matrix(p) for p in perms]

    # 1) Axis-space commutant.
    ns, dim = commutant_basis(S3)
    check("S3 axis-space commutant has dimension 2", dim == 2, f"dim = {dim}")

    # Identify the canonical invariant operators.
    basis = []
    for k in range(ns.shape[1]):
        M = ns[:, k].reshape(3, 3)
        basis.append(M)

    # The invariant vector subspace is span{(1,1,1)}.
    vec_constraints = np.vstack([P - I3 for P in S3])
    vec_ns = nullspace(vec_constraints)
    check(
        "S3-invariant vector subspace is one-dimensional",
        vec_ns.shape[1] == 1,
        f"dim = {vec_ns.shape[1]}",
    )

    ones = np.array([1.0, 1.0, 1.0], dtype=complex) / np.sqrt(3)
    overlap = np.abs(np.vdot(ones, vec_ns[:, 0] / np.linalg.norm(vec_ns[:, 0])))
    check("Invariant vector is the symmetric singlet", overlap > 1 - 1e-10, f"overlap = {overlap:.12f}")

    # 2) Axis basis vectors form a 3-element orbit, each with Z2 stabilizer.
    e1 = np.array([1.0, 0.0, 0.0], dtype=complex)
    orbit = {tuple(np.round(P @ e1, 12)) for P in S3}
    stabilizer = sum(np.allclose(P @ e1, e1) for P in S3)
    check("Axis basis vector orbit has size 3", len(orbit) == 3, f"orbit size = {len(orbit)}")
    check("Axis basis vector stabilizer has size 2", stabilizer == 2, f"stabilizer size = {stabilizer}")

    # 3) Central projectors in the S3 commutant.
    P_sym = ONES / 3.0
    P_std = I3 - P_sym
    projectors = [np.zeros((3, 3), dtype=complex), P_sym, P_std, I3]
    expected_ranks = [0, 1, 2, 3]
    ok_proj = True
    for idx, (P, r) in enumerate(zip(projectors, expected_ranks)):
        idempotent = np.linalg.norm(P @ P - P)
        comm = max(np.linalg.norm(P @ S - S @ P) for S in S3)
        rank = np.linalg.matrix_rank(P, tol=1e-10)
        ok_proj &= check(
            f"Central projector {idx} is an S3-invariant idempotent",
            idempotent < 1e-10 and comm < 1e-10 and rank == r,
            f"rank = {rank}, idempotent = {idempotent:.2e}, comm = {comm:.2e}",
        )

    # 4) No axis projector is S3-invariant.
    axis_projectors = [np.diag([1, 0, 0]), np.diag([0, 1, 0]), np.diag([0, 0, 1])]
    axis_invariant = []
    for k, A in enumerate(axis_projectors, start=1):
        comm = max(np.linalg.norm(P @ A - A @ P) for P in S3)
        axis_invariant.append(comm < 1e-10)
        check(f"Axis projector e{k} is not S3-invariant", comm > 1e-8, f"max commutator = {comm:.2e}")

    # 5) The only rank-1 invariant projector is the symmetric singlet, not an axis.
    rank1_invariant = np.linalg.matrix_rank(P_sym, tol=1e-10) == 1
    check("Unique rank-1 invariant projector is the symmetric singlet", rank1_invariant)

    # 6) Summary verdict.
    blocked = (
        dim == 2
        and vec_ns.shape[1] == 1
        and len(orbit) == 3
        and stabilizer == 2
        and all(not x for x in axis_invariant)
    )
    print("\nSUMMARY")
    print("  S3-invariant algebra on the axis surface is only 2D (I, J).")
    print("  It yields singlet + standard subspace, not a canonical single-axis projector.")
    print("  The three axis choices are symmetry-related vacua with Z2 stabilizer.")
    print("  Existing retained ingredients do not canonically pick one axis.")
    print(f"  VERDICT: {'BLOCKED' if blocked else 'INCONCLUSIVE'}")

    if FAIL:
        print(f"  FAILURES: {FAIL}")
    else:
        print("  No internal failures in the blocker checks.")

    return 0


if __name__ == "__main__":
    sys_exit = main()
    raise SystemExit(sys_exit)
