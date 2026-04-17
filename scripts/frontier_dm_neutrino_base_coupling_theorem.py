#!/usr/bin/env python3
"""
Neutrino Base Normalization Audit
=================================

STATUS: EXACT historical normalization audit; superseded by the bosonic
        normalization theorem for the physical selector

Purpose:
  Test whether the direct local Gamma_1 bridge fixes a UNIQUE unsuppressed
  neutrino Yukawa normalization.

  The bridge theorem fixed the direct local post-EWSB operator as Gamma_1.
  The next sharp question is:

    Does the current branch uniquely determine the bare local ratio
    y_nu^(0) / g_weak?

  The answer at this audit stage was NO. The current branch supported multiple
  exact normalization conventions:

    - full C^16 Frobenius trace      -> 1 / sqrt(2)
    - active chiral subspace trace   -> 1
    - operator norm / singular value -> 1

  So the direct local bridge was fixed, but its physical normalization was not
  yet selected at the audit stage.

  What DOES remain exact is the generation-resolved second-order structure:

    Y_eff(T_1) = y_nu^(0) * diag(a, b, b)

  where a and b are the singlet and residual-pair second-order channel
  coefficients. The open problem at audit time was therefore:

    1. select the physical normalization for y_nu^(0)
    2. determine the dynamical coefficients (a, b)

  This runner is now historical. The later bosonic-normalization theorem
  selects the physical base normalization; the second-order coefficients still
  remain open.
"""

from __future__ import annotations

import math
import sys
import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
I16 = np.eye(16, dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G0 = kron4(SZ, SZ, SZ, SX)
G1 = kron4(SX, I2, I2, I2)
G2 = kron4(SZ, SX, I2, I2)
G3 = kron4(SZ, SZ, SX, I2)
GAMMA_5_4D = G0 @ G1 @ G2 @ G3
P_L = (I16 + GAMMA_5_4D) / 2.0
P_R = (I16 - GAMMA_5_4D) / 2.0

Y_BRIDGE = P_R @ G1 @ P_L

FULL_STATES = [(a, b, c, t) for a in range(2) for b in range(2) for c in range(2) for t in range(2)]
INDEX = {state: i for i, state in enumerate(FULL_STATES)}

O0 = [(0, 0, 0)]
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]


def projector(spatial_states: list[tuple[int, int, int]]) -> np.ndarray:
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            p[INDEX[s + (t,)], INDEX[s + (t,)]] = 1.0
    return p


def restrict_to_t1(matrix: np.ndarray) -> np.ndarray:
    cols = []
    for t in (0, 1):
        for s in T1:
            e = np.zeros((16, 1), dtype=complex)
            e[INDEX[s + (t,)], 0] = 1.0
            cols.append(e)
    basis = np.hstack(cols)
    return basis.conj().T @ matrix @ basis


