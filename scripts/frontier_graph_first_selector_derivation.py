#!/usr/bin/env python3
"""Graph-first selector derivation from canonical cube shifts.

This lane bypasses the old native-bivector -> KS bridge bottleneck and asks a
more direct question consistent with the graph-first axiom:

    Can the cubic taste graph itself derive the weak-axis selector?

On the 3-cube taste graph there are three canonical one-step axis-shift
operators S_i.  This script proves that the first nontrivial even invariant of
H(phi) = sum_i phi_i S_i already yields an S_3-symmetric selector potential
whose minima are the three coordinate axes with residual Z_2 stabilizer.

The result is not yet the full SU(3) theorem, but it does derive the missing
axis-selector on a genuinely graph-native surface.
"""

from __future__ import annotations

import itertools
import math
from typing import Iterable

import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
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


def build_axis_shifts() -> list[np.ndarray]:
    return [
        kron3(SX, I2, I2),
        kron3(I2, SX, I2),
        kron3(I2, I2, SX),
    ]


def cube_axis_permutation_matrix(perm: tuple[int, int, int]) -> np.ndarray:
    basis = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    index = {bits: i for i, bits in enumerate(basis)}
    mat = np.zeros((8, 8), dtype=float)
    for bits, i in index.items():
        new_bits = (bits[perm[0]], bits[perm[1]], bits[perm[2]])
        mat[index[new_bits], i] = 1.0
    return mat


def inverse_perm(perm: tuple[int, int, int]) -> tuple[int, int, int]:
    inv = [0, 0, 0]
    for i, p in enumerate(perm):
        inv[p] = i
    return tuple(inv)


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def h(phi: tuple[float, float, float], shifts: list[np.ndarray]) -> np.ndarray:
    return sum(c * op for c, op in zip(phi, shifts))


def selector_from_phi(phi: np.ndarray) -> tuple[float, np.ndarray]:
    r2 = float(np.dot(phi, phi))
    if r2 <= 0:
        raise ValueError("phi must be nonzero")
    p = (phi * phi) / r2
    f = float(sum(p[i] * p[j] for i in range(3) for j in range(i + 1, 3)))
    return f, p


def simplex_grid(step: float = 0.05) -> list[np.ndarray]:
    n = int(round(1.0 / step))
    pts = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            k = n - i - j
            pts.append(np.array([i, j, k], dtype=float) / n)
    return pts


