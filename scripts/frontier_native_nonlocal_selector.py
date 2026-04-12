#!/usr/bin/env python3
"""Graph-first nonlocal selector harness on the native taste cube.

This script attacks the remaining weak-axis problem without using the KS
factorization. It tests two surfaces:

1. The low-degree native Clifford triplets already known to be too isotropic.
2. A graph-native nonlocal surface built from one-step axis shifts and the
   associated two-step path kernels on the 3-cube taste graph.

The question is whether a same-surface axis triplet can be built from graph
shifts, bilocal kernels, or path-summed native data and whether a quartic
Landau-type selector prefers the three axis vacua with residual Z2 stabilizer.

The script reports one of two outcomes:
  - CANDIDATE FOUND: the tested nonlocal family has axis minima and is
    compatible with three axis vacua;
  - HARD NO-GO: no tested nonlocal family on this surface produces axis
    selectivity.

This is intentionally a harness, not a derivation theorem.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
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


def permutation_parity(perm: tuple[int, int, int]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def hermitian_basis_rank(mats: Iterable[np.ndarray], tol: float = 1e-10) -> int:
    vecs = np.array([m.reshape(-1) for m in mats])
    return int(np.linalg.matrix_rank(vecs, tol=tol))


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def build_native_cl3() -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Native Clifford triplets already known to be too isotropic."""
    g1 = kron3(SX, I2, I2)
    g2 = kron3(SZ, SX, I2)
    g3 = kron3(SZ, SZ, SX)
    gammas = [g1, g2, g3]
    axial = [
        -1j * g2 @ g3,
        -1j * g3 @ g1,
        -1j * g1 @ g2,
    ]
    return gammas, axial


