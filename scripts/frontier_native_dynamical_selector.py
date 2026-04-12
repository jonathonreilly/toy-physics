#!/usr/bin/env python3
"""Native dynamical selector probe.

This script attacks the remaining weak-axis problem without importing the
Kawamoto-Smit factorization or any fitted taste-breaking coefficients.

It checks two surfaces:

1. The low-degree native Clifford triplets on the retained Cl(3) surface.
   Result: isotropic invariants only. No same-surface selector.

2. A larger axis-occupancy simplex / projector-valued order-parameter surface.
   Result: the minimal S_3-symmetric purity-deficit potential
       F(p) = sum_{i<j} p_i p_j = 1/2 * (1 - sum_i p_i^2)
   has exactly three axis-selecting minima and residual Z_2 stabilizers.

The point is not that the microscopic derivation is complete. The point is
that the native low-degree operators fail cleanly, while the larger projector
surface supports the right kind of Landau-like selector potential.
"""

from __future__ import annotations

import itertools

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


def permutation_parity(perm: tuple[int, int, int]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inv += 1
    return -1 if inv % 2 else 1


def build_native_cl3() -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Build the native Cl(3) gamma and bivector triplets."""
    g1 = kron3(SX, I2, I2)
    g2 = kron3(SZ, SX, I2)
    g3 = kron3(SZ, SZ, SX)
    gammas = [g1, g2, g3]
    bivectors = [
        -1j * g2 @ g3,
        -1j * g3 @ g1,
        -1j * g1 @ g2,
    ]
    return gammas, bivectors


def h_from_triplet(phi: tuple[float, float, float], triplet: list[np.ndarray]) -> np.ndarray:
    return sum(c * op for c, op in zip(phi, triplet))


def simplex_grid(step: float = 0.1) -> list[np.ndarray]:
    """Enumerate a coarse simplex grid on p1+p2+p3=1."""
    n = int(round(1.0 / step))
    pts = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            k = n - i - j
            p = np.array([i, j, k], dtype=float) / n
            pts.append(p)
    return pts


def s3_permutations() -> list[tuple[int, int, int]]:
    return list(itertools.permutations((0, 1, 2)))


def permute_vec(v: np.ndarray, perm: tuple[int, int, int]) -> np.ndarray:
    return v[list(perm)]


def axis_potential(p: np.ndarray) -> float:
    """Purity-deficit / pairwise-overlap potential on the simplex."""
    return float(np.sum([p[i] * p[j] for i in range(3) for j in range(i + 1, 3)]))


def projector_potential_from_triplet(phi: np.ndarray) -> float:
    """Lift a triplet order parameter to normalized occupancies and apply the
    axis-purity potential.

    For phi != 0:
        p_i = phi_i^2 / sum_j phi_j^2
        F = sum_{i<j} p_i p_j

    This is the natural larger-surface candidate: a projector-valued order
    parameter on the axis simplex.
    """
    norm2 = float(np.dot(phi, phi))
    if norm2 <= 0.0:
        raise ValueError("phi must be nonzero")
    p = (phi * phi) / norm2
    return axis_potential(p)


def low_degree_no_go(triplet: list[np.ndarray], name: str) -> None:
    print("\n" + "=" * 76)
    print(f"LOW-DEGREE NATIVE SURFACE: {name}")
    print("=" * 76)

    samples = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1)]
    for phi in samples:
        h = h_from_triplet(phi, triplet)
        r2 = float(sum(x * x for x in phi))
        check(
            f"H({phi})^2 = |phi|^2 I",
            np.allclose(h @ h, r2 * I8, atol=1e-10),
            detail=f"|phi|^2 = {r2:.1f}",
        )
        t3 = np.trace(h @ h @ h)
        t4 = np.trace(h @ h @ h @ h).real
        check(f"Tr H({phi})^3 = 0", abs(t3) < 1e-10, detail=f"value = {t3.real:.2e}")
        check(
            f"Tr H({phi})^4 = 8|phi|^4",
            abs(t4 - 8.0 * r2 * r2) < 1e-10,
            detail=f"value = {t4:.6f}",
        )

    # Fit the quartic invariant to confirm isotropy.
    basis_rows = []
    vals = []
    fit_samples = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1)]
    for phi in fit_samples:
        h = h_from_triplet(phi, triplet)
        basis_rows.append([
            sum(x**4 for x in phi),
            sum(phi[i] ** 2 * phi[j] ** 2 for i in range(3) for j in range(i + 1, 3)),
        ])
        vals.append(np.trace(h @ h @ h @ h).real)
    coeffs, *_ = np.linalg.lstsq(np.array(basis_rows, dtype=float), np.array(vals, dtype=float), rcond=None)
    resid = np.linalg.norm(np.array(basis_rows) @ coeffs - np.array(vals))
    check(
        f"{name} quartic invariant is isotropic",
        abs(coeffs[0] - 8.0) < 1e-10 and abs(coeffs[1] - 16.0) < 1e-10 and resid < 1e-10,
        detail=f"a = {coeffs[0]:.6f}, b = {coeffs[1]:.6f}, resid = {resid:.2e}",
    )


def projector_surface_theorem() -> None:
    print("\n" + "=" * 76)
    print("LARGER PROJECTOR-VALUED AXIS SURFACE")
    print("=" * 76)

    # On the axis simplex p_i >= 0, sum p_i = 1, the natural potential is the
    # purity deficit: F = sum_{i<j} p_i p_j = 1/2 (1 - sum p_i^2).
    vertices = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
    ]
    for idx, p in enumerate(vertices, start=1):
        F = axis_potential(p)
        check(f"Vertex e{idx} has zero potential", abs(F) < 1e-12, detail=f"F = {F:.6f}")
        # Stabilizer: identity and the swap of the other two axes.
        swap_other = {
            1: (0, 2, 1),
            2: (2, 1, 0),
            3: (1, 0, 2),
        }[idx]
        check(
            f"Vertex e{idx} has Z2 stabilizer",
            np.allclose(permute_vec(p, swap_other), p, atol=1e-12),
            detail=f"swap = {swap_other}",
        )

    # The potential is S3 symmetric.
    rng = np.random.default_rng(1234)
    for _ in range(25):
        x = rng.random(3)
        p = x / x.sum()
        F = axis_potential(p)
        for perm in s3_permutations():
            q = permute_vec(p, perm)
            check(
                "F(p) is S3 invariant",
                abs(axis_potential(q) - F) < 1e-12,
            )

    # Exact identity: F = 1/2 (1 - sum p_i^2).
    for _ in range(10):
        x = rng.random(3)
        p = x / x.sum()
        lhs = axis_potential(p)
        rhs = 0.5 * (1.0 - float(np.dot(p, p)))
        check("Purity-deficit identity holds", abs(lhs - rhs) < 1e-12, detail=f"lhs = {lhs:.6e}")

    # Grid search on the simplex shows the only minima are the axis vertices.
    pts = simplex_grid(step=0.05)
    vals = np.array([axis_potential(p) for p in pts])
    min_val = float(vals.min())
    mins = [p for p, v in zip(pts, vals) if abs(v - min_val) < 1e-12]
    exact_vertex_matches = all(any(np.allclose(p, v, atol=1e-12) for v in vertices) for p in mins)
    check(
        "Grid minima are exactly the three axis vertices",
        exact_vertex_matches and len(mins) == 3 and abs(min_val) < 1e-12,
        detail=f"min = {min_val:.6f}, count = {len(mins)}",
    )

    # Lift the potential to normalized occupancies derived from the native
    # triplet order parameter.
    directions = {
        "axis": np.array([1.0, 0.0, 0.0]),
        "planar": np.array([1.0, 1.0, 0.0]),
        "diagonal": np.array([1.0, 1.0, 1.0]),
    }
    axis_val = projector_potential_from_triplet(directions["axis"])
    planar_val = projector_potential_from_triplet(directions["planar"])
    diagonal_val = projector_potential_from_triplet(directions["diagonal"])
    check("Native-triple axis potential is minimal", axis_val < planar_val and axis_val < diagonal_val,
          detail=f"axis={axis_val:.6f}, planar={planar_val:.6f}, diagonal={diagonal_val:.6f}")
    check("Planar direction lies above axis", planar_val > axis_val, detail=f"planar={planar_val:.6f}")
    check("Diagonal direction lies above planar", diagonal_val > planar_val, detail=f"diagonal={diagonal_val:.6f}")

    print("\nSummary for the larger surface:")
    print("  The projector-valued axis simplex supports a minimal S3-symmetric")
    print("  selector potential F = sum_{i<j} p_i p_j = 1/2 (1 - sum p_i^2).")
    print("  It has exactly three axis vacua and residual Z2 stabilizers.")
    print("  This is the clean dynamical route that the low-degree Clifford")
    print("  surface cannot supply by itself.")


def main() -> int:
    print("=" * 76)
    print("NATIVE DYNAMICAL SELECTOR PROBE")
    print("=" * 76)
    print("Testing the native Cl(3) surface first, then a larger projector-valued axis simplex.\n")

    gammas, bivectors = build_native_cl3()

    # Confirm the native low-degree Hermitian basis is the expected 8-element span.
    native_basis = [I8] + gammas + bivectors + [1j * gammas[0] @ gammas[1] @ gammas[2]]
    rank = np.linalg.matrix_rank(np.array([m.reshape(-1) for m in native_basis]), tol=1e-10)
    check("Native low-degree Hermitian basis has rank 8", rank == 8, detail=f"rank = {rank}")

    low_degree_no_go(gammas, "Gamma triplet")
    low_degree_no_go(bivectors, "Bivector triplet")
    projector_surface_theorem()

    print("\nFINAL READ")
    print("  - Low-degree native Clifford triplets are too isotropic to select a weak axis.")
    print("  - A larger projector-valued axis simplex does support a minimal S3-symmetric")
    print("    selector potential with three axis minima and residual Z2.")
    print("  - This is an alternative route to axis selection; it does not require KS")
    print("    factorization, but it still needs a microscopic derivation if it is to")
    print("    be promoted as a first-principles theorem.")

    if FAIL:
        print(f"\nFAILURES: {FAIL}")
        return 1
    print(f"\nAll {PASS} checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
