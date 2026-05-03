#!/usr/bin/env python3
"""
SU(3) Wilson lattice gauge theory: minimal Metropolis Monte Carlo.

Purpose:
  Generate <P>(beta) data at multiple beta values to invert the framework's
  reduction law P_L(beta) = P_1plaq(beta_eff(beta)) numerically and Pade-resum
  the onset jet at beta = 6.

Implementation:
  - L^4 periodic lattice with L = 3 (81 sites, 324 links)
  - SU(3) link variables stored as 3x3 complex matrices
  - Metropolis update with small random SU(3) perturbation per link
  - Plaquette observable P = (1/(3 N_plaq)) sum_p Re Tr(U_p)

This is class (B) numerical: results have MC statistical error, not analytic.
The point is to invert the framework's reduction law at multiple beta values
to expose the higher-order onset-jet structure that the framework's
order-beta^5 jet alone cannot reach.

Estimated runtime: ~2-5 minutes per beta value with 5000 sweeps + 1000 therm.
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np


# =============================================================================
# SU(3) algebra utilities
# =============================================================================

def random_hermitian_traceless(rng: np.random.Generator) -> np.ndarray:
    """Random Hermitian traceless 3x3 matrix (Lie algebra of SU(3))."""
    # 8-parameter Gell-Mann decomposition; sample isotropically
    h = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    h = (h + h.conj().T) / 2  # Hermitian
    h -= np.trace(h) / 3 * np.eye(3)  # traceless
    return h


def expmh(a: np.ndarray) -> np.ndarray:
    """Matrix exponential of i * (Hermitian traceless) -> SU(3) element.
    Uses scipy's expm via series for small matrices. We just call scipy here.
    """
    from scipy.linalg import expm
    return expm(1j * a)


def project_su3(m: np.ndarray) -> np.ndarray:
    """Project a 3x3 matrix back onto SU(3) via QR, then det normalization.
    Used periodically to control numerical drift.
    """
    q, r = np.linalg.qr(m)
    d = np.diag(np.diag(r) / np.abs(np.diag(r)))
    q = q @ d
    det = np.linalg.det(q)
    q[:, 0] /= det ** (1 / 3)
    q[:, 1] /= det ** (1 / 3)
    q[:, 2] /= det ** (1 / 3)
    return q


# =============================================================================
# Lattice geometry
# =============================================================================

def make_lattice(L: int, rng: np.random.Generator, hot: bool = False) -> np.ndarray:
    """Create L^4 lattice of SU(3) link variables.

    Shape: (L, L, L, L, 4, 3, 3) - four spatial sites, four directions, 3x3 matrix.
    """
    if hot:
        u = np.zeros((L, L, L, L, 4, 3, 3), dtype=complex)
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        for mu in range(4):
                            h = random_hermitian_traceless(rng) * 0.5
                            u[x0, x1, x2, x3, mu] = expmh(h)
    else:
        # Cold start: all identity
        u = np.zeros((L, L, L, L, 4, 3, 3), dtype=complex)
        eye = np.eye(3, dtype=complex)
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        for mu in range(4):
                            u[x0, x1, x2, x3, mu] = eye
    return u


def staple_sum(u: np.ndarray, x: tuple, mu: int, L: int) -> np.ndarray:
    """Sum of staples around link U_mu(x).

    staple = sum over nu != mu of:
      U_nu(x) U_mu(x + nu_hat) U_nu^dag(x + mu_hat)  [forward staple]
      + U_nu^dag(x - nu_hat) U_mu(x - nu_hat) U_nu(x - nu_hat + mu_hat)  [backward]
    """
    s = np.zeros((3, 3), dtype=complex)
    x = list(x)
    for nu in range(4):
        if nu == mu:
            continue
        # Forward staple: U_nu(x) U_mu(x+nu) U_nu^dag(x+mu)
        x_plus_nu = list(x); x_plus_nu[nu] = (x_plus_nu[nu] + 1) % L
        x_plus_mu = list(x); x_plus_mu[mu] = (x_plus_mu[mu] + 1) % L
        u_nu_x = u[x[0], x[1], x[2], x[3], nu]
        u_mu_xpnu = u[x_plus_nu[0], x_plus_nu[1], x_plus_nu[2], x_plus_nu[3], mu]
        u_nu_xpmu = u[x_plus_mu[0], x_plus_mu[1], x_plus_mu[2], x_plus_mu[3], nu]
        s += u_nu_x @ u_mu_xpnu @ u_nu_xpmu.conj().T

        # Backward staple: U_nu^dag(x-nu) U_mu(x-nu) U_nu(x-nu+mu)
        x_minus_nu = list(x); x_minus_nu[nu] = (x_minus_nu[nu] - 1) % L
        x_mn_pm = list(x_minus_nu); x_mn_pm[mu] = (x_mn_pm[mu] + 1) % L
        u_nu_xmnu = u[x_minus_nu[0], x_minus_nu[1], x_minus_nu[2], x_minus_nu[3], nu]
        u_mu_xmnu = u[x_minus_nu[0], x_minus_nu[1], x_minus_nu[2], x_minus_nu[3], mu]
        u_nu_xmnpm = u[x_mn_pm[0], x_mn_pm[1], x_mn_pm[2], x_mn_pm[3], nu]
        s += u_nu_xmnu.conj().T @ u_mu_xmnu @ u_nu_xmnpm
    return s


def total_plaquette(u: np.ndarray, L: int) -> float:
    """Compute the plaquette average (1/(3 N_plaq)) sum_p Re Tr(U_p)."""
    total = 0.0
    n_plaq = 0
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(4):
                        for nu in range(mu + 1, 4):
                            x_pm = [x0, x1, x2, x3]; x_pm[mu] = (x_pm[mu] + 1) % L
                            x_pn = [x0, x1, x2, x3]; x_pn[nu] = (x_pn[nu] + 1) % L
                            u_mu_x = u[x0, x1, x2, x3, mu]
                            u_nu_xpm = u[x_pm[0], x_pm[1], x_pm[2], x_pm[3], nu]
                            u_mu_xpn = u[x_pn[0], x_pn[1], x_pn[2], x_pn[3], mu]
                            u_nu_x = u[x0, x1, x2, x3, nu]
                            plaq = u_mu_x @ u_nu_xpm @ u_mu_xpn.conj().T @ u_nu_x.conj().T
                            total += np.trace(plaq).real / 3.0
                            n_plaq += 1
    return total / n_plaq


# =============================================================================
# Metropolis update
# =============================================================================

def metropolis_update_link(u: np.ndarray, x: tuple, mu: int, L: int,
                           beta: float, eps: float,
                           rng: np.random.Generator,
                           n_hits: int = 5) -> int:
    """Update link U_mu(x) with n_hits Metropolis trials. Returns # accepted."""
    s = staple_sum(u, x, mu, L)
    u_old = u[x[0], x[1], x[2], x[3], mu].copy()
    n_accept = 0
    for _ in range(n_hits):
        # Propose small random rotation
        h = random_hermitian_traceless(rng) * eps
        delta = expmh(h)
        u_new = delta @ u_old
        # Action change: dS = -(beta/3) Re Tr((u_new - u_old) S^dag)
        dS = -(beta / 3.0) * np.trace((u_new - u_old) @ s.conj().T).real
        if dS < 0 or rng.random() < math.exp(-dS):
            u_old = u_new
            n_accept += 1
    u[x[0], x[1], x[2], x[3], mu] = u_old
    return n_accept