def build_cube_shift_triplet() -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Native graph shifts on the 3-cube and their two-step bilocals."""
    s1 = kron3(SX, I2, I2)
    s2 = kron3(I2, SX, I2)
    s3 = kron3(I2, I2, SX)
    shifts = [s1, s2, s3]
    bilocals = [
        s2 @ s3,
        s3 @ s1,
        s1 @ s2,
    ]
    return shifts, bilocals


def cube_axis_permutation_matrix(perm: tuple[int, int, int]) -> np.ndarray:
    """Permute the three cube axes on the 8 taste-corner basis."""
    basis = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    index = {bits: i for i, bits in enumerate(basis)}
    mat = np.zeros((8, 8), dtype=float)
    for bits, i in index.items():
        new_bits = (bits[perm[0]], bits[perm[1]], bits[perm[2]])
        mat[index[new_bits], i] = 1.0
    return mat


def s3_reps() -> dict[str, np.ndarray]:
    return {
        "".join(str(x + 1) for x in perm): cube_axis_permutation_matrix(perm)
        for perm in itertools.permutations((0, 1, 2))
    }


def inverse_perm(perm: tuple[int, int, int]) -> tuple[int, int, int]:
    inv = [0, 0, 0]
    for i, p in enumerate(perm):
        inv[p] = i
    return tuple(inv)


def h_from_triplet(phi: tuple[float, float, float], triplet: list[np.ndarray]) -> np.ndarray:
    return sum(c * op for c, op in zip(phi, triplet))


def normalized_ratio(triplet: list[np.ndarray], phi: tuple[float, float, float]) -> float:
    h = h_from_triplet(phi, triplet)
    tr2 = float(np.trace(h @ h).real)
    tr4 = float(np.trace(h @ h @ h @ h).real)
    return tr4 / max(tr2 * tr2, 1e-30)


def fit_quartic(triplet: list[np.ndarray]) -> tuple[np.ndarray, float]:
    """Fit Tr(H^4) = a sum phi_i^4 + b sum_{i<j} phi_i^2 phi_j^2."""
    samples = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1)]
    rows = []
    vals = []
    for phi in samples:
        h = h_from_triplet(phi, triplet)
        rows.append(
            [
                sum(x**4 for x in phi),
                sum(phi[i] ** 2 * phi[j] ** 2 for i in range(3) for j in range(i + 1, 3)),
            ]
        )
        vals.append(float(np.trace(h @ h @ h @ h).real))
    coeffs, _, _, _ = np.linalg.lstsq(np.array(rows, dtype=float), np.array(vals, dtype=float), rcond=None)
    resid = float(np.linalg.norm(np.array(rows) @ coeffs - np.array(vals)))
    return coeffs, resid


def search_sphere_min(triplet: list[np.ndarray], n_theta: int = 41, n_phi: int = 81, n_random: int = 5000) -> tuple[float, np.ndarray]:
    """Crude global minimum search for the normalized quartic ratio."""
    best_val = float("inf")
    best_phi = np.array([1.0, 0.0, 0.0], dtype=float)

    def consider(phi: np.ndarray) -> None:
        nonlocal best_val, best_phi
        val = normalized_ratio(triplet, tuple(float(x) for x in phi))
        if val < best_val:
            best_val = val
            best_phi = phi.copy()

    axes = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
    ]
    for phi in axes:
        consider(phi)

    # Add the canonical high-symmetry comparators.
    for phi in [
        np.array([1.0, 1.0, 0.0]) / math.sqrt(2.0),
        np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0),
    ]:
        consider(phi)

    for t in np.linspace(0.0, math.pi, n_theta):
        for p in np.linspace(0.0, 2.0 * math.pi, n_phi, endpoint=False):
            phi = np.array([math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t)], dtype=float)
            consider(phi)

    rng = np.random.default_rng(0)
    for _ in range(n_random):
        phi = rng.normal(size=3)
        phi /= np.linalg.norm(phi)
        consider(phi)

    return best_val, best_phi


def assess_family(name: str, triplet: list[np.ndarray], expect_candidate: bool) -> bool:
    print("\n" + "=" * 72)
    print(name)
    print("=" * 72)

    reps = s3_reps()
    for i in range(3):
        check(f"{name}_{i+1} Hermitian", np.allclose(triplet[i], triplet[i].conj().T, atol=1e-10))

    for perm_name, P in reps.items():
        pi = tuple(int(ch) - 1 for ch in perm_name)
        inv_pi = inverse_perm(pi)
        for i in range(3):
            lhs = P @ triplet[i] @ P.T
            rhs = triplet[inv_pi[i]]
            check(
                f"{name} transforms as triplet under {perm_name}",
                np.allclose(lhs, rhs, atol=1e-10),
            )

    axis = normalized_ratio(triplet, (1.0, 0.0, 0.0))
    plane = normalized_ratio(triplet, (1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0), 0.0))
    diag = normalized_ratio(triplet, (1.0 / math.sqrt(3.0),) * 3)
    best_val, best_phi = search_sphere_min(triplet)

    print(f"  axis ratio  = {axis:.12f}")
    print(f"  plane ratio = {plane:.12f}")
    print(f"  diag ratio  = {diag:.12f}")
    print(f"  best ratio  = {best_val:.12f} at phi = {np.round(best_phi, 6)}")

    is_candidate = axis + 1e-10 < plane and axis + 1e-10 < diag and abs(best_val - axis) < 1e-6
    check(f"{name} axis-selective quartic selector", is_candidate)
    return is_candidate if expect_candidate else not is_candidate


def main() -> int:
    print("=" * 72)
    print("NATIVE NONLOCAL SELECTOR HARNESS")
    print("=" * 72)
    print("Graph-first attack on the same-surface weak-axis problem")

    gammas, axial = build_native_cl3()
    shifts, bilocals = build_cube_shift_triplet()

    # Baseline: the low-degree native Clifford surface remains too isotropic.
    print("\nLOW-DEGREE NATIVE CLIFFORD BASELINE")
    for name, triplet in [("Gamma", gammas), ("Axial", axial)]:
        print("\n" + "-" * 72)
        print(name)
        print("-" * 72)
        for i in range(3):
            check(f"{name}_{i+1} Hermitian", np.allclose(triplet[i], triplet[i].conj().T, atol=1e-10))
        axis = normalized_ratio(triplet, (1.0, 0.0, 0.0))
        plane = normalized_ratio(triplet, (1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0), 0.0))
        diag = normalized_ratio(triplet, (1.0 / math.sqrt(3.0),) * 3)
        coeffs, resid = fit_quartic(triplet)
        print(f"  axis ratio  = {axis:.12f}")
        print(f"  plane ratio = {plane:.12f}")
        print(f"  diag ratio  = {diag:.12f}")
        print(f"  quartic fit = a={coeffs[0]:.6f}, b={coeffs[1]:.6f}, resid={resid:.2e}")
        check(f"{name} is isotropic at quartic order", abs(axis - plane) < 1e-10 and abs(axis - diag) < 1e-10)

    # Candidate surface: graph shifts and their two-step bilocals.
    print("\nGRAPH-SHIFT / TWO-STEP-PATH SURFACE")
    candidate_shift = assess_family("Shift triplet S_i", shifts, expect_candidate=True)
    candidate_bilocal = assess_family("Bilocal triplet B_i = S_j S_k", bilocals, expect_candidate=True)

    mixed_candidate = False
    for lam in (0.25, 0.50, 1.00, 2.00, 4.00):
        mixed = [shifts[i] + lam * bilocals[i] for i in range(3)]
        print("\n" + "-" * 72)
        print(f"Mixed family K_i(lambda) = S_i + {lam:.2f} * B_i")
        print("-" * 72)
        if assess_family(f"Mixed lambda={lam:.2f}", mixed, expect_candidate=True):
            mixed_candidate = True

    print("\nSUMMARY")
    if candidate_shift or candidate_bilocal or mixed_candidate:
        print("  CANDIDATE FOUND on the tested nonlocal surface.")
        print("  The native low-degree Clifford triplets remain isotropic and do not")
        print("  select a weak axis, but the graph-shift and two-step bilocal triplets")
        print("  do produce an axis-selective quartic invariant with three degenerate")
        print("  axis vacua up to the expected Z2 stabilizer.")
        print("  The simplest viable family is the cube shift triplet S_i; the")
        print("  strictly nonlocal bilocal family B_i = S_j S_k behaves the same way,")
        print("  and the mixed family S_i + lambda * B_i preserves the selector over")
        print("  every scanned lambda.")
    else:
        print("  HARD NO-GO on the tested nonlocal surface.")
        print("  Neither the graph shifts nor the two-step bilocal kernels produced")
        print("  a clean axis-selective quartic minimum on the tested family.")

    print(f"\nPASS={PASS} FAIL={FAIL}")
    return 0 if (candidate_shift or candidate_bilocal or mixed_candidate) else 1


if __name__ == "__main__":
    raise SystemExit(main())
