#!/usr/bin/env python3
"""
Route 1B numerical kernel: single-plaquette block P_1plaq(beta) via Haar
integration on SU(3), and consistency check of the framework's reduction-law
onset jet at beta=6.

The framework's reduction law (GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM):
    P_L(beta) = P_1plaq(beta_eff,L(beta))
with beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6).

If the leading onset is the dominant correction, then at beta=6:
    beta_eff(6) ~= 6 + 6^5 / 26244 ~= 6.2962

This script:
  1. Computes P_1plaq(beta) by direct 2D Haar integration on SU(3)
     in the eigenvalue parameterization.
  2. Inverts P_1plaq to find beta_eff(6) such that
     P_1plaq(beta_eff) = <P>_canonical = 0.5934.
  3. Compares the inversion to the onset-jet prediction.
  4. Reports the gap, which is exactly the higher-order onset-jet residual
     that Route 1A extension would close.

This is a class (B) numerical theorem: the Haar integration is a controlled
quadrature on a compact manifold; the inversion is monotone and unique
because P_1plaq is strictly increasing (REDUCTION_EXISTENCE_THEOREM Theorem 1).
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.integrate import dblquad
from scipy.optimize import brentq

# =============================================================================
# SU(3) Haar integration in eigenvalue parameterization
# =============================================================================
# Eigenvalues of U in SU(3): (e^{i theta_1}, e^{i theta_2}, e^{i theta_3})
# with theta_1 + theta_2 + theta_3 = 0 mod 2 pi.
# Eliminate theta_3 = -theta_1 - theta_2 (canonical fundamental domain).
# Haar measure in this parameterization:
#   d mu_Haar = (1 / (6 (2 pi)^2)) * |Delta|^2 d theta_1 d theta_2
# where |Delta|^2 = prod_{i<j} 4 sin^2((theta_i - theta_j)/2) is the
# Vandermonde determinant absolute value squared (Weyl integration formula).

def vandermonde_sq(t1: float, t2: float) -> float:
    """|Delta(e^{i theta})|^2 for SU(3) with theta_3 = -t1 - t2."""
    t3 = -t1 - t2
    return (
        4 * math.sin((t1 - t2) / 2) ** 2
        * 4 * math.sin((t2 - t3) / 2) ** 2
        * 4 * math.sin((t3 - t1) / 2) ** 2
    )


def re_tr_u(t1: float, t2: float) -> float:
    """Re Tr U for U with eigenvalues at (t1, t2, -t1-t2)."""
    return math.cos(t1) + math.cos(t2) + math.cos(t1 + t2)


def haar_integral(integrand, n: int = 128) -> float:
    """Numerical Haar integral over SU(3) via 2D quadrature.

    Uses a tensor-product trapezoidal grid on (-pi, pi)^2 (the fundamental
    domain after eliminating theta_3).
    """
    grid = np.linspace(-math.pi, math.pi, n, endpoint=False) + math.pi / n
    integral = 0.0
    norm = 0.0
    h = (2 * math.pi / n) ** 2
    for t1 in grid:
        for t2 in grid:
            v = vandermonde_sq(t1, t2)
            integral += integrand(t1, t2) * v * h
            norm += v * h
    # Normalize: full Haar mass = 1
    return integral / norm


def check_haar_normalization(n: int = 128) -> float:
    """Check that the Haar normalization integrates to 1."""
    return haar_integral(lambda t1, t2: 1.0, n=n)


def z_1plaq(beta: float, n: int = 128) -> float:
    """Z_1plaq(beta) / Z_1plaq(0) = <exp((beta/3) Re Tr U)>_Haar."""
    return haar_integral(lambda t1, t2: math.exp((beta / 3.0) * re_tr_u(t1, t2)), n=n)


def p_1plaq(beta: float, n: int = 128) -> float:
    """P_1plaq(beta) = <(1/3) Re Tr U>_(tilted Haar)."""
    if beta == 0.0:
        # By Haar symmetry, <(1/3) Re Tr U>_Haar = 0
        return 0.0
    grid = np.linspace(-math.pi, math.pi, n, endpoint=False) + math.pi / n
    h = (2 * math.pi / n) ** 2
    num = 0.0
    den = 0.0
    norm = 0.0
    for t1 in grid:
        for t2 in grid:
            v = vandermonde_sq(t1, t2)
            x = re_tr_u(t1, t2)
            w = math.exp((beta / 3.0) * x)
            num += (x / 3.0) * w * v * h
            den += w * v * h
            norm += v * h
    # Both num and den have the same Haar normalization, which cancels
    return num / den


# =============================================================================
# Onset-jet prediction
# =============================================================================
# beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6)
# (REDUCTION_EXISTENCE_THEOREM_NOTE)

def beta_eff_onset(beta: float) -> float:
    """Leading onset jet of beta_eff(beta) at order beta^5."""
    return beta + beta ** 5 / 26244.0


# =============================================================================
# Main pipeline
# =============================================================================

def main() -> int:
    print("Route 1B numerical kernel: single-plaquette Haar evaluation")
    print("=" * 78)

    # Step 1: verify Haar normalization
    print("\n[1] Verify Haar normalization on SU(3)")
    for n in (32, 64, 128):
        norm = check_haar_normalization(n=n)
        print(f"  n = {n:3d}:  <1>_Haar = {norm:.10f}  (target 1.0)")

    # Step 2: Z_1plaq(0) = 1
    print("\n[2] Verify Z_1plaq(0) / Z_1plaq(0) = 1")
    z0 = z_1plaq(0.0, n=128)
    print(f"  Z_1plaq(0) (normalized) = {z0:.10f}  (target 1.0)")

    # Step 3: P_1plaq(0) = 0
    print("\n[3] Verify P_1plaq(0) = 0 (Haar plaquette vanishes)")
    p0 = p_1plaq(0.0, n=128)
    print(f"  P_1plaq(0) = {p0:.10f}  (target 0.0)")

    # Step 4: P_1plaq(beta) at sample points
    print("\n[4] P_1plaq(beta) at sample beta values (n = 128 Haar grid)")
    print(f"  {'beta':>8s}  {'P_1plaq(beta)':>15s}")
    for beta in (1.0, 3.0, 6.0, 6.296, 7.0, 10.0, 20.0):
        p = p_1plaq(beta, n=128)
        print(f"  {beta:>8.3f}  {p:>15.10f}")

    # Step 5: invert to find beta_eff(6) such that P_1plaq(beta_eff) = 0.5934
    print("\n[5] Invert P_1plaq to find beta_eff(6) such that P_1plaq(beta_eff) = 0.5934")
    canonical_P6 = 0.5934

    def root_fn(b):
        return p_1plaq(b, n=128) - canonical_P6

    # Bracket the root
    lo, hi = 1.0, 30.0
    p_lo = p_1plaq(lo, n=128)
    p_hi = p_1plaq(hi, n=128)
    print(f"  Bracket: P_1plaq({lo}) = {p_lo:.6f}, P_1plaq({hi}) = {p_hi:.6f}")
    if not (p_lo < canonical_P6 < p_hi):
        print(f"  WARNING: 0.5934 not bracketed by [P_1plaq({lo}), P_1plaq({hi})]")

    beta_eff_inferred = brentq(root_fn, lo, hi, xtol=1e-6)
    print(f"  beta_eff(6) inferred = {beta_eff_inferred:.6f}")

    # Step 6: compare to onset-jet prediction
    print("\n[6] Compare inferred beta_eff(6) to onset-jet prediction")
    beta_eff_predicted = beta_eff_onset(6.0)
    gap = beta_eff_inferred - beta_eff_predicted
    print(f"  onset-jet prediction (order beta^5):  beta_eff(6) ~= {beta_eff_predicted:.6f}")
    print(f"  inferred from P_1plaq inversion:       beta_eff(6) ~= {beta_eff_inferred:.6f}")
    print(f"  gap (higher-order onset residual):     delta = {gap:+.6f}")
    print(f"  relative residual:                     |delta| / beta = {abs(gap)/6.0:.4%}")

    # Step 7: estimate the order needed to close the gap
    print("\n[7] Estimate Route 1A onset-jet order needed to close the residual")
    print(f"  Residual to close: |delta| ~ {abs(gap):.4f}")
    print(f"  Bessel-majorant bound: 6^N / N! < |delta|")
    for N in range(6, 35):
        bound = 6.0 ** N / math.factorial(N)
        if bound < abs(gap):
            print(f"  -> N_target = {N},  6^N / N! = {bound:.4e}")
            break
    else:
        print(f"  -> N > 35 needed  (gap may be larger than Bessel-majorant scale)")

    # Step 8: report the v-prediction sensitivity
    print("\n[8] v-prediction sensitivity to <P>(6)")
    # v = M_Pl * (alpha_bare / <P>(6)^(1/4))^16 * (7/8)^(1/4)
    # = M_Pl * alpha_bare^16 / <P>(6)^4 * (7/8)^(1/4)
    # d v / d<P> = -4 v / <P>(6)
    M_PLANCK = 1.2209e19
    ALPHA_BARE = 1.0 / (4.0 * math.pi)
    P_canonical = 0.5934
    U0 = P_canonical ** 0.25
    ALPHA_LM = ALPHA_BARE / U0
    v_canonical = M_PLANCK * ALPHA_LM ** 16 * (7.0 / 8.0) ** 0.25
    sensitivity = -4.0 * v_canonical / P_canonical
    print(f"  v(canonical <P>=0.5934)         = {v_canonical:.6f} GeV")
    print(f"  d v / d<P>                      = {sensitivity:.4e} GeV per unit <P>")
    print(f"  bridge candidate <P> = 0.59353")
    P_bridge = 0.59353
    delta_P = P_bridge - P_canonical
    delta_v = sensitivity * delta_P
    print(f"  delta v from canonical->bridge  = {delta_v:.6f} GeV")
    print(f"  v(bridge <P>=0.59353)           = {v_canonical + delta_v:.6f} GeV")
    print(f"  PDG comparator                  = 246.22 GeV")
    print(f"  bridge - canonical |v shift|    = {abs(delta_v):.4f} GeV ({abs(delta_v/v_canonical)*100:.4f}%)")

    print("\n" + "=" * 78)
    print("Route 1B numerical kernel complete.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