def main() -> int:
    print("=" * 78)
    print("NEUTRINO BASE NORMALIZATION AUDIT")
    print("=" * 78)
    print()

    print("Part 1: Direct local bridge normalization audit")
    gauge_trace = np.trace(G1.conj().T @ G1).real / 16.0
    yukawa_trace = np.trace(Y_BRIDGE.conj().T @ Y_BRIDGE).real / 16.0
    ratio_full = math.sqrt(yukawa_trace / gauge_trace)
    left_gauge_trace = np.trace(P_L @ (G1.conj().T @ G1)).real / np.trace(P_L).real
    left_yukawa_trace = np.trace(Y_BRIDGE.conj().T @ Y_BRIDGE).real / np.trace(P_L).real
    ratio_left = math.sqrt(left_yukawa_trace / left_gauge_trace)
    right_gauge_trace = np.trace(P_R @ (G1 @ G1.conj().T)).real / np.trace(P_R).real
    right_yukawa_trace = np.trace(Y_BRIDGE @ Y_BRIDGE.conj().T).real / np.trace(P_R).real
    ratio_right = math.sqrt(right_yukawa_trace / right_gauge_trace)
    op_ratio = np.linalg.svd(Y_BRIDGE, compute_uv=False).max() / np.linalg.svd(G1, compute_uv=False).max()

    print(f"  Gauge trace   Tr(Gamma_1^dag Gamma_1) / 16 = {gauge_trace:.6f}")
    print(f"  Yukawa trace  Tr(Y^dag Y) / 16          = {yukawa_trace:.6f}")
    print(f"  Full-space Frobenius ratio             = {ratio_full:.6f}")
    print(f"  Left-active Frobenius ratio            = {ratio_left:.6f}")
    print(f"  Right-active Frobenius ratio           = {ratio_right:.6f}")
    print(f"  Operator-norm ratio                    = {op_ratio:.6f}")
    print()

    check("Gamma_1 is unit-normalized on C^16",
          abs(gauge_trace - 1.0) < 1e-12)
    check("Direct chiral bridge has half-trace",
          abs(yukawa_trace - 0.5) < 1e-12)
    check("Full-space Frobenius ratio is 1/sqrt(2)",
          abs(ratio_full - 1.0 / math.sqrt(2.0)) < 1e-12,
          detail=f"ratio = {ratio_full:.12f}")
    check("Active-source Frobenius ratio is 1",
          abs(ratio_left - 1.0) < 1e-12,
          detail=f"ratio = {ratio_left:.12f}")
    check("Active-target Frobenius ratio is 1",
          abs(ratio_right - 1.0) < 1e-12,
          detail=f"ratio = {ratio_right:.12f}")
    check("Operator-norm ratio is 1",
          abs(op_ratio - 1.0) < 1e-12,
          detail=f"ratio = {op_ratio:.12f}")

    print()
    print("Part 2: Second-order channel structure on T_1")
    p_o0 = projector(O0)
    p_t1 = projector(T1)
    p_t2 = projector(T2)

    def return_operator(a: float, b: float) -> np.ndarray:
        k = a * p_o0 + b * p_t2
        return p_t1 @ G1 @ k @ G1 @ p_t1

    test_cases = [
        (1.0, 1.0),
        (2.0, 5.0),
        (0.5, 0.25),
    ]
    for a, b in test_cases:
        restricted = restrict_to_t1(return_operator(a, b))
        expected = np.diag([a, b, b, a, b, b])
        check(
            f"R(a,b) = diag(a,b,b) x I_time for a={a}, b={b}",
            np.allclose(restricted, expected, atol=1e-12),
        )

    print()
    sample = restrict_to_t1(return_operator(2.0, 5.0))
    print("  Example restricted return for (a,b) = (2,5):")
    for row in sample:
        entries = " ".join(f"{val.real:4.1f}" for val in row)
        print(f"    [{entries} ]")
    print()

    avg_coeff = np.trace(sample).real / sample.shape[0]
    check("Average T1 coefficient is (a+2b)/3",
          abs(avg_coeff - (2.0 + 2.0 * 5.0) / 3.0) < 1e-12,
          detail=f"avg = {avg_coeff:.6f}")

    print()
    print("Part 3: Practical impact")
    g_weak_example = 0.653
    y0_full = g_weak_example / math.sqrt(2.0)
    y0_active = g_weak_example
    print(f"  If g_weak = {g_weak_example:.3f}, then:")
    print(f"    full-space benchmark   y_nu^(0) = {y0_full:.6f}")
    print(f"    active-space benchmark y_nu^(0) = {y0_active:.6f}")
    print("  This is the historical audit surface before the later")
    print("  bosonic-normalization selector closed the physical choice.")
    print()

    print("Historical audit read:")
    print("  1. This runner isolates the old normalization ambiguity cleanly.")
    print("  2. Full-space Frobenius normalization gives 1/sqrt(2), while active")
    print("     chiral-subspace and operator-norm normalizations give 1.")
    print("  3. The later bosonic-normalization theorem selects the full-space")
    print("     ratio as physical, so this script should now be read only as")
    print("     the intermediate audit that exposed the ambiguity.")
    print("  4. The exact second-order T_1 return still reduces to two channel")
    print("     coefficients a and b in the 1+2 form diag(a,b,b).")
    print()
    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
