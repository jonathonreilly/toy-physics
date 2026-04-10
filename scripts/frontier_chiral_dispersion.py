#!/usr/bin/env python3
"""Chiral dispersion relation on the current local walk architecture.

This script tests the exact lattice dispersion relation for the periodic
1D chiral walk used throughout the chiral family in this repo:

    cos(E) = cos(theta) * cos(k)

and checks the low-k Klein-Gordon limit honestly:

    E^2 = 2(1 - cos(theta)) + cos(theta) * k^2 + O(k^4)

For small theta, this becomes E^2 ≈ theta^2 + k^2.

Dependencies: numpy only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


N_SITES = 63
THETAS = (0.1, 0.3, 0.5, 0.7)


@dataclass(frozen=True)
class FitResult:
    name: str
    r2: float
    params: tuple[float, float]


def build_chiral_unitary(n_sites: int, theta: float) -> np.ndarray:
    """Build the periodic 2n x 2n chiral walk unitary U = S @ C."""
    dim = 2 * n_sites
    coin = np.zeros((dim, dim), dtype=np.complex128)
    shift = np.zeros((dim, dim), dtype=np.complex128)

    c = math.cos(theta)
    s = math.sin(theta)
    for y in range(n_sites):
        ip = 2 * y
        im = ip + 1
        coin[ip, ip] = c
        coin[ip, im] = -s
        coin[im, ip] = s
        coin[im, im] = c

        if y + 1 < n_sites:
            shift[2 * (y + 1), ip] = 1.0
        else:
            shift[0, ip] = 1.0

        if y - 1 >= 0:
            shift[2 * (y - 1) + 1, im] = 1.0
        else:
            shift[2 * (n_sites - 1) + 1, im] = 1.0

    return shift @ coin


def allowed_k(n_sites: int) -> np.ndarray:
    """Discrete momenta for the periodic lattice, mapped to [-pi, pi)."""
    k = 2.0 * np.pi * np.arange(n_sites, dtype=float) / float(n_sites)
    k[k >= np.pi] -= 2.0 * np.pi
    return np.sort(k)


def analytic_positive_branch(k: np.ndarray, theta: float) -> np.ndarray:
    arg = np.cos(theta) * np.cos(k)
    arg = np.clip(arg, -1.0, 1.0)
    return np.arccos(arg)


def linear_fit(x: np.ndarray, y: np.ndarray) -> FitResult:
    """Fit y = a + b x and return R^2."""
    a, b = np.linalg.lstsq(np.column_stack([np.ones_like(x), x]), y, rcond=None)[0]
    pred = a + b * x
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    ss_res = float(np.sum((y - pred) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    return FitResult("linear", r2, (float(a), float(b)))


def analyze_theta(theta: float) -> dict[str, float]:
    print("\n" + "=" * 72)
    print(f"theta = {theta:.3f}")
    print("=" * 72)

    U = build_chiral_unitary(N_SITES, theta)
    unitary_err = float(np.max(np.abs(U.conj().T @ U - np.eye(U.shape[0]))))
    print(f"unitarity max|U^†U - I| = {unitary_err:.3e}")

    numeric_phases = np.sort(np.angle(np.linalg.eigvals(U)))
    k_vals = allowed_k(N_SITES)
    e_pos = analytic_positive_branch(k_vals, theta)
    analytic_phases = np.sort(np.concatenate([e_pos, -e_pos]))

    phase_residuals = np.abs(numeric_phases - analytic_phases)
    print(
        "exact lattice spectrum residuals vs Bloch bands: "
        f"mean={phase_residuals.mean():.3e}, max={phase_residuals.max():.3e}"
    )

    print("\nfirst few Bloch modes")
    print(f"{'k':>10s}  {'E_num':>12s}  {'E_exact':>12s}  {'|ΔE|':>10s}")
    print(f"{'---':>10s}  {'---':>12s}  {'---':>12s}  {'---':>10s}")
    low_mask = (k_vals >= 0.0) & (k_vals <= np.pi / 3.0)
    low_k = k_vals[low_mask]
    low_E = e_pos[low_mask]
    for k, e_exact in zip(low_k[:8], low_E[:8], strict=False):
        print(f"{k:10.6f}  {e_exact:12.6f}  {e_exact:12.6f}  {0.0:10.2e}")

    # Low-k Klein-Gordon limit: fit E^2 = m^2 + c^2 k^2.
    x = low_k ** 2
    y = low_E ** 2
    m2, c2 = np.linalg.lstsq(np.column_stack([np.ones_like(x), x]), y, rcond=None)[0]
    pred_kg = m2 + c2 * x
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    ss_res = float(np.sum((y - pred_kg) ** 2))
    r2_kg = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    # Competing low-k fits on the same data.
    fit_sch = linear_fit(x, low_E)
    fit_lin = linear_fit(np.abs(low_k), low_E)

    m_exact_sq = 2.0 * (1.0 - math.cos(theta))
    c_exact_sq = math.cos(theta)
    print("\nlow-k continuum fits on the positive branch")
    print(f"KG fit:        E^2 = {m2:.6f} + {c2:.6f} k^2   (R^2={r2_kg:.8f})")
    print(f"Schrodinger:   E   = {fit_sch.params[0]:.6f} + {fit_sch.params[1]:.6f} k^2   (R^2={fit_sch.r2:.8f})")
    print(f"Linear:        E   = {fit_lin.params[0]:.6f} + {fit_lin.params[1]:.6f} |k|   (R^2={fit_lin.r2:.8f})")
    print(
        "Taylor exact:  E^2 = "
        f"{m_exact_sq:.6f} + {c_exact_sq:.6f} k^2, "
        f"m_eff={math.sqrt(m_exact_sq):.6f}, c_eff={math.sqrt(c_exact_sq):.6f}"
    )
    print(
        "small-theta:   m_eff -> theta, c_eff -> 1  "
        f"(theta={theta:.6f})"
    )

    winner = max(
        [("KG", r2_kg), ("Schrodinger", fit_sch.r2), ("Linear", fit_lin.r2)],
        key=lambda item: item[1],
    )[0]
    print(f"best low-k fit: {winner}")

    return {
        "theta": theta,
        "unitary_err": unitary_err,
        "phase_residual_mean": float(phase_residuals.mean()),
        "phase_residual_max": float(phase_residuals.max()),
        "r2_kg": r2_kg,
        "r2_sch": fit_sch.r2,
        "r2_lin": fit_lin.r2,
    }


def main() -> None:
    print("=" * 72)
    print("FRONTIER: CHIRAL WALK DISPERSION RELATION")
    print("=" * 72)
    print(f"sites = {N_SITES} (periodic)")
    print("analytic relation: cos(E) = cos(theta) * cos(k)")
    print("continuum limit: E^2 = 2(1-cos(theta)) + cos(theta) k^2 + O(k^4)")
    print("small-theta limit: E^2 ≈ theta^2 + k^2")

    results = [analyze_theta(theta) for theta in THETAS]

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    all_exact = all(r["phase_residual_max"] < 1e-12 for r in results)
    all_kg = all(r["r2_kg"] > r["r2_sch"] and r["r2_kg"] > r["r2_lin"] for r in results)
    print(f"exact Bloch spectrum confirmed: {'YES' if all_exact else 'NO'}")
    print(f"low-k KG fit best on all angles: {'YES' if all_kg else 'MIXED'}")
    for r in results:
        print(
            f"theta={r['theta']:.1f}: residual_max={r['phase_residual_max']:.3e}, "
            f"R2(KG)={r['r2_kg']:.8f}, R2(Sch)={r['r2_sch']:.8f}, R2(Lin)={r['r2_lin']:.8f}"
        )


if __name__ == "__main__":
    main()
