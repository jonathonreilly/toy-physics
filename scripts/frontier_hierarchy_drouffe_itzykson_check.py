#!/usr/bin/env python3
"""
Cross-check P_1plaq(beta) via the Drouffe-Itzykson Bessel-determinant formula.

For SU(N), the partition function with action exp(beta/N · Re Tr U) equals

    Z_1plaq(beta) / Z_1plaq(0)
        = c_(0,0)(beta)
        = sum_{n in Z} det[ I_{n + i - j}(beta/N) ]_{i,j = 1..N}

where I_nu(z) is the modified Bessel function of the first kind.

For N = 3:
    c_(0,0)(beta) = sum_n det[
        I_n(beta/3),     I_(n-1)(beta/3), I_(n-2)(beta/3) ;
        I_(n+1)(beta/3), I_n(beta/3),     I_(n-1)(beta/3) ;
        I_(n+2)(beta/3), I_(n+1)(beta/3), I_n(beta/3)
    ]

Then P_1plaq(beta) = (1/N_plaq) d/dbeta log Z_1plaq(beta), or equivalently
P_1plaq(beta) = (d/dbeta c_(0,0)(beta)) / c_(0,0)(beta).

Cross-check target:
  - Haar integration kernel: P_1plaq(6) = 0.4225317396
  - Framework Perron-solve P_triv(6) = 0.4225317396
  - Drouffe-Itzykson Bessel determinant: should also give 0.4225317396.

If all three agree to ~10 digits, the framework's reduction-law machinery
has three independent analytic computations of the same single-plaquette
quantity, confirming numerical consistency.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.special import iv


def bessel_det_3x3(n: int, z: float) -> float:
    """Compute det[I_{n+i-j}(z)]_{i,j=1..3} for 3x3 SU(3) block."""
    M = np.zeros((3, 3))
    for i in range(1, 4):
        for j in range(1, 4):
            M[i - 1, j - 1] = iv(n + i - j, z)
    return float(np.linalg.det(M))


def c_00(beta: float, n_max: int = 30) -> float:
    """Drouffe-Itzykson c_(0,0)(beta) for SU(3) via Bessel determinant sum."""
    z = beta / 3.0
    total = 0.0
    for n in range(-n_max, n_max + 1):
        total += bessel_det_3x3(n, z)
    return total


def c_00_derivative(beta: float, n_max: int = 30, h: float = 1e-5) -> float:
    """Numerical d/dbeta c_(0,0) via central difference."""
    return (c_00(beta + h, n_max) - c_00(beta - h, n_max)) / (2 * h)


def p_1plaq_di(beta: float, n_max: int = 30) -> float:
    """P_1plaq(beta) via Drouffe-Itzykson formula."""
    return c_00_derivative(beta, n_max=n_max) / c_00(beta, n_max=n_max)


def main() -> int:
    print("Drouffe-Itzykson cross-check of P_1plaq(beta)")
    print("=" * 78)

    print("\n## c_(0,0)(beta) Bessel-determinant convergence at beta = 6\n")
    z = 6.0 / 3.0  # = 2
    for n_max in (5, 10, 15, 20, 25, 30):
        c = c_00(6.0, n_max=n_max)
        print(f"  n_max = {n_max:3d}:  c_(0,0)(6) = {c:.15f}")

    print("\n## P_1plaq(beta) via Bessel determinant (independent of Haar quadrature)\n")
    print(f"  {'beta':>8s}  {'P_1plaq(DI)':>15s}")
    for beta in (1.0, 3.0, 6.0, 6.296, 7.0, 9.33, 10.0):
        try:
            p = p_1plaq_di(beta, n_max=30)
            print(f"  {beta:>8.3f}  {p:>15.10f}")
        except Exception as e:
            print(f"  {beta:>8.3f}  FAILED ({e})")

    print("\n## Three-way agreement check at beta = 6\n")
    p_di = p_1plaq_di(6.0, n_max=30)
    p_haar = 0.4225317396  # from frontier_hierarchy_route_1b_haar_evaluation.py
    p_framework = 0.4225317396  # from GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE
    print(f"  P_1plaq(6) Drouffe-Itzykson Bessel det:  {p_di:.10f}")
    print(f"  P_1plaq(6) Haar quadrature (kernel):     {p_haar:.10f}")
    print(f"  P_1plaq(6) Framework Perron solve:       {p_framework:.10f}")
    print(f"  |DI - Haar|     = {abs(p_di - p_haar):.3e}")
    print(f"  |DI - Frmwk|    = {abs(p_di - p_framework):.3e}")
    print(f"  |Haar - Frmwk|  = {abs(p_haar - p_framework):.3e}")

    if abs(p_di - p_haar) < 1e-7 and abs(p_di - p_framework) < 1e-7:
        print("\n[PASS] Three independent methods agree on P_1plaq(6) to 7+ digits.")
    else:
        print("\n[CHECK] Methods do not yet agree to 7+ digits.")

    print("\n## Inverted beta_eff(6) at canonical <P>(6) = 0.5934 (target)\n")
    target = 0.5934
    from scipy.optimize import brentq

    def fn(b):
        return p_1plaq_di(b, n_max=30) - target

    beta_eff_6 = brentq(fn, 1.0, 30.0, xtol=1e-6)
    print(f"  beta_eff(6) = {beta_eff_6:.6f}  (cross-check: Haar inversion gave 9.326168)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
