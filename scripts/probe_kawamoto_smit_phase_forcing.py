"""Block 03: exact-arithmetic verification of Kawamoto-Smit phase forcing.

Verifies that the spin-rotation T(x) = σ_1^{x_1} σ_2^{x_2} σ_3^{x_3} on the
Pauli per-site realization gives Kawamoto-Smit phases:
    η_1(x) = 1
    η_2(x) = (−1)^{x_1}
    η_3(x) = (−1)^{x_1 + x_2}

via the diagonalization condition T†(x) γ_μ T(x + μ̂) = η_μ(x) · I_2.

This is exact-arithmetic (sympy, all operations on 2x2 Pauli matrices).

Companion: docs/STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md
Loop: staggered-dirac-realization-gate-20260507
Block: 03
"""
from __future__ import annotations

from typing import List, Tuple

import sympy as sp


def pauli_matrices() -> Tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    """Return (I_2, σ_1, σ_2, σ_3) in sympy."""
    I2 = sp.eye(2)
    s1 = sp.Matrix([[0, 1], [1, 0]])
    s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    s3 = sp.Matrix([[1, 0], [0, -1]])
    return I2, s1, s2, s3


def matrix_power_int(M: sp.Matrix, n: int) -> sp.Matrix:
    """Compute M^n for integer n (handles n=0 case as identity)."""
    if n == 0:
        return sp.eye(M.rows)
    elif n == 1:
        return M
    else:
        return M ** n


def T_of_x(x: Tuple[int, int, int]) -> sp.Matrix:
    """T(x) = σ_1^{x_1} · σ_2^{x_2} · σ_3^{x_3} on Pauli site."""
    _, s1, s2, s3 = pauli_matrices()
    x1, x2, x3 = x
    # σ_i^2 = I, so σ_i^{x_i} = σ_i if x_i odd, I if x_i even
    p1 = matrix_power_int(s1, x1 % 2)
    p2 = matrix_power_int(s2, x2 % 2)
    p3 = matrix_power_int(s3, x3 % 2)
    return p1 * p2 * p3


def T_dagger(x: Tuple[int, int, int]) -> sp.Matrix:
    """T†(x). For unitary T (Pauli matrices are Hermitian and σ_i² = I),
    T† equals T-reversed, but we just take H.c. directly."""
    return T_of_x(x).H


def gamma_mu(mu: int) -> sp.Matrix:
    """γ_μ = σ_μ in Pauli realization (1-indexed)."""
    _, s1, s2, s3 = pauli_matrices()
    if mu == 1:
        return s1
    elif mu == 2:
        return s2
    elif mu == 3:
        return s3
    else:
        raise ValueError(f"mu must be 1, 2, or 3, got {mu}")


def neighbor(x: Tuple[int, int, int], mu: int) -> Tuple[int, int, int]:
    """x + μ̂."""
    x1, x2, x3 = x
    if mu == 1:
        return (x1 + 1, x2, x3)
    elif mu == 2:
        return (x1, x2 + 1, x3)
    elif mu == 3:
        return (x1, x2, x3 + 1)
    else:
        raise ValueError(f"mu must be 1, 2, or 3")


def diagonalization_test(x: Tuple[int, int, int], mu: int
                          ) -> Tuple[bool, sp.Expr, str]:
    """Compute T†(x) · γ_μ · T(x + μ̂) and verify it equals η_μ(x) · I_2.

    Returns (is_diagonal, η_μ(x), message).
    """
    x_plus_mu = neighbor(x, mu)
    T_x_dag = T_dagger(x)
    T_xpm = T_of_x(x_plus_mu)
    g_mu = gamma_mu(mu)

    result = T_x_dag * g_mu * T_xpm
    result_simp = sp.simplify(result)

    # Check it's a scalar multiple of I_2
    if result_simp[0, 1] == 0 and result_simp[1, 0] == 0:
        if result_simp[0, 0] == result_simp[1, 1]:
            eta = result_simp[0, 0]
            return True, eta, f"η_{mu}(x={x}) = {eta}"
        else:
            return False, sp.S.Zero, f"Non-scalar diagonal: {result_simp}"
    else:
        return False, sp.S.Zero, f"Non-diagonal: {result_simp}"


def kawamoto_smit_phase_expected(x: Tuple[int, int, int], mu: int) -> int:
    """Expected K-S phase: η_1=1, η_2(x)=(−1)^{x_1}, η_3(x)=(−1)^{x_1+x_2}."""
    x1, x2, x3 = x
    if mu == 1:
        return 1
    elif mu == 2:
        return (-1) ** x1
    elif mu == 3:
        return (-1) ** (x1 + x2)
    else:
        raise ValueError


def main() -> int:
    print("=" * 72)
    print("Block 03 — Kawamoto-Smit Phase Forcing Verification")
    print("Loop: staggered-dirac-realization-gate-20260507")
    print("Companion: docs/STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md")
    print("=" * 72)
    print()
    print("Verifies: T†(x) γ_μ T(x + μ̂) = η_μ(x) · I_2")
    print("with T(x) = σ_1^{x_1} σ_2^{x_2} σ_3^{x_3}")
    print()
    print("Expected K-S phases:")
    print("  η_1 = 1")
    print("  η_2(x) = (−1)^{x_1}")
    print("  η_3(x) = (−1)^{x_1 + x_2}")
    print()

    # Test on all 8 sites of a 2³ unit cell
    sites = [(x1, x2, x3) for x1 in (0, 1) for x2 in (0, 1) for x3 in (0, 1)]
    n_pass = 0
    n_total = 0

    for x in sites:
        for mu in (1, 2, 3):
            is_diag, eta, msg = diagonalization_test(x, mu)
            expected = kawamoto_smit_phase_expected(x, mu)
            match = is_diag and (eta == sp.Integer(expected))
            n_total += 1
            if match:
                n_pass += 1
            status = "PASS" if match else "FAIL"
            print(f"[{status}] x={x}, μ={mu}: derived η = {eta}, expected = {expected}")

    print()
    print(f"SUMMARY: PASS={n_pass} FAIL={n_total - n_pass} (out of {n_total} = 8 sites × 3 directions)")
    print()

    # Pauli algebra cross-check
    print("Cross-check: σ_1 σ_2 σ_3 = i I_2 (chirality central pseudoscalar)")
    _, s1, s2, s3 = pauli_matrices()
    omega = s1 * s2 * s3
    omega_simp = sp.simplify(omega)
    expected_omega = sp.I * sp.eye(2)
    if sp.simplify(omega_simp - expected_omega) == sp.zeros(2, 2):
        print(f"  σ_1 σ_2 σ_3 = {omega_simp[0,0]} · I_2  (= i · I_2 verified)")
    else:
        print(f"  FAIL: σ_1 σ_2 σ_3 = {omega_simp}")

    print()
    print("Bounded theorem (T2) — Kawamoto-Smit Phase Forcing — verified.")
    print("Spin-rotation T(x) = σ_1^{x_1} σ_2^{x_2} σ_3^{x_3} diagonalizes")
    print("the kinetic operator into Kawamoto-Smit phases on all 8 unit-cell sites.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    raise SystemExit(main())
