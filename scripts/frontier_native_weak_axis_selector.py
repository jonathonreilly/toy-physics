#!/usr/bin/env python3
"""Native weak-axis selector on the low-degree Cl(3) surface.

This script does not assume the KS factorization. It works only on the native
Cl(3) / C^8 taste surface and asks a narrower but critical question:

    Do the natural axis-labelled triplets already present in the native
    Clifford algebra furnish a same-surface S_3 -> Z_2 selector?

The answer matters for the full SU(3) paper claim. If the selector is already
latent in the low-degree native triplets, then the missing bridge theorem may
close without importing extra dynamics. If not, the required selector must live
on a genuinely larger operator surface.

What this script checks:
  1. The native low-degree Hermitian operator surface decomposes into:
       scalar I, pseudoscalar Gamma_5, vector triplet Gamma_i, and
       pseudovector triplet A_i = -i Gamma_j Gamma_k = 2 B_i.
  2. The natural triplet candidates Gamma_i and A_i each satisfy a Clifford
     anticommutation algebra.
  3. For any source H(phi) = sum_i phi_i Phi_i built from either triplet,
     one has H(phi)^2 = |phi|^2 I. Therefore every spectral or trace invariant
     of H depends only on |phi|^2, not on the direction of phi.
  4. In particular, no analytic Landau potential built only from these native
     triplets can distinguish axis, planar, or fully symmetric directions.

This does not kill the full paper. It sharpens the next theorem: the selector
must come from a larger same-surface operator (for example a nonlocal, bilocal,
or genuinely dynamical order parameter), not from the simplest native triplets.
"""

from __future__ import annotations

import itertools
import math
from typing import Iterable

import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
I8 = np.eye(8, dtype=complex)

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


def build_native_cl3() -> tuple[list[np.ndarray], np.ndarray, list[np.ndarray]]:
    """Return Gamma_i, Gamma_5, and normalized pseudovectors A_i."""
    g1 = kron3(SX, I2, I2)
    g2 = kron3(SZ, SX, I2)
    g3 = kron3(SZ, SZ, SX)
    gammas = [g1, g2, g3]
    gamma5 = 1j * g1 @ g2 @ g3
    # A_i = -i Gamma_j Gamma_k = 2 B_i; these square to I and form a second
    # native axis-labelled triplet.
    a1 = -1j * g2 @ g3
    a2 = -1j * g3 @ g1
    a3 = -1j * g1 @ g2
    axial = [a1, a2, a3]
    return gammas, gamma5, axial


def hermitian_basis_rank(mats: Iterable[np.ndarray], tol: float = 1e-10) -> int:
    vecs = np.array([m.reshape(-1) for m in mats])
    return np.linalg.matrix_rank(vecs, tol=tol)


def abstract_s3_on_native_basis() -> dict[str, np.ndarray]:
    """Representation on coeffs [I, G5, V1, V2, V3, A1, A2, A3].

    This is the abstract axis-relabeling action on the native low-degree
    Clifford basis. Under odd permutations, Gamma_5 and the pseudovector A_i
    pick up a sign. The vector Gamma_i permutes without a sign.
    """
    basis_labels = ["I", "G5", "V1", "V2", "V3", "A1", "A2", "A3"]
    index = {lab: i for i, lab in enumerate(basis_labels)}

    def rep(perm: tuple[int, int, int]) -> np.ndarray:
        mat = np.zeros((8, 8), dtype=float)
        parity = permutation_parity(perm)
        mat[index["I"], index["I"]] = 1.0
        mat[index["G5"], index["G5"]] = float(parity)
        for i in range(3):
            j = perm[i]
            mat[index[f"V{j+1}"], index[f"V{i+1}"]] = 1.0
            mat[index[f"A{j+1}"], index[f"A{i+1}"]] = float(parity)
        return mat

    reps = {}
    for perm in itertools.permutations((0, 1, 2)):
        reps["".join(str(x + 1) for x in perm)] = rep(perm)
    return reps


def permutation_parity(perm: tuple[int, int, int]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def h_from_triplet(phi: tuple[float, float, float], triplet: list[np.ndarray]) -> np.ndarray:
    return sum(c * op for c, op in zip(phi, triplet))


def fit_quartic_isotropy(triplet: list[np.ndarray]) -> tuple[np.ndarray, float]:
    """Fit Tr(H^4) = a sum phi_i^4 + b sum_{i<j} phi_i^2 phi_j^2."""
    samples = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1)]
    rows = []
    vals = []
    for phi in samples:
        h = h_from_triplet(phi, triplet)
        rows.append([
            sum(x ** 4 for x in phi),
            sum(phi[i] ** 2 * phi[j] ** 2 for i in range(3) for j in range(i + 1, 3)),
        ])
        vals.append(np.trace(h @ h @ h @ h).real)
    coeffs, _, _, _ = np.linalg.lstsq(np.array(rows, dtype=float), np.array(vals, dtype=float), rcond=None)
    resid = np.linalg.norm(np.array(rows) @ coeffs - np.array(vals))
    return coeffs, resid