def metropolis_sweep(u: np.ndarray, L: int, beta: float, eps: float,
                     rng: np.random.Generator, n_hits: int = 5) -> float:
    """One sweep over all links. Returns acceptance rate."""
    total = 0
    n_total = 0
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(4):
                        total += metropolis_update_link(
                            u, (x0, x1, x2, x3), mu, L, beta, eps, rng, n_hits=n_hits
                        )
                        n_total += n_hits
    return total / n_total


# =============================================================================
# Main runner
# =============================================================================

def run_beta(L: int, beta: float, n_therm: int, n_meas: int,
             eps: float, rng: np.random.Generator,
             measure_every: int = 5) -> tuple[float, float, float]:
    """Run MC at given beta. Returns (mean_P, std_P, accept_rate)."""
    u = make_lattice(L, rng, hot=False)
    # Thermalize
    accept = 0.0
    for s in range(n_therm):
        accept += metropolis_sweep(u, L, beta, eps, rng)
    # Measure
    measurements = []
    for s in range(n_meas):
        accept += metropolis_sweep(u, L, beta, eps, rng)
        if s % measure_every == 0:
            p = total_plaquette(u, L)
            measurements.append(p)
    measurements = np.array(measurements)
    mean = measurements.mean()
    # Naive error (no autocorrelation correction; bin later if needed)
    std = measurements.std() / math.sqrt(len(measurements))
    accept_rate = accept / (n_therm + n_meas)
    return mean, std, accept_rate