def main() -> int:
    print("=" * 76)
    print("GRAPH-FIRST WEAK-AXIS SELECTOR DERIVATION")
    print("=" * 76)

    shifts = build_axis_shifts()

    print("\nCanonical cube shifts")
    for i, s in enumerate(shifts, start=1):
        check(f"S_{i} is Hermitian", np.allclose(s, s.conj().T, atol=1e-10))
        check(f"S_{i}^2 = I", np.allclose(s @ s, I8, atol=1e-10))
    for i in range(3):
        for j in range(i + 1, 3):
            check(
                f"[S_{i+1}, S_{j+1}] = 0",
                np.allclose(commutator(shifts[i], shifts[j]), np.zeros((8, 8)), atol=1e-10),
            )
            check(
                f"{{S_{i+1}, S_{j+1}}} = 2 S_{i+1} S_{j+1}",
                np.allclose(
                    anticommutator(shifts[i], shifts[j]),
                    2.0 * shifts[i] @ shifts[j],
                    atol=1e-10,
                ),
            )

    print("\nTriplet covariance under axis permutations")
    for perm in itertools.permutations((0, 1, 2)):
        P = cube_axis_permutation_matrix(perm)
        inv = inverse_perm(perm)
        for i in range(3):
            lhs = P @ shifts[i] @ P.T
            rhs = shifts[inv[i]]
            check(
                f"S_i transforms as triplet under {perm}",
                np.allclose(lhs, rhs, atol=1e-10),
            )

    print("\nExact quadratic and quartic formulas")
    samples = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1)]
    for phi in samples:
        H = h(phi, shifts)
        s2 = float(sum(x * x for x in phi))
        pair = float(sum(phi[i] ** 2 * phi[j] ** 2 for i in range(3) for j in range(i + 1, 3)))
        tr2 = np.trace(H @ H).real
        tr4 = np.trace(H @ H @ H @ H).real
        expected_tr2 = 8.0 * s2
        expected_tr4 = 8.0 * (s2 * s2 + 4.0 * pair)
        check(
            f"Tr H({phi})^2 = 8 |phi|^2",
            abs(tr2 - expected_tr2) < 1e-10,
            detail=f"value = {tr2:.6f}",
        )
        check(
            f"Tr H({phi})^4 = 8 (|phi|^4 + 4 pair)",
            abs(tr4 - expected_tr4) < 1e-10,
            detail=f"value = {tr4:.6f}",
        )

        selector = tr4 - (tr2 * tr2) / 8.0
        expected_selector = 32.0 * pair
        check(
            f"Selector V_sel({phi}) = 32 sum phi_i^2 phi_j^2",
            abs(selector - expected_selector) < 1e-10,
            detail=f"value = {selector:.6f}",
        )

    print("\nNormalized selector and axis simplex")
    for phi in samples:
        vec = np.array(phi, dtype=float)
        f, p = selector_from_phi(vec)
        H = h(tuple(phi), shifts)
        tr2 = np.trace(H @ H).real
        tr4 = np.trace(H @ H @ H @ H).real
        normalized = (tr4 / (tr2 * tr2)) - 1.0 / 8.0
        check(
            f"Normalized selector matches pairwise overlap for {phi}",
            abs(normalized - 0.5 * f) < 1e-10,
            detail=f"F = {f:.6f}",
        )
        check(
            f"p(phi) lies on simplex for {phi}",
            np.all(p >= -1e-12) and abs(np.sum(p) - 1.0) < 1e-12,
        )

    print("\nAxis minima and residual Z2")
    vertices = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
    ]
    for idx, v in enumerate(vertices, start=1):
        f, _ = selector_from_phi(v)
        check(f"Axis e{idx} has zero selector", abs(f) < 1e-12, detail=f"F = {f:.6f}")
        swap_other = {
            1: (0, 2, 1),
            2: (2, 1, 0),
            3: (1, 0, 2),
        }[idx]
        check(
            f"Axis e{idx} has Z2 stabilizer",
            np.allclose(v[list(swap_other)], v, atol=1e-12),
            detail=f"swap = {swap_other}",
        )

    pts = simplex_grid()
    vals = np.array([sum(p[i] * p[j] for i in range(3) for j in range(i + 1, 3)) for p in pts])
    min_val = float(vals.min())
    mins = [p for p, val in zip(pts, vals) if abs(val - min_val) < 1e-12]
    exact_vertices = all(any(np.allclose(p, v, atol=1e-12) for v in vertices) for p in mins)
    check(
        "Simplex minima are exactly the three axis vertices",
        abs(min_val) < 1e-12 and len(mins) == 3 and exact_vertices,
        detail=f"count = {len(mins)}",
    )

    axis = np.array([1.0, 0.0, 0.0])
    planar = np.array([1.0, 1.0, 0.0])
    diagonal = np.array([1.0, 1.0, 1.0])
    f_axis, _ = selector_from_phi(axis)
    f_planar, _ = selector_from_phi(planar)
    f_diag, _ = selector_from_phi(diagonal)
    check(
        "Axis < planar < diagonal",
        f_axis < f_planar < f_diag,
        detail=f"{f_axis:.6f} < {f_planar:.6f} < {f_diag:.6f}",
    )

    print("\nSUMMARY")
    print("  The canonical one-step cube shifts S_i provide a graph-first triplet.")
    print("  Their first nontrivial even invariant is the quartic selector")
    print("      V_sel(phi) = Tr H(phi)^4 - (Tr H(phi)^2)^2 / 8")
    print("                 = 32 sum_{i<j} phi_i^2 phi_j^2.")
    print("  After normalization p_i = phi_i^2 / sum phi_j^2, this becomes")
    print("      F(p) = sum_{i<j} p_i p_j = 1/2 (1 - sum_i p_i^2),")
    print("  with exactly three axis minima and residual Z2 stabilizer.")
    print("  This derives the weak-axis selector on a graph-native surface.")
    print("  The remaining step is to integrate this selected axis into the")
    print("  bounded commutant theorem without reintroducing the old bridge hole.")

    if FAIL:
        print(f"\nFAIL={FAIL}")
        return 1
    print(f"\nPASS={PASS} FAIL=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
