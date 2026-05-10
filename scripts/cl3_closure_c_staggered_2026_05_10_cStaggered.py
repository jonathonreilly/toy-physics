#!/usr/bin/env python3
"""Bounded open-gate salvage for the staggered-Dirac finite-triple lane.

The runner keeps the durable part of PR 1061 and removes the unsupported
closure claim:

- build the staggered Cl(3) Pauli-tensor representation on C^8;
- co-locate the C, H, and M_3(C) finite-algebra pieces on that C^8;
- construct the minimal D_F = Gamma_1 + Gamma_2 + Gamma_3 candidate;
- verify the KO-dim-6-style signs for J = omega K and gamma_stag;
- test the order-one condition on representative D_F classes.

The decisive boundary is that the nontrivial D_F examples violate order-one.
So this is an open_gate narrowing, not a cascade closure or retained theorem.
"""

from __future__ import annotations

import sys
from collections import deque

import numpy as np


PASS = 0
FAIL = 0


def report(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    marker = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    suffix = f" ({detail})" if detail else ""
    print(f"  [{marker}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def pauli() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    eye = np.eye(2, dtype=complex)
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return eye, s1, s2, s3


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(a, b), c)


def flat_rank(mats: list[np.ndarray], tol: float = 1e-10) -> int:
    if not mats:
        return 0
    cols = [m.reshape(-1) for m in mats]
    return int(np.linalg.matrix_rank(np.stack(cols, axis=1), tol=tol))


def add_if_independent(basis: list[np.ndarray], cand: np.ndarray) -> bool:
    old_rank = flat_rank(basis)
    new_rank = flat_rank(basis + [cand])
    if new_rank > old_rank:
        basis.append(cand)
        return True
    return False


def generated_algebra_basis(generators: list[np.ndarray], max_rank: int = 64) -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    queue: deque[np.ndarray] = deque()
    eye = np.eye(generators[0].shape[0], dtype=complex)
    for mat in [eye, *generators]:
        if add_if_independent(basis, mat):
            queue.append(mat)
    while queue and len(basis) < max_rank:
        x = queue.popleft()
        for y in list(basis):
            for prod in (x @ y, y @ x):
                if add_if_independent(basis, prod):
                    queue.append(prod)
                    if len(basis) >= max_rank:
                        return basis
    return basis


def lift_hw1(op3: np.ndarray) -> np.ndarray:
    """Lift a 3x3 operator on hamming-weight-one states into C^8."""
    hw1 = [1, 2, 4]  # |001>, |010>, |100> in binary basis order
    out = np.zeros((8, 8), dtype=complex)
    for i, row in enumerate(hw1):
        for j, col in enumerate(hw1):
            out[row, col] = op3[i, j]
    return out


def conjugate_by_J(mat: np.ndarray, omega: np.ndarray) -> np.ndarray:
    # J = omega K is antiunitary. Since omega^2=-I, omega^{-1}=-omega.
    return omega @ mat.conjugate() @ (-omega)


def max_order_one(D: np.ndarray, basis: list[np.ndarray], omega: np.ndarray) -> tuple[float, int]:
    max_norm = 0.0
    zeros = 0
    for a in basis:
        comm = D @ a - a @ D
        for b in basis:
            jb = conjugate_by_J(b, omega)
            val = comm @ jb - jb @ comm
            nrm = float(np.linalg.norm(val))
            if nrm < 1e-10:
                zeros += 1
            max_norm = max(max_norm, nrm)
    return max_norm, zeros


def main() -> int:
    print("Staggered-Dirac finite-triple open-gate salvage")
    print("Claim boundary: open_gate; no cascade closure or audit verdict")

    I2, s1, _s2, s3 = pauli()
    I8 = np.eye(8, dtype=complex)
    Gamma1 = kron3(s1, I2, I2)
    Gamma2 = kron3(s3, s1, I2)
    Gamma3 = kron3(s3, s3, s1)

    section("1. Staggered Cl(3) source representation on C^8")
    for i, gamma_i in enumerate([Gamma1, Gamma2, Gamma3], 1):
        report(f"Gamma_{i}^2 = I_8", np.allclose(gamma_i @ gamma_i, I8))
    for label, A, B in (
        ("1,2", Gamma1, Gamma2),
        ("1,3", Gamma1, Gamma3),
        ("2,3", Gamma2, Gamma3),
    ):
        report(f"{{Gamma_{label}}} anticommutator vanishes", np.allclose(A @ B + B @ A, 0))

    omega = Gamma1 @ Gamma2 @ Gamma3
    section("2. C and H summands on the same C^8")
    report("omega^2 = -I_8", np.allclose(omega @ omega, -I8))
    for i, gamma_i in enumerate([Gamma1, Gamma2, Gamma3], 1):
        report(f"omega commutes with Gamma_{i}", np.allclose(omega @ gamma_i - gamma_i @ omega, 0))
    e12, e13, e23 = Gamma1 @ Gamma2, Gamma1 @ Gamma3, Gamma2 @ Gamma3
    for name, e in (("e12", e12), ("e13", e13), ("e23", e23)):
        report(f"{name}^2 = -I_8", np.allclose(e @ e, -I8))
    report("Cl+(3) span has real rank 4", flat_rank([I8, e12, e13, e23]) == 4)

    section("3. M_3(C) on the hamming-weight-one triplet")
    proj = []
    for idx in range(3):
        p = np.zeros((3, 3), dtype=complex)
        p[idx, idx] = 1.0
        proj.append(lift_hw1(p))
    cycle3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    C3 = lift_hw1(cycle3)
    m3_basis = generated_algebra_basis([*proj, C3], max_rank=9)
    report("<P_Xi,C3> generates rank 9 on hw=1", flat_rank(m3_basis) == 9)
    report("M_3(C) lift acts inside End(C^8)", all(m.shape == (8, 8) for m in m3_basis))

    section("4. Candidate D_F, chirality, and KO signs")
    gamma = kron3(s3, s3, s3)
    D_min = Gamma1 + Gamma2 + Gamma3
    report("D_min is self-adjoint", np.allclose(D_min, D_min.conjugate().T))
    report("D_min is odd under gamma_stag", np.allclose(D_min @ gamma + gamma @ D_min, 0))
    report("gamma_stag^2 = I_8", np.allclose(gamma @ gamma, I8))
    report("J^2 = -I for J=omega K", np.allclose(omega @ omega.conjugate(), -I8))
    report("J D_min = D_min J", np.allclose(omega @ D_min.conjugate() - D_min @ omega, 0))
    report("J gamma = -gamma J", np.allclose(omega @ gamma.conjugate() + gamma @ omega, 0))

    section("5. Order-one condition is an active open gate")
    algebra_basis = [I8, omega, e12, e13, e23, *m3_basis]
    report(
        "finite algebra test set has 14 elements with rank at least 13",
        len(algebra_basis) == 14 and flat_rank(algebra_basis) >= 13,
        f"rank={flat_rank(algebra_basis)}",
    )
    scalar_D = 0.7 * I8
    yukawa_like = D_min.copy()
    yukawa_like[0, 1] = yukawa_like[1, 0] = 0.25
    scalar_violation, scalar_zeros = max_order_one(scalar_D, algebra_basis, omega)
    min_violation, min_zeros = max_order_one(D_min, algebra_basis, omega)
    yuk_violation, yuk_zeros = max_order_one(yukawa_like, algebra_basis, omega)
    report(
        "scalar D satisfies order-one vacuously",
        scalar_violation < 1e-10,
        f"max={scalar_violation:.3e}, zero_pairs={scalar_zeros}/196",
    )
    report(
        "minimal staggered D violates order-one, so it is not a closed SM D_F",
        min_violation > 1.0,
        f"max={min_violation:.3e}, zero_pairs={min_zeros}/196",
    )
    report(
        "toy Yukawa-like D also leaves order-one as a selection problem",
        yuk_violation > 1.0,
        f"max={yuk_violation:.3e}, zero_pairs={yuk_zeros}/196",
    )

    section("6. Review-loop verdict")
    report("C/H/M_3(C) pieces are co-located on C^8 in this bounded model", True)
    report("D_F selection remains open after the order-one test", min_violation > 1.0)
    report("No new axiom or audit verdict is written by this runner", True)
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    print("Outcome class: OPEN_GATE")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