def main() -> int:
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    n_therm = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    n_meas = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    eps = 0.3  # Metropolis step size

    print(f"SU(3) Wilson MC: L = {L}^4, n_therm = {n_therm}, n_meas = {n_meas}, eps = {eps}")
    print("=" * 78)

    rng = np.random.default_rng(seed=42)

    # beta values to scan
    betas = [4.0, 4.5, 5.0, 5.5, 5.7, 5.85, 6.0, 6.2, 6.5, 7.0, 8.0]

    print(f"{'beta':>8s}  {'<P>':>10s}  {'std':>9s}  {'accept':>8s}  {'time(s)':>9s}")
    print("-" * 78)

    results = {}
    for beta in betas:
        t0 = time.time()
        mean, std, accept = run_beta(L, beta, n_therm, n_meas, eps, rng)
        elapsed = time.time() - t0
        results[beta] = (mean, std)
        print(f"{beta:>8.2f}  {mean:>10.6f}  {std:>9.6f}  {accept:>7.2%}  {elapsed:>9.1f}")

    print("-" * 78)
    print("\n## Reduction-law inversion: beta_eff(beta) such that P_1plaq(beta_eff) = <P>(beta)")

    # Use the Haar-integration P_1plaq from the kernel
    # We'll re-import the function rather than duplicate code
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
    from frontier_hierarchy_route_1b_haar_evaluation import p_1plaq
    from scipy.optimize import brentq

    print(f"\n{'beta':>8s}  {'<P>(beta)':>11s}  {'beta_eff':>10s}  {'beta_eff - beta':>16s}")
    print("-" * 78)

    beta_eff_data = []
    for beta in betas:
        target = results[beta][0]

        def root_fn(b):
            return p_1plaq(b, n=64) - target

        try:
            # Bracket
            lo, hi = 0.5, 50.0
            beta_eff = brentq(root_fn, lo, hi, xtol=1e-4)
            beta_eff_data.append((beta, beta_eff, target))
            print(f"{beta:>8.2f}  {target:>11.6f}  {beta_eff:>10.4f}  {beta_eff - beta:>+16.4f}")
        except ValueError as e:
            print(f"{beta:>8.2f}  {target:>11.6f}  inversion failed: {e}")

    # Save data for downstream Pade analysis
    out_path = "/tmp/wilson_mc_beta_eff.npz"
    np.savez(out_path, betas=np.array([b for b, _, _ in beta_eff_data]),
             beta_effs=np.array([be for _, be, _ in beta_eff_data]),
             plaqs=np.array([p for _, _, p in beta_eff_data]))
    print(f"\nData saved: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