def verify_triplet(name: str, triplet: list[np.ndarray]) -> None:
    print("\n" + "=" * 72)
    print(f"{name} triplet")
    print("=" * 72)

    for i in range(3):
        check(f"{name}_{i+1} is Hermitian", np.allclose(triplet[i], triplet[i].conj().T, atol=1e-10))
        check(
            f"{name}_{i+1}^2 = I",
            np.allclose(triplet[i] @ triplet[i], I8, atol=1e-10),
        )

    for i in range(3):
        for j in range(i + 1, 3):
            ac = anticommutator(triplet[i], triplet[j])
            check(
                f"{{{name}_{i+1}, {name}_{j+1}}} = 0",
                np.allclose(ac, np.zeros_like(ac), atol=1e-10),
            )

    # Consequence: H(phi)^2 = |phi|^2 I for every phi.
    samples = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1)]
    for phi in samples:
        h = h_from_triplet(phi, triplet)
        radius2 = float(sum(x * x for x in phi))
        check(
            f"H({phi})^2 = |phi|^2 I",
            np.allclose(h @ h, radius2 * I8, atol=1e-10),
            detail=f"|phi|^2 = {radius2:.1f}",
        )
        trace3 = np.trace(h @ h @ h)
        check(
            f"Tr H({phi})^3 = 0",
            abs(trace3) < 1e-10,
            detail=f"value = {trace3.real:.2e}+{trace3.imag:.2e}i",
        )
        trace4 = np.trace(h @ h @ h @ h).real
        expected4 = 8.0 * radius2 * radius2
        check(
            f"Tr H({phi})^4 = 8|phi|^4",
            abs(trace4 - expected4) < 1e-10,
            detail=f"value = {trace4:.6f}",
        )

    coeffs, resid = fit_quartic_isotropy(triplet)
    a, b = coeffs
    check(
        f"{name} quartic invariant is isotropic",
        abs(a - 8.0) < 1e-10 and abs(b - 16.0) < 1e-10 and resid < 1e-10,
        detail=f"a = {a:.6f}, b = {b:.6f}, resid = {resid:.2e}",
    )


def main() -> int:
    print("=" * 72)
    print("NATIVE WEAK-AXIS SELECTOR ON THE LOW-DEGREE Cl(3) SURFACE")
    print("=" * 72)

    gammas, gamma5, axial = build_native_cl3()

    print("\nLow-degree native basis:")
    native_basis = [I8, gamma5] + gammas + axial
    rank = hermitian_basis_rank(native_basis)
    check("Native low-degree Hermitian surface has rank 8", rank == 8, detail=f"rank = {rank}")

    reps = abstract_s3_on_native_basis()
    transposition = reps["213"]
    cycle = reps["231"]
    check("Abstract S3 action preserves the native 8D basis", transposition.shape == (8, 8) and cycle.shape == (8, 8))
    check("Transposition squares to identity", np.allclose(transposition @ transposition, np.eye(8), atol=1e-10))
    check("3-cycle has order 3", np.allclose(cycle @ cycle @ cycle, np.eye(8), atol=1e-10))

    # Orbit/rank structure of the natural basis families under axis relabeling.
    vec_orbit_rank = hermitian_basis_rank([reps[k] @ np.array([0, 0, 1, 0, 0, 0, 0, 0], dtype=float) for k in reps])
    ax_orbit_rank = hermitian_basis_rank([reps[k] @ np.array([0, 0, 0, 0, 0, 1, 0, 0], dtype=float) for k in reps])
    check("Vector family spans a 3D axis-labelled orbit", vec_orbit_rank == 3, detail=f"rank = {vec_orbit_rank}")
    check("Pseudovector family spans a 3D axis-labelled orbit", ax_orbit_rank == 3, detail=f"rank = {ax_orbit_rank}")

    verify_triplet("Gamma", gammas)
    verify_triplet("Axial", axial)

    print("\nSUMMARY")
    print("  The native low-degree Cl(3) surface contains natural axis-labelled")
    print("  triplets (Gamma_i and A_i = -i Gamma_j Gamma_k).")
    print("  However, both triplets generate only isotropic spectral invariants:")
    print("      H(phi)^2 = |phi|^2 I,  Tr H^3 = 0,  Tr H^4 = 8 |phi|^4.")
    print("  Therefore no analytic potential built only from these simplest native")
    print("  triplets can distinguish axis, planar, or symmetric directions.")
    print("  A genuine S3 -> Z2 selector must come from a larger same-surface")
    print("  operator or dynamical mechanism, not from the low-degree Clifford")
    print("  triplets alone.")

    if FAIL:
        print(f"\nFAILURES: {FAIL}")
        return 1
    print(f"\nAll {PASS} checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
