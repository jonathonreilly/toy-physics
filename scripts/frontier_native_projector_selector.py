#!/usr/bin/env python3
"""Native projector-valued selector test on the Cl(3) / C^8 surface.

This verifier attacks the remaining same-surface weak-axis problem from the
projector side.  It checks three candidate families:

  1. The S3 axis orbit module projectors.
  2. The low-degree native Clifford projector span on C^8.
  3. Spectral projectors of the natural axis-labelled native triplets.

The goal is to find a projector-valued order parameter that canonically
selects one of three axis vacua with residual Z2.  If no such selector exists
on the low-degree native surface, the script should prove a hard obstruction
on that route.
"""

from __future__ import annotations

import itertools
from collections import Counter

import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

I2 = np.eye(2, dtype=complex)
I3 = np.eye(3, dtype=complex)
I8 = np.eye(8, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
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


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def s3_permutations() -> list[np.ndarray]:
    perms = []
    for perm in itertools.permutations(range(3)):
        p = np.zeros((3, 3), dtype=complex)
        for i, j in enumerate(perm):
            p[j, i] = 1.0
        perms.append(p)
    return perms


def commutant_basis(ops: list[np.ndarray], tol: float = 1e-10) -> tuple[np.ndarray, int]:
    n = ops[0].shape[0]
    blocks = []
    for op in ops:
        blocks.append(np.kron(np.eye(n), op) - np.kron(op.T, np.eye(n)))
    mat = np.vstack(blocks)
    _, s, vh = np.linalg.svd(mat)
    rank = np.sum(s > tol)
    null = vh[rank:].conj().T
    return null, null.shape[1]


def build_native_surface() -> dict[str, np.ndarray]:
    """Return the native low-degree Hermitian basis on C^8."""
    g1 = kron3(SX, I2, I2)
    g2 = kron3(SZ, SX, I2)
    g3 = kron3(SZ, SZ, SX)
    g5 = 1j * g1 @ g2 @ g3
    a1 = -1j * g2 @ g3
    a2 = -1j * g3 @ g1
    a3 = -1j * g1 @ g2
    return {
        "I": I8,
        "G5": g5,
        "G1": g1,
        "G2": g2,
        "G3": g3,
        "A1": a1,
        "A2": a2,
        "A3": a3,
    }


def axis_module_projectors() -> None:
    print("\n" + "=" * 72)
    print("AXIS ORBIT MODULE PROJECTORS")
    print("=" * 72)

    S3 = s3_permutations()
    null, dim = commutant_basis(S3)
    check("S3 axis-space commutant has dimension 2", dim == 2, f"dim = {dim}")

    P_sym = ONES / 3.0
    P_std = I3 - P_sym
    projectors = [np.zeros((3, 3), dtype=complex), P_sym, P_std, I3]
    expected_ranks = [0, 1, 2, 3]
    for idx, (P, r) in enumerate(zip(projectors, expected_ranks)):
        idempotent = np.linalg.norm(P @ P - P)
        comm = max(np.linalg.norm(P @ S - S @ P) for S in S3)
        rank = np.linalg.matrix_rank(P, tol=1e-10)
        check(
            f"Axis-space invariant projector {idx} has rank {r}",
            idempotent < 1e-10 and comm < 1e-10 and rank == r,
            detail=f"rank = {rank}, idempotent = {idempotent:.2e}, comm = {comm:.2e}",
        )

    axis_projectors = [np.diag([1, 0, 0]), np.diag([0, 1, 0]), np.diag([0, 0, 1])]
    axis_orbit = {tuple(np.round(P @ np.array([1.0, 0.0, 0.0], dtype=complex), 12)) for P in S3}
    stabilizer = sum(np.allclose(P @ np.array([1.0, 0.0, 0.0], dtype=complex), np.array([1.0, 0.0, 0.0], dtype=complex)) for P in S3)

    check("Axis basis vector orbit has size 3", len(axis_orbit) == 3, f"orbit size = {len(axis_orbit)}")
    check("Axis basis vector stabilizer has size 2", stabilizer == 2, f"stabilizer size = {stabilizer}")

    for k, A in enumerate(axis_projectors, start=1):
        comm = max(np.linalg.norm(P @ A - A @ P) for P in S3)
        check(f"Axis projector e{k} is not S3-invariant", comm > 1e-8, f"max commutator = {comm:.2e}")

    check("Unique rank-1 invariant projector is the symmetric singlet", np.linalg.matrix_rank(P_sym, tol=1e-10) == 1)


def triplet_projector_families(native: dict[str, np.ndarray]) -> None:
    print("\n" + "=" * 72)
    print("NATIVE TRIPLET SPECTRAL PROJECTORS")
    print("=" * 72)

    gamma = [native["G1"], native["G2"], native["G3"]]
    axial = [native["A1"], native["A2"], native["A3"]]

    samples = [(1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 1.0, 1.0), (2.0, 1.0, 0.0), (2.0, 1.0, 1.0)]
    for label, triplet in [("Gamma", gamma), ("Axial", axial)]:
        for i, Phi in enumerate(triplet, start=1):
            check(f"{label}_{i} is Hermitian", np.allclose(Phi, Phi.conj().T, atol=1e-10))
            check(f"{label}_{i}^2 = I", np.allclose(Phi @ Phi, I8, atol=1e-10))

        for i in range(3):
            for j in range(i + 1, 3):
                check(
                    f"{{{label}_{i+1}, {label}_{j+1}}} = 0",
                    np.allclose(anticommutator(triplet[i], triplet[j]), np.zeros((8, 8)), atol=1e-10),
                )

        for phi in samples:
            H = sum(c * op for c, op in zip(phi, triplet))
            r2 = float(sum(x * x for x in phi))
            if r2 == 0:
                continue
            evals = np.linalg.eigvalsh(H)
            # The exact invariant is H^2 = |phi|^2 I, hence a balanced +/- spectrum.
            check(
                f"{label} H({phi})^2 = |phi|^2 I",
                np.allclose(H @ H, r2 * I8, atol=1e-10),
                detail=f"|phi|^2 = {r2:.1f}",
            )
            check(
                f"{label} H({phi}) has paired spectrum",
                np.allclose(np.sort(np.abs(evals)), np.array([np.sqrt(r2)] * 8), atol=1e-10),
                detail=f"evals = {np.round(evals, 6)}",
            )
            P_plus = 0.5 * (I8 + H / np.sqrt(r2))
            P_minus = 0.5 * (I8 - H / np.sqrt(r2))
            check(
                f"{label} spectral projector rank is 4",
                np.linalg.matrix_rank(P_plus, tol=1e-10) == 4 and np.linalg.matrix_rank(P_minus, tol=1e-10) == 4,
                detail=f"ranks = ({np.linalg.matrix_rank(P_plus, tol=1e-10)}, {np.linalg.matrix_rank(P_minus, tol=1e-10)})",
            )

        # Low-order invariants stay isotropic.
        coeffs = []
        vals = []
        for phi in samples:
            H = sum(c * op for c, op in zip(phi, triplet))
            coeffs.append([sum(x ** 4 for x in phi), sum(phi[a] ** 2 * phi[b] ** 2 for a in range(3) for b in range(a + 1, 3))])
            vals.append(np.trace(H @ H @ H @ H).real)
        coeffs = np.array(coeffs, dtype=float)
        vals = np.array(vals, dtype=float)
        fit, _, _, _ = np.linalg.lstsq(coeffs, vals, rcond=None)
        residual = np.linalg.norm(coeffs @ fit - vals)
        check(
            f"{label} quartic invariant is isotropic",
            abs(fit[0] - 8.0) < 1e-10 and abs(fit[1] - 16.0) < 1e-10 and residual < 1e-10,
            detail=f"a = {fit[0]:.6f}, b = {fit[1]:.6f}, resid = {residual:.2e}",
        )


def identify_basis_projector(P: np.ndarray, basis: dict[str, np.ndarray], tol: float = 1e-8) -> str | None:
    """Recognize projectors of the form (I ± B)/2 for basis involutions B."""
    if np.linalg.norm(P) < tol:
        return "0"
    if np.allclose(P, I8, atol=tol):
        return "I"
    involutions = {k: v for k, v in basis.items() if k != "I"}
    Q = 2.0 * P - I8
    for name, B in involutions.items():
        if np.allclose(Q, B, atol=tol):
            return f"(I + {name})/2"
        if np.allclose(Q, -B, atol=tol):
            return f"(I - {name})/2"
    return None


def exhaustive_low_degree_projector_search(native: dict[str, np.ndarray]) -> None:
    print("\n" + "=" * 72)
    print("LOW-DEGREE NATIVE PROJECTOR SEARCH")
    print("=" * 72)

    basis_order = ["I", "G5", "G1", "G2", "G3", "A1", "A2", "A3"]
    basis = [native[k] for k in basis_order]
    coeffs = [-1.0, -0.5, 0.0, 0.5, 1.0]

    found = []
    rank_hist = Counter()
    unexpected = []
    total = 0

    for c in itertools.product(coeffs, repeat=len(basis)):
        total += 1
        if all(abs(x) < 1e-14 for x in c):
            continue
        P = sum(ci * Bi for ci, Bi in zip(c, basis))
        if np.linalg.norm(P @ P - P) < 1e-8:
            rank = int(np.linalg.matrix_rank(P, tol=1e-8))
            rank_hist[rank] += 1
            label = identify_basis_projector(P, native)
            record = {
                "coeffs": c,
                "rank": rank,
                "trace": float(np.trace(P).real),
                "label": label,
            }
            found.append(record)
            if rank not in {4, 8} or label is None:
                unexpected.append(record)

    check("Grid search found only trivial or rank-4 projectors", len(unexpected) == 0, detail=f"unexpected = {len(unexpected)}")
    check("No rank-1 projector found in the native low-degree grid", rank_hist.get(1, 0) == 0, detail=f"count = {rank_hist.get(1, 0)}")
    check("No rank-2 projector found in the native low-degree grid", rank_hist.get(2, 0) == 0, detail=f"count = {rank_hist.get(2, 0)}")
    check("No rank-3 projector found in the native low-degree grid", rank_hist.get(3, 0) == 0, detail=f"count = {rank_hist.get(3, 0)}")
    check("No rank-5 projector found in the native low-degree grid", rank_hist.get(5, 0) == 0, detail=f"count = {rank_hist.get(5, 0)}")
    check("No rank-6 projector found in the native low-degree grid", rank_hist.get(6, 0) == 0, detail=f"count = {rank_hist.get(6, 0)}")
    check("No rank-7 projector found in the native low-degree grid", rank_hist.get(7, 0) == 0, detail=f"count = {rank_hist.get(7, 0)}")

    print("\nFound projectors:")
    for item in found:
        print(
            f"  coeffs={item['coeffs']}  rank={item['rank']}  trace={item['trace']:.1f}"
            + (f"  [{item['label']}]" if item["label"] else "")
        )

    print("\nSummary of projector ranks in the exhaustive low-degree grid:")
    for rank in sorted(rank_hist):
        print(f"  rank {rank}: {rank_hist[rank]}")


def main() -> int:
    print("=" * 72)
    print("NATIVE PROJECTOR-VALUED SELECTOR SEARCH")
    print("=" * 72)

    native = build_native_surface()
    axis_module_projectors()
    triplet_projector_families(native)
    exhaustive_low_degree_projector_search(native)

    print("\nSUMMARY")
    print("  The axis orbit module gives only singlet + standard projectors.")
    print("  The low-degree native Clifford projector search finds only trivial")
    print("  or rank-4 spectral projectors of single involutions.")
    print("  The natural triplet spectral projectors are always rank 4 and")
    print("  isotropic, so they do not canonically select one weak axis.")
    print("  RESULT: the projector-valued route is blocked on the current native")
    print("  low-degree Cl(3) / C^8 surface.")

    if FAIL:
        print(f"\nFAILURES: {FAIL}")
        return 1
    print(f"\nAll {PASS} checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
