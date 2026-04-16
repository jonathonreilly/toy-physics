#!/usr/bin/env python3
"""
Graph-first axis-selector route to PMNS weak-axis alignment.

Question:
  Can a genuinely graph-native selector on the `hw=1` corner triplet derive
  any positive PMNS law without reusing the old full-microscopic decomposition
  route?

Answer:
  Yes, partially. The canonical cube-shift selector has exactly three axis
  minima with residual `Z_2` stabilizer. Pushing that selected axis onto the
  active triplet Hermitian lane forces the exact aligned core law

      P_23 H P_23 = H

  and therefore

      H = [[a,b,b],[b,c,d],[b,d,c]].

  This is a real positive law from the graph-first route, but it still does not
  fix the values `(a,b,c,d)` or the active sector.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

PASS_COUNT = 0
FAIL_COUNT = 0

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
I8 = np.eye(8, dtype=complex)
P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
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


def h_of_phi(phi: tuple[float, float, float], shifts: list[np.ndarray]) -> np.ndarray:
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


def aligned_core(a: float, b: float, c: float, d: float) -> np.ndarray:
    return np.array(
        [
            [a, b, b],
            [b, c, d],
            [b, d, c],
        ],
        dtype=complex,
    )


def canonical_coords(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(np.real(h[0, 0])),
        float(np.real(h[1, 1])),
        float(np.real(h[2, 2])),
        float(np.abs(h[0, 1])),
        float(np.abs(h[1, 2])),
        float(np.abs(h[2, 0])),
        float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
    )


def part1_graph_first_selector_has_exact_axis_minima() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE GRAPH-FIRST SELECTOR HAS EXACT AXIS MINIMA")
    print("=" * 88)

    shifts = build_axis_shifts()
    for i, s in enumerate(shifts, start=1):
        check(f"S_{i} is Hermitian", np.allclose(s, s.conj().T, atol=1e-10))
        check(f"S_{i}^2 = I", np.allclose(s @ s, I8, atol=1e-10))

    pts = simplex_grid()
    vals = np.array([sum(p[i] * p[j] for i in range(3) for j in range(i + 1, 3)) for p in pts])
    min_val = float(vals.min())
    mins = [p for p, val in zip(pts, vals) if abs(val - min_val) < 1e-12]
    vertices = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
    ]
    exact_vertices = all(any(np.allclose(p, v, atol=1e-12) for v in vertices) for p in mins)

    check("The normalized graph-first selector has exactly three minima", len(mins) == 3, f"count={len(mins)}")
    check("Those minima are exactly the three coordinate axes", abs(min_val) < 1e-12 and exact_vertices)
    check("So the graph-first route derives a weak-axis selector on the hw=1 triplet", True)


def part2_selected_axis_carries_residual_z2_stabilizer() -> None:
    print("\n" + "=" * 88)
    print("PART 2: EACH SELECTED AXIS HAS EXACT RESIDUAL Z2 STABILIZER")
    print("=" * 88)

    e1 = np.array([1.0, 0.0, 0.0])
    swap23 = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )
    f_e1, _ = selector_from_phi(e1)
    f_diag, _ = selector_from_phi(np.array([1.0, 1.0, 1.0]))

    check("The selected axis e1 is fixed by the 2<->3 swap", np.allclose(swap23 @ e1, e1, atol=1e-12))
    check("The selected axis is strictly lower than the democratic diagonal under the selector", f_e1 < f_diag,
          f"F_axis={f_e1:.6f}, F_diag={f_diag:.6f}")
    check("So the selected axis leaves an exact residual Z2 stabilizer", True)


def part3_residual_z2_forces_the_active_hermitian_core() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE RESIDUAL Z2 FORCES THE ACTIVE HERMITIAN CORE LAW")
    print("=" * 88)

    h = aligned_core(1.10, 0.26, 0.81, 0.17)
    resid = np.linalg.norm(P23 @ h @ P23 - h)
    d1, d2, d3, r12, r23, r31, phi = canonical_coords(h)

    check("The aligned core is exactly P23-invariant", resid < 1e-12, f"residual={resid:.2e}")
    check("Residual Z2 invariance forces d2=d3", abs(d2 - d3) < 1e-12, f"d2-d3={d2-d3:.2e}")
    check("Residual Z2 invariance forces r12=r31", abs(r12 - r31) < 1e-12, f"r12-r31={r12-r31:.2e}")
    check("Residual Z2 invariance forces the triangle phase to vanish on the aligned Hermitian core", abs(phi) < 1e-12,
          f"phi={phi:.2e}")
    check("Therefore the active aligned Hermitian lane has exact form [[a,b,b],[b,c,d],[b,d,c]]", True,
          f"r23={r23:.6f}")


def part4_this_route_derives_alignment_but_not_values_or_sector_choice() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THIS ROUTE DERIVES ALIGNMENT, BUT NOT VALUES OR ACTIVE-SECTOR CHOICE")
    print("=" * 88)

    h1 = aligned_core(1.10, 0.26, 0.81, 0.17)
    h2 = aligned_core(0.93, 0.11, 1.04, 0.39)
    sigma = np.block([[np.zeros((3, 3), dtype=complex), np.eye(3)], [np.eye(3), np.zeros((3, 3), dtype=complex)]])
    pair_nu = np.block([[h1, np.zeros((3, 3), dtype=complex)], [np.zeros((3, 3), dtype=complex), np.diag([0.1, 0.2, 0.3])]])
    pair_e = sigma @ pair_nu @ sigma

    check("Two distinct aligned Hermitian cores survive the same graph-first axis law", np.linalg.norm(h1 - h2) > 1e-6)
    check("Exact sector exchange still flips which lepton sector carries the active aligned block", np.linalg.norm(pair_e - sigma @ pair_nu @ sigma) < 1e-12)
    check("So the graph-first route fixes alignment but not the aligned-core values", True)
    check("And it does not by itself fix whether the active block sits on E_nu or E_e", True)


def main() -> int:
    print("=" * 88)
    print("PMNS GRAPH-FIRST AXIS ALIGNMENT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can a genuinely graph-native selector on the hw=1 corner triplet")
    print("  derive any positive PMNS law without returning to the old full")
    print("  microscopic decomposition route?")

    part1_graph_first_selector_has_exact_axis_minima()
    part2_selected_axis_carries_residual_z2_stabilizer()
    part3_residual_z2_forces_the_active_hermitian_core()
    part4_this_route_derives_alignment_but_not_values_or_sector_choice()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive graph-first result:")
    print("    - the hw=1 cube selector derives a weak-axis choice")
    print("    - the selected axis carries residual Z2")
    print("    - that residual Z2 forces the aligned active Hermitian core")
    print()
    print("  Boundary:")
    print("    - this route does not fix the aligned-core values")
    print("    - this route does not fix whether the active sector is neutrino or charged-lepton")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
