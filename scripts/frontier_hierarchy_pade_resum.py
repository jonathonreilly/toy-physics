#!/usr/bin/env python3
"""
Pade resummation of the framework's reduction-law onset jet.

Reads beta_eff(beta) data from MC inversion (saved by
frontier_hierarchy_wilson_mc_kernel.py) and:

1. Fits beta_eff(beta) - beta = sum_{k>=2} c_k beta^k by least squares
   (with the framework constraint that c_2 = c_3 = c_4 = 0; first
   non-trivial coefficient is c_5).
2. Compares fitted c_5 to the framework's analytic value c_5 = 1/26244.
3. Builds a Pade approximant [N/M] of beta_eff(beta) - beta and
   evaluates at beta = 6.
4. Compares to the direct P_1plaq^(-1) inversion of the canonical
   <P>(6) = 0.5934.

This is class (C) numerical: results have MC + truncation + finite-volume
errors. The point is to expose the higher-order onset-jet structure.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial import polynomial as P

DATA = Path("/tmp/wilson_mc_beta_eff.npz")

FRAMEWORK_C5 = 1.0 / 26244.0  # ~ 3.81e-5

CANONICAL_P6 = 0.5934


def fit_polynomial_constrained(betas: np.ndarray, residuals: np.ndarray,
                                k_min: int = 5, k_max: int = 8) -> np.ndarray:
    """Fit residuals = sum_{k=k_min..k_max} c_k beta^k by least squares.

    Returns coefficient array indexed by k (k=0,1,...,k_max), with
    c_0..c_{k_min-1} = 0.
    """
    # Design matrix: rows = data points, cols = beta^k for k = k_min..k_max
    X = np.column_stack([betas ** k for k in range(k_min, k_max + 1)])
    # Solve least squares
    coefs, _, _, _ = np.linalg.lstsq(X, residuals, rcond=None)
    full = np.zeros(k_max + 1)
    for j, k in enumerate(range(k_min, k_max + 1)):
        full[k] = coefs[j]
    return full


def evaluate_polynomial(coefs: np.ndarray, beta: float) -> float:
    """Evaluate polynomial sum_k c_k * beta^k."""
    return sum(c * beta ** k for k, c in enumerate(coefs))


def pade_approximant(coefs: np.ndarray, n: int, m: int):
    """Build [n/m] Pade approximant of polynomial with given coefficients.

    Returns (P_num, Q_den) such that approximant ~ P/Q matches series to
    order n+m.
    """
    # Pade [n/m] requires the first n+m+1 series coefficients
    if len(coefs) < n + m + 1:
        coefs = np.concatenate([coefs, np.zeros(n + m + 1 - len(coefs))])

    # Solve for Q first: matrix from c_k coefs
    # Standard linear system: see e.g. Baker-Graves-Morris
    if m == 0:
        return coefs[:n + 1], np.array([1.0])

    A = np.zeros((m, m))
    rhs = np.zeros(m)
    for i in range(m):
        for j in range(m):
            idx = n + i + 1 - (j + 1)
            if 0 <= idx < len(coefs):
                A[i, j] = coefs[idx]
        rhs[i] = -coefs[n + i + 1] if n + i + 1 < len(coefs) else 0.0
    q_lower, _, _, _ = np.linalg.lstsq(A, rhs, rcond=None)
    Q = np.concatenate([[1.0], q_lower])

    # Numerator P
    P_num = np.zeros(n + 1)
    for k in range(n + 1):
        P_num[k] = coefs[k]
        for j in range(1, min(k, m) + 1):
            P_num[k] += Q[j] * coefs[k - j]
    return P_num, Q


def pade_eval(P_num: np.ndarray, Q_den: np.ndarray, beta: float) -> float:
    """Evaluate Pade rational at beta."""
    num = sum(P_num[k] * beta ** k for k in range(len(P_num)))
    den = sum(Q_den[k] * beta ** k for k in range(len(Q_den)))
    return num / den


def main() -> int:
    if not DATA.exists():
        print(f"FAIL: data file {DATA} not found. Run wilson_mc_kernel.py first.")
        return 1

    z = np.load(DATA)
    betas = z["betas"]
    beta_effs = z["beta_effs"]
    plaqs = z["plaqs"]

    print(f"Loaded {len(betas)} (beta, beta_eff, <P>) data points from {DATA}")
    print()
    print(f"{'beta':>8s}  {'<P>(beta)':>11s}  {'beta_eff':>10s}  {'beta_eff - beta':>16s}")
    print("-" * 78)
    for b, be, p in zip(betas, beta_effs, plaqs):
        print(f"{b:>8.2f}  {p:>11.6f}  {be:>10.4f}  {be - b:>+16.4f}")

    residuals = beta_effs - betas

    # Fit at various polynomial truncation orders
    print("\n## Constrained polynomial fit: beta_eff(beta) - beta = sum_{k=5..K} c_k beta^k\n")
    for k_max in (5, 6, 7, 8, 9, 10):
        coefs = fit_polynomial_constrained(betas, residuals, k_min=5, k_max=k_max)
        # Evaluate fit residual
        fit_vals = np.array([evaluate_polynomial(coefs, b) for b in betas])
        rms = math.sqrt(np.mean((fit_vals - residuals) ** 2))
        print(f"K = {k_max}:  c_5 = {coefs[5]:+.4e}, framework c_5 = {FRAMEWORK_C5:+.4e}, ratio = {coefs[5]/FRAMEWORK_C5:+.2f}, RMS residual = {rms:.4f}")

    # Detailed fit at K = 8
    print("\n## Detailed fit at K = 8\n")
    coefs8 = fit_polynomial_constrained(betas, residuals, k_min=5, k_max=8)
    for k in range(len(coefs8)):
        if abs(coefs8[k]) > 1e-12:
            print(f"  c_{k} = {coefs8[k]:+.4e}")

    # Predict beta_eff(6) from fit
    print("\n## Prediction at beta = 6\n")
    for k_max in (5, 6, 7, 8, 9, 10):
        coefs = fit_polynomial_constrained(betas, residuals, k_min=5, k_max=k_max)
        be6 = 6.0 + evaluate_polynomial(coefs, 6.0)
        # Convert via P_1plaq for predicted <P>(6)
        sys.path.insert(0, str(Path(__file__).parent))
        from frontier_hierarchy_route_1b_haar_evaluation import p_1plaq
        try:
            p6_pred = p_1plaq(be6, n=64)
        except (ValueError, OverflowError):
            p6_pred = float("nan")
        print(f"K = {k_max}:  beta_eff(6) ~= {be6:.4f},  <P>(6) (via P_1plaq) ~= {p6_pred:.6f}")

    # Pade approximant
    print("\n## Pade approximant of beta_eff(beta) - beta, using K=8 series coefs\n")
    coefs = coefs8
    for (n, m) in [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)]:
        try:
            P_num, Q_den = pade_approximant(coefs, n, m)
            be6_pade = 6.0 + pade_eval(P_num, Q_den, 6.0)
            print(f"  Pade[{n}/{m}]:  beta_eff(6) ~= {be6_pade:.4f}")
        except Exception as e:
            print(f"  Pade[{n}/{m}]: FAILED ({e})")

    # Direct canonical inversion target
    print(f"\n## Reference: direct P_1plaq^(-1)(canonical 0.5934) = 9.33")
    print(f"## Bulk MC <P>(6) ~ 0.5934 (canonical), L=2 MC value ~ 0.624 (this kernel)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
